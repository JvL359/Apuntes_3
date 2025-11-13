
**TF + Feature Engineering · MLP · Advanced methods**

> [!summary] Objetivos de aprendizaje
> 
> - Entender cuándo un modelo **no lineal** mejora la predicción frente a ARIMA/SARIMA.
>     
> - Aplicar **funciones de transferencia (TF)** con _feature engineering_ (temperatura “fría/caliente”).
>     
> - Tratar **valores perdidos** en datos diarios y validar el impacto en el modelo.
>     
> - Entrenar una **red neuronal MLP** con _lags_ y evaluar importancia de variables.
>     
> - Conocer, a nivel conceptual, **regime switching** y **combinación de predictores**.
>     

---

## Datos y librerías

- **Ficheros**:
    
    - `DAILY_DEMAND_TR_NA.xlsx` (train con NAs)
        
    - `DAILY_DEMAND_TR.xlsx` (train limpio)
        
    - `DAILY_DEMAND_TV.xlsx` (validación, h = 7)
        
- **Frecuencia**: diaria con **estacionalidad semanal** (`frequency = 7`).
    
- **Paquetes**: `fpp2`, `TSA`, `lmtest`, `tseries`, `readxl`, `imputeTS`, `MLTools`, `caret`, `nnet`, `NeuralSens`, `NeuralNetTools`.
    

> [!tip] Recordatorio
> 
> - Usa siempre `setwd(dirname(rstudioapi::getActiveDocumentContext()$path))` al inicio.
>     
> - Escala y guarda la escala para deshacerla al final si necesitas interpretar en unidades originales.
>     

---

## Apuntes de teoría (resumen)

### 1) Modelos no lineales (visión general)

- Enfoque de **regresión no lineal**:
    
    yk=f(yk−1:k−p, xk:k−q, εk−1:k−r)+εky_k = f\big(y_{k-1:k-p},\, x_{k:k-q},\, \varepsilon_{k-1:k-r}\big) + \varepsilon_kyk​=f(yk−1:k−p​,xk:k−q​,εk−1:k−r​)+εk​
    
    Donde fff es una función no lineal (red neuronal, árbol, etc.). Casos habituales: **NARX** (con _lags_ de yyy y xxx) y **NARMAX** (incluye términos del error).
    
- **MLP** como aproximador universal: entrenar con _lags_ de entrada y de la propia serie; útil cuando la relación con los _drivers_ (p.ej. temperatura) **no es lineal**. La **sensibilidad estadística** mide la relevancia de una entrada xix_ixi​ como ∂y^/∂xi\partial \hat y/\partial x_i∂y^​/∂xi​.
    

### 2) Otras familias no lineales

- **Gradient Boosting / XGBoost**: ensamble secuencial que ajusta los **residuos** de etapas previas. Parámetros típicos: `eta`, `max_depth`, `subsample`, `colsample_bytree`, `gamma`, `min_child_weight`. Útil con muchas _features_.
    
- **RNN/LSTM**: redes recurrentes para dependencias de largo alcance; los **LSTM** introducen compuertas para controlar flujo de información. (Referencia conceptual para el curso).
    

### 3) Regime switching

- **PAR(p)**: coeficientes que **cambian por estación**; extensión a **PARIMA**.
    
- **TAR/SETAR**: la dinámica cambia cuando la serie cruza **umbrales** (p. ej., yt−ky_{t-k}yt−k​ en intervalos).
    
- **IOHMM**: los **regímenes/estados** dependen de variables exógenas.
    

### 4) Combinación de predictores

- Para dos predictores y^1,y^2\hat y_1,\hat y_2y^​1​,y^​2​: combinación lineal y^c=k1y^1+k2y^2\hat y_c = k_1 \hat y_1 + k_2 \hat y_2y^​c​=k1​y^​1​+k2​y^​2​ (si son insesgados, k2=1−k1k_2=1-k_1k2​=1−k1​). El **peso óptimo** minimiza la varianza del error combinando varianzas y correlación de errores. **AFTER** ajusta pesos **de forma adaptativa** en el tiempo usando errores recientes.
    

