### I. Preparación del entorno

1. ¿Qué son R y RStudio?
> **R** es el lenguaje de programación estadístico que usaremos para el análisis y pronóstico de series temporales. **RStudio** es un entorno de desarrollo que facilita la organización de proyectos, el manejo de datos y la visualización de resultados. En este curso trabajaremos siempre dentro de un proyecto de RStudio.

```r
getwd()        # Muestra la carpeta actual
sessionInfo()  # Información sobre la versión de R y los paquetes
```

###### 1.1. Instalación y carga de paquetes

> Para trabajar con forecasting necesitamos instalar y cargar librerías como `tidyverse` (manipulación), `forecast` y `fpp2` (modelado), `seasonal` (descomposición) y `readxl` (lectura de Excel).

```r
install.packages(c("tidyverse", "forecast", "fpp2", "seasonal", "readxl"))
library(tidyverse)
library(fpp2)
library(forecast)
library(seasonal)
library(readxl)
```

###### 1.2. Ayuda y documentación

> Puedes acceder a la documentación de R con `?función` o con `help()`. Esto te permitirá consultar rápidamente la utilidad y ejemplos de cualquier comando.

```r
?autoplot
example(ts)
help(package = "forecast")
```

---

### II. Fundamentos básicos de R

2. Primeros pasos con R

> Antes de entrar en forecasting, repasamos operaciones básicas, vectores y estructuras de datos simples que luego aplicaremos en análisis de series.

```r
x <- 1:5
mean(x)
sd(x)
```

###### 2.1. Data frames y fechas

> Los **data frames** son tablas de datos y el paquete `lubridate` simplifica el trabajo con fechas, clave para series temporales.

```r
library(lubridate)
df <- tibble(
  fecha = as.Date("2020-01-01") + 0:5*30,
  valor = c(10, 12, 9, 14, 16, 15)
)
df |> mutate(mes = month(fecha, label = TRUE))
```

---

### III. Importación y series temporales

3. Lectura de datos y creación de series

> El primer paso es importar datos desde Excel o CSV y convertirlos en objetos `ts`, que guardan frecuencia (mensual, trimestral, etc.) y fecha de inicio.

```r
fdata <- read_excel("Unemployment.xlsx")
glimpse(fdata)

# Serie mensual desde 2010
y <- ts(fdata$TOTAL, start = c(2010,1), frequency = 12)
y
```

###### 3.1. Visualización inicial

> Graficar la serie permite detectar tendencias, estacionalidad o valores atípicos.

```r
autoplot(y) +
  ggtitle("Unemployment in Spain") +
  xlab("Year") + ylab("Number unemployed")
```

---

### IV. Métodos de descomposición

4. Descomponer una serie

> La descomposición separa la serie en **tendencia**, **estacionalidad** y **residuos**. Es una forma exploratoria de analizar patrones antes de modelar.

###### 4.1. Descomposición clásica

```r
y_dec_add <- decompose(y, type="additive")
autoplot(y_dec_add)

y_dec_mult <- decompose(y, type="multiplicative")
autoplot(y_dec_mult)
```

###### 4.2. Descomposición con SEATS

```r
y_dec_seas <- seas(y)
autoplot(y_dec_seas)

# Serie ajustada estacionalmente
autoplot(seasadj(y_dec_seas))
```

###### 4.3. Gráficos estacionales

```r
ggseasonplot(y)
ggsubseriesplot(y)
```

---

### V. Modelos ARMA y ARIMA

5. Identificación y ajuste de modelos

> Los modelos ARMA/ARIMA son fundamentales. Se identifican con ACF/PACF y se ajustan con `Arima()` o `auto.arima()`.

###### 5.1. Identificación

```r
ggtsdisplay(y, lag.max = 20)
```

###### 5.2. Ajuste manual ARMA

```r
fit_arma <- Arima(y, order=c(1,0,1))
summary(fit_arma)
```

###### 5.3. ARIMA automático

```r
fit_arima <- auto.arima(y)
summary(fit_arima)
autoplot(forecast(fit_arima, h=12))
```

###### 5.4. Diagnóstico de residuales

```r
checkresiduals(fit_arima)
```

---

### VI. Pronósticos y validación

6. Generar y evaluar pronósticos

> Una vez ajustado el modelo, se generan pronósticos y se comparan con los datos reales mediante métricas de error.

###### 6.1. Pronósticos a futuro

```r
fc <- forecast(fit_arima, h=12)
autoplot(fc)
```

###### 6.2. Evaluación del modelo

```r
accuracy(fc)
```

---

## Siguientes pasos

- Repite los ejemplos con tus propios datasets (Unemployment, ARMA_series).

- Practica descomposición aditiva vs. multiplicativa y compara con SEATS.

- Ajusta modelos ARMA/ARIMA cambiando el orden y revisa los residuales.

- Avanza a SARIMA y modelos de regresión dinámica según tu plan de clases.