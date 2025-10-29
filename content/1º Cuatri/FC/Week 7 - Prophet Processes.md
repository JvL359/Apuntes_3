### I. Previos
#### 1. Carga de Librerías
> Añadimos **prophet** (modelo aditivo con tendencia + estacionalidades + festivos), junto con utilidades de EDA y validación.
```r
# Librerías
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
# Setear el Directorio
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
```

### II. Datos
#### 1. Carga y Comprobaciones Iniciales
> Leemos el CSV y dejamos la columna `date` en clase **`Date`** para poder operar con calendarios. Ordenamos por fecha y verificamos la **integridad temporal**:
> 	- **Huecos**: construimos una secuencia diaria completa `date_range` y comparamos con las fechas reales. Si `setdiff(...)` devuelve algo distinto de `integer(0)`, faltan días → habrá que imputar/descartar antes de modelar.
> 	- **NAs**: comprobamos valores perdidos en la variable objetivo `output`. Prophet no trabaja con `y` faltante; los registros con `NA` deben tratarse.
> 	- **Duplicados**: dos filas con la misma fecha distorsionan la tendencia/estacionalidad; conviene agregarlas (p. ej., media) o eliminar.
> 	- **EDA rápida**: con `ggtsdisplay(output)` inspeccionamos **serie + ACF/PACF** hasta 100 lags. En datos diarios suelen aparecer patrones semanales (lag ≈ 7) y mensuales (~30). Esto nos guía sobre qué estacionalidades activar más adelante.
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
> La división debe respetar el **orden temporal** (nada de barajar). Reservamos los **últimos 182 días** (~6 meses) para **validación**:
> 	- `train_data` se usa para **ajustar** y seleccionar hiperparámetros.
> 	- `test_data` se usa para **evaluar** el rendimiento fuera de muestra.  
> Esta separación es coherente con el horizonte de predicción que luego usaremos con Prophet y evita **fugas de información** (data leakage).
```r
# Split train/test
h_test <- 182
train_data <- fdata[1:(nrow(fdata) - h_test), ]
test_data  <- fdata[(nrow(fdata) - h_test + 1):nrow(fdata), ]
```
#### 3. Formato Prophet: ds, y, regresores
> Prophet exige un `data.frame` con:
> 	- **`ds`**: fecha (tipo `Date` o `POSIXct`) ordenada y sin duplicados.
> 	- **`y`**: la variable objetivo.
> 	- **Regresores externos**: columnas adicionales (`x1`, `x2`, …). Importante: además de incluirlas aquí, **hay que declararlas en el modelo** con `add_regressor("x1")`, `add_regressor("x2")`.  
> Reglas prácticas: evita `NA` en los regresores, mantén las mismas unidades/escala que en entrenamiento y recuerda que **para predecir** necesitarás proporcionar sus **valores futuros** en el `future_df`.
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
> **Prophet** es un modelo **aditivo descomponible**, diseñado para series con **tendencias no lineales**, **estacionalidades múltiples** y posibles **rupturas estructurales**. Su forma general es:
> 	$y_t = g(t) + s(t) + h(t) + \varepsilon_t$​
> donde cada término representa un componente interpretable:
> 	- **Tendencia** \( g(t) \): captura el crecimiento o decrecimiento a largo plazo.  
> 	  Puede ser:
> 		1) _Lineal por tramos_ (piecewise linear), donde la pendiente cambia en los llamados **changepoints**.
> 		2) _Logística_, si se define una **capacidad máxima (`cap`)** y opcionalmente una mínima (`floor`), útil para procesos que se estabilizan.
> 	- **Estacionalidad**  $s(t)$ : modela patrones **periódicos** (anual, semanal, diario o personalizados). Prophet usa **series de Fourier** para representar estas oscilaciones. La complejidad de cada estacionalidad se controla mediante el **orden de Fourier**                        (`fourier.order`): valores altos permiten mayor flexibilidad, pero también riesgo de sobreajuste.
> 	- **Festivos o eventos especiales**  $h(t)$: se definen como una tabla con fechas y ventanas de influencia (campos `lower_window`, `upper_window`). Sirven para capturar efectos no periódicos pero recurrentes (p. ej. campañas, vacaciones, huelgas…).
> 	- **Término de error** $\varepsilon_t$: representa la variación no explicada; se asume ruido blanco independiente.
> 
> Prophet ajusta todos los componentes **por máxima verosimilitud** y permite cuantificar la **incertidumbre** mediante intervalos.  
> La flexibilidad de la tendencia se controla con el hiperparámetro `changepoint.prior.scale`:
> 	- valores **bajos** → curva más rígida (suaviza cambios),
> 	- valores **altos** → curva más adaptable (detecta rupturas).
> En conjunto, Prophet combina la **interpretabilidad clásica** de los modelos de descomposición con la **automatización** de un algoritmo moderno de pronóstico, lo que lo hace especialmente útil en entornos con estacionalidades múltiples y series largas con cambios de tendencia.

