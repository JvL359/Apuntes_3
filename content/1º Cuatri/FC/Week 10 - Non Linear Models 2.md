# Teoría en 5 minutos

- **Modelos no lineales como regresión no lineal**: planteamos \\(y_t = f(y_{t-1:t-k}, x_{t:t-k}, \\,\\varepsilon_{t-1:t-k}) + \\varepsilon_t\\). Las variantes **NARX** (sin ruido en la entrada) y **NARMAX** (con ruido/errores realimentados) usan un “aproximador de funciones” (p. ej., redes neuronales). :contentReference[oaicite:0]{index=0}  
- **Sensibilidad estadística en MLP**: medir la relevancia de cada entrada mediante derivadas parciales aproximadas de \\(\\hat y\\) respecto a \\(x_i\\) para hacer *pruning* de variables. :contentReference[oaicite:1]{index=1}  
- **Árboles potenciados (GBM/XGBoost)**: combinación secuencial de aprendices débiles ajustando gradientes de la pérdida; control mediante `eta`, `max_depth`, `subsample`, etc. :contentReference[oaicite:2]{index=2}  
- **Redes recurrentes (Elman/Jordan/LSTM)**: capturan dependencias largas con puertas (LSTM/GRU). :contentReference[oaicite:3]{index=3}  
- **Cambio de régimen**: PAR/ PARIMA (parámetros por estación), TAR/SETAR (umbrales), IOHMM (regímenes guiados por exógenas). :contentReference[oaicite:4]{index=4}  
- **Combinación de pronósticos**: combinación lineal a la Bates–Granger; variantes adaptativas tipo AFTER. :contentReference[oaicite:5]{index=5}

