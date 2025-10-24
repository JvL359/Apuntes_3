### I. Previos
#### 1. Carga de Librerías
> Añadimos **prophet** (modelo aditivo con tendencia + estacionalidades + festivos), junto con utilidades de EDA y validación.
```r
library(tseries)
library(fpp2)
library(prophet)   # https://facebook.github.io/prophet
library(MLTools)   # CheckResiduals.ICAI, utilidades curso
library(plotly)    # Gráficos interactivos
library(lubridate) # Fechas
library(dplyr)     # Manipulación de data frames (prophet_df)
```
#### 2. Directorio
> Igual que en semanas previas. 
```r
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
```

### II. Datos
#### 1. Carga y Comprobaciones iniciales
> Leemos el CSV, ordenamos, revisamos **gaps**, **duplicados** y **NAs**.
```r
# 1. Carga
data_path <- "prophet_data.csv"
fdata <- read.table(data_path, sep = ";", header = TRUE)
head(fdata)

# 2. Columna de fecha al tipo Date
fdata$date <- as.Date(fdata$date)

# 3. Orden y control de huecos/duplicados
fdata <- fdata |> arrange(date)
date_range <- seq(min(fdata$date), max(fdata$date), by = "day")
setdiff(date_range, fdata$date)        # días ausentes
sum(is.na(fdata$output))               # NAs en output
length(fdata$date) - length(unique(fdata$date))  # duplicados

# 4. Exploración de la serie de salida
ggtsdisplay(fdata$output, lag.max = 100)
```
#### 2. División en Train/Test
> Reservamos **182 días** para validación ( ~6 meses) respetando la estructura temporal.
```r
# Split train/test
h_test <- 182
train_data <- fdata[1:(nrow(fdata) - h_test), ]
test_data  <- fdata[(nrow(fdata) - h_test + 1):nrow(fdata), ]
```
#### 3. Formato Prophet: ds, y, regresores
> Prophet requiere `ds` (fecha) y `y` (objetivo). Los regresores externos van como columnas extra y luego se declaran con `add_regressor()`.
```r
# DataFrame de Prophet
prophet_df <- data.frame(
  ds = train_data$date,     # fecha
  y  = train_data$output,   # variable objetivo
  x1 = train_data$input1,   # regresor 1
  x2 = train_data$input2    # regresor 2
)
```

### III. Recordatorio rápido de Prophet (idea)
> Modelo **aditivo**: $y_t = g(t) + s(t) + h(t) + \varepsilon_t$.
> - **Tendencia** `g(t)`: lineal por tramos o logística con _changepoints_.
> - **Estacionalidad** `s(t)`: anual/semanal/diaria (o personalizadas) vía series de Fourier.
> - **Festivos/eventos** `h(t)`: matriz de dummies con ventanas +/- días.
> - Incertidumbre y control de _changepoints_ mediante hiperparámetros.

