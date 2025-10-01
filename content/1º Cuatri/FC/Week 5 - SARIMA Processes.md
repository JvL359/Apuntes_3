### I. Previos
#### 1. Carga de Librerías
> Además de las usadas en semanas anteriores, aquí se añade **`TSstudio`**, que la usaremos para dividir la serie en train/test respetando el orden temporal mediante *`ts_split()`*.
```r
# Librerías
library(MLTools)
library(fpp2)
library(readxl)
library(tidyverse)
library(TSstudio)
library(lmtest)
library(tseries)
```
#### 2. Directorio
> Paso idéntico al de las clases anteriores.
```r
# Setear el Directorio
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
```

### II. Datos
#### 1. Carga y Procesamiento de Datos
> Cargamos el dataset de matriculaciones de coches desde un archivo Excel y realizamos un procesado inicial. Esto incluye:
> 	- Convertir la columna de fechas a formato `Date` en R para poder trabajar con series temporales.
> 	- Ordenar los registros cronológicamente para asegurar consistencia.
> 	- Revisar si existen **huecos** en la secuencia temporal (comparamos con una secuencia completa de meses).
> 	- Comprobar si hay fechas duplicadas o valores faltantes (`NA`) en la columna de interés.  
> Estos pasos garantizan que la serie está limpia antes de convertirla en un objeto `ts`.
```r
# 1. Carga y Primera Visualización
fdata <- read_excel("CarRegistrations.xls")
head(fdata)

# 2. Formato Date y Ordenar
fdata$Fecha <- as.Date(fdata$Fecha, format = "%d/%m/%Y")
fdata <- arrange(fdata, Fecha)
head(fdata)

# 3. Valores Ausentes
valMin <- min(fdata$Fecha)
valMax <- max(fdata$Fecha)
date_range <- seq.Date(valMin, valMax, by = "months")
setdiff(date_range, fdata$Fecha)

# 4. Valores Duplicados
fdata[duplicated(fdata$Fecha), ]
  
# 5. Valores NA
sum(is.na(fdata$CarReg))
```
#### 2. Conversión a un Objeto Serie Temporal
> Una vez validada la serie, la transformamos en un objeto `ts`, que es el formato estándar en R para series temporales. Definimos la frecuencia como `12` porque los datos son mensuales e indicamos la fecha de inicio en vector `c(1960, 1)`, lo que corresponde a enero de 1960. Por último lo graficamos para observar el comportamiento general de la serie.
```r
# 1. Objeto Serie Temporal
freq <- 12
start_date  <-  c(1960, 1)
y <- ts(fdata$CarReg, start = start_date, frequency = freq)

# 2. Plot
autoplot(y) +
  ggtitle("Car registrations") +
  xlab("Year") + ylab("Number registered (thousands)")
```