> En esta semana lo llevamos a práctica con: (1) **TF + ingeniería de variables** (no linealidad *via* *features*), y (2) **MLP** con *cross-validation* y *pruning*.

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE, message = FALSE, warning = FALSE, fig.width = 8, fig.height = 4.5)
set.seed(150)
```
Práctica A · Transfer Function + Feature Engineering
Preliminares
Escritura

library(fpp2)
library(lmtest)
library(tseries) # adf.test
library(TSA)
library(readxl)
library(MLTools)
library(imputeTS)
library(ggplot2)

Escritura

Trabaja en la carpeta del script/proyecto
if (interactive()) {
try(setwd(dirname(rstudioapi::getActiveDocumentContext()$path)), silent = TRUE)
}

Carga de datos y EDA rápida
Escritura

DAILY_DEMAND_TR_NA.xlsx debe contener columnas: DATE/WD/TEMP/DEM (o similar).
fdata <- read_excel("DAILY_DEMAND_TR_NA.xlsx")

Conversión a ts con frecuencia semanal (7)
fdata_ts <- ts(fdata, frequency = 7)
autoplot(fdata_ts, facets = TRUE) + ggtitle("Train · Variables originales")

Valores perdidos e imputación
Escritura

Diagnóstico de NA por variable
ggplot_na_distribution(fdata_ts[,2]); ggplot_na_distribution(fdata_ts[,3]); ggplot_na_distribution(fdata_ts[,4])

Dos alternativas de imputación: (i) split estacional y (ii) Kalman (auto.arima)
imp_seas <- na_seasplit(fdata_ts)
imp_kalman <- na_kalman(fdata_ts, model = "auto.arima")

Visualizamos en DEM (columna 4 como en el guion)
ggplot_na_imputations(fdata_ts[,4], imp_seas[,4])
ggplot_na_imputations(fdata_ts[,4], imp_kalman[,4])

Adoptamos imputación estacional por simplicidad (como en clase)
fdata_ts <- imp_seas

Definición de series y escalado
Escritura

y = DEM, x = (WD, TEMP)
y <- fdata_ts[,2]
x <- fdata_ts[,c(3,4)]
autoplot(cbind(y,x), facets = TRUE)

Escalado (elige el que se usó en clase)
y.tr <- y/100
x.tr <- x/1
autoplot(cbind(y.tr,x.tr), facets = TRUE)

Identificación paso a paso (TF con WD y TEMP)
Paso 1 · Arranque con s grandes
Escritura

TF.fit <- arima(y.tr,
xtransf = x.tr,
order = c(1,0,0),
seasonal = list(order = c(1,0,0), period = 7),
transfer = list(c(0,9), c(0,9)),
method = "ML")
TF.RegressionError.plot(y.tr, x.tr, TF.fit, lag.max = 50) # Diferenciación regular necesaria

Paso 2 · Diferencia y reintenta
Escritura

TF.fit <- arima(y.tr,
xtransf = x.tr,
order = c(1,1,0),
seasonal = list(order = c(1,0,0), period = 7),
transfer = list(c(0,9), c(0,9)),
method = "ML")
summary(TF.fit); coeftest(TF.fit)
TF.RegressionError.plot(y.tr, x.tr, TF.fit, lag.max = 50) # Estacionario → seguimos
TF.Identification.plot(x.tr, TF.fit) # WD: b=0,r=0,s=0 · TEMP: b=0,r=0,s=1

Paso 3 · Fijar (b,r,s) y estimar ARIMA
Escritura

TF.fit <- arima(y.tr,
xtransf = x.tr,
order = c(2,1,1),
seasonal = list(order = c(1,0,0), period = 7),
transfer = list(c(0,0), c(0,1)),
method = "ML")
summary(TF.fit); coeftest(TF.fit)
CheckResiduals.ICAI(TF.fit, lag = 50)
PlotModelDiagnosis(x.tr, y.tr, fitted(TF.fit), together = TRUE)

Ingeniería de variables de temperatura (no linealidad)
Dividimos la temperatura en frío y calor (umbrales 17º y 22º) para capturar la curvatura en la relación TEMP–DEM.

Escritura

Visual relación T–DEM
ggplot(as.data.frame(fdata)) + geom_point(aes(x = TEMP, y = DEM), alpha = 0.4)

Nuevas variables
fdata$tcold <- sapply(as.numeric(fdata_ts[,4]), min, 17) # exceso de frío
fdata$thot <- sapply(as.numeric(fdata_ts[,4]), max, 22) # exceso de calor

Series con WD, tcold, thot
y <- ts(fdata[,2], frequency = 7)
x <- ts(fdata[,c(3,5,6)], frequency = 7)

Re-escalado
y.tr <- y/100
x.tr <- x/1
autoplot(cbind(y.tr,x.tr), facets = TRUE)

Identificación con (WD, tcold, thot)
Escritura

1) Arranque con s grandes
TF.fit <- arima(y.tr,
xtransf = x.tr,
order = c(1,0,0),
seasonal = list(order = c(1,0,0), period = 7),
transfer = list(c(0,9), c(0,9), c(0,9)),
method = "ML")
TF.RegressionError.plot(y.tr, x.tr, TF.fit, lag.max = 50)

2) Diferenciamos
TF.fit <- arima(y.tr,
xtransf = x.tr,
order = c(1,1,0),
seasonal = list(order = c(1,0,0), period = 7),
transfer = list(c(0,9), c(0,9), c(0,9)),
method = "ML")
summary(TF.fit); coeftest(TF.fit)
TF.RegressionError.plot(y.tr, x.tr, TF.fit, lag.max = 50)
TF.Identification.plot(x.tr, TF.fit) # WD: (0,0,0) · tcold: (0,1,0) · thot: (0,1,0)

3) Modelo con (b,r,s) fijados
TF.fit <- arima(y.tr,
xtransf = x.tr,
order = c(2,1,0),
seasonal = list(order = c(1,0,0), period = 7),
transfer = list(c(0,0), c(1,0), c(1,0)),
method = "ML")
summary(TF.fit); coeftest(TF.fit); CheckResiduals.ICAI(TF.fit, lag = 50)

4) MA en vez de AR(2)
TF.fit <- arima(y.tr,
xtransf = x.tr,
order = c(0,1,2),
seasonal = list(order = c(1,0,0), period = 7),
transfer = list(c(0,0), c(1,0), c(1,0)),
method = "ML")
summary(TF.fit); coeftest(TF.fit); CheckResiduals.ICAI(TF.fit, lag = 50)

5) Incrementar órdenes
TF.fit <- arima(y.tr,
xtransf = x.tr,
order = c(0,1,5),
seasonal = list(order = c(2,0,0), period = 7),
transfer = list(c(0,0), c(1,0), c(1,0)),
method = "ML")
summary(TF.fit); coeftest(TF.fit); CheckResiduals.ICAI(TF.fit, lag = 50)

6) Alternativa AR
TF.fit <- arima(y.tr,
xtransf = x.tr,
order = c(5,1,0),
seasonal = list(order = c(2,0,0), period = 7),
transfer = list(c(0,0), c(1,0), c(1,0)),
method = "ML")
summary(TF.fit); coeftest(TF.fit); CheckResiduals.ICAI(TF.fit, lag = 50)

CCF de residuos con cada exógena
res <- residuals(TF.fit); res[is.na(res)] <- 0
ccf(y = res, x = x.tr[,1]); ccf(y = res, x = x.tr[,2]); ccf(y = res, x = x.tr[,3])

7) Ajuste fino de TF para X1 si fuera necesario
TF.fit <- arima(y.tr,
xtransf = x.tr,
order = c(5,1,0),
seasonal = list(order = c(2,0,0), period = 7),
transfer = list(c(0,1), c(1,0), c(1,0)),
method = "ML")
summary(TF.fit); coeftest(TF.fit); CheckResiduals.ICAI(TF.fit, lag = 50)

Fitted y diagnóstico final
autoplot(y.tr, series = "Real") + forecast::autolayer(fitted(TF.fit), series = "Fitted")
accuracy(fitted(TF.fit), y.tr)
PlotModelDiagnosis(x.tr, y.tr, fitted(TF.fit), together = TRUE)

Pronóstico (h = 7)
Escritura

x.tv <- read_excel("DAILY_DEMAND_TV.xlsx")
x.tv$tcold <- sapply(x.tv$TEMP, min, 17)
x.tv$thot <- sapply(x.tv$TEMP, max, 22)

x.tv <- ts(x.tv[,c(2,4,5)])
val.forecast_h7 <- TF.forecast(y.old = y.tr,
x.old = x.tr,
x.new = x.tv,
model = TF.fit,
h = 7)
val.forecast_h7 * 100

Práctica B · MLP para pronóstico no lineal
Preliminares
Escritura

library(MLTools)
library(fpp2)
library(lmtest)
library(tseries)
library(TSA)

library(NeuralSens)
library(caret)
library(kernlab)
library(nnet)
library(NeuralNetTools)
library(Hmisc) # Lag()

Escritura

if (interactive()) {
try(setwd(dirname(rstudioapi::getActiveDocumentContext()$path)), silent = TRUE)
}

Carga y feature set con retardos
Escritura

fdata <- readxl::read_excel("DAILY_DEMAND_TR.xlsx") |> as.data.frame()

Entradas/Salida básicas
fdata.Reg <- fdata[, c(2,3,4)] # DEM, WD, TEMP

Retardos (1 y 7)
fdata.Reg$WD_lag1 <- Lag(fdata$WD, 1)
fdata.Reg$WD_lag7 <- Lag(fdata$WD, 7)
fdata.Reg$TEMP_lag1 <- Lag(fdata$TEMP, 1)
fdata.Reg$TEMP_lag7 <- Lag(fdata$TEMP, 7)
fdata.Reg$DEM_lag1 <- Lag(fdata$DEM, 1)
fdata.Reg$DEM_lag7 <- Lag(fdata$DEM, 7)

head(fdata.Reg)
fdata.Reg.tr <- na.omit(fdata.Reg)

Cross-validation y grid de hiperparámetros
Escritura

ctrl_tune <- trainControl(method = "cv",
number = 10,
summaryFunction = defaultSummary,
savePredictions = TRUE)

set.seed(150)
mlp.fit <- train(form = DEM ~ .,
data = fdata.Reg.tr,
method = "nnet",
linout = TRUE,
tuneGrid = expand.grid(size = seq(10,20,length.out = 3),
decay = 10^(c(-3:0))),
maxit = 200,
preProcess = c("center","scale"),
trControl = ctrl_tune,
metric = "RMSE")
mlp.fit
ggplot(mlp.fit) + scale_x_log10()
plotnet(mlp.fit$finalModel)
SensAnalysisMLP(mlp.fit)

Diagnóstico y error en train
Escritura

mlp_pred <- predict(mlp.fit, newdata = fdata.Reg.tr)
PlotModelDiagnosis(fdata.Reg.tr[,-1], fdata.Reg.tr[,1], mlp_pred, together = TRUE)
accuracy(fdata.Reg.tr[,1], mlp_pred)

plot(fdata.Reg.tr[,1], type = "l", main = "DEM vs MLP (train)"); lines(mlp_pred, col = "red")

Red “pruned” (selección de entradas)
Escritura

set.seed(150)
mlp.fit2 <- train(form = DEM ~ WD + DEM_lag1 + WD_lag1 + TEMP,
data = fdata.Reg.tr,
method = "nnet",
linout = TRUE,
tuneGrid = expand.grid(size = seq(10,20,length.out = 3),
decay = 10^(c(-3:0))),
maxit = 200,
preProcess = c("center","scale"),
trControl = ctrl_tune,
metric = "RMSE")
mlp.fit2
ggplot(mlp.fit2) + scale_x_log10()
plotnet(mlp.fit2$finalModel)
SensAnalysisMLP(mlp.fit2)

Pronóstico recursivo (h = 7)
Escritura

fdata.Reg.tv <- readxl::read_excel("DAILY_DEMAND_TV.xlsx") |> as.data.frame()

Conservar WD y TEMP de validación, crear DEM como NA
fdata.Reg.new <- fdata.Reg.tv[, c(2,3)]
fdata.Reg.new$DEM <- rep(NA, nrow(fdata.Reg.new))

Unimos para disponer de históricos y generar retardos
fdata.join <- rbind(fdata[,c(2:4)], fdata.Reg.new)

Retardos (se recalcularán dentro del bucle)
fdata.join$WD_lag1 <- Lag(fdata.join$WD, 1)
fdata.join$WD_lag7 <- Lag(fdata.join$WD, 7)
fdata.join$TEMP_lag1 <- Lag(fdata.join$TEMP, 1)
fdata.join$TEMP_lag7 <- Lag(fdata.join$TEMP, 7)
fdata.join$DEM_lag1 <- Lag(fdata.join$DEM, 1)
fdata.join$DEM_lag7 <- Lag(fdata.join$DEM, 7)

Bucle de 7 pasos (multi-step con actualización de lags)
tstart <- nrow(fdata)
for (i in (tstart+1):(tstart+7)) {
fdata.join$DEM[i] <- predict(mlp.fit, newdata = fdata.join[i,])
fdata.join$DEM_lag1 <- Lag(fdata.join$DEM, 1)
fdata.join$DEM_lag7 <- Lag(fdata.join$DEM, 7)
}

Pronósticos
fdata.join$DEM[(tstart+1):(tstart+7)]

(Opcional) Combinar TF y MLP
Si deseas, puedes combinar ambos pronósticos (media simple o pesos a la Bates-Granger). Este bloque está como ejemplo y no se evalúa por defecto.

Escritura

Supón que tienes y_tv_true (observado) y dos vectores pred_TF, pred_MLP de igual longitud
pred_COMB <- 0.5pred_TF + 0.5pred_MLP
accuracy(y_tv_true, pred_TF)
accuracy(y_tv_true, pred_MLP)
accuracy(y_tv_true, pred_COMB) # suele mejorar si los errores están poco correlacionados

Conclusiones rápidas
La no linealidad entre temperatura y demanda se captura bien dividiendo TEMP en tcold/thot y usándolas en una TF con estructura ARIMA en el ruido.

Una MLP con cross-validation y pruning ofrece una alternativa competitiva; la sensibilidad ayuda a justificar qué features mantener.

En validación, compara TF vs MLP y, si procede, combina para mejorar RMSE/MAE cuando los errores son complementarios.



---

```r
#################################################################################
##############      Week 10: Nonlinear forecasting (TF + MLP)    ################
##############     --------- Lab script (teaching version) -------- #############
#################################################################################

