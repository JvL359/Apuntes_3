---
estado: pendiente de revisión
---

### I. Transformer Architecture

#### 1. Origin and main idea

> The **Transformer** was introduced in 2017 as an encoder-decoder architecture for sequence-to-sequence (*seq2seq*) tasks such as machine translation. Its central idea is to replace recurrence with **attention**, so input tokens can be processed in parallel rather than sequentially as in RNNs.

> In its original form, the encoder turns the source sentence into **contextualized embeddings**, and the decoder is a language model that generates the target sentence conditioned on those encodings. The decoder starts from `[BOS]` and predicts one token at a time.

> An encoder block combines self-attention and a feed-forward layer, each followed by **Add & Norm**. A decoder block contains self-attention, cross-attention over the encoded inputs and a feed-forward layer, also interleaved with Add & Norm. Cross-attention is the component through which the decoder conditions generation on the source sequence.

#### 2. Transformer model families

> Encoder and decoder stacks can also be used independently. This gives rise to three main families:

- **Encoder-decoder models**, such as T5, map an input sequence $x_1,\ldots,x_n$ to an output sequence $y_1,\ldots,y_m$. At time $t$, the decoder receives the tokens already generated $y_1,\ldots,y_t$ and the encoder outputs to predict $y_{t+1}$. Besides translation, this structure is used for tasks such as speech recognition.
- **Encoder-only models**, such as BERT, receive $x_1,\ldots,x_n$ and produce updated embeddings $\bar{x}_1,\ldots,\bar{x}_n$. Their objective is to learn a high-quality representation of sentence meaning; a classification head (`Linear + Softmax`) can map the encoder output to a class $c$.
- **Decoder-only models**, such as GPT, are language models. Given a token sequence or *prompt*, they generate text token by token. Their blocks have self-attention but no cross-attention, so they are a simplified variant of the original decoder. Many NLP tasks can be reformulated as generation tasks through an appropriate instruction prompt.

### II. The Encoder and Contextual Embeddings

#### 1. Encoder pipeline

> An encoder consists of a stack of $N$ encoder blocks. Before the first block, the input sentence follows this pipeline:

1. **Tokenization** converts the sentence into tokens, each with a token ID.
2. The IDs select rows from the input embedding matrix $E\in\mathbb{R}^{|\mathcal{V}|\times d_{\text{model}}}$, where $\mathcal{V}$ is the vocabulary.
3. **Positional encodings** are added to the input embeddings.
4. The resulting sequence passes through the $N$ encoder blocks.

> The initial embedding associated with a token is static: the token `rose`, for example, starts from the same vector in every sentence. The encoder transforms it into a **contextual embedding**, whose value depends on the other tokens in its particular sentence. Thus, `rose` can be represented as a flower in “he picked the rose” or as the action of standing up in “he finally rose”.

#### 2. Why context changes an embedding

> Static embeddings represent tokens as points in $\mathbb{R}^{d_{\text{model}}}$: semantically similar words tend to be close and dissimilar words farther apart. This is insufficient for polysemy, because one fixed point cannot adapt to the intended meaning of a word in every context.

> For a sentence with initial embeddings $x_1,\ldots,x_n$, the contextual representation of token $i$ is a function of its own embedding and those of the other tokens:

$$
\operatorname{ContextualizedEmbedding}(x_i)=f(x_i,x_1,\ldots,x_{i-1},x_{i+1},\ldots,x_n)
$$

> Attention produces a **change vector** $x'_i$ that indicates how to adjust $x_i$ using its context. The updated embedding is

$$
x_i^{\text{new}}=x_i+x'_i
$$

> The residual addition preserves the original information while allowing the vector to move toward a context-appropriate representation.

### III. Self-Attention

#### 1. Attention as weighted aggregation

> To contextualize a token, information from the surrounding tokens should not contribute equally. A naive aggregation would be

$$
x'_i=\sum_{j=1}^{L}\alpha_jx_j
$$

> where $\alpha_j$ indicates the relevance of token $j$. Attention implements this idea by learning both the relevance weights and the information that each token shares. For example, in “The match burned quickly”, `burned` is much more useful than `The` for resolving the meaning of `match`.

> The mechanism has four conceptual operations:

1. Token $i$ creates a **query** describing the contextual information it needs.
2. Each token $j$ supplies a **key** that determines how well it can answer that query.
3. Each token $j$ also supplies a **value**, the information it can contribute.
4. The values are combined with weights determined by query-key compatibility.

#### 2. Queries, keys and values

> For an input embedding $x_i\in\mathbb{R}^{d_{\text{model}}}$, the learnable projection matrices produce

$$
q_i=x_iW^Q\in\mathbb{R}^{d_q},\qquad
k_i=x_iW^K\in\mathbb{R}^{d_k},\qquad
v_i=x_iW^V\in\mathbb{R}^{d_v}
$$

> with $W^Q\in\mathbb{R}^{d_{\text{model}}\times d_q}$, $W^K\in\mathbb{R}^{d_{\text{model}}\times d_k}$ and $W^V\in\mathbb{R}^{d_{\text{model}}\times d_v}$. Queries can be read as “what information do I need?”, keys as “what kinds of queries can I answer?” and values as “what information can I provide?”.

#### 3. Scores, weights and attention output

> The scaled dot product between query $q_i$ and key $k_j$ measures how much token $i$ attends to token $j$:

$$
\operatorname{att\text{-}score}(q_i,k_j)=\frac{q_i\cdot k_j}{\sqrt{d_k}}\in\mathbb{R}
$$

> For each query, scores are normalized across all keys with a row-wise softmax. The resulting **attention weights** sum to one:

$$
\operatorname{att\text{-}weight}(q_i,k_j)=
\frac{\exp(\operatorname{att\text{-}score}(q_i,k_j))}
{\sum_\ell\exp(\operatorname{att\text{-}score}(q_i,k_\ell))}
$$

> The attention output is the corresponding weighted mixture of values:

$$
\operatorname{att\text{-}output}(x_i)=
\sum_j\operatorname{att\text{-}weight}(q_i,k_j)v_j\in\mathbb{R}^{d_v}
$$

> Finally, the output is projected back to the embedding dimension with $W^O\in\mathbb{R}^{d_v\times d_{\text{model}}}$:

$$
x'_i=\operatorname{att\text{-}output}(x_i)W^O\in\mathbb{R}^{d_{\text{model}}},
\qquad x_i^{\text{new}}=x_i+x'_i
$$

> Therefore, single-head attention first identifies relevant tokens through query-key compatibility, then aggregates their values, and lastly converts that aggregation into the change vector for the original embedding.

#### 4. Multi-head attention

> A single attention head captures one type of contextual dependency. **Multi-head attention** runs $h$ heads in parallel so different dependencies can be captured simultaneously. For head $\ell\in\{1,\ldots,h\}$,

$$
q_i^\ell=x_iW_\ell^Q,\qquad
k_j^\ell=x_jW_\ell^K,\qquad
v_j^\ell=x_jW_\ell^V
$$

$$
\operatorname{att\text{-}output}_\ell(x_i)=
\sum_{j=1}^{L}\operatorname{att\text{-}weight}(q_i^\ell,k_j^\ell)v_j^\ell
\in\mathbb{R}^{d_v}
$$

> The $h$ outputs are concatenated and projected to the original embedding size:

$$
x'_i=\operatorname{Concat}(\operatorname{att\text{-}output}_1(x_i),\ldots,
\operatorname{att\text{-}output}_h(x_i))W^O
\in\mathbb{R}^{1\times d_{\text{model}}}
$$

> Here $W^O\in\mathbb{R}^{hd_v\times d_{\text{model}}}$. The resulting $x'_i$ is again added to $x_i$ to produce $x_i^{\text{new}}$.

### IV. Attention in Matrix Form

#### 1. Parallel computation

> For a sequence of $L$ tokens, stack the embeddings as $X\in\mathbb{R}^{L\times d_{\text{model}}}$. For each head $\ell$, all queries, keys and values can then be computed in parallel:

$$
Q_\ell=XW_\ell^Q\in\mathbb{R}^{L\times d_q},\qquad
K_\ell=XW_\ell^K\in\mathbb{R}^{L\times d_k},\qquad
V_\ell=XW_\ell^V\in\mathbb{R}^{L\times d_v}
$$