### III. Train-Test Split
#### 1. Método
> En el pronóstico de series temporales no podemos dividir los datos al azar como en problemas de machine learning clásicos, porque romperíamos la dependencia temporal.  
> En su lugar, separamos los últimos 5 años de observaciones como conjunto de validación/test, y el resto lo usamos para entrenamiento.  
> Existen varias formas de hacerlo:
> 	- Con la función *`ts_split()`* del paquete `TSstudio`, que automatiza la separación.
> 	- Con *`subset()`*, indicando directamente los índices de inicio y fin de cada subconjunto.
> 	- Con *`head()`* y *`tail()`*, extrayendo manualmente las observaciones de train y test.  
> Una vez realizada la división, es buena práctica visualizar ambas series en un mismo gráfico para verificar que el corte temporal es correcto.
```r
# 1.1. Opción 1
n_test <- floor(5 * freq)
y_split <- ts_split(y, sample.out = n_test)
y_TR <- y_split$train
y_TV <- y_split$test

# 1.2. Opción 2
y_TR <- subset(y, end = length(y) - 5 * 12) 
y_TV <- subset(y, start = length(y) - 5 * 12 + 1)

# 1.3. Opción 3
y_TR <- head(y, length(y) - 5 * 12) 
y_TV <- tail(y, 5 * 12) 

# 2. Vistazo de la División
tail(y_TR)
head(y_TV)

# Plot de la División
autoplot(y_TR, color = "orange") + 
  autolayer(y_TV, color = "blue")
```
#### 2. Qué Hacer si no Sabemos la Proporción de la División
> En algunos datasets no se indica claramente la **frecuencia de muestreo**. En ese caso:
> 	1. Primero graficamos la serie completa, aunque puede salir borrosa si es muy larga.
>     2. Después analizamos la ACF (Función de Autocorrelación) para detectar picos significativos en rezagos regulares. Estos picos marcan el periodo estacional de la serie (por ejemplo, un pico en los lag 24 y 48 sugiere periodicidad de 24 observaciones).
>     3. Una vez identificada la frecuencia, podemos marcarla en el gráfico y usarla como parámetro `freq`.
>     4. Por último, aplicamos una diferenciación estacional con esa frecuencia para eliminar el patrón repetitivo y dejar la serie más cercana a la estacionariedad.
```r
# 1. Carga de Archivo Auxiliar
fdata2 <- ts(read.table("fdata2.dat", sep = ""))

# 2. Plot Triple de la Serie, su ACF y su PACF
ggtsdisplay(fdata2, lag.max = 80)

# 3. Marcado de los Valores Significativos
freq <- 24
ggAcf(fdata2, lag.max = 80)+
  geom_vline(xintercept = (1:4) * freq, color = "green", alpha = 0.25, size=2)
  
# 4. Plot Triple de la Serie Diferenciada, su ACF y su PACF
ggtsdisplay(diff(fdata2, lag = freq), lag.max = 5 * freq)
```

### IV. Identificación SARIMA y Ajuste del Modelo
#### 0. Estructura SARIMA $(p,d,q)(P,D,Q)_s$
> Un modelo SARIMA (Seasonal ARIMA) combina componentes no estacionales y estacionales:
> 	1.  **$(p,d,q)$**: parte no estacional, igual que en un ARIMA clásico.
> 	- $p$: orden autorregresivo (nº de lags de $Y_t$ usados como predictores).
> 	- $d$: nº de diferencias regulares (para eliminar tendencia).
> 	- $q$: orden de medias móviles (nº de lags de los errores incluidos en el modelo).
> 	1. **$(P,D,Q)_s$**: parte estacional.
> 	- $P$: orden autorregresivo estacional (dependencia con el valor en $t-s$, $t-2s$, etc.).
> 	- $D$: nº de diferencias estacionales (por ejemplo, $Y_t - Y_{t-12}$ en datos mensuales).
> 	- $Q$: orden de medias móviles estacionales (errores en $t-s$, $t-2s$, etc.).
> 	- $s$: el periodo estacional de la serie (anual, trimestral, mensual, . . .).

> [!note] 
> - $d$ “borra” la **tendencia**.
> - $D$ “borra” la **estacionalidad repetida**.
> - $p,q$ capturan dependencias **cortas**.
> - $P,Q$ capturan dependencias **largas** ligadas a la estacionalidad.