# Preliminares ------------------------------------------------------------------
library(fpp2)
library(ggplot2)
library(lmtest)
library(tseries)         # adf.test
library(TSA)             # arima() con xtransf/transfer
library(readxl)
library(MLTools)
library(imputeTS)
library(Hmisc)           # Lag()
# Modelos no lineales (MLP)
library(caret)
library(nnet)
library(NeuralNetTools)
# (opcional) análisis de sensibilidad para MLP
suppressWarnings(suppressMessages({
  if (requireNamespace("NeuralSens", quietly = TRUE)) library(NeuralSens)
}))

# Directorio de trabajo ---------------------------------------------------------
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

#################################################################################
# PARTE A. Transfer Function + Feature Engineering (no linealidad vía TEMP)
#################################################################################

# 1) Lectura y EDA rápida -------------------------------------------------------
f_tr_na <- read_excel("DAILY_DEMAND_TR_NA.xlsx")   # cols: DATE, DEM, WD, TEMP
f_tr_na <- as.data.frame(f_tr_na)

# Conversión a ts (freq=7, diaria con patrón semanal) y visualización
ts_tr_na <- ts(f_tr_na[, -1], frequency = 7)
autoplot(ts_tr_na, facets = TRUE) + ggtitle("Train con posibles NA (DEM, WD, TEMP)")