---

## Lab 10 · Parte A — TF + Feature Engineering (no linealidad vía _features_)

### 0) Preliminares e imputación de NAs

`library(fpp2); library(TSA); library(lmtest); library(tseries) library(readxl); library(MLTools); library(imputeTS)  setwd(dirname(rstudioapi::getActiveDocumentContext()$path))  # 1) Lectura fdata <- read_excel("DAILY_DEMAND_TR_NA.xlsx")  # 2) Serie temporal con estacionalidad semanal fdata_ts <- ts(fdata, frequency = 7) autoplot(fdata_ts, facets = TRUE)  # 3) Diagnóstico de NAs ggplot_na_distribution(fdata_ts[,2]) ggplot_na_distribution(fdata_ts[,3]) ggplot_na_distribution(fdata_ts[,4])  # 4) Imputación (elige uno; aquí usamos estacional) imp_seas   <- na_seasplit(fdata_ts) imp_kalman <- na_kalman(fdata_ts, model = "auto.arima")  # 5) Nos quedamos con imp_seas para mantener estructura semanal fdata_ts <- imp_seas`

> [!note] ¿Por qué imputar?  
> Sin imputación los coeficientes de TF/ARIMA se sesgan; usa un método **coherente con la estacionalidad** (semanal) antes de identificar el modelo.

### 1) Modelo TF con variables exógenas (WD, TEMP)

`# Variables y <- fdata_ts[, 2]           # DEM x <- fdata_ts[, c(3,4)]      # WD y TEMP  # Escalado (para estabilidad numérica) y.tr <- y/100 x.tr <- x/1  autoplot(cbind(y.tr, x.tr), facets = TRUE)  # Paso 1: TF inicial con s grande para identificación TF.fit <- arima(y.tr,                 xtransf = x.tr,                 order = c(1,0,0),                 seasonal = list(order = c(1,0,0), period = 7),                 transfer = list(c(0,9), c(0,9)),                 method = "ML")  TF.RegressionError.plot(y.tr, x.tr, TF.fit, lag.max = 50)  # Paso 2: Diferenciar si es necesario y revisar identificación TF.fit <- arima(y.tr,                 xtransf = x.tr,                 order = c(1,1,0),                         # d=1                 seasonal = list(order = c(1,0,0), period = 7),                 transfer = list(c(0,9), c(0,9)),                 method = "ML")  summary(TF.fit); coeftest(TF.fit) TF.RegressionError.plot(y.tr, x.tr, TF.fit, lag.max = 50) TF.Identification.plot(x.tr, TF.fit)  # guía para (b,r,s) # (WD: b=0,r=0,s=0) (TEMP: b=0,r=0,s=1) según el ejemplo de clase`

### 2) _Feature engineering_ de temperatura (no linealidad)

La relación demanda–temperatura no suele ser lineal. Separamos en **frío** y **calor** (umbrales típicos 17°/22°) y reentrenamos.

