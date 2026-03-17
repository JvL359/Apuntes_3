### I. Introduction
#### 1. Idea y Contexto
> Las **redes neuronales artificiales** surgen como una inspiración simplificada del funcionamiento de las neuronas biológicas. La idea básica es combinar varias **entradas** con unos **pesos**, aplicar una suma y después una **función de activación** para obtener una salida.
> Un único perceptrón o neurona artificial puede modelar relaciones sencillas, pero resulta limitado cuando el problema es más complejo. Por ello, se combinan varias neuronas en una **red neuronal artificial**, capaz de representar comportamientos más ricos y aproximar funciones más complejas.
> En este tema se parte de la neurona artificial como bloque básico para entender cómo se construyen redes neuronales y por qué estas permiten resolver problemas que un único modelo lineal no puede capturar.

### II. FeedForward Layer
#### 1. Multi Layer Perceptron (MLP)
> Un **Multi Layer Perceptron (MLP)** es una red neuronal formada por una **capa de entrada**, una o varias **capas ocultas** y una **capa de salida**. Cada capa aplica una transformación lineal a sus entradas y, después, una **función de activación** para introducir no linealidad.
> La idea principal es que una sola neurona o una sola transformación lineal tienen capacidad limitada, mientras que al **combinar varias neuronas en capas** se pueden modelar relaciones más complejas entre las variables de entrada y la salida. En general, las capas ocultas suelen usar activaciones no lineales, mientras que la capa de salida utiliza una activación acorde al problema.
#### 2. Capa y Detalles
> Una **feedforward layer** o capa densa recibe un vector —o un batch de vectores— y aplica una **transformación lineal** de la forma `Z = XW^T + b`, donde `X` representa la entrada, `W` los pesos y `b` el sesgo. Después, a ese resultado se le aplica una **función de activación** elemento a elemento: `A = φ(Z)`.
> El número de parámetros de la capa viene dado por los **pesos** y los **biases**, es decir, `d_in × d_out + d_out`, donde `d_in` es la dimensión de entrada y `d_out` el número de neuronas de salida. Entre las activaciones más habituales aparecen **sigmoid**, **ReLU**, **tanh** y **softmax**. Además, la inicialización de los pesos y el proceso de entrenamiento son importantes para que la red aprenda correctamente.

