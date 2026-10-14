---
estado: pendiente de revisión
---

### I. Encoder-decoder Architecture

#### 1. The Full Transformer

> Un **encoder-decoder Transformer** transforma una secuencia de entrada $x_1,\ldots,x_n$ en una secuencia de salida $y_1,\ldots,y_m$. Ambas pueden tener distinta longitud. El encoder construye representaciones de la entrada completa; el decoder genera la salida **un token cada vez**, condicionado por esas representaciones y por el prefijo de salida disponible.
>
> En traducción, la entrada puede ser `He picked the rose.` y la salida `Él recogió la rosa.`. El encoder procesa la frase inglesa y el decoder produce progresivamente la española.
>
> Las tres operaciones de atención tienen funciones distintas:
>
> - **Encoder self-attention:** $Q$, $K$ y $V$ proceden de la misma secuencia del encoder. Cada posición reúne información de toda la entrada válida.
> - **Decoder masked self-attention:** $Q$, $K$ y $V$ proceden del decoder. La máscara causal permite atender al prefijo y bloquea los tokens futuros de la salida.
> - **Cross-attention:** las queries proceden del decoder y las keys y values del encoder. Conecta lo que el decoder está intentando producir con la información de la entrada.
>
> Cada bloque incorpora además una **feed-forward network** (FFN), conexiones residuales y Layer Normalization. La figura simplifica la normalización para destacar el origen de $Q$, $K$ y $V$ y las conexiones entre ambas pilas.

![[apuntes-7c8df3a83719-p0008-f2516e33450a.png]]

> La salida del encoder alimenta la cross-attention de los bloques del decoder. Así, la generación no depende exclusivamente del texto ya generado: también puede consultar la frase que se está traduciendo.

#### 2. Autoregressive Translation Step by Step

##### 2.1. Encoding the Source

> **1. Tokenización y embeddings.** El tokenizer $T$ convierte el texto en tokens de un vocabulario $\mathcal V$. A cada token se le asigna un embedding y se suma su información posicional. Si se necesita una longitud fija de procesamiento, se añaden tokens de padding; estos deben excluirse de la atención cuando corresponda mediante una máscara de padding.
>
> La suma conserva la dimensión $d_{\mathrm{model}}$. Por ejemplo, dos posiciones ilustrativas son:
>
> $$
> \begin{aligned}
> \text{he:}\quad
> [-0.64,0,\ldots,-0.28]+[0,1,\ldots,1]
> &=[-0.64,1,\ldots,0.72],\\
> \text{picked:}\quad
> [-0.02,-0.27,\ldots,0.17]+[0.84,0.54,\ldots,1]
> &=[0.82,0.27,\ldots,1.17].
> \end{aligned}
> $$
>
> **2. Self-attention del encoder.** Las representaciones se contextualizan atendiendo a la entrada. El vector de `picked` puede incorporar información de `he`, `rose` y las demás posiciones válidas.
>
> **3. Residuales, normalización y FFN.** El resultado se combina con las entradas de las subcapas y se transforma mediante la FFN. Este procedimiento se repite en los bloques del encoder.
>
> **4. Representaciones finales.** Obtenemos:
>
> $$
> (h_1^{\mathrm{enc}},\ldots,h_n^{\mathrm{enc}})
> =\operatorname{TransformerEncoder}(x_1,\ldots,x_n),
> \qquad h_i^{\mathrm{enc}}\in\mathbb R^{d_{\mathrm{model}}}.
> $$
>
> Cada $h_i^{\mathrm{enc}}$ contiene información del token, su posición y su contexto. La salida mantiene una representación por posición; no se comprime obligatoriamente toda la frase en un único vector.

##### 2.2. Generating the First Token

> **5. Inicio del decoder.** Introducimos el token `[BOS]` (*beginning of sequence*), con su embedding y posición. En este momento no hay palabras traducidas anteriores.
>
> **6. Masked self-attention.** El decoder procesa el prefijo disponible. En general, para un prefijo $y_1,\ldots,y_t$:
>
> $$
> (h_1^{\mathrm{dec}},\ldots,h_t^{\mathrm{dec}})
> =\operatorname{Masked\text{-}Attention}(y_1,\ldots,y_t),
> \qquad h_i^{\mathrm{dec}}\in\mathbb R^{d_{\mathrm{model}}}.
> $$
>
> La representación de cada posición solo utiliza las posiciones permitidas por la máscara causal.
>
> **7. Cross-attention.** El estado del decoder proporciona la query para consultar las representaciones del encoder. El contexto recuperado depende de la compatibilidad entre esa query y las keys de los tokens fuente.
>
> **8. FFN y bloques restantes.** La representación se transforma y recorre los bloques del decoder. Al final se obtiene un estado contextualizado tanto por la salida previa como por la entrada.
>
> **9. LM head y softmax.** Una proyección lineal produce $|\mathcal V|$ logits. Softmax los convierte en probabilidades de los posibles próximos tokens:
>
> $$
> P_{\mathrm{enc-dec}}(y_{t+1}\mid x_1,\ldots,x_n,y_1,\ldots,y_t).
> $$
>
> **10. Decoding.** Se elige el próximo token con la estrategia de decoding utilizada. En el ejemplo se obtiene `él` y se añade al prefijo.

| Etapa del primer paso | Vector ilustrativo |
| --- | --- |
| Embedding de `[BOS]`, antes de añadir posición | $[-0.72,0.87,\ldots,0.11]$ |
| Salida de masked self-attention | $[-0.67,0.30,\ldots,0.14]$ |
| Salida de cross-attention | $[0.09,-0.92,\ldots,0.69]$ |
| Representación tras la FFN | $[0.48,0.21,\ldots,-0.91]$ |
| Logits de la LM head | $[-0.45,-0.75,\ldots,0.15]\in\mathbb R^{|\mathcal V|}$ |
| Algunas probabilidades tras softmax | $[0.92\%,0.71\%,\ldots,1.51\%]$ |

> Los puntos suspensivos representan componentes omitidas. Las probabilidades mostradas son una parte del vocabulario, por lo que no constituyen por sí solas una distribución completa.

##### 2.3. Repeating the Process

> **11. Actualización del prefijo.** La siguiente entrada del decoder contiene `[BOS] él`. Repetimos masked self-attention, cross-attention, FFN, LM head y decoding para obtener el token siguiente.
>
> **12. Parada.** Continuamos hasta generar `[EOS]` (*end of sequence*) o alcanzar el máximo $n_{\max}$. La traducción se construye como `él recogió la rosa ...`.
>
> Las representaciones del encoder se calculan sobre una entrada fija y pueden **reutilizarse** durante toda la generación. El prefijo del decoder sí crece en cada paso.
>
> Durante entrenamiento, **teacher forcing** proporciona como prefijo los tokens correctos de la salida, desplazados respecto de los targets. Durante inferencia, el prefijo contiene los tokens que el propio modelo ha generado.

#### 3. Cross-attention

##### 3.1. Queries, Keys and Values

