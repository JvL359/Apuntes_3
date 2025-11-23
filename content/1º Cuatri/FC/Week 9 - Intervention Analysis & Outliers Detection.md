### I. Previos
#### 1. Carga de Librerías
> RELLENAR
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
> RELLENAR
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
#### 2. RELLENAR
> RELLENAR
```r
# 1. RELLENAR
ggtsdisplay(yLS, main="Time Series with LS")

# 2. RELLENAR
ggtsdisplay(diff(yLS), main="Time Series with LS")

# 3. RELLENAR
yLS_arima <- Arima(yLS, order = c(4, 1, 0), include.mean = FALSE)

# 4. RELLENAR
summary(yLS_arima)
coeftest(yLS_arima)
CheckResiduals.ICAI(yLS_arima)

# 5. RELLENAR
autoplot(residuals(yLS_arima)) + ggtitle("Residuals of LS ARIMA Model")

# 6. RELLENAR
boxplot(residuals(yLS_arima), main = "Residuals of Baseline ARIMA Model")
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

Los apuntes continúan en [[Week 10 - Non Linear Models]]