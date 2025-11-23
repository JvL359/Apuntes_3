### I. Previos
#### 1. Carga de Librerías
> En esta semana añadimos las librerías de imputeTS, para tratamiento de valores perdidos, y la de lubridate para manejo de fechas y calendarios.
```r
library(MLTools)
library(fpp2)
library(ggplot2)
library(readxl)
library(tidyverse)
library(forecast)
library(TSA)
library(lmtest)      # contains coeftest function
library(tseries)     # contains adf.test function
library(Hmisc)       # for computing lagged variables
library(TSstudio)
library(astsa)
library(imputeTS)
library(lubridate)
```
#### 2. Directorio
> Igual que en semanas anteriores: ajusta automáticamente al directorio del script activo.
```r
# Setear el Directorio 
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
```

### II. Level Shift Example
#### 1. Generación del Desplazamiento de Nivel
> En este bloque se **simula una serie ARIMA(1,0,1)** completamente limpia y luego se le introduce un **cambio permanente en el nivel** (“level shift”) a partir de un instante T=100.  
> Este tipo de intervención representa, por ejemplo, **una reforma legal, un cambio estructural, o una modificación permanente en la tendencia media**.  
> Es útil para comprender cómo un cambio en la media afecta al modelo ARIMA y por qué es necesario incluir una **variable de intervención tipo step** para capturarlo correctamente.
```r
# 1. Generar Semilla y Tamaño de la Serie
set.seed(123)
n <- 200

# 2. Simular un ARIMA(1,0,1) Limpio
phi <- 0.6
theta <- 0.3
e <- rnorm(n)
y_clean <- numeric(n)
y_clean[1] <- e[1]
for (t in 2:n) {
  y_clean[t] <- phi*y_clean[t-1] + e[t] + theta*e[t-1]
}

# 3. Introducir un Cambio Permanente de Nivel a partir de T = 100
T <- 100
omega <- 10  # Magnitud del cambio
yLS <- y_clean
yLS[T:n] <- yLS[T:n] + omega  # Desplazamiento permanente desde T en adelante

# 4. Convertir las Series a Objetos ts para su Análisis
yLS <- ts(yLS)
y_clean <- ts(y_clean)

# 5. Gráfica de la Serie con Level Shift vs Serie Original
autoplot(yLS, series = "Series with Level Shift") +
  autolayer(y_clean, series = "Clean Series", alpha = 0.5) +
  ggtitle("Time Series with Level Shift at t=100")
```
#### 2. Identificación de un Modelo ARIMA sin Intervención
> En este bloque analizamos primero la **serie con level shift** y su versión **diferenciada**, usando ACF y PACF para intuir órdenes razonables.  
> Después ajustamos un **modelo ARIMA(4,1,0) sin intervención**, es decir, sin incluir explícitamente la variable que representa el cambio de nivel.  
> Finalmente, examinamos los **residuos** (diagnóstico gráfico y boxplot) para comprobar si quedan **patrones no explicados** o **outliers** asociados al level shift, lo que motiva introducir más adelante una **variable de intervención tipo step**.
```r
# 1. Plot Triple de la Serie con Level Shift, su ACF y su PACF
ggtsdisplay(yLS, main="Time Series with LS")

# 2. Plot Triple de la Serie con Level Shift Diferenciada, su ACF y su PACF
ggtsdisplay(diff(yLS), main="Time Series with LS")

# 3. Ajustar Modelo ARIMA Basal sin Intervención
yLS_arima <- Arima(yLS, order = c(4, 1, 0), include.mean = FALSE)

# 4. Resumen General, Significancia de Coeficientes, y Diagnóstico de Residuos
summary(yLS_arima)
coeftest(yLS_arima)
CheckResiduals.ICAI(yLS_arima)

# 5. Visualizar Residuos del Modelo ARIMA con Level Shift
autoplot(residuals(yLS_arima)) + ggtitle("Residuals of LS ARIMA Model")

# 6. Explorar Distribución de Residuos y Posibles Outliers
boxplot(residuals(yLS_arima), main = "Residuals of Baseline ARIMA Model")
```
#### 3. Detección Automática y Ajuste Inicial de Outliers
>En este bloque aplicamos varios métodos **automáticos** para detectar y corregir valores anómalos asociados al **level shift**:
>	1. Una regla sencilla basada en los **residuos del ARIMA** (|residuo| > 3·sd).
>	2. La función `tsoutliers()` y `tsclean()` del paquete **forecast**, que proponen sustituciones automáticas.
>	3. La función `tso()` del paquete **tsoutliers**, que ajusta un modelo ARIMA (aquí con `auto.arima`) y devuelve una **serie ajustada `yadj`** con los outliers corregidos.  
> Estos métodos son útiles como **detección rápida**, pero en el caso de un **cambio permanente de nivel** no sustituyen al uso de una **variable de intervención tipo step**, que modelaremos más adelante de forma explícita.
```r
# 1. Localizar Posibles Outliers en los Residuos (Regla de 3 Sigmas)
which(abs(yLS_arima$residuals) > (3 * sd(yLS_arima$residuals)))

# 2. Detectar Outliers en la Serie con tsoutliers
forecast::tsoutliers(yLS)

# 3. Limpiar la Serie con tsclean y Comparar Antes y Después
yLS_adj <- tsclean(yLS)
autoplot(yLS_adj, series = "LS adjusted time series") +
  autolayer(yLS, series = "Non adjusted time series", alpha = 0.5) +
  ggtitle("Adjusted series with forecast tsoutliers function (non effective for LS)")
  
# 4. Estimar Modelo y Outliers con tso usando auto.arima
out_ls <- tsoutliers::tso(yLS, tsmethod="auto.arima")
print(out_ls)
plot(out_ls)

# 5. Comparar Serie Ajustada con tso frente a Serie Original
y_tso <- out_ls$yadj
autoplot(y_tso, series = "tsoutliers adjusted series") +
  autolayer(yLS, series = "Non adjusted time series", alpha = 0.5) +
  ggtitle("Adjusted series after LS Removal with tsoutliers package")
```
#### 4. Modelado del Level Shift con Función de Transferencia
> En esta parte **modelamos explícitamente el cambio de nivel** mediante una **variable de intervención tipo step**:
> 	- Primero construimos el **regresor `xLS`**, que vale 0 antes de T=100 y 1 desde ese instante en adelante.
> 	- Ajustamos un **modelo TF preliminar** sin diferenciación y analizamos el **error de regresión** para ver si la serie requiere diferencias adicionales.
> 	- A continuación repetimos el ajuste con **diferenciación en la serie** y volvemos a inspeccionar el error de regresión.
> 	- Finalmente, usamos `TF.Identification.plot()` para **identificar órdenes (b, r, s)** razonables de la función de transferencia asociada al step.  
> Este enfoque integra el level shift dentro del modelo ARIMA de forma estructurada e interpretable, en lugar de tratarlo solo como un outlier aislado.
```r
# 1. Crear Regresor Step para el Level Shift
T <- 100
xLS <- rep(0, n)
xLS[T:n] <- 1
xLS <- ts(xLS)
autoplot(xLS) + ggtitle("Level Shift Regressor")

# 2. Estimación del Modelo TF Preliminar sin Diferenciación
TF_LS <- arima(yLS,
                order=c(1, 0, 0),
                xtransf = xLS,
                transfer = list(c(0,9)), #List with (r,s) orders
                include.mean = TRUE,
                method="ML")

# 3. Diagnóstico de los Residuos del Modelo Preliminar
TF.RegressionError.plot(yLS, xLS, TF_LS, lag.max = 20)

# 4. Estimación del Modelo TF con Diferenciación en la Serie
TF_LS <- arima(yLS,
                order=c(1, 1, 0),
                xtransf = xLS,
                transfer = list(c(0,9)), #List with (r,s) orders
                include.mean = TRUE,
                method="ML")

# 5. Diagnóstico de los Residuos del Modelo Diferenciado
TF.RegressionError.plot(yLS, xLS, TF_LS, lag.max = 20)
# NOTE: Si el error de esta regresión no es estacionario en varianza, hay que aplicar Box-Cox a las series de entrada y de salida.

# 6. Identificación visual de los parámetros TF
TF.Identification.plot(xLS, TF_LS)
b <- 0; r <- 0; s <- 0;
p <- 4; d <- 1; q <- 0;
```
#### 5. Ajuste Final del Modelo con Intervención y Comparación de Enfoques
> Aquí usamos los valores **b, r y s** identificados previamente para ajustar el **modelo final de función de transferencia** que incorpora el **level shift**:
> 	1. Construimos el **regresor rezagado `xlag`** usando el retardo b.
> 	2. Ajustamos el modelo TF definitivo (ruido ARIMA(4,1,0) + step) y analizamos el **resumen, significancia y visualización** de los coeficientes, junto con el diagnóstico de residuos.
> 	3. Comprobamos que **no queda correlación cruzada** entre residuos y el regressor de intervención.
> 	4. Comparamos visualmente la **serie observada** con:
> 		- El modelo con **intervención explícita** (`TF_LS`)
> 		- El ARIMA sin intervención (`yLS_arima`)
> 		- El ajuste automático obtenido con `tsoutliers` (`y_tso`)
> 	5. Finalmente, inspeccionamos los **coeficientes** de ambos modelos (con y sin intervención) para ver cómo cambia la estructura al introducir la variable step.
```r
# 1. Ajustar Modelo TF Final con b, r y s Seleccionados
xlag = Lag(xLS, b)   
xlag[is.na(xlag)]=0
TF_LS <- arima(yLS,
			    order=c(p,d,q),
                xtransf = xLS,
                transfer = list(c(r, s)), 
                include.mean = FALSE,
                method="ML")

# 2. Resumen General, Significancia y Gráfico de Coeficientes, y Diagnóstico de Residuos
summary(TF_LS) 
coeftest(TF_LS) 
autoplot(TF_LS)
CheckResiduals.ICAI(TF_LS, lag=50)

# 3. Analizar Correlación Cruzada entre Residuos y Variable de Intervención
res <- residuals(TF_LS)
res[is.na(res)] <- 0
ccf(y = res, x = xLS)

# 4. Comparar Serie Observada, Modelo con Intervención y Modelo ARIMA sin Intervención
autoplot(yLS, series = "Observed") +
  autolayer(fitted(TF_LS), series = "LS intervention") +
  autolayer(yLS_arima$fitted, series = "Arima") + 
  theme(legend.position = "top")
  
# 5. Comparar Serie Observada con Ajuste Automático de tsoutliers
autoplot(yLS, series = "Observed") +
  autolayer(y_tso, series = "tsoutliers package adjustment") + 
  theme(legend.position = "top")
  
# 6. Visualizar Ajuste del Modelo con Intervención sobre la Serie Observada
autoplot(yLS, series = "Observed") +
  autolayer(fitted(TF_LS)) + 
  theme(legend.position = "top")
  
# 7. Comparar Coeficientes del Modelo con Intervención y del ARIMA sin Intervención
coefficients(TF_LS) # Transfer function
coefficients(yLS_arima) # Arima for unadjusted time series  
```