> La diferencia con self-attention está en el **origen de las representaciones**, no en la operación básica de atención. Para el prefijo del decoder y la secuencia fuente:
>
> $$
> \begin{aligned}
> q_i&=h_i^{\mathrm{dec}}W_{\mathrm{enc-dec}}^Q
> \in\mathbb R^{d_q}, &&i=1,\ldots,t,\\
> k_j&=h_j^{\mathrm{enc}}W_{\mathrm{enc-dec}}^K
> \in\mathbb R^{d_k}, &&j=1,\ldots,n,\\
> v_j&=h_j^{\mathrm{enc}}W_{\mathrm{enc-dec}}^V
> \in\mathbb R^{d_v}, &&j=1,\ldots,n.
> \end{aligned}
> $$
>
> La query expresa qué información necesita una posición del decoder. Las keys permiten comparar esa necesidad con las posiciones fuente; los values contienen la información que se combina.
>
> Aunque la salida es causal, la cross-attention puede consultar **toda la entrada fuente válida**: esta ya está disponible antes de comenzar a generar.

##### 3.2. Matrix Form and Dimensions

> Para la formulación matricial usamos la convención local **$n$ posiciones del decoder y $m$ posiciones del encoder**. Esta convención intercambia el uso de $n$ y $m$ respecto del ejemplo inicial; las longitudes se definen aquí por el lado al que pertenecen.
>
> Sean:
>
> $$
> H_{\mathrm{dec}}\in\mathbb R^{n\times d_{\mathrm{model}}},
> \qquad
> H_{\mathrm{enc}}\in\mathbb R^{m\times d_{\mathrm{model}}}.
> $$
>
> $H_{\mathrm{dec}}$ representa los estados posteriores a la masked self-attention y su residual y normalización. Las proyecciones son:
>
> $$
> Q=H_{\mathrm{dec}}W^Q,\qquad
> K=H_{\mathrm{enc}}W^K,\qquad
> V=H_{\mathrm{enc}}W^V.
> $$
>
> Para una cabeza de atención:
>
> $$
> S=\frac{QK^\top}{\sqrt{d_k}},
> \qquad A=\operatorname{softmax}_{\mathrm{row}}(S),
> \qquad Z=AV.
> $$

| Matriz | Dimensión | Significado |
| --- | --- | --- |
| $Q$ | $n\times d_q$ | Una query por posición del decoder |
| $K$ | $m\times d_k$ | Una key por posición del encoder |
| $V$ | $m\times d_v$ | Un value por posición del encoder |
| $QK^\top$ y $S$ | $n\times m$ | Compatibilidades entre posiciones de salida y entrada |
| $A$ | $n\times m$ | Pesos normalizados sobre posiciones fuente |
| $Z$ | $n\times d_v$ | Contexto recuperado por posición del decoder |

> Debe cumplirse $d_q=d_k$ para calcular el producto. La multiplicación dimensional es:
>
> $$
> (n\times d_k)(d_k\times m)=n\times m,
> \qquad
> (n\times m)(m\times d_v)=n\times d_v.
> $$
>
> Softmax se aplica **por fila**, sobre las keys válidas del encoder. Cada fila de $A$ suma uno y la salida de una posición es una media ponderada de los values:
>
> $$
> z_i=\sum_{j=1}^{m}A_{ij}v_j.
> $$
>
> En multi-head attention se repite este mecanismo con distintas proyecciones y se combinan las cabezas con una proyección de salida. El resultado vuelve a tener dimensión $d_{\mathrm{model}}$, necesaria para la suma residual.

##### 3.3. Reading an Attention Matrix

> Consideremos la traducción:
>
> - Entrada: `A tecnologia tem transformado profundamente a forma como vivemos e trabalhamos.`
> - Predicción: `technology has changed deeply the way we live and work .`
> - Traducción de referencia: `Technology has profoundly transformed the way we live and work.`
>
> En el mapa, las **filas** corresponden a tokens de la salida y las **columnas** a tokens de la entrada. Los colores claros indican pesos mayores; los oscuros, menores.

![[apuntes-7c8df3a83719-p0027-591f1c883d18.png]]

> Se observan asociaciones como `technology` con `tecnologia`, `way` con `forma` y `work` con `trabalhamos`. Una palabra fuente puede dividirse en subwords, como `transforma` y `##do`: la alineación no tiene por qué ser entre palabras completas.
>
> El mapa muestra una cabeza de cross-attention concreta. Ayuda a visualizar qué posiciones reciben peso, sin implicar que todas las cabezas aprendan la misma alineación.

#### 4. Decoder Block and Full Decoder

> Sean $X_{\mathrm{dec}}\in\mathbb R^{n\times d_{\mathrm{model}}}$ y $H_{\mathrm{enc}}\in\mathbb R^{m\times d_{\mathrm{model}}}$. Con la disposición **post-LN** de este bloque:
>
> $$
> \begin{aligned}
> Z_1&=\operatorname{LN}\left(
> X_{\mathrm{dec}}+
> \operatorname{MaskedMultiHead}(X_{\mathrm{dec}})
> \right),\\
> Z_2&=\operatorname{LN}\left(
> Z_1+\operatorname{CrossMultiHead}(Z_1,H_{\mathrm{enc}})
> \right),\\
> Y&=\operatorname{LN}\left(Z_2+\operatorname{FFN}(Z_2)\right).
> \end{aligned}
> $$
>
> Primero se integra el prefijo de salida; después se consulta la entrada; finalmente la FFN transforma la representación de cada posición. En la cross-attention, **$Z_1$ proporciona las queries** y **$H_{\mathrm{enc}}$ las keys y values**.
>
> Para el decoder completo, usamos ahora $L$ como longitud de la secuencia y $N$ como número de bloques. Si $X\in\mathbb R^{L\times d_{\mathrm{model}}}$ contiene los embeddings y $P$ las posiciones:
>
> $$
> \begin{aligned}
> X_0&=X+P,\\
> X_n&=\operatorname{DecoderBlock}(X_{n-1},H_{\mathrm{enc}}),
> &&n=1,\ldots,N,\\
> Y&=\operatorname{Softmax}(X_NW_{\mathrm{LM}})
> \in\mathbb R^{L\times|\mathcal V|}.
> \end{aligned}
> $$
>
> La softmax de la LM head se aplica sobre el **vocabulario** en cada fila. No es la softmax de atención, que se normaliza sobre posiciones de la entrada. Cada fila final expresa una distribución del próximo token condicionada por el prefijo permitido y el encoder.

### II. Model Pre-training

#### 5. From a Base Model to an Assistant

> El entrenamiento de grandes Transformers puede organizarse en tres etapas con objetivos diferentes:

| Etapa | Datos y objetivo | Resultado |
| --- | --- | --- |
| **Pre-training** | Grandes corpus; señal de entrenamiento derivada del propio texto | Base model |
| **Supervised fine-tuning (SFT)** | Ejemplos de instrucciones y respuestas deseadas | Instruction-tuned model |
| **Alignment / preference tuning** | Preferencias sobre respuestas, mediante métodos como RLHF o DPO | Preference-tuned model |

