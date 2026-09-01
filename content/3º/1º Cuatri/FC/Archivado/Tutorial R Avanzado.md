### II. Avanzado

1. Introducción a Series Temporales en R
> Una **serie temporal** es un conjunto de observaciones recogidas en intervalos regulares de tiempo (diarios, mensuales, trimestrales, anuales, etc.). El análisis de series temporales busca identificar patrones como **tendencia**, **estacionalidad** y **ciclos**, además de la parte aleatoria. En R, trabajaremos principalmente con los objetos `ts` (base R) y `xts`/`zoo` (paquetes especializados), que permiten estructurar los datos de forma temporal y aplicar métodos de análisis y pronóstico.  
> Esta sección introduce cómo **crear**, **visualizar** y **descomponer** series temporales, lo cual es el primer paso antes de aplicar modelos como ARMA o ARIMA.
###### 1.1. Creación de Series Temporales
> En R, una tarea inicial con series temporales es convertir los datos en objetos que respeten la dimensión temporal. El formato básico es **ts**, que define inicio y frecuencia (ej. 12 mensual, 4 trimestral, 1 anual) y sirve de base para modelos como ARIMA o suavizamiento exponencial. Para datos con fechas irregulares o huecos, son más útiles **xts** o **zoo**, que trabajan con índices Date o POSIXct. Zoo amplió el manejo de series temporales y xts lo perfecciona para análisis financieros y uso con quantmod. En la práctica, **ts** basta con datos regulares, mientras que **xts** y zoo son preferibles en contextos financieros o económicos.
```r
## Ejemplo de creación de series temporales en R

# Cargar librerías necesarias
library(xts)
library(zoo)

## 1. Objeto ts (base R)
# Serie mensual de desempleo desde enero 2010
# (ejemplo similar al usado en clase con datos de España)
y <- ts(fdata$TOTAL, start = c(2010,1), frequency = 12)

# Serie trimestral ficticia desde 2005
z <- ts(c(5,6,7,8,9,10), start = c(2005,1), frequency = 4)

## 2. Objeto zoo
# Creamos una serie con fechas exactas como índice
fechas <- as.Date(c("2020-01-01","2020-02-01","2020-03-01"))
valores <- c(100, 120, 110)
serie_zoo <- zoo(valores, fechas)

## 3. Objeto xts
# Similar a zoo, pero optimizado para análisis financiero
serie_xts <- xts(valores, order.by = fechas)

## Visualización rápida
plot(y, main="Serie ts: mensual", ylab="Valor")
plot(serie_zoo, main="Serie zoo: índice de fechas")
plot(serie_xts, main="Serie xts: datos financieros")
```
###### 1.2. Componentes de una serie temporal
> Una serie temporal combina varios componentes clave para describir sus patrones: **tendencia** (movimiento de largo plazo), **estacionalidad** (repetición regular en intervalos fijos), **ciclos** (fluctuaciones más largas e irregulares) y **ruido** (parte aleatoria no explicada). Estos pueden representarse en un modelo **aditivo** (los efectos se suman) o **multiplicativo** (los efectos se combinan proporcionalmente). Normalmente, series con variabilidad constante se tratan de forma aditiva, mientras que aquellas con variabilidad creciente se modelan multiplicativamente.
```r
## Ejemplo conceptual de descomposición en R

library(fpp2)

# Usamos datos de pasajeros aéreos (AirPassengers)
y <- AirPassengers

# Descomposición aditiva
y_add <- decompose(y, type = "additive")

# Descomposición multiplicativa
y_mult <- decompose(y, type = "multiplicative")

# Visualización de componentes
autoplot(y_add) + ggtitle("Descomposición aditiva")
autoplot(y_mult) + ggtitle("Descomposición multiplicativa")
```
###### 1.3. Visualización inicial
> Antes de aplicar modelos, siempre conviene **graficar la serie temporal**. Las visualizaciones permiten identificar rápidamente si existen **tendencias, estacionalidad o cambios de nivel**. En R se puede usar tanto la función base `plot.ts()` como `autoplot()` del paquete **fpp2/ggplot2**, que ofrece mayor personalización y mejor estética.
```r
library(fpp2)

# Serie de desempleo en España (ejemplo)
y <- ts(fdata$TOTAL, start = c(2010,1), frequency = 12)

# Visualización con autoplot
autoplot(y) +
  ggtitle("Unemployment in Spain") +
  xlab("Year") + ylab("Number unemployed")

# Alternativa base R
plot.ts(y, main="Unemployment in Spain",
        xlab="Year", ylab="Number unemployed")
```
###### 1.4. Selección de Intervalos (window)
> Muchas veces no interesa analizar toda la serie disponible, sino un período específico. Con la función `window()` podemos extraer un subconjunto temporal de un objeto `ts`, indicando la fecha de inicio y fin. Esto resulta útil, por ejemplo, para centrarse en los últimos años de datos antes de ajustar un modelo de pronóstico.
```r
library(fpp2)

# Serie completa de desempleo mensual desde 2010
y <- ts(fdata$TOTAL, start = c(2010,1), frequency = 12)

# Extraer sólo el periodo 2015-2019
y_sub <- window(y, start = c(2015,1), end = c(2019,12))

# Comparación visual
autoplot(y, series = "Serie completa") +
  forecast::autolayer(y_sub, series = "2015-2019") +
  ggtitle("Selección de intervalos con window()") +
  xlab("Year") + ylab("Number unemployed")
```

