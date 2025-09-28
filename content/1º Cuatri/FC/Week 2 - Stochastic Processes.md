### I. Previos
#### 1. Carga de librerías 
> En este caso añadiremos la librería ML-Tools a través de un .zip seleccionando esa opción en `Install Packages`.
> Aparte, importaremos la librería `lmtest`, se utiliza para aplicar pruebas estadísticas que permiten evaluar la validez de modelos de regresión y de series temporales. Con ella se pueden detectar problemas como autocorrelación, heterocedasticidad o mala especificación del modelo, ayudando a verificar si los supuestos del análisis se cumplen.
```r
# Librerías
library(MLTools)
library(fpp2)
library(tidyverse)
library(readxl)
library(lmtest) #contains coeftest function
```