# 2) Imputación de huecos -------------------------------------------------------
# Diagnóstico de NA (por variable)
ggplot_na_distribution(ts_tr_na[, "DEM"])
ggplot_na_distribution(ts_tr_na[, "WD"])
ggplot_na_distribution(ts_tr_na[, "TEMP"])

# Dos enfoques: estacional y Kalman; para la práctica nos quedamos con el estacional
imp_seas   <- na_seasplit(ts_tr_na)
imp_kalman <- na_kalman(ts_tr_na, model = "auto.arima")

# Visual de ejemplo sobre TEMP
ggplot_na_imputations(ts_tr_na[, "TEMP"], imp_seas[, "TEMP"])
ggplot_na_imputations(ts_tr_na[, "TEMP"], imp_kalman[, "TEMP"])

ts_tr <- imp_seas   # Usaremos la versión imputada estacionalmente

# 3) Variables y escalado -------------------------------------------------------
y <- ts_tr[, "DEM"]
x <- ts_tr[, c("WD", "TEMP")]
autoplot(cbind(y, x), facets = TRUE)

# Escalado para estabilidad numérica (mantenemos DEM ~ O(1))
y.tr <- y / 100
x.tr <- x / 1
autoplot(cbind(y.tr, x.tr), facets = TRUE) + ggtitle("Series escaladas")

