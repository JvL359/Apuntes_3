---
estado: pendiente de revisión
---

### I. Decoder-only Language Models

#### 1. From the Transformer Decoder to a Language Model

> Un **decoder-only model** utiliza una pila de bloques del decoder para generar texto. Al independizarlo del Transformer encoder-decoder, se eliminan el encoder y la **cross-attention** que permitía consultar sus salidas. El prompt y los tokens generados forman una única secuencia que se procesa mediante self-attention.
>
> Cada bloque conserva dos componentes principales: **masked multi-head self-attention** y una **position-wise feed-forward network**, con conexiones residuales y layer normalization. La máscara restringe el contexto disponible en cada posición.
>
> Comparado con un encoder, los dos cambios esenciales son la restricción causal de self-attention y una **language modelling head (LM head)** sobre la salida de la pila. Esta cabeza transforma las representaciones contextuales en probabilidades del siguiente token.
>
> En el esquema, las regiones rojas corresponden a los componentes eliminados. La entrada del decoder se encuentra desplazada respecto a los tokens que se deben predecir: cada posición recibe un token y predice el siguiente.

![[apuntes-9edd1e106fe5-p0005-fce324e81284.png]]

#### 2. Next-token Prediction and the LM Head

##### 2.1. The Language Modelling Objective

> Un **language model** asigna una distribución de probabilidad al siguiente token dado un contexto:
>
> $$
> p_{\mathrm{LM}}(w_{t+1}\mid w_1,\ldots,w_t).
> $$
>
> Este objetivo también aparecía en los modelos n-gram, feed-forward y RNN. Lo que cambia en un decoder-only es el mecanismo que representa el contexto.
>
> Para generar después de una entrada de $N$ tokens, tomamos la representación del **último token en la última capa**, $h_N^L$. Aquí $N$ es la longitud de entrada y $L$ el número de bloques. Los embeddings iniciales son $x_1,\ldots,x_N$ y $h_t^\ell$ representa la posición $t$ tras el bloque $\ell$.
>
> Mediante attention, $h_N^L$ incorpora información del prefijo útil para predecir el siguiente token. Que resuma el contexto no significa que codifique perfectamente todo el texto, sino que su entrenamiento la orienta a esta tarea.

##### 2.2. Linear Projection and Softmax

> La LM head contiene una proyección lineal aprendible:
>
> $$
> U\in\mathbb{R}^{d_{\mathrm{model}}\times |V|},
> \qquad u=h_N^L U\in\mathbb{R}^{1\times |V|}.
> $$
>
> Usamos vectores fila: $h_N^L$ tiene dimensión $1\times d_{\mathrm{model}}$. El vector $u$ contiene un **logit** por token del vocabulario $V$. Los logits son puntuaciones reales; todavía no son probabilidades.
>
> Una softmax sobre el vocabulario produce:
>
> $$
> y=\operatorname{softmax}(u),
> \qquad y[v]=\frac{e^{u[v]}}{\sum_{z\in V}e^{u[z]}}.
> $$
>
> La salida satisface $y[v]\geq0$ y $\sum_{v\in V}y[v]=1$. El modelo proporciona la distribución; la **decoding strategy** determina cómo elegir un token a partir de ella.
>
> Por ejemplo, después de «The fish lived in the», una distribución ilustrativa asigna a «sea» el 22 %, a «blue» el 17 %, a «river» el 16 % y a «ocean» el 14 %. También aparecen «when» con el 7 %, «under» con el 2 % y «bicycle» con el 1 %. Son solo algunos tokens: la probabilidad restante corresponde al resto del vocabulario.
>
> El diagrama muestra el cambio de dimensión desde la representación contextual hasta una puntuación y una probabilidad por token.

![[apuntes-9edd1e106fe5-p0016-90096d04451f.png]]

#### 3. Autoregressive Inference

> Durante **inference**, generamos texto de un token en un token:
>
> 1. Introducimos el **prompt** en el modelo.
> 2. Calculamos la distribución del siguiente token con la LM head.
> 3. Elegimos un token mediante la estrategia de decoding.
> 4. Lo añadimos al contexto y repetimos el proceso.
>
> Si tras «The fish lived in the» elegimos «sea», la siguiente predicción se condiciona por «The fish lived in the sea». La distribución se recalcula para el nuevo contexto; los tokens no se eligen independientemente unos de otros.
>
> La generación termina cuando aparece **EOS**, el token de final de secuencia, o cuando se alcanza la longitud máxima de salida. Este bucle es **autoregressive generation**: cada token generado se convierte en parte de la entrada de los pasos posteriores.
>
> Aunque el Transformer permite procesar en paralelo las posiciones de un contexto ya disponible, los nuevos tokens dependen de decisiones anteriores. Esa dependencia mantiene la generación secuencial.

#### 4. Self-supervised Training

##### 4.1. Prefixes and Targets

> Un decoder-only LM puede entrenarse sobre texto bruto, por ejemplo procedente de Internet, sin etiquetado manual: el propio texto proporciona el siguiente token correcto. Esto se denomina **self-supervised learning**.
>
> El texto «The fish lived in the sea EOS» proporciona los siguientes pares de prefijo y objetivo. Incluyendo EOS, son siete tokens y seis predicciones.

| Input prefix | Correct next token |
| --- | --- |
| The | fish |
| The fish | lived |
| The fish lived | in |
| The fish lived in | the |
| The fish lived in the | sea |
| The fish lived in the sea | EOS |

> En general, una secuencia de $N$ tokens, contando el token final incluido en ella, proporciona $N-1$ pares de este tipo. Si contamos solo los seis tokens de entrada y dejamos EOS como objetivo final adicional, obtenemos una predicción por posición de entrada. Hay que distinguir ambas formas de contar.
>
> Durante el entrenamiento se emplean los tokens correctos del texto como contexto. No hace falta generar una continuación para descubrir cuál es el objetivo.

##### 4.2. Cross-entropy Loss

> Para una predicción, evaluamos la probabilidad que el modelo ha asignado al token correcto:
>
> $$
> \ell=-\log y[\text{correct token}].
> $$
>
> Si el objetivo es «sea» y $y[\text{sea}]=0.22$, con logaritmo natural:
>
> $$
> \ell=-\log0.22\approx1.5.
> $$
>
> Esta es la **cross-entropy loss** con un objetivo que concentra toda su probabilidad en el token correcto. Si el modelo le asigna probabilidad $1$, la pérdida es $0$; cuanto menor es esa probabilidad, mayor es la pérdida.
>
> En inference elegimos una continuación. En training conocemos el token correcto y evaluamos su probabilidad; no muestreamos un token para calcular esta pérdida.
>
> La pérdida del ejemplo completo es la media de sus seis pérdidas:
>
> $$
> \mathcal{L}=\frac{\ell_1+\ell_2+\cdots+\ell_6}{6}.
> $$
>
> Por ejemplo, $\ell_1=-\log y_1[\text{fish}]$, $\ell_2=-\log y_2[\text{lived}]$ y $\ell_6=-\log y_6[\mathrm{EOS}]$. Cada distribución corresponde a un contexto distinto.

##### 4.3. All Predictions in One Forward Pass

