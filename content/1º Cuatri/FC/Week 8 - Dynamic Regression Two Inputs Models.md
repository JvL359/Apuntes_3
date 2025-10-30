### I. Previos

#### 1. Carga de Librerías
> Empezamos igual que en el caso anterior
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
> Igual que en semanas anteriores.
```r
# Setear el Directorio 
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))`
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
fdata_ts <- ts(fdata[,-(1:2)], frequency = freq) # EXPLICAR: [,-(1:2)]

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
#### 4. RELLENAR
> Creamos los objetos `ts` para el **periodo de test** (tanto para Y como para X) y los graficamos junto con la parte final del conjunto de entrenamiento para comprobar la continuidad temporal entre ambos periodos.
```r
# 1. Crear Serie TS de Validación para Variable Dependiente
y.ts <- ts(y[ind_TV], frequency = freq,
           start = end(y.tr) + c(0,1)) 
head(y.ts)

# 2. Crear Serie TS de Validación para Variables Explicativas
x.ts <- ts(x[ind_TV,], frequency = freq,
           start = end(x.tr) + c(0,1))
head(x.ts)

# 3. Visualizar Transición entre Entrenamiento y Validación
autoplot(tail(y.tr, 50), series = "Training", color="blue") + 
  forecast::autolayer(y.ts, series = "Test", color = "red") + 
  geom_vline(xintercept = time(tail(y.tr, 10)), linetype="dashed", size=0.5)
```

### Proceso de Identificación de Coeficientes
#### 0. Análisis de las Funciones de Correlación
> Hacemos este paso inicial para estimar los posibles coeficientes de nuestros modelos.
```r
# Plot Triple de la Serie, su ACF y su PACF
ggtsdisplay(y, lag=4 * freq)
```
#### 1. Primer Modelo TF
> RELLENAR
```r
# 1. RELLENAR
TF.fit <- arima(y.TR,
                order=c(1, 0, 0),
                seasonal = list(order=c(1, 0, 0), period=freq),
                xtransf = x.TR,
                transfer = list(c(0,9)), #List with (r,s) orders
                include.mean = TRUE,
                method="ML")

# 2. RELLENAR
# Check regression error to see the need of differentiation
TF.RegressionError.plot(y,x,TF.fit,lag.max = 100)                
```
#### 2. Segundo Modelo TF
> RELLENAR
```r
# 1. RELLENAR
TF.fit <- arima(y.TR,
                order=c(1, 0, 0),
                seasonal = list(order=c(1, 1, 0), period=freq),
                xtransf = x.TR,
                transfer = list(c(0,9)), #List with (r,s) orders
                include.mean = TRUE,
                method="ML")

# 2. RELLENAR
TF.RegressionError.plot(y,x,TF.fit,lag.max = 100)
```
#### 3. Identificación de los Parámetros de la Función de Transferencia
> RELLENAR/COMPLETAR/MEJORAR
> Identificar b, r, s
> b: cuantos no significativos
> r: grado del decaimiento
> s: cuantos significativos antes de la caída
```r
# 1. RELLENAR
TF.Identification.plot(x,TF.fit)

# 2. RELLENAR
p <- 0 ; d <- 0; q <- 1;
P <- 1 ; D <- 1; Q <- 0;

b <- 0; r <- 0; s <- 0;
```
#### 4. TRADUCIR: Fit arima noise with the selected (b, r, s) and ARMA orders
> RELLENAR
```r
# 1. RELLENAR
xlag = Lag(x, b)  
xlag[is.na(xlag)]=0

# 2. RELLENAR
arima.fit <- arima(y,
                   order=c(p, d, q),
                   seasonal = list(order=c(P, D, Q), period=freq),
                   xtransf = xlag,
                   transfer = list(c(r, s)), #List with (r,s) orders
                   include.mean = FALSE,
                   method="ML")
```
#### 5. Diagnóstico del Modelo
> RELLENAR
```r
# 1. RELLENAR
summary(arima.fit) # summary of training errors and estimated coefficients

# 2. RELLENAR
coeftest(arima.fit)

# 3. RELLENAR
CheckResiduals.ICAI(arima.fit, lag=50)
```
#### 6. TRADUCIR: Cross correlation between the residuals and the explanatory variable
> RELLENAR
```r
# RELLENAR
res <- residuals(arima.fit)
res[is.na(res)] <- 0
ccf(y = res, x = x)
```
#### 7. TRADUCIR: Visual check of the fitted values vs real values in the training period
> RELLENAR
```r
# RELLENAR
autoplot(y, series = "Real", size = 2, alpha=0.8, color="blue") +
  forecast::autolayer(fitted(arima.fit), series = "Fitted", color="yellow")
```

### Predicción de Datos Futuros
#### 1. RELLENAR
> RELLENAR
```r
# 1. Inicializar Horizonte y Vector de Predicciones en Validación
h <- 1
y.TV.est <- y * NA

# 2. Bucle Rolling: en cada paso predecimos 1 paso adelante (h=1)
for (i in seq(length(y.TR) + 1, length(y) - h, 1)){# loop for validation period
  y.TV.est[i] <- TF.forecast(y.old = subset(y,end=i-1), #past values of the series
                             x.old = subset(x,end=i-1), #Past values of the explanatory variables
                             x.new = subset(x,start = i,end=i), #New values of the explanatory variables
                             model = arima.fit, #fitted transfer function model
                             h=h)[h] #Forecast horizon
}

# 3. RELLENAR
y.TV.est <- na.omit(y.TV.est)
```
#### 2. RELLENAR
> RELLENAR
```r
# RELLENAR
y.TV.est2 <- TF.forecast(y.old = subset(y,end=i-1), #past values of the series
                             x.old = subset(x,end=i-1), #Past values of the explanatory variables
                             x.new = subset(x,start = i,end=i), #New values of the explanatory variables
                             model = arima.fit, #fitted transfer function model
                             h=length(y.TV)) #forecast horizon
```
#### 3. Plot del Forecast
> RELLENAR
```r
# 1. RELLENAR
y.TV_ts <- ts(y.TV, frequency = freq, start = end(y.TR) + c(0, 1))
y.TV.est_ts <- ts(y.TV.est, frequency = freq, start = end(y.TR) + c(0, 1))

# 2. RELLENAR
y.TV.est2_ts <- ts(y.TV.est2, frequency = freq, start = end(y.TR) + c(0, 1))
head(y.TV_ts)

# 3. RELLENAR
autoplot(y.TV_ts, series = "Test set, real values", size=2, alpha=0.5, color="blue") +
  forecast::autolayer(y.TV.est_ts, series = "Forecast", color = "yellow") + 
  forecast::autolayer(y.TV.est2_ts, series = "Direct Forecast", color = "tan") +
  forecast::autolayer(tail(y.TR, freq), series = "Training data", color = "red") 
  
# 4. RELLENAR
accuracy(y.TV.est*100000,y.TV*100000)
accuracy(y.TV.est2*100000,y.TV*100000)
```
