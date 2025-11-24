### 0. Introducción Teórica
#### 1. Motivación y Contexto
- Limitaciones de los modelos lineales (ARIMA, TF):
    - Relación lineal entre entradas y salida.     
    - Dificultad para capturar saturaciones, umbrales, efectos asimétricos…

- Situaciones típicas en las que aparecen **no linealidades**:
    - Demanda eléctrica vs temperatura.
    - Series financieras con cambios de volatilidad/regímenes.
    - Sistemas donde el comportamiento cambia según el nivel.

- Objetivo de la semana:
    - Ver **dos formas de introducir no linealidad**:
        - Feature engineering + modelos lineales (TF).
        - Modelos no lineales explícitos (MLP/NARX).

#### 2. Modelos de Series Temporales No Lineales Basados en Regresión
##### 2.1. Modelo General de Regresión No Lineal
- Forma general:  $y_t = f(y_{t-1}, y_{t-2}, \dots, x_t, x_{t-1}, \dots) + \varepsilon_t$

- Diferencia con Linealidad: $f(\cdot)$ puede ser cualquier función no lineal (polinómica, a trozos, etc)

- $\varepsilon_t$​ sigue siendo un **término de error** (idealmente ruido blanco), igual que en ARIMA; la diferencia está en la forma de $f(\cdot)$, no en cómo tratamos el ruido.

- Conexión con ARIMA/TF: ARIMA → caso especial donde $f$ es lineal.
##### 2.2. Modelos NAR y NARX
- **NAR (Nonlinear Autoregressive)**:
    - Solo usa retardos de la propia serie: $y_t = f(y_{t-1}, \dots, y_{t-p}) + \varepsilon_t$

- **NARX (Nonlinear Autoregressive with Exogenous Inputs)**:
    - Incluye además inputs exógenos: $x_t, x_{t-1}, \dots$

- Interpretación:
    - Son la versión no lineal de AR/ARX, muy usados en control y forecasting.
##### 2.3. Modelos NARMAX
- Extensión NARX añadiendo términos de ruido pasados: $y_t = f(y_{t-1:\,t-p}, x_{t:\,t-q}, \varepsilon_{t-1:\,t-r}) + \varepsilon_t$

- Relación con ARMA/ARIMA y con modelos de caja negra.

- Comentario práctico:
    - El MLP de la práctica se parece a un **NARX** (lags de DEM y de las X) sin modelar explícitamente $\varepsilon_{t-k}$

#### 3. Modelos de Cambio de Régimen (Regime Switching)
##### 3.1. Idea Intuitiva de Cambio de Régimen
- Concepto de **regímenes o estados**:
    - Períodos de “alta demanda” vs “baja demanda”.
    - Fases de “expansión” vs “recesión”.

- Cada régimen tiene su **propio modelo**:
    - Distintos parámetros AR/MA según el estado.
##### 3.2. Tipos de Modelos de Régimen
- **Modelos threshold (TAR/SETAR)**:
    - Cambios de régimen cuando la serie cruza ciertos umbrales.

- **Modelos Markov-switching (MS-AR, MS-ARMA)**:
    - El régimen sigue una cadena de Markov oculta.

- Comentario:
    - Importantes conceptualmente, pero en las prácticas de esta semana **no se implementan**: el foco está en TF+FE y MLP.
    - Suelen ser útiles cuando vemos **cambios bruscos y persistentes** en la dinámica (no explicables solo con cambios de nivel o cambios de varianza).

#### 4. Combinación de Pronósticos
##### 4.1. Motivación para Combinar Modelos
- Distintos modelos capturan **partes diferentes** de la dinámica.

- Combinación de pronósticos:
    - Reduce riesgo de elegir “el modelo equivocado”.
    - Suele mejorar estabilidad y robustez.

##### 4.2. Estrategias Sencillas de Combinación
- Media simple de pronósticos.

- Combinaciones ponderadas (por error histórico, AIC, etc.).

