### I. Previos
#### 1. Carga de Librerías
> Empezamos igual que en el caso anterior
```r
# Librerías
library(MLTools)
library(fpp2)
library(ggplot2)
library(TSA)
library(Hmisc)     # for computing lagged variables
library(lmtest)    # contains coeftest function
library(tseries)   # contains adf.test function
```
#### 2. Directorio
> Igual que en semanas anteriores.
```r
# Setear el Directorio 
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
```

### II. Carga, EDA y Split de los Datos
#### 1. Carga de Datos
> Cargamos el dataset de varios inputs.
```r
# Carga de Datos
fdata <- read.csv("macro_data.csv")
head(fdata)
```
#### 2. EDA
> En este paso realizamos la **exploración visual y estructural de las series**.  
> Definimos la frecuencia temporal (`freq = 4` para datos trimestrales) y convertimos los datos en un objeto `ts`.  
> El argumento `[,-(1:2)]` elimina las dos primeras columnas del `data.frame` (por ejemplo, fechas o índices) dejando solo las variables numéricas (Y, X1, X2).  
> Representamos las series completas y un fragmento inicial para observar patrones o diferencias de escala, analizamos la ACF/PACF de la variable dependiente, y finalmente escalamos las variables para evitar problemas numéricos durante la estimación.
```r
# 0. Objeto TS
freq <- 4
fdata_ts <- ts(fdata[,-(1:2)], frequency = freq) # Quitar Primeras Dos Columnas

# 1. Visualización Global de Ambas Series (Y y X)
autoplot(fdata_ts, facets = TRUE)

# 2. Visualización de las Primeras Observaciones (zoom)
autoplot(head(fdata_ts, 100), facets = TRUE)

# 3. Plot Triple de la Variable Dependiente, su ACF y su PACF
ggtsdisplay(fdata_ts[,1], lag = 15 * freq)

# 4. Escalado de Valores
scale_y <- 1000
scale_x <- c(1000,1)
y <- fdata_ts[ ,1] / scale_y
x1 <- fdata_ts[ , 2] / scale_x[1]
x2 <- fdata_ts[ , 3] / scale_x[2]

# 5. Combinar Variables Escaladas en un Único Objeto TS
x <- cbind(x1, x2)
fdata_ts <- cbind(y, x1, x2)
head(fdata_ts)
```
#### 3. Split Train / Test
> Dividimos las series en **entrenamiento (train)** y **validación (test)** respetando el orden temporal.  
> Reservamos los últimos 12 trimestres para validación y generamos subconjuntos `y.tr` y `x.tr` para el entrenamiento.
```r
# 1. Output Original
y_orig <- fdata_ts[,1]

# 2. Definir Tamaño de Subconjuntos de Entrenamiento y Validación
len_TV <- 12
len_TR <- nrow(fdata_ts) - len_TV

# 3. Crear Índices para Entrenamiento y Validación
ind <- seq(1:nrow(fdata))
ind_TR <- ind <= len_TR
ind_TV <- !ind_TR

# 4. Crear Subconjuntos de Entrenamiento
y.tr <- ts(y[ind_TR], frequency = freq)
x.tr <- ts(x[ind_TR,], frequency = freq)

# 5. Visualizar Series de Entrenamiento
autoplot(cbind(y.tr,x.tr), facets = TRUE)
```
#### 4. Creación del Conjunto de Validación
> Creamos los objetos `ts` para el **periodo de test** (tanto para Y como para X) y los graficamos junto con la parte final del conjunto de entrenamiento para comprobar la continuidad temporal entre ambos periodos.
```r
# 1. Crear Serie TS de Validación para Variable Dependiente
y.tv <- ts(y[ind_TV], frequency = freq,
           start = end(y.tr) + c(0, 1)) 
head(y.tv)

# 2. Crear Serie TS de Validación para Variables Explicativas
x.tv <- ts(x[ind_TV, ], frequency = freq,
           start = end(x.tr) + c(0, 1))
head(x.tv)

# 3. Visualizar Transición entre Entrenamiento y Validación
autoplot(tail(y.tr, 50), series = "Training", color = "blue") + 
  forecast::autolayer(y.tv, series = "Test", color = "red") + 
  geom_vline(xintercept = time(tail(y.tr, 10)), linetype = "dashed", size = 0.5)
```

