### I. Before RNNs
#### 1. Modelos Autorregresivos
> Los modelos autorregresivos asumen que el valor actual puede modelarse a partir de los valores pasados, es decir, se trabaja con distribuciones del tipo $$P(x_t \mid x_{t-1}, \ldots, x_1)$$o con su esperanza condicional $$\mathbb{E}[x_t \mid x_{t-1}, \ldots, x_1]$$En general, pueden usar un número variable de pasos temporales previos como entrada. Un ejemplo clásico es el modelo AR(p)AR(p)AR(p), que utiliza las ppp observaciones anteriores: $$x_t = c + \sum_{k=1}^{p} \phi_k x_{t-k} + \epsilon_t$$Su principal ventaja es que son fáciles de ajustar porque trabajan con una ventana fija de entradas. Sin embargo, suelen ser demasiado simples cuando los datos presentan dependencias complejas.
#### 2. Modelos Autorregresivos Latentes
> Los modelos autorregresivos latentes introducen un estado oculto $h_t$​ para capturar y resumir dependencias más complejas del pasado. En lugar de depender solo de una ventana fija de observaciones, el modelo mantiene una representación interna que se va actualizando con el tiempo. Una formulación general es: $$h_t = f(h_{t-1}, x_{t-1}; \theta), \qquad \hat{x}_t = g(h_t; \theta)$$donde $f$ y $g$ son funciones de tipo red neuronal.
> La idea clave es que el estado oculto resume la información relevante de las entradas pasadas, haciendo al modelo más expresivo que un modelo autorregresivo clásico.![[Pasted image 20260317164610.png]]
#### 3. Modelos de Secuencia y Orden de Decodificación
> El objetivo general en un modelo de secuencia es modelar la probabilidad conjunta de una secuencia completa: $$P(x_1, x_2, \ldots, x_T)$$
> Esta probabilidad se factoriza como: $$P(x_1, \ldots, x_T) = P(x_1)\prod_{t=2}^{T} P(x_t \mid x_{t-1}, \ldots, x_1)$$Esto refleja que los datos se tratan como secuencias en las que el orden importa, como ocurre en lenguaje natural o en series temporales. Cada término de la factorización expresa cómo un elemento depende de los anteriores, siguiendo la regla de la cadena de la probabilidad.
> En modelado del lenguaje, lo habitual es decodificar de izquierda a derecha: $$P(x_1, \ldots, x_T) = P(x_1)\prod_{t=2}^{T} P(x_t \mid x_1, \ldots, x_{t-1})$$Esta elección responde a una estructura causal: los eventos futuros no deben influir en el pasado. Además, suele ofrecer más capacidad predictiva cuando se trata de predecir el siguiente elemento de la secuencia.
#### 4. Modelos de Markov
> Los modelos de Markov introducen una simplificación adicional: asumen que el futuro es condicionalmente independiente del pasado dado el historial más reciente. En su forma más simple: $$P(x_t \mid x_{t-1}, \ldots, x_1) \approx P(x_t \mid x_{t-1})$$Con esta hipótesis, la probabilidad conjunta queda: $$P(x_1, \ldots, x_T) = P(x_1)\prod_{t=2}^{T} P(x_t \mid x_{t-1})$$Esto da lugar a modelos más sencillos, como las cadenas de Markov. El problema es que esta suposición suele ser demasiado restrictiva cuando existen dependencias de largo alcance. Los Hidden Markov Models (HMMs) introducen un estado no observado para intentar capturar parcialmente esos efectos más largos.
#### 5. Predicción Temporal a Distintos Horizontes
> En predicción temporal, el caso más simple es la predicción a un paso, donde se intenta estimar el siguiente valor: $$\hat{x}_{t+1} = f(x_t, x_{t-1}, \ldots)$$Cuando se quiere predecir varios pasos hacia delante, puede usarse forecasting recursivo: una vez predicho $\hat{x}_{t+1}$​, esa predicción se reutiliza como nueva entrada. Para un horizonte $k$: $$\hat{x}_{t+k} = f(\hat{x}_{t+k-1}, \ldots, x_t)$$El problema de este enfoque es que los errores se van acumulando a medida que aumenta el horizonte de predicción. Por eso, al comparar distintos horizontes, se observa que:
> - en 1-step la predicción sigue bastante bien la señal real
> - en 4-step y 16-step aparece retardo y suavizado
> - en 64-step las desviaciones ya son mucho mayores
> En resumen, cuanto mayor es el horizonte, peor suele ser la precisión.
#### 6. Interpolación vs. Extrapolación
> La interpolación consiste en predecir en regiones del espacio de datos que están bien apoyadas por ejemplos de entrenamiento. En este caso, el riesgo de grandes desviaciones suele ser menor si los datos están bien muestreados.
> La extrapolación, en cambio, implica predecir fuera del rango bien cubierto por los datos observados. Aquí la incertidumbre es mayor, el modelo puede no generalizar bien y los errores suelen crecer, especialmente si cambia el patrón subyacente.
#### 7. Modelos de Lenguaje Antes de las RNNs
> Un modelo de lenguaje asigna una probabilidad a una secuencia de palabras: $$P(x_1, x_2, \ldots, x_T) = \prod_{t=1}^{T} P(x_t \mid x_1, \ldots, x_{t-1})$$Esto permite medir lo probable que es una frase bajo el modelo y tiene aplicaciones en generación de texto, reconocimiento de voz o traducción automática.
> Antes de las RNNs, una aproximación habitual eran los modelos n-gram, que aproximan la probabilidad condicional usando solo las $n-1$ palabras anteriores: $$P(x_t \mid x_{t-1}, x_{t-2}, \ldots, x_1) \approx P(x_t \mid x_{t-1}, \ldots, x_{t-n+1})$$Ejemplos para una secuencia de cuatro palabras $(x_1,x_2,x_3,x_4)$: $$P(x_1,x_2,x_3,x_4)=P(x_1)P(x_2)P(x_3)P(x_4) \quad \text{(unigram)}$$$$P(x_1,x_2,x_3,x_4)=P(x_1)P(x_2\mid x_1)P(x_3\mid x_2)P(x_4\mid x_3) \quad \text{(bigram)}$$ $$P(x_1,x_2,x_3,x_4)=P(x_1)P(x_2\mid x_1)P(x_3\mid x_1,x_2)P(x_4\mid x_2,x_3) \quad \text{(trigram)}$$Aumentar n permite capturar más contexto, pero también incrementa el problema de sparsity: muchos n-gramas aparecen poco o no aparecen nunca.
> 
> La estimación básica se hace por máxima verosimilitud a partir de frecuencias del corpus. Por ejemplo: $$\hat{P}(\text{learning} \mid \text{deep}) = \frac{n(\text{deep},\text{learning})}{n(\text{deep})}.$$Esta es, esencialmente, una frecuencia relativa. El problema aparece cuando ciertos pares o n-gramas tienen conteo cero. Para evitar probabilidades nulas se usa suavizado, por ejemplo Laplace o add-ϵ: $$\hat{P}(x)=\frac{n(x)+\epsilon_1/m}{n+\epsilon_1}, \qquad \hat{P}(x' \mid x)=\frac{n(x,x')+\epsilon_2 \hat{P}(x')}{n(x)+\epsilon_2}$$La idea es actuar como si cada evento se hubiese observado unas pocas veces extra.
#### 8. Perplexity y Preparación de Secuencias
> La perplexity mide lo bien que un modelo probabilístico predice una muestra: $$\text{Perplexity}=\exp\left(-\frac{1}{n}\sum_{t=1}^{n}\log P(x_t \mid x_1,\ldots,x_{t-1})\right)$$Cuanto menor es la perplexity, mayor es la confianza del modelo sobre la secuencia. Una frase muy probable tendrá menor perplexity que una secuencia extraña o incoherente.
> 
> La interpretación básica es:
> - **Modelo perfecto**: $\text{Perplexity} = 1$
> - **Modelo bueno**: $\text{Perplexity} \approx 20 - 100$
> - **Modelo aleatorio**: $\text{Perplexity} = |V|$ donde $|V|$ es el tamaño del vocabulario
> - **Peor caso**: si el modelo asigna probabilidad cero a la secuencia correcta,  $\text{Perplexity} \to \infty$
> 
> Para entrenar modelos de secuencia, una estrategia común es partir el texto en entradas y objetivos desplazados una posición:
> - **Inputs**: las palabras o tokens en posiciones $[t, t+1, \ldots]$
> - **Targets**: la siguiente palabra o token en cada posición, $[t+1, \ldots]$
> Esto suele implementarse mediante ventanas deslizantes u overlapping windows, tanto en modelos n-gram como en modelos neuronales.

### II. Introduction to RNNs
#### 1. Inputs
> Las Recurrent Neural Networks (RNNs) procesan **secuencias de entradas**. En datos de lenguaje o, en general, datos categóricos, los tokens o palabras no pueden introducirse directamente al modelo, sino que primero deben convertirse a una representación numérica. 
> Las dos formas principales de hacerlo son:
> - **One-hot encoding**
> - **Learned embeddings**
> 
> El objetivo es obtener una **representación vectorial** de cada token que pueda introducirse en la RNN en cada instante temporal.
> 
> En **one-hot encoding**, cada token discreto se representa mediante un vector de ceros con un único 1 en la posición correspondiente a ese token. Por ejemplo, si _Apple_ es el token 1, _Chicken_ el 2 y _Broccoli_ el 3, entonces: $$\text{Apple} \to [1,0,0], \quad \text{Chicken} \to [0,1,0], \quad \text{Broccoli} \to [0,0,1]$$Es una representación simple y no ambigua, y en pytorch puede generarse fácilmente con `torch.nn.functional.one_hot`. Su principal inconveniente es que, si el vocabulario es grande, los vectores son de alta dimensión y muy dispersos. Además, no capturan relaciones entre tokens, ya que todos quedan a la misma distancia entre sí.
> 
> En **embeddings**, en lugar de usar un vector disperso muy grande, se aprende una representación densa y de baja dimensión para cada token: $\text{token} \mapsto e_{\text{token}} \in \mathbb{R}^d$ donde $d$ es mucho menor que el tamaño del vocabulario. En pytorch esto se implementa con `nn.Embedding(num_embeddings, embedding_dim)`, donde el identificador de cada token actúa como índice dentro de una tabla aprendida de tamaño $[num\_embeddings, embedding\_dim]$.
> 
> Los embeddings tienen varias ventajas frente al one-hot encoding: son representaciones compactas, reducen la dimensionalidad y permiten que tokens similares tengan embeddings similares, capturando así relaciones semánticas. Además, estos embeddings se entrenan junto con el resto del modelo mediante backpropagation.
> 
> En cuanto a la **forma de la entrada**, la secuencia se organiza según tres ejes: **número de muestras** (_batch size_), **número de pasos temporales** (_time steps_) y **número de características de entrada**      (_input features_). En cada instante temporal, la RNN recibe el vector correspondiente al token o elemento de la secuencia.
#### 2. Por Qué Necesitamos las RNNs
> Primero, las redes neuronales tradicionales **no almacenan información entre time steps**, por lo que no pueden reutilizar directamente el pasado para tareas secuenciales o de forecasting. Segundo, en modelos clásicos de lenguaje como **Markov** o **n-grams**, la probabilidad de un token $x_t$ se condiciona solo a los últimos $n-1$ tokens, lo que obliga a almacenar del orden de $|V|^n$ probabilidades. La diapositiva señala explícitamente que este crecimiento es **exponencial en $n$** y, por tanto, **computacionalmente caro**.
> 
> La solución propuesta es reemplazar ese historial explícito por una **representación latente**: $$P(x_t \mid x_{t-1}, \ldots, x_1) \approx P(x_t \mid h_{t-1})$$donde $h_{t-1}$ es un **hidden state** que resume la información pasada. Esa es la idea base de una RNN: en vez de guardar todo el historial de manera literal, mantener una **memoria compacta** en el estado oculto.
#### 3. Redes Neuronales Sin Estado Oculto
> Antes de introducir la recurrencia, las diapositivas recuerdan el caso de una red feedforward estándar, concretamente un **MLP**. Son como una red con capa de entrada, una o más capas ocultas y una capa de salida, que procesa los datos **en modo feedforward**, es decir, **sin lazo de realimentación**.
> 
> Dado un mini-batch $X \in \mathbb{R}^{n \times d}$, la activación de la capa oculta se calcula como: $$H = \phi(XW_{xh} + b_h)$$- $W_{xh} \in \mathbb{R}^{d \times h}$ conecta entrada con capa oculta
> - $b_h \in \mathbb{R}^{1 \times h}$ es el sesgo
> - $\phi$ es la función de activación
> 
> Una vez obtenida la activación oculta, la salida final es: $$O = HW_{hq} + b_q, \quad W_{hq} \in \mathbb{R}^{h \times q}, \ b_q \in \mathbb{R}^{1 \times q}, \ O \in \mathbb{R}^{n \times q}$$Aquí **no se almacena información para pasos futuros**: todas las salidas se calculan **en paralelo** y sin memoria temporal.
#### 4. RNNs con Estado Oculto
> La diferencia esencial con respecto al MLP es la incorporación de **hidden states**, que permiten **retener información a lo largo del tiempo**. Dado un mini-batch secuencial $X_t \in \mathbb{R}^{n \times d}$, la activación oculta en el instante $t$ se define como: $$H_t = \phi(X_tW_{xh} + H_{t-1}W_{hh} + b_h)$$El término nuevo es $H_{t-1}W_{hh}$, que introduce la dependencia con el estado oculto previo y permite que la red use información histórica al procesar el presente. Según la diapositiva, esta es precisamente la pieza que hace posible trabajar con **datos secuenciales**.
> 
> El cálculo recurrente en cada paso temporal usa:
> - la entrada actual $X_t \in \mathbb{R}^{n \times d}$
> - el estado oculto previo $H_{t-1} \in \mathbb{R}^{n \times h}$
> - la matriz $W_{xh} \in \mathbb{R}^{d \times h}$
> - la matriz $W_{hh} \in \mathbb{R}^{h \times h}$
> - el sesgo $b_h \in \mathbb{R}^{1 \times h}$
> 
> La salida en ese instante se obtiene como:  $O_t = H_tW_{hq} + b_q$  donde:
> - $O_t \in \mathbb{R}^{n \times q}$
> - $W_{hq} \in \mathbb{R}^{h \times q}$
> - $b_q \in \mathbb{R}^{1 \times q}$
> 
> El bloque de salida sigue siendo similar al de un MLP, pero ahora existe una **memoria adicional** a través del estado oculto.
#### 5. Grafo Computacional de una RNN
> Las diapositivas del **computational graph** explican el flujo temporal de una RNN de forma operativa:
> 1. en el paso temporal $t$, se procesa la entrada $X_t$ y se calcula $H_t$
> 2. el estado oculto $H_t$ se pasa al instante siguiente $t+1$
> 3. el proceso se repite para cada paso temporal, manteniendo un flujo continuo de información
> 
> La idea visual es el **despliegue en el tiempo**: una misma celda recurrente se repite a lo largo de la secuencia y va transmitiendo su estado oculto de un paso al siguiente. Así se ve con claridad que la información no “desaparece” tras una sola propagación, sino que se arrastra mediante la cadena de estados ocultos.
#### 6. Ejemplo de Character-Level RNN
> Rellenar diapo 37
#### 7. Gradient Clipping
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