### III. Regression & Classification
#### 1. Regression
> La **regresión** es un problema fundamental de **aprendizaje supervisado** en el que se busca **predecir valores continuos** a partir de unas variables de entrada. Dado un vector de características $x \in \mathbb{R}^d$, el objetivo es aprender una función $f:\mathbb{R}^d \to \mathbb{R}$. En su versión más simple, la **regresión lineal** modela esta relación como una combinación lineal de las entradas: $\hat{y} = \mathbf{w}^\top \mathbf{x} + b$.  
> En esta formulación, los parámetros a aprender son los **pesos** $\mathbf{w}$ y el **sesgo** $b$. Para ajustar el modelo se define una función de pérdida, en estas diapositivas el **error cuadrático medio (MSE)**: $$L(w,b)=\frac{1}{2n}\sum_{i=1}^{n}(\hat{y}^{(i)}-y^{(i)})^2$$y el objetivo de optimización consiste en encontrar los valores $w^*, b^*$ que minimizan dicha pérdida. 
> La regresión lineal puede resolverse de dos formas principales. Por un lado, existe una **solución analítica cerrada** basada en ecuaciones matriciales, $\mathbf{w} = (X^\top X)^{-1}X^\top y$, aunque su coste puede hacerla poco práctica cuando la dimensión es grande. Por otro lado, puede resolverse de forma **iterativa** mediante **descenso por gradiente**, actualizando los parámetros con las reglas $$w \leftarrow w - \eta \frac{\partial L}{\partial w}​, \quad b \leftarrow b - \eta \frac{\partial L}{\partial b}$$​Esta segunda opción es la más relevante en Deep Learning, ya que constituye la base del entrenamiento de redes neuronales.
> Conceptualmente, la regresión lineal puede verse como una **red neuronal de una sola capa**. A partir de ahí, al introducir **múltiples salidas** y, sobre todo, al **apilar capas con no linealidades**, se obtienen redes neuronales capaces de modelar relaciones mucho más complejas. Las diapositivas conectan esta idea con el **teorema de aproximación universal**, según el cual una red con suficientes unidades ocultas y una no linealidad adecuada puede aproximar cualquier función continua.
#### 2. Clasificación
##### 2.1. Binary
> La **clasificación binaria** es un problema de aprendizaje supervisado en el que se busca asignar cada entrada a una de **dos clases posibles**, normalmente codificadas como $\{0,1\}$. En este contexto, el modelo no predice un valor continuo, sino la **probabilidad** de pertenecer a una de las dos clases.
> El modelo base que aparece en estas diapositivas es la **regresión logística**, que puede interpretarse como un modelo lineal con salida probabilística. A partir de una combinación lineal de las entradas, se aplica una **función sigmoide**, que transforma la salida en un valor entre 0 y 1. Así, la predicción puede interpretarse como la probabilidad de que la muestra pertenezca a la clase positiva.
> Geométricamente, en clasificación binaria el modelo aprende una **frontera de decisión** que separa ambas clases. En el caso lineal, esta frontera es una recta o hiperplano.
> Los parámetros a aprender siguen siendo los **pesos** $w$ y el **bias** $b$, pero en este caso la función de pérdida adecuada no es el error cuadrático, sino la **negative log likelihood**, que en las diapositivas aparece como: $$L(w,b)=-\frac{1}{n}\sum_{i=1}^{n}\left[y^{(i)}\log p^{(i)}+(1-y^{(i)})\log(1-p^{(i)})\right], \quad p = \displaystyle \sigma (\mathbf{w}^\top \mathbf{x} + \mathbf{b})$$El objetivo de optimización es encontrar los parámetros que minimizan dicha pérdida: $$w^*, b^*=\arg\min_{w,b} L(w,b)$$En resumen, la clasificación binaria modela la probabilidad de pertenencia a una de dos clases mediante una salida sigmoidal y ajusta sus parámetros minimizando la pérdida de tipo logarítmico.
##### 2.2. Multiclass
> La **clasificación multiclase** extiende la clasificación binaria al caso en que cada entrada puede pertenecer a una de **K clases** posibles. En lugar de predecir una única probabilidad binaria, el modelo produce una distribución de probabilidad sobre todas las clases, y la decisión se toma asignando la clase con mayor probabilidad.
> Para ello se utiliza la activación **softmax**, que transforma las salidas lineales del modelo en probabilidades normalizadas: $$P(y=k\mid x)=\frac{e^{\mathbf{w}_k^\top \mathbf{x}+b_k}}{\sum_{j=1}^{K} e^{\mathbf{w}_j^\top \mathbf{x}+b_j}}$$donde $x\in\mathbb{R}^d, \quad W\in\mathbb{R}^{d\times k}, \quad b\in\mathbb{R}^k$. Así, la salida del modelo puede escribirse como: $$P(y)=\text{softmax}(W^\top x+b)_y$$La función de pérdida asociada es la **cross-entropy loss**: $$L(W,b)=-\frac{1}{n}\sum_{i=1}^{n}\sum_{k=1}^{K} y_k^{(i)}\log p_k^{(i)}$$donde $K$ es el número de clases, $y_k^{(i)}$ es la etiqueta codificada en _one-hot_ para la clase $k$ de la muestra $i$, y $p_k^{(i)}$​ es la probabilidad predicha para esa clase. El objetivo del entrenamiento es encontrar los parámetros $W^*, b^*$ que minimizan esta pérdida.
> A diferencia de la regresión lineal, en clasificación logística no existe una **solución cerrada**, por lo que el problema se resuelve mediante métodos iterativos, como el **descenso por gradiente** con reglas de actualización análogas a las de la regresión, pero aplicadas a predicciones transformadas mediante sigmoide o softmax: $$\mathbf{w}\leftarrow \mathbf{w}-\eta \frac{1}{n}\sum_{i=1}^{n}(p^{(i)}-y^{(i)})x^{(i)}, \quad b\leftarrow b-\eta \frac{1}{n}\sum_{i=1}^{n}(p^{(i)}-y^{(i)})$$Intuitivamente, el modelo aprende varias **fronteras de decisión** que dividen el espacio de entrada en regiones, una para cada clase.
##### 2.3. Implementación Práctica
> Cuando los datos de entrada son **imágenes**, aparece un problema práctico: una imagen es un tensor **2D**, mientras que un **MLP** espera como entrada un tensor **1D**. Por ello, antes de introducir la imagen en la red, es necesario aplicar una operación de **flattening**, que convierte la matriz de píxeles en un vector. Así, por ejemplo, una imagen de MNIST puede transformarse en un vector largo que después se conecta a las neuronas de entrada del perceptrón multicapa.
> En pytorch, esta operación puede implementarse de dos maneras. La primera es mediante la capa **`torch.nn.Flatten`**, que se usa como un módulo dentro del modelo. La segunda es mediante la operación **`torch.flatten()`**, que aplica el aplanado directamente sobre un tensor. Ambas permiten transformar la entrada para adaptarla al formato esperado por una red densa.
> Las diapositivas distinguen además entre **`torch.nn`** y **`torch.nn.functional`**. `torch.nn` proporciona **clases o módulos** reutilizables para definir capas dentro del `__init__()` del modelo, lo que resulta más adecuado para arquitecturas completas y serializables. En cambio, `torch.nn.functional` proporciona **funciones sin estado**, pensadas para usarse directamente en `forward()` o en operaciones puntuales.
> En clasificación multiclase también aparece una cuestión práctica importante: la **estabilidad numérica del softmax**. La implementación ingenua puede provocar _overflow_ o _underflow_ al exponenciar valores grandes. Para evitarlo, se resta el máximo logit antes de aplicar la exponencial: $$\text{softmax}(z_i)=\frac{e^{z_i-\max(z)}}{\sum_{j=1}^{K}e^{z_j-\max(z)}}$$Esta transformación no cambia el resultado, pero hace el cálculo más estable. De forma relacionada, el truco de **log-softmax** permite calcular directamente el logaritmo del softmax de manera numéricamente más robusta.

