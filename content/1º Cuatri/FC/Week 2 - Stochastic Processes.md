### I. Previos
#### 1. Carga de Librerías 
> En este caso añadiremos la librería ML-Tools a través de un .zip seleccionando esa opción en `Install Packages`.
> Aparte, importaremos la librería *`lmtest`*, esta se usa para aplicar pruebas estadísticas que ayudan a evaluar y diagnosticar modelos de regresión y series temporales. En concreto, la función *`coeftest()`* nos servirá para contrastar la significancia estadística de los coeficientes de un modelo, mostrando sus estimaciones junto con errores estándar, valores t y p-valores.
```r
# Librerías
library(MLTools)
library(fpp2)
library(tidyverse)
library(readxl)
library(lmtest) 
```
#### 2. Directorio
> Igual que en [[Week 1 - Decomposition Methods]]
```r
# Setear el Directorio
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
```

### II. Ruido Blanco
> [!note] 
> Para esta asignatura es muy importante distinguir entre los términos:
> 	- Estacionario (Stationary), sus propiedades estadísticas (media, varianza, autocorrelaciones) **no dependen del tiempo**.
> 	- Estacional (Seasonal), se refiere a patrones que se repiten en **periodos de tiempo fijos**.
#### 1. Definición
> Un **Proceso de Ruido Blanco** es una secuencia de variables aleatorias:
> 	- No correlacionadas entre sí (no hay memoria, cada valor es independiente de los anteriores).
> 	- Con media cero. \*
> 	- Con varianza constante (homocedasticidad). \*
> 		\* Esto hace que un proceso de Ruido Blanco sea *estacionario* 
> 	- Si además cada valor sigue una distribución normal, hablamos de ruido blanco gaussiano.
> Formalmente:
> 	$\{ \varepsilon_t \} \sim WN(0, \sigma^2) \quad \text{con} \quad E[\varepsilon_t] = 0, \quad Var(\varepsilon_t) = \sigma^2, \quad Cov(\varepsilon_t, \varepsilon_{t'} ) = 0 \ \forall t \neq t'$

#### 2. Uso
> El ruido blanco representa la parte impredecible de una serie temporal. Todo buen modelo debe reducir la serie observada hasta un residuo que sea indistinguible de ruido blanco.
###### 2.1. Ruido Puro o Base de Comparación
> El ruido blanco es la referencia de una serie sin estructura.
> Si un modelo ajustado deja residuos que se comportan como ruido blanco, eso significa que el modelo ha capturado toda la información sistemática de la serie (tendencia, estacionalidad, correlaciones).
###### 2.2. Componente de los Modelos ARMA/ARIMA
> En los modelos estocásticos, el ruido blanco es la parte impredecible.
> Por ejemplo:  $Y_t = \phi Y_{t-1} + \varepsilon_t,$  aquí, $\varepsilon_t$ es ruido blanco: el “shock” o innovación en el sistema.

2.3. Diagnóstico de Modelos
> Una vez ajustado un modelo ARIMA o de suavizado exponencial, se comprueba que los residuos sean ruido blanco.
> Si no lo son (si muestran autocorrelación), el modelo está mal especificado.
###### 2.4. Simulación y Pruebas
> Se usa ruido blanco para simular series y comprobar el comportamiento de métodos de pronóstico.
>  También como input en procesos ARMA para generar datos artificiales.

###### 2.5. Gaussiano vs No Gaussiano
> - **Gaussiano**: cada $\varepsilon_t$ sigue una Normal(0,σ²). Esto es útil porque facilita inferencia estadística y resultados asintóticos.
> - **No gaussiano**: mantiene independencia y varianza constante, pero con otra distribución (ej. uniforme, t-Student). Se sigue considerando ruido blanco, pero las propiedades de los estimadores cambian.
#### 3. Creación
> Para crear una serie temporal de ruido blanco gaussiano obtenemos una muestra de n valores aleatorios de una distribución normal estándar, y se lo asignamos a un objeto ts.
```r
# 1. Muestra Aleatoria
n <- 150
z <- rnorm(n, mean = 0, sd = 1) 

# 2. Objeto ts
w <- ts(z)
```
#### 4. Visualización 
> Nos sirve para comprobar que no hay patrones ni correlaciones, confirmando que se trata solo de fluctuaciones aleatorias.
```r
# 1. Solo Valores Numéricos
head(w, 25)

# 2. Gráfica de la Serie
autoplot(w) +
  ggtitle("White noise") + 
  geom_point(aes(x = 1:n, y = z), size=1.5, col="blue")
```
#### 5. ACF & PACF de Ruido Blanco
> Esta es otra manera de comprobar que una serie se comporta como ruido blanco, es decir, que no tiene patrones ni correlaciones aprovechables para el modelado. 
> - **`ACF`**: Auto Correlation Function, mide la correlación entre la serie y sus rezagos (valores pasados).
> En un proceso de ruido blanco, todas las autocorrelaciones (excepto en el lag 0) deberían ser ≈ 0. Las barras negras son las correlaciones observadas en tu muestra, y las líneas azules marcan el intervalo de confianza (aprox. $\pm \dfrac{2}{\sqrt{n}}$).  
> 	Si las barras caen dentro de esas bandas, no hay evidencia de correlación significativa, que es lo esperado en ruido blanco.
> - **`PACF`**: Partial Auto Correlation Function, mide la correlación entre la serie y sus rezagos, eliminando la influencia de los rezagos intermedios. Para ruido blanco, también debería dar ≈ 0 en todos los lags. Igual que en la ACF, vemos que ninguna barra sobresale de las bandas azules, lo que confirma que no hay estructura.
> 
> 	*`Nota`*: `lag` significa cuántos pasos atrás en el tiempo miramos para comparar la serie consigo misma. 
> 		- lag 1: comparo el valor en t con el valor en t−1.
> 		- lag 2: comparo el valor en t con el de t−2.
> 		- Y así sucesivamente.
> 	El `lag 0` es la serie comparada consigo misma, que por definición la correlación siempre es 1.
```r
# Plot Triple de la Serie del Ruido, su ACF y su PACF
ggtsdisplay(w, lag.max = 20)
```

### III. Random Walks
#### 1. Definición
> Un **Random Walk (RW)** es un proceso estocástico donde el valor actual es la suma del valor anterior más un término de ruido blanco:
> 	$Y_t = Y_{t-1} + w_t, \quad w_t \sim WN(0,\sigma^2)$
> Forma de un Random Walk con drift:  $Y_t = k + Y_{t-1} + w_t​​,$  donde k es la constante de drift, la cual es responsable del crecimiento o decrecimiento promedio (k > 0 o k < 0).
> - Cada paso se construye a partir del anterior.
> - La innovación ($\varepsilon_t$​) es impredecible, por lo que introduce aleatoriedad.
> - No tiene media constante ni varianza constante, por lo que no es estacionario, cambia con el tiempo. En el caso de la varianza, es creciente /  $Var(Y_t) = t \cdot \sigma^2$
> Intuitivamente: imagina una persona que da pasos al azar en una línea recta. No sabemos hacia dónde va en el futuro, solo sabemos dónde está ahora y que su próximo paso será aleatorio.
#### 2. Uso
> Un random walk representa procesos donde el futuro depende solo del presente más un shock aleatorio. Su única memoria es su último paso, y es la base del modelo ingenuo de predicción.
###### 2.1. Modelo Base en Finanzas
> Se usa mucho para modelar precios de acciones o divisas. Los precios siguen un random walk, estos no se pueden predecir a partir de los datos pasados.
###### 2.2. Referencia para Pronósticos
> El random walk es equivalente al método ingenuo (naive forecast):
> 	$\hat{Y}_{t+1} = Y_t$
> Es decir, el mejor pronóstico para mañana es simplemente el valor de hoy.
#### 3. Creación
> Para crear una serie temporal de ruido blanco gaussiano obtenemos la suma acumulada de una muestra de n valores aleatorios de una distribución normal estándar (con o sin constante de drift), y se lo asignamos a un objeto ts. Usaremos `set.seed` para que cada vez que ejecutemos el código obtengamos el mismo resultado, esto es imprescindible para la reproducibilidad.
```r
# 1. Muestra Aleatoria
n = 1000
set.seed(2024)
w = 10 * rnorm(n)

# 2. Constante de Drift
k = 0.1

# 3. Objeto ts
rw_ts = ts(k * (1:n)  + cumsum(w))
```
#### 4. Visualización
> Nos sirve para apreciar cómo los shocks aleatorios acumulados generan trayectorias con tendencia aparente y varianza creciente, a diferencia del ruido blanco.
```r
# Gráfica de la Serie
autoplot(rw_ts) +
  ggtitle("Random walk with drift") 
```
#### 5. ACF & PACF de Random Walk
> En un random walk, a diferencia del ruido blanco, sí aparecen correlaciones que reflejan la fuerte dependencia con el valor inmediatamente anterior.
> - **`ACF`**: muestra una decadencia lenta (no se corta bruscamente), lo que indica que los valores están altamente correlacionados con muchos rezagos. Esta persistencia en la autocorrelación es lo que delata que la serie  no es estacionaria.
> - **`PACF`**: suele tener un pico muy alto en el `lag 1` (ya que cada valor depende directamente del anterior), pero después las correlaciones parciales se reducen rápidamente.
> 	*`Idea clave`*: Mientras que el ruido blanco tiene una ACF y PACF planas, el random walk presenta autocorrelaciones persistentes en la ACF y un corte claro en el primer lag de la PACF.
```r
# Plot Triple de la Serie del Random Walk, su ACF y su PACF
ggtsdisplay(rw_ts, lag.max = 50)
```

### IV. ACF & PACF de Series Estacionales
#### 1. Uso
> Nos sirve para detectar y cuantificar la estacionalidad (y la no-estacionariedad asociada) en una serie temporal. La forma de la ACF y la PACF revela el periodo estacional (por ejemplo 12 meses) y da pistas para identificar modelos SARIMA y/o aplicar diferenciación regular/estacional y transformaciones.
#### 2. Pasos a Seguir
> Método para aplicar ACF y PACF a una serie estacional paso a paso.
###### 2.1. Graficar la Serie Temporal
> Se ve la tendencia creciente de la serie y los posibles picos repetidos cada periodo estacional.
```r
# PLot de la Serie
autoplot(AirPassengers)
```
###### 2.2. Graficar el ACF y PACF
> Usamos `ggtsdisplay` para obtener el gráfico de la serie con su ACF y PACF.
```r
# Plot Triple de la Serie del Random Walk, su ACF y su PACF
ggtsdisplay(AirPassengers)
```
###### 2.3. Valores Individuales
> Fijando el periodo estacional visto en el primer punto, nos sirve para reportar magnitudes exactas.
```r
# 1. Periodo Estacional
sp = 12

# 2. Tabla Numérica de Autocorrelaciones
Acf(AirPassengers,lag.max = 2 * sp, plot = FALSE)
```
###### 2.4. Lag Plots
> Dispersogramas de la serie contra sus lags. Las nubes alineadas (o no) confirman (o no) fuerte dependencia y permiten (o no) visualizar la estacionalidad (patrones que se repiten en ciertos lags).
```r
# Plot
gglagplot(AirPassengers, seasonal = FALSE, do.lines = FALSE, colour = FALSE)
```
###### 2.5. Comparativa de la Serie Original con un Lag
> Este paso es una comprobación visual de la autocorrelación. En lugar de mirar solo la ACF numérica, se ven dos series casi paralelas (original y rezagada). Para series estacionales, si eliges   k = 12, la similitud es aún más evidente, porque la estacionalidad se repite cada año.
> En resumen, este bloque grafica la serie junto con una copia desplazada k pasos atrás, para visualizar la autocorrelación directamente.
```r
# 1. Escoger el Lag y Definir la Serie
k <- 7
lagged <- stats::lag(AirPassengers, k)

# Definir la Serie Conjunta
AirPassengers_lag <- cbind(Original = AirPassengers, lagged = lagged)
head(AirPassengers_lag, k + 2)

# PLot Conjunto
ts.plot(AirPassengers_lag,
        lty = 1:2,
        main = "AirPassengers and lagged Series", 
        ylab = "Passengers", xlab = "Time")
legend("topleft", legend = c("Original", "lagged"), 
       lty = 1:2)
```

### V. Introducción a los Modelos ARMA
#### 1. Pasos 0
> Cargar, preparar y visualizar la serie antes de entrenar el modelo para detectar patrones de autocorrelación que orienten la elección inicial del orden del ARMA.
```r
# 1. Carga de Datos
fdata <- read_excel("ARMA_series.xls")

# 2. Objeto ts y Primer Vistazo
fdata_ts <- ts(fdata)
head(fdata_ts)

# 3. ACF y PACF de la Serie
ggtsdisplay(y, lag.max = 20)
```
#### 2. Entrenamiento del Modelo
> Se entrena un modelo ARIMA sobre la serie de datos, especificando el orden estimado (p,d,q). Posteriormente se revisa el resumen del ajuste, que incluye los coeficientes estimados, su significancia y las medidas de error del entrenamiento. Finalmente, se contrasta de manera explícita la significancia estadística de los coeficientes mediante un test adicional. 
> Si los residuos no son ruido blanco o los pronósticos muestran sesgo, es necesario reajustar el modelo con un orden diferente.
```r
# 1. Entrenamiento con un Orden Estimado de un ARMA(1,1)
arima.fit <- Arima(y, order=c(1,0,1), include.mean = TRUE)

# 2. Resumen de los Errores de Training y Coeficientes Estimados
summary(arima.fit) 

# 3. Significancia Estadística de los Coeficientes Estimados
coeftest(arima.fit)
```
#### 3. Visualización del Modelo
> Nos sirve para analizar gráficamente los resultados del modelo ARIMA ajustado. Se incluyen representaciones del modelo, la validación de residuos, la comparación entre valores reales y ajustados, la simulación de series con parámetros dados, y la proyección de pronósticos.
```r
# 1. Plot Modelo Ajustado
autoplot(arima.fit)  

# 2. Diagnóstico de Residuos (Se comporta como ruido blanco?)
CheckResiduals.ICAI(arima.fit, bins = 100, lags = 20)

# 3. ACF y PACF de los Residuos (Adecuación del modelo)
ggtsdisplay(residuals(arima.fit), lag.max = 20)
# Si los residuos no son ruido blanco, cambiar el orden del ARMA

# 4. Comparativa Serie Real y los Valores Ajustados
autoplot(y, series = "Real") +
  forecast::autolayer(arima.fit$fitted, series = "Fitted")
  
# 5. Simulación de una Nueva Serie Temporal ARMA con Parámetros Dados
sim_ts <- arima.sim(n = 250,
                 list(ar = c(0.8897, -0.4858), ma = c(-0.2279, 0.2488)),
                 sd = sqrt(0.1796))
                 
# 6. Pronóstico a 5 Pasos Usando el Modelo Entrenado
y_est <- forecast::forecast(arima.fit, h=5)
autoplot(y_est)
```

Los apuntes continúan en [[Week 3 - ARMA Processes]]