### III. Intervention Analysis
#### 1. Carga de Datos y Preprocesamiento
> En este primer bloque preparamos los **datos reales de desempleo en España** para aplicar un modelo de **intervención**.  
> Se carga el fichero Excel con las series mensuales y se construye un objeto `ts` que contiene:
> 	- **TOTAL**: la serie de paro (variable dependiente),
> 	- **X**: una variable de intervención (por ejemplo, un dummy que toma valor 1 a partir de una reforma o cambio de política).  
> El rango temporal se fija a partir de 2010 para evitar ruido anterior. Después dividimos el conjunto en **training** (hasta 2023-09) y **validación** (desde 2023-10), respetando el orden temporal.  
> A continuación escalamos la variable de desempleo a millones para facilitar la estimación y, finalmente, examinamos la **transformación Box-Cox** recomendada para estabilizar la varianza antes de ajustar un modelo ARIMA con función de transferencia.
```r
# 1. Cargar el DataSet
fdata <- read_excel("UnemploymentSpainInterv_2010_2024.xlsx")

# 2. Convertir en Objeto ts
freq <- 12
fdata_ts <- fdata %>% filter(DATE >= lubridate::ymd("2010-01-01")) %>% select(TOTAL, X) %>% ts(start = c(2010,1), frequency = freq)
autoplot(fdata_ts, facets = TRUE)

# 3. Training Set
y <- window(fdata_ts[,"TOTAL"], end = c(2023,9)) 
x <- window(fdata_ts[,"X"], end = c(2023,9))

# 4. Validation Set
y.tv <- window(fdata_ts[,"TOTAL"], start = c(2023,10)) 
x.tv <- window(fdata_ts[,"X"], start = c(2023,10))

# 5. Escalar Valores
y <- y/1e6
y.tv <- y.tv/1e6

# 6. Transformación Box-Cox 
Lambda <- BoxCox.lambda.plot(y, freq)
y <- BoxCox(y, Lambda)
```
#### 2. Identificación Preliminar del Modelo con Intervención
> En este bloque realizamos la **identificación inicial** del modelo con intervención.  
> Primero exploramos la serie de paro escalada mediante `ggtsdisplay()`, observando su **tendencia, estacionalidad** y la forma de la **ACF/PACF** hasta 60 retardos, lo que sugiere el uso de un modelo estacional mensual.  
> A continuación ajustamos un **modelo preliminar de función de transferencia**: un ARIMA(1,1,0)(1,1,0)12 para el ruido, junto con una estructura de transferencia inicial (r=0, s=7) para la variable de intervención `x`.  
> El objetivo de este primer modelo no es que sea definitivo, sino **explorar la dinámica** y utilizar:
> 	- `TF.RegressionError.plot()` para evaluar si el **error de regresión** parece estacionario y si la estructura ARIMA es razonable.
> 	- `TF.Identification.plot()` para inspeccionar los coeficientes de la parte de transferencia y así **sugerir valores para b, r, s** que se usarán en el modelo final.
```r
# 0. Plot Triple de la Serie, su ACF y su PACF
ggtsdisplay(y, lag=60)

# 1. Ajustar Modelo TF Preliminar con Orden de Transferencia Amplio
TF.fit <- arima(y,
                order=c(1,1,0),
                seasonal = list(order=c(1,1,0),period=freq),
                xtransf = x,
                transfer = list(c(0,7)), #List with (r,s) orders
                include.mean = TRUE,
                method="ML")

# 2. Diagnóstico de los Residuos del Modelo Preliminar
TF.RegressionError.plot(y, x, TF.fit, lag.max = 120)
# NOTE: Si el error de esta regresión no es estacionario en varianza, hay que aplicar Box-Cox a las series de entrada y de salida.

# 3. Identificación visual de los parámetros TF
TF.Identification.plot(x, TF.fit)
b <- 0; r <- 1; s <- 1;
p <- 2; d <- 1; q <- 1;
P <- 0; D <- 1; Q <- 1;
```
#### 3. Ajuste del Modelo Final con Intervención y Forecast
> En este bloque utilizamos los valores **b, r, s** y los órdenes $ARIMA(p,d,q)(P,D,Q)_{freq}$​ seleccionados en la fase de identificación para ajustar el **modelo definitivo de función de transferencia** con intervención.  
> Primero construimos el **regresor rezagado `xlag`** aplicando el lag b a la variable de intervención y sustituyendo los `NA` iniciales por 0. Después estimamos el modelo TF final y analizamos:
> 	- El **resumen** y la **significancia** de los coeficientes (parte ARIMA + intervención),
> 	- El comportamiento de los **residuos** (ruido blanco vs. estructura remanente),
> 	- La **correlación cruzada** entre residuos y `x` para comprobar que la intervención está bien capturada.  
> A continuación comparamos visualmente la serie real con los **valores ajustados** por el modelo y, finalmente, generamos un **forecast de 12 meses** suponiendo que la intervención (variable `X`) se mantiene activa (`x_fut = 1`) durante todo el horizonte futuro.
```r
# 1. Ajustar Modelo TF Final con b, r y s Seleccionados
xlag = Lag(x,b)   
xlag[is.na(xlag)]=0
TF.fit <- arima(y,
                order=c(p,d,q),
                seasonal = list(order=c(P,D,Q),period=freq),
                xtransf = xlag,
                transfer = list(c(r,s)), 
                include.mean = FALSE,
                method="ML")

# 2. Resumen General, Significancia y Gráfico de Coeficientes, y Diagnóstico de Residuos
summary(TF.fit) 
coeftest(TF.fit) 
autoplot(TF.fit)
CheckResiduals.ICAI(TF.fit, lag=50)

# 3. Analizar Correlación Cruzada entre Residuos y Variable de Intervención
res <- residuals(TF.fit)
res[is.na(res)] <- 0
ccf(y = res, x = x)

# 4. Comparar Serie Real y Valores Ajustados del Modelo TF
autoplot(y, series = "Real")+
  forecast::autolayer(fitted(TF.fit), series = "Fitted")

# 5. Generar Pronóstico con Intervención Activa en el Horizonte Futuro
x_fut <- rep(1, 12)
y.tv.TF <- TF.forecast(y.old = y,      # past values of the series
                       x.old = x,      # past values of the explanatory variables
                       x.new = x_fut,  # new values of the explanatory variables
                       model = TF.fit, # fitted transfer function model
                       h = 12)         # forecast horizon
```
#### 4. Modelo ARIMA Sin Intervención y Comparación de Pronósticos
> En este último bloque construimos un **modelo de referencia** sin intervención para cuantificar cuánto aporta realmente la variable `X`.  
> Ajustamos un $ARIMA(2,1,1)(0,1,1)_{freq}$, es decir, un modelo puramente **univariado** sobre la serie de desempleo `y`, sin información explícita sobre el cambio de política o evento recogido en `X`.  
> Analizamos sus coeficientes y residuos para comprobar que es un modelo razonable y luego generamos un **pronóstico de 12 meses**.  
> Finalmente, comparamos la **precisión en el conjunto de validación** entre:
> 	- El ARIMA sin intervención (`y.tv.ARIMA`),
> 	- El modelo con intervención vía función de transferencia (`y.tv.TF`).  
> La comparación gráfica y mediante métricas (`accuracy`) permite ver si **incluir la intervención mejora de forma clara los pronósticos**.
```r
# 1. Ajustar Modelo ARIMA Sin Intervención
arima.fit <- arima(y,
                   order=c(2,1,1),
                   seasonal = list(order=c(0,1,1),period=freq),
                   include.mean = FALSE,
                   method="ML")

# 2. Resumen General, Significancia y Gráfico de Coeficientes, y Diagnóstico de Residuos
summary(arima.fit) 
coeftest(arima.fit) 
autoplot(arima.fit)
CheckResiduals.ICAI(arima.fit, lag=50)

# 3. Comparar Serie Real y Valores Ajustados del Modelo ARIMA
autoplot(y, series = "Real")+
  forecast::autolayer(fitted(arima.fit), series = "Fitted")

# 4. Generar Pronóstico con Modelo ARIMA Sin Intervención
y.tv.ARIMA <- forecast(y,                  # y series up to sample i 
                       model = arima.fit,  # Model trained
                       h=12)$mean          # h is the forecast horizon

# 5. Evaluar Precisión de Ambos Modelos en el Conjunto de Validación
results <- as.data.frame(cbind(y.tv,y.tv.TF, y.tv.ARIMA)) # DF de pronósticos 
accuracy(results$y.tv, results$y.tv.ARIMA)
accuracy(results$y.tv, results$y.tv.TF)

# 6. Comparar Pronósticos del Modelo ARIMA y del Modelo TF
autoplot(y.tv, series = "Real")+
  forecast::autolayer(y.tv.ARIMA, series = "ARIMA") +
  forecast::autolayer(ts(y.tv.TF, start=c(2023,10), frequency = freq), series = "TF")
```