### IV. Loss Functions & Non Linearities
#### 1. MLE
> **Maximum Likelihood Estimation (MLE)** es un criterio para estimar los parámetros θ\thetaθ de un modelo probabilístico haciendo que los datos observados sean lo más probables posible según el modelo. Si el dataset es $X=\{x^{(1)},\dots,x^{(m)}\}$, la idea es elegir los parámetros que maximizan la **likelihood**: $$L(\theta)=\prod_{i=1}^{m} p(x^{(i)};\theta)$$Es decir, se busca qué valores de $\theta$ explican mejor los datos observados. Conceptualmente, se distingue entre la distribución real de los datos $P_{data}$​, que genera las muestras y normalmente es desconocida, y la distribución del modelo $P_{model}(\cdot;\theta)$, que depende de los parámetros. El objetivo del MLE es ajustar $\theta$ para que $P_{model}$ se aproxime lo máximo posible a $P_{data}$​.
> En la práctica, en lugar de maximizar un producto de probabilidades, se maximiza la **log-likelihood**, porque transforma productos en sumas y simplifica el cálculo: $$\log L(\theta)=\sum_{i=1}^{m}\log p(x^{(i)};\theta)$$Como el logaritmo es monótono, maximizar la likelihood es equivalente a maximizar la log-likelihood, o de forma equivalente, a minimizar la **negative log-likelihood (NLL)**: $$-\log L(\theta)=-\sum_{i=1}^{m}\log p(x^{(i)};\theta)$$Esto conecta directamente con el entrenamiento mediante optimización por gradiente.
> En **aprendizaje supervisado**, lo que se maximiza es la **likelihood condicional**: $$\theta_{ML}=\arg\max_{\theta} P(Y\mid X;\theta)$$o, para muestras independientes: $$\theta_{ML}=\arg\max_{\theta}\sum_{i=1}^{m}\log P(y^{(i)}\mid x^{(i)};\theta)$$Una idea clave es que muchas funciones de pérdida en Deep Learning se obtienen a partir de MLE bajo ciertas hipótesis probabilísticas:
> - En **clasificación**, si la salida del modelo representa una distribución categórica, maximizar la likelihood equivale a minimizar la **cross-entropy**.
> - En **regresión**, si se asume ruido gaussiano en los errores, maximizar la likelihood equivale a minimizar el **MSE**.
> Por tanto, MLE proporciona la base probabilística que justifica pérdidas tan habituales como **cross-entropy** y **mean squared error**. En este sentido, entrenar una red neuronal puede interpretarse como ajustar sus parámetros para que las predicciones del modelo asignen la máxima probabilidad posible a los datos observados.
#### 2. Other Losses
> - **L1 Loss:** mide la **diferencia absoluta** entre predicciones y valores reales. Su fórmula es $$L=\frac{1}{n}\sum |y_{\text{true}}-y_{\text{pred}}|$$Penaliza los errores de forma **lineal**, por lo que es más **robusta a outliers** que MSE. En PyTorch se usa con `nn.L1Loss()`.
> 
> - **MSE:** mide la **diferencia cuadrática** entre predicciones y valores reales. Su fórmula es $$L=\frac{1}{n}\sum (y_{\text{true}}-y_{\text{pred}})^2$$Penaliza más los errores grandes, por lo que es **más sensible a outliers**. Es una pérdida muy común en tareas de **regresión**. En PyTorch se usa con `nn.MSELoss()`.
> 
> - **Huber Loss:** es una pérdida **híbrida entre L1 y L2**. Se comporta de forma **cuadrática para errores pequeños** y **lineal para errores grandes**, por lo que resulta menos sensible a outliers que MSE, pero más suave que L1 cerca del cero. Está controlada por un parámetro `delta` y en pytorch se implementa con `nn.HuberLoss(delta=1.0)`. ![[Pasted image 20260317115804.png]]
> 
> - **Binary Cross Entropy Loss:** se usa en **clasificación binaria**. En pytorch se prefiere **`BCEWithLogitsLoss`** frente a `BCELoss`, porque combina internamente **sigmoide + binary cross entropy** en una sola operación, lo que mejora la **estabilidad numérica** y el comportamiento del gradiente. Por eso, el modelo debe devolver **logits**, es decir, la salida cruda **sin sigmoide final**.
> 
> - **Cross Entropy Loss:** se usa en **clasificación multiclase**. En pytorch se recomienda **`CrossEntropyLoss`**, ya que combina internamente **softmax + negative log-likelihood**, con una implementación más estable numéricamente y optimizada para trabajar en log-space. Igual que antes, el modelo debe devolver **logits**, es decir, **sin softmax final**, y las etiquetas deben darse como **índices de clase**.
> 
> - **Entropy with Logits or with Probabilities:** en general, conviene trabajar **con logits y no con probabilidades** en la última capa del modelo. Dejar fuera la sigmoide o la softmax mejora la **estabilidad numérica**, produce un **flujo de gradiente más estable**, simplifica la arquitectura y aprovecha implementaciones optimizadas de pytorch. Por ello, en práctica se usa **`BCEWithLogitsLoss`** para clasificación binaria y **`CrossEntropyLoss`** para clasificación multiclase.
#### 3. Non Linearities Need
> Las **no linealidades** son necesarias porque los modelos lineales tienen una capacidad limitada para representar relaciones complejas. De hecho, apilar varias capas lineales **sin** funciones de activación no aporta más expresividad, ya que su composición sigue siendo equivalente a **una sola transformación lineal**. Por eso, sin activaciones, una red profunda no dejaría de ser esencialmente un modelo lineal.
> Las **funciones de activación** introducen esa no linealidad que permite a la red aprender relaciones complejas y construir **representaciones jerárquicas** de los datos. Gracias a ellas, la red puede capturar tanto patrones simples como características de mayor nivel, algo fundamental en problemas reales.
> Además, las activaciones también influyen en el entrenamiento. Ayudan a mantener un mejor **flujo del gradiente** durante la retro-propagación y pueden evitar problemas de saturación o desaparición del gradiente. Por eso, no solo deben ser no lineales, sino también tener propiedades deseables como ser **continuas y diferenciables** casi en todas partes, **computacionalmente eficientes**, favorecer la **preservación del gradiente** y, en algunos casos, producir salidas **centradas en cero** para facilitar la convergencia.
> En resumen, las no linealidades son las que convierten una red neuronal en un modelo capaz de aprender funciones complejas; sin ellas, incluso una red con muchas capas seguiría comportándose como una transformación lineal.
> ![[Pasted image 20260317115551.png]]
#### 4. Activations
> Las **funciones de activación** introducen la no linealidad necesaria para que una red neuronal pueda aprender relaciones complejas. En PyTorch suelen poder usarse tanto como **módulos** de `torch.nn` como mediante funciones de `torch.nn.functional`, según convenga en la implementación.
> Las activaciones más habituales son:
> - **Sigmoide:** transforma la entrada en un valor entre **0 y 1**. Es útil cuando la salida debe interpretarse como una probabilidad, especialmente en clasificación binaria.
>    
> - **Tanh:** es similar a sigmoide, pero su salida está en **[-1,1]**, por lo que está **centrada en cero**. Esto puede favorecer el entrenamiento frente a sigmoide en algunos casos.
>    
> - **ReLU:** devuelve $0$ para entradas negativas y $x$ para entradas positivas. Es una de las activaciones más usadas por su simplicidad y eficiencia.  
>    Un problema asociado es el **Dead ReLU Problem**, que aparece cuando una neurona queda siempre en la zona negativa y pasa a producir solo ceros, dejando de aprender. Entre las causas están malas inicializaciones, _learning rates_ altos o sesgos muy negativos.
>    
> - **Leaky ReLU:** modifica ReLU permitiendo una **pequeña pendiente negativa** para entradas menores que cero. Así evita que las neuronas queden completamente inactivas.
>    
> - **PReLU:** es una variante de Leaky ReLU donde esa pendiente negativa es **aprendible**. Por tanto, añade un parámetro entrenable al modelo.
>    
> - **ELU:** para valores positivos se comporta como una recta, y para valores negativos usa una rama exponencial. Su idea es suavizar el comportamiento de ReLU en la parte negativa.
>    
> - **SELU:** es una extensión de ELU diseñada para redes **self-normalizing**, manteniendo activaciones cercanas a media cero y varianza unitaria durante el _forward_.
>    
> - **Absolute value:** usa el valor absoluto como activación, es decir, $|x|$. Aparece como una alternativa posible, aunque menos estándar que ReLU o Tanh.
>    
> - **MaxOut:** es una activación más general que toma el **máximo de varias transformaciones lineales**. Esta puede aproximar cualquier función convexa, aumentar la capacidad del modelo y puede aproximar distintas formas de activación, pero a cambio requiere **más parámetros**, más coste computacional y puede aumentar el riesgo de _overfitting_. ![[Pasted image 20260317115505.png]]
> 
> En conjunto, **ReLU y sus variantes** suelen ser las opciones más prácticas en muchas redes profundas, mientras que activaciones como **Sigmoid** y **Tanh** siguen siendo útiles en contextos concretos, y **MaxOut** ofrece más flexibilidad a costa de mayor complejidad.
#### 5. Preguntas
> 1. ¿Qué funciones de activación necesitan más entrenamiento?
> 	Las que **tienen parámetros aprendibles** o **aumentan mucho la capacidad del modelo**:
> 	- **PReLU**: necesita más entrenamiento que ReLU o Leaky ReLU porque la pendiente en la parte negativa **se aprende**.
> 	- **MaxOut**: es la que más claramente necesita más entrenamiento, porque cada unidad trabaja con **varias transformaciones lineales** y, por tanto, introduce **muchos más parámetros**.
> 	En cambio:
> 	- **Sigmoid, Tanh, ReLU, Leaky ReLU, ELU y SELU** no tienen parámetros propios que aprender como activación.
> 
> 2. ¿Qué funciones de activación dan más expresividad?
> 	La más expresiva es **MaxOut**, puede aproximar cualquier función convexa, generaliza ReLU y otras activaciones, y aumenta la capacidad del modelo aprendiendo varias regiones lineales.
> 	Después, en flexibilidad:
> 	- **PReLU** es más flexible que **Leaky ReLU** y **ReLU**, porque la pendiente negativa no es fija, sino aprendible.
> 	- **Leaky ReLU** y **ELU/SELU** son más flexibles que **ReLU** en la parte negativa.
> 	- **Sigmoid** y **Tanh** introducen no linealidad, pero no aparecen en estas diapositivas como las más expresivas para redes profundas.
> 
> 3. Ventajas y desventajas de cada una:
> - Sigmoid:
> 	- **Expresividad**: introduce no linealidad y produce salidas entre 0 y 1.
> 	- **Computación**: requiere exponenciales.
> 	- **Forward/backward**: puede saturarse en los extremos, lo que dificulta el flujo del gradiente.
> - Tanh:
> 	- **Expresividad**: similar a sigmoide, pero con salida entre -1 y 1.
> 	- **Computación**: también requiere exponenciales.
> 	- **Forward/backward**: mejora frente a sigmoide en que está **centrada en cero**, pero también puede saturarse.
> - ReLU:
> 	- **Expresividad**: simple pero muy efectiva; base de muchas redes profundas.
> 	- **Computación**: muy barata.
> 	- **Forward/backward**: buen flujo de gradiente para entradas positivas, pero puede aparecer el problema de las **dead ReLU**, donde una neurona deja de activarse y deja de aprender.
> - Leaky ReLU:
> 	- **Expresividad**: algo mayor que ReLU, porque mantiene respuesta en la zona negativa.
> 	- **Computación**: casi tan barata como ReLU.
> 	- **Forward/backward**: reduce el problema de las dead ReLU al dejar una pequeña pendiente negativa.
> - PReLU:
> 	- **Expresividad**: mayor que Leaky ReLU, porque la pendiente negativa se aprende.
> 	- **Computación**: un poco más costosa por tener parámetros extra.
> 	- **Forward/backward**: evita mejor neuronas muertas, pero necesita aprender más y guardar estado.
> - ELU:
> 	- **Expresividad**: similar a ReLU-like, pero con transición más suave en la parte negativa.
> 	- **Computación**: más cara que ReLU porque usa exponencial.
> 	- **Forward/backward**: busca mejorar la suavidad alrededor de 0 y evitar la parte totalmente muerta negativa.
> - SELU:
> 	- **Expresividad**: similar a ELU.
> 	- **Computación**: también más cara que ReLU.
> 	- **Forward/backward**: está diseñada para redes **self-normalizing**, manteniendo activaciones cerca de media 0 y varianza 1 durante el forward.
> - Absolute Value:
> 	- **Expresividad**: introduce una no linealidad simple.
> 	- **Computación**: muy barata.
> 	- **Forward/backward**: en las diapositivas aparece como alternativa, pero no se desarrolla tanto como las demás.
> - MaxOut:
> 	- **Expresividad**: la más alta de las mostradas.
> 	- **Computación**: la más costosa, porque requiere más parámetros y más memoria.
> 	- **Forward/backward**: aumenta mucho la capacidad, pero hace el entrenamiento más lento, más difícil de optimizar y con mayor riesgo de **overfitting**.
> 
> Conclusión rápida:
> - **Más entrenamiento**: **PReLU** y sobre todo **MaxOut**.
> - **Más expresividad**: **MaxOut**.
> - **Más práctica y eficiente**: **ReLU** y sus variantes.
> - **Para evitar dead ReLU**: **Leaky ReLU** o **PReLU**.
> - **Si quieres suavidad / self-normalization**: **ELU** o **SELU**.

