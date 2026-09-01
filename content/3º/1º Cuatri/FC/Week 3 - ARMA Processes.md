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
> Paso idéntico al de las clases anteriores.
```r
# Setear el Directorio
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
```

### II. AR Processes
#### 1. Caso No Estacional
###### 1.1. Definición
> Un proceso estocástico $Y_t$ se considera AutoRegresivo si satisface la siguiente ecuación:
> 	$Y_t = \phi_1 Y_{t-1} + \phi_2 Y_{t-2} + \dots + \phi_p Y_{t-p} + \varepsilon_t$ 
> 	- $\varepsilon_t$ es Ruido Blanco Gaussiano.
> 	- $\phi_1, \dots, \phi_p$ son constantes llamadas coeficientes del proceso.
> 	- $p$ es el orden del proceso, que este es llamado $AR(p)$.
> Una serie temporal que proviene de un proceso AR se denomina *serie temporal autorregresiva*.
> Este tipo de proceso puede entenderse como análogo a un *modelo de regresión lineal múltiple*, con la diferencia de que las variables explicativas no son externas, sino que son los lags recientes de la propia serie. En otras palabras, la predicción de $Y_t$​ se hace usando como predictores los valores anteriores de la misma serie. Así, la serie se “regresa sobre sí misma”.
###### 1.2. BackShift Operator y Characteristic Polynomial
> Usando un Operador de Retroceso  $B(Y_t) = Y_{t-1}$  podemos reescribir el proceso como:
> 	$\Phi(B)Y_t = (1- \phi_1B - \dots - \phi_pB^p)Y_t = \varepsilon_t$
> 	donde $\Phi(B) = (1- \phi_1B - \dots - \phi_pB^p)$ es el polinomio característico del proceso.
###### 1.3. Estacionariedad de un AR
> No todos los procesos AR son estacionarios: un random walk es un ejemplo de proceso $AR(1)$, pero sabemos que no es estacionario. Un proceso autorregresivo $AR(p)$ es estacionario si y solo si las raíces del polinomio característico están fuera del círculo unitario.
> 	Nota: círculo de radio 1 centrado en el (0,0) en el plano complejo.
#### 2. Serie Temporal Generada por un AR(2) Puro
###### 2.1. Ecuación Inicial
> Usando la notación del Polinomio Característico:
> 	$(1 - (1/3)B - (1/2)B^2)Y_t = \varepsilon_t$
###### 2.2. Punto de Inicio
> En este caso el punto de inicio será Ruido Blanco Gaussiano.
```r
# Creación de Ruido Blanco Gaussiano
n <- 500
set.seed(42)
w <- ts(rnorm(n, mean = 0, sd = 1))
head(w, 25)
```
###### 2.3. Serie AutoRegresiva
> Con un bucle vamos generando la serie.
```r
# 1. Vector de Coeficientes
phi <- c(1/3, 1/2)

# 2. Vector Nulo de Longitud n
y <- rep(0, n)

# 3. Primeros Valores
y[1] <- w[1]
y[2] <- -phi[1] * y[1] + w[2]

# 4. Bucle de Simulación de la Serie
for (t in 3:n){
  y[t] <- phi[1] * y[t - 1] + phi[2] * y[t - 2] + w[t]
}

# 5. Objeto Serie Temporal
y <- ts(y)
```
###### 2.4. Gráficas de la Serie
> Podemos graficar la serie para ver el comportamiento obtenido tras aplicar esta lógica.
```r
# Plot de la Serie
autoplot(head(y, 100))
```
#### 3. ACF y PACF de un Modelo AR(p) Puro
> Dada una serie temporal generada por un proceso $AR(p)$ puro, tratar de identificar el valor de $p$ a partir de la ACF no es sencillo. La ACF teórica de un proceso AutoRegresivo puro decae exponencialmente. Sin embargo, el patrón de ese decaimiento puede ser complejo y, además, en la práctica solo tenemos acceso a valores estimados de la ACF.
> Esa es la razón por la que se utiliza la PACF. La autocorrelación parcial mide la correlación entre valores rezagados (lags) en una serie temporal cuando eliminamos la influencia de los rezagos intermedios que también están correlacionados.
> La PACF (teórica) de un proceso autorregresivo puro $AR(p)$ es igual a 0 para rezagos mayores que $p$. En la práctica, esto significa que en los gráficos de PACF (estimada) esperamos que solo los primeros $p$ rezagos sean significativamente distintos de 0.
> Sin embargo, es importante recordar que la ACF y la PACF deben considerarse siempre conjuntamente para identificar la estructura del proceso.
```r
# Plot Triple de la Serie AutoRegresiva, su ACF y su PACF
ggtsdisplay(y, lag.max = min(n/5, 50))
```
#### 4. Entrenamiento del Modelo
> Suponiendo que sabemos que la serie fue generada mediante un $AR(2)$, pero no sabemos los coeficientes $\phi_1, \phi_2$. Podemos entrenar un modelo ARIMA sobre la serie de datos, escogiendo los parámetros (p,d,q) como (2,0,0).
```r
# 1. Entrenamiento con un Orden de un AR(2)
arima.fit <- Arima(y, order=c(2, 0, 0), include.mean = FALSE)

# 2. Resumen de los Errores de Training y Coeficientes Estimados
summary(arima.fit) 

# 3. Significancia Estadística de los Coeficientes Estimados
coeftest(arima.fit)
```
#### 5. Visualización del Modelo
> Nos sirve para analizar gráficamente los resultados del modelo ARIMA ajustado. Se incluyen representaciones del modelo; la validación de residuos, que se definen como $e_t = \hat{y}_t - y_t$ y deberían comportarse como Ruido Blanco Gaussiano; y la comparación entre valores reales y ajustados.
```r
# 1. Estacionariedad
autoplot(arima.fit)

# 2. Diagnóstico de Residuos (Se comporta como ruido blanco?)
CheckResiduals.ICAI(arima.fit, bins = 100, lags = 20)

# 3. ACF y PACF de los Residuos (Adecuación del modelo)
ggtsdisplay(residuals(arima.fit), lag.max = 20)
# Si los residuos no son ruido blanco, cambiar el orden del ARMA

# 4. Comparativa Serie Real y los Valores Ajustados
autoplot(y, series = "Real") +
  forecast::autolayer(arima.fit$fitted, series = "Fitted")
```