# 4) Identificación (pasos docentes) -------------------------------------------
# 4.1. Modelo inicial con s grande (para ver polinomios de transferencia)
TF.fit <- arima(y.tr,
                xtransf = x.tr,
                order = c(1, 0, 0),
                seasonal = list(order = c(1, 0, 0), period = 7),
                transfer = list(c(0, 9), c(0, 9)),
                method = "ML")

TF.RegressionError.plot(y.tr, x.tr, TF.fit, lag.max = 50)   # pide diferencia regular

# 4.2. Diferenciamos (d=1). Identificación de (b,r,s) por variable
TF.fit <- arima(y.tr,
                xtransf = x.tr,
                order = c(1, 1, 0),
                seasonal = list(order = c(1, 0, 0), period = 7),
                transfer = list(c(0, 9), c(0, 9)),
                method = "ML")
summary(TF.fit); coeftest(TF.fit)
TF.RegressionError.plot(y.tr, x.tr, TF.fit, lag.max = 50)   # estacionario
TF.Identification.plot(x.tr, TF.fit)                       # WD: (0,0,0) / TEMP: (0,1,0) (orientativo)

# 4.3. Con (b,r,s) candidate y ARIMA de ruido
TF.fit <- arima(y.tr,
                xtransf = x.tr,
                order = c(2, 1, 1),
                seasonal = list(order = c(1, 0, 0), period = 7),
                transfer = list(c(0, 0), c(0, 1)),
                method = "ML")