### IV. Imputación de Valores Faltantes y Detección de Outliers (básico)
#### 1. Valores Faltantes
> En este apartado trabajamos con la serie `tsAirgap`, que contiene **valores faltantes** distribuidos a lo largo del tiempo.  
> Primero visualizamos la **distribución temporal de los NAs** para detectar si aparecen en bloques, de forma aislada o siguiendo algún patrón estacional.  
> Después comparamos distintas estrategias de **imputación de valores faltantes** usando el paquete `imputeTS`:
> 	- Métodos basados en **descomposición estacional** (`na_seadec`, `na_seasplit`),
> 	- Métodos basados en **filtros de Kalman**, tanto con un modelo `auto.arima` como con un modelo estructural `StructTS`.  
> Cada llamada a `ggplot_na_imputations()` permite ver **serie original vs serie imputada**, para valorar visualmente qué método respeta mejor la estructura de la serie.
```r
# 1. Cargar Serie con Valores Faltantes
y <- tsAirgap

# 2. Visualizar Distribución de Valores Faltantes en el Tiempo
ggplot_na_distribution(y)

# 3. Imputación Basada en Descomposición Estacional (na_seadec)
imp_seadec <- na_seadec(y)
ggplot_na_imputations(y, imp_seadec)

# 4. Imputación por División Estacional de la Serie (na_seasplit)
imp_seas <- na_seasplit(y)
ggplot_na_imputations(y, imp_seas)

# 5. Imputación Mediante Filtro de Kalman con Modelo auto.arima
imp_kalman_aa <- na_kalman(y, model = "auto.arima")
ggplot_na_imputations(y, imp_kalman_aa)

# 6. Imputación Mediante Filtro de Kalman con Modelo StructTS
imp_kalman_st <- na_kalman(y, model = "StructTS")
ggplot_na_imputations(y, imp_kalman_st)
```
#### 2. Outliers
> En este apartado trabajamos con la serie `gold`, que contiene **posibles valores atípicos** en el precio diario del oro.  
> Primero representamos la serie para localizar visualmente **picos anómalos**.  
> Después utilizamos `tsoutliers()` (paquete **forecast/fpp2**) para **detectar** automáticamente los outliers y sugerir **valores de sustitución**.  
> Con `tsclean()` generamos una versión **“limpia”** de la serie, en la que los outliers han sido corregidos (y también se imputarían NAs si existieran).  
> Finalmente comparamos gráficamente la serie original con la corregida y marcamos los puntos donde se han aplicado **reemplazos**, lo que permite ver de forma clara **qué observaciones se consideran outliers y cómo se han ajustado**.
```r
# 1. Cargar Serie con Outliers
y <- gold

# 2. Visualizar Serie Temporal con Outliers
autoplot(y)

# 3. Detectar Outliers con tsoutliers
tsoutliers(y)

# 4. Corregir Serie con tsclean
z <- tsclean(y)

# 5. Comparar Serie Original y Serie Corregida
autoplot(y, color = "blue") +
  autolayer(z, color = "red")

# 6. Visualizar Outliers Detectados sobre la Serie Corregida
autoplot(z, series="clean", color='red', lwd=0.9) +
  autolayer(y, series="original", color='gray', lwd=1) +
  geom_point(data = tsoutliers(y) %>% as.data.frame(),
             aes(x=index, y=replacements), col='blue') +
  labs(x = "Day", y = "Gold price ($US)")
```