### III. MA Processes
#### 1. Caso No Estacional
###### 1.1. Definición
> Un proceso estocástico $Y_t$ se considera MovingAverage si satisface la siguiente ecuación:
> 	$Y_t = \varepsilon_t + \theta_1 \varepsilon_{t-1} + \theta_2 \varepsilon_{t-2} + \dots + \theta_q \varepsilon_{t-q}$
> 	- $\varepsilon_t$ es Ruido Blanco Gaussiano.
> 	- $\theta_1, \dots, \theta_p$ son constantes llamadas coeficientes del proceso.
> 	- $q$ es el orden del proceso, que este es llamado $MA(q)$.
> Una serie temporal que proviene de un proceso MA se denomina _serie temporal de media móvil_.  
> A diferencia de un modelo AR, aquí el valor de $Y_t$​ no se explica a partir de sus propios rezagos, sino como una combinación lineal del ruido blanco actual y de errores aleatorios pasados.  
> Es importante notar que estos errores ($\varepsilon_{t-k}$) no son observables directamente y los coeficientes $\theta_k$​ solo pueden conocerse al ajustar el modelo.
###### 1.2. Characteristic Polynomial
> El Polinomio Característico de un proceso MA(q) es el siguiente:
> 	$\Theta(B) = 1 + \theta_1B + \dots + \theta_qB^q$
> Usando esta notación el proceso se puede reescribir como:
> 	$Y_t = \Theta(B)\varepsilon_t$
###### 1.3. Invertibilidad
> Un proceso $MA(q)$ es invertible si se puede expresar como un proceso $AR(\infty)$:
> 	$\varepsilon_t = \Theta(B)^{-1} Y_t = (1 + \pi_1B + \pi_2B^2 + \pi_3B^3 + \dots)Y_t$
> Un proceso AverageMoving $MA(q)$ es invertible si y solo si las raíces del polinomio característico están fuera del círculo unitario.
#### 2. Serie Temporal Generada por un MA(2) Puro
###### 2.1. Ecuación Inicial
> Análogo al apartado anterior empezamos con la ecuación del polinomio característico:
> 	$Y_t = \varepsilon_t + 0.4 \varepsilon_{t-1} - 0.3 \varepsilon_{t-2} = (1+ 0.4B -0.3B^2) \varepsilon_t$
###### 2.2. Punto de Inicio
> En este caso el punto de inicio será Ruido Blanco Gaussiano.
```r
# Creación de Ruido Blanco Gaussiano
set.seed(42)
n <- 1000
w <- rnorm(n)
head(w, 25)
```
###### 2.3. Serie AutoRegresiva
> Con un bucle vamos generando la serie.
```r
# 1. Vector de Coeficientes
theta <- c(0.4, -0.3)

# 2. Vector Nulo de Longitud n
y <- rep(0, n)

# 3. Primeros Valores
y[1] <- w[1]
y[2] <- w[2] + theta[1] * w[1] 

# 4. Bucle de Simulación de la Serie
for (t in 3:n){
  y[t] <- w[t] + theta[1] * w[t - 1] + theta[2] * w[t - 2]
}

# 5. Objeto Serie Temporal
y <- ts(y)
```
###### 2.4. Gráficas de la Serie
> Podemos graficar la serie para ver el comportamiento obtenido tras aplicar esta lógica.
```r
# Plot de la Serie
autoplot(head(y, 100))
```
#### 3. ACF y PACF de un Modelo MA(p) Puro
> Para una serie generada por un proceso $MA(q)$ puro, la pauta es “la inversa” del caso $AR(p)$. La ACF teórica se anula a partir del rezago $q$ (corte neto), mientras que la PACF decae (a menudo de forma exponencial, con patrones que pueden variar).  
> En la práctica, en la ACF (estimada) esperamos que solo los primeros $q$ lags sean significativamente distintos de 0; en la PACF veremos decaimiento rápido sin un corte claro.  
> Aun así, para una identificación correcta, ACF y PACF deben leerse conjuntamente y no de forma mecánica.
```r
# Plot Triple de la Moving Average, su ACF y su PACF
ggtsdisplay(y, lag.max = min(n/5, 30))
```
#### 4. Entrenamiento del Modelo
> Suponiendo que sabemos que la serie fue generada mediante un $MA(2)$, pero no conocemos los coeficientes $\theta_1, \theta_2$​. Podemos entrenar un modelo ARIMA sobre la serie de datos, escogiendo los parámetros (p,d,q) como (0,0,2).
```r
# 1. Entrenamiento con un Orden de un MA(2)
arima.fit <- Arima(y, order=c(0, 0, 2), include.mean = FALSE)

# 2. Resumen de los Errores de Training y Coeficientes Estimados
summary(arima.fit) 

# 3. Significancia Estadística de los Coeficientes Estimados
coeftest(arima.fit)
```
#### 5. Visualización del Modelo
> Nos sirve para analizar gráficamente los resultados del modelo ARIMA ajustado. Se incluyen representaciones del modelo; la validación de residuos, que se definen como $e_t = \hat{y}_t - y_t$ y deberían comportarse como Ruido Blanco Gaussiano; y la comparación entre valores reales y ajustados.
```r
# 1. Estacionariedad
autoplot(arima.fit)

# 2. Diagnóstico de Residuos (Se comporta como ruido blanco?)
CheckResiduals.ICAI(arima.fit, bins = 100, lags = 20)

# 3. ACF y PACF de los Residuos (Adecuación del modelo)
ggtsdisplay(residuals(arima.fit), lag.max = 20)
# Si los residuos no son ruido blanco, cambiar el orden del ARMA

# 4. Comparativa Serie Real y los Valores Ajustados
autoplot(y, series = "Real") +
  forecast::autolayer(arima.fit$fitted, series = "Fitted")
```