### III. Identificación de Coeficientes y Ajuste del Modelo
#### 0. Análisis de las Funciones de Correlación y Box Cox
> Hacemos este paso inicial para estimar los posibles coeficientes de nuestros modelos.
```r
# 1. Plot Triple de la Serie, su ACF y su PACF
ggtsdisplay(y.tr, lag=4 * freq)
```
#### 1. Primer Modelo TF
> Estimamos un primer modelo de **Transfer Function (TF)** con estructura sencilla para identificar el retardo (b) y el grado del numerador (s).  
> Ajustamos un modelo preliminar con ruido ARIMA(1, 0, 0) y dos funciones de transferencia (una por cada input), ambas de orden (r = 0, s = 9).  
> Después, analizamos los residuos con `TF.RegressionError.plot()` para verificar si el modelo captura correctamente la dinámica o si es necesario diferenciar la serie.
```r
# 1. Estimación del Modelo Preliminar TF
TF.fit <- arima(y.tr,
                order = c(1, 0, 0),
                # seasonal = list(order=c(1, 0, 0), period=freq),
                xtransf = x.tr,
                transfer = list(c(0, 9), c(0, 9)),
                include.mean = TRUE,
                method = "ML")

# 2. Diagnóstico de los Residuos del Modelo Preliminar (diferencia adicional ?)
TF.RegressionError.plot(y.tr, x.tr, TF.fit, lag.max = 50)            
```
#### 2. Segundo Modelo TF
> En esta segunda estimación introducimos **diferenciación estacional (D = 1)** para capturar mejor la estacionalidad observada en la serie.  
> Ahora pasamos a la forma SARIMA(1,0,0)(1,1,0)[freq] y la misma estructura de las funciones de transferencia (r = 0, s = 9).  
> Tras el ajuste, analizamos nuevamente los residuos, primero con `summary()` y `coeftest()`, y después con `TF.RegressionError.plot()` para comprobar si la serie se ha estabilizado y si la estructura de errores es más cercana a un ruido blanco.
```r
# 1.  Estimación del modelo con diferenciación estacional
TF.fit <- arima(y.tr,
                xtransf = x.tr,
                order=c(1,1,0),
                # seasonal = list(order=c(1,0,0),period=freq),
                transfer = list(c(0,9),c(0,9)),
                method="ML")

# 2. Resumen General y Significancia de los Coeficientes del Modelo
summary(TF.fit)
coeftest(TF.fit)

# 3. Diagnóstico de los Residuos del Modelo Diferenciado (ha mejorado ?)
TF.RegressionError.plot(y.tr, x.tr, TF.fit, lag.max = 50)
# NOTE: Si el error de esta regresión no es estacionario en varianza, hay que aplicar Box-Cox a las series de entrada y de salida.
```
#### 3. Identificación de los Parámetros de la Función de Transferencia
> Este paso permite **determinar los parámetros b, r y s** de la función de transferencia para cada $x_i$.
> 	- **b**: número de coeficientes iniciales no significativos → indica el **retardo** de la respuesta de Y respecto a X.
> 	- **r**: grado del polinomio en el denominador → representa la **suavización o decaimiento** de la respuesta.  
> 	- **s**: número de coeficientes significativos antes de que los efectos desaparezcan → mide la **duración del impacto** de X sobre Y.
> Utilizamos `TF.Identification.plot()` para visualizar los coeficientes estimados y así ajustar estos valores antes del modelo final.
```r
# 1. Identificación visual de los parámetros TF
TF.Identification.plot(x.tr, TF.fit)

# 2. Definición inicial de los órdenes (ajustar según los resultados del gráfico)
p <- 0 ; d <- 1; q <- 1;
P <- 0 ; D <- 0; Q <- 0;

b1 <- 0; r1 <- 1; s1 <- 0;  
b2 <- 0; r2 <- 0; s2 <- 0;
```
#### 4. Ajuste del modelo ARIMA con los parámetros seleccionados
> En este paso ajustamos el **modelo final de función de transferencia (TF)** con los valores de b,r,s obtenidos en la fase anterior (para cada input) y con los órdenes SARIMA (p,d,q)(P,D,Q) definidos para el ruido. Primero generamos la variable explicativa rezagada `xlag` según el valor de **b**, y después estimamos el modelo completo combinando la parte dinámica (ruido ARIMA) y la parte explicativa (transfer functions).
```r
# 1. Crear las Variables Explicativas con los Lags Seleccionados
xlag <- x.tr
xlag[, 1] <- Lag(x.tr[, 1], b1)
xlag[, 2] <- Lag(x.tr[, 2], b2)
xlag[is.na(xlag)] = 0

# 2. Ajuste del Modelo Final ARIMA con 2 Funciones de Transferencia
arima.fit <- arima(y.tr,
                   order = c(p, d, q),
                   seasonal = list(order=c(P, D, Q), period=freq),
                   xtransf = xlag,
                   transfer = list(c(r1, s1), c(r2, s2)),
                   method = "ML")
```
#### 5. Diagnóstico del Modelo
> Evaluamos la calidad del modelo y la validez de los supuestos estadísticos.
> 	- `summary()` muestra los coeficientes estimados y el error residual.
> 	- `coeftest()` verifica la **significancia estadística** de los parámetros.
> 	- `CheckResiduals.ICAI()` permite analizar si los residuos se comportan como **ruido blanco**, condición necesaria para considerar el modelo adecuado.
```r
# 1. Resumen General del Modelo Ajustado
summary(arima.fit) 

# 2. Prueba de Significancia de los Coeficientes
coeftest(arima.fit)

# 3. Diagnóstico de los Residuos (ruido blanco ?)
CheckResiduals.ICAI(arima.fit, lag=50)
```
#### 6. Análisis de Residuos y Calidad del Ajuste
> Este análisis permite comprobar si **queda correlación entre los residuos y las variables Xi**.  
> Si los residuos están correctamente modelados, la CCF debería mostrar valores cercanos a cero en todos los retardos. Una correlación significativa indicaría que **el modelo no captura completamente la relación dinámica** entre el output y los inputs.
> Comparamos visualmente los valores ajustados del modelo con los valores reales para verificar **la calidad del ajuste** durante el periodo de entrenamiento. Una buena superposición indica que el modelo captura adecuadamente el patrón general y la estacionalidad de la serie.
```r
# 1. Calcular Residuos del Modelo
res <- residuals(arima.fit)
res[is.na(res)] <- 0

# 2. Analizar Correlación Cruzada entre Residuos y Variables X
ccf(y = res, x = x.tr[,1])
ccf(y = res, x = x.tr[,2])

# 3. Graficar Serie Real frente a Serie Ajustada del Modelo
autoplot(y.tr, series = "Real", size = 2, alpha = 0.8, color = "blue")+
  forecast::autolayer(fitted(arima.fit), series = "Fitted", color = "yellow")
```

