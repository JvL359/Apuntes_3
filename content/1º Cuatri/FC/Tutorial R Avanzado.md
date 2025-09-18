
### II. Avanzado

1. Introducción a Series Temporales en R
> Una **serie temporal** es un conjunto de observaciones recogidas en intervalos regulares de tiempo (diarios, mensuales, trimestrales, anuales, etc.). El análisis de series temporales busca identificar patrones como **tendencia**, **estacionalidad** y **ciclos**, además de la parte aleatoria. En R, trabajaremos principalmente con los objetos `ts` (base R) y `xts`/`zoo` (paquetes especializados), que permiten estructurar los datos de forma temporal y aplicar métodos de análisis y pronóstico.  
> Esta sección introduce cómo **crear**, **visualizar** y **descomponer** series temporales, lo cual es el primer paso antes de aplicar modelos como ARMA o ARIMA.
###### 1.1. Creación de Series Temporales
> El objeto **`ts`** es el más utilizado en forecasting. Necesita:
> 	- **datos numéricos**
> 	- **inicio** (`start`) → año y período inicial
> 	- **frecuencia** (`frequency`) → nº de observaciones por unidad de tiempo
> 		- `12` = mensual
> 		- `4` = trimestral
> 		- `1` = anual
```r
library(quantmod)
library(xts)

# Serie temporal regular con ts()
ventas <- c(120, 135, 128, 142, 138, 155, 162, 148, 158, 165, 172, 180)
ts_ventas <- ts(ventas, start = c(2023, 1), frequency = 12)  # Mensual

# Serie temporal irregular con xts()
fechas <- as.Date(c("2024-01-01", "2024-01-05", "2024-01-10"))
valores <- c(100, 105, 98)
ts_irregular <- xts(valores, order.by = fechas)

# Descargar datos de PIB de EE.UU. desde FRED
getSymbols("GDP", src = "FRED")
head(GDP)
```
###### 1.2. Componentes de una serie temporal
> Una serie temporal puede descomponerse en:
> 1. **Tendencia** → dirección a largo plazo (crecimiento o decrecimiento).
> 2. **Estacionalidad** → patrones que se repiten en periodos fijos (ejemplo: ventas navideñas).
> 3. **Ciclos** → fluctuaciones irregulares ligadas a la economía.
> 4. **Ruido** → variaciones aleatorias.
```r
library(ggplot2)
library(forecast)

# Visualizar la serie de ventas
autoplot(ts_ventas) +
  ggtitle("Serie Temporal de Ventas") +
  xlab("Tiempo") + ylab("Unidades")

# Descomposición clásica (aditiva)
descomp <- decompose(ts_ventas, type = "additive")
autoplot(descomp)
```
###### 1.3. Exploración Inicial de Series
> Antes de modelar, conviene **inspeccionar propiedades básicas** de la serie: inicio, fin, frecuencia, longitud y resumen estadístico. Estas funciones te permiten confirmar que la serie está correctamente definida antes de pasar a métodos de forecasting.
```r
# Información de la serie ts
start(ts_ventas)     # Fecha de inicio
end(ts_ventas)       # Fecha final
frequency(ts_ventas) # Frecuencia temporal
length(ts_ventas)    # Número de observaciones
summary(ts_ventas)   # Resumen estadístico

# Visualización interactiva
library(dygraphs)
dygraph(ts_ventas, main = "Ventas mensuales (2023)") 
```

2. Métodos de Descomposición
> La **descomposición** de una serie temporal consiste en separar sus componentes principales:
> - **Tendencia (τ)** → movimiento de largo plazo.
> - **Estacionalidad (σ)** → patrones repetitivos en intervalos regulares.
> - **Irregularidad (e)** → ruido aleatorio.
> Existen varios métodos de descomposición:
> 1. **Clásicos (aditivo y multiplicativo).**
> 2. **SEATS (basado en modelos ARIMA).**
> 3. **X11/X13 (métodos Census, comunes en datos económicos).**
###### 2.1. Descomposición Clásica
> La **descomposición clásica** usa medias móviles para estimar la tendencia y luego extraer los componentes. 
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