> [!example] Ejemplo: **$SARIMA(1,1,1)(1,1,1)_{12}$​**
> 1. Aplica una diferencia regular ($d=1$) → quita tendencia. 
> 2. Aplica una diferencia estacional de orden 1 ($D=1$, $s=12$) → quita patrón anual.
> 3. Ajusta un ARMA(1,1) a la parte residual no estacional.
> 4. Añade un AR(1) y un MA(1) sobre los rezagos estacionales (lag 12).
#### 1. Transformación Box-Cox
> Antes de identificar el orden SARIMA conviene estabilizar la varianza si aumenta con el nivel de la serie. La transformación de Box–Cox (controlada por el parámetro $\lambda$) ayuda a que la serie se parezca más a estacionaria y a que ACF/PACF sean más interpretables.
> 	1. Estimamos $\lambda$ con el gráfico media–desviación (ventana de 12 por ser datos mensuales).
> 	2. Aplicamos la transformación con ese $\lambda$ (si $\lambda \approx 1$, la transformación no cambia la serie; si $\lambda = 0$, equivale a log⁡).
> 	3. Comparamos visualmente la serie transformada con la original para verificar que la heterocedasticidad se reduce.
```r
# 1. Estimar λ con el Gráfico Media–Desviación (ventana mensual)
Lambda <- BoxCox.lambda.plot(y_TR, window.width = 12)

# 2. Aplicar la Transformación Box-Cox Usando λ Óptimo
z <- BoxCox(y_TR, Lambda)

# 3. Comparar serie transformada (z) vs. original (train)
p1 <- autoplot(z) + ggtitle("Serie transformada (Box–Cox)")
p2 <- autoplot(y_TR) + ggtitle("Serie de entrenamiento")
gridExtra::grid.arrange(p1, p2, nrow = 2 )
```
#### 2. Diferenciación
> El objetivo es lograr estacionariedad en media con el menor número de diferencias posible. Procedemos en dos capas:
> 	- Revisar la no estacionalidad (tendencia) y aplicar diferencia regular si la ACF decae lentamente;
> 	- Revisar la estacionalidad y aplicar diferencia estacional si hay picos grandes en múltiplos de `freq`.  
> Importante evitar sobre-diferenciar: una señal típica de exceso es un gran pico negativo en la ACF en el lag 1 (≈ −0.5 a −1) y residuos muy ruidosos.
###### 1.1. Diagnóstico inicial con ACF/PACF
> Inspeccionamos `z` (tras Box–Cox) para decidir si necesita diferencias.  
> Hay que recordar que si la ACF disminuye muy lentamente, esto indica que la serie necesita una diferenciación regular. Un decaimiento lento y autocorrelaciones altas en los primeros rezagos son síntomas de la presencia de una raíz unitaria. Por otro lado, la aparición de picos repetidos en múltiplos de la frecuencia (`freq`) señala la existencia de estacionalidad, lo cual sugiere la necesidad de aplicar una diferenciación estacional.
```r
# 1. Plot Triple de la Serie Transformada (z), su ACF y su PACF, para decidir d y D
ggtsdisplay(z, lag.max = 100)
```
###### 1.2. Diferenciación Estacional
> Si la ACF muestra picos fuertes en `freq, 2*freq, 3*freq, …`, aplicamos una diferencia estacional de orden 1: $∇_s z_t = z_t − z_{t−s}$.  
> Tras esta operación, esos picos deberían disminuir notablemente; la serie pierde el patrón repetitivo y queda lista para evaluar si aún necesita diferencia regular.
```r
# 1. Diferencia estacional de orden 1 (s = freq)
B12z<- diff(z, lag = freq, differences = 1)

# 2. Plot Triple de la Serie tras DE, su ACF y su PACF
ggtsdisplay(B12z, lag.max = 4 * freq)
```
###### 1.3. Diferenciación Regular
> Si la ACF de `z` (o de `B12z` si ya quitaste la estacionalidad) sigue con decaimiento lento, aplica una diferencia regular: $∇ z_t = z_t − z_{t−1}$.  
> Después, la ACF debería recortarse más rápido; si aparece un gran pico negativo en lag 1, probablemente te has pasado de diferencias.
```r
# 1. Diferencia regular de orden 1 (eliminar tendencia)
Bz <- diff(z, differences = 1)

# 2. Plot Triple de la Serie tras DR, su ACF y su PACF
ggtsdisplay(Bz, lag.max = 4 * freq)
```
###### 1.4. Diferenciación Doble (Estacional y Regular)
> En muchas series mensuales, lo habitual es usar (d, D) = (1, 1): diferencia regular y estacional.
> El orden de aplicación no importa: $∇_s(∇ z_t) = ∇(∇_s z_t)$. Tras ambas, la serie debería verse “plana” y la ACF/PACF servirán para elegir (p, q)(P, Q).
```r
# 1. Ambas Diferencias: Regular y Estacional (orden 1 cada una) 
B12Bz <- diff(Bz, lag = freq, differences = 1) 

# 2. Plot Triple de la Serie tras DRE, su ACF y su PACF 
ggtsdisplay(B12Bz, lag.max = 4 * freq) 

# 3. Orden No Importa: Comparación Visual
B_B12z<- diff(B12z, differences = 1) 
autoplot(B12Bz, color = "blue", size = 2) + 
autolayer(B_B12z, color = "orange", size = 0.5)
```
###### 1.5. Comprobar Sobre-Diferenciación
> Para no aplicar más diferencias de las necesarias podemos usar funciones que nos dan una guía:
> 	- **`ndiffs(z)`**: recomienda el número mínimo de diferencias regulares necesarias para lograr estacionariedad.
> 	- **`nsdiffs(z, m = freq)`**: recomienda el número mínimo de diferencias estacionales necesarias.  
> Estas funciones se basan en contrastes de raíz unitaria, pero conviene validar visualmente con ACF/PACF y comprobar que la serie no está sobre-diferenciada (gran pico negativo en lag 1).
```r
# 1. Para Diferencias Regulares (d)
ndiffs(z) 

# 2. Para Diferencias Estacionales (D)
nsdiffs(z, m=freq) 
```
#### 3. Selección del Orden $(p, d, q)(P, D, Q)_s$ del Modelo
> Una vez aplicadas las transformaciones (Box–Cox y diferenciaciones), usamos la ACF/PACF de la serie resultante para proponer los órdenes del modelo SARIMA:
> 	1.  $p$ y $q$: se deducen de la parte no estacional.
> 	- Un pico significativo en la PACF en rezagos bajos sugiere un componente AR ($p$).
> 	- Un pico significativo en la ACF en rezagos bajos sugiere un componente MA ($q$).
> 	2. $P$ y $Q$: se deducen de la parte estacional, observando picos en múltiplos de la frecuencia ($s$).
> 	- Picos en la PACF en lags estacionales → AR estacional ($P$).
> 	- Picos en la ACF en lags estacionales → MA estacional ($Q$).
> 	1. $d$ y $D$: vienen determinados por las diferencias aplicadas previamente (regular y estacional).
> Como punto de partida, seleccionamos un modelo $SARIMA(0,1,1)(1,1,1)_{12}$, que suele ser un candidato razonable en series mensuales con fuerte estacionalidad. Este orden se ajustará y validará más adelante con criterios de información y diagnóstico de residuos.
```r
# Orden Propuesto SARIMA
p <- 0  # AR no estacional
d <- 1  # Diferencia regular
q <- 1  # MA no estacional

P <- 1  # AR estacional
D <- 1  # Diferencia estacional
Q <- 1  # MA estacional
```
#### 4. Ajustar el Modelo con el Orden Estimado
> Una vez fijados los parámetros $(p,d,q)(P,D,Q)_s$, ajustamos el modelo SARIMA sobre la serie de entrenamiento `y_TR`.
> 	- Usamos la función **`Arima()`** del paquete `forecast`.
> 	- Incluimos el parámetro **`lambda`** para aplicar la transformación Box–Cox dentro del ajuste.
> 	- Indicamos la frecuencia estacional (`period = freq`) y el orden estacional en la lista `seasonal`.
> 	- Ponemos `include.constant = FALSE` porque al aplicar diferenciación ya no se necesita intercepto en el modelo (evita redundancia).  
> Este ajuste nos permitirá obtener los coeficientes estimados y pasar a la fase de diagnóstico de residuos.
```r
# 'Rellenar aquí'
arima.fit <- Arima(y_TR,
                   order=c(p, d, q),
                   seasonal = list(order=c(P, D, Q), period=freq),
                   lambda = Lambda,
                   include.constant = FALSE)
```