- Comentario:
    - En este curso, la combinación se puede **relacionar conceptualmente** con:
        - Modelos lineales + no lineales.
        - Diferentes configuraciones (TF vs MLP) que podrían combinarse.
	- En la práctica, muchas competiciones de forecasting y aplicaciones reales usan **ensambles** (combinación de varios modelos) porque tienden a ser más **robustos** que cualquier modelo individual.

#### 5. Conexión con las Prácticas de la Semana 10
##### 5.1. TF + Feature Engineering como Modelo No Lineal Implícito
- Usar TF lineales, pero:
    - Transformar inputs (por ejemplo, dividir temperatura en `tcold` y `thot`).
    - Esto equivale a aproximar una relación no lineal con un modelo lineal por tramos en las entradas.

##### 5.2. MLP como NARX No Lineal
- Red neuronal MLP que recibe:
    - Lags de DEM (output) y de las variables exógenas.

- Se comporta como un modelo **NARX no lineal**:
    - Aprende automáticamente la forma de $f(\cdot)$.

- Validación mediante cross-validation y forecast iterativo a 7 días.

### I. Previos
#### 1. Carga de Librerías
> En esta semana añadimos las librerías de *`NeuralSens`* para RELLENAR, *`caret`* para RELLENAR, *`kernlab`* para RELLENAR, *`nnet`* para RELLENAR, y *`NeuralNetTools`* para RELLENAR.
```r
# Librerías
library(fpp2)
library(lmtest)
library(tseries) 
library(TSA)
library(readxl)
library(MLTools)
library(imputeTS)
library(NeuralSens)
library(caret)
library(kernlab)
library(nnet)
library(NeuralNetTools)
```
#### 2. Directorio
> Igual que en semanas anteriores: ajusta automáticamente al directorio del script activo.
```r
# Setear el Directorio 
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
```
	
