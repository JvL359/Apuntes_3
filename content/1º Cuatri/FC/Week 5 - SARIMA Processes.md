### I. Previos
#### 1. Carga de Librerías
> Además de las usadas en semanas anteriores, aquí se añade **`TSstudio`**, que la usaremos para dividir la serie en train/test respetando el orden temporal mediante *`ts_split()`*.
```r
# Librerías
library(MLTools)
library(fpp2)
library(readxl)
library(tidyverse)
library(TSstudio)
library(lmtest)
library(tseries)
```
#### 2. Directorio
> a
```r
# Setear el Directorio
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
```

### II. Datos
#### 1. Carga y Procesamiento de Datos
> Cargamos el dataset de matriculaciones de coches desde un archivo Excel y realizamos un procesado inicial. Esto incluye:
> 	- Convertir la columna de fechas a formato `Date` en R para poder trabajar con series temporales.
> 	- Ordenar los registros cronológicamente para asegurar consistencia.
> 	- Revisar si existen **huecos** en la secuencia temporal (comparamos con una secuencia completa de meses).
> 	- Comprobar si hay fechas duplicadas o valores faltantes (`NA`) en la columna de interés.  
> Estos pasos garantizan que la serie está limpia antes de convertirla en un objeto `ts`.
```r
# 1. Carga y Primera Visualización
fdata <- read_excel("CarRegistrations.xls")
head(fdata)

# 2. Formato Date y Ordenar
fdata$Fecha <- as.Date(fdata$Fecha, format = "%d/%m/%Y")
fdata <- arrange(fdata, DATE)
head(fdata)

# 3. Valores Ausentes
valMin <- min(fdata$Data)
valMax <- min(fdata$Data)
date_range <- seq.Date(valMin, valMax, by = "months")
setdiff(date_range, fdata$DATE)

# 4. Valores Duplicados
fdata[duplicated(fdata$Fecha), ]
  
# 5. Valores NA
sum(is.na(fdata$CarReg))
```
#### 2. Conversión a un Objeto Serie Temporal
> Una vez validada la serie, la transformamos en un objeto `ts`, que es el formato estándar en R para series temporales. Definimos la frecuencia como `12` porque los datos son mensuales e indicamos la fecha de inicio en vector `c(1960, 1)`, lo que corresponde a enero de 1960. Por último lo graficamos para observar el comportamiento general de la serie.
```r
# 1. Objeto Serie Temporal
freq <- 12
start_date  <-  c(1960, 1)
y <- ts(fdata$CarReg, start = start_date, frequency = freq)

# 2. Plot
autoplot(y) +
  ggtitle("Car registrations") +
  xlab("Year") + ylab("Number registered (thousands)")
```

### III. Train-Test Split
#### 1. Método
> En el pronóstico de series temporales no podemos dividir los datos al azar como en problemas de machine learning clásicos, porque romperíamos la dependencia temporal.  
> En su lugar, separamos los últimos 5 años de observaciones como conjunto de validación/test, y el resto lo usamos para entrenamiento.  
> Existen varias formas de hacerlo:
> 	- Con la función *`ts_split()`* del paquete `TSstudio`, que automatiza la separación.
> 	- Con *`subset()`*, indicando directamente los índices de inicio y fin de cada subconjunto.
> 	- Con *`head()`* y *`tail()`*, extrayendo manualmente las observaciones de train y test.  
> Una vez realizada la división, es buena práctica visualizar ambas series en un mismo gráfico para verificar que el corte temporal es correcto.
```r
# 1.1. Opción 1
n_test <- floor(5 * freq)
y_split <- ts_split(y, sample.out = n_test)
y_TR <- y_split$train
y_TV <- y_split$test

# 1.2. Opción 2
y_TR <- subset(y, end = length(y) - 5 * 12) 
y_TV <- subset(y, start = length(y) - 5 * 12 + 1)

# 1.3. Opción 3
y_TR <- head(y, length(y) - 5 * 12) 
y_TV <- tail(y, 5 * 12) 

# 2. Vistazo de la División
tail(y_TR)
head(y_TV)

# Plot de la División
autoplot(y_TR, color = "orange") + 
  autolayer(y_TV, color = "blue")
```
#### 2. Qué Hacer si no Sabemos la Proporción de la División
> En algunos datasets no se indica claramente la **frecuencia de muestreo**. En ese caso:
> 	1. Primero graficamos la serie completa, aunque puede salir borrosa si es muy larga.
>     2. Después analizamos la ACF (Función de Autocorrelación) para detectar picos significativos en rezagos regulares. Estos picos marcan el periodo estacional de la serie (por ejemplo, un pico en los lag 24 y 48 sugiere periodicidad de 24 observaciones).
>     3. Una vez identificada la frecuencia, podemos marcarla en el gráfico y usarla como parámetro `freq`.
>     4. Por último, aplicamos una diferenciación estacional con esa frecuencia para eliminar el patrón repetitivo y dejar la serie más cercana a la estacionariedad.
```r
# 1. Carga de Archivo Auxiliar
fdata2 <- ts(read.table("fdata2.dat", sep = ""))

# 2. Plot Triple de la Serie, su ACF y su PACF
ggtsdisplay(fdata2, lag.max = 80)

# 3. Marcado de los Valores Significativos
freq <- 24
ggAcf(fdata2, lag.max = 80)+
  geom_vline(xintercept = (1:4) * freq, color = "green", alpha = 0.25, size=2)
  
# 4. Plot Triple de la Serie Diferenciada, su ACF y su PACF
ggtsdisplay(diff(fdata2, lag = freq), lag.max = 5 * freq)
```

