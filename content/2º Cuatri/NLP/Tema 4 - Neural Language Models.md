### I. Vuelta a los Modelos de Lenguaje
#### 1. Recordatorio de la Tarea de Modelado de Lenguaje
> Un modelo de lenguaje toma una secuencia de palabras $w_1,w_2,\dots,w_t$ y devuelve una distribución de probabilidad para la siguiente palabra: $P(w_{t+1}\mid w_1,w_2,\dots,w_t)$.  
> Intuición del material: dado un contexto como “she was a”, el modelo asigna probabilidades a palabras del vocabulario, por ejemplo $p(\text{woman}\mid \text{she was a})$, $p(\text{doctor}\mid \text{she was a})$, etc.
#### 2. Recordatorio del Modelo Clásico $n$-Gram
> En el enfoque estadístico, para definir $P(w_{t+1}\mid w_1,\dots,w_t)$ se hace una **asunción de Markov**: la siguiente palabra depende solo de las últimas $n-1$ palabras:  $$P(w_{t+1}\mid w_1,\dots,w_t)\approx P(w_{t+1}\mid w_{t-n+2},\dots,w_t)$$Luego se estima por conteos de $n$-gramas en un corpus: $$P(w_{t+1}\mid w_{t-n+2},\dots,w_t)=\frac{\mathrm{count}(w_{t-n+2},\dots,w_t,w_{t+1})}{\mathrm{count}(w_{t-n+2},\dots,w_t)}$$Consecuencia que enfatiza el material: en el peor caso hay que almacenar conteos para hasta $|V|^n$ $n$-gramas; el tamaño crece exponencialmente con $n$ y el modelo no captura dependencias de largo plazo.

### II. Problemas de Ceros y de Generalización en Modelos por Conteo
#### 1. Ejemplo con Shakespeare (Sparsity Extrema)
> El material ilustra la sparsity en bigramas con el corpus de Shakespeare:
> - $884{,}647$ tokens de palabra.
> - vocabulario de tamaño $|V|=29{,}066$ tipos.  
> Shakespeare usa aproximadamente $300{,}000$ tipos de bigrama, frente a $|V|^2=844$ millones de bigramas posibles, por lo que el $99.96$ de los bigramas posibles no ocurren.  
> Una estimación por frecuencia relativa asigna probabilidad no nula solo a aproximadamente el $0.04$ de los bigramas posibles (y aún menos para trigramas, $4$-gramas, etc.), lo que genera problemas de generalización: combinaciones no vistas tienen probabilidad $0$ (o muy pequeña si se suaviza).
#### 2. Motivación: “¿Podemos Hacerlo Mejor?”
> El material plantea la transición: si el modelo por conteo falla por sparsity y por crecimiento exponencial, ¿cómo construir un **LM neuronal** para modelar $P(w_{t+1}\mid w_{t-n+2},\dots,w_t)$?  
> Propuesta: una red neuronal feed-forward con:
> - entrada: concatenación de $n-1$ vectores de palabra,
> - salida: una capa $\mathrm{softmax}$ sobre $|V|$ unidades (distribución sobre el vocabulario para la siguiente palabra).  
> Referencia citada: Bengio et al. (2003), “A Neural Probabilistic Language Model”.

### III. Redes Neuronales Feed-Forward: Definiciones Que Usa el Tema
#### 1. Red con Una Capa Oculta
> Una red con una capa oculta se define como una función $f:\mathbb{R}^{d_{in}}\to\mathbb{R}^{d_{out}}$ dada por:  $$z^{[1]}=xW^{[1]}+b^{[1]},\qquad h^{[1]}=\phi^{[1]}(z^{[1]})$$$$z^{[2]}=h^{[1]}W^{[2]}+b^{[2]},\qquad y=\phi^{[2]}(z^{[2]})$$donde $x\in\mathbb{R}^{1\times d_{in}} \quad W^{[1]}\in\mathbb{R}^{d_{in}\times d_h} \quad b^{[1]}\in\mathbb{R}^{1\times d_h}, \quad W^{[2]}\in\mathbb{R}^{d_h\times d_{out}}, \quad b^{[2]}\in\mathbb{R}^{1\times d_{out}}$  
> El material llama “hidden units” a los componentes $h^{[1]}_j$ y “output units” a $y_j$.
#### 2. Red con $L$ Capas
> Para $L\in\mathbb{N}$ capas totales, el material define una red $g:\mathbb{R}^{d_{in}}\to\mathbb{R}^{d_{out}}$ como:  $$a^{[0]}=x$$$$z^{[l]}=a^{[l-1]}W^{[l]}+b^{[l]},\qquad a^{[l]}=\phi^{[l]}(z^{[l]}),\qquad l=1,\dots,L$$$$y=a^{[L]}$$
#### 3. Funciones de Activación: Sigmoid, ReLU y Softmax
> El material define una activación como una función $\phi:\mathbb{R}^n\to\mathbb{R}^n$ aplicada elemento a elemento.
> Sigmoid:  $$\sigma([z_1,\dots,z_n])=\left[\frac{1}{1+e^{-z_1}},\dots,\frac{1}{1+e^{-z_n}}\right]$$y cada componente se mapea a $(0,1)$.  
> ReLU:  $$\mathrm{ReLU}(z)=\max(0,z)$$con ejemplo donde valores negativos se llevan a $0$ y los positivos se mantienen.  
> Softmax (para normalizar a distribución): $$\phi(z)_i=\frac{e^{z_i}}{\sum_{j=1}^{d}e^{z_j}},\qquad i=1,\dots,d$$

