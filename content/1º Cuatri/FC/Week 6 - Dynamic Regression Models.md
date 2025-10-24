### I. Previos
#### 1. Carga de Librerías
> Añadimos paquetes para regresión dinámica y funciones de transferencia. `TSA` y `astsa` facilitan modelos _transfer function_ (Pankratz). `Hmisc::Lag()` ayuda a crear lags con NAs conservando el índice temporal.
```r
# Librerías
library(MLTools)
library(fpp2)
library(ggplot2)
library(readxl)
library(lmtest)
library(tseries)
library(tidyverse)
library(TSstudio)
library(astsa)
library(TSA)
library(Hmisc)  # variables lageadas
```
#### 2. Directorio
> Igual que en semanas previas.
```r
# Setear el Directorio
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
```

### II. Formulación del Modelo
#### 1. Formulación
> **Pankratz (Transfer Function):**  
> $y[t] = c + \frac{\omega(B)}{\delta(B)}, x[t-b] + v[t]$, con $v[t]$ ruido ARIMA $(p,d,q)(P,D,Q)_s$.  
> Donde $y$ es la variable de salida, $x$ la de entrada, y $v$ es el ruido autocorrelacionado ARMA.

### III. Ejemplo 1
#### 1. Formato
> Para este ejemplo, la variable de entrada `x1` será ruido blanco.
#### 2. Generar la Variable Explicativa Aleatoria
> Creamos **`x1`** como **ruido blanco gaussiano** y lo convertimos en objeto `ts`.  
> Con **`ggtsdisplay()`** inspeccionamos la serie, su **ACF/PACF** y un **histograma**: al ser ruido blanco, salvo el lag 0 todas las barras deberían caer dentro de las bandas azules (no hay autocorrelación apreciable).  
> A continuación simulamos el **ruido ARMA del modelo** (aquí un **AR(1)** con ϕ=0.8 y σ²=0.25). Su ACF debe **decaer geométricamente** y la PACF **cortarse en lag 1**.  
> Finalmente generamos la salida **`y1`** con una **función de transferencia simple**:  
> $y_t = 0.7\,x_t + v_t$​. En notación de Pankratz: **ω(B)=0.7 (s=0)**, **δ(B)=1 (r=0)**, **b=0** y **c=0**.  
> Para trabajar cómodos, unimos todo en un objeto multivariado.
```r
# 1. Fijamos semilla, tamaño y generamos x1 ~ WN(0,1) como objeto ts
set.seed(2024)
N <- 500
x1 <- rnorm(N)
x1 <- ts(x1)

# 2. Chequeo visual: serie + ACF/PACF + histograma (ruido blanco ?)
ggtsdisplay(x1, lag.max = 100, main = "x1", plot.type = "histogram")

# 3. Simulamos el ruido del modelo: AR(1) con phi = 0.8 y var = 0.25 (ARMA noise v(t))
set.seed(100)
ar_noise <- arima.sim(n = N, 
                      list(ar = c(0.8)),
                      sd = sqrt(0.25))
ggtsdisplay(ar_noise,lag.max = 100, main = "ARMA noise")

# 4. Salida del sistema (transfer function simple): y_t = 0.7 * x_t + v_t
y1 <- 0.7 * x1 + ar_noise

# 5. Componemos un ts multivariado con input, output y ruido y mostramos primeras filas
fdata1 <- cbind(x1, y1, n=ar_noise)
head(fdata1)
```
#### 3. Función Cross-Correlation
> Usamos la **CCF** para estudiar la correlación entre una serie y los **lags** de otra.
> 	- Primero creamos el lag de `x1` con `Hmisc::Lag()` (mantiene el índice y pone `NA` al inicio).
> 	- Comparamos con `stats::lag()` (desplaza el inicio de la serie) para que veas la diferencia.
> 	- La **CCF de `x1` con su lag1** debe mostrar un **pico = 1 en k = 1** (propiedad trivial de una serie con su propio lag).
> 	- Por último, miramos la **CCF de `y1` con `x1`**: como $y_t = 0.7\,x_t + v_t$, el pico fuerte aparece en **lag 0**.
```r
# 1. Creamos el lag 1 de x1 con Hmisc::Lag() (conserva el índice y pone NA al inicio)
x1_lag1 <- Lag(x1, shift = 1)
head(x1_lag1)

# 2. Para esta demo, rellenamos el NA inicial con 0 y comparamos con stats::lag()
x1_lag1[is.na(x1_lag1)] <- 0
head(stats::lag(x1, n = 1))  # distinto: cambia el inicio de la serie

# 3. CCF entre x1 y su propio lag1 -> pico = 1 en k = 1
ccf(y = x1, x = x1_lag1)
abline(v = -5:5, col="orange", lty = 2)

# 4. Alternativa: usar na.action = na.pass para no rellenar el NA manualmente
ccf(y = x1, x = Lag(x1, shift = 1), na.action = na.pass)
abline(v = -5:5, col="orange", lty = 2)

# 5. CCF entre la salida y1 y la entrada x1 -> máximo en lag 0 (por y_t = 0.7 x_t + v_t)
ccf(y = y1, x = x1)
abline(v = -5:5, col="orange", lty = 2)
```
#### 4. Modelo Clásico de Regresión Lineal
> Ajustamos una **regresión estática** $y_1 \sim x_1$​ sin intercepto (la teoría dice β≈0.7).  
> El coeficiente sale significativo, **pero los residuos muestran autocorrelación** (el término de error real es AR(1)), así que el modelo no captura toda la dinámica.  
> La CCF entre **residuos** y `x1` no muestra correlación marcada (coherente con que `x1` es ruido blanco sin autocorrelación).
```r
# 1. OLS no dinámico (sin intercepto)
lm1.fit <- lm(y1 ~ x1 - 1, data = fdata1 )

# 2. Resumen (β debería ≈ 0.7, significativo)
summary(lm1.fit)

# 3. Diagnóstico de residuos: no parecen ruido blanco (BG/Ljung-Box significativos)
CheckResiduals.ICAI(lm1.fit, lag=100)

# 4. CCF de residuos del OLS con x1 (no debería quedar relación fuerte)
ccf(y = residuals(lm1.fit), x = x1)
abline(v = -5:5, col="orange", lty = 2)
```
#### 5. Modelo de Función de Transferencia
> Volvemos al enfoque **dinámico**: $y_t = \frac{\omega(B)}{\delta(B)}x_t + v_t$ con $v_t$​ AR(1).  
> En este ejemplo: $\omega(B)=\omega_0$ con $s=0$, $\delta(B)=1$ con $r=0$, $b=0$, e **incluimos AR(1)** en el ruido.  
> En `TSA::arima`, esto se especifica con `xtransf` (entrada) y `transfer = list(c(r, s))`.
```r
# Transfer function + AR(1) en el ruido: y_t = ω0 * x_t + v_t,  v_t = AR(1)
arima1.fit <- TSA::arima(y1,
                    order=c(1,0,0),                # AR(1) para el ruido v_t
                    # seasonal = list(order=c(0,0,0),period=24),
                    xtransf = x1,                  # variable(s) de entrada
                    transfer = list(c(0,0)),       # (r, s) = (0, 0) => ω(B)=ω0, δ(B)=1
                    include.mean = FALSE,          # c = 0 en este ejemplo
                    method="ML")
```
#### 6. Diagnóstico del Modelo
> - `summary()` → esperamos **ω₀ ≈ 0.7** y **AR1 ≈ 0.8**, ambos significativos.
> - `coeftest()` → esperamos **ω₀ ≈ 0.7** y **AR1 ≈ 0.8**, ambos significativos.
> - `CheckResiduals.ICAI()` → **residuos ≈ ruido blanco** (p-valor grande en Ljung–Box).
> - `CCF(residuos, x1)` → **sin picos**, no queda correlación entre la entrada y los errores.
```r
# 1. Resumen: coeficientes (ω0 y AR1), AIC y métricas de error
summary(arima1.fit)

# 2. Significancia de los parámetros (t-tests)
coeftest(arima1.fit)

# 3. Residuos ~ ruido blanco (ACF/PACF sin estructura; Ljung-Box no significativo)
CheckResiduals.ICAI(arima1.fit, lag=100)

# 4. CCF entre entrada y residuos (debería quedar plana si el modelo está bien ajustado)
ccf(y = residuals(arima1.fit), x = x1)
abline(v = -5:5, col="orange", lty = 2)
```