2. Métodos de Descomposición
> La **descomposición** de una serie temporal consiste en separar sus componentes principales:
> - **Tendencia (τ)** → movimiento de largo plazo.
> - **Estacionalidad (σ)** → patrones repetitivos en intervalos regulares.
> - **Irregularidad (e)** → ruido aleatorio.
> Esto facilita entender cómo evoluciona la serie y preparar los datos para el modelado. Existen distintos enfoques: la **descomposición clásica** (aditiva o multiplicativa), el método **STL** (Seasonal-Trend decomposition using Loess) y procedimientos más avanzados como **X-13ARIMA-SEATS** implementados en el paquete `seasonal`. Cada uno ofrece distintas ventajas en cuanto a flexibilidad y robustez frente a cambios estructurales.
###### 2.1. Descomposición Clásica
> La descomposición clásica es el enfoque más sencillo y se basa en separar una serie temporal en **tendencia, estacionalidad y residuo**. Se aplica bajo dos supuestos:
> - **Aditiva:** $y(t) = \tau(t) + \sigma(t) + e(t)$
> 	 Si la estacionalidad es **constante en magnitud**.
> - **Multiplicativa:** $y(t) = \tau(t) \times \sigma(t) \times e(t)$
> 	Usa multiplicativa si la estacionalidad **aumenta con el nivel de la serie**.
> 	(más común en series económicas, donde la estacionalidad crece con el nivel de la serie).
```r
library(fpp2)
library(ggplot2)

# Cargar datos de desempleo (ejemplo Lab 1)
fdata <- read.table("Unemployment.dat", sep = ",", header = TRUE)
fdata$DATE <- as.Date(fdata$DATE, format = "%d/%m/%Y")

# Convertir a serie mensual desde 2010
y <- ts(fdata$TOTAL, start = c(2010,1), frequency = 12)

# Descomposición aditiva
y_dec_add <- decompose(y, type = "additive")
autoplot(y_dec_add) + ggtitle("Descomposición Aditiva")

# Descomposición multiplicativa
y_dec_mult <- decompose(y, type = "multiplicative")
autoplot(y_dec_mult) + ggtitle("Descomposición Multiplicativa")
```
###### 2.2. Descomposición SEATS
> **SEATS (Seasonal Extraction in ARIMA Time Series)** es un método avanzado basado en modelos ARIMA, implementado en R con el paquete `seasonal`. La ventaja es que estima los componentes con más flexibilidad y suele ajustarse mejor que la descomposición clásica.
```r
library(seasonal)

# Descomposición SEATS
y_dec_seas <- seas(y)
autoplot(y_dec_seas) +
  ggtitle("SEATS Decomposition")
```
###### 2.3. X11/X13-ARIMA
> Los métodos **X11/X13** (del U.S. Census Bureau) son muy usados en macroeconomía y estadísticas oficiales. También son iterativos y refinan la extracción de tendencia y estacionalidad. 
> En R, también se implementan con `seasonal` (opción `"x11"` o `"x13"`).
> En práctica profesional, SEATS y X11 suelen preferirse sobre la descomposición clásica porque manejan mejor **outliers, efectos de calendario y series económicas reales**.
```r
# Descomposición con X11
y_dec_x11 <- seas(y, x11 = "")
autoplot(y_dec_x11) +
  ggtitle("X11 Decomposition")
```
###### 2.4. Ajuste Estacional y Comparación
> Una vez descompuesta la serie, podemos extraer componentes y comparar distintos métodos. Esto permite ver cómo cada método elimina la estacionalidad y deja una serie más estable para modelar.
```r
# Serie ajustada estacionalmente (remove seasonality)
autoplot(seasadj(y_dec_add), series = "Aditiva") +
  autolayer(seasadj(y_dec_mult), series = "Multiplicativa") +
  autolayer(seasadj(y_dec_seas), series = "SEATS") +
  ggtitle("Comparación de Ajustes Estacionales")
```

