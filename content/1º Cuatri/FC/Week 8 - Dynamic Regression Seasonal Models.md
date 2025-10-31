### I. Previos

#### 1. Carga de Librerías
> Esta vez añadiremos las siguientes librerías:
> - **library(TSA)** / **library(astsa)**: soporte para **transfer functions** (Pankratz) y utilidades de CCF/prewhitening.
> - **library(Hmisc)**: `Lag()` para crear lags manteniendo el índice temporal (útil al alinear entradas/salida).
```r
# Librerías
library(MLTools)
library(fpp2)
library(ggplot2)
library(TSA)
library(Hmisc) # for computing lagged variables
library(lmtest)  #contains coeftest function
library(tseries) #contains adf.test function
```
#### 2. Directorio
> Igual que en semanas anteriores: ajusta automáticamente al directorio del script activo.
```r
# Setear el Directorio 
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))`
```

### II. Carga, EDA y Split de los Datos
#### 1. Carga de Datos
> Cargamos el dataset con **Y** (output) y **X** (input).  
> Renombramos columnas si hace falta para mantener consistencia con el resto de semanas.
```r
# 1. Carga de Datos
fdata <- read.table("Seasonal_TF_1.dat", header = TRUE, sep = "")
head(fdata)

# 2. Renombrar Columnas
colnames(fdata) <- c("Y","X")
```
#### 2. EDA
> En esta fase hacemos una exploración visual de las series para detectar **tendencia, estacionalidad** y posibles diferencias de escala.  
> Convertimos los datos a un objeto `ts` con frecuencia 24, representamos las series completas y un fragmento inicial para observar su comportamiento, y analizamos la **autocorrelación** de Y mediante `ggtsdisplay()`.  
> Finalmente, escalamos ambas variables para facilitar la identificación del modelo y evitar problemas numéricos.
```r
# 0. Objeto TS
freq <- 24
fdata_ts <- ts(fdata, frequency = freq)

# 1. Visualización Global de Ambas Series (Y y X)
autoplot(fdata_ts, facets = TRUE)

# 2. Visualización de las Primeras Observaciones (zoom)
autoplot(head(fdata_ts, 100), facets = TRUE)

# 3. Plot Triple de la Variable Dependiente, su ACF y su PACF
ggtsdisplay(fdata_ts[,1], lag = 5 * freq)

# 4. Escalado de Valores
y <- fdata_ts[,1] / 100000
x <- fdata_ts[,2] / 100000
```
#### 3. Split Train / Test
> Dividimos las series en **conjunto de entrenamiento (Train)** y **validación (Test)** respetando el orden temporal.  
> Reservamos los últimos cuatro ciclos estacionales (`4 * freq`) para la validación, lo que permite evaluar el rendimiento del modelo en datos no utilizados durante el ajuste.
```r
# 0. Tamaño del Split
test_size = 4 * freq

# 1. Train
y.TR <- subset(y, end = length(y) - test_size)
x.TR <- subset(x, end = length(y) - test_size)

# 2. Test
y.TV <- subset(y, start = length(y) - test_size + 1)
x.TV <- subset(x, start = length(y) - test_size + 1)

# 3. Comprobación
tail(y.TR)
head(y.TV)
```

### III. Identificación de Coeficientes y Ajuste del Modelo
#### 0. Análisis de las Funciones de Correlación
> Hacemos este paso inicial para estimar los posibles coeficientes de nuestros modelos.
```r
# Plot Triple de la Serie, su ACF y su PACF
ggtsdisplay(y, lag=4 * freq)
```
#### 1. Primer Modelo TF
> Estimamos un primer modelo de **Transfer Function (TF)** con estructura sencilla para identificar el retardo (b) y el grado del numerador (s).  
> Ajustamos un modelo preliminar con ruido SARIMA(1,0,0)(1,0,0)[freq] y una función de transferencia de orden (r=0, s=9).  
> Después, analizamos los residuos con `TF.RegressionError.plot()` para verificar si el modelo captura correctamente la dinámica o si es necesario diferenciar la serie.
```r
# 1. Estimación del Modelo Preliminar TF
TF.fit <- arima(y.TR,
                order = c(1, 0, 0),
                seasonal = list(order=c(1, 0, 0), period=freq),
                xtransf = x.TR,
                transfer = list(c(0, 9)), #List with (r,s) orders
                include.mean = TRUE,
                method = "ML")

