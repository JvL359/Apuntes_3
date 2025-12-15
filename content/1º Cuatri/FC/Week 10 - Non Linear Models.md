### 0. Introducción Teórica
#### 1. Motivación y Contexto
>  Limitaciones de los modelos lineales (ARIMA, TF):
    - Relación lineal entre entradas y salida.     
    - Dificultad para capturar saturaciones, umbrales, efectos asimétricos…
> Situaciones típicas en las que aparecen **no linealidades**:
    - Demanda eléctrica vs temperatura.
    - Series financieras con cambios de volatilidad/regímenes.
    - Sistemas donde el comportamiento cambia según el nivel.
> Objetivo de la semana:
    - Ver **tres formas de introducir no linealidad**:
        - Feature engineering + modelos lineales (TF).
        - Modelos no lineales explícitos (MLP/NARX).
        - Modelos no lineales basados en árboles y boosting (XGBoost).
#### 2. Modelos de Series Temporales No Lineales Basados en Regresión
##### 2.1. Modelo General de Regresión No Lineal
> Forma general:  $y_t = f(y_{t-1}, y_{t-2}, \dots, x_t, x_{t-1}, \dots) + \varepsilon_t$
> Diferencia con Linealidad: $f(\cdot)$ puede ser cualquier función no lineal (polinómica, a trozos, etc)
> $\varepsilon_t$​ sigue siendo un **término de error** (idealmente ruido blanco), igual que en ARIMA; la diferencia está en la forma de $f(\cdot)$, no en cómo tratamos el ruido.
> Conexión con ARIMA/TF: ARIMA → caso especial donde $f$ es lineal.
##### 2.2. Modelos NAR y NARX
> **NAR (Nonlinear Autoregressive)**:
    - Solo usa retardos de la propia serie: $y_t = f(y_{t-1}, \dots, y_{t-p}) + \varepsilon_t$
> **NARX (Nonlinear Autoregressive with Exogenous Inputs)**:
    - Incluye además inputs exógenos: $x_t, x_{t-1}, \dots$
> Interpretación:
    - Son la versión no lineal de AR/ARX, muy usados en control y forecasting.
##### 2.3. Modelos NARMAX
> Extensión NARX añadiendo términos de ruido pasados: $y_t = f(y_{t-1:\,t-p}, x_{t:\,t-q}, \varepsilon_{t-1:\,t-r}) + \varepsilon_t$
> Relación con ARMA/ARIMA y con modelos de caja negra.
> Comentario práctico:
    - El MLP de la práctica se parece a un **NARX** (lags de DEM y de las X) sin modelar explícitamente $\varepsilon_{t-k}$
##### 2.4. Modelos XGBOOST
> Idea básica:
> 	- Un **árbol de regresión** particiona el espacio de variables en regiones y asigna una **constante** a cada región → aproximación por tramos, altamente no lineal.
> 	- Un modelo de **boosting** (como XGBoost) combina muchos árboles “débiles” entrenados de forma secuencial, corrigiendo los errores del anterior.
> Conexión con el modelo general:
> 	- XGBoost implementa una función $y_t = f(\text{lags de } y_t,\ \text{lags de } x_t,\ \text{inputs actuales}) + \varepsilon_t$    donde $f(\cdot)$ es una suma de muchos árboles de decisión → **no lineal y muy flexible**.
> Comentario práctico:
> 	- Al igual que el MLP, XGBoost se puede usar como un **NARX no lineal**, recibiendo como inputs los lags de DEM, WD, TEMP, etc.
> 	- En vez de aprender pesos y activaciones como una red, aprende **particiones del espacio** (reglas tipo “si TEMP > 25 y DEM_lag1 alto, entonces…”).
#### 3. Modelos de Cambio de Régimen (Regime Switching)
##### 3.1. Idea Intuitiva de Cambio de Régimen
> Concepto de **regímenes o estados**:
    - Períodos de “alta demanda” vs “baja demanda”.
    - Fases de “expansión” vs “recesión”.
>Cada régimen tiene su **propio modelo**:
    - Distintos parámetros AR/MA según el estado.
##### 3.2. Tipos de Modelos de Régimen
> **Modelos threshold (TAR/SETAR)**:
    - Cambios de régimen cuando la serie cruza ciertos umbrales.
> **Modelos Markov-switching (MS-AR, MS-ARMA)**:
    - El régimen sigue una cadena de Markov oculta.
> Comentario:
    - Importantes conceptualmente, pero en las prácticas de esta semana **no se implementan**: el foco está en TF+FE y MLP.
    - Suelen ser útiles cuando vemos **cambios bruscos y persistentes** en la dinámica (no explicables solo con cambios de nivel o cambios de varianza).
#### 4. Combinación de Pronósticos
##### 4.1. Motivación para Combinar Modelos
> Distintos modelos capturan **partes diferentes** de la dinámica.
> Combinación de pronósticos:
    - Reduce riesgo de elegir “el modelo equivocado”.
    - Suele mejorar estabilidad y robustez.
##### 4.2. Estrategias Sencillas de Combinación
> Media simple de pronósticos.
> Combinaciones ponderadas (por error histórico, AIC, etc.).
> Comentario:
    - En este curso, la combinación se puede **relacionar conceptualmente** con:
        - Modelos lineales + no lineales.
        - Diferentes configuraciones (TF vs MLP) que podrían combinarse.
	- En la práctica, muchas competiciones de forecasting y aplicaciones reales usan **ensambles** (combinación de varios modelos) porque tienden a ser más **robustos** que cualquier modelo individual.
#### 5. Conexión con las Prácticas de la Semana 10
##### 5.1. TF + Feature Engineering como Modelo No Lineal Implícito
> Usar TF lineales, pero:
    - Transformar inputs (por ejemplo, dividir temperatura en `tcold` y `thot`).
    - Esto equivale a aproximar una relación no lineal con un modelo lineal por tramos en las entradas.
##### 5.2. MLP como NARX No Lineal
> Red neuronal MLP que recibe:
    - Lags de DEM (output) y de las variables exógenas.
> Se comporta como un modelo **NARX no lineal**:
    - Aprende automáticamente la forma de $f(\cdot)$.
> Validación mediante cross-validation y forecast iterativo a 7 días.
##### 5.3. XGBOOST como Regresor No Lineal
> El modelo recibe:
> 	- Lags de DEM (`DEM_lag1`, `DEM_lag7`),
> 	- Lags de WD y TEMP (`WD_lag1`, `WD_lag7`, `TEMP_lag1`, `TEMP_lag7`),
> 	- Más las variables contemporáneas (`WD`, `TEMP`).
> Así se comporta como un **modelo NARX no lineal basado en árboles**:
> - Aprende interacciones y umbrales (por ejemplo, efectos distintos de la temperatura según el tipo de día o el nivel de demanda previa).
> La **no linealidad** no se mete “a mano” como en TF+feature engineering, sino que:
> 	- XGBoost descubre automáticamente particiones y combinaciones de variables que explican mejor la demanda.
> La interpretación se apoya en:
> 	- **Importancia de variables** (`varImp(xgb.fit)`),
> 	- Comparación visual de **valores reales vs predichos** y diagnóstico de errores.

### I. Previos
#### 1. Carga de Librerías
> En esta semana añadimos las librerías de **`NeuralSens`** para el análisis de sensibilidad e interpretación de redes neuronales; **`caret`** para el entrenamiento y validación cruzada de modelos (incluyendo MLP y XGBoost), **`kernlab`** para disponer de métodos kernel/SVM integrados en caret; **`nnet`** para construir redes neuronales MLP sencillas; **`NeuralNetTools`** para visualizar y diagnosticar redes neuronales; y **`xgboost`** para ajustar modelos no lineales de boosting basado en árboles.
```r
# Librerías
library(fpp2)
library(lmtest)
library(tseries) 
library(TSA)
library(readxl)
library(MLTools)
library(imputeTS)
library(NeuralSens)
library(caret)
library(kernlab)
library(nnet)
library(NeuralNetTools)
library(xgboost)
```
#### 2. Directorio
> Igual que en semanas anteriores: ajusta automáticamente al directorio del script activo.
```r
# Setear el Directorio 
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
```