### IV. Modelo de Lenguaje Neuronal de Ventana Fija
#### 1. Idea de Arquitectura
> Un LM neuronal de ventana fija implementa el mismo objetivo que un $n$-gram: modelar $P(w_{n+1}\mid w_1,\dots,w_n)$ usando un contexto de tamaño fijo.  
> La idea visual del material (diagramas): tokenización $\rightarrow$ embeddings $\rightarrow$ red neuronal $\rightarrow$ $\mathrm{softmax}$ sobre el vocabulario (probabilidades del siguiente token).
#### 2. Definición Formal (Con Matriz de Embeddings)
> Sea una matriz de embeddings $E\in\mathbb{R}^{|V|\times d_{emb}}$ para un vocabulario $V$. Dadas palabras $w_1,\dots,w_n\in V$, sean $e_1,\dots,e_n$ sus embeddings.  
> Capa de entrada: concatenación de embeddings:  $$x=[e_1,\dots,e_n]\in\mathbb{R}^{n\cdot d_{emb}}$$Salida: $$y=a^{[L]}=\mathrm{softmax}(z^{[L]}),\qquad y\in\mathbb{R}^{|V|}$$donde $y$ es la distribución de probabilidad sobre $V$ para la siguiente palabra.
#### 3. Forma “Con Una Capa Oculta” del Diagrama
> El diagrama del material resume el cómputo como: $$x=(e(w_1);\dots;e(w_N))$$$$h=f(xW+b_1)$$$$y=\mathrm{softmax}(hU+b_2)$$produciendo una distribución sobre el vocabulario.
#### 4. Quiz del Material: Mini-LM con Vocabulario Indexado
> Se propone un vocabulario indexado $V={w_1:\text{the},w_2:\text{cat},w_3:\text{dog},w_4:\text{pet},w_5:\text{barks},w_6:\text{meows}}$ y embeddings $1$-dimensionales:  $$E=[e_{\text{the}}:[0],,e_{\text{cat}}:[1],,e_{\text{dog}}:[-1],,e_{\text{pet}}:[0],,e_{\text{meows}}:[0],,e_{\text{barks}}:[0]]$$Modelo con ventana de tamaño $2$ y una capa (salida):  $$a^{[0]}=x,\quad z^{[1]}=a^{[0]}W^{[1]}+b^{[1]},\quad y=\mathrm{softmax}(z^{[1]})$$donde $y_i$ es la probabilidad asignada a $w_i$ como siguiente palabra.  
> Se dan $W^{[1]}\in\mathbb{R}^{2\times 6}$ y $b^{[1]}\in\mathbb{R}^{1\times 6}$ y se pide calcular $P(\text{meows}\mid \text{the, cat})$, $P(\text{barks}\mid \text{the, dog})$, etc. **La solución numérica no aparece en el material aportado.**

### V. Entrenamiento de un LM Neuronal de Ventana Fija
#### 1. Cómo Se Construye el Entrenamiento (Recorrido del Texto)
> El material describe el entrenamiento con un corpus grande: se recorre el texto y, en cada posición, se pide al modelo predecir la siguiente palabra dadas las $n$ palabras previas (ventana fija).  
> Ejemplo ilustrativo: dado “cats are very cute”, predecir “animals”.  
> Se entrena con descenso por gradiente minimizando el error de predicción medido con pérdida de cross-entropy.
#### 2. Pérdida en un Paso (Decoder Loss)
> En cada paso hay una única palabra correcta $w_k$ como siguiente palabra. Si el modelo asigna probabilidad $\hat{y}_k$ a esa palabra, la pérdida es:  $$L=-\log \hat{y}_k.$$El material aclara: $\hat{y}\in\mathbb{R}^{1\times |V|}$ es el vector de probabilidades predichas y $\hat{y}_k$ es la probabilidad asignada a la palabra correcta $w_k$.