### IV. Predicción de Datos Futuros
#### 1. Predicción de Horizonte 1
> Generamos predicciones de un paso adelante (**h = 1**) dentro del periodo de validación.  
> En cada iteración, usamos todos los datos disponibles hasta ese momento y predecimos el siguiente valor.
```r
# 1. Inicializar Horizonte y Vector de Predicciones en Validación
h <- 1
y.tv.est <- y * NA

# 2. Bucle Rolling: en cada paso predecimos 1 paso adelante (h=1)
for (i in seq(length(y.tr) + 1, length(y) - h, 1)){
  y.tv.est[i] <- TF.forecast(y.old = subset(y, end=i-1),
                            x.old = subset(x, end=i-1), 
                            x.new = subset(x, start=i, end=i), 
                            model = arima.fit, 
                            h=h)[h] 
}

# 3. Limpiar NAs del Vector de Predicciones
y.tv.est <- na.omit(y.tv.est)
```
#### 2. Predicción Directa Multi-Step
> Calculamos ahora un **forecast directo** para todo el periodo de validación, proyectando simultáneamente los próximos valores según el horizonte total `length(y.TV)`.
```r
# 1. Inicializar Vector de Predicciones en Validación
y.tv.est2 <- y * NA

# 2. Predicción Directa para Todo el Horizonte de Validación  
y.tv.est2 <- TF.forecast(y.old = y.tr, 
                        x.old = x.tr, 
                        x.new = x.tv, 
                        model = arima.fit, 
                        h = length(y.tv))  
  
# 3. Limpiar NAs del Vector de Predicciones
y.tv.est2 <- na.omit(y.tv.est2)                 
```
#### 3. Plot del Forecast
> Representamos las predicciones frente a los valores reales y calculamos métricas de error (**MAE, RMSE, MAPE**). Esto permite comparar el rendimiento de ambos enfoques (rolling y directo).
```r
# 1. Crear Objetos TS para Valores Reales y Predichos
y.tv_ts <- ts(y.tv, frequency = freq, start = end(y.tr) + c(0, 1))
y.tv.est_ts <- ts(y.tv.est, frequency = freq, start = end(y.tr) + c(0, 1))

# 2. Crear Objeto TS para Predicción Directa
y.tv.est2_ts <- ts(y.tv.est2, frequency = freq, start = end(y.tr) + c(0, 1))
head(y.tv_ts)

# 3. Graficar Valores Reales, Predicciones y Datos de Entrenamiento
autoplot(y.tv_ts, series="Test set, real values", size=2, alpha=0.5, color="blue") +
  forecast::autolayer(y.tv.est_ts, series = "Forecast", color = "yellow") + 
  forecast::autolayer(y.tv.est2_ts, series = "Direct Forecast", color = "tan") +
  forecast::autolayer(tail(y.tr, freq), series = "Training data", color = "red") 
  
# 4. Calcular Métricas de Precisión de Ambas Estrategias
accuracy(y.tv.est * 100000, y.tv * 100000)
accuracy(y.tv.est2 * 100000, y.tv * 100000)
```