### II. Feature Engineering with Transfer Function
#### 1. Carga y Preprocesamiento de Datos 
> En este primer bloque preparamos la serie diaria de demanda para poder ajustarle un modelo de función de transferencia.  
> Leemos el fichero de **entrenamiento con huecos** (`DAILY_DEMAND_TR_NA.xlsx`) y lo convertimos en un objeto `ts` con frecuencia semanal (`freq=7`), lo que permite trabajar cómodamente con patrones de día de la semana.  
> A continuación inspeccionamos la **distribución temporal de los valores faltantes** en las tres variables principales (demanda, calendario laboral `WD`, temperatura `TEMP`) y probamos dos estrategias de **imputación** usando `imputeTS`:
> 	- `na_seasplit()`, que reconstruye los NAs respetando la estacionalidad,
> 	- `na_kalman()` con modelo `auto.arima`, que usa un filtro de Kalman.  
> Para el resto del ejercicio nos quedamos con la versión imputada estacional (`imp_seas`).  
> Finalmente definimos la serie objetivo $y$ (demanda) y la matriz de regresores $x$ (WD y TEMP), y realizamos un **re-escalado** simple (demanda/100) para evitar problemas numéricos y facilitar la estimación de los modelos TF posteriores.
```r
# 1. Lectura de Datos con NAs
fdata <- read_excel("DAILY_DEMAND_TR_NA.xlsx")

# 2. Convertir Data Frame a Objeto ts con Frecuencia Semanal
freq <- 7
fdata_ts <- ts(fdata, frequency = freq)
autoplot(fdata_ts, facets = TRUE)

# 3. Visualizar Distribución de Valores Faltantes por Variable
ggplot_na_distribution(fdata_ts[, 2])
ggplot_na_distribution(fdata_ts[, 3])
ggplot_na_distribution(fdata_ts[, 4])

# 4. Imputación Estacional de Valores Faltantes (na_seasplit)
imp_seas <- na_seasplit(fdata_ts)
ggplot_na_imputations(fdata_ts[, 4], imp_seas[, 4])

# 5. Imputación mediante Filtro de Kalman con Modelo auto.arima
imp_kalman <- na_kalman(fdata_ts, model = "auto.arima")
ggplot_na_imputations(fdata_ts[, 4], imp_kalman[, 4])

# 6. Seleccionar Serie Imputada Estacional como Base de Trabajo
fdata_ts <- imp_seas

# 7. Definir Serie de Salida y Matriz de Inputs (WD y TEMP)
y <- fdata_ts[, 2]
x <- fdata_ts[, c(3, 4)]
autoplot(cbind(y, x), facets = TRUE)

# 8. Escalar Series para Estabilizar Magnitudes
y.tr <- y / 100
x.tr <- x / 1
autoplot(cbind(y.tr, x.tr), facets = TRUE)
```
#### 2. TF Lineal con WD y TEMP (Sin Feature Engineering)
###### 2.1. Identificación y Ajuste Inicial (TF con 2 Inputs)
> En este bloque construimos un **primer modelo de función de transferencia** con los dos regresores originales: `WD` (calendario laboral) y `TEMP`.  
> Ajustamos un ARIMA básico **sin diferenciación** y con un **orden de numerador grande** en las funciones de transferencia (`s=9` para ambos inputs). Este modelo preliminar no se usa para interpretar los coeficientes, sino para inspeccionar el **error de regresión** mediante `TF.RegressionError.plot()`.  
> Si ese error no es estacionario, significa que todavía hace falta aplicar **diferenciación regular** a la serie de salida, y por tanto **los coeficientes de las variables explicativas no son interpretables** en este primer intento. A partir de este diagnóstico decidiremos el orden de diferenciación en el siguiente paso.
```r
# 1. Estimación del Modelo TF Preliminar sin Diferenciación y con s Grande
TF.fit <- arima(y.tr,
                xtransf = x.tr,
                order = c(1, 0, 0),
                seasonal = list(order = c(1, 0, 0), period = freq),
                transfer = list(c(0, 9), c(0, 9)),
                method = "ML")

# 2. Diagnóstico de los Residuos del Modelo Preliminar
TF.RegressionError.plot(y.tr, x.tr, TF.fit, lag.max = 50)
# Se Necesita Diferenciación Regular y no se Pueden Interpretar los Coeficientes de las Variables Explicativas
```
###### 2.2. Añadir Diferenciación Regular
> Aquí repetimos el ajuste del modelo de función de transferencia, pero ahora incorporando **diferenciación regular** en la parte ARIMA de la serie (`order = c(1, 1, 0)`).  
> Estimamos de nuevo el modelo con numeradores largos (`s = 9` para ambos inputs) y analizamos:
> 	- El **resumen del modelo** y la **significancia** de los coeficientes (`summary`, `coeftest`).
> 	- El **diagnóstico de residuos** con `CheckResiduals.ICAI()` y el **error de regresión** con `TF.RegressionError.plot()`.  
> En este caso, el error de regresión resulta **estacionario**, por lo que ya podemos interpretar la parte de regresión y seguir refinando la estructura ARIMA (por ejemplo, planteando un ARMA(2,1) en la parte regular y AR(1) estacional).  
> Finalmente, usamos `TF.Identification.plot()` para inspeccionar los coeficientes asociados a cada regresor (`WD`, `TEMP`) y proponer valores iniciales para (b, r, s), que usaremos en el siguiente ajuste.
```r
# 1. Estimación del Modelo TF con Diferenciación Regular y s Grande
TF.fit <- arima(y.tr,
                xtransf = x.tr,
                order = c(1, 1, 0),
                seasonal = list(order = c(1, 0, 0), period = freq),
                transfer = list(c(0, 9), c(0, 9)),
                method = "ML")

# 2. Resumen General, Significancia de Coeficientes, y Diagnóstico de Residuos
summary(TF.fit)          
coeftest(TF.fit)         
CheckResiduals.ICAI(TF.fit, lag=50)

# 3. Diagnóstico de los Residuos del Modelo Diferenciado
TF.RegressionError.plot(y.tr, x.tr, TF.fit, lag.max = 50)
# NOTE: Si el error de esta regresión no es estacionario en varianza, hay que aplicar Box-Cox a las series de entrada y de salida.
# El Error de Regresión es Estacionario, por lo que Podemos Continuar
# Probar AR(1)7 para el Componente Estacional y ARMA(2,1) para el Componente Regular?

# 4. Identificación visual de los parámetros TF
TF.Identification.plot(x.tr, TF.fit)
b_w <- 0; r_w <- 0; s_w <- 0  # WD
b_t <- 0; r_t <- 0; s_t <- 1  # TEMP
```
###### 2.3 Modelo TF con Estructura Seleccionada
> En este paso construimos un **modelo de función de transferencia más parsimonioso**, utilizando los valores de (r, s) obtenidos en la fase de identificación para cada regresor:
> 	- $(r_w, s_w)$ para la variable de calendario laboral `WD`.
> 	- $(r_t, s_t)$ para la temperatura `TEMP`.  
> Mantenemos una estructura ARIMA más rica en la parte de ruido, por ejemplo (2,1,1) con componente estacional semanal, y dejamos fijado b = 0 (sin retardo explícito), tal y como sugería `TF.Identification.plot()`.  
> A partir de este modelo revisamos el **summary**, la **significancia de los coeficientes**, el **diagnóstico de residuos** y, con `PlotModelDiagnosis()`, comparamos **valores reales vs ajustados** para comprobar que el TF lineal con `WD` y `TEMP` captura razonablemente bien la dinámica antes de introducir la no linealidad vía feature engineering.
```r
# 1. Ajustar Modelo TF con Órdenes (b,r,s) Seleccionados y ARIMA Inicial
xlag_w <- Lag(x.tr[,1], b_w)
xlag_w[is.na(xlag_w)]=0
xlag_t <- Lag(x.tr[,2], b_t)
xlag_t[is.na(xlag_t)]=0
xlag <- cbind(xlag_w, xlag_t)
TF.fit <- arima(y.tr,
                xtransf = xlag,
                order = c(2, 1, 1),
                seasonal = list(order = c(1, 0, 0), period = freq),
                transfer = list(c(r_w, s_w), c(r_t, s_t)),
                method = "ML")

# 2. Resumen General, Significancia de Coeficientes, y Diagnóstico de Residuos
summary(TF.fit)      
coeftest(TF.fit)        
CheckResiduals.ICAI(TF.fit, lag = 50)

# 3. Diagnóstico Gráfico del Modelo (Ajuste vs Real)
PlotModelDiagnosis(x.tr, y.tr, fitted(TF.fit), together = TRUE)
```
#### 3. Feature Engineering sobre la Temperatura (tcold, thot)
> En este bloque introducimos **no linealidad explícita** en el modelo mediante _feature engineering_.  
> Primero comprobamos gráficamente que la relación entre **temperatura (TEMP)** y **demanda eléctrica (DEM)** no es lineal: la demanda baja cuando hace frío extremo, sube en temperaturas templadas y vuelve a bajar cuando hace demasiado calor.  
> Para capturar esta curva en forma de “U invertida”, transformamos TEMP en dos nuevas variables:
> 	- **tcold** → mide cuánto cae la temperatura por debajo de un umbral frío (17º).
> 	- **thot** → mide cuánto supera la temperatura un umbral cálido (22º).  
> Estas variables permiten modelar la relación de manera **lineal por tramos**, lo que convierte a nuestro TF en un modelo **lineal en parámetros pero no lineal en los inputs**.  
> Después reconstruimos las series temporales con estas nuevas variables y las escalamos para ajustarlas correctamente en el modelo TF.
```r
# 1. Analizar Relación No Lineal entre Temperatura y Demanda
ggplot(fdata) + geom_point(aes(x = TEMP, y = DEM))

# 2. Crear Variables de Temperatura Fría y Caliente (Relación No Lineal por Tramos)
fdata$tcold <- sapply(as.numeric(fdata_ts[, 4]), min, 17)
fdata$thot  <- sapply(as.numeric(fdata_ts[, 4]), max, 22)

# 3. Crear Nuevas Series Temporales con WD, tcold y thot
y <- ts(fdata[, 2], frequency = freq)
x <- ts(fdata[, c(3, 5, 6)], frequency = freq)
autoplot(cbind(y, x), facets = TRUE)

# 4. Escalar Nuevas Series para el Modelo TF
y.tr <- y / 100
x.tr <- x / 1
autoplot(cbind(y.tr, x.tr), facets = TRUE)
```
#### 4. TF con WD, tcold y thot (Identificación y Modelo Final)
###### 4.1. Identificación y Ajuste Inicial con 3 Inputs
> En este paso repetimos el procedimiento inicial de identificación, pero ahora con **tres regresores**:
> 	- `WD`
> 	- `tcold`  
> 	- `thot`
> Ajustamos un **modelo preliminar TF sin diferenciación** y con **orden del numerador grande (s=9)** para cada input.  
> Igual que antes, este modelo _no se interpreta_, sino que sirve para diagnosticar si la combinación de salida e inputs es estacionaria.
> Tras aplicar `TF.RegressionError.plot()`, observaremos que el **error de regresión no es estacionario**, lo que indica que la serie debe ser diferenciada antes de estimar un modelo interpretable. Es exactamente el mismo patrón que con los dos inputs, pero ahora en presencia de un input transformado de forma no lineal.
```r
# 1. Estimación del Modelo TF Preliminar sin Diferenciación y con s Grande
TF.fit <- arima(y.tr,
                xtransf = x.tr,
                order = c(1, 0, 0),
                seasonal = list(order = c(1, 0, 0), period = freq),
                transfer = list(c(0, 9), c(0, 9), c(0, 9)),
                method = "ML")

# 2. Resumen General, Significancia de Coeficientes, y Diagnóstico de Residuos
summary(TF.fit)          
coeftest(TF.fit)         
CheckResiduals.ICAI(TF.fit, lag=50)

# 3. Diagnóstico de los Residuos del Modelo Preliminar
TF.RegressionError.plot(y.tr, x.tr, TF.fit, lag.max = 50)
# Se Necesita Diferenciación Regular y no se Pueden Interpretar los Coeficientes de las Variables Explicativas
```
###### 4.2. Añadir Diferenciación Regular
> Igual que hicimos con dos inputs, ahora repetimos el ajuste TF con los **tres regresores (WD, tcold, thot)** pero incorporando **diferenciación regular** en la parte ARIMA (`d = 1`).  
> Volvemos a usar numeradores largos (`s = 9`) para cada input, revisamos el **resumen del modelo**, la **significancia de los coeficientes** y el **diagnóstico de residuos**.  
> El gráfico de `TF.RegressionError.plot()` muestra que el **error de regresión es ya estacionario**, de modo que podemos interpretar la parte de regresión y afinar la estructura ARIMA (por ejemplo, probar $AR(1)_7$ estacional y $AR(2)$ en la parte regular).  
> Finalmente, con `TF.Identification.plot()` analizamos la **respuesta asociada a cada input** y fijamos valores iniciales para (b, r, s): sin retardo para todos (b = 0), función de transferencia trivial para `WD` y respuestas de orden 1 para `tcold` y `thot`. Estos serán los parámetros de partida en el modelo TF más parsimonioso que ajustaremos a continuación.
```r
# 1. Estimación del Modelo TF con Diferenciación Regular y s Grande
TF.fit <- arima(y.tr,
                xtransf = x.tr,
                order = c(1, 1, 0),
                seasonal = list(order = c(1, 0, 0), period = freq),
                transfer = list(c(0, 9), c(0, 9), c(0, 9)),
                method = "ML")

# 2. Resumen General, Significancia de Coeficientes, y Diagnóstico de Residuos
summary(TF.fit)         
coeftest(TF.fit)   
CheckResiduals.ICAI(TF.fit, lag=50)     

# 3. Diagnóstico de los Residuos del Modelo Diferenciado
TF.RegressionError.plot(y.tr, x.tr, TF.fit, lag.max = 50)
# NOTE: Si el error de esta regresión no es estacionario en varianza, hay que aplicar Box-Cox a las series de entrada y de salida.
# El Error de Regresión es Estacionario, por lo que Podemos Continuar
# Probar AR(1)7 para el Componente Estacional y ARMA(2) para el Componente Regular?

# 4. Identificar Coeficientes de Transfer Function para Cada Input
TF.Identification.plot(x.tr, TF.fit)
b_w  <- 0; r_w  <- 0; s_w  <- 0  # WD
b_tc <- 0; r_tc <- 1; s_tc <- 0  # tcold
b_th <- 0; r_th <- 1; s_th <- 0  # thot
```
###### 4.3. TF con Estructura Seleccionada
> En este paso construimos el **modelo de función de transferencia definitivo** utilizando los valores identificados de (b, r, s) para cada una de las tres variables explicativas:
> 	- **WD** → respuesta inmediata y simple (r=0, s=0).
> 	- **tcold** → relación dinámica de orden 1 (r=1).
> 	- **thot** → relación dinámica también de orden 1 (r=1).
> Primero aplicamos los retardos b (aunque sean igual a 0, lo hacemos de forma explícita por claridad), construimos la matriz `xlag`, y luego ajustamos el modelo ARIMA con la parte de ruido estructurada como $(2,1,0)(1,0,0)_7$​.  
> Finalmente revisamos:
> 	- **Significancia estadística de los coeficientes**
> 	- **Diagnóstico de residuos** mediante `CheckResiduals.ICAI()`
> Este modelo es ya la **versión parsimoniosa**, interpretable y adecuada para forecasting antes de la exploración de estructuras ARMA alternativas.
```r
# 1. Ajustar Modelo TF con Órdenes Seleccionados y ARIMA Inicial
xlag_w <- Lag(x.tr[,1], b_w)
xlag_w[is.na(xlag_w)]=0
xlag_tc <- Lag(x.tr[,3], b_tc)
xlag_tc[is.na(xlag_tc)]=0
xlag_th <- Lag(x.tr[,4], b_th)
xlag_th[is.na(xlag_th)]=0
xlag <- cbind(xlag_w, xlag_tc, xlag_th)
TF.fit <- arima(y.tr,
                xtransf = xlag,
                order = c(2, 1, 0),
                seasonal = list(order = c(1, 0, 0), period = freq),
                transfer = list(c(r_w, s_w), c(r_tc, s_tc), c(r_th, s_th)),
                method = "ML")

# 2. Resumen General, Significancia de Coeficientes, y Diagnóstico de Residuos
summary(TF.fit)
coeftest(TF.fit)
CheckResiduals.ICAI(TF.fit, lag = 50)
```
###### 4.4. Probar Alternativa MA en Lugar de AR
> En este bloque exploramos una **alternativa para la parte regular del ARIMA**, sustituyendo los términos autorregresivos por términos de media móvil.  
> En lugar del modelo (2,1,0) anterior probamos ahora un **MA(2) diferenciado**: $(0,1,2)(1,0,0)_7,$ manteniendo la **misma estructura de función de transferencia** para `WD`, `tcold` y `thot`.  
> De nuevo recalculamos los lags de las variables explicativas (según $b_w, b_{tc}, b_{th}$), ajustamos el modelo y revisamos:
> 	- El **resumen de parámetros** y su significancia.
> 	- El **diagnóstico de residuos**: si los residuos no se comportan como ruido blanco, es indicio de que la estructura ARMA todavía no es adecuada.  
> En este caso se observan **correlaciones residuales en lags concretos (4, 5 y 14)**, lo que sugiere que debemos **incrementar los órdenes** del modelo ARMA en pasos posteriores.
```r
# 1. Probar Modelo (0,1,2)(1,0,0)[7] con la Misma Estructura TF
xlag_w <- Lag(x.tr[,1], b_w)
xlag_w[is.na(xlag_w)]=0
xlag_tc <- Lag(x.tr[,3], b_tc)
xlag_tc[is.na(xlag_tc)]=0
xlag_th <- Lag(x.tr[,4], b_th)
xlag_th[is.na(xlag_th)]=0
xlag <- cbind(xlag_w, xlag_tc, xlag_th)
TF.fit <- arima(y.tr,
                xtransf = xlag,
                order = c(0, 1, 2),
                seasonal = list(order = c(1, 0, 0), period = freq),
                transfer = list(c(r_w, s_w), c(r_tc, s_tc), c(r_th, s_th)),
                method = "ML")

# 2. Resumen General, Significancia de Coeficientes, y Diagnóstico de Residuos
summary(TF.fit)
coeftest(TF.fit)
CheckResiduals.ICAI(TF.fit, lag = 50)
# TRADUCIR: If residuals are not white noise, change order of ARMA
# TRADUCIR: Remaning correlations in lags 4 and 5 and 14. Increase orders
```
###### 4.5. Incrementar Órdenes para Mejorar Correlaciones
> Como en el paso anterior aún quedaban **correlaciones residuales**, aquí probamos un modelo ARIMA más flexible tanto en la parte regular como en la estacional.  
> Pasamos a un modelo $(0,1,5)(2,0,0)_7:$​
> 	- Aumentamos el orden MA regular a 5.
> De nuevo recalculamos los lags de `WD`, `tcold` y `thot`, ajustamos el modelo TF con la misma estructura (r,s) para las funciones de transferencia y evaluamos:
> 	- Si las **correlaciones residuales** se han reducido.
> 	- Si los **coeficientes MA** son significativos.
> En este caso, aunque las correlaciones quedan bien modeladas, **muchos términos MA no son significativos**, lo que sugiere que la estructura es demasiado compleja y conviene probar una **alternativa basada en términos AR** en lugar de tantos MA.
```r
# 1. Probar Modelo (0,1,5)(2,0,0)[7]
xlag_w <- Lag(x.tr[,1], b_w)
xlag_w[is.na(xlag_w)]=0
xlag_tc <- Lag(x.tr[,3], b_tc)
xlag_tc[is.na(xlag_tc)]=0
xlag_th <- Lag(x.tr[,4], b_th)
xlag_th[is.na(xlag_th)]=0
xlag <- cbind(xlag_w, xlag_tc, xlag_th)
TF.fit <- arima(y.tr,
                xtransf = xlag,
                order = c(0, 1, 5),
                seasonal = list(order = c(2, 0, 0), period = freq),
                transfer = list(c(r_w, s_w), c(r_tc, s_tc), c(r_th, s_th)),
                method = "ML")

# 2. Resumen General, Significancia de Coeficientes, y Diagnóstico de Residuos
summary(TF.fit)
coeftest(TF.fit)
CheckResiduals.ICAI(TF.fit, lag = 50)
# Si los Residuos no son Ruido Blanco, hay que Cambiar el Orden del ARMA
# Las Correlaciones se Modelan, pero Muchos Términos MA no son Significativos → Probar Alternativa AR
```
###### 4.6. Alternativa AR para Parte Regular
> Tras ver que el modelo con muchos términos MA no era parsimonioso, aquí probamos una **alternativa basada en términos AR** en la parte regular: $(5,1,0)(2,0,0)_7$​  
> Mantenemos la misma estructura de función de transferencia para `WD`, `tcold` y `thot`, recalculamos los lags y ajustamos el modelo.  
> El resultado es bastante satisfactorio:
> 	- Todos los **coeficientes son significativos**,
> 	- Las **correlaciones residuales son pequeñas**, lo que indica que el ruido está bien modelado.
> Como comprobación adicional, analizamos las **correlaciones cruzadas entre los residuos y cada una de las variables explicativas**. En este diagnóstico todavía se aprecia cierta correlación con la primera variable (`X1`, correspondiente a `WD`), lo que sugiere ajustar ligeramente la estructura de su función de transferencia en el siguiente paso.
```r
# 1. Probar Modelo (5,1,0)(2,0,0)[7]
xlag_w <- Lag(x.tr[,1], b_w)
xlag_w[is.na(xlag_w)]=0
xlag_tc <- Lag(x.tr[,3], b_tc)
xlag_tc[is.na(xlag_tc)]=0
xlag_th <- Lag(x.tr[,4], b_th)
xlag_th[is.na(xlag_th)]=0
xlag <- cbind(xlag_w, xlag_tc, xlag_th)
TF.fit <- arima(y.tr,
                xtransf = xlag,
                order = c(5, 1, 0),
                seasonal = list(order = c(2, 0, 0), period = freq),
                transfer = list(c(r_w, s_w), c(r_tc, s_tc), c(r_th, s_th)),
                method = "ML")

# 2. Resumen General, Significancia de Coeficientes, y Diagnóstico de Residuos
summary(TF.fit)
coeftest(TF.fit)
CheckResiduals.ICAI(TF.fit, lag = 50)
# Todos los Coeficientes son Significativos → Bien
# Todas las Correlaciones son Pequeñas → Bien

# 3. Comprobar Correlación Cruzada Residuos - Variables Explicativas
res <- residuals(TF.fit)
res[is.na(res)] <- 0
ccf(y = res, x = x.tr[, 1])
ccf(y = res, x = x.tr[, 2])
ccf(y = res, x = x.tr[, 3])

# X1 Parece Correlacionada con los Residuos → Ajustar la Función de Transferencia
```
###### 4.7. Ajustar TF para X1 y Modelo Final
> En este último paso afinamos la función de transferencia asociada a X1 (el calendario laboral `WD`), ya que en el diagnóstico anterior todavía aparecía cierta correlación entre esta variable y los residuos.  
> Manteniendo la estructura ARIMA $(5,1,0)(2,0,0)_7$ y los términos de `tcold` y `thot`, reajustamos la TF de `WD` (refinando $(r_w, s_w)$) y volvemos a estimar el modelo completo.  
> A continuación:
> 	- Comprobamos que los **coeficientes del modelo son (en su mayoría) significativos** y que las **correlaciones residuales son pequeñas**,
> 	- Revisamos la **correlación cruzada residuos–inputs**, verificando que la relación con `X1` mejora claramente,
> 	- Comparamos la **serie real frente a la ajustada**, calculamos la **accuracy** en entrenamiento y usamos `PlotModelDiagnosis()` para evaluar de forma conjunta ajuste y residuos.
> Este será el **modelo TF final** con feature engineering sobre la temperatura, listo para usar en la fase de forecasting.
```r
# 1. Probar (5,1,0)(2,0,0)[7] Modificando TF de X1
xlag_w <- Lag(x.tr[,1], b_w)
xlag_w[is.na(xlag_w)]=0
xlag_tc <- Lag(x.tr[,3], b_tc)
xlag_tc[is.na(xlag_tc)]=0
xlag_th <- Lag(x.tr[,4], b_th)
xlag_th[is.na(xlag_th)]=0
xlag <- cbind(xlag_w, xlag_tc, xlag_th)
TF.fit <- arima(y.tr,
                xtransf = xlag,
                order = c(5, 1, 0),
                seasonal = list(order = c(2, 0, 0), period = freq),
                transfer = list(c(r_w, s_w), c(r_tc, s_tc), c(r_th, s_th)),
                method = "ML")

# 2. Resumen General, Significancia de Coeficientes, y Diagnóstico de Residuos
summary(TF.fit)
coeftest(TF.fit)
CheckResiduals.ICAI(TF.fit, lag = 50)
# Todos los Coeficientes Parecen Significativos (Revisar Individualmente)
# Todas las Correlaciones son Pequeñas → Bien

# 3. Última Comprobación de Correlación Cruzada Residuos - Inputs
res <- residuals(TF.fit)
res[is.na(res)] <- 0
ccf(y = res, x = x.tr[, 1])  # --> much better
ccf(y = res, x = x.tr[, 2])
ccf(y = res, x = x.tr[, 3])

# 4. Comparar Serie Real y Valores Ajustados
autoplot(y.tr, series = "Real") +
  forecast::autolayer(fitted(TF.fit), series = "Fitted")

# 5. Medir Errores de Entrenamiento del Modelo
accuracy(fitted(TF.fit), y.tr)

# 6. Diagnóstico Global del Modelo (Ajuste y Residuos)
PlotModelDiagnosis(x.tr, y.tr, fitted(TF.fit), together = TRUE)
```
#### 5. Forecast para Nuevos Datos (h = 7)
> En este último bloque utilizamos el **modelo TF final** para generar un pronóstico de **7 días** sobre un conjunto de validación.  
> Primero cargamos el fichero `DAILY_DEMAND_TV.xlsx`, que contiene los nuevos valores de `WD` y `TEMP` para el periodo a predecir. A estos datos les aplicamos el mismo **feature engineering** que en entrenamiento, creando de nuevo las variables `tcold` y `thot` a partir de la temperatura.  
> Después construimos un objeto `ts` con las tres entradas (`WD`, `tcold`, `thot`) y llamamos a `TF.forecast()`, proporcionando:
> 	- `y.old` y `x.old`: series históricas usadas en el ajuste,
> 	- `x.new`: las nuevas trayectorias de los regresores en validación,
> 	- `h = 7`: horizonte de predicción.  
> El resultado `val.forecast_h7` se encuentra en la escala reescalada (demanda/100), por lo que finalmente **re-escalamos** multiplicando por 100 para recuperar la escala original de la demanda.
```r
# 1. Leer Datos de Validación con Nuevos Valores de WD y TEMP
x.tv <- read_excel("DAILY_DEMAND_TV.xlsx")

# 2. Crear Variables de Temperatura Fría y Caliente en Validación
x.tv$tcold <- sapply(x.tv$TEMP, min, 17)
x.tv$thot  <- sapply(x.tv$TEMP, max, 22)

# 3. Convertir a Objeto ts con las Tres Variables de Entrada
x.tv <- ts(x.tv[, c(2, 4, 5)])

# 4. Obtener Pronóstico para Horizonte h = 7 con el Modelo TF Entrenado
val.forecast_h7 <- TF.forecast(y.old  = y.tr,  # Past values of the series
                               x.old  = x.tr,  # Past values of the variables
                               x.new  = x.tv,  # New values of the variables
                               model  = TF.fit, # Fitted transfer function model
                               h      = 7)      # Forecast horizon

# 5. Reescalar Pronósticos a la Escala Original
val.forecast_h7 * 100
```

