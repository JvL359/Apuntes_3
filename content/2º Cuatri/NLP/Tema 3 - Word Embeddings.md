### I. Word Embeddings: Visión General
#### 1. Representación de Palabras Como Vectores
> Cuando trabajamos con texto, necesitamos convertir palabras a **vectores numéricos** porque los modelos de ML toman **vectores** como entrada.  
> Un vector real asociado a una palabra se denomina **word embedding** (ejemplo: “dog” $\rightarrow$ un vector real).
#### 2. One-Hot Vectors y Sus Limitaciones
> La representación más simple es el **one-hot**: para la palabra i-ésima del vocabulario, el vector tiene un 1 en la dimensión i y 0 en el resto.  
> El material recalca que **no es una buena representación** porque:
> - Los vectores son **muy largos**: dimensión igual al número de palabras del vocabulario (ej. >500.000).
> - **No captura significado**: distancia/similaridad vectorial no corresponde a distancia/similaridad semántica.
> - Todas las palabras quedan **ortogonales**: “cat” está tan “cerca” de “dog” como de “table”.
#### 3. Word Embeddings “Mejores” (Densos)
> En embeddings densos, cada palabra se representa con un vector real de dimensión n, donde (n) suele ser **mucho menor** que el tamaño del vocabulario.  
> El material afirma que **cada dimensión** captura alguna **propiedad/atributo** de las palabras.
#### 4. Dos Ideas Centrales del Material
> El material resume dos ideas:
> - **Proyección a un espacio vectorial**: cada palabra se mapea a un vector en $\mathbb{R}^n$, donde cada dimensión codifica algún aspecto de su uso/significado.
> - **El significado se captura por posición**: palabras cercanas en el espacio deberían tener significados similares; la “cercanía” se mide con **distancia o similitud** (ej. distancia euclídea; también se menciona cosine/dot product).
#### 5. Definición Formal y Exploración de Espacios
> **Definición (Word Embeddings)**: dada un vocabulario $V$, el embedding de una palabra $w\in V$ es un vector $x_w\in \mathbb{R}^d$, donde $d\in\mathbb{N}$ es el tamaño del embedding.  
> El material indica que la posición en el espacio codifica información semántica: palabras con significado similar tienden a quedar **cerca/similares**.  
> Incluye enlaces para explorar embeddings: Tensorflow Embedding Projector y “Word Embedding Universe”.
#### 6. Analogías con Aritmética Vectorial
> El material comenta que relaciones entre palabras pueden reflejarse en la **geometría del espacio**, permitiendo analogías con aritmética vectorial (no siempre sale lo esperado, pero es un fenómeno interesante).  
> Incluye un enlace a una demo de analogías (“WordEmbeddingDemo”).
#### 7. Embeddings Como Representación Estándar
> Mensaje explícito del material: **prácticamente todo modelo moderno de NLP usa embeddings**, independientemente de la tarea (incluye LLMs).  
> Se presentan como la **representación de entrada por defecto**.