summary(TF.fit); coeftest(TF.fit)
CheckResiduals.ICAI(TF.fit, lag = 50)
PlotModelDiagnosis(x.tr, y.tr, fitted(TF.fit), together = TRUE)

# 5) Feature engineering no lineal en TEMP --------------------------------------
# Relación no lineal DEM ~ TEMP: generamos "bisagras" frío/calor (17ºC / 22ºC)
# tcold = max(17 - TEMP, 0); thot = max(TEMP - 22, 0)
f_tr <- f_tr_na
f_tr$tcold <- pmax(17 - f_tr$TEMP, 0)
f_tr$thot  <- pmax(f_tr$TEMP - 22, 0)

y <- ts(f_tr$DEM, frequency = 7)
x <- ts(f_tr[, c("WD", "tcold", "thot")], frequency = 7)
y.tr <- y / 100
x.tr <- x / 1
autoplot(cbind(y.tr, x.tr), facets = TRUE) + ggtitle("Con features no lineales (tcold/thot)")

# 6) Re-identificación y ajuste final (pasos docentes) --------------------------
# (1) s grande
TF.fit <- arima(y.tr, xtransf = x.tr,
                order = c(1, 0, 0),
                seasonal = list(order = c(1, 0, 0), period = 7),
                transfer = list(c(0, 9), c(0, 9), c(0, 9)),
                method = "ML")
TF.RegressionError.plot(y.tr, x.tr, TF.fit, lag.max = 50)  # d=1

# (2) con d=1 y s grande
TF.fit <- arima(y.tr, xtransf = x.tr,
                order = c(1, 1, 0),
                seasonal = list(order = c(1, 0, 0), period = 7),
                transfer = list(c(0, 9), c(0, 9), c(0, 9)),
                method = "ML")
summary(TF.fit); coeftest(TF.fit)
TF.RegressionError.plot(y.tr, x.tr, TF.fit, lag.max = 50)
TF.Identification.plot(x.tr, TF.fit)
# WD: (0,0,0)   tcold: (1,0)   thot: (1,0)  (orientativo)

# (3)–(7) búsqueda de estructura ARIMA y TF (como en la guía docente)
TF.fit <- arima(y.tr, xtransf = x.tr,
                order = c(5, 1, 0),
                seasonal = list(order = c(2, 0, 0), period = 7),
                transfer = list(c(0, 1), c(1, 0), c(1, 0)),  # WD con s=1; tcold/thot r=1
                method = "ML")
summary(TF.fit); coeftest(TF.fit)
CheckResiduals.ICAI(TF.fit, lag = 50)

# CCF residuos vs inputs (diagnóstico)
res <- residuals(TF.fit); res[is.na(res)] <- 0
ccf(ts(res, start = start(y.tr), frequency = 7), x.tr[, "WD"])
ccf(ts(res, start = start(y.tr), frequency = 7), x.tr[, "tcold"])
ccf(ts(res, start = start(y.tr), frequency = 7), x.tr[, "thot"])

# Ajuste y error en train
autoplot(y.tr, series = "Real") + forecast::autolayer(fitted(TF.fit), series = "Fitted")
acc_TF_train <- accuracy(fitted(TF.fit), y.tr); acc_TF_train
PlotModelDiagnosis(x.tr, y.tr, fitted(TF.fit), together = TRUE)

# 7) Forecast h = 7 con covariables nuevas --------------------------------------
x.tv <- read_excel("DAILY_DEMAND_TV.xlsx")    # cols: DATE, WD, TEMP
x.tv <- as.data.frame(x.tv)
# Generamos tcold/thot para TV
x.tv$tcold <- pmax(17 - x.tv$TEMP, 0)
x.tv$thot  <- pmax(x.tv$TEMP - 22, 0)
x.tv.ts <- ts(x.tv[, c("WD", "tcold", "thot")], frequency = 7)

