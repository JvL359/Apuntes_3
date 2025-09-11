
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
###### 2.2. Variables
> Asignación de variables
```r
x <- 10       # Recomendado
y = 20        # También válido
30 -> z       # Menos común

# Buenas prácticas
mi_variable <- 5   # snake_case recomendado

```
###### 2.3. Funciones
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
###### 3.1. Importación de datos
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
###### 3.2. Limpieza de Datos
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
###### 3.3. Transformación de Datos
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

El tutorial continua en [[Tutorial R Avanzado]]