![[apuntes-7c8df3a83719-p0033-62906d958c57.png]]

> **Pre-training** aprende patrones lingüísticos, conocimientos y representaciones reutilizables. Para un decoder-only, el objetivo habitual es predecir el siguiente token. BERT y T5 emplean otros objetivos, que relacionan la arquitectura con la señal de aprendizaje.
>
> El resultado es un **base model** o **foundation model**: una base adaptable a muchas tareas. A diferencia del enfoque tradicional de entrenar desde cero un modelo especializado para cada problema, parte del aprendizaje se comparte entre aplicaciones.
>
> Un base model puede completar texto sin comportarse como un asistente. Ante `How do I reset my password?`, podría continuar una lista de preguntas, por ejemplo con otra sobre cambiar la dirección de correo, porque está reproduciendo un patrón textual.
>
> **SFT** enseña el comportamiento instrucción-respuesta. Para la misma consulta, la respuesta deseada pasa a ser una explicación de los pasos para restablecer la contraseña.
>
> **Alignment** orienta las respuestas hacia preferencias de utilidad, veracidad y comportamiento adecuado. El pretraining, por sí solo, puede reproducir información falsa o instrucciones perjudiciales presentes en los datos. Por ejemplo, ante una petición de acceso no autorizado, la conducta deseada es rechazarla y orientar hacia mecanismos legítimos de recuperación cuando proceda.
>
> Estas etapas no son intercambiables: aprender a modelar texto, responder instrucciones y satisfacer preferencias son objetivos relacionados, pero distintos.

#### 6. Pre-training Data

##### 6.1. Scale and Diversity

> Los corpus de pretraining combinan páginas web, libros, código, artículos científicos, foros y otras fuentes. Su diversidad permite aprender registros, dominios y estructuras diferentes: una función de código y una noticia ofrecen señales complementarias.
>
> La escala suele medirse en **tokens procesados**. En los ejemplos de grandes modelos de 2025, como DeepSeek-v3, Gemma 3 y Qwen 3, aparecen cantidades entre $14\times10^{12}$ y $36\times10^{12}$ tokens. En español, $10^{12}$ es un **billón**; el inglés *billion* significa $10^9$.
>
> La composición del corpus y el número de veces que se utiliza cada fuente también importan. Una mezcla de entrenamiento no tiene por qué reproducir las proporciones de los archivos descargados.

##### 6.2. A Data Mixture Example

> La mezcla de LLaMA ilustra cómo se distribuye el entrenamiento entre fuentes. Los epochs indicados corresponden al entrenamiento de $1.4\times10^{12}$ tokens; el entrenamiento de $10^{12}$ tokens utiliza las mismas proporciones.

| Fuente | Proporción de la mezcla | Epochs | Tamaño |
| --- | ---: | ---: | ---: |
| CommonCrawl | 67.0% | 1.10 | 3.3 TB |
| C4 | 15.0% | 1.06 | 783 GB |
| GitHub | 4.5% | 0.64 | 328 GB |
| Wikipedia | 4.5% | 2.45 | 83 GB |
| Books | 4.5% | 2.23 | 85 GB |
| ArXiv | 2.5% | 1.06 | 92 GB |
| StackExchange | 2.0% | 1.03 | 78 GB |

> Un valor superior a un epoch indica reutilización de esa fuente; uno inferior significa que no se recorre por completo. Wikipedia y Books se reutilizan más que GitHub en esta configuración.
>
> **FineWeb**, publicado por Hugging Face en 2024, es un ejemplo de corpus público: aproximadamente $15\times10^{12}$ tokens y 44 TB. Su disponibilidad permite investigar con datos accesibles, frente a conjuntos de entrenamiento de modelos de frontera que con frecuencia no se publican completos. Los resultados favorables frente a otros corpus abiertos dependen de la evaluación considerada.

##### 6.3. Cleaning and Filtering

> La preparación de datos requiere **seleccionar, filtrar, limpiar y deduplicar**:
>
> - Eliminar repeticiones, como varias copias de la misma frase sobre el océano Pacífico.
> - Filtrar texto de baja calidad, por ejemplo ofertas de tipo clickbait con poco contenido útil.
> - Limpiar HTML roto y caracteres de control.
> - Conservar contenido útil de distintas fuentes, como libros y código.
>
> Aumentar el tamaño sin controlar la calidad puede multiplicar ruido o duplicados. La selección del corpus determina qué información y patrones se ponen a disposición del objetivo de aprendizaje.

### III. GPT and Causal Language Modeling

#### 7. Causal Language Modeling Loss

> **Causal Language Modeling (CLM)** entrena un decoder-only para predecir el siguiente token utilizando el prefijo. No dispone de un encoder separado ni del contexto futuro del token a predecir.
>
> Preguntas como `The largest ocean is ...`, `Madrid is the capital of ...` o `Water boils at 100 degrees ...` ilustran la forma del problema: continuar una secuencia con tokens compatibles con su contexto.
>
> Sea $x=(x_1,\ldots,x_T)$. En esta sección, $L$ indica la **última capa**, no la longitud utilizada antes para formular el decoder completo. El estado $h_i^L$ se calcula con el prefijo $x_1,\ldots,x_i$. En teacher forcing, la secuencia de entrada al decoder coincide con los tokens correctos del prefijo; si la llamamos $y_1,\ldots,y_i$, aquí $y_j=x_j$.
>
> La LM head produce:
>
> $$
> u_i=h_i^LW,\qquad
> \hat p_i=\operatorname{softmax}(u_i),
> \qquad
> \hat p_i[x_{i+1}]
> =P(x_{i+1}\mid x_1,\ldots,x_i).
> $$
>
> Con estados representados como vectores fila, $W\in\mathbb R^{d_{\mathrm{model}}\times|\mathcal V|}$. $\hat p_i$ es la distribución sobre el vocabulario y $\hat p_i[x_{i+1}]$ selecciona la probabilidad del target correcto.
>
> Para un token:
>
> $$
> L_{\mathrm{CE}}(x_{i+1})
> =-\log\hat p_i[x_{i+1}].
> $$
>
> Para la secuencia, con esta convención de predecir desde la segunda posición:
>
> $$
> L_{\mathrm{CLM}}(x)
> =\frac{1}{T-1}\sum_{i=1}^{T-1}L_{\mathrm{CE}}(x_{i+1})
> =-\frac{1}{T-1}\sum_{i=1}^{T-1}
> \log\hat p_i[x_{i+1}].
> $$
>
> Minimizar la pérdida aumenta las probabilidades asignadas a los tokens reales de entrenamiento. La máscara causal impide que el modelo utilice el propio target futuro para predecirlo, aunque durante entrenamiento se procese la secuencia en paralelo.

#### 8. GPT: Pre-training and Supervised Fine-tuning

##### 8.1. Transfer to Downstream Tasks