> The matrix $Q_\ell K_\ell^\top\in\mathbb{R}^{L\times L}$ contains every query-key score. Applying softmax row by row yields the attention-weight matrix, and multiplying it by $V_\ell$ computes all weighted sums at once:

$$
\operatorname{Attention}(Q_\ell,K_\ell,V_\ell)=
\operatorname{softmax}\left(\frac{Q_\ell K_\ell^\top}{\sqrt{d_k}}\right)V_\ell
\in\mathbb{R}^{L\times d_v}
$$

> Concatenating the head outputs gives

$$
C=\operatorname{Concat}(\operatorname{Attention}(Q_1,K_1,V_1),\ldots,
\operatorname{Attention}(Q_h,K_h,V_h))\in\mathbb{R}^{L\times hd_v}
$$

> and the output projection produces the complete change-vector matrix:

$$
X'=CW^O\in\mathbb{R}^{L\times d_{\text{model}}}
$$

#### 2. Vectorized implementation

> A direct implementation with loops computes a dot product for every query-key pair and is slow. The following vectorized form performs the same operations as matrix multiplications for all tokens at once:

```python
import numpy as np
from scipy.special import softmax

def single_head_attention_vectorized(X, W_Q, W_K, W_V, W_O):
    # X: (T, d_model)
    d_k = W_K.shape[1]
    Q = X @ W_Q                    # (T, d_k)
    K = X @ W_K                    # (T, d_k)
    V = X @ W_V                    # (T, d_v)

    scores = (Q @ K.T) / np.sqrt(d_k)  # (T, T)
    weights = softmax(scores, axis=1)  # row-wise normalization
    att_out = weights @ V              # (T, d_v)

    return X + att_out @ W_O           # residual connection
```

> En el experimento con 1000 tokens, esta vectorización redujo el tiempo de ejecución respecto a los bucles explícitos en aproximadamente $200\times$. El resultado sigue teniendo forma $(T,d_{\text{model}})$: cada fila es el embedding contextualizado de un token.

### V. Encoder Block Components

#### 1. Residual connections

> Cada subcapa del encoder —self-attention y feed-forward network— se rodea de una **residual connection** y se sigue de layer normalization. La conexión residual suma el cambio calculado a la entrada:

$$
f_{\text{residual}}(X,X')=X+X'
$$

> Al volver a propagar la entrada, una red profunda conserva información importante y reduce el riesgo de que se distorsione u olvide al atravesar muchas capas.

#### 2. Layer normalization

> **Layer normalization** estabiliza el entrenamiento y se aplica de forma independiente a cada embedding. Para $x=[x_1,\ldots,x_d]$,

$$
\operatorname{LN}(x)=\gamma\frac{x-\mu}{\sqrt{\sigma^2+\epsilon}}+\beta
$$

> donde la media y la varianza se calculan sobre las $d$ componentes del propio vector:

$$
\mu=\frac{1}{d}\sum_{k=1}^{d}x_k,
\qquad
\sigma^2=\frac{1}{d}\sum_{k=1}^{d}(x_k-\mu)^2
$$

> $\gamma\in\mathbb{R}^{d}$ y $\beta\in\mathbb{R}^{d}$ son parámetros aprendibles, y $\epsilon$ evita una división por cero. Sin el reescalado y desplazamiento aprendibles, cada vector normalizado queda con media $0$ y varianza $1$.

#### 3. Position-wise feed-forward network

> Tras self-attention, cada embedding pasa de forma independiente por la misma **feed-forward network** (FFN). Esta capa introduce no linealidad y, por tanto, capacidad expresiva adicional:

$$
\operatorname{FF}(z_i)=\max(0,z_iW_1+b_1)W_2+b_2
$$

> La primera capa expande la dimensión de $d_{\text{model}}$ a $d_{\text{ff}}$ y la segunda la proyecta de vuelta:

| Term | Dimensions |
| --- | --- |
| Input $z_i$ | $(1\times d_{\text{model}})$ |
| $W_1$ and $b_1$ | $(d_{\text{model}}\times d_{\text{ff}})$ and $(1\times d_{\text{ff}})$ |
| Intermediate result | $(1\times d_{\text{ff}})$ |
| $W_2$ and $b_2$ | $(d_{\text{ff}}\times d_{\text{model}})$ and $(1\times d_{\text{model}})$ |
| Final output | $(1\times d_{\text{model}})$ |

> En el Transformer original, $d_{\text{model}}=512$ y $d_{\text{ff}}=2048$. La salida de la FFN vuelve a combinarse residualmente con su entrada y se normaliza; esta secuencia se repite en cada encoder block.

### VI. Positional Encodings

#### 1. Why position information is necessary

> La self-attention no incorpora por sí misma el orden de las palabras: reconoce qué tokens están presentes, pero no su secuencia. Por ello es **permutation-invariant**. Sin información posicional, `dog chases cat` y `cat chases dog` contienen los mismos tokens y producen las mismas combinaciones de query, key y value, aunque sus roles gramaticales sean distintos.

> Para añadir orden, se suma un vector posicional $p_i\in\mathbb{R}^{d_{\text{model}}}$ al embedding $e_i$ de cada token:

$$
e_i+p_i
$$

> Así, las proyecciones dependen también de la posición:

$$
q_i=(x_i+p_i)W^Q,\qquad k_j=(x_j+p_j)W^K
$$

> Entradas distintas producen pesos de atención distintos, de modo que el mecanismo puede diferenciar roles que dependen del orden.

#### 2. Learned and functional encodings

> Los **learned positional embeddings** almacenan una matriz $P\in\mathbb{R}^{n_{\max}\times d_{\text{model}}}$ con un vector aprendido por posición. Aprenden patrones útiles y suelen rendir bien, pero no generalizan a secuencias más largas que las vistas durante el entrenamiento sin un costoso reentrenamiento; además, un embedding de posición aislado puede no ser interpretable.

> Los **functional positional encodings** calculan cada posición de forma determinista mediante $f:\mathbb{N}\to\mathbb{R}^{d_{\text{model}}}$, con $f(i)=p_i$. No requieren fijar una longitud máxima y permiten extenderse sin reentrenar, aunque las secuencias mucho más largas que las observadas en entrenamiento no siempre mantienen el mismo rendimiento.

#### 3. Sinusoidal positional encodings

> El Transformer original emplea un esquema funcional sinusoidal. Para la entrada $i$ del vector correspondiente a la posición $\operatorname{pos}$,

$$
\operatorname{PE}(\operatorname{pos},i)=
\begin{cases}
\sin\left(\dfrac{\operatorname{pos}}{10000^{i/d_{\text{model}}}}\right), & \text{si } i \text{ es par}\\
\cos\left(\dfrac{\operatorname{pos}}{10000^{(i-1)/d_{\text{model}}}}\right), & \text{si } i \text{ es impar}
\end{cases}
$$

> Cada componente procede de una función periódica. Al aumentar el índice de la componente, la onda oscila más lentamente; mezclar frecuencias rápidas y lentas asigna a cada posición un patrón único. Las posiciones cercanas tienen mayor similitud por producto escalar que las lejanas, lo que permite a la atención aprovechar distancias relativas entre tokens.

#### 4. Complete encoder

> Si $X\in\mathbb{R}^{L\times d_{\text{model}}}$ es la matriz de embeddings de entrada y $P\in\mathbb{R}^{L\times d_{\text{model}}}$ la matriz de positional encodings, el encoder forma primero los embeddings sensibles a la posición:

$$
X_0=X+P
$$

> A continuación, los procesa con una pila de $N$ encoder blocks:

$$
X_n=\operatorname{EncoderBlock}(X_{n-1}),\qquad n=1,\ldots,N
$$

> La salida final es la matriz de embeddings contextualizados:

$$
O=X_N\in\mathbb{R}^{L\times d_{\text{model}}}
$$

### VII. Final Summary

> Transformer models use attention instead of recurrence, which enables parallel processing. Encoder-only, decoder-only and encoder-decoder variants adapt this principle to representation learning, generation and sequence-to-sequence tasks.

> The encoder turns static token embeddings into contextual embeddings. Multi-head self-attention selects and aggregates contextual information through queries, keys and values; residual connections preserve the input, layer normalization stabilizes the computation and the FFN adds nonlinearity. Positional encodings complete the representation by supplying the word-order information that self-attention lacks.
