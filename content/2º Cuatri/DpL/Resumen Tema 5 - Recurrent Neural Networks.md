### I. Before RNNs
#### 1. Modelos Autorregresivos
> Los modelos autorregresivos asumen que el valor actual puede modelarse a partir de los valores pasados, es decir, se trabaja con distribuciones del tipo $$P(x_t \mid x_{t-1}, \ldots, x_1)$$o con su esperanza condicional $$\mathbb{E}[x_t \mid x_{t-1}, \ldots, x_1]$$En general, pueden usar un número variable de pasos temporales previos como entrada. Un ejemplo clásico es el modelo $AR(p)$, que utiliza las $p$ observaciones anteriores: $$x_t = c + \sum_{k=1}^{p} \phi_k x_{t-k} + \epsilon_t$$Su principal ventaja es que son fáciles de ajustar porque trabajan con una ventana fija de entradas. Sin embargo, suelen ser demasiado simples cuando los datos presentan dependencias complejas.
#### 2. Modelos Autorregresivos Latentes
> Los modelos autorregresivos latentes introducen un estado oculto $h_t$​ para capturar y resumir dependencias más complejas del pasado. En lugar de depender solo de una ventana fija de observaciones, el modelo mantiene una representación interna que se va actualizando con el tiempo. Una formulación general es: $$h_t = f(h_{t-1}, x_{t-1}; \theta), \qquad \hat{x}_t = g(h_t; \theta)$$donde $f$ y $g$ son funciones de tipo red neuronal.
> La idea clave es que el estado oculto resume la información relevante de las entradas pasadas, haciendo al modelo más expresivo que un modelo autorregresivo clásico.![[Pasted image 20260317164610.png]]
#### 3. Modelos de Secuencia y Orden de Decodificación
> El objetivo general en un modelo de secuencia es modelar la probabilidad conjunta de una secuencia completa: $$P(x_1, x_2, \ldots, x_T)$$Esta probabilidad se factoriza como: $$P(x_1, \ldots, x_T) = P(x_1)\prod_{t=2}^{T} P(x_t \mid x_{t-1}, \ldots, x_1)$$Esto refleja que los datos se tratan como secuencias en las que el orden importa, como ocurre en lenguaje natural o en series temporales. Cada término de la factorización expresa cómo un elemento depende de los anteriores, siguiendo la regla de la cadena de la probabilidad.
> En modelado del lenguaje, lo habitual es decodificar de izquierda a derecha: $$P(x_1, \ldots, x_T) = P(x_1)\prod_{t=2}^{T} P(x_t \mid x_1, \ldots, x_{t-1})$$Esta elección responde a una estructura causal: los eventos futuros no deben influir en el pasado. Además, suele ofrecer más capacidad predictiva cuando se trata de predecir el siguiente elemento de la secuencia.
#### 4. Modelos de Markov
> Los modelos de Markov introducen una simplificación adicional: asumen que el futuro es condicionalmente independiente del pasado dado el historial más reciente. En su forma más simple: $$P(x_t \mid x_{t-1}, \ldots, x_1) \approx P(x_t \mid x_{t-1})$$Con esta hipótesis, la probabilidad conjunta queda: $$P(x_1, \ldots, x_T) = P(x_1)\prod_{t=2}^{T} P(x_t \mid x_{t-1})$$Esto da lugar a modelos más sencillos, como las cadenas de Markov. El problema es que esta suposición suele ser demasiado restrictiva cuando existen dependencias de largo alcance. Los Hidden Markov Models (HMMs) introducen un estado no observado para intentar capturar parcialmente esos efectos más largos.
#### 5. Predicción Temporal a Distintos Horizontes
> En predicción temporal, el caso más simple es la predicción a un paso, donde se intenta estimar el siguiente valor: $$\hat{x}_{t+1} = f(x_t, x_{t-1}, \ldots)$$![[Pasted image 20260320161715.png]]
> 
> Cuando se quiere predecir varios pasos hacia delante, puede usarse forecasting recursivo: una vez predicho $\hat{x}_{t+1}$​, esa predicción se reutiliza como nueva entrada. Para un horizonte $k$: $$\hat{x}_{t+k} = f(\hat{x}_{t+k-1}, \ldots, x_t)$$![[Pasted image 20260320162021.png]]
>
> El problema de este enfoque es que los errores se van acumulando a medida que aumenta el horizonte de predicción. Por eso, al comparar distintos horizontes: ![[Pasted image 20260320162106.png]] 
> se observa que:
> - en 1-step la predicción sigue bastante bien la señal real
> - en 4-step y 16-step aparece retardo y suavizado
> - en 64-step las desviaciones ya son mucho mayores
> 
> En resumen, cuanto mayor es el horizonte, peor suele ser la precisión.
#### 6. Interpolación vs. Extrapolación
> La interpolación consiste en predecir en regiones del espacio de datos que están bien apoyadas por ejemplos de entrenamiento. En este caso, el riesgo de grandes desviaciones suele ser menor si los datos están bien muestreados.
> La extrapolación, en cambio, implica predecir fuera del rango bien cubierto por los datos observados. Aquí la incertidumbre es mayor, el modelo puede no generalizar bien y los errores suelen crecer, especialmente si cambia el patrón subyacente. ![[Pasted image 20260320162212.png]]
#### 7. Modelos de Lenguaje Antes de las RNNs
> Un modelo de lenguaje asigna una probabilidad a una secuencia de palabras: $$P(x_1, x_2, \ldots, x_T) = \prod_{t=1}^{T} P(x_t \mid x_1, \ldots, x_{t-1})$$Esto permite medir lo probable que es una frase bajo el modelo y tiene aplicaciones en generación de texto, reconocimiento de voz o traducción automática.
> Antes de las RNNs, una aproximación habitual eran los modelos n-gram, que aproximan la probabilidad condicional usando solo las $n-1$ palabras anteriores: $$P(x_t \mid x_{t-1}, x_{t-2}, \ldots, x_1) \approx P(x_t \mid x_{t-1}, \ldots, x_{t-n+1})$$Ejemplos para una secuencia de cuatro palabras $(x_1,x_2,x_3,x_4)$: $$P(x_1,x_2,x_3,x_4)=P(x_1)P(x_2)P(x_3)P(x_4) \quad \text{(unigram)}$$ $$P(x_1,x_2,x_3,x_4)=P(x_1)P(x_2\mid x_1)P(x_3\mid x_2)P(x_4\mid x_3) \quad \text{(bigram)}$$ $$P(x_1,x_2,x_3,x_4)=P(x_1)P(x_2\mid x_1)P(x_3\mid x_1,x_2)P(x_4\mid x_2,x_3) \quad \text{(trigram)}$$Aumentar n permite capturar más contexto, pero también incrementa el problema de sparsity: muchos n-gramas aparecen poco o no aparecen nunca.
> 
> La estimación básica se hace por máxima verosimilitud a partir de frecuencias del corpus. Por ejemplo: $$\hat{P}(\text{learning} \mid \text{deep}) = \frac{n(\text{deep},\text{learning})}{n(\text{deep})}.$$Esta es, esencialmente, una frecuencia relativa. El problema aparece cuando ciertos pares o n-gramas tienen conteo cero. Para evitar probabilidades nulas se usa suavizado, por ejemplo Laplace o add-ϵ: $$\hat{P}(x)=\frac{n(x)+\epsilon_1/m}{n+\epsilon_1}, \qquad \hat{P}(x' \mid x)=\frac{n(x,x')+\epsilon_2 \hat{P}(x')}{n(x)+\epsilon_2}$$La idea es actuar como si cada evento se hubiese observado unas pocas veces extra.
#### 8. Perplexity & Partitioning Sequences
> La perplexity mide lo bien que un modelo probabilístico predice una muestra: $$\text{Perplexity}=\exp\left(-\frac{1}{n}\sum_{t=1}^{n}\log P(x_t \mid x_1,\ldots,x_{t-1})\right)$$Cuanto menor es la perplexity, mayor es la confianza del modelo sobre la secuencia. Una frase muy probable tendrá menor perplexity que una secuencia extraña o incoherente.
> 
> La interpretación básica es:
> - **Modelo perfecto**: $\text{Perplexity} = 1$
> - **Modelo bueno**: $\text{Perplexity} \approx 20 - 100$
> - **Modelo aleatorio**: $\text{Perplexity} = |V|$ donde $|V|$ es el tamaño del vocabulario
> - **Peor caso**: si el modelo asigna probabilidad cero a la secuencia correcta,  $\text{Perplexity} \to \infty$
> 
> Para entrenar modelos de secuencia, una estrategia común es partir el texto en entradas y objetivos desplazados una posición: ![[Pasted image 20260320162546.png]]
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
> En cuanto a la **forma de la entrada**, la secuencia se organiza según tres ejes: ![[Pasted image 20260320162742.png]]
>  **número de muestras** (batch size), **número de pasos temporales** (time steps) y **número de características de entrada** (input features). En cada instante temporal, la RNN recibe el vector correspondiente al token o elemento de la secuencia.
#### 2. Necesidad de las RNNs
> Las redes neuronales tradicionales **no almacenan información entre time steps**, por lo que no pueden usar directamente información pasada en tareas secuenciales o de forecasting. Además, en modelos clásicos de lenguaje como **Markov** o **n-grams**, la probabilidad de un token $x_t$ se condiciona solo a los últimos $n-1$ tokens. Esto obliga a almacenar del orden de $|V|^n$ probabilidades, que crecen **exponencialmente con $\large n$** y hacen que el modelo sea **computacionalmente costoso**.
> 
> Frente a esto, las RNNs sustituyen el historial explícito por una **representación latente**: $$P(x_t \mid x_{t-1}, \ldots, x_1) \approx P(x_t \mid h_{t-1})$$donde $h_{t-1}$ es un **hidden state** que resume la información pasada. La idea central es no almacenar todo el historial de forma explícita, sino mantener una **representación compacta del pasado** en el estado oculto.
#### 3. NNs sin Estado Oculto
> Antes de introducir la recurrencia, se parte de una red neuronal feedforward estándar, como un **Multilayer Perceptron (MLP)**. Un MLP consta de una **capa de entrada**, una o más **capas ocultas** y una **capa de salida**, y procesa los datos en modo **feedforward**, es decir, **sin recurrencia ni lazo de realimentación**.
> 
> Dado un mini-batch de ejemplos $X \in \mathbb{R}^{n \times d}$, donde $n$ es el tamaño del batch y $d$ el número de características de entrada, la activación de la capa oculta se calcula como:  $$H = \phi(XW_{xh} + b_h)$$donde:
> - $W_{xh} \in \mathbb{R}^{d \times h}$ son los pesos que conectan la entrada con la capa oculta.
> - $b_h \in \mathbb{R}^{1 \times h}$ es el sesgo de la capa oculta.
> - $\phi$ es la función de activación.
> 
> Una vez obtenidas las activaciones ocultas, la salida final se calcula como:  $$O = HW_{hq} + b_q$$donde:
> - $W_{hq} \in \mathbb{R}^{h \times q}$ son los pesos que conectan la capa oculta con la salida.
> - $b_q \in \mathbb{R}^{1 \times q}$ es el sesgo de la capa de salida.
> - $O \in \mathbb{R}^{n \times q}$ representa la salida final del modelo.
> 
> En este caso **no se almacena información entre time steps para reutilizarla más adelante**: las salidas se calculan **en paralelo** y no existe una memoria temporal asociada al modelo.
#### 4. RNNs con Estado Oculto
> A diferencia de un MLP, una RNN incorpora **hidden states** que le permiten **retener información entre time steps**. Dado un mini-batch secuencial $X_t \in \mathbb{R}^{n \times d}$, la activación oculta en el instante $t$ se calcula como:  $$H_t = \phi(X_tW_{xh} + H_{t-1}W_{hh} + b_h)$$donde el término $H_{t-1}W_{hh}$ introduce la dependencia con el estado oculto previo. Gracias a esta conexión recurrente, la red puede incorporar información histórica al procesar la entrada actual, lo que la hace adecuada para **datos secuenciales**.
> 
> En cada paso temporal, el cálculo recurrente utiliza:
> - La entrada actual $X_t \in \mathbb{R}^{n \times d}$
> - El estado oculto previo $H_{t-1} \in \mathbb{R}^{n \times h}$
> - La matriz de pesos $W_{xh} \in \mathbb{R}^{d \times h}$ (**input-to-hidden**)
> - La matriz de pesos $W_{hh} \in \mathbb{R}^{h \times h}$ (**hidden-to-hidden**)
> - El sesgo $b_h \in \mathbb{R}^{1 \times h}$
> 
> La salida en el instante $t$ se obtiene como:  $$O_t = H_tW_{hq} + b_q$$donde:
> - $O_t \in \mathbb{R}^{n \times q}$
> - $W_{hq} \in \mathbb{R}^{h \times q}$
> - $b_q \in \mathbb{R}^{1 \times q}$
> 
> La capa de salida es similar a la de un MLP, pero la RNN añade una **memoria temporal** a través del estado oculto.
#### 5. Grafo Computacional
> El **computational graph** de una RNN puede entenderse como un proceso recurrente que se repite en cada paso temporal: ![[Pasted image 20260320163308.png]]![[Pasted image 20260320163716.png]]
> 1. En el instante $t$, se procesa la entrada $X_t$ y se calcula el estado oculto $H_t$.
> 2. El estado oculto $H_t$ se transmite al siguiente paso temporal $t+1$.
> 3. Este proceso se repite a lo largo de toda la secuencia, manteniendo un **flujo continuo de información**.
> 
> La idea clave es el **despliegue en el tiempo** (_unrolling_): la misma celda recurrente se aplica repetidamente en los distintos instantes de la secuencia. En cada paso, la red combina la entrada actual con el estado oculto anterior para producir un nuevo estado oculto y, si corresponde, una salida. Así, la información pasada puede influir en el procesamiento presente a través de la cadena de estados ocultos.
#### 6. Character-Level RNN
> En una **Character-Level RNN**, la secuencia de entrada está formada por **caracteres** y el modelo aprende a predecir el carácter siguiente en cada paso temporal. Así, en cada instante $t$, la red recibe un carácter de entrada, actualiza su estado oculto $H_t$ y produce una salida $O_t$ asociada a la predicción del siguiente carácter.
> 
> La idea es desplazar la secuencia objetivo una posición respecto a la secuencia de entrada. Por ejemplo, si la entrada es:  $m,\ a,\ c,\ h,\ i,\ n$  la secuencia objetivo será:  $a,\ c,\ h,\ i,\ n,\ e$ ![[Pasted image 20260320123439.png]]
> 
> De este modo, la RNN aprende dependencias secuenciales a nivel de carácter, usando el estado oculto para arrastrar información de los caracteres anteriores.
#### 7. Gradient Clipping
> **Gradient clipping** es una técnica que se usa para evitar el problema de los **exploding gradients**, especialmente frecuente en RNNs. Cuando los gradientes son demasiado grandes, el entrenamiento se vuelve inestable y las actualizaciones pueden ser tan grandes que arruinen el proceso de optimización.
> 
> La idea es **limitar la magnitud del gradiente** para mantener estable el entrenamiento. Esto se consigue a partir de una función continua Lipschitz, cuyo cambio está acotado por:  $$|f(\mathbf{x}) - f(\mathbf{y})| \leq L|\mathbf{x}-\mathbf{y}|$$y, aplicado a una actualización de gradiente, se obtiene:  $$|f(\mathbf{x}) - f(\mathbf{x} - \eta \mathbf{g})| \leq L\eta |\mathbf{g}|$$Por tanto, si $|\mathbf{g}|$ es muy grande, también puede serlo el cambio en la función, lo que justifica acotar el gradiente.
> 
> El mecanismo es sencillo: durante backpropagation se calcula el gradiente $\mathbf{g}$ y, si su norma supera un umbral $\theta$, se reescala como:  $$\mathbf{g} \leftarrow \min\left(1,\frac{\theta}{|\mathbf{g}|}\right)\mathbf{g}$$De este modo, la norma del gradiente no excede el valor fijado por $\theta$.
> 
> En pytorch, esto puede aplicarse con `torch.nn.utils.clip_grad_norm_`, normalmente entre `loss.backward()` y `optimizer.step()`.
> 
> Se utiliza sobre todo en:
> - **RNNs, LSTMs y GRUs**, que son propensas a exploding gradients
> - Redes profundas con activaciones muy no lineales
> - Situaciones donde la pérdida presenta picos o el entrenamiento se vuelve inestable
> 
> La elección del umbral $\theta$ es importante, si es **demasiado grande**, apenas tiene efecto; si es **demasiado pequeño**, el entrenamiento se ralentiza porque las actualizaciones son demasiado pequeñas. Por ello, su valor suele ajustarse **empíricamente**.

### III. Backpropagation Through Time 
#### 1. Cálculo de Gradientes y Backpropagation en RNNs
> En una RNN, el cálculo de gradientes es más difícil que en una red feedforward porque el estado oculto $h_t$ depende tanto de la entrada actual $x_t$ como del estado oculto anterior $h_{t-1}$. Esto introduce una **dependencia recurrente**, de modo que los gradientes deben propagarse hacia atrás a través de múltiples pasos temporales.
> 
> Las ecuaciones básicas del modelo son: $$h_t = f(W_{hx}x_t + W_{hh}h_{t-1}), \qquad o_t = W_{qh}h_t$$La función de pérdida total se construye agregando la pérdida en cada instante temporal. Esto es la media de las pérdidas a lo largo de $T$ pasos:  $$L = \frac{1}{T}\sum_{t=1}^{T} \ell(o_t, y_t)$$donde cada $\ell$ compara la predicción $o_t$ con el objetivo $y_t$, por ejemplo mediante **CE** o **MSE**. ![[Pasted image 20260320163835.png]]
> 
> Como la pérdida depende de todas las salidas de la secuencia, el gradiente respecto a los parámetros del modelo debe tener en cuenta **todos los time steps**. Por eso, en una RNN el proceso de entrenamiento requiere propagar los gradientes hacia atrás a través de la cadena de estados ocultos, acumulando la contribución de cada paso temporal.
#### 2. Backpropagation Through Time
> En RNNs, el entrenamiento se realiza mediante **Backpropagation Through Time (BPTT)**, ya que la pérdida total depende de las salidas producidas en todos los pasos temporales. Si la pérdida total se define como:  $$L=\frac{1}{T}\sum_{t=1}^{T}\ell(o_t,y_t)$$entonces el gradiente respecto a cada salida es: $$\frac{\partial L}{\partial o_t}=\frac{1}{T}\frac{\partial \ell(o_t,y_t)}{\partial o_t}\in\mathbb{R}^q$$Para los pesos de salida $W_{qh}$, el gradiente acumula la contribución de todos los instantes:  $$\frac{\partial L}{\partial W_{qh}}=\sum_{t=1}^{T}\frac{\partial L}{\partial o_t}h_t^\top$$Esto refleja que cada salida $o_t=W_{qh}h_t$ aporta una parte del gradiente, y todas esas contribuciones se suman a lo largo del tiempo.
> 
> El gradiente respecto al estado oculto también se propaga recursivamente hacia atrás. Para el último instante: $$\frac{\partial L}{\partial h_T}=W_{qh}^\top\frac{\partial L}{\partial o_T}$$y para $t<T$: $$\frac{\partial L}{\partial h_t}=W_{hh}^\top\frac{\partial L}{\partial h_{t+1}}+W_{qh}^\top\frac{\partial L}{\partial o_t}$$Esto muestra que $\frac{\partial L}{\partial h_t}$ depende tanto del error del instante actual como de los gradientes que llegan desde pasos futuros. En forma expandida, cada estado oculto recibe contribuciones de todos los tiempos posteriores.
> 
> De manera análoga, los gradientes de los pesos recurrentes y de entrada se obtienen acumulando términos a lo largo de toda la secuencia: $$\frac{\partial L}{\partial W_{hx}}=\sum_{t=1}^{T}\frac{\partial L}{\partial h_t}x_t^\top,\qquad \frac{\partial L}{\partial W_{hh}}=\sum_{t=1}^{T}\frac{\partial L}{\partial h_t}h_{t-1}^\top$$![[Pasted image 20260320163929.png]]
> La idea clave es que **cada matriz de pesos acumula gradientes procedentes de todos los pasos temporales**. El problema es que, cuando $T$ es grande, estas sumas pueden ser **costosas computacionalmente** y además dar lugar a **vanishing gradients** o **gradient explosion**.
#### 3. Truncated BPTT y Estrategias Prácticas
> Calcular el gradiente completo sobre todos los pasos temporales corresponde a **full BPTT**, pero en la práctica suele resultar demasiado costoso o inestable. Por eso se utiliza con frecuencia **Truncated Backpropagation Through Time (TBPTT)**.
> 
> La idea de TBPTT es **no retropropagar a través de toda la secuencia**, sino detener la propagación tras $\tau$ pasos temporales. Esto reduce el coste en memoria y computación, y además ayuda a evitar gradientes extremadamente grandes o muy pequeños. El valor de $\tau$ suele elegirse para capturar las dependencias de corto plazo más útiles.
> 
> Frente al cálculo completo: ![[Pasted image 20260320164219.png]]
> - **Full BPTT** tiene en cuenta toda la secuencia, pero es caro y puede ser inestable.
> - **TBPTT** usa una ventana truncada y suele ofrecer un mejor equilibrio entre coste y estabilidad.
> 
> También existe una variante de **randomized truncation**, en la que el punto de truncamiento o la longitud $\tau$ se elige aleatoriamente. La motivación es exponer al modelo a subsecuencias de distintas longitudes y, potencialmente, capturar mejor dependencias de rango medio.
> 
> Sin embargo, esta estrategia no siempre mejora a la truncación fija: en la práctica puede aumentar la varianza y sus beneficios suelen ser pequeños. Por eso, la opción más habitual es usar una **truncación regular con $\large \tau$ fijo**, que normalmente actúa como el **sweet spot** entre coste, estabilidad y capacidad de aprendizaje.

### IV. First Types of RNNs
#### 1. Deep RNNs
> Las **Deep RNNs** extienden las RNNs tradicionales apilando **múltiples capas recurrentes** en lugar de usar una sola capa oculta. Mientras que una RNN estándar procesa la secuencia con una única capa recurrente, una Deep RNN organiza varias capas una encima de otra, de forma similar a la profundidad en MLPs o CNNs. ![[Pasted image 20260320170423.png]]
> 
> Esta mayor profundidad permite aprender **representaciones jerárquicas** y capturar relaciones más complejas en los datos secuenciales. Las primeras capas capturan información de alta frecuencia (corto plazo), y según se avanza en la red, las capas capturan información de frecuencias más bajas (largo plazo). Además, puede ayudar a modelar dependencias de largo alcance de forma más efectiva, por lo que resulta útil en tareas como **speech recognition**, **text generation** y **time-series forecasting**.
> 
> Si la entrada es una secuencia $X_t \in \mathbb{R}^{n \times d}$, una Deep RNN consta de $L$ capas ocultas y estados ocultos $H_t^{(l)} \in \mathbb{R}^{n \times h}$, donde $h$ es el número de unidades ocultas. La salida final es $O_t \in \mathbb{R}^{n \times q}$.
> 
> La primera capa recurrente se calcula como: $$H_t^{(1)}=\phi_1\left(X_tW_{xh}^{(1)}+H_{t-1}^{(1)}W_{hh}^{(1)}+b_h^{(1)}\right)$$Para las capas más profundas $(l=2,\dots,L)$, la entrada ya no es $X_t$, sino la salida de la capa anterior en el mismo instante temporal:  $$H_t^{(l)}=\phi_l\left(H_t^{(l-1)}W_{xh}^{(l)}+H_{t-1}^{(l)}W_{hh}^{(l)}+b_h^{(l)}\right)$$La salida se obtiene a partir de la última capa oculta:  $$O_t=H_t^{(L)}W_{hq}+b_q$$donde $W_{hq}\in\mathbb{R}^{h\times q}$ proyecta el estado oculto al espacio de salida y $b_q\in\mathbb{R}^{1\times q}$ es el sesgo.
> 
> En conjunto, la profundidad hace que cada capa extraiga características progresivamente más abstractas, lo que mejora la capacidad del modelo para representar dependencias complejas en secuencias. Además, esta arquitectura también puede combinarse con **LSTMs** o **GRUs** para mejorar la memoria a largo plazo.
#### 2. Bidirectional RNNs
> Las **Bidirectional RNNs (BiRNNs)** extienden las RNNs estándar procesando la secuencia en **ambas direcciones**: una RNN recorre la entrada de **izquierda a derecha** y otra de **derecha a izquierda**. De este modo, el modelo puede utilizar simultáneamente **contexto pasado y futuro** al hacer una predicción. ![[Pasted image 20260320165025.png]]
> 
> Esto es útil en tareas donde no basta con conocer solo las palabras anteriores, sino que conviene disponer de la **secuencia completa**. Por ejemplo, en **Part-of-Speech tagging** o en el relleno de palabras faltantes, la interpretación de un elemento puede depender tanto de lo que aparece antes como de lo que aparece después.
> 
> La arquitectura utiliza dos estados ocultos en cada instante $t$:
> - un estado hacia delante $\overrightarrow{H}_t$
> - un estado hacia atrás $\overleftarrow{H}_t$
> 
> Sus ecuaciones son:  $$\overrightarrow{H}_t=\phi\left(X_tW_{xh}^{(f)}+\overrightarrow{H}_{t-1}W_{hh}^{(f)}+b_h^{(f)}\right)$$ $$\overleftarrow{H}_t=\phi\left(X_tW_{xh}^{(b)}+\overleftarrow{H}_{t+1}W_{hh}^{(b)}+b_h^{(b)}\right)$$Después, ambos estados ocultos se **concatenan** antes de pasar a la capa de salida:  $$O_t= \left [\overrightarrow{H}_t;\overleftarrow{H}_t \right] W_{hq}+b_q$$
> La principal ventaja de las BiRNNs es que capturan dependencias en las dos direcciones y son más conscientes del contexto que una RNN unidireccional. Por eso se han usado en tareas como **POS tagging**, **Named Entity Recognition (NER)**, **speech recognition** y **machine translation**.
> 
> Como limitaciones, requieren disponer de la **secuencia completa** antes de procesarla, por lo que no son ideales para tareas en tiempo real. Además, son más costosas computacionalmente que las RNNs estándar y siguen pudiendo sufrir problemas de **vanishing** o **exploding gradients**. Por último, éstas han sido reemplazadas en gran medida por **attention mechanisms**.
#### 3. Encoder - Decoder
> La arquitectura **Encoder-Decoder** se utiliza en tareas **sequence-to-sequence (Seq2Seq)**, como **machine translation**, **text summarization** y **speech-to-text**. Su objetivo es transformar una **secuencia de entrada** en una **secuencia de salida**, permitiendo trabajar con longitudes variables tanto en la entrada como en la salida. ![[Pasted image 20260320170820.png]]
> 
> El modelo consta de dos componentes principales: ![[Pasted image 20260320175936.png]]
> - **Encoder**: procesa la secuencia de entrada y la comprime en un **estado codificado** o **context vector** de longitud fija.
> - **Decoder**: genera la secuencia de salida a partir de ese estado.
> 
> El **encoder** recibe una secuencia de longitud variable y la transforma en una representación comprimida mediante una **RNN, GRU o LSTM**. Va procesando la entrada paso a paso y actualizando un estado oculto, de forma que el estado final resume la secuencia completa:  $$h_t = f(x_t, h_{t-1})$$Puede ser **unidireccional**, usando solo información pasada, o **bidireccional**, incorporando tanto información pasada como futura.
> 
> El **decoder** toma el estado del encoder y genera la salida **token a token**. En cada paso utiliza el **token previo**, el **vector de contexto** y su **estado anterior**:  $$s_{t'} = g(y_{t'-1}, c, s_{t'-1})$$El proceso continúa hasta generar un token de fin de secuencia (**EOS**). El decoder también puede implementarse con **RNNs, GRUs o LSTMs**.
> 
> Durante el entrenamiento se usa normalmente **teacher forcing**, es decir, en cada paso se alimenta al decoder con el **token correcto anterior** en lugar del token predicho por el propio modelo. Esto acelera el entrenamiento, pero introduce **exposure bias**. La función de pérdida utilizada es **Cross-Entropy Loss** con enmascarado para ignorar los tokens de padding. ![[Pasted image 20260320180057.png]]
> 
> En inferencia, el decoder ya no dispone de la secuencia correcta, así que genera los tokens uno a uno usando sus propias predicciones previas.
#### 4. Decoding Strategies
> En tareas **sequence-to-sequence**, la salida debe generarse token a token, y por eso hacen falta estrategias de búsqueda para decidir qué secuencia producir. La opción más simple es **greedy search**, pero no siempre encuentra la mejor secuencia. En el extremo opuesto, **exhaustive search** evalúa todas las secuencias posibles y elige la de mayor probabilidad, aunque su coste crece como  $O(|\mathcal{Y}|^{T'})$ donde $T'$ es la longitud de la secuencia y $\mathcal{Y}$ el vocabulario, por lo que resulta computacionalmente inviable.
> 
> En **greedy search**, en cada paso temporal $t'$ se selecciona el token con mayor probabilidad condicional:  $$y_{t'}=\arg\max_{y\in\mathcal{Y}} P(y\mid y_1,\ldots,y_{t'-1},c)$$El proceso continúa hasta generar el token especial de fin de secuencia **\<eos>**. Su ventaja es que es simple y rápido, pero su inconveniente es que una decisión localmente óptima en un paso puede impedir encontrar la mejor secuencia global.
> 
> Como punto intermedio aparece **beam search**, que busca equilibrar eficiencia y calidad. En lugar de conservar una sola hipótesis, mantiene en cada paso las $k$ mejores secuencias candidatas, donde $k$ es el **beam size**. En cada instante:
> - se expanden las $k$ secuencias actuales
> - se evalúan sus extensiones
> - se conservan solo las $k$ mejores
> 
> Así, beam search reduce el coste frente a exhaustive search y normalmente mejora los resultados respecto a greedy search. Por ejemplo, con $k=2$, el modelo mantiene siempre las dos mejores secuencias parciales en cada paso.
> 
> La secuencia final se elige maximizando una puntuación basada en la suma de log-probabilidades con normalización por longitud: $$\frac{1}{L^\alpha}\sum_{t'=1}^{L}\log P(y_{t'}\mid y_1,\ldots,y_{t'-1},c)$$donde $L$ es la longitud de la secuencia y $\alpha$ es un factor de normalización de longitud.

### V. Modern RNNs
#### 1. Long Short-Term Memory
> Las **LSTMs** se diseñaron para abordar los problemas de **vanishing** y **exploding gradients** en RNNs. Su idea principal es introducir una **memory cell** capaz de mantener información a lo largo de secuencias largas. ![[Pasted image 20260320181401.png]]
> 
> Cada celda LSTM incluye un **estado interno** $C_t$ y tres puertas que regulan el flujo de información:
> - **Input gate**: controla cuánta información nueva se añade.
> - **Forget gate**: determina cuánta información pasada se conserva.
> - **Output gate**: controla cuánta información se transmite hacia delante.
> 
> Estas puertas se implementan como capas totalmente conectadas con activación sigmoide:  $$I_t=\sigma(X_tW_{xi}+H_{t-1}W_{hi}+b_i)$$$$F_t=\sigma(X_tW_{xf}+H_{t-1}W_{hf}+b_f)$$$$O_t=\sigma(X_tW_{xo}+H_{t-1}W_{ho}+b_o)$$Además, calcula un **input node** o valor candidato para la memoria usando una activación **tanh**:  $$\tilde{C}_t=\tanh(X_tW_{xc}+H_{t-1}W_{hc}+b_c)$$Este término genera los posibles nuevos valores que podrían incorporarse al estado de memoria.
> 
> El **estado interno de la celda** se actualiza combinando la información previa y la nueva información candidata:  $$C_t=F_t\odot C_{t-1}+I_t\odot \tilde{C}_t$$Así, la forget gate decide qué parte de la memoria anterior se mantiene y la input gate cuánto contenido nuevo se añade.
> 
> Finalmente, el **estado oculto** se calcula a partir de la memoria y la output gate: $$H_t=O_t\odot \tanh(C_t)$$De este modo, la LSTM controla de forma selectiva qué información pasa al siguiente paso temporal.
> 
> En conjunto, la característica clave de las LSTMs es su **gated memory cell**, que les permite decidir explícitamente cuándo **actualizar**, **olvidar** y **propagar** información, mejorando así la capacidad de modelar dependencias de largo plazo frente a una RNN estándar.
#### 2. Gated Recurrent Units
> Las **GRUs** son una arquitectura de RNN equivalente a una **variante simplificada de las LSTMs**. Su objetivo es controlar el flujo de información mediante mecanismos de compuertas, pero con una estructura más simple. ![[Pasted image 20260320181232.png]]
> 
> Una GRU utiliza dos puertas:
> - **Reset gate** $(R_t)$: controla cuánta información pasada se descarta.
> - **Update gate** $(Z_t)$: determina cuánta información pasada se conserva.
> 
> A partir de estas compuertas, se calcula primero un **estado oculto candidato**:  $$\tilde{H}_t=\tanh\left(X_tW_{xh}+(R_t\odot H_{t-1})W_{hh}+b_h\right)$$  
> Aquí, la **reset gate** regula la influencia del estado oculto previo sobre el nuevo contenido candidato.
> 
> Después, el **estado oculto final** se actualiza combinando el estado anterior y el estado candidato:  $$H_t=Z_t\odot H_{t-1}+(1-Z_t)\odot \tilde{H}_t$$Así, la **update gate** decide cuánto del pasado se mantiene y cuánto se reemplaza por la nueva información.
> 
> En conjunto, las GRUs simplifican la arquitectura de las LSTM, pero siguen permitiendo controlar qué información pasada se conserva y cuánto contenido nuevo se incorpora al estado oculto.