# 2. Diagnóstico de los Residuos del Modelo Preliminar (diferencia adicional ?)
TF.RegressionError.plot(y, x, TF.fit, lag.max = 100)                
```
#### 2. Segundo Modelo TF
> En esta segunda estimación introducimos **diferenciación estacional (D = 1)** para capturar mejor la estacionalidad observada en la serie.  
> Mantenemos la forma SARIMA(1,0,0)(1,1,0)[freq] anterior y la misma estructura de función de transferencia (r = 0, s = 9).  
> Tras el ajuste, analizamos nuevamente los residuos con `TF.RegressionError.plot()` para comprobar si la serie se ha estabilizado y si la estructura de errores es más cercana a un ruido blanco.
```r
# 1.  Estimación del modelo con diferenciación estacional
TF.fit <- arima(y.TR,
                order = c(1, 0, 0),
                seasonal = list(order=c(1, 1, 0), period=freq),
                xtransf = x.TR,
                transfer = list(c(0, 9)), #List with (r,s) orders
                include.mean = TRUE,
                method = "ML")

# 2. Diagnóstico de los Residuos del Modelo Diferenciado (ha mejorado ?)
TF.RegressionError.plot(y, x, TF.fit, lag.max = 100)
```
#### 3. Identificación de los Parámetros de la Función de Transferencia
> Este paso permite **determinar los parámetros b, r y s** de la función de transferencia.
> 	- **b**: número de coeficientes iniciales no significativos → indica el **retardo** de la respuesta de Y respecto a X.
> 	- **r**: grado del polinomio en el denominador → representa la **suavización o decaimiento** de la respuesta.  
> 	- **s**: número de coeficientes significativos antes de que los efectos desaparezcan → mide la **duración del impacto** de X sobre Y.
> Utilizamos `TF.Identification.plot()` para visualizar los coeficientes estimados y así ajustar estos valores antes del modelo final.
```r
# 1. Identificación visual de los parámetros TF
TF.Identification.plot(x,TF.fit)

# 2. Definición inicial de los órdenes (ajustar según los resultados del gráfico)
p <- 0 ; d <- 0; q <- 1;
P <- 1 ; D <- 1; Q <- 0;

b <- 0; r <- 0; s <- 0;
```
#### 4. Ajuste del modelo ARIMA con los parámetros seleccionados
> En este paso ajustamos el **modelo final de función de transferencia (TF)** con los valores de b,r,s obtenidos en la fase anterior y con los órdenes ARIMA (p,d,q)(P,D,Q) definidos para el ruido.  
> Primero generamos la variable explicativa rezagada `xlag` según el valor de **b**, y después estimamos el modelo completo combinando la parte dinámica (ruido ARIMA) y la parte explicativa (transfer function).
```r
# 1. Crear la Variable Explicativa con el Lag Seleccionado
xlag = Lag(x, b)  
xlag[is.na(xlag)]=0

# 2. Ajuste del Modelo Final ARIMA con Función de Transferencia
arima.fit <- arima(y,
                   order=c(p, d, q),
                   seasonal = list(order=c(P, D, Q), period=freq),
                   xtransf = xlag,
                   transfer = list(c(r, s)), #List with (r,s) orders
                   include.mean = FALSE,
                   method="ML")
```
#### 5. Diagnóstico del Modelo
> Evaluamos la calidad del modelo y la validez de los supuestos estadísticos.
> 	- `summary()` muestra los coeficientes estimados y el error residual.
> 	- `coeftest()` verifica la **significancia estadística** de los parámetros.
> 		- `CheckResiduals.ICAI()` permite analizar si los residuos se comportan como **ruido blanco**, condición necesaria para considerar el modelo adecuado.
```r
# 1. Resumen General del Modelo Ajustado
summary(arima.fit) 

# 2. Prueba de Significancia de los Coeficientes
coeftest(arima.fit)

# 3. Diagnóstico de los Residuos (ruido blanco ?)
CheckResiduals.ICAI(arima.fit, lag=50)
```
#### 6. Análisis de Residuos y Calidad del Ajuste
> Este análisis permite comprobar si **queda correlación entre los residuos y la variable X**.  
> Si los residuos están correctamente modelados, la CCF debería mostrar valores cercanos a cero en todos los retardos. Una correlación significativa indicaría que **el modelo no captura completamente la relación dinámica** entre Y y X.
> Comparamos visualmente los valores ajustados del modelo con los valores reales para verificar **la calidad del ajuste** durante el periodo de entrenamiento. Una buena superposición indica que el modelo captura adecuadamente el patrón general y la estacionalidad de la serie.
```r
# 1. Calcular Residuos del Modelo
res <- residuals(arima.fit)
res[is.na(res)] <- 0