> **GPT**, presentado en 2018 en *Improving Language Understanding by Generative Pre-Training*, utiliza dos fases:
>
> 1. Pretraining con lenguaje no etiquetado y objetivo causal.
> 2. Fine-tuning supervisado para una tarea concreta, reutilizando los parámetros aprendidos y adaptando la entrada y la salida a la tarea.
>
> El pretraining proporciona un punto de partida mejor que una inicialización aleatoria. Las etiquetas de una tarea pueden ser escasas; aprovechar representaciones aprendidas en grandes corpus reduce la necesidad de aprender toda la estructura lingüística con esos pocos ejemplos.
>
> Los resultados de comprensión de textos muestran que un modelo entrenado para generar también puede transferirse a tareas discriminativas.

| Modelo o método | Story Cloze | RACE-m | RACE-h | RACE |
| --- | ---: | ---: | ---: | ---: |
| val-LS-skip | 76.5 | — | — | — |
| Hidden Coherence Model | 77.6 | — | — | — |
| Dynamic Fusion Net, ensemble de 9 modelos | — | 55.6 | 49.4 | 51.2 |
| BiAttention MRU, ensemble de 9 modelos | — | 60.2 | 50.3 | 53.3 |
| Fine-tuned Transformer LM | **86.5** | **62.9** | **57.4** | **59.0** |

> Story Cloze evalúa la elección de una continuación coherente; RACE evalúa comprensión lectora. Los números corresponden a la comparación histórica de GPT, no a una clasificación actual de modelos.

##### 8.2. Why Pre-training Helps

![[apuntes-7c8df3a83719-p0054-ceac9166cb7c.png]]

> **Panel izquierdo:** al aumentar las actualizaciones de pretraining, mejora el rendimiento relativo zero-shot en varias tareas, aunque estas no hayan sido el objetivo supervisado del entrenamiento. Las curvas corresponden a sentiment analysis, Winograd schema resolution, linguistic acceptability y question answering.
>
> **Panel derecho:** el fine-tuning desde un modelo preentrenado, en líneas continuas, alcanza resultados mejores y más rápidamente que desde una inicialización aleatoria, en líneas discontinuas.
>
> El pretraining tiene, por tanto, dos efectos observables: puede producir capacidades utilizables directamente y facilita la adaptación posterior con supervisión. El rendimiento zero-shot inicial no tiene por qué ser igual en todas las tareas.

#### 9. GPT-3 and In-context Learning

##### 9.1. Zero-shot, One-shot and Few-shot

> **GPT-3**, presentado en 2020 en *Language Models are Few-shot Learners*, muestra que un modelo suficientemente grande puede realizar tareas mediante el contexto del prompt, sin efectuar fine-tuning para cada una.
>
> **In-context learning (ICL)** proporciona instrucciones y, opcionalmente, ejemplos dentro de la entrada. El modelo continúa el texto aprovechando el patrón que estos muestran.

| Configuración | Contenido del prompt | Actualización de parámetros |
| --- | --- | --- |
| **Zero-shot** | Instrucción y caso que se quiere procesar | No |
| **One-shot** | Instrucción, un ejemplo resuelto y nuevo caso | No |
| **Few-shot** | Instrucción, varios ejemplos resueltos y nuevo caso | No |
| **Supervised fine-tuning** | Ejemplos usados como datos de entrenamiento | Sí |

> En los tres prompts, `cheese =>` es la consulta que debe completar el modelo. Lo que cambia es la cantidad de demostraciones anteriores.

```text
Zero-shot
Translate English to French:
cheese =>

One-shot
Translate English to French:
sea otter => loutre de mer
cheese =>

Few-shot
Translate English to French:
sea otter => loutre de mer
peppermint => menthe poivrée
plush giraffe => girafe peluche
cheese =>
```

> En ICL los ejemplos actúan como **contexto para la inferencia**. En fine-tuning actúan como **supervisión para modificar los pesos** mediante entrenamiento. Añadir demostraciones al prompt no equivale a ejecutar gradient descent.

##### 9.2. Model Scale and Demonstrations

![[apuntes-7c8df3a83719-p0062-6a0715493c6b.png]]

> En TriviaQA, la accuracy aumenta al crecer el número de parámetros, desde modelos de $0.1$ hasta $175\times10^9$ parámetros. Para una misma escala, few-shot con $K=64$ ejemplos supera a one-shot y zero-shot en esta comparación.
>
> El modelo de $175\times10^9$ parámetros en few-shot alcanza aproximadamente un 71% y supera la referencia de fine-tuning mostrada, cercana al 68%. La figura ilustra un resultado experimental concreto: más escala y demostraciones pueden mejorar ICL, sin garantizar la misma ganancia en cualquier tarea o prompt.
>
> La evolución de GPT combina así **pretraining reutilizable**, adaptación supervisada cuando se necesita y aprovechamiento del contexto para resolver tareas sin actualizar los parámetros.

### IV. BERT and Bidirectional Pre-training

#### 10. Encoder-only Language Understanding

##### 10.1. Bidirectional Context

> **BERT** significa **Bidirectional Encoder Representations from Transformers**. Presentado en 2018, utiliza una arquitectura **encoder-only** para aprender representaciones contextualizadas de los tokens.
>
> El encoder puede atender a tokens anteriores y posteriores de la entrada. Esto ayuda a interpretar palabras ambiguas:
>
> - En `We went to the river bank`, `river` aporta contexto para interpretar `bank`.
> - En `I need to go to the bank to deposit money`, `deposit money` proporciona información a la derecha de `bank`.
>
> El contexto de ambos lados puede contribuir a la representación de la palabra. Un decoder causal solo dispone del prefijo para cada posición.
>
> La bidireccionalidad es una decisión útil para aprender representaciones, pero no implica que los modelos causales sean incapaces de comprender lenguaje. Los resultados de GPT muestran que un decoder-only también puede adquirir capacidades de comprensión.
>
> BERT se preentrena y después se adapta a tareas como clasificación, natural language inference y question answering, con modificaciones pequeñas en las entradas o cabezas de salida.

##### 10.2. GLUE and Transfer Results

> **GLUE** (*General Language Understanding Evaluation*) reúne tareas distintas para evaluar si las representaciones aprendidas se transfieren más allá de un único problema.

| Tarea | Qué evalúa | Métrica |
| --- | --- | --- |
| CoLA | Aceptabilidad gramatical | Matthews correlation |
| SST-2 | Sentimiento positivo o negativo | Accuracy |
| STS-B | Similitud semántica entre dos frases | Pearson/Spearman correlation |
| MRPC | Detección de paráfrasis | Accuracy/F1 |
| QQP | Equivalencia entre preguntas | Accuracy/F1 |
| MNLI | Entailment, contradiction o neutral entre premisa e hipótesis | Accuracy, matched/mismatched |
| QNLI | Relación entre una pregunta y una frase que puede contener su respuesta | Accuracy |
| RTE | Entailment entre textos | Accuracy |
| WNLI | Interpretación de referencias pronominales formulada como inferencia | Accuracy |