### IV. Modelado paso a paso
#### 1) Modelo sin estacionalidad (solo tendencia)
> Punto de partida: desactivamos estacionalidades; Prophet seguirá aprendiendo tendencia con _changepoints_ automáticos.
```r
# 1. Instanciar el Modelo
model1 <- prophet(
  yearly.seasonality = FALSE,
  weekly.seasonality = FALSE,
  daily.seasonality  = FALSE
) %>% fit.prophet(prophet_df)

# 2. Predicción del Modelo
pred1 <- predict(model1, prophet_df)

# 3. Curva + Changepoints Interactiva
p1 <- plot(model1, pred1) + add_changepoints_to_plot(model1)
try(ggplotly(p1))

# 4. Componentes y Residuos
prophet_plot_components(model1, pred1)
resid1 <- prophet_df$y - pred1$yhat
CheckResiduals.ICAI(resid1, lags = 36)
```
#### 2) Tendencia con changepoints definidos por el analista
> Útil cuando conocemos rupturas (cambios de política, producto, etc.).
```r
# 0. Determinar los Changepoints
changepoints <- as.Date(c("2017-01-01","2019-06-01","2022-01-01"))

# 1. Instanciar el Modelo
model2 <- prophet(
  yearly.seasonality = FALSE,
  weekly.seasonality = FALSE,
  daily.seasonality  = FALSE,
  changepoints = changepoints
) %>% fit.prophet(prophet_df)

# 2. Predicción del Modelo
pred2 <- predict(model2, prophet_df)

# 3. Curva + Changepoints Interactiva
plot(model2, pred2) + add_changepoints_to_plot(model2)

# 4. Componentes y Residuos
prophet_plot_components(model2, pred2)
resid2 <- prophet_df$y - pred2$yhat
CheckResiduals.ICAI(resid2, lags = 36)
```
#### 3) Añadir estacionalidad anual y semanal
```r
# 1. Instanciar el Modelo
model3 <- prophet(
  yearly.seasonality = TRUE,
  weekly.seasonality = TRUE,
  daily.seasonality  = FALSE,
  changepoints = changepoints
) %>% fit.prophet(prophet_df)

# 2. Predicción del Modelo
pred3 <- predict(model3, prophet_df)

# 3. Curva + Changepoints Interactiva
plot(model3, pred3) + add_changepoints_to_plot(model3)

# 4. Componentes y Residuos
prophet_plot_components(model3, pred3)
resid3 <- prophet_df$y - pred3$yhat
CheckResiduals.ICAI(resid3, lags = 36)
```
#### 4) Estacionalidad **mensual** (personalizada)
> Periodo ~ **30.5 días** con orden de Fourier moderado.
```r
# 1. Instanciar el Modelo
model4 <- prophet(
  yearly.seasonality = TRUE,
  weekly.seasonality = TRUE,
  daily.seasonality  = FALSE,
  changepoints = changepoints
) %>% add_seasonality(name = "monthly", period = 30.5, fourier.order = 3)
  %>% fit.prophet(prophet_df)
  
# 2. Predicción del Modelo
pred4 <- predict(model4, prophet_df)

# 3. Curva + Changepoints Interactiva
plot(model4, pred4) |> ggplotly()

# 4. Componentes y Residuos
prophet_plot_components(model4, pred4)
resid4 <- prophet_df$y - pred4$yhat
CheckResiduals.ICAI(resid4, lags = 36)
```
#### 5) Añadir regresores externos
> Antes, revisa su estructura temporal.
```r
# 0. ACF/PACF de los regresores
ggtsdisplay(fdata$input1, lag.max = 36)
ggtsdisplay(fdata$input2, lag.max = 36)

# 1. Instanciar el Modelo
model5 <- prophet(
  yearly.seasonality = TRUE,
  weekly.seasonality = TRUE,
  daily.seasonality  = FALSE,
  changepoints = changepoints
) %>% add_seasonality(name = "monthly", period = 30.5, fourier.order = 5)
  %>% add_regressor("x1") %>% add_regressor("x2")
  %>% fit.prophet(prophet_df)

# 2. Predicción del Modelo
pred5 <- predict(model5, prophet_df)

# 3. Curva + Changepoints Interactiva
plot(model5, pred5) |> ggplotly()

# 4. Componentes y Residuos
prophet_plot_components(model5, pred5)
resid5 <- prophet_df$y - pred5$yhat
CheckResiduals.ICAI(resid5, lags = 36)

# 5. Detección simple de outliers de residuo (> 3 sd)
out_idx <- which(abs(resid5) > (mean(resid5) + 3*sd(resid5)))
fdata$date[out_idx]
```
#### 6) Festivos (ventanas ±días)
> Los festivos actúan como dummies con ventana. Aquí creamos una Navidad sintética.
```r
# 0. Determinar Festivos
holidays <- data.frame(
  holiday = 'christmas',
  ds = seq.Date(as.Date("2015-12-24"), as.Date("2022-12-24"), by = "year"),
  lower_window = 0,
  upper_window = 5
)

# 1. Instanciar el Modelo
model6 <- prophet(
  yearly.seasonality = TRUE,
  weekly.seasonality = TRUE,
  daily.seasonality  = FALSE,
  changepoints = changepoints,
  holidays = holidays
) %>% add_seasonality(name = 'monthly', period = 30.5, fourier.order = 5)
  %>% add_regressor('x1') %>% add_regressor('x2')
  %>% fit.prophet(prophet_df)

# 2. Predicción del Modelo
pred6 <- predict(model6, prophet_df)

# 3. Curva + Changepoints Interactiva
plot(model6, pred6) |> ggplotly()

# 4. Componentes y Residuos
prophet_plot_components(model6, pred6)
resid6 <- prophet_df$y - pred6$yhat
CheckResiduals.ICAI(resid6, lags = 36)
```
#### 7) Ajuste manual de hiperparámetros
> En Prophet, pasar un **entero** en `yearly.seasonality`/`weekly.seasonality` indica el **orden de Fourier**.
```r
# 1. Instanciar el Modelo
model7 <- prophet(
  yearly.seasonality = 3,
  weekly.seasonality = 3,
  daily.seasonality  = FALSE,
  changepoints = changepoints,
  holidays = holidays
) %>% add_seasonality(name = 'monthly', period = 30.5, fourier.order = 5)
  %>% add_regressor('x1') %>% add_regressor('x2')
  %>% fit.prophet(prophet_df)

# 2. Predicción del Modelo
pred7 <- predict(model7, prophet_df)

# 3. Curva + Changepoints Interactiva
plot(model7, pred7) + add_changepoints_to_plot(model7) |> ggplotly()

# 4. Componentes y Residuos
prophet_plot_components(model7, pred7)
resid7 <- prophet_df$y - pred7$yhat
CheckResiduals.ICAI(resid7, lags = 36)
```
#### 8) Grid search con validación cruzada temporal
> Exploramos órdenes de Fourier (anual/semanal/mensual) y evaluamos con `cross_validation()` + `performance_metrics()`.
```r
param_grid <- expand.grid(
  yearly_fourier_order = c(1, 3, 5),
  weekly_fourier_order = c(1, 3, 5),
  monthly_fourier_order = c(1, 3, 5)
)

cv_results <- data.frame()
for (i in 1:nrow(param_grid)) {
  params <- param_grid[i, ]
  tmp <- prophet(
    yearly.seasonality = params$yearly_fourier_order,
    weekly.seasonality = params$weekly_fourier_order,
    daily.seasonality  = FALSE,
    changepoints = changepoints,
    holidays = holidays
  ) %>% add_seasonality(name = 'monthly', period = 30.5,
                        fourier.order = params$monthly_fourier_order)
    %>% add_regressor('x1') %>% add_regressor('x2')
    %>% fit.prophet(prophet_df)
  
  cv <- cross_validation(tmp, initial = 365*2, period = 180,
                         horizon = 365, units = 'days')
  perf <- performance_metrics(cv)
  cv_results <- rbind(cv_results,
    data.frame(
      yearly_fourier_order = params$yearly_fourier_order,
      weekly_fourier_order = params$weekly_fourier_order,
      monthly_fourier_order = params$monthly_fourier_order,
      MAPE = perf$mape[1], RMSE = perf$rmse[1]
    )
  )
}
cv_results

# Selección (aquí por MAPE; podrías elegir RMSE)
best_params <- cv_results %>% filter(MAPE == min(MAPE))
best_params

# Modelo final con los mejores hiperparámetros
model8 <- prophet(
  yearly.seasonality = best_params$yearly_fourier_order[1],
  weekly.seasonality = best_params$weekly_fourier_order[1],
  daily.seasonality  = FALSE,
  changepoints = changepoints,
  holidays = holidays
) %>% add_seasonality(name = 'monthly', period = 30.5,
                      fourier.order = best_params$monthly_fourier_order[1])
  %>% add_regressor('x1') %>% add_regressor('x2')
  %>% fit.prophet(prophet_df)

pred8 <- predict(model8, prophet_df)
plot(model8, pred8) |> ggplotly()
prophet_plot_components(model8, pred8)
resid8 <- prophet_df$y - pred8$yhat
CheckResiduals.ICAI(resid8, lags = 36)
```

