
### I. R Básico

1. Introducción a R
> **R** es un lenguaje de programación estadístico, gratuito y de código abierto, especializado en el análisis de datos y en el trabajo con series temporales. Se utiliza ampliamente en ciencia de datos, economía y finanzas gracias a la gran cantidad de paquetes disponibles para manipulación, visualización y pronósticos, como `forecast`, `tseries` o `fpp2`. Estos permiten desde el análisis exploratorio hasta la construcción de modelos avanzados, como ARIMA o el Suavizamiento Exponencial. Además, **R** facilita la creación de gráficos de alta calidad y el manejo de datos temporales, y suele emplearse junto a **RStudio**, un entorno que organiza y simplifica la escritura y ejecución de código.
###### 1.1. Instalación de paquetes
> Librerías necesarias para el tratamiento y análisis de series temporales.
```r
install.packages(c(
  "tidyverse",   # Manipulación de datos
  "forecast",    # Modelos de pronóstico
  "tseries",     # Tests de series temporales
  "xts", "zoo",  # Objetos de series temporales
  "lubridate",   # Manejo de fechas
  "ggplot2",     # Visualizaciones
  "fpp2"         # Datasets y ejemplos del libro de Hyndman
))
```
2. Primeros Pasos: Conceptos Básicos
> R funciona como una **calculadora avanzada** y un **lenguaje de programación**. Vamos a ver ejemplos de operaciones, asignación de variables y funciones básicas.
###### 2.1. Operadores
> Operaciones aritméticas
```r
5 + 3   # Suma → 8
10 - 4  # Resta → 6
6 * 7   # Multiplicación → 42
15 / 3  # División → 5
2^3     # Potencia → 8
17 %% 5 # Resto → 2
```
###### 2.2 Variables
> Asignación de variables
```r
x <- 10       # Recomendado
y = 20        # También válido
30 -> z       # Menos común

# Buenas prácticas
mi_variable <- 5   # snake_case recomendado

```
###### 2.3 Funciones
> Funciones matemáticas
```r
sqrt(16)        # Raíz cuadrada → 4
abs(-5)         # Valor absoluto → 5
round(3.14159,2) # Redondeo → 3.14

# Información sobre objetos
length(c(1,2,3,4)) # Longitud → 4
class(5)           # Tipo → "numeric"
```

3. Manipulación de Datos en R
> La manipulación de datos es esencial para garantizar que la información con la que trabajamos sea confiable y esté en el formato correcto. En R, los datos suelen venir en **archivos CSV, Excel o APIs** y necesitamos limpiarlos, transformarlos y adaptarlos para análisis temporal. Usaremos principalmente el paquete **tidyverse**, que ofrece herramientas como `readr`, `dplyr` y `tidyr` para estas tareas.
###### 3. Importación de datos
> En forecasting, los datos pueden provenir de archivos locales o de fuentes externas como **Yahoo Finance** o **FRED** (Federal Reserve Economic Data).
```r
## Archivos CSV y Excel
# Importar CSV con base R
datos <- read.csv("archivo.csv", header = TRUE, sep = ",")

# Importar CSV con tidyverse (recomendado)
library(readr)
datos <- read_csv("archivo.csv")

# Importar Excel
install.packages("readxl")
library(readxl)
datos_excel <- read_excel("archivo.xlsx", sheet = "Hoja1")


## Datos financieros y económicos
# Yahoo Finance con quantmod
library(quantmod)
getSymbols("AAPL", from = "2020-01-01", to = "2024-01-01")
head(AAPL)

# Datos económicos de FRED
getSymbols("GDP", src = "FRED")
head(GDP)


## Una vez cargados, es recomendable explorar los datos
head(datos)     # Primeras filas
str(datos)      # Estructura
summary(datos)  # Estadísticas descriptivas

```
###### 3. Limpieza de Datos
> Los datos reales suelen tener valores faltantes, duplicados o inconsistencias. En forecasting es mejor **imputar valores faltantes** en lugar de eliminarlos, para no romper la continuidad de la serie.
```r
library(dplyr)

# Eliminar duplicados
datos <- distinct(datos)

# Identificar valores faltantes
colSums(is.na(datos))

# Eliminar filas con NA
datos <- na.omit(datos)

# Reemplazar NA por 0 o por la media
datos$precio[is.na(datos$precio)] <- 0
datos$volumen <- ifelse(is.na(datos$volumen),
                        mean(datos$volumen, na.rm = TRUE),
                        datos$volumen)
```
###### 3. Transformación de Datos
> Transformar los datos significa reestructurarlos, crear nuevas variables o preparar la **columna de fechas** para convertir el dataset en una **serie temporal**. 
> Este tipo de transformaciones son clave para:
> - **Resamplear** (cambiar frecuencia diaria → mensual, mensual → trimestral).
> - **Agregar** (promedios, sumas por período).
> - **Preparar la variable temporal** antes de crear objetos `ts` o `xts`.
```r
library(dplyr)
library(lubridate)

# Crear una variable de año y mes
datos <- datos %>%
  mutate(
    fecha = ymd(fecha),          # convertir texto a fecha
    anio = year(fecha),
    mes = month(fecha, label=TRUE)
  )

# Filtrar por rango de fechas
datos_filtrados <- datos %>%
  filter(fecha >= "2023-01-01" & fecha <= "2023-12-31")

# Resumir datos por mes
datos_mensuales <- datos %>%
  group_by(anio, mes) %>%
  summarise(promedio_precio = mean(precio, na.rm = TRUE))

```