### II. Hipótesis Distribucional y Similaridad
#### 1. ¿De Dónde Salen los Embeddings?
> El material plantea la pregunta: queremos aprender embeddings de forma que palabras con significados similares tengan vectores similares, pero ¿cómo “sabe” el modelo que dos palabras son similares?  
> Se propone un “juego” (diapositivas con imágenes) para motivar la idea.  
> **No aparece en el material aportado (en texto extraíble) el detalle exacto del juego**, porque está en imágenes sin transcripción.
#### 2. Hipótesis Distribucional
> Cita atribuida a J.R. Firth: “You shall know a word by the company it keeps”.  
> **Definición (Distributional Hypothesis)**: palabras que se usan y ocurren en **contextos similares** tienden a tener **significados similares**.
#### 3. Ejemplo: “Bourbon” y “Tezgüino”
> El material ilustra que “bourbon” (whiskey de maíz) es semánticamente similar a “tezgüino”: ambas encajan en contextos parecidos (bottle…, likes…, has alcohol…, made with corn…).  
> También indica que “volleyball” no encaja en esos contextos y por tanto no sería similar a “tezgüino”.
#### 4. Contexto Como Ventana de Palabras
> Para operacionalizar la idea, el material define el **contexto** de una palabra como las palabras que aparecen dentro de una **ventana de tamaño fijo**.  
> Ejemplo mostrado: tamaño de ventana = 2 (dos palabras a izquierda y dos a derecha).
#### 5. Similaridad Medida con Producto Escalar
> El material propone cuantificar similitud con **dot product**: $$\text{similarity}(x_1,x_2)=x_1\cdot x_2.$$Incluye un ejemplo numérico donde el dot product entre “bourbon” y “tezgüino” es positivo y grande, y entre “bourbon” y “cat” es negativo.
#### 6. De Contextos a Vectores Similares (Recap del Material)
> Idea operativa del material (resumen por pasos):
> 1. El contexto de una palabra son las palabras cercanas en una ventana fija.
> 2. En un gran conjunto de textos, cada palabra aparece en muchos contextos.
> 3. Por la hipótesis distribucional, los contextos observados informan del significado.
> 4. Se construye una representación vectorial usando esos contextos.
> 5. Se anima (encourage) a que el vector de cada palabra sea similar a los de sus palabras de contexto (en el material: “similar” (\approx) dot product grande).
> 6. Si dos palabras (w_1,w_2) aparecen en muchos contextos similares, ambas se ven empujadas a ser similares a los mismos vecinos.
> 7. Resultado: (w_1) y (w_2) quedan **indirectamente** empujadas a ser similares entre sí (sin compararlas directamente).

### III. Aprendizaje de Embeddings con word2vec: Skip-Gram con Negative Sampling (SGNS)
#### 1. word2vec y Enfoque del Tema
> El material presenta **word2vec** como un conjunto de técnicas para obtener representaciones vectoriales de palabras.  
> En este tema se centra en **Skip-gram with Negative Sampling (SGNS)**.
#### 2. Centro y Contexto
> Con una ventana de contexto de tamaño 2, para la frase “The quick brown fox jumps over the lazy dog”:
> - **Center word**: la palabra foco (ej. “jumps”).
> - **Context word**: palabras dentro de la ventana alrededor (ej. “brown”, “fox”, “over”, “the”).
#### 3. Tarea Binaria de Predicción (Skip-Gram)