> Una implementación directa introduciría cada prefijo por separado. Para $N$ tokens con el objetivo final incluido, necesitaría $N-1$ llamadas al modelo y repetiría el procesamiento de muchos tokens.
>
> Podemos introducir toda la secuencia de entrada como una matriz de embeddings y obtener una representación $h_t^L$ por posición. Aplicamos **la misma LM head** a todas ellas:
>
> $$
> y_t=\operatorname{softmax}(h_t^L U).
> $$
>
> La salida de la posición de «The» se compara con «fish»; la de «fish», con «lived»; y así sucesivamente. La última posición de entrada, «sea», se compara con EOS. Las etiquetas están **desplazadas un token** respecto a la entrada.
>
> El esquema dibuja varias LM heads para mostrar su aplicación por posición, pero todas comparten la misma matriz $U$. En una sola pasada obtenemos las distribuciones, las pérdidas individuales y su media.

![[apuntes-9edd1e106fe5-p0033-5a042fa13c6d.png]]

> Esta paralelización solo conserva el problema de predicción correcto si cada posición tiene acceso al mismo prefijo que tendría en una llamada individual. La self-attention sin máscara permite consultar tokens futuros y rompe esa condición.

#### 5. Causal Masked Attention

##### 5.1. Why the Future Must Be Hidden

> Si introducimos «The fish lived in the sea» y dejamos que todas las posiciones atiendan a todas las demás, la representación de «fish» puede consultar «lived», aunque precisamente deba predecirlo.
>
> El modelo podría aprovechar una **fuga de información**: copiar o utilizar el objetivo que ya está presente más adelante en la entrada. Durante inference ese futuro todavía no existe.
>
> La **causal mask**, también llamada **look-ahead mask**, impide atender a posiciones posteriores. La posición $i$ puede consultar las posiciones $j\leq i$, incluida ella misma. Esto es coherente porque el objetivo de esa fila es el token de la posición $i+1$.

##### 5.2. Scores, Mask, Weights and Values

> Una cabeza comienza con las proyecciones habituales:
>
> $$
> Q=XW^Q,\qquad K=XW^K,\qquad V=XW^V.
> $$
>
> En esta expresión, $V$ es la **matriz de values**; el contexto distingue este uso del vocabulario $V$. Los scores de atención son:
>
> $$
> S=\frac{QK^\top}{\sqrt{d_k}}.
> $$
>
> Cada fila corresponde a una query y cada columna a una key. Antes de aplicar softmax, sumamos la máscara:
>
> $$
> M_{ij}=
> \begin{cases}
> 0,&j\leq i,\\
> -\infty,&j>i.
> \end{cases}
> $$
>
> Así, las posiciones permitidas conservan su score y las posiciones futuras reciben $-\infty$. En implementaciones numéricas puede usarse un valor negativo de magnitud muy grande.
>
> Aplicamos softmax **por filas** y multiplicamos los pesos por los values:
>
> $$
> A=\operatorname{softmax}_{\mathrm{row}}(S+M),
> \qquad \mathrm{output}=AV.
> $$
>
> Como $e^{-\infty}=0$, los pesos de las posiciones futuras son cero. Los pesos permitidos de cada fila suman $1$. La máscara restringe las conexiones de attention antes de la normalización.

##### 5.3. A Numerical Masking Example

> Para «robots must obey orders», tomamos la siguiente matriz ilustrativa de scores para mostrar el enmascaramiento:
>
> $$
> S=
> \begin{pmatrix}
> 2.1&0.3&1.2&0.8\\
> 0.5&1.9&0.2&1.1\\
> 1.4&0.7&2.3&0.6\\
> 0.9&1.6&0.4&2.0
> \end{pmatrix}.
> $$
>
> El orden de filas y columnas es «robots», «must», «obey», «orders». La máscara produce:
>
> $$
> S+M=
> \begin{pmatrix}
> 2.1&-\infty&-\infty&-\infty\\
> 0.5&1.9&-\infty&-\infty\\
> 1.4&0.7&2.3&-\infty\\
> 0.9&1.6&0.4&2.0
> \end{pmatrix}.
> $$
>
> Tras la softmax, redondeando a cuatro decimales:
>
> $$
> A\approx
> \begin{pmatrix}
> 1&0&0&0\\
> 0.1978&0.8022&0&0\\
> 0.2528&0.1255&0.6217&0\\
> 0.1510&0.3040&0.0916&0.4535
> \end{pmatrix}.
> $$
>
> «Robots» solo atiende a sí mismo. «Must» atiende a «robots» y «must». «Obey» puede consultar tres tokens y «orders» los cuatro. Por ejemplo:
>
> $$
> A_{21}=\frac{e^{0.5}}{e^{0.5}+e^{1.9}}\approx0.1978.
> $$
>
> Los valores enmascarados no participan en el denominador. Después, $AV$ mezcla únicamente los values permitidos para cada posición.