### VI. Número de Parámetros y Escalabilidad
#### 1. Conteo de Parámetros en un LM de Ventana Fija (Una Capa Oculta)
> Sea $d_{in}$ la dimensión de entrada, con una capa oculta de tamaño $d_h$ y una salida de tamaño $|V|$. El material cuenta:
> - Capa oculta: $W^{[1]}\in\mathbb{R}^{d_{in}\times d_h}$ aporta $d_{in}\cdot d_h$ parámetros, y $b^{[1]}\in\mathbb{R}^{1\times d_h}$ aporta $d_h$.
> - Capa de salida: $W^{[2]}\in\mathbb{R}^{d_h\times |V|}$ aporta $d_h\cdot |V|$, y $b^{[2]}\in\mathbb{R}^{1\times |V|}$ aporta $|V|$.  
> Total: $\left(d_{in}\cdot d_h\right)+d_h+\left(d_h\cdot |V|\right)+|V|$  
#### 2. Crecimiento Lineal con Hiperparámetros
> El material usa que $d_{in}=n\cdot d_{emb}$ (tamaño de ventana por tamaño de embedding) para reescribir:  $$\left(n\cdot d_{emb}\cdot d_h\right)+d_h+\left(d_h\cdot |V|\right)+|V|.$$Concluye que el número de parámetros crece linealmente con $n$, con $d_{emb}$ y $d_h$, y con $|V|$ (manteniendo los otros fijos).
#### 3. Comparación con $n$-Grams (Exponencial vs Lineal)
> Para un $n$-gram clásico, en el peor caso hay $|V|^{n-1}$ contextos posibles y cada uno requiere una distribución sobre $|V|$ palabras, por lo que el total (peor caso) es $|V|^n$ parámetros: crecimiento exponencial en $n$.  
> El material compara con un LM neuronal con $d_{emb}=50$, $d_h=128$ y $|V|=10{,}000$: para $n\in{3,4,5,6}$, el LM neuronal está alrededor de $\approx 1.31\text{M}$–$\approx 1.33\text{M}$ parámetros, mientras que el $n$-gram está en $10^{12}$, $10^{16}$, $10^{20}$, $10^{24}$ respectivamente.

### VII. Ventajas y Limitaciones Frente a Modelos por Conteo
#### 1. Ventaja de Generalización gracias a Embeddings
> El material argumenta que, si palabras similares tienen embeddings similares, el modelo tiende a predecir probabilidades similares en contextos similares:  $$P(w\mid \text{the doctor saw the})\approx P(w\mid \text{a nurse sees her})$$Idea operativa: un cambio pequeño en la entrada (embeddings) induce un cambio pequeño en la probabilidad predicha.  
> Ejemplo del material: aunque el modelo no haya visto “a nurse sees her patient”, si vio una frase similar como “the doctor saw her patient”, puede generalizar y asignar:  $$P(\text{patient}\mid \text{the doctor saw the})\approx P(\text{patient}\mid \text{a nurse sees her})$$En contraste, un $n$-gram sin suavizado predeciría “patient” tras “the doctor saw her”, pero no tras “a nurse sees her”.
#### 2. Quiz de Generalización con Palabra Nueva
> Se extiende el vocabulario con “kitten” y se asume que su embedding es similar al de “cat”, por ejemplo: $e_{\text{cat}}=[1]$ y $e_{\text{kitten}}=[0.9]$.  
> Incluso si “the kitten meows” no apareció en entrenamiento, se espera: $$P(\text{meows}\mid \text{the, kitten})\approx P(\text{meows}\mid \text{the, cat})$$**El material lo plantea como ejercicio de cálculo con el mini-modelo; la solución numérica no aparece.**
#### 3. Limitación: Sensibilidad al Orden de Palabras
> El material (citando a Bengio et al.) avisa: la generalización es sensible al orden; solo funciona bien cuando aparecen las mismas palabras en las mismas posiciones.  
> Se comparan dos oraciones con el mismo significado pero distinto orden:  
> $1)$ “The cat chased the mouse in the garden.”  
> $2)$ “In the garden, the cat chased the mouse.”  
> Aunque tengan significado idéntico, un LM de ventana fija ve entradas distintas y no generaliza fácilmente del primer orden al segundo; el material lo resume como:  $$P(\text{mouse}\mid \text{the cat chased the}\dots)\not\approx P(\text{mouse}\mid \text{in the garden the}\dots)$$
#### 4. Limitación Estructural: La Asunción de Ventana (Markov) Sigue
> Resumen explícito del material: aunque sea neuronal, el LM de ventana fija sigue haciendo una asunción tipo Markov (contexto acotado por la ventana), por lo que no puede tratar contextos arbitrariamente largos.

### VIII. Resumen Final del Tema
#### 1. Qué Te Tienes Que Llevar
> - Un LM neuronal de ventana fija modela $P(w_{n+1}\mid w_1,\dots,w_n)$ con una red feed-forward que concatena embeddings y usa $\mathrm{softmax}$ para producir una distribución sobre $V$.
> - Se entrena recorriendo un corpus y minimizando, en cada paso, $L=-\log \hat{y}_k$ (cross-entropy sobre la palabra correcta).
> - Ventaja clave sobre $n$-grams: crecimiento de parámetros lineal en $n$, $d_{emb}$, $d_h$ y $|V|$, frente a crecimiento exponencial $|V|^n$ en el peor caso para $n$-grams.
> - Ventaja de generalización: embeddings permiten suavidad en la entrada y generalizar a contextos “parecidos”.
> - Limitaciones: contexto acotado por ventana (no arbitrariamente largo) y generalización muy sensible al orden.

Los apuntes continúan en [[2º Cuatri/NLP/Tema 5 - Recurrent Neural Networks]]