> [!warning] Corrección
> En el material aparece SST-2 con una etiqueta «neutral» y una puntuación continua, pero la expresión correcta es «SST-2: clasificación binaria de sentimiento positivo o negativo». La variante SST-2 de GLUE no incluye una tercera clase neutral.
> Fuente de comprobación: [GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding](https://arxiv.org/html/1804.07461v3#S3.SS1).

> Por ejemplo, CoLA pregunta si una secuencia como `This toast is than that one.` es gramaticalmente aceptable. STS-B compara el grado de similitud de dos frases; MRPC y QQP deciden si dos formulaciones expresan lo mismo. MNLI y RTE evalúan relaciones lógicas, mientras que WNLI requiere interpretar a quién se refiere un pronombre.
>
> La comparación histórica siguiente muestra mejoras de BERT frente a modelos anteriores. Las columnas siguen las métricas agregadas de la comparación; no todos los números representan accuracy. MNLI contiene los resultados matched/mismatched.

| Modelo | Average | CoLA | SST-2 | STS-B | MRPC | QQP | MNLI | QNLI | RTE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| BiLSTM + ELMo + Attention | 71.0 | 36.0 | 90.4 | 73.3 | 84.9 | 64.8 | 76.4 / 76.1 | 79.8 | 56.8 |
| Pre-OpenAI state of the art | 74.0 | 35.0 | 93.2 | 81.0 | 86.0 | 66.1 | 80.6 / 80.1 | 82.3 | 61.7 |
| OpenAI GPT | 75.1 | 45.4 | 91.3 | 80.0 | 82.3 | 70.3 | 82.1 / 81.4 | 87.4 | 56.0 |
| BERT-base | 79.6 | 52.1 | 93.5 | 85.8 | 88.9 | 71.2 | 84.6 / 83.4 | 90.5 | 66.4 |
| BERT-large | **82.1** | **60.5** | **94.9** | **86.5** | **89.3** | **72.1** | **86.7 / 85.9** | **92.7** | **70.1** |

> BERT-large mejora el promedio de 75.1 de GPT a 82.1 en esta tabla. La importancia de la comparación es la **transferencia a tareas variadas**, no que una única métrica describa toda la comprensión lingüística.

#### 11. Masked Language Modeling

##### 11.1. Denoising Objective

> **Masked Language Modeling (MLM)** entrena al encoder para recuperar tokens originales a partir de una entrada parcialmente corrompida. Se relaciona con un ejercicio **cloze**, en el que se completan huecos aprovechando el contexto a ambos lados.
>
> Esta corrupción permite usar atención bidireccional sin que la tarea se reduzca siempre a copiar el target visible. Por ejemplo, una sustitución puede convertir `The dog barked at me` en `The sandwich barked at me`; el target de la posición afectada continúa siendo el token original.
>
> En BERT se selecciona aleatoriamente el **15% de las posiciones** de tokens como targets. Dentro de ese conjunto seleccionado:
>
> - **80%:** el token se sustituye por `[MASK]`.
> - **10%:** se sustituye por un token aleatorio.
> - **10%:** permanece sin cambios.
>
> Los porcentajes 80/10/10 se aplican **al 15% seleccionado**, no a toda la secuencia. En proporción al total, corresponden aproximadamente al 12%, 1.5% y 1.5%, respectivamente.

| Si se selecciona `hairy` en `my dog is hairy` | Entrada resultante | Target de la posición |
| --- | --- | --- |
| Sustitución por `[MASK]`, 80% | `my dog is [MASK]` | `hairy` |
| Sustitución aleatoria, 10% | `my dog is apple` | `hairy` |
| Sin cambios, 10% | `my dog is hairy` | `hairy` |

> La mezcla evita depender exclusivamente de la presencia de `[MASK]`, que no suele aparecer en la entrada de las tareas de fine-tuning. Mantener algunos targets sin cambios también permite aprovechar información del token observado.
>
> Esta explicación se refiere a las **posiciones seleccionadas**: los demás tokens no son ruido y siguen proporcionando contexto útil. Aunque algunas posiciones mantengan el token original, la tarea global sigue requiriendo representaciones contextualizadas.

![[apuntes-7c8df3a83719-p0074-7055155af523.png]]

> En la figura se seleccionan las posiciones de `long`, `thanks` y `the`. Las dos primeras se sustituyen por máscaras; la tercera, por `apricot`. El encoder procesa toda la secuencia, pero las cabezas que contribuyen a la pérdida deben recuperar los **tokens originales** de las posiciones seleccionadas.

##### 11.2. MLM Loss

> Sea $x=(x_1,\ldots,x_n)$ la secuencia original y $M\subseteq\{1,\ldots,n\}$ el conjunto de posiciones seleccionadas para predicción. Llamamos $\tilde x$ a la versión corrompida que realmente recibe el encoder; esta distinción separa la entrada del target.
>
> Para $i\in M$, el estado final $h_i^L$ se calcula a partir de $\tilde x$ y produce:
>
> $$
> u_i=h_i^LW,\qquad
> \hat p_i=\operatorname{softmax}(u_i),
> \qquad
> L_{\mathrm{CE}}(x_i)=-\log\hat p_i[x_i].
> $$
>
> La pérdida media es:
>
> $$
> L_{\mathrm{MLM}}(x)
> =\frac{1}{|M|}\sum_{i\in M}L_{\mathrm{CE}}(x_i)
> =-\frac{1}{|M|}\sum_{i\in M}\log\hat p_i[x_i].
> $$
>
> El target $x_i$ es el token original **en la misma posición $i$**; en CLM el estado $h_i^L$ predecía el token siguiente $x_{i+1}$. Además, MLM puede utilizar contexto a ambos lados de la posición.
>
> $M$ incluye también el 10% seleccionado que quedó sin cambios. No se define únicamente como las posiciones que muestran físicamente `[MASK]`: las sustituciones aleatorias y los targets conservados también contribuyen a la pérdida.
>
> Todos los parámetros del modelo reciben gradientes a través de las posiciones supervisadas. Un token no seleccionado puede influir en los estados que sí generan pérdida mediante la atención, aunque no tenga un término propio de cross-entropy.

##### 11.3. Supervision Density

> CLM proporciona targets en prácticamente todas las posiciones de una secuencia, según la convención de desplazamiento usada. MLM supervisa directamente solo el subconjunto seleccionado, aproximadamente el 15%.
>
> Por tanto, para un presupuesto similar de tokens procesados, **MLM tiene una señal directa de predicción menos densa**. Esto puede exigir más procesamiento para acumular un número comparable de targets y es una desventaja de eficiencia al escalar.
>
> La comparación se refiere a la densidad de supervisión. La calidad final también depende de la arquitectura, los datos y el objetivo: no convierte automáticamente CLM en el mejor método para todas las tareas.

#### 12. Next Sentence Prediction

##### 12.1. Constructing Sentence Pairs

> **Next Sentence Prediction (NSP)** añade una tarea para aprender relaciones entre dos segmentos de texto, $A$ y $B$. Se predice una de dos clases:
>
> - **IsNext:** $B$ es la continuación real de $A$ en el corpus.
> - **NotNext:** $B$ se ha tomado aleatoriamente de otra parte del corpus.
>
> La construcción de los datos usa aproximadamente un **50% de pares positivos** y un **50% de pares negativos**. Las etiquetas se obtienen del propio corpus, sin anotación manual de cada relación.
>
> NSP es una tarea de continuidad textual. Puede ayudar a representar relaciones útiles para question answering o inference, pero su etiqueta no es una etiqueta de entailment o contradiction.
>
> Los dos segmentos se introducen conjuntamente:
>
> $$
> [\mathrm{CLS}],\ A,\ [\mathrm{SEP}],\ B,\ [\mathrm{SEP}].
> $$
>
> `[CLS]` se coloca al principio y su representación final se usa para clasificación. `[SEP]` separa los segmentos y marca el final de la secuencia. Las máscaras de MLM pueden aplicarse a los tokens de ambos segmentos.

##### 12.2. Segment Embeddings

> La entrada de BERT suma **tres embeddings** por posición:
>
> $$
> x_i=e_i+p_i+s_i\in\mathbb R^{d_{\mathrm{model}}}.
> $$
>
> $e_i$ representa el token, $p_i$ su posición y $s_i$ el segmento al que pertenece. Hay **dos segment embeddings aprendidos**, $E_A$ y $E_B$, compartidos por las posiciones de cada segmento.

![[apuntes-7c8df3a83719-p0087-cb11f9eceb09.png]]

> En el ejemplo, `[CLS] my dog is cute [SEP]` recibe $E_A$, y `he likes play ##ing [SEP]` recibe $E_B$. Las posiciones continúan a lo largo de la secuencia completa; no se reinician para el segundo segmento.
>
> La suma distingue tres preguntas: **qué token** aparece, **dónde** está y **a qué segmento** pertenece. Al sumarse, los tres componentes deben tener la misma dimensión.

##### 12.3. Classification Head and Joint Loss

> El vector final de `[CLS]` resume la entrada para la tarea de clasificación:
>
> $$
> h_{\mathrm{[CLS]}}^L\in\mathbb R^{1\times d_{\mathrm{model}}},
> \qquad
> W_{\mathrm{NSP}}\in\mathbb R^{d_{\mathrm{model}}\times2}.
> $$
>
> La cabeza se aplica a la **salida contextualizada del encoder**, no al embedding inicial de `[CLS]`:
>
> $$
> y_{\mathrm{[CLS]}}
> =\operatorname{softmax}(h_{\mathrm{[CLS]}}^LW_{\mathrm{NSP}})
> \in\mathbb R^2.
> $$
>
> Si $y_{\mathrm{true}}\in\{0,1\}$ es la etiqueta y $\hat y$ la probabilidad de **IsNext**, la binary cross-entropy es:
>
> $$
> L_{\mathrm{NSP}}(x)
> =-\left[
> y_{\mathrm{true}}\log\hat y+
> (1-y_{\mathrm{true}})\log(1-\hat y)
> \right].
> $$
>
> Cuando la etiqueta es 1, el término activo favorece una probabilidad alta de IsNext. Cuando es 0, favorece una probabilidad alta de NotNext. Esta forma binaria es equivalente a seleccionar la probabilidad de la clase correcta de la softmax de dos clases.
>
> El pretraining de BERT combina las dos tareas:
>
> $$
> L_{\mathrm{total}}=L_{\mathrm{MLM}}(x)+L_{\mathrm{NSP}}(x).
> $$
>
> La cabeza MLM trabaja con estados de posiciones seleccionadas; la cabeza NSP con el estado de `[CLS]`. Ambas pérdidas entrenan el **mismo encoder compartido**, además de sus respectivas cabezas.

##### 12.4. Practice: Identify the NSP Label

> Para cada entrada, decidir si la etiqueta debe ser **IsNext** o **NotNext**.

```text
Caso 1
[CLS] the man went to [MASK] store [SEP]
he bought a gallon [MASK] milk [SEP]
Label = ?

Caso 2
[CLS] the man [MASK] to the store [SEP]
penguin [MASK] are flight ##less birds [SEP]
Label = ?
```

#### 13. BERT Architecture and Fine-tuning

##### 13.1. Pre-training Architecture

> Si el primer segmento contiene $m$ tokens $w_1,\ldots,w_m$ y el segundo $n$ tokens $w_{m+1},\ldots,w_{m+n}$, la secuencia es:
>
> $$
> [\mathrm{CLS}],w_1,\ldots,w_m,[\mathrm{SEP}],
> w_{m+1},\ldots,w_{m+n},[\mathrm{SEP}].
> $$
>
> Hay $m+n+3$ posiciones, contando los tres tokens especiales. A los tokens seleccionados se les aplica el procedimiento de corrupción de MLM.
>
> Aquí $x_i$ denota el **embedding de entrada completo**, $e_i+p_i+s_i$, en lugar del identificador de un token utilizado en la definición de la pérdida. El encoder apila $L$ bloques:
>
> $$
> H^{[0]}=[x_1,\ldots,x_{m+n+3}]^\top
> \in\mathbb R^{(m+n+3)\times d_{\mathrm{model}}},
> $$
>
> $$
> H^{[l]}
> =\operatorname{EncoderBlock}^{[l]}(H^{[l-1]})
> =[h_1^l,\ldots,h_{m+n+3}^l]^\top,
> \qquad l=1,\ldots,L.
> $$
>
> La matriz tiene **una fila por token**. En esta escritura, el apilamiento con $\top$ expresa la orientación matricial; al aplicar las cabezas se toma cada estado como vector fila.
>
> Las dos salidas de pretraining son:
>
> $$
> \begin{aligned}
> \text{MLM:}\quad
> &\operatorname{softmax}(h_i^LW_{\mathrm{MLM}})
> &&\text{para cada }i\in M,\\
> \text{NSP:}\quad
> &p(y\mid s_A,s_B)
> =\operatorname{softmax}(h_{\mathrm{[CLS]}}^LW_{\mathrm{NSP}}),
> &&y\in\{\mathrm{IsNext},\mathrm{NotNext}\}.
> \end{aligned}
> $$
>
> $W_{\mathrm{MLM}}$ proyecta al vocabulario y $W_{\mathrm{NSP}}$ a dos clases. El encoder y ambas cabezas tienen parámetros entrenables.

##### 13.2. Swapping the Head for Classification

> Para adaptar BERT a una clasificación de $K$ clases, se introduce una cabeza nueva:
>
> $$
> W_{\mathrm{new}}\in\mathbb R^{d_{\mathrm{model}}\times K},
> \qquad
> y_{\mathrm{[CLS]}}
> =\operatorname{softmax}(h_{\mathrm{[CLS]}}^LW_{\mathrm{new}})
> \in\mathbb R^K.
> $$
>
> Para una entrada de $m$ tokens, la formulación abreviada del clasificador es:
>
> $$
> H=\operatorname{Encoder}([x_{\mathrm{[CLS]}},x_1,\ldots,x_m]^\top)
> \in\mathbb R^{(m+1)\times d_{\mathrm{model}}},
> $$
>
> $$
> z=h_{\mathrm{[CLS]}}^LW_{\mathrm{new}},
> \qquad y=\operatorname{softmax}(z)\in\mathbb R^K.
> $$
>
> Esta formulación abrevia el formato de tokens especiales para destacar el estado de clasificación; en la preparación de la entrada se mantiene el formato requerido por el tokenizer del modelo.
>
> Se ejecutan unas pocas épocas de fine-tuning con ejemplos etiquetados de la tarea. La cabeza nueva aprende a relacionar la representación con las clases y, en el fine-tuning habitual de BERT, **también se ajustan los parámetros del encoder**.
>
> La cabeza depende de la tarea: clasificación de una entrada usa `[CLS]`, mientras que una tarea con decisiones por token utiliza los estados de las posiciones correspondientes. Se reutilizan las representaciones del encoder y se cambia la forma de convertirlas en una salida.

#### 14. ModernBERT

> **ModernBERT**, publicado en 2024, mantiene el diseño encoder-only y moderniza BERT. La comparación presentada destaca:
>
> - Mayor velocidad y eficiencia de memoria, del orden de **2×** en las condiciones de comparación.
> - Ampliación del contexto máximo desde **512 tokens** de BERT hasta aproximadamente **8k tokens**.
> - Mejor rendimiento global en las evaluaciones consideradas.
>
> Las mejoras de velocidad y memoria dependen de la implementación, hardware y carga de trabajo. Un encoder moderno puede seguir siendo una opción útil para tareas de representación y comprensión, aunque existan grandes modelos generativos.

##### 14.1. Fill-mask with Hugging Face

> El ejemplo crea una `pipeline` de `transformers` para **fill-mask** usando `answerdotai/ModernBERT-base`. `device=0` selecciona la primera GPU y `dtype=torch.float16` solicita precisión de 16 bits; la configuración presupone un entorno compatible.

```python
import torch
from transformers import pipeline

pipeline = pipeline(
    task="fill-mask",
    model="answerdotai/ModernBERT-base",
    dtype=torch.float16,
    device=0
)

pipeline("The theory of relativity was proposed by Albert [MASK].")
```

> La salida ilustrativa contiene candidatos y puntuaciones de predicción para la posición enmascarada:

```python
[
    {'score': 0.9995, 'token_str': ' Einstein'},
    {'score': 0.00005, 'token_str': ' Wilson'},
    {'score': 0.00004, 'token_str': ' Ellis'},
    {'score': 0.00004, 'token_str': ' Lorentz'},
    {'score': 0.00004, 'token_str': ' Wien'}
]
```

> `Einstein` concentra prácticamente toda la probabilidad mostrada. Esto ejemplifica recuperación de un token utilizando el contexto bidireccional; no es generación autoregresiva de una respuesta completa. El listado recoge candidatos de la salida ilustrativa, no todos los tokens del vocabulario.

### V. T5 and Span Corruption

#### 15. A Unified Text-to-text Framework

> **T5** significa **Text-To-Text Transfer Transformer**. Utiliza un encoder-decoder y formula las tareas de NLP como problemas **sequence-to-sequence**, con texto tanto en la entrada como en la salida.
>
> La tarea se indica mediante un prefijo textual. Traducción, resumen, clasificación y question answering comparten así una forma de entrada-salida y un mecanismo de generación.

![[apuntes-7c8df3a83719-p0100-bc9566232f52.png]]

> La figura reúne cuatro aplicaciones:
>
> - **Traducción:** `translate English to German: That is good.` produce `Das ist gut.`.
> - **Aceptabilidad:** una entrada CoLA como `The course is jumping well.` produce una etiqueta textual como `not acceptable`.
> - **Similitud:** dos frases sobre un rinoceronte pastando producen una puntuación representada como texto, `3.8`.
> - **Resumen:** un texto sobre una tormenta y la respuesta de los servicios de emergencia se transforma en una versión breve.
>
> En clasificación, la salida puede ser una palabra que representa una clase; en similitud, una cadena que representa un número. No es necesario que todas las tareas tengan una cabeza de clasificación distinta: el decoder genera el texto target con el mismo mecanismo.

#### 16. Span Corruption

##### 16.1. Corrupting and Reconstructing Spans

> El pretraining de T5 usa un objetivo de **denoising** basado en **span corruption**. Se eliminan grupos de tokens consecutivos y el modelo aprende a reconstruirlos.
>
> A diferencia del enmascaramiento de posiciones individuales de BERT:
>
> 1. Seleccionamos tokens que se van a ocultar.
> 2. Agrupamos los seleccionados consecutivos en spans.
> 3. Sustituimos cada span por un **sentinel token** distinto.
> 4. El encoder recibe el texto restante con esos sentinels.
> 5. El decoder genera los spans eliminados, precedidos por los sentinels que los identifican, y un sentinel final.

![[apuntes-7c8df3a83719-p0105-14b3539cae91.png]]

> Para el ejemplo:
>
> - Texto original: `Thank you for inviting me to your party last week.`
> - Entrada del encoder: `Thank you <X> me to your party <Y> week.`
> - Target del decoder: `<X> for inviting <Y> last <Z>`.
>
> `for inviting` es un span y `last` otro. `<X>` y `<Y>` permiten asociar cada fragmento generado con el hueco correspondiente. `<Z>` es el sentinel final del target.
>
> El target contiene **los fragmentos eliminados y sus delimitadores**, no una copia completa del texto original. El decoder debe utilizar tanto el texto visible del encoder como los tokens anteriores de su propia salida.

##### 16.2. Conditional Cross-entropy

> Sea $x$ la secuencia fuente corrompida del encoder y $y=(y_1,\ldots,y_T)$ la secuencia target, formada por sentinels y tokens eliminados. Con teacher forcing, el decoder utiliza los tokens correctos anteriores del target.
>
> Si $h_i^L$ es el estado de la última capa del decoder después de procesar el prefijo $y_1,\ldots,y_i$, la LM head produce:
>
> $$
> u_i=h_i^LW,\qquad
> \hat p_i=\operatorname{softmax}(u_i),
> $$
>
> $$
> \hat p_i[y_{i+1}]
> =P(y_{i+1}\mid x,y_1,\ldots,y_i).
> $$
>
> La cross-entropy de ese token es:
>
> $$
> L_{\mathrm{CE}}(y_{i+1})
> =-\log\hat p_i[y_{i+1}].
> $$

> [!warning] Corrección
> En el material aparece $P(y_{i+1}\mid y_1,\ldots,y_i)$ para T5, pero la expresión correcta es $P(y_{i+1}\mid x,y_1,\ldots,y_i)$: la generación del decoder también está condicionada por la entrada del encoder $x$.
> Fuente de comprobación: [Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer](https://arxiv.org/html/1910.10683v4#S2.S4).

> Para incluir desde el **primer token target**, se introduce el token de inicio del decoder antes de $y_1$. Podemos escribir la pérdida media sobre los $T$ targets como:
>
> $$
> L_{\mathrm{span}}(x,y)
> =-\frac{1}{T}\sum_{t=1}^{T}
> \log P(y_t\mid x,y_1,\ldots,y_{t-1}).
> $$
>
> Para $t=1$, el prefijo de tokens target está vacío y el decoder parte de su token de inicio. La entrada se desplaza respecto del target: el estado que predice $y_t$ no recibe ese token como parte del prefijo.
>
> En el ejemplo resuelto, $\hat p_1,\ldots,\hat p_6$ se numeran **por la posición target que predicen**, en lugar de por el último token del prefijo. Los seis targets ilustrativos son `<X>`, `for`, `inviting`, `<Y>`, `last` y `<Z>`:
>
> $$
> \begin{aligned}
> \mathcal L=\frac{1}{6}\big(&
> -\log\hat p_1[\text{<X>}]
> -\log\hat p_2[\text{for}]
> -\log\hat p_3[\text{inviting}]\\
> &-\log\hat p_4[\text{<Y>}]
> -\log\hat p_5[\text{last}]
> -\log\hat p_6[\text{<Z>}]\big).
> \end{aligned}
> $$
>
> Es una media de cross-entropies, igual que en otros objetivos de predicción de tokens; lo que cambia es **qué recibe el encoder, qué debe producir el decoder y cuál es el contexto de cada predicción**.
>
> La unidad de token del ejemplo es ilustrativa; una implementación utiliza la tokenización efectiva de su vocabulario.

##### 16.3. Relationship to Other Objectives

> En T5 se estudiaron también objetivos como causal language modeling, pero span corruption ofreció los mejores resultados en la comparación considerada. Este resultado depende del diseño y evaluación del modelo; no implica que span corruption domine CLM en cualquier arquitectura.
>
> Los tres enfoques reutilizan el aprendizaje de predicción de tokens:
>
> - **GPT:** recuperar el próximo token desde un prefijo causal.
> - **BERT:** recuperar el token original de una posición seleccionada desde una entrada parcialmente corrompida y bidireccional.
> - **T5:** generar una secuencia de spans eliminados desde una entrada corrompida y el prefijo del target.

#### 17. Transfer Results

> T5 consiguió resultados de state of the art en varias tareas en su evaluación histórica, incluyendo question answering, resumen y clasificación. Las tablas muestran el efecto de la escala en SQuAD y SuperGLUE.
>
> **EM** (*exact match*) exige coincidencia exacta con la respuesta; **F1** combina precisión y recall. En los resultados de comprensión con varias tareas, cada columna conserva su métrica. Los números de “Previous best” pueden proceder de sistemas distintos para cada tarea.

| Modelo | SQuAD EM | SQuAD F1 | SuperGLUE Average | BoolQ Accuracy | CB F1 | CB Accuracy | COPA Accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Previous best | 90.1 | 95.5 | 84.6 | 87.1 | 90.5 | 95.2 | 90.6 |
| T5-Small | 79.10 | 87.24 | 63.3 | 76.4 | 56.9 | 81.6 | 46.0 |
| T5-Base | 85.44 | 92.08 | 76.2 | 81.4 | 86.2 | 94.0 | 71.2 |
| T5-Large | 86.66 | 93.79 | 82.3 | 85.4 | 91.6 | 94.8 | 83.4 |
| T5-3B | 88.53 | 94.95 | 86.4 | 89.9 | 90.3 | 94.4 | 92.0 |
| T5-11B | **91.26** | **96.22** | **88.9** | **91.2** | **93.9** | **96.8** | **94.8** |

| Modelo | MultiRC F1a | MultiRC EM | ReCoRD F1 | ReCoRD Accuracy | RTE Accuracy | WiC Accuracy | WSC Accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Previous best | 84.4 | 52.5 | 90.6 | 90.0 | 88.2 | 69.9 | 89.0 |
| T5-Small | 69.3 | 26.3 | 56.3 | 55.4 | 73.3 | 69.6 | 70.5 |
| T5-Base | 79.7 | 43.1 | 75.0 | 74.2 | 81.5 | 68.3 | 80.8 |
| T5-Large | 83.3 | 50.7 | 86.8 | 85.9 | 87.8 | 69.3 | 86.3 |
| T5-3B | 86.8 | 58.3 | 91.2 | 90.4 | 90.7 | 72.1 | 90.4 |
| T5-11B | **88.1** | **63.3** | **94.1** | **93.4** | **92.5** | **76.9** | **93.8** |

> T5-11B supera las referencias mostradas en todas estas columnas. La tendencia general favorece modelos mayores, aunque algunas métricas intermedias no mejoran de manera estrictamente monótona. La evidencia combina **pretraining, adaptación y escala** dentro de un formato común text-to-text.

### VI. Final Summary

| Modelo o familia | Arquitectura | Objetivo de pretraining | Contexto para predecir | Salida característica |
| --- | --- | --- | --- | --- |
| GPT | Decoder-only | CLM | Prefijo causal | Próximo token |
| BERT | Encoder-only | MLM + NSP | Entrada bidireccional corrompida; pares de segmentos para NSP | Tokens originales seleccionados y clase IsNext/NotNext |
| T5 | Encoder-decoder | Span corruption | Entrada fuente del encoder y prefijo causal del decoder | Spans eliminados delimitados por sentinels |

> - **Encoder-decoder:** el encoder representa la entrada; el decoder genera la salida. Cross-attention usa queries del decoder y keys/values del encoder.
> - **Dimensiones:** con $n$ queries y $m$ keys, la matriz de pesos es $n\times m$. La salida tiene una representación por query.
> - **Pretraining:** aprende una base reutilizable con grandes corpus. La mezcla y la limpieza de datos importan junto con su tamaño.
> - **SFT y alignment:** adaptan el comportamiento hacia respuestas a instrucciones y preferencias. Un base model no es automáticamente un asistente.
> - **GPT:** la pérdida causal supervisa el siguiente token. El pretraining facilita fine-tuning e ICL; ICL utiliza ejemplos en el prompt sin actualizar pesos.
> - **BERT:** el 15% seleccionado se distribuye en 80% máscaras, 10% sustituciones aleatorias y 10% sin cambios. MLM supervisa las posiciones seleccionadas; NSP clasifica pares usando el estado final de `[CLS]`.
> - **Fine-tuning de BERT:** cambia la cabeza según la tarea y puede ajustar todo el encoder. La entrada combina embeddings de token, posición y segmento.
> - **T5:** expresa las tareas como texto a texto. En span corruption, el encoder recibe el texto con huecos y el decoder genera los fragmentos eliminados, condicionado por esa entrada.
> - **Pérdidas:** CLM, MLM y span corruption usan cross-entropy de tokens, pero difieren en targets, contexto y posiciones supervisadas. NSP añade una pérdida de clasificación binaria.