### V. Diagnóstico del Modelo
> Tras ajustar el modelo, realizamos un diagnóstico completo para comprobar si es adecuado:
> 	1. **Resumen del ajuste**: con `summary()` vemos los coeficientes estimados, significancia, medidas de error y criterios de información (AIC, BIC).
> 	2. **Contraste de coeficientes**: con `coeftest()` verificamos estadísticamente si los parámetros son significativos.
> 	3. **Visualización del ajuste**: graficamos el modelo con `autoplot()`, que incluye la serie ajustada y residuos.
> 	4. **Diagnóstico de residuos**: usamos `CheckResiduals.ICAI()` para comprobar si los residuos se comportan como ruido blanco (sin autocorrelación, media cero, varianza constante).
> 	5. **Comparación valores reales vs. ajustados**: representamos la serie original junto con los valores ajustados para ver la calidad del fit en el conjunto de entrenamiento.
```r
# 1. Resumen del Modelo (coeficientes, errores y AIC/BIC)
summary(arima.fit)

# 2. Contraste de Significancia Estadística de los Coeficientes
coeftest(arima.fit)

# 3. Visualización del Modelo Ajustado
autoplot(arima.fit)

# 4. Diagnóstico de Residuos (¿se comportan como ruido blanco?)
CheckResiduals.ICAI(arima.fit, bins = 100, lags = 100)

# 5. Comparación Entre Valores Reales y Ajustados en Entrenamiento
autoplot(y_TR, series = "Real") +
  forecast::autolayer(arima.fit$fitted, series = "Fitted")
```