### II. Feature Engineering with Transfer Function
#### 1. Carga de Datos y Preprocesamiento
> RELLENAR
```r
# 1. Lectura de Datos con NAs
fdata <- read_excel("DAILY_DEMAND_TR_NA.xlsx")

# 2. Convertir Data Frame a Objeto ts con Frecuencia Semanal
fdata_ts <- ts(fdata, frequency = 7)
autoplot(fdata_ts, facets = TRUE)

# 3. Visualizar Distribución de Valores Faltantes por Variable
ggplot_na_distribution(fdata_ts[, 2])
ggplot_na_distribution(fdata_ts[, 3])
ggplot_na_distribution(fdata_ts[, 4])

# 4. Imputación Estacional de Valores Faltantes (na_seasplit)
imp_seas <- na_seasplit(fdata_ts)
ggplot_na_imputations(fdata_ts[, 4], imp_seas[, 4])

# 5. Imputación mediante Filtro de Kalman con Modelo auto.arima
imp_kalman <- na_kalman(fdata_ts, model = "auto.arima")
ggplot_na_imputations(fdata_ts[, 4], imp_kalman[, 4])

# 6. Seleccionar Serie Imputada Estacional como Base de Trabajo
fdata_ts <- imp_seas

# 7. Definir Serie de Salida y Matriz de Inputs (WD y TEMP)
y <- fdata_ts[, 2]
x <- fdata_ts[, c(3, 4)]
autoplot(cbind(y, x), facets = TRUE)

# 8. Escalar Series para Estabilizar Magnitudes
y.tr <- y / 100
x.tr <- x / 1
autoplot(cbind(y.tr, x.tr), facets = TRUE)
```
#### 2. TF Lineal con WD y TEMP (Sin Feature Engineering)
> RELLENAR
```r
## Primer paso: Identificación y Ajuste Inicial (TF con 2 Inputs) ---------------------

# 1. Ajustar Modelo TF Preliminar sin Diferenciación y con s Grande
#    (Esta función arima pertenece al paquete TSA)
TF.fit <- arima(y.tr,
                xtransf = x.tr,
                order = c(1, 0, 0),
                seasonal = list(order = c(1, 0, 0), period = 7),
                transfer = list(c(0, 9), c(0, 9)),
                method = "ML")

# 2. Evaluar Error de Regresión para Ver Necesidad de Diferenciación
TF.RegressionError.plot(y.tr, x.tr, TF.fit, lag.max = 50)
# Regular differentiation is needed and coefficients of explanatory variables cannot be interpreted


## Segundo Paso: Añadir Diferenciación Regular ---------------------------------

# 3. Ajustar Modelo TF con Diferenciación Regular y s Grande
TF.fit <- arima(y.tr,
                xtransf = x.tr,
                order = c(1, 1, 0),
                seasonal = list(order = c(1, 0, 0), period = 7),
                transfer = list(c(0, 9), c(0, 9)),
                method = "ML")

# 4. Revisar Errores de Entrenamiento y Significancia de Coeficientes
summary(TF.fit)          # Summary of training errors and estimated coefficients
coeftest(TF.fit)         # Statistical significance of estimated coefficients

# 5. Evaluar Error de Regresión para Comprobar Estacionariedad
TF.RegressionError.plot(y.tr, x.tr, TF.fit, lag.max = 50)
# Regression error is stationary, then, we can continue
# NOTE: If this regression error was not stationary in variance, boxcox should be applied to input and output series.
# Try AR(1)7 for seasonal component and ARMA(2,1) for regular component?

# 6. Identificar Coeficientes de Transfer Function para Cada Input
TF.Identification.plot(x.tr, TF.fit)
# WD:    b=0, r=0, s=0
# TEMP:  b=0, r=0, s=1


## Tercer Paso: Modelo TF con Estructura Seleccionada ---------------------------

# 7. Ajustar Modelo TF con Órdenes (b,r,s) Seleccionados y ARIMA Inicial
TF.fit <- arima(y.tr,
                xtransf = x.tr,
                order = c(2, 1, 1),
                seasonal = list(order = c(1, 0, 0), period = 7),
                transfer = list(c(0, 0), c(0, 1)),
                method = "ML")

# 8. Revisar Errores de Entrenamiento, Coeficientes y Residuos
summary(TF.fit)          # Summary of training errors and estimated coefficients
coeftest(TF.fit)         # Statistical significance of estimated coefficients
CheckResiduals.ICAI(TF.fit, lag = 50)

# 9. Diagnóstico Gráfico del Modelo (Ajuste vs Real)
PlotModelDiagnosis(x.tr, y.tr, fitted(TF.fit), together = TRUE)
```
#### 3. Feature Engineering sobre la Temperatura (tcold, thot)
> RELLENAR
```r
# 1. Analizar Relación No Lineal entre Temperatura y Demanda
ggplot(fdata) + geom_point(aes(x = TEMP, y = DEM))

# 2. Crear Variables de Temperatura Fría y Caliente (Relación No Lineal por Tramos)
fdata$tcold <- sapply(as.numeric(fdata_ts[, 4]), min, 17)
fdata$thot  <- sapply(as.numeric(fdata_ts[, 4]), max, 22)

# 3. Crear Nuevas Series Temporales con WD, tcold y thot
y <- ts(fdata[, 2], frequency = 7)
x <- ts(fdata[, c(3, 5, 6)], frequency = 7)
autoplot(cbind(y, x), facets = TRUE)

# 4. Escalar Nuevas Series para el Modelo TF
y.tr <- y / 100
x.tr <- x / 1
autoplot(cbind(y.tr, x.tr), facets = TRUE)
```
#### 4. TF con WD, tcold y thot (Identificación y Modelo Final)
> RELLENAR
```r
## Primer Paso: Identificación y Ajuste Inicial con 3 Inputs ---------------------------

# 1. Ajustar Modelo TF Preliminar sin Diferenciación y s Grande
#    (Esta función arima pertenece al paquete TSA)
TF.fit <- arima(y.tr,
                xtransf = x.tr,
                order = c(1, 0, 0),
                seasonal = list(order = c(1, 0, 0), period = 7),
                transfer = list(c(0, 9), c(0, 9), c(0, 9)),
                method = "ML")

# 2. Evaluar Error de Regresión para Ver Necesidad de Diferenciación
TF.RegressionError.plot(y.tr, x.tr, TF.fit, lag.max = 50)
# Regular differentiation is needed and coefficients of explanatory variables cannot be interpreted


## Segundo Paso: Añadir Diferenciación Regular ---------------------------------

# 3. Ajustar Modelo TF con Diferenciación Regular y s Grande
TF.fit <- arima(y.tr,
                xtransf = x.tr,
                order = c(1, 1, 0),
                seasonal = list(order = c(1, 0, 0), period = 7),
                transfer = list(c(0, 9), c(0, 9), c(0, 9)),
                method = "ML")

# 4. Revisar Errores de Entrenamiento y Significancia de Coeficientes
summary(TF.fit)          # Summary of training errors and estimated coefficients
coeftest(TF.fit)         # Statistical significance of estimated coefficients

# 5. Evaluar Error de Regresión para Comprobar Estacionariedad
TF.RegressionError.plot(y.tr, x.tr, TF.fit, lag.max = 50)
# Regression error is stationary, then, we can continue
# NOTE: If this regression error was not stationary in variance, boxcox should be applied to input and output series.
# Try AR(1)7 for seasonal component and AR(2) for regular component?

# 6. Identificar Coeficientes de Transfer Function para Cada Input
TF.Identification.plot(x.tr, TF.fit)
# WD:    b=0, r=0, s=0
# tcold: b=0, r=1, s=0
# thot:  b=0, r=1, s=0


## Tercer Paso: TF con Estructura Seleccionada ----------------------------------

# 7. Ajustar Modelo TF con Órdenes Seleccionados y ARIMA Inicial
TF.fit <- arima(y.tr,
                xtransf = x.tr,
                order = c(2, 1, 0),
                seasonal = list(order = c(1, 0, 0), period = 7),
                transfer = list(c(0, 0), c(1, 0), c(1, 0)),
                method = "ML")

# 8. Revisar Errores de Entrenamiento, Coeficientes y Residuos
summary(TF.fit)
coeftest(TF.fit)
CheckResiduals.ICAI(TF.fit, lag = 50)


## Cuarto Paso: Probar Alternativa MA en Lugar de AR ----------------------------

# 9. Probar Modelo (0,1,2)(1,0,0)[7] con la Misma Estructura TF
TF.fit <- arima(y.tr,
                xtransf = x.tr,
                order = c(0, 1, 2),
                seasonal = list(order = c(1, 0, 0), period = 7),
                transfer = list(c(0, 0), c(1, 0), c(1, 0)),
                method = "ML")

summary(TF.fit)
coeftest(TF.fit)
CheckResiduals.ICAI(TF.fit, lag = 50)
# If residuals are not white noise, change order of ARMA
# Remaning correlations in lags 4 and 5 and 14. Increase orders


## Quinto Paso: Incrementar Órdenes para Mejorar Correlaciones ------------------

# 10. Probar Modelo (0,1,5)(2,0,0)[7]
TF.fit <- arima(y.tr,
                xtransf = x.tr,
                order = c(0, 1, 5),
                seasonal = list(order = c(2, 0, 0), period = 7),
                transfer = list(c(0, 0), c(1, 0), c(1, 0)),
                method = "ML")

summary(TF.fit)
coeftest(TF.fit)
CheckResiduals.ICAI(TF.fit, lag = 50)
# If residuals are not white noise, change order of ARMA
# Correlations are modeled, But many MA terms not significant. Try AR alternative


## Sexto Paso: Alternativa AR para Parte Regular --------------------------------

# 11. Probar Modelo (5,1,0)(2,0,0)[7]
TF.fit <- arima(y.tr,
                xtransf = x.tr,
                order = c(5, 1, 0),
                seasonal = list(order = c(2, 0, 0), period = 7),
                transfer = list(c(0, 0), c(1, 0), c(1, 0)),
                method = "ML")

summary(TF.fit)
coeftest(TF.fit)
CheckResiduals.ICAI(TF.fit, lag = 50)
# All coefficients significant --> Good.
# All correlations are small   --> Good.

# 12. Comprobar Correlación Cruzada Residuos - Variables Explicativas
res <- residuals(TF.fit)
res[is.na(res)] <- 0
ccf(y = res, x = x.tr[, 1])
ccf(y = res, x = x.tr[, 2])
ccf(y = res, x = x.tr[, 3])
########
# X1 seems correlated with residuals -> modify TF


## Séptimo Paso: Ajustar TF para X1 y Modelo Final ------------------------------

# 13. Probar (5,1,0)(2,0,0)[7] Modificando TF de X1
TF.fit <- arima(y.tr,
                xtransf = x.tr,
                order = c(5, 1, 0),
                seasonal = list(order = c(2, 0, 0), period = 7),
                transfer = list(c(0, 1), c(1, 0), c(1, 0)),
                method = "ML")

summary(TF.fit)
coeftest(TF.fit)
CheckResiduals.ICAI(TF.fit, lag = 50)
# All coefficients significant ???
# All correlations are small   --> Good.

# 14. Última Comprobación de Correlación Cruzada Residuos - Inputs
res <- residuals(TF.fit)
res[is.na(res)] <- 0
ccf(y = res, x = x.tr[, 1])  # --> much better
ccf(y = res, x = x.tr[, 2])
ccf(y = res, x = x.tr[, 3])


## Diagnóstico Final del Modelo -------------------------------------------------

# 15. Comparar Serie Real y Valores Ajustados
autoplot(y.tr, series = "Real") +
  forecast::autolayer(fitted(TF.fit), series = "Fitted")

# 16. Medir Errores de Entrenamiento del Modelo
accuracy(fitted(TF.fit), y.tr)

# 17. Diagnóstico Global del Modelo (Ajuste y Residuos)
PlotModelDiagnosis(x.tr, y.tr, fitted(TF.fit), together = TRUE)
```
#### 5. Forecast para Nuevos Datos (h = 7)
> RELLENAR
```r
# 1. Leer Datos de Validación con Nuevos Valores de WD y TEMP
x.tv <- read_excel("DAILY_DEMAND_TV.xlsx")

# 2. Crear Variables de Temperatura Fría y Caliente en Validación
x.tv$tcold <- sapply(x.tv$TEMP, min, 17)
x.tv$thot  <- sapply(x.tv$TEMP, max, 22)

# 3. Convertir a Objeto ts con las Tres Variables de Entrada
x.tv <- ts(x.tv[, c(2, 4, 5)])

# 4. Obtener Pronóstico para Horizonte h = 7 con el Modelo TF Entrenado
val.forecast_h7 <- TF.forecast(y.old  = y.tr,  # Past values of the series
                               x.old  = x.tr,  # Past values of the explanatory variables
                               x.new  = x.tv,  # New values of the explanatory variables
                               model  = TF.fit, # Fitted transfer function model
                               h      = 7)      # Forecast horizon

# 5. Reescalar Pronósticos a la Escala Original
val.forecast_h7 * 100
```

### III. RELLENAR
#### 1. RELLENAR
> RELLENAR
```r
Rellenar
```
#### 2. RELLENAR
> RELLENAR
```r
Rellenar
```
#### 3. RELLENAR
> RELLENAR
```r
Rellenar
```
#### 4. RELLENAR
> RELLENAR
```r
Rellenar
```
#### 5. RELLENAR
> RELLENAR
```r
Rellenar
```

### IV. RELLENAR
#### 1. RELLENAR
> RELLENAR
```r
Rellenar
```
#### 2. RELLENAR
> RELLENAR
```r
Rellenar
```
#### 3. RELLENAR
> RELLENAR
```r
Rellenar
```
#### 4. RELLENAR
> RELLENAR
```r
Rellenar
```
#### 5. RELLENAR
> RELLENAR
```r
Rellenar
```

### V. RELLENAR
#### 1. RELLENAR
> RELLENAR
```r
Rellenar
```
#### 2. RELLENAR
> RELLENAR
```r
Rellenar
```
#### 3. RELLENAR
> RELLENAR
```r
Rellenar
```
#### 4. RELLENAR
> RELLENAR
```r
Rellenar
```
#### 5. RELLENAR
> RELLENAR
```r
Rellenar
```