> Skip-gram aprende embeddings resolviendo una tarea binaria: dada una pareja $(\text{cen},\text{ctxt})$, predecir la probabilidad de que $\text{ctxt}$ sea un contexto real de $\text{cen}$ : $$P(\text{true}\mid \text{cen},\text{ctxt}).$$Al ser binaria: $$P(\text{false}\mid \text{cen},\text{ctxt})=1-P(\text{true}\mid \text{cen},\text{ctxt}).$$En un modelo bien entrenado, estas probabilidades reflejan patrones reales de co-ocurrencia (alta para vecinos frecuentes, baja para raros).
#### 4. Dos Embeddings Por Palabra: Centro y Contexto
> El material asigna a cada palabra $w$ dos vectores entrenables:
> - embedding de centro: $e^{\text{cen}}_w$ (cuando $w$ actúa como centro)
> - embedding de contexto: $e^{\text{ctxt}}_w$ (cuando $w$ actúa como contexto)
#### 5. Cálculo de Probabilidades en Skip-Gram
> Para un par $(w,c)$:
> - Dot product: $z=e^{\text{cen}}_w\cdot e^{\text{ctxt}}_c$  
> - Sigmoid: $P(\text{true}\mid w,c)=\sigma(z),\qquad P(\text{false}\mid w,c)=1-\sigma(z)$  
#### 6. Datos de Entrenamiento: Sliding Window
> Los ejemplos etiquetados se extraen automáticamente: recorrer el texto con una **ventana deslizante** de tamaño fijo $\ell$, moviendo una palabra cada vez; en cada paso hay un centro y sus contextos.  
> Cada par centro-contexto extraído se etiqueta con 1 (co-ocurrencia real en ventana).
#### 7. Skip-Gram Como Clasificador con Matrices de Embeddings
> **Definición (Skip-gram classifier)**: dados pares $((w,c),1)$ en un dataset $D$, el modelo usa dos matrices de embeddings: $$E^{\text{cen}}\in\mathbb{R}^{|V|\times d},\quad E^{\text{ctxt}}\in\mathbb{R}^{|V|\times d}.$$Si el vocabulario está indexado (ej. $V={1:\text{“a”},2:\text{“an”},3:\text{“the”},\dots}$), entonces la fila i de $E^{\text{cen}}$ es $e^{\text{cen}}_w$ y la fila i de $E^{\text{ctxt}}$ es $e^{\text{ctxt}}_w$ para la palabra $w$ con índice i.  
> Predicción del clasificador: $P(\text{label}=1\mid w,c)=\sigma!\left(e^{\text{ctxt}}_c\cdot e^{\text{cen}}_w\right)$  
#### 8. Objetivo Con Solo Ejemplos Positivos (Problema Skip-Gram)
> **Definición (Skip-gram problem):** dado $D$ con pares $((w,c),1)$, encontrar $E^{\text{cen}},E^{\text{ctxt}}$ maximizando la likelihood: $$\arg\max_{(E^{\text{cen}},E^{\text{ctxt}})}\prod_{((w,c),1)\in D}P(\text{label}=1\mid w,c)=\arg\max\prod_{((w,c),1)\in D}\sigma(e^{\text{ctxt}}_c\cdot e^{\text{cen}}_w).$$El material reescribe esto como suma de logs y minimización de la negativa (lo identifica como cross-entropy cuando todas las labels son 1): $$\arg\min_{(E^{\text{cen}},E^{\text{ctxt}})}-\sum_{((w,c),1)\in D}\log\sigma(e^{\text{ctxt}}_c\cdot e^{\text{cen}}_w)$$ 
#### 9. Problema: “Solo Positivos” Permite una Solución Trivial
> El material señala un “loophole”: si todos los ejemplos tienen label 1, el modelo puede ajustar “perfecto” prediciendo siempre probabilidad cercana a 1.  
> Ejemplo de solución trivial: asignar el mismo vector grande a todas las palabras (ej. $(10,10,10,\dots)$) hace que los dot products sean grandes y $\sigma(\cdot)\approx 1$ en todos los pares positivos.  
> Consecuencia: embeddings inútiles (todas las palabras colapsan al mismo punto).
#### 10. Negative Examples y Negative Sampling
> Para evitar la solución trivial, se introducen **negative examples**: pares de palabras que **no** ocurrieron como vecinas en el corpus, para los cuales el modelo debería dar probabilidad cercana a 0.  
> En práctica, se crean muestreando palabras aleatorias del vocabulario y emparejándolas con una palabra centro.  
> **Negative sampling** en el material: por cada ejemplo positivo, se añaden $k$ negativos (en la diapositiva ilustrativa, $k=3)$.  
> Se define un conjunto $D^{-}$ con ejemplos negativos $((w,n),0)$.
#### 11. Definición Formal del Problema SGNS
> **Definición (SGNS Problem)**: dado un dataset $D$ de positivos $((w,c),1)$ y un dataset $D^{-}$ de negativos $((w,n),0)$, encontrar:
> - $E^{\text{cen}}\in\mathbb{R}^{|V|\times d}$ (center embeddings)
> - $E^{\text{ctxt}}\in\mathbb{R}^{|V|\times d}$ (context embeddings)  
> Maximizando la likelihood conjunta:  
>     $\arg\max_{(E^{\text{cen}},E^{\text{ctxt}})}\prod_{((w,c),1)\in D}P(\text{label}=1\mid w,c)\ \prod_{((w,n),0)\in D^-}P(\text{label}=0\mid w,n)$  
#### 12. Función de Pérdida SGNS (Tal Como La Deriva el Material)
> El material desarrolla la likelihood en términos de $\sigma(\cdot)$ y pasa a minimización con logs:  $$\arg\max\left[\prod_{(w,c)\in D}\sigma(e^{\text{ctxt}}_c\cdot e^{\text{cen}}_w)\ \prod_{(w,n)\in D^-}\left(1-\sigma(e^{\text{ctxt}}_n\cdot e^{\text{cen}}_w)\right)\right]$$$$\arg\min\left[-\sum_{(w,c)\in D}\log\sigma(e^{\text{ctxt}}_c\cdot e^{\text{cen}}_w)\ -\sum_{(w,n)\in D^-}\log\left(1-\sigma(e^{\text{ctxt}}_n\cdot e^{\text{cen}}_w)\right)\right]$$Usando el hecho $1-\sigma(x)=\sigma(-x)$, el material deja la forma final:  
> $$\arg\min\left[-\sum_{(w,c)\in D}\log\sigma(e^{\text{ctxt}}_c\cdot e^{\text{cen}}_w)\ -\sum_{(w,n)\in D^-}\log\sigma(-e^{\text{ctxt}}_n\cdot e^{\text{cen}}_w)\right]$$
#### 13. Interpretación de la Loss (Reward vs Penalize)