### VI. Pronóstico Futuro y Validación
#### 1. Pronóstico en el Conjunto de Entrenamiento
> Generamos pronósticos a 12 pasos adelante (un año en datos mensuales) usando el modelo ajustado.
> 	- La función **`forecast()`** nos da la media esperada y los intervalos de confianza.
> 	- Mostramos los primeros 12 valores previstos.
> 	- Para visualizar, representamos los últimos 30 puntos de la serie de entrenamiento junto con los pronósticos y sombreamos el periodo de validación en naranja para distinguirlo.
```r
# 1. Pronóstico a 12 Pasos con el Modelo SARIMA Ajustado
y_est <- forecast::forecast(y_TR, model = arima.fit, h = freq)
head(y_est$mean, n = 12)

# 2. Límites del Rectángulo de Validación
xmin <- 1995
xmax <- 1996
ymin <- 0
ymax <- Inf

# 3. Gráfico: Últimos 30 Puntos de Train + Predicción + Zona de Validación
autoplot(subset(y, start = length(y_TR) - 30, end = length(y_TR) + freq)) + 
autolayer(y_est, alpha = 0.5) +
annotate("rect", xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax,
        alpha = 0.2, fill = "orange")
```
#### 2. Validación Rolling Forecast (h = 1)
> Para evaluar la calidad de los pronósticos, no solo usamos el horizonte fijo de 12 pasos, sino que también hacemos una validación con horizonte 1 (rolling forecast):
> 	- Recorremos el periodo de validación y en cada paso entrenamos con los datos hasta $t-1$ para predecir $t$.
> 	- Guardamos estas predicciones en `y_TV_est`.
> 	- Así comparamos el pronóstico “directo” a 12 pasos (`y_est`, en azul) con el pronóstico iterativo de horizonte 1 (en rojo).
> 	- Por último, medimos el error de validación con métricas como RMSE, MAE, MAPE y confirmamos con un cálculo manual del RMSE.
```r
# 1. Inicializar Vector de Predicciones en Validación
y_TV_est <- y * NA

# Bucle Rolling: en cada paso predecimos 1 paso adelante (h=1)
for (i in seq(length(y_TR) + 1, length(y), 1)){
  y_TV_est[i] <- forecast::forecast(subset(y, end = i-1),
                                    model = arima.fit,
                                    h = 1)$mean
}

# 2. Comparación Gráfica: últimos 24 puntos de train + validación
autoplot(subset(y, start = length(y_TR) - 24, end = length(y_TR) + 12)) +
  forecast::autolayer(y_est$mean, color = "blue") +
  forecast::autolayer(subset(y_TV_est,
                             start = length(y_TR) + 1,
                             end   = length(y_TR) + 12),
                      color = "red")

# 3. Cálculo de Métricas de Error en Validación
accuracy(subset(y_TV_est, start = length(y_TR) + 1), y)

# 4. RMSE Directo
sqrt(mean((y_TV_est - y_TV)^2))
```
