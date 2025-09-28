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
> 	- **`read.table`**: forma general de leer cualquier archivo que tenga forma de tabla, pudiendo elegir su separador con *`sep`* y avisar de un posible encabezado con *`header`*.
> 	- **`read.csv`**: especializado para archivos `.csv`; también cuenta con el separador y el encabezado.
> 	- **`read_excel`**: especializado para archivos `.xls` y `.xlsx`; pudiendo elegir la hoja que cargar como datos con *`sheet`*.
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
fdata <- arrange(fdata, DATE)

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

### III. Objeto Serie Temporal
#### 1. Creación del Objeto ts
> Objeto de trabajo para el análisis de la serie temporal, el cual recibe los siguientes argumentos:
> 	- Columna de valores de los datos.
> 	- Fecha inicial en formato vector del año y el periodo inicial de la serie.
> 	- Frecuencia de la serie.
```r
# En este caso el periodo inicial de 1 significa mes 1 (enero) por la frecuencia de 12
y <- ts(fdata$TOTAL, start = c(2010, 1), frequency = 12)
```

#### 2. Graficar el Objeto ts
> Podemos ver cual es el comportamiento de la serie temporal.
###### 2.1. Visualización Inicial Completa
> Representa la serie temporal completa de inicio a fin.
```r
# Se puede añadir título y labels
autoplot(y) +
  ggtitle("Unemployment in Spain") +
  xlab("Year") + ylab("Number unemployed")
```
###### 2.2. Visualización Inicial Parcial
> Usando window se puede extraer un intervalo de la serie.
```r
# 1. Selección del Intervalo
y_a <- window(y, end = c(2019, 12))
y_b <- window(y, start = c(2020, 1))
y_c <- window(y, start = c(2015, 1), end = c(2017, 12))

# 2. Gráfica conjunta de los Intervalos
autoplot(y_a, color="orange") +
  autolayer(y_b, color = "blue") +
  autolayer(y_c, color = "red") +
  ggtitle("Unemployment in Spain") +
  xlab("Year") + ylab("Number unemployed")
```

### IV. Métodos de Descomposición
#### 1. Descomposición Aditiva Clásica
> Usando el `type` "additive" obtenemos esta descomposición.
> Esta descomposición supone que los componentes se suman de manera lineal:
> 	$Y_t = T_t + S_t + E_t$​
> donde $Y_t$​ es la serie observada, $T_t$​ la tendencia, $S_t$​ la estacionalidad y $E_t$ el ruido aleatorio.
> Esto se usa cuando la amplitud de las fluctuaciones estacionales es constante a lo largo del tiempo (los “picos” y “valles” tienen siempre más o menos la misma magnitud).
```r
# Descomposición
y_dec_add <- decompose(y, type="additive")

# 2. Gráfica de la descomposición
autoplot(y_dec_add) + xlab("Year") +
  ggtitle("Classical additive decomposition")
```
#### 2. Descomposición Multiplicativa Clásica
> Usando el `type` "multiplicative" obtenemos esta descomposición.
> Esta descomposición asume que los componentes se combinan mediante un producto:
> 	$Y_t = T_t \times S_t \times E_t$
> Este modelo se usa cuando la amplitud de la estacionalidad crece o disminuye proporcionalmente al nivel de la serie (por ejemplo, las ventas aumentan en diciembre, pero el salto es mayor si la tendencia ya es alta).
```r
# 1. Descomposición
y_dec_mult <- decompose(y, type="multiplicative")

# 2. Gráfica de la descomposición
autoplot(y_dec_mult) + xlab("Year") +
  ggtitle("Classical multiplicative decomposition")
```
#### 3. Descomposición SEATS
> Usando una librería específica (`seasonal`) y su método `seas` obtenemos esta descomposición.
> Parte de un modelo `ARIMA` ajustado a la serie. A partir de ese modelo, separa la serie en sus componentes: tendencia-ciclo, estacionalidad e irregularidad.  A diferencia de los enfoques clásicos aditivo o multiplicativo (que son más mecánicos), SEATS es un método model-based, es decir, la descomposición se deriva de un modelo estadístico bien definido.
###### 3.1. Librería Adicional
```r
# En un código completo esta linea iría al inicio con el resto de librerías
library(seasonal)
```
###### 3.2. Aplicar la descomposición
```r
# 1. Descomposición
y_dec_seas <- seas(y)

# 2. Gráfica de la descomposición
autoplot(y_dec_seas) + xlab("Year") +
  ggtitle("SEATS decomposition")
```

#### 4. Comparativa de Descomposiciones
> Comparar **componentes estacionales** permite verificar si el patrón de estacionalidad es estable a lo largo del tiempo o si ha cambiado (por ejemplo, si la estacionalidad de las ventas de verano ahora empieza antes o es más intensa que antes).
> **Ajustar los componentes estacionales** consiste en eliminar ese efecto estacional de la serie, de modo que se pueda analizar mejor la tendencia y el ciclo subyacente sin que los picos y valles regulares confundan el análisis.
```r
# 1. Comparación de componentes estacionales
autoplot(seasonal(y_dec_mult), series = "Multiplicative") +
  forecast::autolayer(seasonal(y_dec_seas), series = "SEATS")
  
# 2. Comparación del ajuste de componentes estacionales
autoplot(seasadj(y_dec_add), series = "Additive") +
  forecast::autolayer(seasadj(y_dec_mult), series = "Multiplicative") +
  forecast::autolayer(seasadj(y_dec_seas),series = "SEATS")
```

Los apuntes continúan en [[Week 2 - Stochastic Processes]]