### V. Initialization & Optimization
#### 1. Initialization
##### 1.1. Idea
> La **inicialización** de los pesos es crucial porque condiciona cómo se propagan las activaciones y los gradientes a través de la red. Si los pesos iniciales son demasiado pequeños, la señal puede debilitarse y aparecer problemas de **vanishing**; si son demasiado grandes, las activaciones y los gradientes pueden crecer en exceso y provocar **exploding**.
> El objetivo de una buena inicialización es facilitar una propagación estable tanto en el **forward** como en el **backward**, lo que se traduce en un entrenamiento más eficiente y, en general, en una convergencia más rápida.
##### 1.2. Zero / Constant
> La inicialización **zero/constant** consiste en fijar todos los pesos a $0$ o a una misma constante $k$. Su principal ventaja es que es muy simple de implementar, pero presenta un problema fundamental de **simetría**: todas las neuronas de una misma capa empiezan igual y, por tanto, aprenden exactamente lo mismo.
> Además, esta estrategia lleva a gradientes poco útiles o nulos y dificulta seriamente el aprendizaje. En redes profundas, las distribuciones de gradientes tienden a concentrarse cerca de cero y las activaciones pierden variabilidad, lo que empeora la propagación de la señal entre capas.
> Por ello, la conclusión práctica es clara: **no debe usarse para inicializar pesos**; como mucho puede aceptarse en algunos casos para los **bias**.
##### 1.3. Random / Normal (Naive)
> La inicialización **random/normal naive** rompe la simetría asignando a los pesos pequeños valores aleatorios, por ejemplo tomados de una distribución normal como $\mathcal{N}(0, 0.01)$. Esto mejora respecto a la inicialización constante y puede funcionar en redes poco profundas.
> Sin embargo, sigue siendo una estrategia limitada para redes profundas, porque depende mucho de la **desviación estándar** elegida. Si esta es demasiado pequeña, las activaciones se van reduciendo capa a capa y pueden desaparecer; si es demasiado grande, las activaciones crecen demasiado y se vuelven inestables.
> En consecuencia, aunque esta inicialización rompe la simetría, puede seguir produciendo problemas de **vanishing/exploding activations o gradients**, por lo que resulta **subóptima en redes profundas**.
##### 1.4. Constant Activation Variance
> La idea de **constant activation variance** es elegir la escala de los pesos para que la **varianza de las activaciones se mantenga aproximadamente constante** al atravesar las capas. Si para una neurona  $y_i=\sum_j w_{ij}x_j$  y se asume independencia entre entradas y pesos, entonces la varianza de la salida crece como  $\sigma_{y_i}^2=\sigma_x^2 \cdot d_x \cdot \sigma_w^2$  donde $d_x$ es el número de entradas. Para evitar que las activaciones se apaguen o exploten al profundizar en la red, se escala la varianza de los pesos como  $\sigma_w^2=\frac{1}{d_x}$  
> Con ello se busca una propagación más estable de la señal entre capas.
##### 1.5. Xavier / Glorot
> La inicialización **Xavier/Glorot** está diseñada para mantener la varianza de las activaciones dentro de unos límites razonables a lo largo de la red. Tiene en cuenta tanto el número de **entradas** $d_x$ como el de **salidas** $d_y$ de la capa.
> Dos formas habituales son:  $$W \sim U\left(-\sqrt{\frac{6}{d_x+d_y}},\sqrt{\frac{6}{d_x+d_y}}\right)$$ $$W \sim \mathcal{N}\left(0,\frac{2}{d_x+d_y}\right)$$Sus principales ventajas son que mantiene estable la varianza de activaciones y funciona bien con activaciones como **sigmoide** y **tanh**. Como inconveniente, no es la mejor opción para **ReLU**. En pytorch aparece, por ejemplo, como `torch.nn.init.xavier_uniform_()`.
##### 1.6. He / Kaiming
> La inicialización **He/Kaiming** está pensada para activaciones del tipo **ReLU**. Como ReLU anula aproximadamente la mitad de las activaciones negativas, la varianza efectiva se reduce, y por eso se corrige escalando los pesos con $$\mathrm{Var}(w_{ij})=\frac{2}{d_x}$$o, de forma equivalente, usando una normal del tipo $$\mathcal{N}\left(0,\sqrt{\frac{2}{d_x}}\right)$$Esta inicialización estabiliza mejor tanto el **forward pass** como el **backward pass**, evitando problemas de activaciones o gradientes que desaparecen o explotan. Es la opción más adecuada para redes profundas con **ReLU**, mientras que resulta menos apropiada para **sigmoide** o **tanh**. En PyTorch puede usarse con `torch.nn.init.kaiming_normal_()`, y para variantes como **Leaky ReLU** se ajusta el factor mediante `torch.nn.init.calculate_gain`.
#### 2. Optimization
##### 2.1. Idea General
> La **optimización** en un modelo de _feedforward_ consiste en ajustar sus parámetros $\theta$ para **minimizar una función de pérdida diferenciable** $\ell(o,y)$, que mide la diferencia entre la salida del modelo $o$ y el valor real $y$. El modelo recibe una entrada $x$, la procesa mediante capas lineales y no lineales, produce una predicción $o=f(x,\theta)$, y a partir de ella se calcula la pérdida.
> 
> En tareas de **regresión**, la pérdida suele medirse mediante una **norma de distancia**, como **MSE** o **MAE**; en **clasificación**, se emplea típicamente la **cross-entropy**. Sobre un dataset, el objetivo es minimizar la pérdida esperada:  $$L(\theta)=\mathbb{E}_{x,y\sim D}[\ell(f(x,\theta),y)]$$El proceso de optimización es **iterativo**: primero se calculan las predicciones, después la pérdida, luego los gradientes respecto a los parámetros, y finalmente se actualizan esos parámetros mediante algoritmos de optimización. Intuitivamente, esto equivale a moverse por el **loss landscape** buscando un mínimo local o global de la función de pérdida. Este paisaje depende de la arquitectura del modelo, de sus parámetros y de los datos de entrada y salida.
##### 2.2. Gradient Descend
> El **gradient descent** es un algoritmo de optimización que actualiza iterativamente los parámetros del modelo en la dirección opuesta al gradiente de la función de pérdida:  $$\theta \leftarrow \theta - \eta ,\nabla_{\theta}L(\theta)$$donde (\eta) es la **learning rate**, que controla el tamaño del paso, y $\nabla_{\theta}L(\theta)$ es el gradiente de la pérdida respecto a los parámetros. La idea es repetir estas actualizaciones hasta acercarse a un mínimo de la función de pérdida.
>
> Existen tres variantes principales:
> - **Batch Gradient Descent:** calcula el gradiente usando **todo el dataset** en cada actualización:  $$\nabla_{\theta}L(\theta)=\frac{1}{N}\sum_{i=1}^{N}\nabla_{\theta}\ell(f(x_i,\theta),y_i)$$Produce una dirección de descenso estable, pero es costoso en tiempo y memoria para datasets grandes.
> 
> - **Stochastic Gradient Descent (SGD):** actualiza los parámetros con **una sola muestra** cada vez:  $$\nabla_{\theta}L(\theta)\approx \nabla_{\theta}\ell(f(x_i,\theta),y_i)$$Es más eficiente para datasets grandes, pero introduce mucho ruido en las actualizaciones y puede oscilar alrededor del mínimo.
> 
> - **Mini-Batch Gradient Descent:** usa un **pequeño batch** de tamaño $B$:  $$\nabla_{\theta}L(\theta)=\frac{1}{B}\sum_{i=1}^{B}\nabla_{\theta}\ell(f(x_i,\theta),y_i)$$Es la opción más usada en Deep Learning porque equilibra eficiencia computacional y estabilidad, además de aprovechar bien las operaciones matriciales en GPU.
> 
> ![[Pasted image 20260317125838.png]]
> 
> Un aspecto clave es la **learning rate**:
> - si es **demasiado pequeña**, la convergencia es muy lenta;
> - si es **adecuada**, el entrenamiento converge de forma suave y estable;
> - si es **demasiado grande**, puede producir oscilaciones, _overshooting_ o incluso divergencia.
> ![[Pasted image 20260317125902.png]]
> 
> En resumen, gradient descent busca minimizar la pérdida actualizando los parámetros paso a paso, y en la práctica suele usarse en su versión **mini-batch**, con especial cuidado en la elección de la **learning rate**.