# Pronóstico con parámetros del TF
fc_TF_h7 <- TF.forecast(y.old = y.tr,
                        x.old = x.tr,
                        x.new = x.tv.ts,
                        model = TF.fit,
                        h = 7)
# Devuelve en escala de y.tr → desescalar:
TF_forecast <- as.numeric(fc_TF_h7) * 100
TF_forecast

#################################################################################
# PARTE B. MLP (Multilayer Perceptron) para pronóstico no lineal
#################################################################################

# 8) Lectura (train limpio) y lags ---------------------------------------------
f_tr_clean <- read_excel("DAILY_DEMAND_TR.xlsx")  # mismo formato pero sin NA
f_tr_clean <- as.data.frame(f_tr_clean)

# Conjunto para regresión (DEM como y; WD y TEMP como x); añadimos retardos útiles
reg <- f_tr_clean[, c("DEM", "WD", "TEMP")]
reg$WD_lag1   <- Lag(reg$WD,   1)
reg$WD_lag7   <- Lag(reg$WD,   7)
reg$TEMP_lag1 <- Lag(reg$TEMP, 1)
reg$TEMP_lag7 <- Lag(reg$TEMP, 7)
reg$DEM_lag1  <- Lag(reg$DEM,  1)
reg$DEM_lag7  <- Lag(reg$DEM,  7)

reg_tr <- na.omit(reg)   # eliminamos NAs de los lags iniciales

# 9) Control de CV y entrenamiento MLP ------------------------------------------
set.seed(150)
ctrl_cv <- trainControl(method = "cv", number = 10,
                        summaryFunction = defaultSummary,
                        savePredictions = TRUE)

# Modelo completo (todas las entradas)
set.seed(150)
mlp.fit <- train(DEM ~ .,
                 data = reg_tr,
                 method = "nnet",
                 linout = TRUE,
                 tuneGrid = expand.grid(size = seq(10, 20, length.out = 3),
                                        decay = 10^(-3:0)),
                 maxit = 200,
                 preProcess = c("center", "scale"),
                 trControl = ctrl_cv,
                 metric = "RMSE")
mlp.fit
ggplot(mlp.fit) + scale_x_log10()
try(plotnet(mlp.fit$finalModel), silent = TRUE)
if ("NeuralSens" %in% .packages()) try(SensAnalysisMLP(mlp.fit), silent = TRUE)

# Diagnóstico y error en train
mlp_pred <- predict(mlp.fit, newdata = reg_tr)
PlotModelDiagnosis(reg_tr[, -1], reg_tr[, 1], mlp_pred, together = TRUE)
acc_MLP_train <- accuracy(reg_tr[, 1], mlp_pred); acc_MLP_train

# (Opcional) red podada con subconjunto de variables
set.seed(150)
mlp.fit2 <- train(DEM ~ WD + DEM_lag1 + WD_lag1 + TEMP,
                  data = reg_tr,
                  method = "nnet",
                  linout = TRUE,
                  tuneGrid = expand.grid(size = seq(10, 20, length.out = 3),
                                         decay = 10^(-3:0)),
                  maxit = 200,
                  preProcess = c("center", "scale"),
                  trControl = ctrl_cv,
                  metric = "RMSE")
mlp.fit2
ggplot(mlp.fit2) + scale_x_log10()
try(plotnet(mlp.fit2$finalModel), silent = TRUE)
if ("NeuralSens" %in% .packages()) try(SensAnalysisMLP(mlp.fit2), silent = TRUE)

# 10) Forecast h = 7 con MLP (recursivo para DEM_lag) ---------------------------
x_tv <- read_excel("DAILY_DEMAND_TV.xlsx")    # WD, TEMP para los 7 días (sin DEM)
x_tv <- as.data.frame(x_tv)

# Construimos dataset conjunto (histórico + 7 nuevos) para crear lags con DEM previos
join <- rbind(f_tr_clean[, c("WD", "TEMP", "DEM")],
              data.frame(WD = x_tv$WD, TEMP = x_tv$TEMP, DEM = NA_real_))

