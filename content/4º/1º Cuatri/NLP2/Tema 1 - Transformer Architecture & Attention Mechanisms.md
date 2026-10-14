---
estado: pendiente de revisión
---

### I. The Transformer Architecture

#### 1. From Recurrence to Attention

> El **Transformer**, introducido en 2017, utiliza attention para relacionar los elementos de una secuencia sin recurrir a una cadena de estados recurrentes. Su arquitectura original se diseñó para tareas **sequence-to-sequence (seq2seq)**, como traducir una oración a otro idioma.
>
> En una RNN, procesar una posición depende del estado calculado en la anterior. En el Transformer, las representaciones de las posiciones de entrada pueden calcularse en paralelo mediante operaciones matriciales. Esto permitió mejorar tanto los resultados de traducción como la eficiencia del cálculo.
>
> La ausencia de recurrencia no implica que toda generación sea paralela: un decoder autoregresivo sigue generando cada token a partir de los anteriores. La paralelización se refiere al procesamiento de las posiciones que ya están disponibles.

#### 2. Transformer Families

> Las pilas de encoder y decoder pueden combinarse o utilizarse como modelos independientes. Las tres familias comparten componentes, pero difieren en la información a la que puede acceder cada posición y en la finalidad de su salida.

| Family | Funcionamiento | Salida y usos habituales | Example |
| --- | --- | --- | --- |
| **Encoder-decoder** | El encoder representa la entrada; el decoder genera una secuencia condicionada por esa representación y por los tokens de salida anteriores. | Traducción y otras tareas seq2seq, como speech recognition. | T5 |
| **Encoder-only** | Contextualiza los tokens de entrada usando el conjunto de la secuencia. | Representaciones para comprensión y text classification mediante una cabeza adicional. | BERT |
| **Decoder-only** | Procesa un prompt y predice los siguientes tokens con self-attention causal. | Generación de texto; otras tareas se expresan mediante instrucciones. | GPT |

> En el esquema, $N\times$ indica la repetición de un bloque. El decoder del modelo encoder-decoder incluye **cross-attention** sobre la salida del encoder; el decoder-only carece de esa subcapa.

![[apuntes-2b48110fe70d-p0010-7397967a7694.png]]

##### 2.1. Encoder-decoder Models

> La entrada $x_1,\ldots,x_n$ se convierte en una secuencia de representaciones contextuales. El decoder produce $y_1,\ldots,y_m$; las longitudes de entrada y salida pueden ser distintas.
>
> Si en el instante $t$ se han generado $y_1,\ldots,y_t$, el decoder utiliza ese prefijo y las salidas del encoder para predecir $y_{t+1}$. La generación comienza con un token como `[BOS]`. La capa **Linear + Softmax** transforma la representación del decoder en probabilidades sobre los tokens de salida.
>
> Hay dos fuentes de información: la self-attention del decoder relaciona posiciones de la salida disponible, mientras que la cross-attention consulta la entrada codificada. En esta última, las queries proceden del decoder y las keys y values de la salida del encoder.
>
> El mismo patrón puede aplicarse al reconocimiento del habla: una secuencia de características acústicas se codifica y el decoder genera una secuencia de palabras.

##### 2.2. Encoder-only Models

> Un encoder-only recibe $x_1,\ldots,x_n$ y devuelve nuevos embeddings $\bar{x}_1,\ldots,\bar{x}_n$. Su objetivo es construir una representación de calidad del significado de la entrada.
>
> Para clasificar un texto, se añade una **classification head** sobre una representación de la salida del encoder. Una capa lineal obtiene puntuaciones de clase y softmax las convierte en probabilidades. La representación de la secuencia puede obtenerse mediante un mecanismo de pooling; la cabeza de clasificación es un componente adicional al encoder.

##### 2.3. Decoder-only Models

> Un decoder-only funciona como **language model**: recibe una secuencia inicial o **prompt** y genera texto token a token. Su self-attention está enmascarada para que una posición no consulte tokens futuros.
>
> Muchas tareas de NLP pueden reformularse como generación de texto. Por ejemplo, un prompt puede pedir una etiqueta de clasificación, un resumen, una respuesta a una pregunta o la extracción de nombres. Esta versatilidad procede de expresar distintas tareas como instrucciones y respuestas textuales.

### II. Input and Contextual Embeddings

#### 3. Tokenization and Embedding Lookup

> El encoder contiene una pila de $N$ **encoder blocks**, cada uno con varias subcapas. Antes de entrar en esa pila, el texto se convierte en tokens, sus IDs se transforman en vectores y se incorpora información de posición.
>
> Un **tokenizer** convierte la oración en una secuencia de tokens. Cada token tiene un ID dentro de un vocabulario $V$. En el ejemplo «he picked the rose», los IDs ilustrativos son $101$, $245$, $387$ y $51$.
>
> Los IDs seleccionan filas de la **input embedding matrix**:
>
> $$
> E\in\mathbb{R}^{|V|\times d_{\mathrm{model}}}.
> $$
>
> Cada fila contiene un vector de dimensión $d_{\mathrm{model}}$. El ID actúa como índice de consulta; su valor numérico no representa por sí mismo el significado del token.
>
> La tabla muestra un ejemplo de lookup con $d_{\mathrm{model}}=4$.

| Token | Token ID | Input embedding |
| --- | ---: | --- |
| he | 101 | $[-0.34,\;0.07,\;-0.12,\;-0.28]$ |
| picked | 245 | $[-0.02,\;-0.27,\;0.15,\;0.17]$ |
| the | 387 | $[0.05,\;-0.09,\;0.11,\;-0.07]$ |
| rose | 51 | $[0.03,\;-0.01,\;-0.06,\;-0.05]$ |

> Si el mismo token aparece en dos oraciones, el lookup devuelve la misma fila de $E$. Esa representación inicial es **estática respecto al contexto**: «rose» parte del mismo vector tanto en «he picked the rose» como en «he finally rose».
>
> Los valores de $E$ pueden aprenderse durante el entrenamiento. Que un embedding sea estático respecto al contexto significa que el lookup no cambia con la oración, no que sus parámetros nunca se entrenen.

#### 4. Why Contextual Embeddings Matter

> En un espacio de embeddings, palabras con significados similares tienden a situarse cerca y palabras diferentes, lejos. Métodos como word2vec asignan un único vector a cada palabra. Ese punto fijo tiene dificultades para representar la **polisemia**, porque una misma forma puede tener varios significados.
>
> «Rose» puede referirse a una flor o al pasado de «rise». Otros ejemplos son «train» y «bat». La polisemia es frecuente; su proporción estimada en inglés puede variar ampliamente, aproximadamente entre el 40 % y el 80 %, según cómo se cuenten las palabras y sus sentidos.
>
> Un **contextual embedding** representa el significado de un token dentro de una secuencia concreta. Para un token $i$, su representación depende de su embedding inicial y del resto de embeddings:
>
> $$
> \operatorname{ContextualizedEmbedding}(x_i)
> =
> f(x_i,x_1,\ldots,x_{i-1},x_{i+1},\ldots,x_n).
> $$
>
> La función se implementa mediante las transformaciones del encoder. Attention permite reunir información del contexto para actualizar cada representación.