### IV. ARMA Processes
#### 1. Definición
> Un proceso estocástico $Y_t$ se considera AutoRegresivo y MovingAverage si satisface la ecuación: 
> 	$Y_t = \phi_1 Y_{t-1} + \dots + \phi_p Y_{t-p} + \theta_1 \varepsilon_{t-1} + \dots + \theta_q \varepsilon_{t-q}$
> 	Que es una combinación de la ecuación de AR y de MA.
#### 2. Characteristic Polynomial
> La expresión en términos del polinomio característico de un proceso $ARMA(p, q)$ es la siguiente:
> 	$\Phi(B) Y_t = \Theta(B) \varepsilon_t$
#### 3. Estacionariedad e Invertibilidad
> Un proceso $ARMA(p , q)$ es estacionario e invertible al mismo tiempo si las raíces de los dos polinomios $\Phi(B)$ y $\Theta(B)$ están fuera del círculo unitario.
#### 4. Serie Temporal Generada por un ARMA(p, q)
> Ecuación Inicial: $Y_t = \phi_1 Y_{t-1} + \phi_2 Y_{t-2} + \varepsilon_t + \theta_1 \varepsilon_{t-1} + \theta_2 \varepsilon_{t-2}$
```r
# 1. Creación de Ruido Blanco Gaussiano
set.seed(42)
n <- 1000
w <- rnorm(n)

# 2. Vectores de Coeficientes Aleatoriosx
phi <- c(runif(1, -1, 1), 0)
theta <- c(runif(1, -1, 1), 0)

# 3. Vector Nulo de Longitud n
y <- rep(0, n)

# 3. Primeros Valores
y[1] <- w[1]
y[2] <- phi[1] * y[1] + w[2] + theta[1] * w[1] 

# 4. Bucle de Simulación de la Serie
for (t in 3:n){
  y[t] <- phi[1] * y[t - 1] + phi[2] * y[t - 2] + w[t] + theta[1] * w[t - 1] + theta[2] * w[t - 2]
}

# 5. Objeto Serie Temporal
y <- ts(y)

# 6. Plot de la Serie
autoplot(y)
```
#### 5. ACF y PACF de un Modelo ARMA(p, q)
> Como podemos ver, los patrones en la ACF y la PACF son más difíciles de analizar, y básicamente nos dicen que esto no es un proceso AR o MA puro. Pero encontrar el orden puede ser complicado, y a menudo es cuestión de prueba y error, guiándose por las herramientas de diagnóstico que ya hemos visto.
> Nuestro objetivo será llegar a un modelo con coeficientes significativos y residuos que se comporten como ruido blanco.
> Una regla básica es mantener las cosas simples. A veces puede ser tentador empezar con un modelo bastante complejo, como un $ARMA(2,2)$, y luego eliminar los coeficientes no significativos, pero esto no es una buena idea.
> Repetimos una vez más: la ACF y la PACF deben considerarse conjuntamente. En particular, es un error pensar algo como: “obtienes $p$ mirando la PACF y $q$ mirando la ACF”.
> En resumen: en ARMA la identificación no es tan directa como en AR o MA puros, y lo importante es simplicidad, significancia de coeficientes y residuos tipo ruido blanco.
```r
# Plot Triple de la ARMA, su ACF y su PACF
ggtsdisplay(y, lag.max = min(n/5, 30))
```

### V. Extra: Convertir fechas del último al primer día del mes
> Algunos conjuntos de datos mensuales guardan la fecha como último día del mes (31/01/2023).  
> Sin embargo, para análisis exploratorio (EDA) y ciertas funciones de R, es más conveniente trabajar con el primer día del mes (01/01/2023).
> Este apartado muestra cómo hacer esa conversión.
```r
# 1. Cargar los Datos con los Últimos Días de cada Mes
fdata <- read.table("month_final_day.csv", header = TRUE, sep = ",")
head(fdata)

# 2. Convertir la Columna al Formato Date
fdata$date <- as.Date(fdata$date, format = "%Y-%m-%d")
head(fdata)

# 3. Formatear el Día de la Fecha
fdata$date <- format(fdata$date, format = "%Y-%m-01")
head(fdata)

# 4. Pasar de String a Date (otra vez)
fdata$date <- as.Date(fdata$date, format = "%Y-%m-%d")
head(fdata)
```

Los apuntes continúan en [[Week 4 - ARIMA Processes & Metodología Box-Jenkins]]