### IV. Modelado paso a paso
#### 1) Modelo sin Estacionalidad (solo tendencia)
> Comenzamos con la versión más simple de Prophet: sin estacionalidades ni eventos, solo la **tendencia global**. El modelo identifica automáticamente **cambios en la pendiente** (changepoints) y estima una curva suavizada que sigue la evolución a largo plazo. Sirve como línea base para comparar con versiones más complejas.
```r
# 1. Instanciar el Modelo
model1 <- prophet(
  yearly.seasonality = FALSE,
  weekly.seasonality = FALSE,
  daily.seasonality  = FALSE
) %>% fit.prophet(prophet_df)

# 2. Predicción del Modelo
pred1 <- predict(model1, prophet_df)

# 3. Curva + Changepoints
p1 <- plot(model1, pred1) + add_changepoints_to_plot(model1)
try(ggplotly(p1))

# 4. Componentes y Residuos
prophet_plot_components(model1, pred1)
resid1 <- prophet_df$y - pred1$yhat
CheckResiduals.ICAI(resid1, lags = 36)
```
#### 2) Tendencia con Changepoints Definidos
> Aquí forzamos los **changepoints** en fechas específicas donde sabemos que hubo rupturas o saltos estructurales. Prophet ajusta la tendencia con **pendientes diferentes** antes y después de cada punto definido. Es útil cuando el analista conoce momentos concretos de cambio (p. ej. políticas, reformas, eventos externos).
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

# 3. Curva + Changepoints
plot(model2, pred2) + add_changepoints_to_plot(model2)

# 4. Componentes y Residuos
prophet_plot_components(model2, pred2)
resid2 <- prophet_df$y - pred2$yhat
CheckResiduals.ICAI(resid2, lags = 36)
```
#### 3) Añadir Estacionalidad Anual y Semanal
> Incorporamos los **patrones periódicos** más comunes: la **variación anual** (efecto de estaciones o ciclos largos) y la **semanal** (efecto de días laborables vs. fines de semana). Prophet usa funciones de **Fourier** para estimar estas oscilaciones. El resultado es una mejor captura de los movimientos cíclicos regulares del sistema.
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

# 3. Curva + Changepoints
plot(model3, pred3) + add_changepoints_to_plot(model3)

# 4. Componentes y Residuos
prophet_plot_components(model3, pred3)
resid3 <- prophet_df$y - pred3$yhat
CheckResiduals.ICAI(resid3, lags = 36)
```
#### 4) Estacionalidad Mensual Personalizada
> Añadimos una estacionalidad **adicional de periodo ≈ 30.5 días**, útil para fenómenos con ciclo mensual (p. ej., consumo, facturación, clima). Con `fourier.order = 3` limitamos la complejidad del patrón para evitar sobreajuste. Este componente complementa los patrones anual y semanal, mejorando la precisión a corto plazo.
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