# Recalcular lags y predecir de forma recursiva con el mejor MLP (elige mlp.fit o mlp.fit2)
best_mlp <- if (min(mlp.fit$results$RMSE) <= min(mlp.fit2$results$RMSE)) mlp.fit else mlp.fit2

tstart <- nrow(f_tr_clean)
for (i in (tstart + 1):(tstart + 7)) {
  join$WD_lag1[i]   <- join$WD[i - 1]
  join$WD_lag7[i]   <- join$WD[i - 7]
  join$TEMP_lag1[i] <- join$TEMP[i - 1]
  join$TEMP_lag7[i] <- join$TEMP[i - 7]
  join$DEM_lag1[i]  <- join$DEM[i - 1]
  join$DEM_lag7[i]  <- join$DEM[i - 7]

  # Predicción y escritura para que al siguiente día se usen sus lags
  join$DEM[i] <- predict(best_mlp, newdata = join[i, ])
}

MLP_forecast <- join$DEM[(tstart + 1):(tstart + 7)]
MLP_forecast

#################################################################################
# PARTE C. Comparación y combinación de pronósticos (TF vs MLP)
#################################################################################

# 11) Métricas de entrenamiento (escalas originales) ----------------------------
# TF en escala original
y_orig      <- as.numeric(y.tr) * 100
yhat_TF_tr  <- as.numeric(fitted(TF.fit)) * 100
rmse_TF_tr  <- sqrt(mean((y_orig - yhat_TF_tr)^2))
mae_TF_tr   <- mean(abs(y_orig - yhat_TF_tr))

# MLP (usa reg_tr)
rmse_MLP_tr <- sqrt(mean((reg_tr$DEM - mlp_pred)^2))
mae_MLP_tr  <- mean(abs(reg_tr$DEM - mlp_pred))

data.frame(Model = c("TF (train)", "MLP (train)"),
           RMSE  = c(rmse_TF_tr, rmse_MLP_tr),
           MAE   = c(mae_TF_tr,  mae_MLP_tr))

# 12) Pronósticos h=7 y combinación (ponderación por 1/RMSE^2) -----------------
TF_fc  <- as.numeric(TF_forecast)
MLP_fc <- as.numeric(MLP_forecast)

w_TF  <- 1 / (rmse_TF_tr^2)
w_MLP <- 1 / (rmse_MLP_tr^2)
w_TF  <- w_TF / (w_TF + w_MLP)
w_MLP <- 1 - w_TF

FC_comb <- w_TF * TF_fc + w_MLP * MLP_fc
weights <- c(w_TF = w_TF, w_MLP = w_MLP); weights

# 13) Tabla final de pronósticos ------------------------------------------------
salida <- data.frame(
  Day = 1:7,
  TF   = round(TF_fc,  2),
  MLP  = round(MLP_fc, 2),
  COMB = round(FC_comb, 2)
)
salida

# (Si tu fichero TV trae las fechas en una primera columna DATE, puedes añadirlas:)
if ("DATE" %in% names(x.tv)) {
  salida$DATE <- as.Date(x.tv$DATE)
  salida <- salida[, c("DATE", "TF", "MLP", "COMB")]
}
salida

# 14) Visual rápido (si hay fecha en TV) ---------------------------------------
if ("DATE" %in% names(x.tv)) {
  ggplot(salida, aes(DATE)) +
    geom_line(aes(y = TF,  color = "TF"))  +
    geom_line(aes(y = MLP, color = "MLP")) +
    geom_line(aes(y = COMB, color = "COMB"), linewidth = 1) +
    scale_color_manual(values = c("TF" = "#e31a1c", "MLP" = "#1f78b4", "COMB" = "#33a02c")) +
    labs(title = "Forecasts h=7 (TF, MLP y combinación)", x = NULL, y = "Demanda") +
    theme_minimal(base_size = 12)
}

#################################################################################
# FIN DEL LAB WEEK 10
#################################################################################
```