`# Scatter para ver no linealidad ggplot(as.data.frame(fdata_ts)) +    geom_point(aes(x = TEMP, y = DEM))  # Nuevas features fdata$tcold <- sapply(as.numeric(fdata_ts[,4]), min, 17)  # por debajo de 17 fdata$thot  <- sapply(as.numeric(fdata_ts[,4]), max, 22)  # por encima de 22  y <- ts(fdata[,2], frequency = 7) x <- ts(fdata[,c(3,5,6)], frequency = 7)   # WD, tcold, thot  y.tr <- y/100; x.tr <- x/1 autoplot(cbind(y.tr, x.tr), facets = TRUE)  # TF inicial con s grande TF.fit <- arima(y.tr,                 xtransf = x.tr,                 order = c(1,1,0),                 seasonal = list(order = c(1,0,0), period = 7),                 transfer = list(c(0,9), c(0,9), c(0,9)),                 method = "ML") summary(TF.fit); coeftest(TF.fit) TF.RegressionError.plot(y.tr, x.tr, TF.fit, lag.max = 50) TF.Identification.plot(x.tr, TF.fit) # (WD: 0,0,0) (tcold: 0,1,0) (thot: 0,1,0) — según indicación de clase  # Afinado ARMA + TF TF.fit <- arima(y.tr,                 xtransf = x.tr,                 order = c(5,1,0),                             # ejemplo final bueno                 seasonal = list(order = c(2,0,0), period = 7),                 transfer = list(c(0,1), c(1,0), c(1,0)),                 method = "ML")  summary(TF.fit); coeftest(TF.fit) CheckResiduals.ICAI(TF.fit, lag = 50)  # CCF residuos vs X para verificar que no queda relación res <- residuals(TF.fit); res[is.na(res)] <- 0 ccf(res, x.tr[,1]); ccf(res, x.tr[,2]); ccf(res, x.tr[,3])  # Ajuste y diagnóstico autoplot(y.tr, series = "Real") + forecast::autolayer(fitted(TF.fit), series = "Fitted") accuracy(fitted(TF.fit), y.tr) PlotModelDiagnosis(x.tr, y.tr, fitted(TF.fit), together = TRUE)`

### 3) _Forecast_ h = 7 con _drivers_ futuros

`x.tv <- read_excel("DAILY_DEMAND_TV.xlsx") x.tv$tcold <- sapply(x.tv$TEMP, min, 17) x.tv$thot  <- sapply(x.tv$TEMP, max, 22) x.tv <- ts(x.tv[, c(2,4,5)])   # WD, tcold, thot  val.forecast_h7 <- TF.forecast(y.old = y.tr,                                x.old = x.tr,                                x.new = x.tv,                                model = TF.fit,                                h = 7)  # Desescalar si quieres valores en demanda original: pred_h7 <- val.forecast_h7 * 100 pred_h7`

---

## Lab 10 · Parte B — MLP para _nonlinear forecasting_

### 0) _Features_ y _lags_

`library(MLTools); library(fpp2); library(caret); library(nnet) library(NeuralSens); library(NeuralNetTools); library(TSA); library(lmtest)  setwd(dirname(rstudioapi::getActiveDocumentContext()$path))  fdata <- readxl::read_excel("DAILY_DEMAND_TR.xlsx") |> as.data.frame()  # Variables base (DEM, WD, TEMP) fdata.Reg <- fdata[, c(2,3,4)]  # Lags con Hmisc::Lag library(Hmisc) fdata.Reg$WD_lag1   <- Lag(fdata$WD,   1) fdata.Reg$WD_lag7   <- Lag(fdata$WD,   7) fdata.Reg$TEMP_lag1 <- Lag(fdata$TEMP, 1) fdata.Reg$TEMP_lag7 <- Lag(fdata$TEMP, 7) fdata.Reg$DEM_lag1  <- Lag(fdata$DEM,  1) fdata.Reg$DEM_lag7  <- Lag(fdata$DEM,  7)  # Eliminar NAs de los primeros lags fdata.Reg.tr <- na.omit(fdata.Reg)`

### 1) Entrenamiento con _cross-validation_

`set.seed(150)  ctrl_tune <- trainControl(method = "cv", number = 10,                           summaryFunction = defaultSummary,                           savePredictions = TRUE)  mlp.fit <- train(DEM ~ ., data = fdata.Reg.tr,                  method = "nnet", linout = TRUE,                  preProcess = c("center","scale"),                  tuneGrid = expand.grid(size = seq(10,20,length.out = 3),                                         decay = 10^(c(-3:0))),                  maxit = 200, trControl = ctrl_tune, metric = "RMSE")  mlp.fit ggplot(mlp.fit) + scale_x_log10() plotnet(mlp.fit$finalModel) SensAnalysisMLP(mlp.fit)  # Predicción en train y diagnóstico mlp_pred <- predict(mlp.fit, newdata = fdata.Reg.tr) PlotModelDiagnosis(fdata.Reg.tr[,-1], fdata.Reg.tr[,1], mlp_pred, together = TRUE) accuracy(fdata.Reg.tr[,1], mlp_pred)`