### V. Detección de Outliers (avanzado)
#### 1. Ejemplo de Outlier Aditivo (AO)
###### 1.1. Simulación y Modelo ARIMA Sin Intervención
> En este primer bloque construimos un ejemplo controlado de **outlier aditivo (AO)**:
> 	1. Simulamos una serie **ARIMA(1,0,1)** (aquí reducida a AR(1)) limpia y la guardamos como referencia.
> 	2. Introducimos un **salto puntual** en t=100t = 100t=100 sumando +10 solo en esa observación; este es el AO.  
> 	3. Ajustamos un **modelo ARIMA básico** ignorando la existencia del outlier y analizamos la **ACF/PACF**, los **residuos** y una regla de **3 sigmas** para ver cómo el AO distorsiona el ajuste.  
> Este escenario sirve como punto de partida para comparar después métodos de tratamiento automático (`tsclean`) y el enfoque más riguroso mediante **modelos de intervención**.
```r
# 1. Fijar Semilla y Definir Longitud de la Serie
set.seed(123)
n <- 200

# 2. Simular Serie ARIMA(1,0,1) Limpia (Aquí sin Parte MA)
# yAO <- arima.sim(list(ar = 0.7, ma = 0.4), n = n)
yAO <- arima.sim(list(ar = 0.7, ma = 0), n = n)
y_orig <- yAO

# 3. Visualizar Serie ARIMA Limpia
autoplot(yAO)

# 4. Introducir Outlier Aditivo en t = 100 y Comparar con Serie Original
yAO[100] <- yAO[100] + 10   # AO de +10 en un Único Punto
autoplot(yAO, series = "Series with AO outlier") +
  autolayer(y_orig, series = "Original Series", alpha = 0.5) +
  ggtitle("Time Series with Additive Outlier at t=100")

# 5. Ajustar Modelo ARIMA Basal Ignorando el Outlier y Analizar Residuos
ggtsdisplay(yAO, main = "Time Series with AO")
yAO_arima <- Arima(yAO, order = c(1, 0, 0), include.mean = FALSE)

# 6. Resumen General, Significancia de Coeficientes, y Diagnóstico de Residuos
summary(yAO_arima)
coeftest(yAO_arima)
CheckResiduals.ICAI(yAO_arima)

# 7. Visualizar Residuos y Localizar Outliers Potenciales
autoplot(residuals(yAO_arima)) + ggtitle("Residuals of AO ARIMA Model")
boxplot(residuals(yAO_arima), main = "Residuals of Baseline ARIMA Model")
which(abs(yAO_arima$residuals) > (3 * sd(yAO_arima$residuals)))
```
###### 1.2. Corrección Automática del AO con `tsoutliers` y `tsclean`
> En este bloque usamos herramientas **automáticas** del paquete `forecast` para tratar el outlier aditivo sin especificar explícitamente un modelo de intervención.  
> Primero aplicamos `tsoutliers(yAO)` para **detectar** el AO y obtener la propuesta de **valor de reemplazo**. Después utilizamos `tsclean(yAO)` para generar una serie **ajustada**, donde el outlier ha sido suavizado/corregido (y en general también se imputarían NAs si existieran).  
> A continuación comparamos visualmente la serie original y la corregida y volvemos a ajustar un **ARIMA(1,0,0)** sobre la serie limpia. Finalmente, analizamos el diagnóstico del nuevo modelo para ver cómo **mejora el comportamiento de los residuos** al eliminar el AO de forma automática, en contraste con la versión sin limpiar.
```r
# 1. Detectar Outliers de Forma Automática con tsoutliers
forecast::tsoutliers(yAO)

# 2. Limpiar la Serie con tsclean y Comparar con la Serie Original
yAO_adj <- tsclean(yAO)

autoplot(yAO_adj, series = "AO adjusted time series") +
  autolayer(yAO, series = "Non adjusted time series", alpha = 0.5) +
  ggtitle("Adjusted Series after AO Removal")

# 3. Ajustar ARIMA a la Serie Ajustada
ggtsdisplay(yAO_adj)
yAO_adj_arima <- Arima(yAO_adj, order = c(1, 0, 0), include.mean = FALSE)

# 4. Resumen General, Significancia de Coeficientes, y Diagnóstico de Residuos 
summary(yAO_adj_arima)
coeftest(yAO_adj_arima)
CheckResiduals.ICAI(yAO_adj_arima)
```
###### 1.3. Modelado del AO como Intervención con Función de Transferencia
> En este bloque pasamos de la corrección “automática” a un enfoque **estructurado** de modelado del outlier aditivo.  
> Primero definimos una **variable de intervención tipo impulso** `xAO`, que vale 1 solo en t=100t = 100t=100 (momento del AO) y 0 en el resto de instantes. Esta variable entra en el modelo como **regresor exógeno**.  
> A continuación ajustamos un **modelo de función de transferencia** (TF): un ARIMA(1,0,0) para el ruido y una parte de transferencia inicial con orden (r=0,s=9)(r = 0, s = 9)(r=0,s=9), que actúa sobre el impulso.  
> Usamos `TF.RegressionError.plot()` para inspeccionar el **error de regresión** y comprobar si la estructura es razonablemente estacionaria (en caso contrario, podría ser necesaria una transformación Box–Cox).  
> Finalmente, con `TF.Identification.plot()` examinamos los **coeficientes de la transferencia** asociados a `xAO`, lo que nos ayuda a elegir valores más parsimoniosos para (b,r,s)(b, r, s)(b,r,s) en el modelo definitivo.
```r
# 1. Crear Variable de Intervención Tipo Impulso para el AO
xAO <- rep(0, n)
T <- 100
xAO[T] <- 1  # Indicador del AO en t = 100

# 2. Ajustar Modelo TF Preliminar con Impulso y Orden de Transferencia Amplio
TF_AO <- arima(yAO,
               order = c(1, 0, 0),
               xtransf = xAO,
               transfer = list(c(0, 9)), # List with (r,s) orders
               include.mean = TRUE,
               method = "ML")

# 3. Diagnóstico de los Residuos del Modelo Preliminar con Impulso
TF.RegressionError.plot(yAO, xAO, TF_AO, lag.max = 20)
# NOTE: Si el error de esta regresión no es estacionario en varianza, hay que aplicar Box-Cox a las series de entrada y de salida.

# 4. Identificación visual de los parámetros TF
TF.Identification.plot(xAO, TF_AO)
b <- 0; r <- 0; s <- 0;
p <- 1; d <- 0; q <- 0;
```
###### 1.4. Ajuste Final del Modelo TF para el AO y Comparación de Enfoques
> En este último bloque construimos el **modelo definitivo de función de transferencia** para el outlier aditivo, usando los valores de b, r, s seleccionados en la fase de identificación.  
> Primero generamos el **regresor rezagado** `xlag` aplicando el lag b al impulso y volvemos a ajustar el modelo TF (ARIMA + intervención) sin término de media.  
> A continuación analizamos el **resumen**, la **significancia de los coeficientes**, la **visualización del modelo** y el **diagnóstico de residuos**, verificando que la intervención captura correctamente el AO y que los residuos se comportan como ruido blanco.  
> Después comprobamos la **correlación cruzada** entre residuos y la variable de intervención para asegurarnos de que no queda información sistemática sin explicar.  
> Finalmente comparamos:
> 	- El **pronóstico** del modelo con intervención frente a la serie corregida automáticamente con `tsclean`,
> 	- Los **coeficientes** de los tres modelos (ARIMA sin ajustar, ARIMA tras `tsclean` y TF con intervención), lo que permite ver cómo cambia la estructura al modelar explícitamente el AO.
```r
# 1. Ajustar Modelo TF Final con Impulso y Estructura Seleccionada
xlag <- Lag(xAO, b)  
xlag[is.na(xlag)] <- 0
TF_AO <- arima(yAO,
               order = c(1, 0, 0),
               xtransf = xlag,
               transfer = list(c(r, s)),
               include.mean = FALSE,
               method = "ML")

# 2. Resumen General, Significancia y Gráfico de Coeficientes, y Diagnóstico de Residuos
summary(TF_AO)        
coeftest(TF_AO)      
autoplot(TF_AO)
CheckResiduals.ICAI(TF_AO, lag = 50)

# 3. Analizar Correlación Cruzada entre Residuos y Variable de Intervención
res <- residuals(TF_AO)
res[is.na(res)] <- 0
ccf(y = res, x = xAO)

# 4. Comparar Pronóstico del Modelo TF con la Serie Ajustada con tsoutliers
autoplot(MLTools::TF.RegressionError(yAO, xAO, TF_AO), series = "TF_RegError") + 
  autolayer(yAO_adj, series = "Adjusted with tsoutliers") + 
  ggtitle("Forecast after modelling AO intervention")

# 5. Comparar Coeficientes de los Distintos Modelos
coefficients(TF_AO)         # Transfer Function
coefficients(yAO_arima)     # ARIMA para Serie sin Ajustar
coefficients(yAO_adj_arima) # ARIMA para Serie Ajustada
```
#### 2. Ejemplo de Outlier de Innovación (IO)
###### 2.1. Simulación del IO y Modelo ARIMA Sin Intervención
> En este bloque construimos un ejemplo controlado de **outlier de innovación (IO)**.  
> A diferencia del AO (que altera solo una observación), aquí modificamos la **innovación** $e_t$​ en t=100, de forma que el shock se **propaga dinámicamente** a través del modelo AR(1). 
> Primero generamos la serie limpia `y_clean` y la versión con IO `yIO` usando la misma estructura ARIMA(1,0,1) (simplificada a AR(1)), y las comparamos gráficamente.  
> Después ajustamos un **ARIMA básico ignorando el IO** y estudiamos sus **residuos y outliers potenciales**, para ver cómo este tipo de perturbación afecta a la calidad del modelo y motiva un tratamiento más sofisticado (automatizado o mediante intervención).
```r
# 1. Fijar Semilla y Definir Longitud de la Serie
set.seed(123)
n <- 300

# 2. Generar Innovación Limpia y con Outlier de Innovación en t = 100
e_clean <- rnorm(n)
e_IO <- e_clean
e_IO[100] <- e_IO[100] + 20  

# 3. Definir Parámetros del Proceso ARIMA(1,0,1)
# phi <- 0
phi <- 0.7
# theta <- c(0.6, -0.3)
theta <- c(0, 0)

# 4. Inicializar Series Limpia y con IO
y_clean <- numeric(n)
yIO <- numeric(n)

# 5. Generar Ambas Series (Limpia y con IO) Mediante la Ecuación ARIMA
for (t in 2:n) {
  y_clean[t] <- phi * y_clean[t - 1] + e_clean[t] +
    theta[1] * e_clean[t - 1] + theta[2] * ifelse(t > 2, e_clean[t - 2], 0)
  yIO[t] <- phi * yIO[t - 1] + e_IO[t] +
    theta[1] * e_IO[t - 1] + theta[2] * ifelse(t > 2, e_IO[t - 2], 0)
}

# 6. Convertir a Objetos ts
y_clean <- ts(y_clean)
yIO <- ts(yIO)

# 7. Gráfico conjunto de las Series
autoplot(y_clean, series = "Clean Series") +
  autolayer(yIO, series = "Series with IO") +
  theme(legend.position = "top")

# 8. Ajustar Modelo ARIMA Basal Ignorando el IO y Analizar Residuos
ggtsdisplay(yIO, main = "Time Series with IO")
yIO_arima <- Arima(yIO, order = c(1, 0, 0), include.mean = FALSE)

# 9. Resumen General, Significancia de Coeficientes, y Diagnóstico de Residuos 
summary(yIO_arima)
coeftest(yIO_arima)
CheckResiduals.ICAI(yIO_arima)

# 10. Visualizar Residuos y Localizar Outliers Potenciales
autoplot(residuals(yIO_arima)) + ggtitle("Residuals of IO ARIMA Model")
boxplot(residuals(yIO_arima), main = "Residuals of Baseline ARIMA Model")
which(abs(yIO_arima$residuals) > 10)
```
###### 2.2. Corrección Automática del IO con `tsoutliers` y `tsclean`
> Igual que en el caso del AO, aquí aplicamos un enfoque **automático** para tratar el **outlier de innovación**.  
> Primero usamos `tsoutliers(yIO)` para detectar observaciones problemáticas y obtener propuestas de reemplazo. A continuación, `tsclean(yIO)` genera una serie **ajustada** (`yIO_adj`) donde el efecto del IO se ha suavizado/corregido.  
> En la gráfica comparamos tres series:
> 	- La serie limpia original (`y_clean`),
> 	- La serie con IO (`yIO`),
> 	- La serie ajustada (`yIO_adj`),  
> Lo que permite ver hasta qué punto la corrección se acerca a la serie “ideal”.  
> Después volvemos a ajustar un **ARIMA(1,0,0)** sobre la serie corregida y analizamos el diagnóstico (ACF/PACF, residuos, significancia de coeficientes) para comprobar si el comportamiento del modelo mejora respecto al caso en el que ignorábamos el IO.
```r
# 1. Detectar Outliers de Forma Automática con tsoutliers
forecast::tsoutliers(yIO)

# 2. Limpiar la Serie con tsclean y Comparar con Series Limpia y Original
yIO_adj <- tsclean(yIO)

autoplot(yIO_adj, series = "IO adjusted time series") +
  autolayer(y_clean, series = "Original time series (before IO injection)", 
            alpha = 0.25, linewidth = 2) +
  autolayer(yIO, series = "Non adjusted time series") +
  ggtitle("Adjusted Series after IO Removal")

# 3. Ajustar ARIMA a la Serie Ajustada y Evaluar Diagnóstico
ggtsdisplay(yIO_adj)
yIO_adj_arima <- Arima(yIO_adj, order = c(1, 0, 0), include.mean = FALSE)

# 4. Resumen General, Significancia de Coeficientes, y Diagnóstico de Residuos 
summary(yIO_adj_arima)
coeftest(yIO_adj_arima)
CheckResiduals.ICAI(yIO_adj_arima)
```
###### 2.3. Modelado del IO como Intervención con Función de Transferencia
> Aquí repetimos la idea de la intervención tipo impulso, pero aplicada al **outlier de innovación**.  
> Definimos una variable `xIO` que vale 1 solo en t=100 (instante del shock en la innovación) y 0 en el resto, y la incluimos como **regresor exógeno** en un modelo de **función de transferencia** preliminar con orden (r=0, s=9).  
> El objetivo de este primer ajuste no es obtener el modelo definitivo, sino estudiar el **error de regresión** con `TF.RegressionError.plot()` y usar `TF.Identification.plot()` para inspeccionar la respuesta asociada a `xIO`, lo que nos orienta sobre valores razonables de (b, r, s) para el modelo final que capturará explícitamente el IO.
```r
# 1. Crear Variable de Intervención Tipo Impulso para el IO
T <- 100
xIO <- rep(0, n)
xIO[T] <- 1  # Indicador del IO en t = 100

# 2. Ajustar Modelo TF Preliminar con Impulso y Orden de Transferencia Amplio
TF_IO <- arima(yIO,
               order = c(1, 0, 0),
               xtransf = xIO,
               transfer = list(c(0, 9)), # List with (r,s) orders
               include.mean = TRUE,
               method = "ML")

# 3. Diagnóstico de los Residuos del Modelo Preliminar con Impulso
TF.RegressionError.plot(yIO, xIO, TF_IO, lag.max = 20)

# 4. Identificación visual de los parámetros TF
TF.Identification.plot(xIO, TF_IO)
b <- 0; r <- 1; s <- 0;
p <- 1; d <- 0; q <- 1;
```
###### 2.4. Ajuste Final del Modelo TF para IO y Comparación de Enfoques
> Cerramos el ejemplo del **outlier de innovación** construyendo el **modelo definitivo de función de transferencia** con los órdenes (p,d,q)(P,D,Q) y (b,r,s) ya seleccionados.  
> Primero generamos el **regresor rezagado** `xlag` aplicando el lag b al impulso `xIO`, y estimamos el modelo TF completo (ARIMA + intervención).  
> A continuación revisamos el **resumen del modelo**, la **significancia de los coeficientes**, la **gráfica del ajuste** y el **diagnóstico de residuos** para comprobar que el IO queda correctamente modelado y que los residuos son aproximadamente ruido blanco.  
> Luego analizamos la **correlación cruzada** entre residuos y la variable de intervención para asegurarnos de que ya no queda estructura asociada al IO sin capturar.  
> Por último, comparamos:
> 	- El **pronóstico** del modelo con intervención con la serie corregida automáticamente (`yIO_adj`),
> 	- Los **coeficientes** de los tres modelos (ARIMA sin ajustar, ARIMA tras `tsclean` y TF con intervención), lo que permite ver el impacto de **modelar explícitamente el IO** frente a simplemente “limpiarlo”.
```r
# 1. Ajustar Modelo TF Final para IO con Estructura Seleccionada
xlag <- Lag(xIO, b)   
xlag[is.na(xlag)] <- 0
TF_IO <- arima(yIO,
               order = c(p, d, q),
               xtransf = xlag,
               transfer = list(c(r, s)),
               include.mean = FALSE,
               method = "ML")

# 2. Resumen General, Significancia y Gráfico de Coeficientes, y Diagnóstico de Residuos
summary(TF_IO)    
coeftest(TF_IO)      
autoplot(TF_IO)
CheckResiduals.ICAI(TF_IO, lag = 50)

# 3. Analizar Correlación Cruzada entre Residuos y Variable de Intervención
res <- residuals(TF_IO)
res[is.na(res)] <- 0
ccf(y = res, x = xIO)

# 4. Comparar Pronóstico del Modelo TF con la Serie Ajustada con tsoutliers
autoplot(MLTools::TF.RegressionError(yIO, xIO, TF_IO), series = "TF_RegError") + 
  autolayer(yIO_adj, series = "Adjusted with tsoutliers") + 
  ggtitle("Forecast after modelling IO intervention")

# 5. Comparar Coeficientes de los Distintos Modelos
coefficients(TF_IO)         # Transfer Function
coefficients(yIO_arima)     # ARIMA para Serie sin Ajustar
coefficients(yIO_adj_arima) # ARIMA para Serie Ajustada
```

Los apuntes continúan en [[Week 10 - Non Linear Models]]