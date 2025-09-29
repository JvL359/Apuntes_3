### I. Previos
#### 1. Carga de Librerías
> Aparte de las mismas de las sesiones anteriores, importaremos *`tseries`* que sirve para realizar contrastes de raíz unitaria. En concreto, la función *`adf.test`* nos servirá para implementar el test de Dickey-Fuller aumentado (ADF), que sirve para comprobar si una serie es estacionaria o si necesita diferenciación.
```r
# Librerías
library(MLTools)
library(fpp2)
library(readxl)
library(tidyverse)
library(lmtest)  
library(tseries) 
```
#### 2. Directorio
> Paso idéntico al de la clase anterior.
```r
# Setear el Directorio
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
```

### II. Metodología de Box-Jenkins
#### 1. Transformación Box-Cox
###### 1.1. Definición
> Esta transformación se aplica a menudo cuando tenemos una serie temporal con varianza no homogénea y tratamos de hacerla más homogénea, de modo que el comportamiento de la serie parezca más estacionario. Viene dada por:
> 	$w_t = \begin{cases} \log(y_t), & \text{si } \lambda = 0; \\[6pt] \frac{\text{sign}(y_t)|y_t|^{\lambda} - 1}{\lambda}, & \text{en otro caso}. \end{cases}$
> 	Nota: cuando $\lambda = 1$, formalmente obtenemos $w_t = |y_t| - 1$.  
> 	De hecho, nosotros (y muchas librerías) tomaremos $\lambda = 1$ con el significado de “no se requiere ningún cambio”, y en ese caso se define simplemente $w_t = y_t$​.
###### 1.2. Ejemplo: Serie Temporal Heterocedástica
> 1. La serie temporal `jj` de la librería astsa describe las ganancias trimestrales por acción de Johnson & Johnson (1960 a 1980). El gráfico de abajo muestra claramente que la varianza aumenta con el nivel de la serie temporal.
> 2. Usemos la función *`BoxCox.lambda.plot`* para explorar si la transformación de Box-Cox puede ser útil y qué valor de λ\lambdaλ conviene usar. El gráfico resultante es un diagrama log-log (desviación estándar frente a media móvil). La línea azul ajustada muestra la relación entre ambas magnitudes.
> 3. El gráfico y el alto valor de $R^2$ indican que la transformación de Box-Cox puede ser realmente útil. Así que la aplicamos.
> 4. Ahora comparamos los gráficos de la serie temporal original y la transformada
> 	Los gráficos muestran:
> 	- Arriba (y): la serie original (ganancias de Johnson & Johnson), donde se aprecia un incremento de la varianza a lo largo del tiempo.
> 	- Abajo (z): la serie transformada con Box-Cox, donde la varianza se ha vuelto más homogénea.
```r
# 1
library(astsa)
y <- jj
autoplot(y)

# 2
Lambda <- BoxCox.lambda.plot(y)

# 3
z <- BoxCox(y, lambda = Lambda)

# 4
p1 <- autoplot(y)
p2 <- autoplot(z)
gridExtra::grid.arrange(p1, p2)
```
###### 1.3. ¿Por qué Funciona?
> Usando una aproximación de primer orden de Taylor se puede mostrar que la siguiente relación entre la varianza de la serie transformada y la no transformada se cumple:
> 	$Var(z_t) \approx y_t^{2\lambda - 2} \cdot Var(y_t)$
> Ahora supongamos que la varianza de la serie temporal es proporcional a su valor:
> 	$Var(z_t) \approx y_t^{2\lambda - 2} \cdot y_t = y_t^{2\lambda - 1}$
> Entonces, para hacer que la varianza de $z_t$​ sea constante deberíamos elegir:
> 	$2\lambda - 1 = 0 \;\;\Rightarrow\;\; \lambda = \tfrac{1}{2}$
> Es decir, en ese caso la transformación de Box-Cox es esencialmente una transformación de raíz cuadrada. Resultados similares se cumplen siempre que podamos suponer que la varianza de la serie temporal es proporcional a una potencia de su valor, es decir:
> 	$Var(y_t) \propto y_t^k$
> Esto significa que para la desviación estándar:
> 	$Sd(y_t)^2 \propto y_t^k$
> Y si hacemos un diagrama de dispersión log-log de $Sd(y_t)$ vs. $y_t$​ (usando estimaciones locales), la pendiente de la recta de regresión ajustada a ese gráfico nos dará el valor de $k$, lo cual a su vez nos llevará a $\lambda$ (como se ilustró arriba para el caso $k=1$).
#### 2. Analizar si es Necesario la Diferenciación
###### 2.1. 