### V. Pronóstico y validación final
#### 1. Future dataframe con regresores
> Para pronosticar, hay que proporcionar valores futuros de los **regresores**.
```r
future_df <- make_future_dataframe(model8, periods = h_test, freq = 'days',
                                   include_history = FALSE)
future_df$x1 <- test_data$input1
future_df$x2 <- test_data$input2

pred_test <- predict(model8, future_df)

# Visual: pronóstico vs datos reales (rojo)
plot(model8, pred_test) +
  geom_point(data = test_data, aes(x = future_df$ds, y = output),
             color = "red", alpha = 0.5) |> ggplotly()

# Componentes del pronóstico
prophet_plot_components(model8, pred_test)
```
#### 2. Evaluación (train y test)
```r
# Residuos de test y diagnóstico
resid_test <- test_data$output - pred_test$yhat
CheckResiduals.ICAI(resid_test, lags = 36)

# Métricas
accuracy(pred8$yhat, train_data$output)
accuracy(pred_test$yhat, test_data$output)
```

### VI. Notas y buenas prácticas

- **Escala de `y` y regresores**: si hay magnitudes muy distintas o outliers, considera transformaciones/robustez.
    
- **`seasonality.mode`**: prueba `"multiplicative"` cuando la estacionalidad crece con el nivel.
    
- **Tendencia logística** (`growth = "logistic"`): usa `cap` (y opcionalmente `floor`) para asintotas.
    
- **Changepoints**: ajusta `changepoint.prior.scale` (más alto → mayor flexibilidad) o fija fechas.
    
- **Festivos**: define ventanas adecuadas (p. ej., `upper_window` > 0 si el efecto dura varios días).
    
- **Entrenamiento repetido**: usa `cross_validation()` para evitar _overfitting_ de Fourier.
    
- **Reproductibilidad**: fija `seed` si haces _grid search_ extensivo.
    

> **Checklist**
> 
> -  ¿Residuos ≈ ruido blanco?
>     
> -  ¿Componentes (tendencia/seasonal/holiday) tienen sentido de negocio?
>     
> -  ¿Regresores futuros disponibles en `future_df`?
>     
> -  ¿Hiperparámetros validados vía CV?
>     
> -  ¿Modo aditivo vs multiplicativo comprobado?
>