### IV. Identificación SARIMA y Ajuste del Modelo
#### 1. Transformación Box-Cox
> Antes de identificar el orden SARIMA conviene estabilizar la varianza si aumenta con el nivel de la serie. La transformación de Box–Cox (controlada por el parámetro $\lambda$) ayuda a que la serie se parezca más a estacionaria y a que ACF/PACF sean más interpretables.
> 	1. Estimamos $\lambda$ con el gráfico media–desviación (ventana de 12 por ser datos mensuales).
> 	2. Aplicamos la transformación con ese $\lambda$ (si $\lambda \approx 1$, la transformación no cambia la serie; si $\lambda = 0$, equivale a log⁡).
> 	3. Comparamos visualmente la serie transformada con la original para verificar que la heterocedasticidad se reduce.
```r
# 1. Estimar λ con el Gráfico Media–Desviación (ventana mensual)
Lambda <- BoxCox.lambda.plot(y_TR, window.width = 12)

# 2. Aplicar la Transformación Box-Cox Usando λ Óptimo
z <- BoxCox(y_TR, Lambda)

# 3. Comparar serie transformada (z) vs. original (y o y_TR)
p1 <- autoplot(z)
p2 <- autoplot(y)
gridExtra::grid.arrange(p1, p2, nrow = 2 )
```
#### 2. Diferenciación
> 'Rellenar aquí'
###### 1.1. 'Rellenar aquí'
> 'Rellenar aquí' (incluyendo esto: recall if the ACF decreases very slowly -> needs differentiation)
```r
# 1. 'Rellenar aquí'
ggtsdisplay(z,lag.max = 100)
```
###### 1.2. Diferenciación Estacional
> 'Rellenar aquí'
```r
# 1. 'Rellenar aquí'
B12z<- diff(z, lag = freq, differences = 1)

# 2. 'Rellenar aquí'
ggtsdisplay(B12z,lag.max = 4 * freq)
```
###### 1.3. Diferenciación Regular (Sin Estacional)
> 'Rellenar aquí'
```r
# 1. 'Rellenar aquí'
Bz <- diff(z,differences = 1)

# 2. 'Rellenar aquí'
ggtsdisplay(Bz, lag.max = 4 * freq)
```
###### 1.2. Diferenciación Doble (Estacional y Regular)
> 'Rellenar aquí'
```r
# 1. 'Rellenar aquí'
B12Bz <- diff(Bz, lag = freq, differences = 1)

# 2. 'Rellenar aquí'
ggtsdisplay(B12Bz, lag.max = 4 * freq)

# 3. Orden No Importa
B_B12z<- diff(B12z, differences = 1)
autoplot(B12Bz, color = "blue", size = 2) + autolayer(B_B12z, color = "orange", size = 0.5)
```