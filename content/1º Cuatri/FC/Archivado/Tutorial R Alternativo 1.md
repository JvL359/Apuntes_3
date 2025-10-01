# 1) Preparación del entorno (R, RStudio y paquetes)

**Descripción general** → En esta sección instalaremos y configuraremos todo para trabajar con R en pronósticos. Verás qué son R y RStudio, cómo instalar paquetes y dónde encontrar ayuda. Al final tendrás tu entorno listo para cargar datos, analizarlos y crear tus primeros modelos de forecasting.

### 1.1 ¿Qué son R y RStudio?

**Explicación**: R es el lenguaje de programación; RStudio es un entorno (IDE) que facilita escribir código, ver gráficos y gestionar proyectos. Usaremos RStudio para organizar scripts, datos y resultados en una carpeta de proyecto.  
**Código en R (ejemplo práctico)**:

```r
getwd()   # Muestra la carpeta actual del proyecto
sessionInfo() # Versión de R y paquetes cargados
```

### 1.2 Instalar y cargar paquetes

**Explicación**: Los paquetes amplían R con funciones listas para usar. Para manipulación y gráficos usaremos `tidyverse`; para pronósticos, `forecast` y `fpp2`. También usaremos `seasonal` para descomposición avanzada.  
**Código en R (ejemplo práctico)**:

```r
install.packages(c("tidyverse", "forecast", "fpp2", "seasonal", "readxl"))
library(tidyverse)
library(fpp2)
library(forecast)
library(seasonal)
library(readxl)
```

### 1.3 Encontrar ayuda rápidamente

**Explicación**: La documentación integrada de R te evita perder tiempo. El prefijo `?` abre la ayuda de una función y `example()` muestra cómo se usa. Úsalo siempre que tengas dudas.  
**Código en R (ejemplo práctico)**:

```r
?autoplot
example(ts)
help(package = "forecast")
```

---

# 2) Fundamentos básicos de R

**Descripción general** → Antes de meternos con forecasting, necesitas conocer lo esencial de R: cómo asignar valores, trabajar con vectores, data frames y fechas. Esto te dará soltura para entender el código de tus prácticas.

### 2.1 Asignaciones y operaciones básicas

```r
x <- 1:5
mean(x)
sd(x)
```

### 2.2 Data frames y fechas

```r
library(lubridate)
df <- tibble(
  fecha = as.Date("2020-01-01") + 0:5*30,
  valor = c(10, 12, 9, 14, 16, 15)
)
df |> mutate(mes = month(fecha, label = TRUE))
```

---

# 3) Importación de datos y creación de series temporales

**Descripción general** → El punto de partida en forecasting es importar datos y transformarlos en objetos de serie temporal (`ts`). Aprenderás a leer CSV/Excel, manejar fechas y definir frecuencia (mensual, trimestral, etc.).

### 3.1 Leer datos desde Excel o CSV

```r
fdata <- read_excel("Unemployment.xlsx")
glimpse(fdata)
```

### 3.2 Conversión a objeto `ts`

```r
# Supongamos que la columna TOTAL son desempleados mensuales desde 2010-01
y <- ts(fdata$TOTAL, start = c(2010,1), frequency = 12)
y
```

### 3.3 Graficar la serie

```r
autoplot(y) +
  ggtitle("Unemployment in Spain") +
  xlab("Year") + ylab("Number unemployed")
```

---

# 4) Métodos de descomposición

**Descripción general** → La descomposición separa una serie en tendencia, estacionalidad y residuos. Es un paso exploratorio clave antes de aplicar modelos como ARIMA.

### 4.1 Descomposición clásica (aditiva y multiplicativa)

```r
y_dec_add <- decompose(y, type="additive")
autoplot(y_dec_add)

y_dec_mult <- decompose(y, type="multiplicative")
autoplot(y_dec_mult)
```

### 4.2 Descomposición con SEATS (`seasonal`)

```r
library(seasonal)
y_dec_seas <- seas(y)
autoplot(y_dec_seas)

# Serie ajustada estacionalmente
autoplot(seasadj(y_dec_seas))
```

### 4.3 Gráficos estacionales

```r
ggseasonplot(y) + ggtitle("Seasonal plot")
ggsubseriesplot(y)
```

---

# 5) Modelos ARMA y ARIMA

**Descripción general** → Los modelos ARMA/ARIMA son fundamentales en forecasting. Se identifican con los gráficos ACF/PACF y luego se ajustan con `Arima()` o `auto.arima()`.

### 5.1 Identificación con ACF y PACF

```r
ggtsdisplay(y, lag.max = 20)
```

### 5.2 Ajuste de un modelo ARMA

```r
fit_arma <- Arima(y, order=c(1,0,1))
summary(fit_arma)
```

### 5.3 ARIMA automático

```r
fit_arima <- auto.arima(y)
summary(fit_arima)
autoplot(forecast(fit_arima, h=12))
```

### 5.4 Diagnóstico de residuales

```r
checkresiduals(fit_arima)
```

---

# 6) Pronósticos y validación

**Descripción general** → Finalmente, generamos pronósticos y los comparamos con los datos reales para evaluar la precisión del modelo.

### 6.1 Pronósticos a futuro

```r
fc <- forecast(fit_arima, h=12)
autoplot(fc)
```

### 6.2 Evaluación del modelo

```r
accuracy(fc)
```

---

## Siguientes pasos

- Repite los ejemplos con tus propios datasets (Unemployment, ARMA_series).
    
- Practica descomposición aditiva vs. multiplicativa y compara con SEATS.
    
- Ajusta modelos ARMA/ARIMA cambiando el orden y revisa los residuales.
    
- Avanza a SARIMA y modelos de regresión dinámica según tu plan de clases.