# 2. Analizar Correlación Cruzada entre Residuos y Variable X
ccf(y = res, x = x)

# 3. Graficar Serie Real frente a Serie Ajustada del Modelo
autoplot(y, series = "Real", size = 2, alpha = 0.8, color = "blue") +
  forecast::autolayer(fitted(arima.fit), series = "Fitted", color = "yellow")
```
### IV. Predicción de Datos Futuros
#### 1. Predicción de Horizonte 1
> Generamos predicciones de un paso adelante (**h = 1**) dentro del periodo de validación.  
> En cada iteración, usamos todos los datos disponibles hasta ese momento y predecimos el siguiente valor.
```r
# 1. Inicializar Horizonte y Vector de Predicciones en Validación
h <- 1
y.TV.est <- y * NA

# 2. Bucle Rolling: en cada paso predecimos 1 paso adelante (h=1)
for (i in seq(length(y.TR) + 1, length(y) - h, 1)){
  y.TV.est[i] <- TF.forecast(y.old = subset(y,end=i-1), 
                            x.old = subset(x,end=i-1), 
                            x.new = subset(x,start = i,end=i), 
                            model = arima.fit, 
                            h = h)[h] 
}

# 3. Limpiar NAs del Vector de Predicciones
y.TV.est <- na.omit(y.TV.est)
```
#### 2. Predicción Directa Multi-Step
> Calculamos ahora un **forecast directo** para todo el periodo de validación, proyectando simultáneamente los próximos valores según el horizonte total `length(y.TV)`.
```r
# 1. Inicializar Vector de Predicciones en Validación
y.TV.est2 <- y * NA

# 2. Predicción Directa para Todo el Horizonte de Validación
y.TV.est2 <- TF.forecast(y.old = y.TR, 
                        x.old = x.TR, 
                        x.new = x.TV,  
                        model = arima.fit, 
                        h = length(y.TV))
  
# 3. Limpiar NAs del Vector de Predicciones
y.TV.est2 <- na.omit(y.TV.est2)
```
#### 3. Plot del Forecast
> Representamos las predicciones frente a los valores reales y calculamos métricas de error (**MAE, RMSE, MAPE**). Esto permite comparar el rendimiento de ambos enfoques (rolling y directo).
```r
# 1. Crear Objetos TS para Valores Reales y Predichos
y.TV_ts <- ts(y.TV, frequency = freq, start = end(y.TR) + c(0, 1))
y.TV.est_ts <- ts(y.TV.est, frequency = freq, start = end(y.TR) + c(0, 1))

# 2. Crear Objeto TS para Predicción Directa
y.TV.est2_ts <- ts(y.TV.est2, frequency = freq, start = end(y.TR) + c(0, 1))
head(y.TV_ts)

# 3. Graficar Valores Reales, Predicciones y Datos de Entrenamiento
autoplot(y.TV_ts, series="Test set, real values", size=2, alpha=0.5, color="blue") +
  forecast::autolayer(y.TV.est_ts, series = "Forecast", color = "yellow") + 
  forecast::autolayer(y.TV.est2_ts, series = "Direct Forecast", color = "tan") +
  forecast::autolayer(tail(y.TR, freq), series = "Training data", color = "red") 
  
# 4. Calcular Métricas de Precisión de Ambas Estrategias
accuracy(y.TV.est * 100000, y.TV * 100000)
accuracy(y.TV.est2 * 100000, y.TV * 100000)
```


> [!summary]  Checklist Final
> - ¿(d, D) son mínimos y suficientes para **lograr estacionariedad**?
> - ¿El retardo **b (lag)** está justificado (por CCF, prewhitening o TF preliminar)?
> - ¿Los **residuos** se comportan como **ruido blanco** y no muestran correlación con X?
> - ¿El modelo es **parsimonioso** (ω(B) y δ(B) simples) y **estable**?
> - ¿Los **pronósticos** en el conjunto de test son **coherentes y razonables**?