### 2) Modelo “pruned” (simplificado)

`set.seed(150) mlp.fit2 <- train(DEM ~ WD + DEM_lag1 + WD_lag1 + TEMP,                   data = fdata.Reg.tr, method = "nnet", linout = TRUE,                   preProcess = c("center","scale"),                   tuneGrid = expand.grid(size = seq(10,20,length.out = 3),                                          decay = 10^(c(-3:0))),                   maxit = 200, trControl = ctrl_tune, metric = "RMSE")  mlp.fit2 ggplot(mlp.fit2) + scale_x_log10() plotnet(mlp.fit2$finalModel) SensAnalysisMLP(mlp.fit2)`

### 3) _Forecast_ h = 7 (recursivo)

`# Leemos drivers de validación fdata.Reg.tv <- readxl::read_excel("DAILY_DEMAND_TV.xlsx") |> as.data.frame()  # Construimos dataframe para concatenar histórico + TV fdata.Reg.new <- fdata.Reg.tv[, c(2,3)]   # WD, TEMP fdata.Reg.new$DEM <- rep(NA, nrow(fdata.Reg.new))  # placeholder  fdata.join <- rbind(fdata[, c(2:4)], fdata.Reg.new)  # Recalcular lags sobre el conjunto ampliado fdata.join$WD_lag1   <- Lag(fdata.join$WD,   1) fdata.join$WD_lag7   <- Lag(fdata.join$WD,   7) fdata.join$TEMP_lag1 <- Lag(fdata.join$TEMP, 1) fdata.join$TEMP_lag7 <- Lag(fdata.join$TEMP, 7) fdata.join$DEM_lag1  <- Lag(fdata.join$DEM,  1) fdata.join$DEM_lag7  <- Lag(fdata.join$DEM,  7)  # Bucle recursivo tstart <- nrow(fdata) for(i in (tstart+1):(tstart+7)){   fdata.join$DEM[i] <- predict(mlp.fit, newdata = fdata.join[i,])   fdata.join$DEM_lag1 <- Lag(fdata.join$DEM, 1)   fdata.join$DEM_lag7 <- Lag(fdata.join$DEM, 7) }  # Predicciones h=7 fdata.join$DEM[(tstart+1):(tstart+7)]`

> [!warning] Buenas prácticas con MLP
> 
> - Siempre **centra/escala**.
>     
> - Usa **lags** suficientes (1 y 7 al menos por la semana).
>     
> - CV estratificado no aplica; con series temporales, evita “fugas” (aquí el _setup_ del curso usa CV simple).
>     

---

## Qué entregar (sugerencia)

1. **Breve informe** (1–2 páginas):
    
    - Qué _features_ usaste (WD, TEMP, tcold, thot, lags) y por qué.
        
    - Diagrama/figura de **no linealidad TEMP–DEM**.
        
    - **Diagnóstico** TF final (residuos, CCF) + principales coeficientes e interpretación.
        
    - **Resultados MLP** (RMSE CV, variables más influyentes via sensibilidad).
        
    - **Comparación** TF vs MLP en validación h=7 (tabla y gráfico).
        
2. **Código limpio** (`Week10.R`) con secciones: imputación, TF, _feature engineering_, MLP, _forecast_.
    
3. **Gráficos**:
    
    - Autoplot series y _facets_.
        
    - CCFs y `CheckResiduals.ICAI`.
        
    - Ajuste vs real y _forecast_ h=7 para ambos enfoques.
        

---

## Checklist de calidad

-  Imputación coherente con la estacionalidad semanal.
    
-  TF con (b,r,s) justificado por `TF.Identification.plot`.
    
-  Residuos ~ ruido blanco y **CCF(res, X)** sin picos relevantes.
    
-  _Feature engineering_ de temperatura probado (tcold/thot).
    
-  MLP con **CV** y _preProcess = center/scale_.
    
-  _Forecast_ h=7 reportado en unidades originales.
    
-  Comparación TF vs MLP en la misma ventana de validación.