# 3. Curva + Changepoints
plot(model4, pred4) + add_changepoints_to_plot(model4) |> ggplotly()

# 4. Componentes y Residuos
prophet_plot_components(model4, pred4)
resid4 <- prophet_df$y - pred4$yhat
CheckResiduals.ICAI(resid4, lags = 36)
```
#### 5) Añadir Regresores Externos
> Incorporamos variables explicativas (`x1`, `x2`) que podrían influir en la salida —por ejemplo, temperatura, tráfico o indicadores externos. Prophet las trata como **efectos lineales adicionales**, ajustando su contribución junto con la tendencia y estacionalidad. Tras el ajuste, comprobamos los residuos y detectamos posibles **outliers** o fechas atípicas que el modelo no explica bien.
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

# 3. Curva + Changepoints
plot(model5, pred5) + add_changepoints_to_plot(model5) |> ggplotly()

# 4. Componentes y Residuos
prophet_plot_components(model5, pred5)
resid5 <- prophet_df$y - pred5$yhat
CheckResiduals.ICAI(resid5, lags = 36)

# 5. Detección simple de outliers de residuo (> 3 sd)
out_idx <- which(abs(resid5) > (mean(resid5) + 3*sd(resid5)))
fdata$date[out_idx]
```
#### 6) Festivos (ventana con ±días)
> Añadimos el efecto de **festivos o eventos especiales**, definidos con sus **ventanas de influencia** (`lower_window`, `upper_window`). En este ejemplo se simula **Navidad**, afectando desde dos días antes hasta tres días después. Prophet crea variables dummy para cada fecha y estima su impacto, mejorando la capacidad del modelo para capturar picos o caídas estacionales no periódicas.
```r
# 0. Determinar Festivos
holidays <- data.frame(
  holiday = 'christmas',
  ds = seq.Date(as.Date("2015-12-24"), as.Date("2022-12-24"), by = "year"),
  lower_window = 2,
  upper_window = 3
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

# 3. Curva + Changepoints
plot(model6, pred6) + add_changepoints_to_plot(model6) |> ggplotly()

# 4. Componentes y Residuos
prophet_plot_components(model6, pred6)
resid6 <- prophet_df$y - pred6$yhat
CheckResiduals.ICAI(resid6, lags = 36)
```
#### 7) Ajuste Manual de Hiperparámetros
> Prophet permite controlar la **complejidad de las estacionalidades** modificando directamente los **órdenes de Fourier** (`yearly.seasonality = 3`, `weekly.seasonality = 3`). Esto sirve para **suavizar** patrones demasiado flexibles o reducir el riesgo de sobreajuste. Es un ajuste fino que busca equilibrio entre precisión y estabilidad en los pronósticos.
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

# 3. Curva + Changepoints
plot(model7, pred7) + add_changepoints_to_plot(model7) |> ggplotly()

# 4. Componentes y Residuos
prophet_plot_components(model7, pred7)
resid7 <- prophet_df$y - pred7$yhat
CheckResiduals.ICAI(resid7, lags = 36)
```
#### 8) Grid search con validación cruzada temporal
> En esta fase realizamos una **búsqueda en rejilla (grid search)** para encontrar la combinación óptima de **órdenes de Fourier** en las estacionalidades anual, semanal y mensual. 
> Prophet no tiene un optimizador automático para estos parámetros, así que iteramos sobre todas las combinaciones posibles y medimos el rendimiento mediante **validación cruzada temporal** (`cross_validation`).  
> Este método divide la serie en ventanas deslizantes respetando la secuencia temporal: se entrena en los primeros años, se evalúa en horizontes futuros y se repite.  
> Para cada modelo se calculan métricas de error como **MAPE** y **RMSE** usando `performance_metrics()`. 
> Finalmente, se selecciona la configuración con el menor error (en este caso, el mínimo MAPE) y se entrena el **modelo final** con esos hiperparámetros.  
> Esta práctica evita el sobreajuste y asegura que el modelo sea **robusto y generalizable** en diferentes períodos de la serie.
```r
# 1. Grid de Hiperparámetros
param_grid <- expand.grid(
  yearly_fourier_order = c(1, 3, 5),
  weekly_fourier_order = c(1, 3, 5),
  monthly_fourier_order = c(1, 3, 5)
)