### IV. Ejemplo 2
#### 1. Formato
> Para este ejemplo, conservaremos la variable de entrada `x1` como ruido blanco, y añadiremos una variable `x2` _time series_ con autocorrelación.
#### 2. Generar la Variable Explicativa Autocorrelacionada
> Cargamos **`x2`** desde archivo y la convertimos a `ts`.  
> Con **`ggtsdisplay()`** vemos que **`x2` es claramente autocorrelacionada**: la **ACF decae lentamente** (cola larga) y la **PACF** muestra **picos iniciales altos**.  
> Mantenemos el **ruido AR(1)** del ejemplo 1 (`ar_noise`) y generamos la salida **`y2`** con una **transfer function simple**:  
> $y_t = 0.7\,x_t + v_t$​, donde $v_t$ es AR(1).  
> En notación de Pankratz: ω(B)=0.7 (s=0), δ(B)=1 (r=0), b=0, c=0, y ruido AR(1) en el error.
```r
# 1. Cargamos x2 y la pasamos a ts
x2 <- read.table("TEMP.dat", sep = "", header = TRUE)
x2 <- ts(x2$TEMP)

# 2. Inspección: serie + ACF/PACF muestran autocorrelación marcada
ggtsdisplay(x2,lag.max = 100, main = "x2")

# 3. Salida del sistema con el mismo ruido AR(1) del ejemplo 1
y2 <- 0.7 * x2 + ar_noise

# 4. Dataset multivariado para trabajar cómodo
fdata2 <- cbind(x2, y2, n=ar_noise)
head(fdata2)
```
#### 3. Función Cross-Correlation
> La **CCF(y2, x2)** ahora muestra muchos lags significativos alrededor de 0 (no un único pico).  
> ¿Por qué? Porque **`x2` está autocorrelacionada**: 
> La CCF mezcla el efecto causal $y_t \leftarrow x_t$​ con la **estructura interna** de `x2`.  
> Con inputs autocorrelacionados, lo correcto es **preblanquear** `x2` (y filtrar `y2` con el mismo filtro) antes de usar CCF para identificar retardos.
```r
# CCF directa (sin preblanqueo): aparece un “bloque” de lags significativos
ccf(y = y2, x = x2)
abline(v = -5:5, col="orange", lty = 2)
```
#### 4. Modelo Clásico de Regresión Lineal
> Ajustamos un **OLS estático** y2∼x2y_2 \sim x_2y2​∼x2​ sin intercepto. 
> El coeficiente sale muy significativo (≈ 0.7) y el R² es altísimo, **pero los residuos no son ruido blanco** (presentan autocorrelación) **y además quedan correlacionados con la entrada** → el modelo **no capta la dinámica** (el error verdadero es AR(1) y `x2` es autocorrelacionada).
```r
# 1. OLS no dinámico
lm2.fit <- lm(y2 ~ x2 - 1, data = fdata2 )

# 2. Resumen (β ≈ 0.7, pero ojo con la inferencia en series)
summary(lm2.fit)

# 3. Diagnóstico: residuos con estructura temporal
CheckResiduals.ICAI(lm2.fit, lag=100)

# 4. Aún hay correlación entre residuos e input (mala señal)
ccf(y = residuals(lm2.fit), x = x2)
abline(v = -5:5, col="orange", lty = 2)
```
#### 5. Modelo de Función de Transferencia
> Corregimos las carencias del OLS con un **modelo de función de transferencia** + **ruido AR(1)**:  $y_t = \omega_0 x_t + v_t,\; v_t=\text{AR}(1)$.  
> En `TSA::arima`, esto se expresa con `xtransf = x2` y `transfer = list(c(0,0))` (es decir, r=0,s=0).
```r
# Transfer function con AR(1) en el ruido (usa la arima de TSA)
arima2.fit <- arima(y2,
                    order=c(1,0,0),      # AR(1) en el ruido
                    xtransf = x2,        # variable de entrada
                    transfer = list(c(0,0)), # (r, s) = (0, 0): ω(B)=ω0, δ(B)=1
                    include.mean = FALSE,
                    method="ML")
```
#### 6. Diagnóstico del Modelo
> - `summary()` → esperamos **ω₀ ≈ 0.7** y **AR1 ≈ 0.73**, ambos **significativos**. 
> - `coeftest()` → esperamos **ω₀ ≈ 0.7** y **AR1 ≈ 0.73**, ambos **significativos**. 
> - `CheckResiduals.ICAI()` → **residuos ≈ ruido blanco** (p-valor Ljung–Box alto).
> - **CCF(residuos, x2)** → **plana** (sin correlación remanente).  
> Con esto, el modelo **pasa todas las comprobaciones**.
```r
# 1. Coeficientes y métricas
summary(arima2.fit) # summary of training errors and estimated coefficients

# 2. Significancia estadística
coeftest(arima2.fit)

# 3. Residuos: ¿ruido blanco?
CheckResiduals.ICAI(arima2.fit, lag=100)

# 4. No debe quedar correlación entre input y residuos
ccf(y = residuals(arima2.fit), x = x2)
abline(v = -5:5, col="orange", lty = 2)
```

