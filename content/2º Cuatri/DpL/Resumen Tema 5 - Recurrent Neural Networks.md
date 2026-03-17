### I. Before RNNs
#### 1. Modelos Autorregresivos
> El material comienza con los **modelos autorregresivos**, que asumen que el valor actual puede modelarse a partir de observaciones pasadas. Se plantean dos formas de interés: modelar la probabilidad condicional del siguiente valor o su esperanza condicional. También se indica que el número de pasos temporales de entrada puede variar. $$P(x_t \mid x_{t-1}, \ldots, x_1)$ o $E[x_t \mid x_{t-1}, \ldots, x_1)$$Como ejemplo, las diapositivas presentan el modelo **AR(p)**, que usa las $p$ observaciones pasadas: $$x_t = c + \sum_{k=1}^{p} \phi_k x_{t-k} + \epsilon_t$$La ventaja que se destaca es que estos modelos son **fáciles de ajustar** porque trabajan con una **ventana fija de entradas**. La limitación señalada en el material es que suelen ser **demasiado simples para datos complejos**.
#### 2. Modelos Autorregresivos Latentes
> Para capturar dependencias más complejas, el material introduce un **estado oculto** $h_t$, cuya función es **capturar o resumir información del pasado**. La idea es que este estado intermedio haga al modelo más expresivo que un autorregresivo clásico.
> Se propone la siguiente forma de modelado: $$h_t = f(h_{t-1}, x_{t-1}; \theta), \qquad \hat{x}_t = g(h_t; \theta)$$donde $f$ y $g$ son funciones tipo red neuronal. El diagrama del material muestra precisamente esa cadena temporal: cada entrada alimenta un estado oculto, y cada estado oculto produce una salida, de modo que la información relevante del pasado queda resumida en la secuencia de estados $h_{t-1}, h_t, h_{t+1}$.
#### 3. Modelos de Secuencia y Orden de Decodificación
> El objetivo general pasa a ser modelar una **secuencia completa**: $$P(x_1, x_2, \ldots, x_T)$$El material factoriza esta probabilidad con la **regla de la cadena**: $$P(x_1, \ldots, x_T) = P(x_1)\prod_{t=2}^{T} P(x_t \mid x_{t-1}, \ldots, x_1)$$La idea central es tratar los datos como una **secuencia en la que el orden importa**, por ejemplo en lenguaje o en series temporales. También se indica que una serie temporal puede verse como una ocurrencia de estas probabilidades para cada instante $t$.
> 
> En el caso del **modelado del lenguaje**, las diapositivas remarcan que normalmente se predice **de izquierda a derecha**: $$P(x_1, \ldots, x_T) = P(x_1)\prod_{t=2}^{T} P(x_t \mid x_1, \ldots, x_{t-1})$$La justificación que aparece en el material es la **estructura causal**: los eventos futuros no pueden influir en el pasado. Además, se afirma que suele haber mayor capacidad predictiva cuando se predice el **siguiente** elemento, en vez de posiciones arbitrarias. Se menciona explícitamente que **RNNs** y **Transformers con causal masking** implementan esta factorización izquierda-a-derecha, y a veces también derecha-a-izquierda.
#### 4. Modelos de Markov
> Las diapositivas presentan después la **hipótesis de Markov**, según la cual el futuro es condicionalmente independiente del pasado dado el historial más reciente. En su forma más simple, esto se aproxima por: $$P(x_t \mid x_{t-1}, \ldots, x_1) \approx P(x_t \mid x_{t-1})$$A partir de esta hipótesis se obtienen modelos más simples, como las **cadenas de Markov**: $$P(x_1, \ldots, x_T) = P(x_1)\prod_{t=2}^{T} P(x_t \mid x_{t-1})$$El propio material advierte que esta simplificación suele ser **demasiado restrictiva** cuando importan dependencias de largo alcance. Como extensión, se mencionan los **Hidden Markov Models (HMMs)**, que añaden un **estado no observado** para abordar parcialmente esos efectos de mayor alcance.
#### 5. Predicción Temporal a Distintos Horizontes
> Una primera tarea es la **predicción a un paso**: estimar $\hat{x}_{t+1}$ a partir de $x_t, x_{t-1}, \ldots$. El material la escribe como: $$\hat{x}_{t+1} = f(x_t, x_{t-1}, \ldots)$$La figura correspondiente compara las predicciones con las etiquetas reales, mostrando visualmente el caso de **1-step prediction**.
> 
> Para horizontes más largos, las diapositivas introducen la **predicción recursiva** o **K-ahead prediction**: una vez obtenida $\hat{x}_{t+1}$, esa salida se reutiliza como nueva entrada para predecir más allá. $$\hat{x}_{t+k} = f(\hat{x}_{t+k-1}, \ldots, x_t)$$El punto importante del material es que este enfoque puede generar **acumulación de errores** a medida que crece $k$. En la comparación entre horizontes de **1, 4, 16 y 64 pasos**, se indica que:
> - En **1-step**, la predicción sigue bastante bien la señal real.
> - En **4-step** y **16-step**, aparecen retraso y suavizado.
> - En **64-step**, las desviaciones acumuladas son ya grandes.
> La idea que dejan las figuras es que cuanto mayor es el horizonte, peor tiende a ser la precisión.
#### 6. Interpolación vs. Extrapolación
> El material diferencia entre **interpolación** y **extrapolación**. En interpolación, el modelo está normalmente mejor respaldado por ejemplos de entrenamiento, por lo que hay menos riesgo de grandes desviaciones si los datos están bien muestreados.
> En cambio, en extrapolación hay **más incertidumbre** y el modelo puede generalizar peor. Las diapositivas remarcan que, si el patrón subyacente cambia, los errores pueden ser grandes.
#### 7. Modelos de Lenguaje Antes de las RNNs
> En la parte de lenguaje, el material define un **language model** como un modelo que asigna una probabilidad a una secuencia de palabras: $$P(x_1, x_2, \ldots, x_T) = \prod_{t=1}^{T} P(x_t \mid x_1, \ldots, x_{t-1})$$Se indica que esto permite medir cuán probable es una oración bajo el modelo y que se usa en tareas como **text generation**, **speech recognition** y **machine translation**.
> 
> A continuación aparecen los **n-grams**, que aproximan la probabilidad condicional mirando solo las $n-1$ palabras anteriores: $$P(x_t \mid x_{t-1}, x_{t-2}, \ldots, x_1) \approx P(x_t \mid x_{t-1}, \ldots, x_{t-n+1})$$Para una secuencia de cuatro palabras $(x_1, x_2, x_3, x_4)$, el material da estos ejemplos:
> - **Unigram**: $P(x_1, x_2, x_3, x_4) = P(x_1)P(x_2)P(x_3)P(x_4)$
> - **Bigram**: $P(x_1, x_2, x_3, x_4) = P(x_1)P(x_2 \mid x_1)P(x_3 \mid x_2)P(x_4 \mid x_3)$
> - **Trigram**: $P(x_1, x_2, x_3, x_4) = P(x_1)P(x_2 \mid x_1)P(x_3 \mid x_1, x_2)P(x_4 \mid x_2, x_3)$
> 
> La conclusión explícita del material es que valores mayores de $n$ permiten capturar **más contexto**, pero aumentan el riesgo de **data sparsity**.
> 
> Para estimar probabilidades, las diapositivas usan **frecuencias del corpus**. El ejemplo dado es: $$\hat{P}(\text{learning} \mid \text{deep}) = \dfrac{n(\text{deep}, \text{learning})}{n(\text{deep})}$$Se aclara que esto es, esencialmente, una **estimación por frecuencia relativa**. El problema señalado es la aparición de **conteos cero** cuando los pares de palabras, o los n-grams en general, son raros o no se han visto.
> 
> Para evitar probabilidades nulas, el material introduce el **Laplace (Add-$\Large \epsilon$) Smoothing**: $$\hat{P}(x) = \dfrac{n(x) + \epsilon_1/m}{n + \epsilon_1}, \qquad \hat{P}(x' \mid x) = \dfrac{n(x,x') + \epsilon_2 \hat{P}(x')}{n(x) + \epsilon_2}$$La intuición que dan las diapositivas es **hacer como si cada evento hubiera sido observado unas pocas veces extra**. También se nombran métodos más sofisticados, como **Kneser-Ney** y **Good-Turing**.
#### 8. Perplexity y Preparación de Secuencias
> El criterio de evaluación presentado es la **perplexity**, que mide lo bien que un modelo probabilístico predice una muestra: $$\text{Perplexity} = \exp\left(-\dfrac{1}{n}\sum_{t=1}^{n}\log P(x_t \mid x_1, \ldots, x_{t-1})\right)$$El material indica de forma explícita que una **perplexity más baja** significa que el modelo está **más seguro** de la secuencia. Para ilustrarlo, compara frases más probables y menos probables, como “It is raining outside” frente a secuencias claramente anómalas.
> 
> Además, las diapositivas proponen esta interpretación de valores:
> - **Modelo perfecto**: $\text{Perplexity} = 1$
> - **Modelo bueno**: $\text{Perplexity} \approx 20 - 100$
> - **Modelo aleatorio**: $\text{Perplexity} = |V|$ donde $|V|$ es el tamaño del vocabulario
> - **Peor caso**: $\text{Perplexity} \to \infty$
> 
> La justificación que aparece en el material es que un modelo perfecto asigna probabilidad 1 a la secuencia correcta, mientras que un modelo que asigna probabilidad 0 provoca log-probabilidad de $-\infty$ y, por tanto, perplexity infinita.
> 
> Por último, el material explica una estrategia habitual para **particionar secuencias** al entrenar:
> - **Inputs**: las palabras o tokens en posiciones $[t, t+1, \ldots]$
> - **Targets**: la siguiente palabra o token en cada posición, $[t+1, \ldots]$
> 
> Se indica también que son comunes las **ventanas solapadas** o **sliding windows** para entrenar tanto modelos n-gram como modelos neuronales. La figura final lo ilustra con una secuencia desplazada entre entrada y objetivo.

### II. Introduction to RNNs
#### 1. Inputs
> Rellenar


### III. Backpropagation Through Time 
#### 1. Idea
> Rellenar
#### 2. Explicación en Detalle



### IV. First Types of RNNs
#### 1. Bidirectional RNNs
> Rellenar
#### 2. Encoder - Decoder
> Rellenar
#### 3. Decoding Strategies
> Rellenar
### V. Modern RNNs
#### 1. Long Short-Term Memory (LSTM)
> Rellenar
#### 2. Gated Recurrent Units (GRU)
> Rellenar