> Para un centro $w$, una positiva $(w,c)$ y varios negativos $(w,n)$, el material escribe la pérdida como: $$-\log\sigma(e^{\text{ctxt}}_c\cdot e^{\text{cen}}_w)\ -\sum_{((w,n),0)}\log\sigma(-e^{\text{ctxt}}_n\cdot e^{\text{cen}}_w)$$Interpretación directa del material:
> - **Reward**: alta similitud (dot product grande) entre $w$ y su contexto real $c$.
> - **Penalize**: alta similitud entre $w$ y palabras negativas $n$.  
> El material discute el efecto: si $e^{\text{ctxt}}_c\cdot e^{\text{cen}}_w$ es muy grande, entonces $\sigma(\cdot)\approx 1$ y el término de pérdida se hace pequeño; si es muy pequeño, la pérdida crece.  
> Para negativos, si $e^{\text{ctxt}}_n\cdot e^{\text{cen}}_w$ es grande, entonces $-\big(e^{\text{ctxt}}_n\cdot e^{\text{cen}}_w\big)$ es muy pequeño, $\sigma(\cdot)\approx 0$ y el término de pérdida es grande (penalización fuerte).

### IV. Después del Entrenamiento y Limitaciones
#### 1. Qué Se Conserva Tras Entrenar
> Durante el entrenamiento skip-gram, el modelo aprende **dos embeddings por palabra**: uno de centro y otro de contexto.  
> Al finalizar:
> - se conservan solo los **center-word embeddings**
> - los **context-word embeddings** se descartan  
>     Uso que lista el material para los center embeddings: inputs a modelos de lenguaje, features para clasificación y representaciones semánticas generales.
#### 2. Skip-Gram Como Tarea Instrumental
> El material subraya que skip-gram es un medio para aprender representaciones útiles, **no** un fin en sí mismo: no interesa realmente predecir si dos palabras van juntas en una ventana; esa predicción binaria es solo una tarea de entrenamiento.  
> El objetivo final son **los embeddings**, no el clasificador.
#### 3. Limitación: Un Solo Embedding Estático Por Palabra
> Pregunta del material: en skip-gram cada palabra tiene un embedding único y fijo; ¿Qué limitaciones tiene?  
> Ejemplo: “table” en “Convert this data into a table in Excel.” vs “Put this bottle on the table.” tiene significados distintos, pero skip-gram asigna un único vector a “table”.
#### 4. Embeddings Contextualizados
> El material afirma que los embeddings state-of-the-art son **contextualizados**, no estáticos: la misma palabra recibe embeddings distintos según el contexto.  
> Indica que se verá cómo obtener embeddings contextuales más adelante (en NLP 2).

### V. Resumen del Tema
> - Los embeddings representan palabras como vectores reales (densos), en un espacio donde la **posición** codifica información semántica.
> - La hipótesis distribucional conecta **contextos compartidos** con **significado compartido**.
> - SGNS aprende embeddings resolviendo una tarea binaria y usando **negativos** para evitar soluciones triviales.
> - Tras entrenar, se conservan los **center embeddings** como representación final; una limitación de skip-gram es que los embeddings son **estáticos** (polisemia).