### V. Ejemplo 3
#### 1. Formato
> Para este ejemplo, conservaremos la variable de entrada `x1` como ruido blanco, y lagearemos la variable `x2` _time series_ con autocorrelación.
#### 2. Generar la Variable Explicativa Autocorrelacionada y Lageada
> Construimos una **versión rezagada** de `x2` con **`Lag(x2, 3)`** y **eliminamos los `NA` iniciales** (ojo al `Start` que cambia).  
> Para **alinear** perfectamente las tres series (`x2`, `x2lg3`, `ar_noise`) usamos **`ts.intersect()`**. Guardamos los nombres de columnas, **creamos la salida** con la función de transferencia simple  
> $y_4[t] = 0.7 \, x_2[t-3] + v(t)$ (el mismo **ruido AR(1)** de antes) y **restauramos** los nombres.  
> Finalmente, extraemos **vectores `ts`** listos para el modelado.
```r
# 1. Serie rezagada 3 pasos y sin NAs iniciales
x2lg3 <- na.omit(Lag(x2, 3))
head(x2lg3)

# 2. Alineación segura de x2, x2lg3 y ar_noise
fdata4 <- ts.intersect(x2, x2lg3, ar_noise)
nc4 <- ncol(fdata4)
cnames4 <- colnames(fdata4)
head(fdata4)

# 3. Generamos la salida con TF simple: y4 = 0.7 * x2[t-3] + v(t)
fdata4 <- cbind(fdata4, y4 = 0.7 * fdata4[,"x2lg3"] + fdata4[,"ar_noise"])
head(fdata4)

# 4. Restauramos nombres originales de las columnas intersectadas
colnames(fdata4)[1:nc4] <- cnames4
head(fdata4)

# 5. Vectores ts finales
y4 <- fdata4[,"y4"]
x2 <- fdata4[,"x2"]
x2lg3 <- fdata4[,"x2lg3"]
```
#### 3. Función Cross-Correlation
> La **CCF(y4, x2)** directa muestra un “bloque” de lags significativos alrededor de 0 debido a la **autocorrelación de `x2`**; aun así, se intuye **b = 3**. Más adelante confirmaremos `b` con **LTF/Prewhitening**.
```r
# CCF directa entre la salida y4 y la entrada x2
ccf(y = y4, x = x2, lwd=2)
abline(v = -5:5, col="orange", lty = 2)
```
#### 4. Modelo de Función de Transferencia
> Estrategia en dos pasos:  
> - **(i) Identificación preliminar** con un TF **muy flexible en el numerador** (`s` grande) y **ruido AR(1)** de baja complejidad. Miramos qué **coeficiente de la TF** destaca → pista para `b`.  
> - **(ii) Diagnóstico del “regression error”**: si hay tendencia, **diferenciamos** (`d=1`) y proponemos una estructura ARMA para el ruido. Con el lag detectado (`b=3`) ajustamos el **modelo final** sencillo $\omega(B)=\omega_0, \delta(B)=1$.
```r
# 1. TF preliminar (numerador largo para "descubrir" el retardo), ruido AR(1)
TF.fit <- TSA::arima(y4,
                order=c(1, 0, 0),
                #seasonal = list(order=c(1,0,0),period=24),
                xtransf = x2,
                transfer = list(c(0, 9)), #List with (r,s) orders
                include.mean = TRUE,
                method="ML")
                
# 2. Coeficientes y significancia (el lag ~3 debería sobresalir)
summary(TF.fit)
coeftest(TF.fit)

# 3. Gráfico de identificación: qué lags del numerador son relevantes
TF.Identification.plot(x2, TF.fit)

# 4. Error de regresión: decide si hace falta diferenciar y sugiere ARMA del ruido
TF.RegressionError.plot(y4, x2, TF.fit, lag.max = 100)

# 5. Usamos el retardo detectado: b = 3 (xlag), y diferenciamos d = 1
xlag = Lag(x2, 3)   # b
xlag[is.na(xlag)]=0

# 6. Modelo final: TF simple con b=3 + ruido ARIMA(1,1,0)
arima.fit <- arima(y4,
                   order=c(1, 1, 0), # ARMA model for the noise
                   xtransf = xlag,
                   transfer = list(c(0, 0)), #List with (r,s) orders
                   include.mean = FALSE,
                   method="ML")
```
#### 5. Diagnóstico del Modelo
> - **Parámetros**: esperamos **ω₀ ≈ 0.7** y **AR1 ≈ 0.7–0.8**, ambos **significativos**.
> - **Residuos**: deben parecer **ruido blanco** (ACF/PACF sin estructura; **Ljung–Box** no significativo).
> - **CCF(residuos, x2)**: **plana** (sin correlación remanente con la entrada).
```r
# 1. Resumen del ajuste
summary(arima.fit)

# 2. Significancia de parámetros
coeftest(arima.fit)

# 3. Residuos ≈ ruido blanco (p-valor Ljung–Box alto)
CheckResiduals.ICAI(arima.fit, lag=25)

# 4. No debe quedar correlación entre la entrada y los residuos
res <- residuals(arima.fit)
res[is.na(res)] <- 0
ccf(y = res, x = x2)
```
#### 6. Prewhitening
> Para **confirmar el retardo** cuando la entrada está autocorrelacionada:
> Ajusta ARIMA a `x2` (residuos ≈ WN). 2) **Filtra `y4` con el mismo modelo** para “remover” la autocorrelación inducida. 3) Calcula **CCF** entre **`y4` transformada** y **residuos de `x2`**.  
> El resultado destaca nítidamente **b = 3**, frente a la CCF directa que era confusa.
```r
# 1. Prewhitening automático (TSA): CCF de salida transformada vs residuos de la entrada
prewhiten(y4, x2, main="Prewhitening of y4 & x2")
abline(v = -5:5, col="orange", lty = 2)

# 2. Comparación: CCF directa (más confusa)
ccf(y4, x2)
abline(v = -5:5, col="orange", lty = 2)
```
