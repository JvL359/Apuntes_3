### I. Previos
#### 1. Carga de Librerías
> Paso idéntico al de la clase anterior.
```r
# Librerías
library(MLTools)
library(fpp2)
library(tidyverse)
library(readxl)
library(lmtest) 
```
#### 2. Directorio
> Paso idéntico al de la clase anterior.
```r
# Setear el Directorio
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
```

### II. AR Processes
#### 1. Definición en el Caso No Estacional
> Un proceso estocástico $Y_t$ se considera AutoRegresivo si satisface la siguiente ecuación:
> 	$Y_t = \phi_1 Y_{t-1} + \phi_2 Y_{t-2} + \dots + \phi_p Y_{t-p} + \varepsilon_t$ 
> 	- $\varepsilon_t$ es Ruido Blanco Gaussiano.
> 	- $\phi_1, \dots, \phi_p$ son constantes llamadas coeficientes del proceso.
> 	- $p$ es el orden del proceso, que este es llamado $AR(p)$.
> Una serie temporal que proviene de un proceso AR se denomina *serie temporal autorregresiva*.
> Este tipo de proceso puede entenderse como análogo a un *modelo de regresión lineal múltiple*, con la diferencia de que las variables explicativas no son externas, sino que son los lags recientes de la propia serie. En otras palabras, la predicción de $Y_t$​ se hace usando como predictores los valores anteriores de la misma serie. Así, la serie se “regresa sobre sí misma”.
#### 2. BackShift Operator
> Usando un Operador de Retroceso  $B(Y_t) = Y_{t-1}$  podemos reescribir el proceso como:
> 	$\Phi(B)Y_t = (1- \phi_1B - \dots - phi_pB^p)Y_t = \varepsilon_t$
> 	donde $\Phi(B) = (1- \phi_1B - \dots - phi_pB^p)$ es el polinomio característico del proceso.