3. Modelos ARMA
> Los **modelos ARMA (Autoregressive Moving Average)** combinan dos componentes:
> - **AR (Autoregresivo):** el valor actual depende de valores pasados de la propia serie.
> - **MA (Media móvil):** el valor actual depende de errores pasados (ruido).
> Un modelo **ARMA(p,q)** tiene la forma: $y_t = c + \phi_1 y_{t-1} + \cdots + \phi_p y_{t-p} + \theta_1 e_{t-1} + \cdots + \theta_q e_{t-q} + e_t$
> Se utilizan principalmente para **series estacionarias**, es decir, sin tendencia ni estacionalidad persistente.
###### 3.1. Identificación de un modelo ARMA
> El primer paso es comprobar si la serie es estacionaria. Si no lo es, habría que transformarla o diferenciarla (esto ya entra en ARIMA, que veremos más adelante).
> Interpretación:
> - Si la ACF se corta rápidamente y la PACF decae lentamente → modelo AR(p).
> - Si la PACF se corta y la ACF decae lentamente → modelo MA(q).
> - Si ambas decaen → modelo ARMA(p,q).
```r
library(fpp2)
library(tidyverse)

# Cargar datos de ejemplo (Lab 2)
fdata <- readxl::read_excel("ARMA_series.xls")
fdata_ts <- ts(fdata)

# Seleccionar columna de interés
y <- fdata_ts[, 2]

# Visualizar y comprobar estacionariedad
autoplot(y) + ggtitle("Serie temporal candidata a ARMA")

# ACF y PACF para identificar órdenes p y q
ggtsdisplay(y, lag.max = 20)
```
###### 3.2. Estimación del modelo
> Una vez identificados los órdenes, se ajusta un modelo con `Arima()`.
```r
library(lmtest)  # para pruebas de significancia

# Ajustar un ARMA(1,1) con d = 0 (sin diferenciación)
arma_fit <- Arima(y, order = c(1, 0, 1), include.mean = TRUE) 

# Resumen de parámetros y errores
summary(arma_fit)

# Prueba de significancia de coeficientes
coeftest(arma_fit)
```
###### 3.3. Diagnóstico del modelo
> Un buen modelo debe dejar residuos que se parezcan a **ruido blanco** (no correlacionados y con media cero). Si los residuos muestran autocorrelación → el modelo no captura toda la dinámica y hay que probar con otro orden.
```r
# Comprobar residuos
checkresiduals(arma_fit)

# ACF y PACF de residuos
ggtsdisplay(residuals(arma_fit), lag.max = 20)
```
###### 3.4. Pronóstico con ARMA
> Una vez validado, el modelo puede usarse para generar predicciones a corto plazo. Los intervalos de confianza muestran la **incertidumbre creciente** en el futuro.
```r
# Forecast a 5 pasos adelante
y_forecast <- forecast::forecast(arma_fit, h = 5)

# Visualización
autoplot(y_forecast) +
  ggtitle("Pronóstico ARMA(1,1)") +
  xlab("Tiempo") + ylab("Valores")
```