# 2. Cross Validation de los Hiperparámetros
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

# 3. Selección de los Mejores (aquí por MAPE; podrías elegir RMSE)
best_params <- cv_results %>% filter(MAPE == min(MAPE))
best_params

# 4. Modelo final con los Mejores Hiperparámetros
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

# 5. Predicción del Modelo
pred8 <- predict(model8, prophet_df)

# 6. Curva + Changepoints
plot(model8, pred8) + add_changepoints_to_plot(model8) |> ggplotly()

# 7. Componentes y Residuos
prophet_plot_components(model8, pred8)
resid8 <- prophet_df$y - pred8$yhat
CheckResiduals.ICAI(resid8, lags = 36)
```

### V. Pronóstico Final y Validación del Modelo
> Con el modelo óptimo (`model8`) generamos el **dataframe futuro** (`make_future_dataframe`) indicando el número de días a pronosticar y añadiendo los **valores futuros de los regresores externos** (`x1`, `x2`).  
> Luego realizamos las **predicciones** y visualizamos los resultados comparando los **valores reales** (en rojo) con los **valores estimados por Prophet**.  
> Los **componentes** muestran cómo cada parte del modelo (tendencia, estacionalidad y festivos) contribuye al pronóstico total.  
> Finalmente, analizamos los **residuos de test** para verificar que se comporten como ruido blanco y calculamos las métricas de **precisión** (`accuracy`) tanto en entrenamiento como en test, comprobando la capacidad predictiva y la estabilidad del modelo fuera de muestra.
```r
# 0. Crear el DataFrame de las Predicciones
prophet_df_test <- make_future_dataframe(
    model8, 
    periods = 182, # Number of samples to forecast
    freq = 'days', # Frequency of samples to forecast
    include_history = FALSE # indicate if previous dates should be included
    ) 
prophet_df_test$x1 <- test_data$input1
prophet_df_test$x2 <- test_data$input2

# 2. Realizar las Predicciones
predictions_test <- predict(model8, prophet_df_test)

# 3. Valor Real vs Valor Predicho
p <- plot(model8, predictions_test) + 
    geom_point(data=test_data, aes(x = prophet_df_test$ds, y = output), 
               color = "red", alpha = 0.5)
ggplotly(p)

# 4. Componentes y Residuos
prophet_plot_components(model8, predictions_test)
residuals_test <- test_data$output - predictions_test$yhat
CheckResiduals.ICAI(residuals_test, 36)

# 5. Evaluación del model
accuracy(predictions$yhat, train_data$output)
accuracy(predictions_test$yhat, test_data$output)
```

### VI. Comentarios Finales
> [!summary]  Notas y buenas prácticas
> - **Escala de `y` y regresores**: si hay magnitudes muy distintas o outliers, considera transformaciones/robustez.
> - **Estacionalidad creciente con el nivel**: probar `seasonality.mode`: con `"multiplicative"`.
> - **Tendencia logística** (`growth = "logistic"`): usa `cap` (y opcionalmente `floor`) para asíntotas.
> - **Changepoints**: ajusta `changepoint.prior.scale` (más alto → mayor flexibilidad) o fija fechas.
> - **Festivos**: define ventanas adecuadas (p. ej., `upper_window` > 0 si el efecto dura varios días).
> - **Entrenamiento repetido**: usa `cross_validation()` para evitar _overfitting_ de Fourier.
> - **Reproductibilidad**: fija `seed` si haces _grid search_ extensivo. 

> [!summary] Checklist 
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

Los apuntes continúan en [[Week 8 - Dynamic Regression Seasonal Models]]