##### 4.1. A Geometric Example

> En una ilustración bidimensional, el eje horizontal representa «motion verbs» y el vertical, «flowers». «Lily» ocupa $(0,1)$, «climbed» ocupa $(1,0)$ y el embedding estático de «rose» se sitúa en $(1,1)$, combinando sus dos posibles sentidos.
>
> Al procesar «He picked the rose», la representación de «rose» se desplaza hacia las flores. En «She finally rose», se desplaza hacia los verbos de movimiento. Las coordenadas sirven como intuición: las dimensiones de un embedding real no tienen por qué corresponder a categorías semánticas tan explícitas.

![[apuntes-2b48110fe70d-p0044-8ffe538b2e91.png]]

> La actualización puede interpretarse como sumar un **change vector** $x'_i$ al vector de entrada:
>
> $$
> x_i^{\mathrm{new}}=x_i+x'_i.
> $$
>
> Por ejemplo, desde $(1,1)$, el desplazamiento $(-0.9,-0.1)$ produce $(0.1,0.9)$, cerca de «lily». Esta suma describe la residual connection de attention; el bloque completo también aplica normalización y una FFN.

> [!warning] Corrección
> En el material aparece $x_i^{\mathrm{new}}=(0.9,0.9)$ al sumar $x_i=(1,1)$ y $x'_i=(-0.9,-0.1)$, pero la expresión correcta es $(1,1)+(-0.9,-0.1)=(0.1,0.9)$, sumando componente a componente.
> Fuente de comprobación: [NumPy: suma elemento a elemento](https://numpy.org/doc/stable/reference/generated/numpy.add.html)

### III. Single-head Self-attention

#### 5. Attention as Weighted Aggregation

> Consideremos «The match burned quickly», con embeddings $x_1,x_2,x_3,x_4$. «Match» puede significar una cerilla o un partido. «Burned» aporta información especialmente útil para determinar el sentido de «match».
>
> Una primera idea sería reunir contexto sumando todos los embeddings:
>
> $$
> x'_i=\sum_{j=1}^{L}x_j.
> $$
>
> El problema es que todos los tokens contribuyen por igual. Una suma ponderada permite asignar más relevancia a unos que a otros:
>
> $$
> x'_i=\sum_{j=1}^{L}\alpha_jx_j.
> $$
>
> Attention desarrolla esta idea de dos maneras: calcula pesos específicos para la consulta del token $i$ y transforma la información que cada token $j$ comparte. Por eso, la suma final combina **value vectors**, que no tienen por qué coincidir con los embeddings originales.

#### 6. Queries, Keys and Values

> Cada embedding produce tres proyecciones aprendidas. Se utilizan vectores fila, de modo que las matrices de pesos multiplican por la derecha.

| Vector | Proyección | Dimensión | Interpretación |
| --- | --- | --- | --- |
| **Query** $q_i$ | $q_i=x_iW^Q$ | $1\times d_q$ | Qué información contextual necesita el token $i$. |
| **Key** $k_i$ | $k_i=x_iW^K$ | $1\times d_k$ | Para qué consultas puede ser relevante el token $i$. |
| **Value** $v_i$ | $v_i=x_iW^V$ | $1\times d_v$ | Qué información aporta el token $i$ cuando se le presta atención. |

> Las dimensiones de las matrices son:
>
> $$
> W^Q\in\mathbb{R}^{d_{\mathrm{model}}\times d_q},
> \qquad
> W^K\in\mathbb{R}^{d_{\mathrm{model}}\times d_k},
> \qquad
> W^V\in\mathbb{R}^{d_{\mathrm{model}}\times d_v}.
> $$
>
> Para calcular el producto escalar entre query y key necesitamos **$d_q=d_k$**. La dimensión $d_v$ puede ser distinta. Las mismas matrices se aplican a todos los tokens de una cabeza.
>
> En la analogía, la query de «match» busca contexto para aclarar una palabra polisémica; la key de «burned» indica su relevancia para esa consulta y su value aporta información sobre quemarse. Son interpretaciones pedagógicas de vectores aprendidos, no preguntas textuales que el modelo genere internamente.
>
> Se denomina **self-attention** porque queries, keys y values proceden de la misma secuencia de representaciones, aunque sus proyecciones sean diferentes.

#### 7. Scaled Dot-product Attention

##### 7.1. Attention Scores

> Para actualizar el token $i$, comparamos su query con todas las keys. El producto escalar cuantifica su compatibilidad:
>
> $$
> \operatorname{att\text{-}score}(q_i,k_j)
> =
> \frac{q_i\cdot k_j}{\sqrt{d_k}}
> \in\mathbb{R}.
> $$
>
> Por ejemplo, $q_2\cdot k_3$ expresa la compatibilidad entre la consulta de «match» y la key de «burned». Las filas corresponden a tokens que consultan y las columnas a tokens consultados.
>
> Los scores pueden ser negativos y todavía no son probabilidades. Tampoco tienen por qué ser simétricos: $q_i\cdot k_j$ y $q_j\cdot k_i$ utilizan proyecciones y consultas diferentes.
>
> El factor $1/\sqrt{d_k}$ controla la escala. Si las componentes de query y key fueran independientes, con media $0$ y varianza $1$, la varianza de su producto escalar sería $d_k$. Al dividir por $\sqrt{d_k}$ se mantiene una escala comparable y se reduce la saturación de softmax, que produciría gradientes pequeños.

##### 7.2. Attention Weights

> Aplicamos **softmax por filas**, manteniendo fija la query y normalizando sobre todas las keys:
>
> $$
> \operatorname{att\text{-}weight}(q_i,k_j)
> =
> \frac{
> \exp\!\left(\operatorname{att\text{-}score}(q_i,k_j)\right)
> }{
> \displaystyle\sum_{\ell=1}^{L}
> \exp\!\left(\operatorname{att\text{-}score}(q_i,k_\ell)\right)
> }.
> $$
>
> Con scores finitos y más de un token, los pesos están entre $0$ y $1$ y cada fila suma $1$. Las columnas no tienen por qué sumar $1$: cada token reparte su propia atención de forma independiente.
>
> Si todos los scores de una fila son iguales, sus pesos son uniformes. Si uno es mucho mayor que los demás, concentra gran parte de la atención.

##### 7.3. Weighted Sum, Output Projection and Residual Addition

> Una vez calculados los pesos, reunimos la información de los values:
>
> $$
> \operatorname{att\text{-}output}(x_i)
> =
> \sum_{j=1}^{L}
> \operatorname{att\text{-}weight}(q_i,k_j)v_j
> \in\mathbb{R}^{1\times d_v}.
> $$
>
> Las **keys determinan los pesos** y los **values aportan el contenido**. La suma puede incluir el propio token, porque también dispone de una key y un value.
>
> Esta salida tiene dimensión $d_v$. Para poder sumarla al embedding original, se proyecta a $d_{\mathrm{model}}$:
>
> $$
> W^O\in\mathbb{R}^{d_v\times d_{\mathrm{model}}},
> \qquad
> x'_i=\operatorname{att\text{-}output}(x_i)W^O,
> \qquad
> x_i^{\mathrm{new}}=x_i+x'_i.
> $$
>
> Hay tres objetos distintos: la mezcla de values, el change vector tras $W^O$ y la representación obtenida al sumar la residual connection. Confundirlos oculta por qué se necesita la proyección de salida.

##### 7.4. Single-token Algorithm

> Para actualizar un embedding $x$, las entradas son el conjunto de embeddings $x_t$, $t=1,\ldots,T$, y las matrices aprendidas $W^Q,W^K,W^V,W^O$, con dimensiones compatibles.
>
> 1. Calcular $q=xW^Q$.
> 2. Para cada $t$, calcular $k_t=x_tW^K$ y $v_t=x_tW^V$.
> 3. Calcular todos los scores $q\cdot k_t/\sqrt{d_k}$.
> 4. Normalizarlos conjuntamente mediante softmax.
> 5. Obtener $\operatorname{att\text{-}output}(x)=\sum_{t=1}^{T}\operatorname{att\text{-}weight}(q,k_t)v_t$.
> 6. Proyectar $x'=\operatorname{att\text{-}output}(x)W^O$ y devolver $x^{\mathrm{new}}=x+x'$.
>
> Es un cálculo hacia delante con un número finito de operaciones; no es un procedimiento iterativo con un criterio de convergencia. En self-attention, el conjunto consultado incluye normalmente la posición actual.

#### 8. Worked Attention Examples

##### 8.1. The Match Burned Quickly

> Para los tokens «The», «match», «burned» y «quickly», consideramos la siguiente matriz de scores:
>
> $$
> \begin{bmatrix}
> -1.0&1.5&0.2&-0.5\\
> -0.5&-0.5&3.0&-0.5\\
> 0.2&0.8&0.8&0.2\\
> 1.0&1.0&1.0&1.0
> \end{bmatrix}.
> $$
>
> Tras normalizar cada fila, los pesos aproximados son:
>
> $$
> \begin{bmatrix}
> 0.055&0.671&0.183&0.091\\
> 0.028&0.028&0.917&0.028\\
> 0.177&0.323&0.323&0.177\\
> 0.250&0.250&0.250&0.250
> \end{bmatrix}.
> $$
>
> Las pequeñas diferencias respecto a una suma exacta de $1$ proceden de aproximar los decimales. Para «match», la salida es aproximadamente:
>
> $$
> \operatorname{att\text{-}output}(x_2)
> \approx
> 0.028v_1+0.028v_2+0.917v_3+0.028v_4.
> $$
>
> «Burned» recibe cerca del $92\,\%$ de la atención de «match». En cambio, la última fila tiene scores iguales y reparte la atención por igual entre las cuatro posiciones.

##### 8.2. Thinking Machines

> En un ejemplo de dos tokens, la query de «Thinking» produce productos escalares $112$ y $96$ con las keys de «Thinking» y «Machines». Si $\sqrt{d_k}=8$, los scores son $14$ y $12$:
>
> $$
> \operatorname{softmax}([14,12])
> \approx[0.88,0.12].
> $$
>
> La salida correspondiente a esa query combina $0.88v_1+0.12v_2$. Aunque las tres proyecciones se obtienen de los mismos embeddings, cada una cumple una función distinta en el cálculo.

##### 8.3. Three Inputs with Explicit Projections

> El siguiente ejemplo desarrolla las operaciones para tres embeddings, con $d_{\mathrm{model}}=4$ y $d_q=d_k=d_v=3$:
>
> $$
> x_1=[1,0,1,0],\qquad
> x_2=[0,2,0,2],\qquad
> x_3=[1,1,1,1].
> $$
>
> Las matrices de proyección son:
>
> $$
> W^Q=
> \begin{bmatrix}
> 1&0&1\\
> 1&0&0\\
> 0&0&1\\
> 0&1&1
> \end{bmatrix},
> \quad
> W^K=
> \begin{bmatrix}
> 0&0&1\\
> 1&1&0\\
> 0&1&0\\
> 1&1&0
> \end{bmatrix},
> \quad
> W^V=
> \begin{bmatrix}
> 0&2&0\\
> 0&3&0\\
> 1&0&3\\
> 1&1&0
> \end{bmatrix}.
> $$
>
> Al multiplicar cada embedding por cada matriz se obtiene:

| Input | Query | Key | Value |
| --- | --- | --- | --- |
| $x_1$ | $[1,0,2]$ | $[0,1,1]$ | $[1,2,3]$ |
| $x_2$ | $[2,2,2]$ | $[4,4,0]$ | $[2,8,0]$ |
| $x_3$ | $[2,1,3]$ | $[2,3,1]$ | $[2,6,3]$ |

> Por ejemplo, $k_1=[1,0,1,0]W^K=[0,1,1]$: el producto selecciona y suma las filas primera y tercera de $W^K$.
>
> Para simplificar el ejemplo, se **omite el escalado** por $\sqrt{d_k}$. Con la query $q_1=[1,0,2]$, los scores son:
>
> $$
> [q_1\cdot k_1,\;q_1\cdot k_2,\;q_1\cdot k_3]=[2,4,4].
> $$
>
> El esquema utiliza una aproximación gruesa de sus pesos, $[0,0.5,0.5]$, para ilustrar la mezcla. Esos valores no son el softmax exacto: el primer peso es positivo. Con esa aproximación, las contribuciones representadas son:
>
> $$
> 0v_1=[0,0,0],\qquad
> 0.5v_2=[1,4,0],\qquad
> 0.5v_3=[1,3,1.5],
> $$
>
> y su suma da:
>
> $$
> \operatorname{att\text{-}output}(x_1)\approx[2,7,1.5].
> $$
>
> Este desarrollo llega hasta la mezcla de values. Para obtener el change vector faltaría aplicar $W^O$ y, después, sumar el embedding de entrada.

### IV. Multi-head Attention and Matrix Computation

#### 9. Multiple Attention Heads

##### 9.1. Independent Projections and Dependencies

> Una sola cabeza produce una mezcla de información contextual. **Multi-head attention** calcula varias mezclas en paralelo para que el modelo pueda captar distintas dependencias y distintos subespacios de representación.
>
> Cada cabeza $\ell\in\{1,\ldots,h\}$ tiene sus propias matrices $W_\ell^Q,W_\ell^K,W_\ell^V$:
>
> $$
> q_i^\ell=x_iW_\ell^Q,\qquad
> k_j^\ell=x_jW_\ell^K,\qquad
> v_j^\ell=x_jW_\ell^V.
> $$
>
> A partir de sus propios scores y pesos, cada cabeza produce:
>
> $$
> \operatorname{att\text{-}output}^{\ell}(x_i)
> =
> \sum_{j=1}^{L}
> \operatorname{att\text{-}weight}(q_i^\ell,k_j^\ell)v_j^\ell
> \in\mathbb{R}^{1\times d_v}.
> $$
>
> Las cabezas aplican el mismo procedimiento, pero no comparten sus proyecciones. Pueden aprender relaciones distintas; no se les asigna de antemano un papel gramatical específico.

##### 9.2. Concatenation and Output Projection

> Las salidas de las $h$ cabezas se **concatenan**, manteniendo separados sus componentes. El vector concatenado tiene dimensión $h\,d_v$ y se proyecta con una única matriz de salida:
>
> $$
> W^O\in\mathbb{R}^{h d_v\times d_{\mathrm{model}}},
> $$
>
> $$
> x'_i=
> \operatorname{Concat}\!\left(
> \operatorname{att\text{-}output}^{1}(x_i),\ldots,
> \operatorname{att\text{-}output}^{h}(x_i)
> \right)W^O,
> \qquad
> x_i^{\mathrm{new}}=x_i+x'_i.
> $$
>
> El diagrama se lee de abajo arriba: proyecciones lineales, atención en paralelo, concatenación y proyección final. Dentro de cada cabeza, primero se multiplican queries y keys, se escala y se aplica softmax; esos pesos multiplican los values.

![[apuntes-2b48110fe70d-p0128-8d6305f2b422.png]]

> Para actualizar un token con varias cabezas, se repiten los pasos de single-head attention para cada $\ell$, se concatenan las mezclas resultantes, se aplica $W^O$ y se devuelve $x+x'$. La suma residual se realiza después de combinar las cabezas.
>
> En un ejemplo con dos cabezas:
>
> $$
> \operatorname{att\text{-}output}^{1}(x_1)=[2,7,1.5],
> \qquad
> \operatorname{att\text{-}output}^{2}(x_1)=[2,7.8,0.3],
> $$
>
> $$
> \operatorname{Concat}(\cdots)=[2,7,1.5,2,7.8,0.3]
> \in\mathbb{R}^{1\times 6}.
> $$
>
> Si $d_{\mathrm{model}}=4$, $W^O$ tiene tamaño $6\times4$. El ejemplo ilustra un change vector $[1,2,1,2]$, que sumado a $x_1=[1,0,1,0]$ produce $[2,2,2,2]$. Los valores concretos de esa proyección dependen de $W^O$; concatenar no determina por sí solo el resultado.

#### 10. Attention in Matrix Form

##### 10.1. Parallel Computation and Dimensions

> Apilamos los embeddings como filas de:
>
> $$
> X\in\mathbb{R}^{L\times d_{\mathrm{model}}}.
> $$
>
> Para una cabeza, todos los tokens se proyectan simultáneamente:
>
> $$
> Q=XW^Q\in\mathbb{R}^{L\times d_q},
> \qquad
> K=XW^K\in\mathbb{R}^{L\times d_k},
> \qquad
> V=XW^V\in\mathbb{R}^{L\times d_v}.
> $$
>
> Como $d_q=d_k$, la matriz $QK^\top$ tiene tamaño $L\times L$. Su entrada $(i,j)$ es $q_i\cdot k_j$. La operación completa de una cabeza es:
>
> $$
> \operatorname{Attention}(Q,K,V)
> =
> \operatorname{softmax}\!\left(
> \frac{QK^\top}{\sqrt{d_k}}
> \right)V
> \in\mathbb{R}^{L\times d_v},
> $$
>
> donde softmax actúa **por filas**, sobre el eje de las keys.

| Objeto | Dimensión | Significado |
| --- | --- | --- |
| $X$ | $L\times d_{\mathrm{model}}$ | Representaciones de entrada. |
| $Q$, $K$ | $L\times d_k$ | Una query y una key por token. |
| $V$ | $L\times d_v$ | Un value por token. |
| $QK^\top/\sqrt{d_k}$ | $L\times L$ | Compatibilidades entre cada query y todas las keys. |
| $\operatorname{softmax}(QK^\top/\sqrt{d_k})$ | $L\times L$ | Distribuciones de atención por query. |
| $\operatorname{Attention}(Q,K,V)$ | $L\times d_v$ | Mezclas de values. |

> En el siguiente esquema, $n$ es el número de tokens, equivalente a $L$, y $d$ es el tamaño del embedding, equivalente a $d_{\mathrm{model}}$. $W_q,W_k,W_v$ representan las proyecciones $W^Q,W^K,W^V$; $A$ es la matriz de pesos y $Z$ la mezcla de values. El esquema enfatiza las dimensiones; en scaled dot-product attention se incluye el factor $1/\sqrt{d_k}$ antes de softmax.

![[apuntes-2b48110fe70d-p0122-0b1efa0fd60f.png]]

##### 10.2. Multi-head Matrix Form

> Para cada cabeza $\ell$ se calculan $Q_\ell=XW_\ell^Q$, $K_\ell=XW_\ell^K$ y $V_\ell=XW_\ell^V$. Después:
>
> $$
> C=
> \operatorname{Concat}\!\left(
> \operatorname{Attention}(Q_1,K_1,V_1),\ldots,
> \operatorname{Attention}(Q_h,K_h,V_h)
> \right)
> \in\mathbb{R}^{L\times h d_v},
> $$
>
> $$
> X'=\operatorname{MultiHead}(X)=CW^O
> \in\mathbb{R}^{L\times d_{\mathrm{model}}}.
> $$
>
> La concatenación se realiza sobre las características, conservando las $L$ filas. **MultiHead devuelve los change vectors**; la residual connection añade después $X$. Algunos desarrollos utilizan $T$ para la longitud de la secuencia en lugar de $L$.

##### 10.3. She Loves Playing Pool

> Un ejemplo matricial utiliza $L=4$ y $d_{\mathrm{model}}=4$. Las filas corresponden, en orden, a «She», «loves», «playing» y «pool»:
>
> $$
> X=
> \begin{bmatrix}
> 0&1&2&3\\
> 1&2&3&0\\
> 2&3&0&1\\
> 3&0&1&2
> \end{bmatrix}.
> $$
>
> Con las proyecciones coherentes con el desarrollo final:
>
> $$
> W^Q=
> \begin{bmatrix}0&1\\0&0\\1&0\\0&0\end{bmatrix},
> \qquad
> W^K=
> \begin{bmatrix}1&0\\0&1\\0&0\\0&0\end{bmatrix},
> \qquad
> W^V=
> \begin{bmatrix}0&2\\1&1\\2&0\\3&2\end{bmatrix},
> $$
>
> se obtiene:
>
> $$
> Q=
> \begin{bmatrix}2&0\\3&1\\0&2\\1&3\end{bmatrix},
> \qquad
> K=
> \begin{bmatrix}0&1\\1&2\\2&3\\3&0\end{bmatrix},
> \qquad
> V=
> \begin{bmatrix}14&7\\8&4\\6&9\\8&10\end{bmatrix}.
> $$

> [!warning] Corrección
> En el material aparece inicialmente $W^Q=\begin{bmatrix}0&1\\1&2\\2&3\\3&0\end{bmatrix}$ junto a la matriz $Q$ anterior, pero la expresión correcta que permite obtener esa $Q$ es $W^Q=\begin{bmatrix}0&1\\0&0\\1&0\\0&0\end{bmatrix}$, utilizada después en el propio desarrollo. Por ejemplo, con la primera matriz, $[0,1,2,3]W^Q=[14,8]$, no $[2,0]$.
> Fuente de comprobación: [NumPy: producto matricial](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html)

> La transposición de $K$ coloca cada key en una columna. Al multiplicar:
>
> $$
> QK^\top=
> \begin{bmatrix}
> 0&2&4&6\\
> 1&5&9&9\\
> 2&4&6&0\\
> 3&7&11&3
> \end{bmatrix}.
> $$
>
> Este ejemplo ilustra la atención **sin escalado**; utiliza $\operatorname{softmax}(QK^\top)$, no $\operatorname{softmax}(QK^\top/\sqrt{2})$. No hay que trasladar esa omisión a la definición general.
>
> Los pesos, aproximados, son:
>
> $$
> \begin{bmatrix}
> 0.002&0.016&0.117&0.865\\
> 0.000&0.009&0.495&0.495\\
> 0.016&0.117&0.865&0.002\\
> 0.000&0.018&0.981&0.000
> \end{bmatrix}.
> $$
>
> Un valor mostrado como $0.000$ representa aquí un peso positivo muy pequeño. La primera query concentra la atención en «pool»; la segunda la reparte principalmente entre «playing» y «pool».
>
> Multiplicar esa distribución por $V$ da la mezcla de values de cada fila. Por ejemplo, para «She»:
>
> $$
> \operatorname{att\text{-}output}(x_{\mathrm{She}})
> \approx
> 0.002[14,7]+0.016[8,4]
> +0.117[6,9]+0.865[8,10]
> \approx[7.78,9.78].
> $$
>
> Las demás salidas se sitúan aproximadamente en $[7.0,9.4]$, $[6.4,8.4]$ y $[6.0,8.9]$. Cada fila conserva su propia combinación contextual. Todas las salidas tienen dimensión $d_v=2$; la proyección con $W^O$ las devolvería a dimensión $4$ antes de la suma residual.

#### 11. Implementing Attention Efficiently

##### 11.1. A Direct Implementation with Loops

> La implementación directa calcula un score por cada pareja de tokens y acumula la mezcla de values mediante bucles. El código devuelve $X+\operatorname{Attention}(Q,K,V)W^O$; no incluye todavía layer normalization ni la FFN del encoder.
>
> Se necesitan NumPy, softmax de SciPy y un reloj para el ejemplo de medida de tiempo. Las matrices de entrada deben tener dimensiones compatibles y $X$ debe contener embeddings de tipo flotante.

```python
import time
import numpy as np
from scipy.special import softmax


def single_head_attention(X, W_Q, W_K, W_V, W_O):
    """Single-head attention con bucles explícitos y suma residual."""
    T, d_model = X.shape
    d_k = W_K.shape[1]

    Q = X @ W_Q
    K = X @ W_K
    V = X @ W_V

    X_new = np.zeros_like(X)
    scale = np.sqrt(d_k)

    for i in range(T):
        q_i = Q[i]
        scores = np.zeros(T)

        # Comparar la query actual con todas las keys.
        for j in range(T):
            k_j = K[j]
            scores[j] = (q_i @ k_j) / scale

        weights = softmax(scores)
        att_out = np.zeros(V.shape[1])

        # Acumular la información compartida por cada posición.
        for j in range(T):
            att_out += weights[j] * V[j]

        x_prime_i = att_out @ W_O
        X_new[i] = X[i] + x_prime_i

    return X_new
```

> Cada query consulta todas las keys de la misma entrada. Los nuevos embeddings se guardan en `X_new` y no sustituyen a `X` durante los bucles; todas las posiciones se actualizan a partir de las mismas representaciones de entrada.

##### 11.2. Vectorized Implementation

> La versión matricial realiza las mismas operaciones sin bucles de Python sobre los tokens. `axis=1` es decisivo: normaliza cada fila de scores sobre las keys.

```python
def single_head_attention_vectorized(X, W_Q, W_K, W_V, W_O):
    """Single-head attention mediante operaciones matriciales."""
    T, d_model = X.shape
    d_k = W_K.shape[1]

    Q = X @ W_Q
    K = X @ W_K
    V = X @ W_V

    scores = (Q @ K.T) / np.sqrt(d_k)  # (T, T)
    weights = softmax(scores, axis=1)
    att_out = weights @ V             # (T, d_v)

    X_new = X + att_out @ W_O         # (T, d_model)
    return X_new
```

> La vectorización permite utilizar multiplicaciones matriciales optimizadas y procesar las queries en paralelo. Sigue existiendo una matriz de $T\times T$ relaciones: eliminar los bucles de Python no elimina el número cuadrático de parejas.

##### 11.3. Timing Example

> El ejemplo utiliza $T=1000$, $d_{\mathrm{model}}=64$, $d_k=32$ y $d_v=32$. Los embeddings y las matrices se generan con una distribución normal estándar y semilla $0$. Se compara el mismo cálculo con las mismas entradas.

```python
rng = np.random.default_rng(0)
T = 1000
d_model = 64
d_k = 32
d_v = 32

X = rng.normal(size=(T, d_model))
W_Q = rng.normal(size=(d_model, d_k))
W_K = rng.normal(size=(d_model, d_k))
W_V = rng.normal(size=(d_model, d_v))
W_O = rng.normal(size=(d_v, d_model))

# Alias empleado en la comparación de tiempos.
single_head_attention_naive = single_head_attention

t0 = time.perf_counter()
X_new_naive = single_head_attention_naive(X, W_Q, W_K, W_V, W_O)
t1 = time.perf_counter()

t2 = time.perf_counter()
X_new_vec = single_head_attention_vectorized(X, W_Q, W_K, W_V, W_O)
t3 = time.perf_counter()

naive_ms = (t1 - t0) * 1000
vec_ms = (t3 - t2) * 1000
speedup = naive_ms / vec_ms if vec_ms > 0 else float("inf")

print("Input shape:", X.shape)
print("Output shape:", X_new_vec.shape)
print(f"Naive time:      {naive_ms:.2f} ms")
print(f"Vectorized time: {vec_ms:.2f} ms")
print(f"Speedup (naive/vec): {speedup:.2f}x")
```

> Las matrices de entrada y salida tienen tamaño $(1000,64)$. Una medida inicial del cálculo con bucles dio $3379.22$ ms. En la comparación conjunta, los tiempos ilustrativos fueron $4871.70$ ms con bucles y $23.24$ ms con operaciones matriciales, con una aceleración indicada de aproximadamente $210\times$.
>
> Esos tiempos son resultados concretos de un entorno de ejecución; no constituyen una garantía de aceleración para cualquier máquina, longitud o implementación.

##### 11.4. Inspecting Attention Heads

> **exBERT** y **BertViz** permiten visualizar los patrones de atención por capa y cabeza. Por ejemplo, se pueden inspeccionar las cabezas de BERT en «The match burned quickly, leaving behind only a thin trail of smoke and the faint smell of sulfur».
>
> Estas visualizaciones ayudan a observar qué posiciones reciben más peso y a proponer interpretaciones de las dependencias aprendidas. Muchas cabezas son difíciles de interpretar; una distribución de atención por sí sola no describe toda la transformación de la representación.

### V. The Encoder Block

#### 12. Residual Connections

> Cada encoder block contiene una subcapa de **multi-head self-attention** y una **position-wise feed-forward network**. Cada subcapa está rodeada por una residual connection, seguida de layer normalization.
>
> La residual connection de attention añade los change vectors a las representaciones de entrada:
>
> $$
> f_{\mathrm{residual}}(X,X')=X+X'.
> $$
>
> Esta ruta permite conservar la información de entrada mientras se aprende una actualización. También facilita el aprendizaje en redes profundas. Para que la suma esté definida, entrada y actualización deben tener el mismo tamaño $L\times d_{\mathrm{model}}$.
>
> En el diagrama, las rutas discontinuas llevan la entrada de cada subcapa hasta la suma correspondiente. La primera operación **Add & Normalize** combina la entrada de attention con su salida; la segunda aplica el mismo patrón alrededor de la FFN.

![[apuntes-2b48110fe70d-p0132-7937e6701143.png]]

#### 13. Layer Normalization

##### 13.1. Definition and Role

> **Layer normalization** estabiliza la escala de las activaciones y ayuda al entrenamiento. En el encoder se aplica **por separado a cada embedding**, calculando sus estadísticas sobre las características de ese vector.
>
> Para $x=[x_1,\ldots,x_d]$, donde $d=d_{\mathrm{model}}$, definimos:
>
> $$
> \mu=\frac{1}{d}\sum_{k=1}^{d}x_k,
> \qquad
> \sigma^2=\frac{1}{d}\sum_{k=1}^{d}(x_k-\mu)^2,
> $$
>
> $$
> \operatorname{LN}(x)
> =
> \gamma\frac{x-\mu}{\sqrt{\sigma^2+\epsilon}}+\beta.
> $$
>
> $\gamma,\beta\in\mathbb{R}^{d}$ son parámetros aprendidos de escala y desplazamiento; la multiplicación por $\gamma$ se realiza componente a componente. $\epsilon>0$ evita la división por cero y problemas numéricos si la varianza es muy pequeña.
>
> Antes de aplicar $\gamma$ y $\beta$, el vector centrado y normalizado tiene media $0$ y varianza $\sigma^2/(\sigma^2+\epsilon)$, próxima a $1$ cuando $\epsilon$ es pequeño frente a $\sigma^2$. La varianza es exactamente $1$ en el caso ideal $\epsilon=0$ y $\sigma^2>0$.
>
> Tras aplicar parámetros aprendidos distintos por componente, la salida no tiene por qué mantener media $0$ ni varianza $1$. Estas cifras describen la normalización intermedia bajo sus hipótesis, no una restricción fija de la salida final.

##### 13.2. Numerical Example

> Consideremos dos embeddings de tres componentes:
>
> $$
> X=
> \begin{bmatrix}
> 0.2&0.1&0.3\\
> 0.5&0.1&0.1
> \end{bmatrix}.
> $$
>
> Calculamos estadísticas independientes para cada fila:
>
> $$
> \mu_1=\frac{0.2+0.1+0.3}{3}=0.2,
> $$
>
> $$
> \sqrt{\sigma_1^2}
> =
> \sqrt{\frac{(0.2-0.2)^2+(0.1-0.2)^2+(0.3-0.2)^2}{3}}
> \approx0.0816,
> $$
>
> $$
> \mu_2=\frac{0.5+0.1+0.1}{3}\approx0.2333,
> $$
>
> $$
> \sqrt{\sigma_2^2}
> =
> \sqrt{\frac{(0.5-\mu_2)^2+(0.1-\mu_2)^2+(0.1-\mu_2)^2}{3}}
> \approx0.1885.
> $$
>
> Con $\gamma$ igual a un vector de unos, $\beta$ igual a un vector de ceros y $\epsilon=0$, la primera fila se transforma en:
>
> $$
> \left[
> \frac{0.2-0.2}{0.0816},
> \frac{0.1-0.2}{0.0816},
> \frac{0.3-0.2}{0.0816}
> \right]
> \approx[0,-1.225,1.225].
> $$
>
> La segunda se obtiene restando su propia media y dividiendo por su propia desviación estándar:
>
> $$
> \left[
> \frac{0.5-0.2333}{0.1885},
> \frac{0.1-0.2333}{0.1885},
> \frac{0.1-0.2333}{0.1885}
> \right]
> \approx[1.41,-0.71,-0.71].
> $$
>
> Sin aproximaciones decimales, ambas filas tienen media $0$ y varianza $1$ bajo estas hipótesis. Las estadísticas de una fila no dependen de los tokens de la otra.

#### 14. Position-wise Feed-forward Network

> Después de self-attention y de su operación Add & Norm, cada representación pasa por la misma **feed-forward network (FFN)** de su bloque. Se aplica a todas las posiciones por separado y con los mismos parámetros:
>
> $$
> \operatorname{FF}(z_i)
> =
> \max(0,z_iW_1+b_1)W_2+b_2.
> $$
>
> Hay dos transformaciones afines y una **ReLU** entre ellas. La primera expande la dimensión de $d_{\mathrm{model}}$ a $d_{\mathrm{ff}}$; la segunda devuelve el vector a $d_{\mathrm{model}}$.

| Term | Dimensions |
| --- | --- |
| $z_i$ | $1\times d_{\mathrm{model}}$ |
| $W_1$ | $d_{\mathrm{model}}\times d_{\mathrm{ff}}$ |
| $b_1$ | $1\times d_{\mathrm{ff}}$ |
| $\max(0,z_iW_1+b_1)$ | $1\times d_{\mathrm{ff}}$ |
| $W_2$ | $d_{\mathrm{ff}}\times d_{\mathrm{model}}$ |
| $b_2$ | $1\times d_{\mathrm{model}}$ |
| $\operatorname{FF}(z_i)$ | $1\times d_{\mathrm{model}}$ |

> En el Transformer original, $d_{\mathrm{model}}=512$ y $d_{\mathrm{ff}}=2048$. La expansión y la activación no lineal aportan capacidad para transformar las características de cada representación.
>
> **Attention mezcla información entre tokens**; la **FFN transforma las características de cada token**. La FFN no consulta otras posiciones directamente, aunque su entrada ya incorpora contexto por la attention anterior.
>
> Compartir la FFN entre posiciones no significa que todos los bloques de la pila tengan los mismos parámetros: cada bloque puede aprender sus propias transformaciones.

#### 15. Complete Encoder Block

> Para una entrada $X\in\mathbb{R}^{T\times d_{\mathrm{model}}}$, el bloque combina las dos subcapas:
>
> $$
> Z_1=
> \operatorname{LayerNorm}\!\left(
> X+\operatorname{MultiHead}(X)
> \right),
> $$
>
> $$
> Z_2=
> \operatorname{LayerNorm}\!\left(
> Z_1+\operatorname{FFN}(Z_1)
> \right),
> \qquad Y=Z_2.
> $$
>
> La FFN actúa por filas y las dos normalizaciones pertenecen a subcapas distintas. La salida $Y$ conserva el número de posiciones y la dimensión del embedding.
>
> Este orden es **post-norm**: primero se calcula la subcapa, se suma su entrada y después se normaliza. La descripción del bloque emplea este orden de operaciones.

> [!warning] Corrección
> En el material aparece $Z_2=\operatorname{LayerNorm}(H+\operatorname{FFN}(H))$ sin definir $H$, pero la expresión correcta, con la notación del bloque, es $Z_2=\operatorname{LayerNorm}(Z_1+\operatorname{FFN}(Z_1))$. Si se utiliza $H$, debe definirse como $H=Z_1$, la salida de la primera subcapa.
> Fuente de comprobación: [Attention Is All You Need: encoder stack](https://arxiv.org/html/1706.03762v7#S3.SS1)

### VI. Positional Encodings

#### 16. Why Self-attention Needs Position

##### 16.1. The Word-order Problem

> El orden puede cambiar los papeles gramaticales y el significado: «The dog chases the cat» y «The cat chases the dog» contienen las mismas palabras, pero intercambian quién realiza la acción.
>
> Sin información de posición, la self-attention del encoder calcula queries, keys y values a partir del contenido de los tokens. Para el token «dog», el peso de «cat» en «dog chases cat» es:
>
> $$
> \frac{
> \exp(q_{\mathrm{dog}}\cdot k_{\mathrm{cat}}/\sqrt{d_k})
> }{
> \exp(q_{\mathrm{dog}}\cdot k_{\mathrm{dog}}/\sqrt{d_k})
> +\exp(q_{\mathrm{dog}}\cdot k_{\mathrm{chases}}/\sqrt{d_k})
> +\exp(q_{\mathrm{dog}}\cdot k_{\mathrm{cat}}/\sqrt{d_k})
> }.
> $$
>
> En «cat chases dog», la query de «dog» y las keys son las mismas. El numerador no cambia y el denominador contiene los mismos tres términos, solo reordenados. Por tanto, el peso asociado a cada palabra sigue siendo el mismo.
>
> También permanece igual la mezcla de values del token «dog»:
>
> $$
> \operatorname{att\text{-}output}(x_{\mathrm{dog}})
> =
> \sum_j
> \operatorname{att\text{-}weight}(q_{\mathrm{dog}},k_j)v_j.
> $$
>
> Los pesos no tienen que ser uniformes: son los mismos para las mismas palabras en ambas secuencias. Sin posición, el contenido de «dog» no indica si está antes o después del verbo.

> [!warning] Corrección
> En el material aparece que self-attention sin posiciones es formalmente «permutation-invariant», pero la expresión correcta para la salida secuencial completa es **permutation-equivariant**: $f(\Pi X)=\Pi f(X)$, donde $\Pi$ permuta las filas. Las representaciones se reordenan con sus tokens. Para una query fija, la agregación sí es invariante al reordenar conjuntamente las parejas key-value.
> Fuente de comprobación: [Set Transformer: permutation equivariance](https://proceedings.mlr.press/v97/lee19d/lee19d.pdf)

##### 16.2. Position-aware Inputs

> Introducimos un **positional encoding** $p_i\in\mathbb{R}^{d_{\mathrm{model}}}$ en cada posición. Si $e_i$ es el embedding obtenido del lookup, la representación que entra en el primer bloque es:
>
> $$
> e_i+p_i.
> $$
>
> La posición y el contenido se suman porque tienen la misma dimensión. Con la notación $x_i$ para el embedding sin posición:
>
> $$
> q_i=(x_i+p_i)W^Q,
> \qquad
> k_j=(x_j+p_j)W^K.
> $$
>
> Al cambiar las posiciones, cambian los vectores de entrada y las compatibilidades pueden ser diferentes. Los values también se calculan a partir de las entradas que ya incluyen posición.

#### 17. Learned and Functional Encodings

> Hay dos enfoques principales para construir los vectores posicionales.

| Approach | Construcción | Ventajas | Limitaciones |
| --- | --- | --- | --- |
| **Learned positional embeddings** | Una matriz $P\in\mathbb{R}^{n_{\max}\times d_{\mathrm{model}}}$ almacena una fila aprendida por posición. | Puede aprender patrones útiles para la tarea; es un enfoque sencillo y eficaz. | El lookup está limitado a las posiciones disponibles en la tabla. Los vectores no tienen necesariamente una interpretación directa. |
| **Functional positional encodings** | Una función determinista $f:\mathbb{N}\to\mathbb{R}^{d_{\mathrm{model}}}$ calcula $p_i=f(i)$. | Permite definir vectores para posiciones adicionales sin aprender nuevas filas; puede incorporar relaciones entre posiciones. | Poder calcular posiciones más largas no garantiza un buen rendimiento fuera de las longitudes de entrenamiento. |

> En el enfoque aprendido, $n_{\max}$ fija el tamaño de la tabla. Extenderla exige añadir o adaptar embeddings; además, las posiciones sin entrenamiento suficiente pueden generalizar mal incluso si caben en la tabla.
>
> En el enfoque funcional, la fórmula no requiere un máximo matemático predefinido. La implementación y la capacidad del modelo pueden seguir imponiendo límites de contexto.

#### 18. Sinusoidal Positional Encodings

##### 18.1. Encoding Function

> El Transformer original utiliza senos y cosenos de distintas frecuencias. $\operatorname{PE}(pos,i)$ es la componente $i$ del vector posicional del token situado en $pos$:
>
> $$
> \operatorname{PE}(pos,i)=
> \begin{cases}
> \displaystyle\sin\!\left(
> \frac{pos}{10000^{i/d_{\mathrm{model}}}}
> \right),& i\text{ par},\\[6pt]
> \displaystyle\cos\!\left(
> \frac{pos}{10000^{(i-1)/d_{\mathrm{model}}}}
> \right),& i\text{ impar}.
> \end{cases}
> $$
>
> Los índices empiezan en $0$ en esta fórmula. Las componentes $0$ y $1$ forman una pareja seno-coseno con la misma frecuencia; las componentes $2$ y $3$ forman otra, y así sucesivamente.
>
> En «The dog chased the cat», «dog» está en $pos=1$. Para $d_{\mathrm{model}}=4$:
>
> $$
> \begin{aligned}
> \operatorname{PE}(1,0)&=\sin(1),\\
> \operatorname{PE}(1,1)&=\cos(1),\\
> \operatorname{PE}(1,2)&=\sin(1/100)=\sin(0.01),\\
> \operatorname{PE}(1,3)&=\cos(1/100)=\cos(0.01).
> \end{aligned}
> $$
>
> Por tanto:
>
> $$
> p_1=[\sin(1),\cos(1),\sin(0.01),\cos(0.01)]
> \approx[0.8415,0.5403,0.0100,1.0000].
> $$
>
> Las aproximaciones solo facilitan la lectura; los valores del encoding se calculan mediante la fórmula.

##### 18.2. Frequencies and Position Patterns

> Cada componente es una función periódica de la posición. Al avanzar hacia parejas con índices mayores, el denominador aumenta y la oscilación se vuelve más lenta. La combinación de ondas rápidas y lentas proporciona un patrón posicional distintivo dentro de las longitudes de uso.
>
> En la visualización, cada curva corresponde a una componente del encoding. Los puntos de un mismo color recogen sus valores para una posición concreta; al reunirlos se forma un vector $p_{pos}$. Las columnas de la tabla son posiciones y las filas son componentes.

![[apuntes-2b48110fe70d-p0166-f26b2a8795f6.png]]

> La pareja inicial utiliza $\sin(pos)$ y $\cos(pos)$; las siguientes parejas recorren ciclos más largos. Una sola onda repetiría valores, mientras que el conjunto de frecuencias permite distinguir posiciones.
>
> La analogía con la codificación binaria ayuda a entenderlo: distintos bits cambian a distintas velocidades; aquí las funciones binarias se sustituyen por ondas suaves. No se interpreta cada componente como un bit, sino como parte de un patrón continuo.

##### 18.3. Relative Positions

> Los encodings sinusoidales también contienen información sobre separación relativa. Para una pareja de componentes con frecuencia $\omega$:
>
> $$
> \sin(\omega x)\sin(\omega y)
> +\cos(\omega x)\cos(\omega y)
> =
> \cos\!\left(\omega(x-y)\right).
> $$
>
> El producto escalar depende así de diferencias de posición. Con $d_{\mathrm{model}}$ par:
>
> $$
> \operatorname{PE}(x)\cdot\operatorname{PE}(y)
> =
> \sum_{r=0}^{d_{\mathrm{model}}/2-1}
> \cos\!\left(
> \frac{x-y}{10000^{2r/d_{\mathrm{model}}}}
> \right).
> $$
>
> Las posiciones próximas pueden compartir patrones similares, pero esta suma es oscilatoria. No proporciona una medida de distancia que disminuya estrictamente al separar los tokens.

> [!warning] Corrección
> En el material aparece que, cuanto más alejadas están dos posiciones, menor es siempre su similitud por producto escalar, pero la expresión correcta es una suma de cosenos de la diferencia de posición, como se muestra arriba. Esa suma puede oscilar y no es monótona con la distancia.
> Fuente de comprobación: [Dive into Deep Learning: sinusoidal and relative positional information](https://d2l.ai/chapter_attention-mechanisms-and-transformers/self-attention-and-positional-encoding.html#relative-positional-information)

### VII. The Complete Encoder

#### 19. From Tokens to Contextualized Representations

> Sea $X\in\mathbb{R}^{L\times d_{\mathrm{model}}}$ la matriz de embeddings de entrada y $P\in\mathbb{R}^{L\times d_{\mathrm{model}}}$ la matriz de positional encodings seleccionados o calculados para esas posiciones.
>
> Primero se forman las representaciones que incluyen posición:
>
> $$
> X_0=X+P.
> $$
>
> Después se aplican los $N$ bloques de la pila:
>
> $$
> X_n=\operatorname{EncoderBlock}(X_{n-1}),
> \qquad n=1,\ldots,N.
> $$
>
> Cada bloque vuelve a relacionar las posiciones mediante attention y transforma sus características mediante la FFN, con las correspondientes sumas residuales y normalizaciones.
>
> El resultado final es:
>
> $$
> O=X_N\in\mathbb{R}^{L\times d_{\mathrm{model}}}.
> $$
>
> Se conserva **un vector contextualizado por token de entrada**. La dimensión no crece al apilar bloques: aumenta la profundidad de las transformaciones. Las capas superiores reciben representaciones ya contextualizadas por las inferiores.
>
> Esta salida puede utilizarse como entrada de una cabeza de clasificación o como memoria del decoder en un modelo encoder-decoder.

### VIII. Final Summary

> El Transformer sustituye la recurrencia por attention para relacionar las posiciones disponibles mediante cálculo paralelo. Sus familias utilizan esas representaciones para comprender una entrada, generar texto o transformar una secuencia en otra.
>
> El recorrido del encoder es:
>
> **Tokenization → embedding lookup → positional encoding → encoder blocks → contextual embeddings.**
>
> Dentro de cada bloque:
>
> **Multi-head self-attention → residual addition + layer normalization → position-wise FFN → residual addition + layer normalization.**

| Component | Qué aporta | Relación esencial |
| --- | --- | --- |
| Input embeddings | Representación inicial del contenido. | Una fila de $E$ por token del vocabulario. |
| Positional encodings | Información de orden. | $X_0=X+P$. |
| Queries and keys | Compatibilidad entre posiciones. | Scores $QK^\top/\sqrt{d_k}$. |
| Softmax | Distribución de atención para cada query. | Normaliza por filas. |
| Values | Información que se combina. | $\operatorname{Attention}(Q,K,V)=\operatorname{softmax}(QK^\top/\sqrt{d_k})V$. |
| Multiple heads | Varias mezclas contextuales aprendidas. | Concatenación y proyección con $W^O$. |
| Residual connections | Conservar y actualizar la representación. | Entrada más salida de la subcapa. |
| Layer normalization | Control de escala por embedding. | Estadísticas sobre las características de cada fila. |
| FFN | Transformación no lineal por posición. | Expansión a $d_{\mathrm{ff}}$ y retorno a $d_{\mathrm{model}}$. |

> Para seguir un cálculo, conviene distinguir **scores**, **weights**, **mezcla de values**, **change vector** y **representación tras la residual connection**. Sus dimensiones y funciones explican el orden de todas las operaciones.
>
> La attention del encoder sin posición conserva la representación de cada token al reordenar el contexto y reordena la salida completa con la entrada. Los positional encodings permiten incorporar el orden; los sinusoidales codifican diferencias de posición sin garantizar que la similitud decrezca de forma monótona con la distancia.