### III. MLP for Non Lineal Forecasting
#### 1. Carga y Preprocesamiento de Datos 
> En este bloque preparamos el **dataset de regresión** que va a alimentar a la red neuronal MLP.  
> Primero leemos el fichero de entrenamiento `DAILY_DEMAND_TR.xlsx` y extraemos las tres variables base:
> 	- **DEM**: demanda (output a predecir),
> 	- **WD**: indicador de día laborable / fin de semana,
> 	- **TEMP**: temperatura.
> Para que la red pueda capturar la **dinámica temporal** y se parezca a un modelo **NARX**, añadimos **retardos (lags)** de cada variable usando `Lag()` de `Hmisc` (más cómodo que `stats::lag`):
> 	- `WD_lag1`, `WD_lag7` → efecto del calendario de ayer y del mismo día de la semana anterior.
> 	- `TEMP_lag1`, `TEMP_lag7` → temperatura reciente y patrón semanal.
> 	- `DEM_lag1`, `DEM_lag7` → inercia de la propia demanda (autoregresión no lineal).
> Estos lags introducen memoria en el modelo y convierten la red neuronal en algo muy parecido a un **modelo NARX no lineal**.  
> Como consecuencia de los lags, las primeras filas contienen `NA`, así que creamos la versión final de entrenamiento `fdata.Reg.tr` eliminando esos registros con `na.omit()`.
```r
# 1. Lectura de Datos de Entrenamiento
fdata <- readxl::read_excel("DAILY_DEMAND_TR.xlsx")
fdata <- as.data.frame(fdata)

# 2. Inicializar Dataset de Regresión con Output e Inputs Contemporáneos
fdata.Reg <- fdata[, c(2, 3, 4)]  # (DEM, WD, TEMP)

# 3. Incluir Variables Rezagadas con Lag de Hmisc (Más Limpio que stats::lag)
fdata.Reg$WD_lag1   <- Lag(fdata$WD,   1)
fdata.Reg$WD_lag7   <- Lag(fdata$WD,   7)
fdata.Reg$TEMP_lag1 <- Lag(fdata$TEMP, 1)
fdata.Reg$TEMP_lag7 <- Lag(fdata$TEMP, 7)
fdata.Reg$DEM_lag1  <- Lag(fdata$DEM,  1)
fdata.Reg$DEM_lag7  <- Lag(fdata$DEM,  7)

# 4. Comprobar Cabecera del Dataset con Lags (Aparecen NAs al Principio)
head(fdata.Reg)

# 5. Crear Versión de Entrenamiento Eliminando Registros con NAs
fdata.Reg.tr <- fdata.Reg
fdata.Reg.tr <- na.omit(fdata.Reg.tr)
```
#### 2. Configuración de la Validación Cruzada
> Antes de entrenar la red neuronal definimos cómo vamos a medir su capacidad de generalización. Usamos `caret::trainControl()` para crear un esquema de **validación cruzada K-fold con K=10**: el conjunto de datos se divide en 10 partes, se entrena en 9 y se evalúa en la restante, repitiendo el proceso rotando los folds.  
> Con esto obtenemos una estimación más estable del error fuera de muestra y evitamos quedarnos solo con el error de entrenamiento (que suele ser demasiado optimista, sobre todo en modelos flexibles como las redes neuronales).  
> Además, activamos `savePredictions = TRUE` para guardar las predicciones de cada fold y usamos `defaultSummary` como función de resumen, que calcula métricas estándar de regresión (RMSE, MAE, R²) para comparar configuraciones del MLP.
```r
# Definir Esquema de Validación Cruzada K-Fold (K = 10)
ctrl_tune <- trainControl(
  method = "cv",             # Validación Cruzada
  number = 10,               # Número de Folds
  summaryFunction = defaultSummary,  # Métrica de Rendimiento en Test
  savePredictions = TRUE     # Guardar Predicciones de los Folds
)
```
#### 3. Red Neuronal MLP Completa y Evaluación en Entrenamiento
> En este bloque entrenamos una **red neuronal MLP “grande”** usando **todas las variables disponibles** (DEM lags, WD, TEMP y sus lags).  
> Usamos `caret::train()` con el método `"nnet"` (red feedforward clásica) en modo **regresión** (`linout = TRUE`), combinando:
> 	- **Validación cruzada 10-fold** (`trControl = ctrl_tune`) para estimar el error de generalización.
> 	- Un **grid de hiperparámetros**:
> 		- `size`: número de neuronas en la capa oculta (10, 15, 20).
> 		- `decay`: regularización L2 sobre los pesos (`10^{-3}, 10^{-2}, 10^{-1}, 10^0`).
> 	- **Preprocesado interno** de las entradas con centrado y escalado (`preProcess = c("center","scale")`), algo esencial para que el MLP entrene de forma estable.
> Con `mlp.fit` inspeccionamos el rendimiento por combinación de hiperparámetros y, con `ggplot(mlp.fit)`, vemos cómo cambia el RMSE en función de `size` y `decay`.  
> Luego visualizamos la **arquitectura de la red** (`plotnet()`) y su **análisis de sensibilidad** (`SensAnalysisMLP()`), que indica qué inputs influyen más en la salida.
> A continuación calculamos las **predicciones en el conjunto de entrenamiento**, usamos `PlotModelDiagnosis()` para analizar ajuste y residuos, medimos la precisión con `accuracy()` y, por último, comparamos visualmente la **serie real de DEM** frente a la predicha por la red (línea roja), para ver rápidamente si el MLP está capturando la dinámica principal o si hay sobre/infraajuste.
```r
# 1. Ajustar Red Neuronal MLP con Todas las Variables (DEM ~ .)
set.seed(150)  # Fijar Semilla para Reproducibilidad
mlp.fit <- train(
  form = DEM ~ .,             # Fórmula con Todas las Variables Explicativas
  data = fdata.Reg.tr,        # Dataset de Entrenamiento sin NAs
  method = "nnet",            # Modelo de Red Neuronal Feedforward
  linout = TRUE,              # Salida Lineal (Regresión)
  # tuneGrid = data.frame(size = 5, decay = 0),
  tuneGrid = expand.grid(
    size  = seq(10, 20, length.out = 3),  # Número de Neuronas Ocultas
    decay = 10^(c(-3:0))                  # Parámetro de Regularización (Weight Decay)
  ),
  maxit = 200,                        # Iteraciones Máximas de Entrenamiento
  preProcess = c("center", "scale"),  # Estandarización de Inputs
  trControl = ctrl_tune,              # Esquema de Validación Cruzada
  metric = "RMSE"                     # Métrica a Minimizar
)

# 2. Inspeccionar Resultados de la Validación Cruzada
mlp.fit
ggplot(mlp.fit) + scale_x_log10()

# 3. Visualizar la Arquitectura de la Red Ajustada
plotnet(mlp.fit$finalModel)     # Diagrama de la Red
SensAnalysisMLP(mlp.fit)        # Análisis de Sensibilidad de los Inputs

# 4. Obtener Predicciones en el Conjunto de Entrenamiento
mlp_pred <- predict(mlp.fit, newdata = fdata.Reg.tr)

# 5. Diagnóstico del Modelo: Ajuste vs Real y Residuos
PlotModelDiagnosis(
  fdata.Reg.tr[, -1],     # Variables Explicativas
  fdata.Reg.tr[, 1],      # Output Real DEM
  mlp_pred,               # Predicción del MLP
  together = TRUE
)

# 6. Medir Errores de Entrenamiento (Precision de la Red)
accuracy(fdata.Reg.tr[, 1], mlp_pred)

# 7. Visualización de la Serie Real Frente a la Predicha
plot(fdata.Reg.tr[, 1], type = "l")
lines(mlp_pred, col = "red")
```
#### 4. Red Neuronal Podada (Pruned MLP) y Análisis de Sensibilidad
> Después de entrenar una red con **todas** las variables, el siguiente paso natural es **simplificar el modelo** para ganar interpretabilidad y reducir riesgo de sobreajuste.  
> Aquí entrenamos una **red neuronal podada** usando solo un **subconjunto de inputs** que tienen sentido desde el punto de vista del dominio:
> 	- `WD` → información de día laborable / fin de semana.
> 	- `TEMP` → efecto directo de la temperatura actual.
> 	- `DEM_lag1` → inercia de la demanda (ayer).
> 	- `WD_lag1` → efecto del patrón laboral del día anterior.
> Mantenemos el mismo esquema de **validación cruzada**, el mismo grid de hiperparámetros (`size`, `decay`) y el mismo preprocesado (centrar y escalar).  
> Con `mlp.fit2` y `ggplot(mlp.fit2)` revisamos el comportamiento del modelo reducido, y con `plotnet()` y `SensAnalysisMLP()` analizamos:
> 	- La **estructura de la red resultante**.
> 	- Qué variables son **más influyentes** en la predicción de DEM.
> Esta red podada suele ser más fácil de interpretar y, si el rendimiento es similar al modelo completo, es preferible como modelo final.
```r
# 1. Ajustar Red Neuronal MLP con Subconjunto de Variables (Modelo Podado)
set.seed(150)  # Fijar Semilla para Reproducibilidad
mlp.fit2 <- train(
  form = DEM ~ WD + DEM_lag1 + WD_lag1 + TEMP,  # Selección Manual de Inputs
  data = fdata.Reg.tr,
  method = "nnet",
  linout = TRUE,
  # tuneGrid = data.frame(size = 5, decay = 0),
  tuneGrid = expand.grid(
    size  = seq(10, 20, length.out = 3),
    decay = 10^(c(-3:0))
  ),
  maxit = 200,
  preProcess = c("center", "scale"),
  trControl = ctrl_tune,
  metric = "RMSE"
)

# 2. Inspeccionar Resultados de la Red Podada
mlp.fit2
ggplot(mlp.fit2) + scale_x_log10()

# 3. Visualizar Arquitectura y Sensibilidad de la Red Podada
plotnet(mlp.fit2$finalModel)  # Estructura de la Red
SensAnalysisMLP(mlp.fit2)     # Análisis de Sensibilidad de Inputs
```
#### 5. Forecast Multi-Step con MLP y Lags Recalculados
> Aquí utilizamos el MLP entrenado para hacer un **forecast multi-step (h = 7)**, respetando la estructura con lags que usamos en entrenamiento (tipo **NARX**).  
> Primero leemos el fichero de validación `DAILY_DEMAND_TV.xlsx` con los nuevos valores de `WD` y `TEMP`, y construimos un data frame `fdata.Reg.new` donde dejamos `DEM` como **desconocido (NA)** para esos 7 días. Después concatenamos los **datos históricos** con estos nuevos registros en `fdata.join` y volvemos a crear **todas las variables rezagadas** (`WD_lag*`, `TEMP_lag*`, `DEM_lag*`) sobre el conjunto ampliado.
> A partir de ahí, el forecast se hace de forma **iterativa**:
> 	- En cada paso i, predecimos `DEM[i]` con el modelo `mlp.fit`.
> 	- Esa predicción se escribe en `fdata.join$DEM[i]` y se usan las funciones `Lag()` para **recalcular los lags de DEM**, de modo que los siguientes pasos `DEM_lag1` y `DEM_lag7` ya incorporan las predicciones anteriores.
> Este esquema emula un **NARX iterativo**: cada predicción depende de predicciones anteriores, no solo de datos pasados reales.  
> Al final extraemos `DEM[(tstart+1):(tstart+7)]`, que son los **7 pronósticos futuros** generados por el MLP para el periodo de validación.
```r
# 1. Leer Datos de Validación con Nuevos Valores de WD y TEMP
fdata.Reg.tv <- readxl::read_excel("DAILY_DEMAND_TV.xlsx")
fdata.Reg.tv <- as.data.frame(fdata.Reg.tv)

# 2. Inicializar Dataset de Nuevos Inputs para Forecast (WD, TEMP)
fdata.Reg.new <- fdata.Reg.tv[, c(2, 3)]

# 3. Crear Variable Auxiliar de Salida DEM con NAs para el Horizonte Futuro
fdata.Reg.new$DEM <- rep(NA, length(fdata.Reg.new[, 1]))

# 4. Unir Datos Históricos de Entrenamiento con Nuevos Registros de Validación
fdata.join <- rbind(fdata[, c(2:4)], fdata.Reg.new)

# 5. Crear Variables Rezagadas sobre el Conjunto Ampliado
fdata.join$WD_lag1   <- Lag(fdata.join$WD,   1)
fdata.join$WD_lag7   <- Lag(fdata.join$WD,   7)
fdata.join$TEMP_lag1 <- Lag(fdata.join$TEMP, 1)
fdata.join$TEMP_lag7 <- Lag(fdata.join$TEMP, 7)
fdata.join$DEM_lag1  <- Lag(fdata.join$DEM,  1)
fdata.join$DEM_lag7  <- Lag(fdata.join$DEM,  7)

# 6. Definir Índice de Inicio del Horizonte de Predicción
tstart <- dim(fdata)[1]

# 7. Bucle de Forecast Iterativo para Horizonte h = 7
for (i in (tstart + 1):(tstart + 7)) {
  # 7.1. Predecir DEM en el Instante i usando el MLP Ajustado
  fdata.join$DEM[i] <- predict(mlp.fit, newdata = fdata.join[i, ])
  
  # 7.2. Recalcular Lags de DEM para que los Siguientes Pasos Usen Predicciones
  fdata.join$DEM_lag1 <- Lag(fdata.join$DEM, 1)
  fdata.join$DEM_lag7 <- Lag(fdata.join$DEM, 7)
}

# 8. Extraer Pronósticos para los 7 Próximos Días
fdata.join$DEM[(tstart + 1):(tstart + 7)]
```