> [!warning] Corrección
> En el material aparece la matriz ilustrativa $S$ como resultado de multiplicar unas matrices concretas $Q$ y $K^\top$, pero la expresión correcta para esas matrices es $QK^\top/\sqrt{3}$ y no coincide con $S$. Por ejemplo, su entrada $(1,1)$ es $(0.2\cdot0.6+0.7\cdot0.9+0.4\cdot0.3)/\sqrt{3}\approx0.5023$, no $2.1$. El ejemplo de máscara anterior utiliza $S$ como punto de partida independiente.
> Fuente de comprobación: [Fuente oficial o académica](https://arxiv.org/html/1706.03762v7#S3.SS2.SSS1)

> Las matrices concretas del ejemplo son:
>
> $$
> Q=
> \begin{pmatrix}
> 0.2&0.7&0.4\\
> 0.5&0.1&0.9\\
> 0.8&0.6&0.3\\
> 0.4&0.9&0.5
> \end{pmatrix},
> \qquad
> K^\top=
> \begin{pmatrix}
> 0.6&0.1&0.8&0.3\\
> 0.9&0.4&0.2&0.7\\
> 0.3&0.8&0.5&0.6
> \end{pmatrix}.
> $$
>
> Su producto escalado resulta:
>
> $$
> \frac{QK^\top}{\sqrt{3}}\approx
> \begin{pmatrix}
> 0.5023&0.3580&0.2887&0.4561\\
> 0.3811&0.4677&0.5023&0.4388\\
> 0.6409&0.3233&0.5254&0.4850\\
> 0.6928&0.4619&0.4330&0.6062
> \end{pmatrix}.
> $$
>
> Para continuar el cálculo con estas queries y keys se enmascara esta última matriz. La matriz ilustrativa $S$ anterior permite estudiar por separado el efecto de la máscara y la softmax.

##### 5.4. Decoder Block

> En la definición matricial del bloque se usa $L$ para la **longitud de la secuencia**, con $X\in\mathbb{R}^{L\times d_{\mathrm{model}}}$. Esta convención intercambia los papeles de $N$ y $L$ respecto a los diagramas con $h_N^L$.
>
> Cada cabeza calcula:
>
> $$
> \mathrm{head}=
> \operatorname{Softmax}_{\mathrm{row}}
> \left(\frac{QK^\top+M}{\sqrt{d_k}}\right)V.
> $$
>
> Con una máscara cuyos valores son $0$ y $-\infty$, colocarla antes o después de dividir por $\sqrt{d_k}>0$ mantiene las mismas posiciones permitidas y bloqueadas. Si se utiliza un valor finito muy negativo, su escala debe ser suficiente para anular numéricamente los pesos futuros.
>
> Las cabezas se concatenan y se proyectan de nuevo a dimensión $d_{\mathrm{model}}$. La formulación del bloque coloca layer normalization después de cada suma residual:
>
> $$
> Z=\operatorname{LayerNorm}\bigl(X+\operatorname{MaskedMHA}(X)\bigr),
> $$
>
> $$
> \operatorname{DecoderBlock}(X)
> =\operatorname{LayerNorm}\bigl(Z+\operatorname{FFN}(Z)\bigr).
> $$
>
> La FFN actúa por posición, por lo que no introduce acceso al futuro. Aplicar la máscara en todas las capas mantiene la restricción causal a lo largo de la pila.

##### 5.5. Complete Decoder

> Sean $X$ los token embeddings y $P$ los positional encodings, ambos en $\mathbb{R}^{L\times d_{\mathrm{model}}}$. Primero incorporamos la posición:
>
> $$
> X_0=X+P.
> $$
>
> Después aplicamos $N$ decoder blocks:
>
> $$
> X_n=\operatorname{DecoderBlock}(X_{n-1}),
> \qquad n=1,\ldots,N.
> $$
>
> La LM head procesa todas las filas de $X_N$:
>
> $$
> Y=\operatorname{Softmax}_{\mathrm{row}}(X_NU)
> \in\mathbb{R}^{L\times |V|}.
> $$
>
> Su fila $i$ representa $P(\,\cdot\mid w_1,\ldots,w_i)$. En training usamos todas las filas con sus objetivos desplazados; para continuar un prompt en inference usamos la distribución de la última posición disponible.

### II. Deterministic Decoding

#### 6. Decoding as a Search Problem

> **Decoding** es el proceso de seleccionar tokens para construir la salida de un language model. Cambiar la estrategia puede alterar considerablemente el texto generado sin cambiar los parámetros del modelo.
>
> Una primera familia contiene métodos **deterministas**, como greedy decoding y beam search. Otra utiliza **sampling**, que introduce aleatoriedad. Contrastive search es una alternativa determinista que combina confianza del modelo y una penalización de degeneración.
>
> Dado un prompt $\mathbf{w}$, una elección natural consiste en buscar la secuencia más probable:
>
> $$
> \mathbf{w}^{*}=\arg\max_{\mathbf{y}\in V^{*}}P(\mathbf{y}\mid\mathbf{w}).
> $$
>
> $V^{*}$ es el conjunto de secuencias finitas sobre el vocabulario $V$, que incluye EOS. En el problema de decoding restringimos la búsqueda a respuestas admisibles, por ejemplo terminadas en EOS o de una longitud fijada. Sin esta condición, la secuencia vacía tendría probabilidad $1$ y sería una solución trivial. En una búsqueda práctica también imponemos una longitud máxima.
>
> Si $\mathbf{w}=(w_1,\ldots,w_m)$ y $\mathbf{y}=(y_1,\ldots,y_T)$, la probabilidad se factoriza:
>
> $$
> \begin{aligned}
> P(y_1,\ldots,y_T\mid w_1,\ldots,w_m)
> &=\prod_{i=1}^{T}P(y_i\mid\mathbf{w},y_1,\ldots,y_{i-1})\\
> &=P(y_1\mid\mathbf{w})P(y_2\mid\mathbf{w},y_1)
> \cdots P(y_T\mid\mathbf{w},y_1,\ldots,y_{T-1}).
> \end{aligned}
> $$
>
> Podemos puntuar una secuencia candidata con las probabilidades de sus tokens. Sin embargo, explorar todas las secuencias resulta inviable: solo para longitud $T=20$ y $|V|=50\,000$ hay:
>
> $$
> |V|^T=50\,000^{20}\approx10^{94}
> $$
>
> posibilidades. Con una longitud máxima $n$, el espacio de búsqueda crece como $O(|V|^n)$. Greedy y beam search exploran una parte de él para aproximar el objetivo.

#### 7. Greedy Decoding

##### 7.1. Local Decisions

> **Greedy decoding** elige el token de mayor probabilidad en cada paso:
>
> $$
> y_{n+1}=\arg\max_{v\in V}P(v\mid\mathbf{w},y_1,\ldots,y_n).
> $$
>
> Comienza con el prompt, obtiene la distribución, selecciona su máximo y añade ese token. Repite hasta EOS o el límite de longitud. Si hay empate, una regla de desempate fija conserva el comportamiento determinista.
>
> La estrategia es simple y rápida, porque solo mantiene una secuencia. Su limitación es que una elección **localmente óptima** puede conducir a una continuación globalmente peor.

##### 7.2. Local Optimum versus Sequence Optimum

> En un árbol de generación, cada rama añade un token y cada nodo puede indicar su probabilidad condicionada por el camino anterior. Mostrar los dos tokens más probables en cada nivel permite visualizar algunas alternativas, aunque no representa todo el vocabulario.
>
> Con GPT-2 y el prompt «I have a dream», cinco tokens nuevos mediante greedy producen el ejemplo «I have a dream of being a doctor.».
>
> La comparación resuelta entre dos caminos de cinco tokens, contando la puntuación, muestra:
>
> $$
> \log P(\text{«of being a doctor.»}\mid\text{«I have a dream»})=-10.42,
> $$
>
> $$
> \log P(\text{«.I have a dream»}\mid\text{«I have a dream»})=-6.26.
> $$
>
> El segundo camino tiene mayor probabilidad, aunque greedy elija el primero. Elegir el máximo en cada distribución condicionada por decisiones previas no equivale a maximizar conjuntamente la secuencia.
>
> Si $y_1,\ldots,y_T$ son las decisiones de greedy, en general no podemos identificar su puntuación con el máximo global:
>
> $$
> \underbrace{
> \max_{y_1\in V}P(y_1\mid\mathbf{w})
> \prod_{t=2}^{T}\max_{y_t\in V}P(y_t\mid y_1,\ldots,y_{t-1},\mathbf{w})
> }_{\text{decisiones sucesivas sobre el prefijo elegido}}
> \neq
> \underbrace{
> \max_{\mathbf{y}\in V^{*}}\left[
> P(y_1\mid\mathbf{w})\prod_{t=2}^{|\mathbf{y}|}
> P(y_t\mid y_1,\ldots,y_{t-1},\mathbf{w})\right]
> }_{\text{búsqueda conjunta de la secuencia}}.
> $$
>
> La desigualdad expresa la falta de garantía de igualdad; en algunos casos ambos métodos sí pueden coincidir.

##### 7.3. GPT-2 with Hugging Face

> `AutoTokenizer` convierte el prompt en los tensores de entrada. `AutoModelForCausalLM` carga GPT-2 con su cabeza de language modelling. El modelo y los tensores se colocan en GPU si CUDA está disponible, o en CPU en caso contrario.
>
> Esta preparación se reutiliza en los ejemplos de generación siguientes. Se asigna EOS como token de padding para GPT-2.

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed
import torch

torch_device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained(
    "gpt2",
    pad_token_id=tokenizer.eos_token_id,
).to(torch_device)

model_inputs = tokenizer(
    "I have a dream",
    return_tensors="pt",
).to(torch_device)
```

> La llamada siguiente utiliza greedy y permite cinco tokens nuevos. `max_new_tokens` cuenta tokens añadidos, no la longitud del prompt. `decode()` devuelve el texto completo, y `skip_special_tokens=True` oculta los tokens especiales en la visualización.

```python
greedy_output = model.generate(**model_inputs, max_new_tokens=5)

print("Output:\n" + 100 * "-")
print(tokenizer.decode(greedy_output[0], skip_special_tokens=True))
```

> El ejemplo de salida es:

```text
I have a dream of being a doctor.
```

> Si ampliamos la generación a treinta tokens, el ejemplo muestra **decoding degeneration**: repeticiones que reducen la calidad del texto.

```python
greedy_output = model.generate(**model_inputs, max_new_tokens=30)

print("Output:\n" + 100 * "-")
print(tokenizer.decode(greedy_output[0], skip_special_tokens=True))
```

```text
I have a dream of being a doctor. I have a dream of being a doctor. I have a dream of being a doctor. I have a dream of being a
```

> Greedy es computacionalmente barato, pero su preferencia por tokens muy predecibles puede producir texto **genérico** y **repetitivo**.

#### 8. Beam Search

##### 8.1. Maintaining Several Hypotheses

> **Beam search** conserva hasta $k$ hipótesis parciales, donde $k$ es el **beam size**. En cada paso expande las hipótesis activas, puntúa sus continuaciones y conserva las mejores.
>
> La selección compara **secuencias parciales completas**, no solo las probabilidades del último token. Conservar varias ramas reduce el riesgo de descartar pronto una continuación útil.
>
> Para una respuesta $(y_1,\ldots,y_n)$ al prompt $\mathbf{w}$, usamos su log-probabilidad:
>
> $$
> \begin{aligned}
> \operatorname{score}(y_1,\ldots,y_n)
> &=\log P(y_1,\ldots,y_n\mid\mathbf{w})\\
> &=\sum_{i=1}^{n}\log P(y_i\mid\mathbf{w},y_1,\ldots,y_{i-1})\\
> &=\log P(y_1\mid\mathbf{w})
> +\log P(y_2\mid\mathbf{w},y_1)+\cdots.
> \end{aligned}
> $$
>
> Los logaritmos convierten productos en sumas. Las puntuaciones son no positivas; una puntuación mayor, más próxima a cero, representa mayor probabilidad. Inicialmente el prompt tiene score $0$, porque puntuamos la continuación **condicionada** por él.
>
> Con $k=1$, la versión sin penalizaciones y con los mismos criterios de parada se reduce a greedy. Valores como $5$ o $10$ permiten mantener más alternativas a costa de más cálculo.

##### 8.2. An Example with Natural Language

> Después de «The», el ejemplo asigna probabilidad $0.5$ a «nice», $0.4$ a «dog» y $0.1$ a «car». Greedy sigue «nice» y después «woman», con probabilidad condicionada $0.4$:
>
> $$
> P(\text{«nice woman»}\mid\text{«The»})=0.5\cdot0.4=0.20.
> $$
>
> Un beam de tamaño $2$ conserva también «dog». Su continuación «has» tiene probabilidad $0.9$:
>
> $$
> P(\text{«dog has»}\mid\text{«The»})=0.4\cdot0.9=0.36.
> $$
>
> Al considerar ambas ramas, puede elegir la secuencia más probable de este ejemplo. Explorar más opciones ayuda, pero un beam finito todavía puede descartar el prefijo del óptimo global.

##### 8.3. Worked Example: Vocabulary A, B, C

> Sea $V=\{A,B,C\}$, el prompt `ABA`, $k=2$ y una continuación de dos tokens. Usamos pares $\langle s,\mathbf{y}\rangle$, donde $\mathbf{y}$ contiene el prompt y la continuación, y $s$ puntúa solo esta última.
>
> El árbol muestra probabilidades y log-probabilidades **del último token condicionado por su prefijo**. Para obtener el score acumulado de una hoja sumamos las log-probabilidades de las ramas recorridas.

![[apuntes-9edd1e106fe5-p0070-e3d6f3eaafaf.png]]

> **Inicialización, $t=0$**:
>
> $$
> B_0=\{\langle0,\mathrm{ABA}\rangle\},
> \qquad F_0=\varnothing.
> $$
>
> $B_t$ contiene hipótesis activas y $F_t$ hipótesis completadas. El score inicial es $\log1=0$.
>
> **Primer paso, $t=1$**: expandimos el prompt con todos los tokens.

| Candidate | Conditional probability | Accumulated score |
| --- | ---: | --- |
| `ABAA` | $P(A\mid\mathrm{ABA})=0.5$ | $0+\log0.5\approx-0.6931$ |
| `ABAB` | $P(B\mid\mathrm{ABA})=0.3$ | $0+\log0.3\approx-1.2039$ |
| `ABAC` | $P(C\mid\mathrm{ABA})=0.2$ | $0+\log0.2\approx-1.6094$ |

> Conservamos los dos mejores candidatos:
>
> $$
> B_1=
> \{\langle-0.6931,\mathrm{ABAA}\rangle,
> \langle-1.2039,\mathrm{ABAB}\rangle\}.
> $$
>
> **Segundo paso, $t=2$**: expandimos las dos hipótesis de $B_1$. La rama `ABAC` ha sido descartada y no se expande en esta búsqueda.

| Previous hypothesis | Candidate | Next-token probability | Accumulated score |
| --- | --- | ---: | --- |
| `ABAA` | `ABAAA` | $0.4$ | $-0.6931+\log0.4\approx-1.6094$ |
| `ABAA` | `ABAAB` | $0.4$ | $-0.6931+\log0.4\approx-1.6094$ |
| `ABAA` | `ABAAC` | $0.2$ | $-0.6931+\log0.2\approx-2.3026$ |
| `ABAB` | `ABABA` | $0.3$ | $-1.2039+\log0.3\approx-2.4078$ |
| `ABAB` | `ABABB` | $0.4$ | $-1.2039+\log0.4\approx-2.1202$ |
| `ABAB` | `ABABC` | $0.3$ | $-1.2039+\log0.3\approx-2.4078$ |

> Seleccionamos:
>
> $$
> B_2=
> \{\langle-1.6094,\mathrm{ABAAA}\rangle,
> \langle-1.6094,\mathrm{ABAAB}\rangle\}.
> $$
>
> Se ha alcanzado el límite de dos tokens nuevos. Ambas candidatas tienen probabilidad $0.5\cdot0.4=0.20$, por lo que una regla de desempate determina la salida final.

> [!warning] Corrección
> En el material aparecen scores $-1.6094$, $-0.6931$ y $-1.2039$ para las hojas `ABACA`, `ABACB` y `ABACC` al etiquetar el árbol con puntuaciones acumuladas, pero las expresiones correctas son $\log(0.2\cdot0.2)\approx-3.2189$, $\log(0.2\cdot0.5)\approx-2.3026$ y $\log(0.2\cdot0.3)\approx-2.8134$. Las etiquetas originales son log-probabilidades del último token, no del camino completo. La selección de $B_2$ no cambia porque estas hojas proceden de una rama ya descartada.
> Fuente de comprobación: [Fuente oficial o académica](https://huggingface.co/blog/how-to-generate#beam-search)

##### 8.4. Completed Hypotheses and Stopping Conditions

> Distintas hipótesis pueden emitir EOS en pasos diferentes. Cuando una emite EOS, se considera **completada**: se añade a $F_t$ y deja de expandirse, mientras continuamos con las demás.
>
> Dos criterios habituales de parada son alcanzar la longitud máxima $M$ o acumular al menos un número prefijado de hipótesis completas. Ese número puede coincidir con $k$.
>
> El siguiente procedimiento usa una longitud inicial $L$, un máximo total $M$, beam size $k$, vocabulario $V$ y una función `score`. Por tanto, permite como máximo $M-L$ tokens nuevos. $\mathbf{y}\circ v$ significa concatenar el token $v$ a la secuencia.
>
> 1. Inicializamos $B_0=\{\langle0,(x_1,\ldots,x_L)\rangle\}$ y $F_0=\varnothing$.
> 2. Para $t=1,\ldots,M-L$, creamos $H=\varnothing$ y conservamos los resultados completos anteriores mediante $F_t=F_{t-1}$.
> 3. Para cada $\langle s,\mathbf{y}\rangle\in B_{t-1}$ y cada $v\in V$, calculamos $s'=\operatorname{score}(\mathbf{y}\circ v)$ y añadimos $\langle s',\mathbf{y}\circ v\rangle$ a $H$. Con score de log-probabilidad, equivale a sumar $\log P(v\mid\mathbf{y})$ al score previo.
> 4. Vaciamos $B_t$. Mientras $|B_t|<k$, extraemos de $H$ la hipótesis con mayor score.
> 5. Si su último token es EOS, la añadimos a $F_t$; en otro caso, a $B_t$.
> 6. Si $|F_t|\geq k$, devolvemos la hipótesis de mayor score en $F_t$. Si continuamos, eliminamos de $H$ la hipótesis procesada y repetimos la selección.
> 7. Al terminar los $M-L$ pasos, devolvemos la mejor hipótesis de $F_{M-L}$ si este conjunto no está vacío. Si no hay ninguna terminada, devolvemos la mejor de $B_{M-L}$.
>
> $H$ contiene todas las expansiones antes de la selección; $B_t$ contiene únicamente las continuaciones activas. Una hipótesis con EOS no ocupa un puesto del beam activo en esta variante.
>
> El bucle de selección presupone suficientes candidatos en $H$ para llenar el beam o alcanzar la parada. Si se agotan, no se puede calcular un máximo sobre un conjunto vacío: se conserva el beam disponible y se finaliza si no quedan hipótesis activas.
>
> El criterio de reunir $k$ hipótesis completas es una decisión de esta variante. Por sí solo no demuestra que la mejor respuesta global ya se haya encontrado.

##### 8.5. Length Bias and Length Penalties

> La probabilidad de una secuencia es un producto de probabilidades de tokens:
>
> $$
> P(y_1,\ldots,y_T\mid\mathbf{x})
> =\prod_{t=1}^{T}P(y_t\mid\mathbf{x},y_{<t}).
> $$
>
> Al añadir factores menores que $1$, el producto disminuye y la log-probabilidad acumula términos negativos. Por ello, al comparar respuestas de distinta longitud, el score sin modificar tiende a favorecer las más cortas. Esto no significa que cualquier respuesta corta sea más probable que cualquier respuesta larga.
>
> Una **length penalty** modifica la puntuación con una función de la longitud. La versión más simple divide por $T$:
>
> $$
> \operatorname{score}(y_1,\ldots,y_T)
> =\frac{\log P(y_1,\ldots,y_T\mid\mathbf{x})}{T}.
> $$
>
> Es la log-probabilidad media por token. Permite comparar secuencias de distinta longitud con una normalización que reduce ese sesgo. Una vez modificada la función, optimizamos este score y no la probabilidad bruta.

##### 8.6. GPT-2 with Beam Search

> `num_beams` fija el beam size. En este ejemplo se generan hasta ochenta tokens nuevos con cinco hipótesis y se impide repetir un n-gram de longitud cuatro mediante `no_repeat_ngram_size=4`.

```python
model_inputs = tokenizer(
    " I have a dream",
    return_tensors="pt",
).to(torch_device)

beam_output = model.generate(
    **model_inputs,
    max_new_tokens=80,
    num_beams=5,
    no_repeat_ngram_size=4,
)

print("Output:\n" + 100 * "-")
print(tokenizer.decode(beam_output[0], skip_special_tokens=True))
```

> `no_repeat_ngram_size` actúa sobre repeticiones, mientras que una length penalty actúa sobre la comparación de longitudes. Son mecanismos diferentes.
>
> El ejemplo conserva el tema del sueño personal y reduce la repetición literal de la misma frase:

```text
 I have a dream.

I have a dream that I will be able to live my life in peace.

My dream is that I will live my life with dignity and respect.

It is my dream to be able to do what I want to do.

And it is my dream that my life will be a happy one.

That I will have a happy life.
```

> Beam search puede encontrar continuaciones más probables que las que conserva greedy, pero sigue siendo una búsqueda aproximada y es computacionalmente más costosa.

#### 9. High Probability and Text Quality

> Greedy y beam search, con los mismos parámetros y reglas de desempate, son deterministas y buscan aproximar una continuación de alta probabilidad. Sin embargo, **máxima probabilidad no garantiza máxima calidad** en generación abierta.
>
> Una secuencia que repite expresiones muy predecibles puede recibir una probabilidad elevada y resultar poco natural. **Text degeneration** incluye texto genérico, incoherente o atrapado en bucles de repetición.
>
> Aprender un modelo mediante un objetivo de likelihood puede proporcionar buenas distribuciones sin que maximizar esa likelihood durante decoding produzca siempre la mejor redacción.
>
> La gráfica compara la probabilidad que un modelo asigna a tokens generados por beam search y a tokens de texto humano, partiendo del mismo contexto. En el ejemplo, beam search mantiene probabilidades próximas a $1$ y repite una expresión sobre el estado del arte de computer vision y machine learning. El texto humano continúa una descripción de un producto con mayor variedad, y sus probabilidades fluctúan mucho más.

![[apuntes-9edd1e106fe5-p0088-8a66ae784a70.png]]

> La variabilidad no convierte automáticamente una salida en buena, pero muestra que un texto natural no tiene que utilizar siempre la continuación más predecible.

### III. Sampling-based Decoding

#### 10. Pure Sampling and the Unreliable Tail

##### 10.1. Sampling Instead of Maximizing

> **Pure sampling** elige aleatoriamente el siguiente token con la distribución del modelo:
>
> $$
> w_t\sim P(w\mid w_1,\ldots,w_{t-1}).
> $$
>
> El símbolo $\sim$ significa «muestreado de». Se mantiene el mismo bucle autoregresivo, pero se sustituye el argmax por una extracción aleatoria.
>
> La estrategia mantiene una sola secuencia y evita el coste de conservar múltiples hipótesis de beam search. Puede producir texto más diverso y menos repetitivo, aunque tiene sus propias limitaciones.
>
> En una distribución de siguiente token suele haber unos pocos candidatos muy probables y una **long tail** de miles de tokens individualmente poco probables. La suma de sus probabilidades puede ser grande: en un ejemplo ilustrativo, el grupo principal reúne aproximadamente la mitad de la masa y la cola la otra mitad.
>
> Por tanto, «cada token de la cola es improbable» no significa «muestrear de la cola es improbable». Su masa conjunta hace que se elijan estos tokens con frecuencia. Esta **unreliable tail** puede introducir cambios de tema abruptos y producir texto inconexo.

##### 10.2. GPT-2 with Pure Sampling

> Recuperamos el prompt sin el espacio inicial del ejemplo de beam search. `do_sample=True` activa sampling y `top_k=0` desactiva el filtro top-$k$. La semilla controla la aleatoriedad del ejemplo.

```python
model_inputs = tokenizer(
    "I have a dream",
    return_tensors="pt",
).to(torch_device)

set_seed(40)
sample_output = model.generate(
    **model_inputs,
    max_new_tokens=100,
    do_sample=True,
    top_k=0,
)

print("Output:\n" + 100 * "-")
print(tokenizer.decode(sample_output[0], skip_special_tokens=True))
```

> La salida ilustrativa pasa de un sueño sobre crear una empresa a referencias políticas y militares poco conectadas entre sí:

```text
I have a dream of someday starting a company that provides most of its income to veterans, bringing back the troops, their families, homeland and people fighting us now and forever.
    The next generation."
    Kennedy toured Colorado in protest of the dubiously named Dick Cheney. During his radio address, Clinton used an old California promo to deflect those who wanted change. "I'm gonna kick my ass when it comes to the nullification of all the killings in the military. The crying and cursing in the media."
Those
```

> Top-$k$ y top-$p$ reducen este problema truncando la distribución antes de muestrear y renormalizando las probabilidades que se conservan.

#### 11. Top-k Sampling

##### 11.1. Truncation and Renormalization

> **Top-$k$ sampling** conserva los $k$ tokens de mayor probabilidad y descarta los demás. Sea $V_k\subseteq V$ ese conjunto para el contexto $(w_1,\ldots,w_t)$:
>
> $$
> P_{\mathrm{top}\text{-}k}(w\mid w_1,\ldots,w_t)=
> \begin{cases}
> \displaystyle\frac{P(w\mid w_1,\ldots,w_t)}
> {\sum_{u\in V_k}P(u\mid w_1,\ldots,w_t)},&w\in V_k,\\[2mm]
> 0,&w\notin V_k.
> \end{cases}
> $$
>
> La división redistribuye proporcionalmente la masa entre los tokens retenidos, de modo que sus probabilidades sumen $1$. Después muestreamos con esta distribución.
>
> Sus casos límite ayudan a interpretar $k$:
>
> - Con $k=1$, solo queda el token más probable y la selección coincide con greedy, salvo el tratamiento de empates.
> - Con $k=|V|$, no se elimina ningún token y obtenemos pure sampling.
> - Aumentar $k$ suele aumentar la diversidad y admitir candidatos menos probables.
> - Disminuir $k$ restringe la salida a continuaciones más predecibles, pero puede hacerla genérica.
>
> «Más seguro» en esta comparación se refiere a elegir tokens más probables, no a garantizar corrección factual.

##### 11.2. A Fixed Number of Tokens

> El número de candidatos retenidos no se adapta a la forma de la distribución. En una distribución **flat**, con muchas opciones razonables, un $k$ pequeño puede descartar demasiadas. En una distribución **sharp**, concentrada en pocas opciones, ese mismo $k$ puede admitir tokens poco adecuados.
>
> En el ejemplo, conservar seis tokens después de «The» retiene una masa de aproximadamente $0.68$ y excluye opciones plausibles como «people», «big», «house» y «cat». Después de «The car», conservar seis reúne aproximadamente $0.99$, aunque entre los candidatos aparezca «a», una continuación poco apropiada.
>
> Las barras azules representan los tokens conservados y las negras los descartados. El mismo número de tokens representa masas y conjuntos de opciones de calidad distinta.

![[apuntes-9edd1e106fe5-p0094-e064e80c4c8f.png]]

> Una comparación con $k=8$ refleja la misma limitación: en una distribución concentrada se admiten candidatos de la cola, mientras que en una más plana se pierden muchos candidatos razonables. Esto motiva definir el corte mediante masa de probabilidad.

##### 11.3. GPT-2 with Top-k Sampling

> GPT-2 utilizó este esquema para generar texto. El ejemplo fija `top_k=4`, mantiene sampling y permite cien tokens nuevos.

```python
set_seed(79)
sample_output = model.generate(
    **model_inputs,
    max_new_tokens=100,
    do_sample=True,
    top_k=4,
)

print("Output:\n" + 100 * "-")
print(tokenizer.decode(sample_output[0], skip_special_tokens=True))
```

> La salida tiene frases plausibles, aunque pasa del sueño personal a una noticia deportiva: limitar la cola no garantiza continuidad temática.

```text
I have a dream of making it to the top of the world, but I don't know where it's going. I don't know if I'm going to be able to do it."

The former Manchester United striker, who has been linked with a move to Chelsea, has made no secret of his ambition to become an international footballer, and is currently training with Chelsea.

He has also spoken to the club about his desire to become a full-time manager and has been in talks with the Football
```

#### 12. Top-p or Nucleus Sampling

##### 12.1. Selecting a Probability Mass

> **Top-$p$ sampling**, o **nucleus sampling**, conserva el menor conjunto de tokens más probables cuya masa acumulada alcanza un umbral $p$. En lugar de fijar cuántos tokens entran, fija cuánta probabilidad deben reunir.
>
> Dados $p\in(0,1]$ y los tokens ordenados por probabilidad decreciente:
>
> $$
> P(v_1\mid w_1,\ldots,w_t)\geq P(v_2\mid w_1,\ldots,w_t)
> \geq\cdots\geq P(v_{|V|}\mid w_1,\ldots,w_t),
> $$
>
> definimos:
>
> $$
> j^{*}=\min\left\{j:\sum_{i=1}^{j}P(v_i\mid w_1,\ldots,w_t)\geq p\right\},
> \qquad V_p=\{v_1,\ldots,v_{j^{*}}\}.
> $$
>
> El token que permite alcanzar o superar $p$ se incluye. La masa retenida puede superar el umbral porque no se conserva una fracción de un token.
>
> La nueva distribución es:
>
> $$
> P_{\mathrm{top}\text{-}p}(w\mid w_1,\ldots,w_t)=
> \begin{cases}
> \displaystyle\frac{P(w\mid w_1,\ldots,w_t)}
> {\sum_{u\in V_p}P(u\mid w_1,\ldots,w_t)},&w\in V_p,\\[2mm]
> 0,&w\notin V_p.
> \end{cases}
> $$
>
> El procedimiento consiste en ordenar, acumular hasta alcanzar $p$, renormalizar y muestrear. Se recalcula el núcleo en cada paso.
>
> Con $p=1$, conservamos toda la masa de la distribución y recuperamos pure sampling. Si el token más probable ya alcanza $p$, el núcleo contiene solo ese token.

##### 12.2. Adapting to the Distribution

> Con $p=0.92$, el ejemplo después de «The» necesita nueve tokens y retiene una masa de $0.94$. Después de «The car», bastan tres tokens para reunir $0.97$.
>
> Una distribución más plana permite más candidatos; una distribución más concentrada permite menos. Las barras azules muestran el núcleo elegido en cada caso.

![[apuntes-9edd1e106fe5-p0101-895e63a97fb5.png]]

> Top-$k$ fija el **número de tokens** y top-$p$ fija un **umbral de masa acumulada**. Ambos eliminan candidatos, renormalizan y muestrean; ninguno convierte la generación en una garantía de coherencia o veracidad.

##### 12.3. GPT-2 with Top-p Sampling

> `top_p=0.7` activa el umbral del ejemplo. `top_k=0` evita combinarlo con un corte adicional por número de tokens.

```python
set_seed(79)
sample_output = model.generate(
    **model_inputs,
    max_new_tokens=100,
    do_sample=True,
    top_p=0.7,
    top_k=0,
)

print("Output:\n" + 100 * "-")
print(tokenizer.decode(sample_output[0], skip_special_tokens=True))
```

> En este ejemplo, la continuación mantiene más continuidad alrededor de crear una empresa y desarrollar productos:

```text
I have a dream of someday starting a company that provides high quality products for $10,000 a year."

"I would love to be part of a product development team that creates the next generation of learning experiences for students ," she added. "It's been an honor to be able to work with an amazing team of entrepreneurs and give back to their community. My hope is that my work can inspire a whole new generation of business owners and entrepreneurs to grow and become more self-sufficient in the coming years."
```

### IV. Contrastive Search

#### 13. Preserving Coherence while Reducing Degeneration

##### 13.1. Model Confidence and Degeneration Penalty

> **Contrastive search** busca mantener la coherencia sin quedar atrapado en continuaciones repetitivas. Combina la probabilidad del siguiente token con una penalización por similitud con las representaciones del contexto.
>
> Dado el prefijo $\mathbf{x}_{<t}=(x_1,\ldots,x_{t-1})$, identificamos el conjunto $\mathcal{V}_k$ de los $k$ tokens de mayor probabilidad bajo $P_{\mathrm{LM}}(\,\cdot\mid\mathbf{x}_{<t})$. Elegimos:
>
> $$
> x_t=\arg\max_{v\in\mathcal{V}_k}
> \left\{
> \underbrace{(1-\alpha)P_{\mathrm{LM}}(v\mid\mathbf{x}_{<t})}_{\text{model confidence}}
> -
> \underbrace{\alpha\max_{1\leq j\leq t-1}s(h_v,h_j)}_{\text{degeneration penalty}}
> \right\}.
> $$
>
> La **model confidence** recompensa candidatos probables, manteniendo la coherencia con el contexto. La **degeneration penalty** reduce la puntuación de candidatos cuya representación es muy similar a alguna representación anterior.
>
> $h_v$ es la representación contextual del token candidato $v$ y $h_j$ la del token previo en posición $j$. El máximo compara el candidato con el token previo más similar; no calcula la similitud media con todo el prefijo.
>
> La fórmula utiliza la **probabilidad**, no la log-probabilidad de beam search. Además, $\mathcal{V}_k$ limita qué candidatos se evalúan: no muestreamos entre ellos, sino que elegimos el máximo de una puntuación modificada.

##### 13.2. Cosine Similarity

> La similitud se mide con **cosine similarity**:
>
> $$
> s(h_i,h_j)=\frac{h_i\cdot h_j}{\|h_i\|\,\|h_j\|}.
> $$
>
> Para un vector $z=(z_1,\ldots,z_d)$, la norma euclídea es:
>
> $$
> \|z\|=\sqrt{z_1^2+z_2^2+\cdots+z_d^2}.
> $$
>
> Para vectores no nulos, la similitud está entre $-1$ y $1$. Mide la coincidencia de dirección sin depender directamente de sus magnitudes. Una similitud elevada con alguna representación del contexto aumenta la penalización.
>
> El método no exige que el token candidato sea distinto en su forma escrita de todos los anteriores. La penalización se calcula sobre **representaciones contextuales**, por lo que no equivale a prohibir repetir una palabra o un n-gram.

##### 13.3. Obtaining Candidate Representations

> Para cada $v\in\mathcal{V}_k$:
>
> 1. Concatenamos $(x_1,\ldots,x_{t-1})$ con $v$.
> 2. Introducimos esa secuencia en el decoder.
> 3. Recuperamos las salidas del **último decoder block**: $h_1,\ldots,h_{t-1},h_v$.
>
> El diagrama muestra un contexto de cuatro tokens más un candidato. La representación de este se obtiene después de procesarlo con el contexto, no mediante el simple lookup de su input embedding.

![[apuntes-9edd1e106fe5-p0117-8db6d9296297.png]]

> Evaluar un candidato requiere calcular su representación contextual. Repetirlo para todos los tokens del vocabulario sería costoso; por eso se restringe a los top-$k$.
>
> Como la atención es causal, añadir $v$ no modifica la información permitida para los tokens anteriores. Sus representaciones no necesitan incorporar el nuevo token para que el procedimiento sea coherente.

##### 13.4. The Role of Alpha and the Complete Procedure

> El hiperparámetro $\alpha\in[0,1]$ controla el equilibrio entre los dos términos:
>
> - Con $\alpha=0$, solo importa la probabilidad. Como el token más probable pertenece a $\mathcal{V}_k$, el método se reduce a greedy.
> - Al aumentar $\alpha$, aumenta el peso de evitar representaciones similares al contexto y disminuye el de la probabilidad.
> - Con $\alpha=1$, la puntuación solo penaliza similitud, aunque la selección sigue restringida a los candidatos top-$k$.
>
> El procedimiento por paso es:
>
> 1. Procesamos el contexto actual $\mathbf{x}_{<t}$ con el decoder.
> 2. Proyectamos la representación de su última posición mediante la LM head para obtener logits sobre el vocabulario.
> 3. Aplicamos softmax y calculamos $P_{\mathrm{LM}}(\,\cdot\mid\mathbf{x}_{<t})$.
> 4. Seleccionamos $\mathcal{V}_k$.
> 5. Para cada candidato $v$, procesamos la concatenación del contexto y $v$ para obtener $h_v$ y las representaciones $h_j$.
> 6. Calculamos $\max_{1\leq j\leq t-1}s(h_v,h_j)$ para cada candidato.
> 7. Combinamos confianza y penalización, elegimos el argmax y añadimos el token seleccionado al contexto.
>
> La generación repite este procedimiento hasta EOS o el límite de longitud. Se presupone un contexto no vacío para obtener la distribución y comparar con representaciones anteriores.
>
> Contrastive search mantiene una única secuencia de salida, pero hace más trabajo por token que greedy debido a la evaluación de candidatos. Su objetivo es equilibrar coherencia y diversidad; no garantiza corrección factual.

### V. Choosing and Inspecting Decoding Strategies

#### 14. Task, Model and Decoding Strategy

##### 14.1. What Is Being Evaluated?

> La mejor estrategia depende de la **tarea** y del **modelo**. En unas tareas interesa producir una respuesta precisa y consistente; en otras, la variedad y naturalidad de una continuación abierta tienen mayor peso.
>
> La comparación utiliza distintos datasets y métricas. No debemos comparar directamente números de métricas diferentes.

| Task | Benchmarks | Evaluation focus |
| --- | --- | --- |
| **Math Problem Solving** | GSM8K | Exactitud de la respuesta. |
| **Code Generation** | MBPP, HumanEval | `Pass@1`: éxito del primer programa candidato. |
| **Commonsense Reasoning** | CommonsenseQA, StrategyQA | Exactitud en preguntas de razonamiento. |
| **Translation** | WMT22 | Calidad de traducción, con BLEU-4 en la comparación. |
| **Summarization** | CNN/DM, XSUM | Calidad del resumen, con ROUGE-L en la comparación. |
| **Open-ended Text Generation** | Book, Wikinews, Wikitext | Fluidez y coherencia de generación abierta; se compara MAUVE. |
| **Factual Knowledge** | FActScore | Corrección factual de las afirmaciones. |
| **Instruction Following** | AlpacaEval | Capacidad de seguir instrucciones; se compara win rate. |

> En las tablas, `BS` identifica beam search y `CS` contrastive search. También se comparan otros métodos deterministas, como `DBS`, `FSD`, `FSD-d`, `CD` y `DoLa`, y otros métodos estocásticos, como muestreo con temperatura, top-$p$, top-$k$, $\eta$, Mirostat y typical sampling. Sus mecanismos no se desarrollan aquí.

##### 14.2. Findings for Llama2-7B and Llama2-7B-Chat

> En la comparación de **Llama2-7B**, los métodos deterministas suelen obtener mejores resultados que los estocásticos en las tareas de respuesta precisa. La generación abierta constituye la excepción principal: greedy y beam search pueden obtener resultados especialmente pobres.
>
> Algunos resultados representativos muestran tanto esa diferencia como la mejora de métodos deterministas que reducen la degeneración:

| Llama2-7B benchmark | Greedy | Beam search | Contrastive search | Top-p | Top-k |
| --- | ---: | ---: | ---: | ---: | ---: |
| HumanEval, Pass@1 | 12.80 | 15.24 | 14.63 | 9.15 | 8.54 |
| GSM8K, accuracy | 13.87 | 17.21 | 14.63 | 12.96 | 9.10 |
| Wikinews, MAUVE | 40.10 | 41.33 | 96.66 | 95.19 | 96.47 |
| Book, MAUVE | 13.10 | 17.54 | 88.41 | 95.99 | 94.84 |

> En generación abierta, contrastive search y otros métodos deterministas que combaten la degeneración se acercan a los métodos estocásticos. Por tanto, no debemos reducir toda la familia determinista al comportamiento repetitivo de greedy.
>
> Con **Llama2-7B-Chat**, ajustado para seguir instrucciones, las diferencias entre estrategias son menos pronunciadas en varios casos. Por ejemplo, en HumanEval, greedy obtiene $12.80$, beam search $14.02$, contrastive search $13.41$, top-$p$ $13.41$ y top-$k$ $14.02$.
>
> En el conjunto de resultados, los enfoques deterministas pueden resultar útiles cuando se priorizan razonamiento matemático, generación de código, conocimiento factual o seguimiento de instrucciones. También pueden producir menos alucinaciones en algunas comparaciones. Estas observaciones describen modelos y tareas concretos, no una garantía universal para cualquier estrategia determinista.

##### 14.3. Model Scale

> La comparación de la familia Llama2 incluye modelos de $7$B, $13$B y $70$B, tanto base como Chat. Al aumentar la escala, las diferencias entre estrategias pueden reducirse.
>
> La tabla de escalado resume la dispersión de resultados con **relative deviation percentage (RDP)**. Una RDP menor indica menor variación de rendimiento entre los métodos comparados para esa tarea.
>
> Por ejemplo, en los modelos base, la RDP de MBPP baja de $25.81$ con $7$B a $15.23$ con $70$B, y la de GSM8K de $23.06$ a $11.92$. En las variantes Chat, pasa de $9.08$ a $3.74$ en MBPP y de $6.25$ a $2.28$ en GSM8K.
>
> La reducción no es idéntica en todas las tareas: en Wikinews, la RDP del modelo Chat de $7$B es $8.84$ y la del de $70$B es $6.04$. Un modelo más capaz puede depender menos de la estrategia, pero el tamaño por sí solo no elimina las alucinaciones ni hace irrelevante el decoding.

#### 15. Step-by-step Visualization

> **Transformer Explainer** permite inspeccionar la inferencia con GPT-2: cómo la entrada pasa por attention y la pila del decoder hasta obtener logits y probabilidades. Las visualizaciones de los componentes del Transformer ayudan a relacionar las operaciones matriciales con el flujo de información.
>
> **DecViz** permite explorar las estrategias de decoding:
>
> 1. Cargamos un language model y fijamos un prompt.
> 2. Avanzamos token a token.
> 3. Observamos cómo cambia la distribución del siguiente token.
> 4. Inspeccionamos los candidatos que considera cada estrategia, resaltados mediante colores.
>
> El ejemplo de greedy utiliza «I have a dream». El de beam search parte de «The house», con beam size $2$ y longitud máxima total $10$, contando prompt y respuesta. Los ejemplos top-$k$ y top-$p$ permiten comparar un corte por número de candidatos con un núcleo definido por masa acumulada.
>
> Estas herramientas permiten observar el comportamiento de las estrategias; sus visualizaciones no sustituyen la distinción entre probabilidad local del token y puntuación acumulada de la hipótesis.

### VI. Final Summary

> Un **decoder-only LM** utiliza self-attention causal y una **LM head** para convertir representaciones contextuales en probabilidades del siguiente token. La máscara evita acceso al futuro y permite entrenar todas las posiciones en una pasada con etiquetas desplazadas; durante inference generamos autoregresivamente.
>
> El entrenamiento minimiza la **cross-entropy** del token correcto. La estrategia de decoding decide cómo utilizar la distribución aprendida al construir una respuesta.

| Strategy | Selection rule | Main trade-off |
| --- | --- | --- |
| **Greedy** | Máximo de probabilidad en cada paso. | Rápido; sin garantía de óptimo global y propenso a repetición. |
| **Beam search** | Mantiene $k$ hipótesis y compara scores acumulados. | Explora más opciones; más costoso y todavía aproximado. |
| **Pure sampling** | Muestrea de toda la distribución. | Diversidad; puede seleccionar tokens de la unreliable tail. |
| **Top-k sampling** | Renormaliza y muestrea entre $k$ tokens. | Filtra la cola, pero el número de candidatos es fijo. |
| **Top-p sampling** | Renormaliza y muestrea del núcleo que alcanza $p$. | Adapta el número de candidatos a la distribución. |
| **Contrastive search** | Maximiza confianza menos penalización por similitud. | Reduce degeneración manteniendo coherencia, con más cálculo por token. |

> Para comparar hipótesis, la probabilidad de la secuencia es el producto de probabilidades condicionadas y su log-probabilidad es una suma. Las length penalties modifican este score para reducir la preferencia por respuestas cortas.
>
> **Mayor probabilidad no equivale necesariamente a mejor texto**. La elección depende de la tarea, del modelo y del equilibrio entre exactitud, coherencia, diversidad y coste.
