### I. Previos
#### 1. Carga de librerías 
> En este caso añadiremos la librería ML-Tools a través de un .zip seleccionando esa opción en `Install Packages`.
> Aparte, importaremos la librería *`lmtest`*, esta se usa para aplicar pruebas estadísticas que ayudan a evaluar y diagnosticar modelos de regresión y series temporales. En concreto, la función *`coeftest()`* nos servirá para contrastar la significancia estadística de los coeficientes de un modelo, mostrando sus estimaciones junto con errores estándar, valores t y p-valores.
```r
# Librerías
library(MLTools)
library(fpp2)
library(tidyverse)
library(readxl)
library(lmtest) 
```
#### 2. Directorio
> Igual que en [[Week 1 - Decomposition Methods]]
```r
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
```

### II. Ruido Blanco
#### 1. Definición
> Un **Proceso de Ruido Blanco** es una secuencia de variables aleatorias:
> 	- No correlacionadas entre sí (no hay memoria, cada valor es independiente de los anteriores).
> 	- Con media cero.
> 	- Con varianza constante (homocedasticidad).
> 	- Si además cada valor sigue una distribución normal, hablamos de ruido blanco gaussiano.
> Formalmente:
> 	$\{ \varepsilon_t \} \sim WN(0, \sigma^2) \quad \text{con} \quad E[\varepsilon_t] = 0, \quad Var(\varepsilon_t) = \sigma^2, \quad Cov(\varepsilon_t, \varepsilon_{t'} ) = 0 \ \forall t \neq t'$

#### 2. Uso
> El ruido blanco representa la parte impredecible de una serie temporal. Todo buen modelo debe reducir la serie observada hasta un residuo que sea indistinguible de ruido blanco.
###### 2.1. Ruido Puro o Base de Comparación
> El ruido blanco es la referencia de una serie sin estructura.
> Si un modelo ajustado deja residuos que se comportan como ruido blanco, eso significa que el modelo ha capturado toda la información sistemática de la serie (tendencia, estacionalidad, correlaciones).
###### 2.2. Componente de los Modelos ARMA/ARIMA
> En los modelos estocásticos, el ruido blanco es la parte impredecible.
> Por ejemplo:  $Y_t = \phi Y_{t-1} + \varepsilon_t,$  aquí, $\varepsilon_t$ es ruido blanco: el “shock” o innovación en el sistema.

2.3. Diagnóstico de Modelos
> Una vez ajustado un modelo ARIMA o de suavizado exponencial, se comprueba que los residuos sean ruido blanco.
> Si no lo son (si muestran autocorrelación), el modelo está mal especificado.
###### 2.4. Simulación y Pruebas
> Se usa ruido blanco para simular series y comprobar el comportamiento de métodos de pronóstico.
>  También como input en procesos ARMA para generar datos artificiales.

###### 2.5. Gaussiano vs No Gaussiano
> - **Gaussiano**: cada $\varepsilon_t$ sigue una Normal(0,σ²). Esto es útil porque facilita inferencia estadística y resultados asintóticos.
> - **No gaussiano**: mantiene independencia y varianza constante, pero con otra distribución (ej. uniforme, t-Student). Se sigue considerando ruido blanco, pero las propiedades de los estimadores cambian.
#### 3. Creación
> Para crear una serie temporal de ruido blanco gaussiano obtenemos una muestra de n valores aleatorios de una distribución normal estándar.
```r
# 1. N muestras normales estándar
n <- 150
z <- rnorm(n, mean = 0, sd = 1) 

# 2. Objeto ts
w <- ts(z)
```
#### 4. Visualización 
> Nos sirve para comprobar que no hay patrones ni correlaciones, confirmando que se trata solo de fluctuaciones aleatorias.
```r
# 1. Solo valores numéricos
head(w, 25)

# 2. Gráfica de la serie
autoplot(w) +
  ggtitle("White noise") + 
  geom_point(aes(x = 1:n, y = z), size=1.5, col="blue")
```
#### 5. ACF & PACF de Ruido Blanco
> Esta es otra manera de comprobar que una serie se comporta como ruido blanco, es decir, que no tiene patrones ni correlaciones aprovechables para el modelado. 
> - **`ACF`**: Auto Correlation Function, mide la correlación entre la serie y sus rezagos (valores pasados).
> En un proceso de ruido blanco, todas las autocorrelaciones (excepto en el lag 0) deberían ser ≈ 0. Las barras negras son las correlaciones observadas en tu muestra, y las líneas azules marcan el intervalo de confianza (aprox. $\pm \dfrac{2}{\sqrt{n}}$).  
> 	Si las barras caen dentro de esas bandas, no hay evidencia de correlación significativa, que es lo esperado en ruido blanco.
> - **`PACF`**: Partial Auto Correlation Function, mide la correlación entre la serie y sus rezagos, eliminando la influencia de los rezagos intermedios. Para ruido blanco, también debería dar ≈ 0 en todos los lags. Igual que en la ACF, vemos que ninguna barra sobresale de las bandas azules, lo que confirma que no hay estructura.
> 
> 	*`Nota`*: `lag` significa cuántos pasos atrás en el tiempo miramos para comparar la serie consigo misma. 
> 		- lag 1: comparo el valor en t con el valor en t−1.
> 		- lag 2: comparo el valor en t con el de t−2.
> 		- Y así sucesivamente.
> 	El `lag 0` es la serie comparada consigo misma, que por definición la correlación siempre es 1.
```r
ggtsdisplay(w, lag.max = 20)
```

### III. Random Walks
#### 1. Definición
> Un **Random Walk (RW)** es un proceso estocástico donde el valor actual es la suma del valor anterior más un término de ruido blanco:
> 	$Y_t = Y_{t-1} + \varepsilon_t, \quad \varepsilon_t \sim WN(0,\sigma^2)$
> Forma de un Random Walk con drift:  $Y_t = k + Y_{t-1} + w_t​​$  donde k es la constante de drift, la cual es responsable del crecimiento o decrecimiento promedio (k > 0 o k < 0).
> - Cada paso se construye a partir del anterior.
> - La innovación ($\varepsilon_t$​) es impredecible, por lo que introduce aleatoriedad.
> - No tiene media constante ni varianza constante, por lo que no es estacionario, cambia con el tiempo. En el caso de la varianza, es creciente /  $Var(Y_t) = t \cdot \sigma^2$
> Intuitivamente: imagina una persona que da pasos al azar en una línea recta. No sabemos hacia dónde va en el futuro, solo sabemos dónde está ahora y que su próximo paso será aleatorio.
#### 2. Uso
> Un random walk representa procesos donde el futuro depende solo del presente más un shock aleatorio. Su única memoria es su último paso, y es la base del modelo ingenuo de predicción.
###### 2.1. Modelo Base en Finanzas
> Se usa mucho para modelar precios de acciones o divisas. Los precios siguen un random walk, estos no se pueden predecir a partir de los datos pasados.
###### 2.2. Referencia para Pronósticos
> El random walk es equivalente al método ingenuo (naive forecast):
> 	$\hat{Y}_{t+1} = Y_t$
> Es decir, el mejor pronóstico para mañana es simplemente el valor de hoy.
#### 3. Creación

