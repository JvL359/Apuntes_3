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
> Paso idéntico al de las clases anteriores.
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
#### 2. Analizar Necesidad de Diferenciar: Diferenciación para Eliminar una Tendencia Lineal
###### 2.1. Definición
> Supongamos que $Y_t$​ es una serie temporal con una tendencia lineal, por ejemplo:
> 	$Y_t = a + bt + u_t$
> donde $u_t$ es estacionario. Entonces:
> 	$\nabla Y_t = Y_t - Y_{t-1} = b + \nabla u_t$
> Ahora bien, si $u_t$​ es (débilmente) estacionario, lo mismo ocurre con su primera diferencia. Sin embargo, hay que tener en cuenta que diferenciar añade dinámicas adicionales a la serie temporal.
> Por ejemplo, si $u_t$ es ruido blanco, entonces su diferencia será estacionaria, pero ya no será ruido blanco, será por definición un proceso $MA(1)$.
> Por lo tanto, la diferenciación debe mantenerse al mínimo. Si sobre-diferenciamos la serie temporal, las funciones ACF y PACF pueden dejar de ser útiles para encontrar un buen ajuste.
###### 2.2. Ejemplo: Serie de Precios de Cierre de las Acciones de Google
> 1. Esta serie temporal muestra claramente una tendencia.
> 2. Por lo tanto, aplicamos una primera diferencia regular de orden 1. El resultado sugiere que la serie temporal diferenciada se comporta como ruido blanco (podemos usar las herramientas de diagnóstico que aprendimos en la sesión anterior para comprobarlo). En particular, el precio de cierre de las acciones parece ser un random walk).
> 3. Pero cuando sobre-diferenciamos, aparece una nueva dinámica en la serie resultante, como muestran la ACF y la PACF de abajo. Ajustar un modelo sobre esta segunda diferencia sería una mala idea, porque haría que los pronósticos y las estimaciones fueran poco fiables.
```r
# 1. Plot Triple de la Serie, su ACF y su PACF
ggtsdisplay(goog)

# 2. Primera Diferencia Regualar de Orden 1
ggtsdisplay(diff(goog, differences = 1))

# 3. Segunda Diferencia Regualar de Orden 1
ggtsdisplay(diff(goog, differences = 2))
```
###### 2.3. ¿Cuándo Usar la Segunda Diferencia?
> 1. Típicamente, cuando tenemos series cuya tendencia se ajusta mejor con una curva cuadrática en lugar de una lineal. Por ejemplo, la serie temporal del PIB de EEUU.
> 2. Si aplicamos una primera diferencia para eliminar una tendencia lineal, obtenemos lo siguiente.
> 3. Como todavía se observa una tendencia ascendente, aplicamos una segunda diferencia, y ahora la serie resultante se parece mucho más a una serie temporal estacionaria.
```r
# 1. Plot Triple de la Serie, su ACF y su PACF
ggtsdisplay(usgdp)

# 2. Primera Diferencia Regualar de Orden 1
ggtsdisplay(diff(usgdp, differences = 1))

# 3. Segunda Diferencia Regualar de Orden 1
ggtsdisplay(diff(usgdp, differences = 2))
```

### III. Extra
#### 1. Función ndiffs
> Esta función calcula las diferencias de una serie temporal y luego realiza un test de hipótesis para comprobar si el resultado es estacionario.
> Pero ten en cuenta que los resultados de los tests de estacionariedad a menudo son difíciles de interpretar (la hipótesis nula puede no ser tan sencilla como parece).
> Se recomienda practicar examinando los gráficos para decidir el número de diferenciaciones necesarias, en lugar de depender ciegamente de `ndiffs`.
```r
# La salida en este caso es 2
ndiffs(usgdp)
```
#### 2. Nota: Diferenciar con diff
> Hay que tener cuidado porque una diferencia regular de segundo orden es:
> 	*$\nabla(\nabla Y_t) = \nabla^2 Y_t = \nabla(Y_t - Y_{t-1}) = (Y_t - Y_{t-1}) - (Y_{t-1} - Y_{t-2}) = Y_t - 2Y_{t-1} + Y_{t-2}$*
> Esto es muy diferente de calcular simplemente $Y_t - Y_{t-2}$​.
> Sin embargo, la función `diff` se puede usar para calcular ambas operaciones, y necesitas saber cuál estás utilizando. 
> Los argumentos *`lag`* y *`differences`* son los que debemos entender.
> En caso de duda, si necesitásemos una diferencia de segundo orden *$\nabla^2 Y_t$* siempre se puede aplicar `diff` dos veces.
```r
# 1. lag = 2 calcula y_t - y_{t-2}
diff(y, lag = 2)

# 2. differences = 2 calcula la diferencia de segundo orden: y_t - 2y_{t-1} + y_{t-2}
diff(y, differences = 2)

# 3. diff dos veces es equivalente a differences = 2
diff(diff(y))
```

Los apuntes continúan en [[Week 5 - SARIMA Processes]]