4. Introducción a Series Temporales
> Una **serie temporal** es una secuencia de observaciones tomadas en intervalos regulares de tiempo (diarios, mensuales, trimestrales, etc.). El forecasting se centra en analizar patrones como **tendencia, estacionalidad, ciclos y ruido** para predecir valores futuros.  
> En R, las series temporales se pueden manejar principalmente con dos tipos de objetos:
> - `ts` → series regulares (misma frecuencia).
> - `xts` → series irregulares (ejemplo: datos financieros con fechas específicas).
###### 4.1. Creación de Series Temporales
> Podemos crear series temporales a partir de vectores numéricos o datos financieros descargados con `quantmod`.
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
###### 4.2. Componentes de una serie temporal
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
###### 4.3. Exploración Inicial de Series
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

5. Métodos de Descomposición
> La **descomposición** de una serie temporal consiste en separar sus componentes principales:
> - **Tendencia (τ)** → movimiento de largo plazo.
> - **Estacionalidad (σ)** → patrones repetitivos en intervalos regulares.
> - **Irregularidad (e)** → ruido aleatorio.
> Existen varios métodos de descomposición:
> 1. **Clásicos (aditivo y multiplicativo).**
> 2. **SEATS (basado en modelos ARIMA).**
> 3. **X11/X13 (métodos Census, comunes en datos económicos).**
###### 5.1. Descomposición Clásica
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
###### 5.2. Descomposición SEATS
> **SEATS (Seasonal Extraction in ARIMA Time Series)** es un método avanzado basado en modelos ARIMA, implementado en R con el paquete `seasonal`. La ventaja es que estima los componentes con más flexibilidad y suele ajustarse mejor que la descomposición clásica.
```r
library(seasonal)

# Descomposición SEATS
y_dec_seas <- seas(y)
autoplot(y_dec_seas) +
  ggtitle("SEATS Decomposition")
```
###### 5.3. X11/X13-ARIMA
> Los métodos **X11/X13** (del U.S. Census Bureau) son muy usados en macroeconomía y estadísticas oficiales. También son iterativos y refinan la extracción de tendencia y estacionalidad. 
> En R, también se implementan con `seasonal` (opción `"x11"` o `"x13"`).
> En práctica profesional, SEATS y X11 suelen preferirse sobre la descomposición clásica porque manejan mejor **outliers, efectos de calendario y series económicas reales**.
```r
# Descomposición con X11
y_dec_x11 <- seas(y, x11 = "")
autoplot(y_dec_x11) +
  ggtitle("X11 Decomposition")
```
###### 5.4. Ajuste Estacional y Comparación
> Una vez descompuesta la serie, podemos extraer componentes y comparar distintos métodos. Esto permite ver cómo cada método elimina la estacionalidad y deja una serie más estable para modelar.
```r
# Serie ajustada estacionalmente (remove seasonality)
autoplot(seasadj(y_dec_add), series = "Aditiva") +
  autolayer(seasadj(y_dec_mult), series = "Multiplicativa") +
  autolayer(seasadj(y_dec_seas), series = "SEATS") +
  ggtitle("Comparación de Ajustes Estacionales")
```

6. Modelos ARMA
> Los **modelos ARMA (Autoregressive Moving Average)** combinan dos componentes:
> - **AR (Autoregresivo):** el valor actual depende de valores pasados de la propia serie.
> - **MA (Media móvil):** el valor actual depende de errores pasados (ruido).
> Un modelo **ARMA(p,q)** tiene la forma: $y_t = c + \phi_1 y_{t-1} + \cdots + \phi_p y_{t-p} + \theta_1 e_{t-1} + \cdots + \theta_q e_{t-q} + e_t$
> Se utilizan principalmente para **series estacionarias**, es decir, sin tendencia ni estacionalidad persistente.
###### 6.1. Identificación de un modelo ARMA
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
###### 6.2. Estimación del modelo
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
###### 6.3. Diagnóstico del modelo
> Un buen modelo debe dejar residuos que se parezcan a **ruido blanco** (no correlacionados y con media cero). Si los residuos muestran autocorrelación → el modelo no captura toda la dinámica y hay que probar con otro orden.
```r
# Comprobar residuos
checkresiduals(arma_fit)

# ACF y PACF de residuos
ggtsdisplay(residuals(arma_fit), lag.max = 20)
```
###### 6.4. Pronóstico con ARMA
> Una vez validado, el modelo puede usarse para generar predicciones a corto plazo. Los intervalos de confianza muestran la **incertidumbre creciente** en el futuro.
```r
# Forecast a 5 pasos adelante
y_forecast <- forecast::forecast(arma_fit, h = 5)

# Visualización
autoplot(y_forecast) +
  ggtitle("Pronóstico ARMA(1,1)") +
  xlab("Tiempo") + ylab("Valores")
```