### IV. XGBOOST in NLP
#### 1. Carga de Datos, Creación de Lags y Dataset de Regresión
> En este bloque construimos el **dataset de regresión** que va a usar XGBoost para predecir la demanda.  
> Primero leemos el fichero diario de entrenamiento `DAILY_DEMAND_TR.xlsx` y nos quedamos con las tres variables base:
> 	- **DEM**: demanda (variable objetivo).
> 	- **WD**: tipo de día (laborable / fin de semana).
> 	- **TEMP**: temperatura.
> Para que el modelo pueda capturar la **dinámica temporal** (memoria de la serie), añadimos **retardos (lags)** de cada variable con `Lag()` de `Hmisc`:
> 	- `WD_lag1`, `WD_lag7` → calendario de ayer y del mismo día de la semana pasada.
> 	- `TEMP_lag1`, `TEMP_lag7` → temperatura reciente y patrón semanal.
> 	- `DEM_lag1`, `DEM_lag7` → autoregresión de la propia demanda.
> Estos lags convierten el problema en una regresión tipo **NARX**: XGBoost recibe como inputs tanto valores actuales como pasados.  
> Las primeras filas quedan con `NA` debido a los lags, por lo que creamos `fdata.Reg.tr` eliminando esas filas antes de entrenar el modelo.
```r
# 1. Lectura de Datos de Entrenamiento
fdata <- readxl::read_excel("DAILY_DEMAND_TR.xlsx")
fdata <- as.data.frame(fdata)

# 2. Inicializar Dataset de Regresión con Output e Inputs Contemporáneos

fdata.Reg <- fdata[, c(2, 3, 4)]  # (DEM, WD, TEMP)

# 3. Incluir Variables Rezagadas con Lag de Hmisc
fdata.Reg$WD_lag1    <- Lag(fdata$WD,   1)
fdata.Reg$WD_lag7    <- Lag(fdata$WD,   7)
fdata.Reg$TEMP_lag1  <- Lag(fdata$TEMP, 1)
fdata.Reg$TEMP_lag7  <- Lag(fdata$TEMP, 7)
fdata.Reg$DEM_lag1   <- Lag(fdata$DEM,  1)
fdata.Reg$DEM_lag7   <- Lag(fdata$DEM,  7)

# 4. Crear Dataset de Entrenamiento Eliminando Filas con NAs
fdata.Reg.tr <- na.omit(fdata.Reg)
```
#### 2. Configuración de la Validación Cruzada
> Antes de entrenar XGBoost definimos cómo vamos a **evaluar su capacidad de generalización**.  
> Usamos `caret::trainControl()` con **validación cruzada K-fold (K = 10)**: dividimos los datos en 10 bloques, entrenamos en 9 y validamos en 1, rotando hasta usar todos los bloques como validación.  
> Con `summaryFunction = defaultSummary` obtenemos métricas estándar de regresión (**RMSE, MAE, R²**) en cada fold, y con `savePredictions = TRUE` guardamos todas las predicciones para poder analizar el comportamiento del modelo a posteriori. Esto es lo que usará `caret::train()` al ajustar XGBoost.
```r
# 1. Definir Esquema de Validación Cruzada K-Fold (K = 10)
ctrl_tune <- trainControl(
  method = "cv",                     # Validación cruzada
  number = 10,                       # Número de folds
  summaryFunction = defaultSummary,  # Métricas de rendimiento (RMSE, MAE, R²)
  savePredictions = TRUE             # Guardar predicciones de los folds
)
```
#### 3. Entrenamiento del Modelo y Diagnóstico en Entrenamiento
###### 3.1. Entrenamiento
> En este bloque entrenamos el modelo **XGBoost** usando `caret`.  
> Primero fijamos una semilla (`set.seed(150)`) para que la búsqueda de hiperparámetros sea **reproducible**. Después definimos un **grid de hiperparámetros** (`xgbGrid`) que explora distintas combinaciones de:
> 	- `nrounds` (número de árboles),
> 	- `max_depth` (complejidad de cada árbol),
> 	- `eta` (learning rate),
> 	- otros parámetros de regularización y muestreo (`gamma`, `colsample_bytree`, `min_child_weight`, `subsample`).
> Con `train(..., method = "xgbTree")` y el `trainControl` definido antes, `caret` hace **validación cruzada** para cada combinación del grid y se queda con la que minimiza el **RMSE**. Además, aplicamos un preprocesado de **centrado y escalado** de los inputs para estabilizar el entrenamiento.
> Finalmente inspeccionamos el objeto `xgb.fit`, visualizamos el rendimiento en función de los hiperparámetros (`ggplot(xgb.fit)`) y calculamos la **importancia de variables** con `varImp()`, lo que nos indica qué lags o variables (DEM, WD, TEMP, etc.) son más relevantes para la predicción de la demanda.
```r
# 1. Fijar Semilla para Reproducibilidad
set.seed(150)

# 2. Definir Grid de Hiperparámetros para XGBoost
xgbGrid <- expand.grid(
  nrounds = c(100, 200, 600),   # Número de Árboles de Boosting
  max_depth = c(3, 6),          # Profundidad Máxima de Cada Árbol
  eta = c(0.05, 0.1, 0.3),      # Learning Rate (Tamaño de Paso)
  gamma = c(0),                 # Reducción de Pérdida Mínima para Hacer un Split
  colsample_bytree = c(0.8),    # Proporción de Columnas Muestreadas por Árbol
  min_child_weight = c(1),      # Peso Mínimo en Hijos (Control de Sobreajuste)
  subsample = c(0.8)            # Proporción de Filas Muestreadas por Iteración
)

# 3. Entrenar el Modelo XGBoost con caret
xgb.fit <- train(
  DEM ~ ., 
  data = fdata.Reg.tr, 
  method = "xgbTree",
  tuneGrid = xgbGrid,
  preProcess = c("center", "scale"),  # Centrando y Escalando Inputs
  trControl = ctrl_tune, 
  metric = "RMSE"                     # Métrica de Optimización
)

# 4. Inspeccionar Información del Modelo y del Proceso de Validación
xgb.fit
print(xgb.fit)
ggplot(xgb.fit) + scale_x_log10()

# 5. Importancia de Variables según XGBoost
var_imp <- varImp(xgb.fit)
print(var_imp)
plot(var_imp)
```
###### 3.2 Diagnóstico
> En este bloque evaluamos qué tal se comporta el modelo XGBoost en el **conjunto de entrenamiento**.  
> Primero generamos las predicciones `xgb_pred` sobre `fdata.Reg.tr` y usamos `PlotModelDiagnosis()` para revisar, de forma conjunta, **ajuste vs valores reales** y posibles **patrones en los residuos** (no linealidades no capturadas, heterocedasticidad, etc.).  
> Después calculamos métricas de error con `accuracy()` (RMSE, MAE, …) para cuantificar el rendimiento del modelo en train.  
> Finalmente dibujamos la **serie real frente a la predicha**: si el modelo es razonable, las curvas deberían solaparse bastante, especialmente en la dinámica de medio y largo plazo.
```r
# 1. Obtener Predicciones en el Conjunto de Entrenamiento
xgb_pred <- predict(xgb.fit, newdata = fdata.Reg.tr)

# 7. Diagnóstico del Modelo: Ajuste, Residuos y Patrones
PlotModelDiagnosis(
  fdata.Reg.tr[, -1],  # Variables Explicativas
  fdata.Reg.tr[, 1],   # Demanda Real
  xgb_pred,            # Predicción del Modelo XGBoost
  together = TRUE
)

# 2. Medir Errores de Entrenamiento
accuracy(fdata.Reg.tr[, 1], xgb_pred)

# 3. Gráfico de Serie Real vs Predicción en Entrenamiento
plot(fdata.Reg.tr[, 1],
     type = "l",
     main = "Actual vs Predicted",
     ylab = "Demand")
lines(xgb_pred, col = "red")
legend("topright",
       legend = c("Actual", "Predicted"),
       col = c("black", "red"),
       lty = 1)
```
#### 4. Forecast Multi-Step con XGBoost y Lags Recalculados
> En este bloque usamos el modelo XGBoost entrenado para generar un **forecast multi-step (h = 7 días)**.  
> Primero leemos el fichero de validación `DAILY_DEMAND_TV.xlsx`, que contiene los nuevos valores conocidos de **WD** y **TEMP** para los próximos días, y creamos un dataset `fdata.Reg.new` donde `DEM` está inicialmente a `NA`.  
> A continuación, concatenamos los datos **históricos** con estos nuevos registros en `fdata.join` y volvemos a construir todos los **lags** (de WD, TEMP y DEM).
> El pronóstico se hace de forma **iterativa/recursiva**:
> 	- En cada paso `i` predecimos `DEM[i]` usando `predict(xgb.fit, newdata=fdata.join[i, ])`
> 	- Guardamos esa predicción en `fdata.join$DEM[i]` y **recalculamos los lags de DEM**, de forma que el siguiente paso use como pasado tanto **observaciones reales** como **predicciones previas**.
> Al final extraemos las 7 predicciones correspondientes a los nuevos días, que representan la demanda pronosticada para la próxima semana.
```r
# 1. Leer Datos de Validación con Nuevos Valores de WD y TEMP
fdata.Reg.tv <- readxl::read_excel("DAILY_DEMAND_TV.xlsx")
fdata.Reg.tv <- as.data.frame(fdata.Reg.tv)

# 2. Preparar Dataset de Nuevos Inputs (WD, TEMP) para Forecast
fdata.Reg.new <- fdata.Reg.tv[, c(2, 3)]
fdata.Reg.new$DEM <- rep(NA, nrow(fdata.Reg.new))  # Output Futuro Desconocido

# 3. Unir Datos Históricos y Nuevos Registros en un Solo Data Frame
fdata.join <- rbind(fdata[, c(2:4)], fdata.Reg.new)

# 4. Crear Variables Rezagadas sobre el Conjunto Ampliado
fdata.join$WD_lag1    <- Lag(fdata.join$WD,   1)
fdata.join$WD_lag7    <- Lag(fdata.join$WD,   7)
fdata.join$TEMP_lag1  <- Lag(fdata.join$TEMP, 1)
fdata.join$TEMP_lag7  <- Lag(fdata.join$TEMP, 7)
fdata.join$DEM_lag1   <- Lag(fdata.join$DEM,  1)
fdata.join$DEM_lag7   <- Lag(fdata.join$DEM,  7)

# 5. Definir Índice de Inicio del Horizonte de Predicción
tstart <- nrow(fdata)

# 6. Bucle de Forecast Iterativo para Horizonte h = 7
for (i in (tstart + 1):(tstart + 7)) {
  # 6.1. Predecir DEM en el Instante i con el Modelo XGBoost
  fdata.join$DEM[i] <- predict(xgb.fit, newdata = fdata.join[i, ])
  
  # 6.2. Recalcular Lags de DEM Usando las Predicciones Recientes
  fdata.join$DEM_lag1 <- Lag(fdata.join$DEM, 1)
  fdata.join$DEM_lag7 <- Lag(fdata.join$DEM, 7)
}

# 7. Extraer Pronósticos para los Próximos 7 Días
forecasts <- fdata.join$DEM[(tstart + 1):(tstart + 7)]
print("Forecasted Demand for the next 7 days:")
print(forecasts)
```

Fin de los apuntes de la asignatura :)