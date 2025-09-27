### I. Previos
#### 1. Carga de librerías
> - **library(fpp2)**: reúne funciones y datasets para análisis y pronóstico de series temporales, cargando automáticamente paquetes como `forecast` y `ggplot2`.
> - **library(tidyverse)**: colección de paquetes diseñados para importar, transformar, visualizar y modelar datos de forma coherente y eficiente.
> - **library(readxl)**: permite leer directamente archivos de Excel (`.xls` y `.xlsx`) en R de manera sencilla.
```r
# Cargar Librerías
library(fpp2) 
library(tidyverse)
library(readxl)
```
#### 2. Directorio
> Ajusta automáticamente tu directorio de trabajo al mismo directorio donde está guardado tu script activo en RStudio.
```r
# Setear el Directorio
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
```

### II. Datos
#### 1. Lectura y Carga de Datos
> Cargar un dataset de diferentes tipos de archivos
> 	- **`read.table`**: forma general de leer cualquier archivo que tenga forma de tabla, pudiendo elegir su separador con `sep` y avisar de un posible encabezado con `header`.
> 	- **`read.csv`**: especializado para archivos *.csv*; también cuenta con el separador y el encabezado.
> 	- **`read_excel`**: especializado para archivos *.xls* y *.xlsx*; pudiendo elegir la hoja que cargar como datos con `sheet`.
```r
# 1. Forma General
fdata <- read.table("Unemployment.dat", sep = ",", header = TRUE)

# 2. CSV
fdata <- read.csv("archivo.csv", header = TRUE, sep = ",")

# 3. Excel
fdata <- read_excel("Unemployment.xlsx", sheet = 2)
```
#### 2. Visualización Inicial
> Conocer mejor los datos con los que vamos a tratar
> 	- **`head y tail`**: igual que Pandas.
> 	- **`glimpse`**: muestra el nº de filas, los nombres de las variables, su tipo, y sus primeros valores.
> 	- **`str`**: misma información que `glimpse` pero en un formato menos mejor y más peor.
```r
# 1. head y tail
head(fdata, 10)
tail(fdata, 10)

# 2. Base R
str(fdata)

# 3. Librería dplyr de tidyverse
glimpse(fdata)
```
#### 3. EDA para Series Temporales
> Permite entender cada cuánto se registran los datos (diario, mensual, trimestral…), lo cual es clave para elegir los métodos de modelado y pronóstico adecuados.
> También ayuda a detectar huecos o irregularidades en el registro que podrían distorsionar el análisis, y orienta sobre si es necesario imputar, interpolar o limpiar los datos antes de seguir.
###### 3.1. Frecuencia
> - **`Convertir a Formato Date`**: ahora la columna `DATE` de texto (`dd/mm/yyyy`) pasa a ser un objeto de fecha en R.
> - **`Ordenar por Fecha`**: poder identificar la frecuencia de los datos de la serie.
> - **`Identificar la Frecuencia`**: usar glimpse para determinar si la serie es anual (1), trimestral (4), mensual (12), semanal (52), o diario (365).
```r
# 1. Convertir a Date
fdata$DATE <- as.Date(fdata$DATE, format = "%d/%m/%Y")

# 2. Ordenar fechas
fdata <- arrange(fdata,DATE)

# 3. Identifiación
glimpse(fdata)
```
###### 3.2. Valores Ausentes
> - **`Mínimo y Máximo Valor`**: Para establecer una secuencia de fechas y compararla con la serie. Esta secuencia hay que ordenarla por la frecuencia de la serie obtenida en 
> - **`Comparación`**: Si la longitud es 0 significa que no hay ningún gap.
```r
# 1. Secuencia de Fechas entre la mínima y la máxima de la serie temporal
valMin <- min(fdata$Data)
valMax <- min(fdata$Data)
date_range <- seq.Date(valMin, valMax, by = "months")

# 2. Comparación de la secuencia con la propia serie temporal
setdiff(date_range, fdata$DATE)
```

### III. Serie Temporal
#### 1. 

