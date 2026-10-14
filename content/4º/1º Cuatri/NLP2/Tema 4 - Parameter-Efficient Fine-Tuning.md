---
estado: pendiente de revisión
---

### I. Fine-Tuning and PEFT

#### 1. From Pre-Training to Specialization

> El **fine-tuning** adapta un modelo preentrenado a una tarea, un dominio o un comportamiento concreto mediante entrenamiento adicional. El preentrenamiento proporciona capacidades generales; la adaptación dirige esas capacidades hacia el uso deseado. La analogía es la de un médico con formación general que después se especializa en cardiología o dermatología.

> Hay dos motivos principales para adaptar un modelo. El primero es incorporar **conocimiento y patrones propios de un dominio**: por ejemplo, aprender el vocabulario y las descripciones características de textos dermatológicos. El segundo es modificar **cómo responde**: un modelo de lenguaje entrenado para continuar texto puede seguir una pregunta con otras preguntas, mientras que un modelo ajustado para seguir instrucciones aprende a producir la respuesta solicitada.

##### 1.1. Instruction Fine-Tuning

> En **instruction fine-tuning**, los ejemplos de entrenamiento emparejan una instrucción con la salida deseada. Una instrucción puede pedir resumir un texto, traducir una oración o contestar una pregunta. El entrenamiento sigue siendo supervisado: se compara la respuesta generada con la respuesta objetivo y se ajustan los parámetros que se hayan declarado entrenables.

| Instruction | Desired behavior |
| --- | --- |
| Summarize this text | Producir un resumen |
| Translate this sentence into Spanish | Producir la traducción |
| What is your first name? | Responder a la pregunta, en lugar de continuar una lista de preguntas |

> Combinar instrucciones de tareas diversas puede mejorar la capacidad para seguir instrucciones de **tareas no vistas durante ese ajuste**. Por ejemplo, se puede entrenar con traducción, razonamiento de sentido común, sentimiento y correferencia, y después evaluar inferencia textual sin proporcionar ejemplos de esa tarea en el prompt. Este es el planteamiento de instruction tuning con generalización **zero-shot**: las tareas de entrenamiento enseñan un comportamiento transferible.

> La forma del entrenamiento y la cantidad de parámetros actualizados son decisiones distintas. Se puede realizar instruction fine-tuning actualizando todo el modelo o usando una técnica PEFT. Del mismo modo, PEFT puede aplicarse a una tarea supervisada específica sin convertir necesariamente al modelo en un asistente general.

#### 2. The Cost of Full Fine-Tuning

##### 2.1. Training Memory

> En **full fine-tuning**, todos los parámetros del modelo se pueden actualizar. Tener memoria suficiente para cargar los pesos no garantiza poder entrenar: también hay que almacenar gradientes, estados del optimizador, activaciones del forward pass y otros resultados intermedios.

| Memory component | Purpose |
| --- | --- |
| Model weights | Representar el modelo actual |
| Gradients | Indicar cómo modificar los parámetros entrenables |
| Optimizer states | Mantener información utilizada por el optimizador para actualizar los pesos |
| Forward activations | Permitir calcular los gradientes durante backpropagation |
| Temporary buffers | Realizar las operaciones del entrenamiento |

> Como referencia de coste, los componentes adicionales del entrenamiento pueden ocupar del orden de **12–20 veces la memoria de los pesos**. Este factor es orientativo: cambia con la precisión numérica, el optimizador, el tamaño del batch, la longitud de las secuencias y las técnicas de ahorro de memoria. Para modelos cuyos pesos ya ocupan cientos de GB, el entrenamiento completo resulta especialmente costoso.

##### 2.2. Storage per Task

> El coste continúa después del entrenamiento. Si se mantiene una copia completa del modelo para question answering, otra para resumen y otra para generación, cada especialización añade una copia grande de los pesos. Así, el almacenamiento y la distribución de modelos crecen con el número de tareas.

> **PEFT —Parameter-Efficient Fine-Tuning—** busca adaptar el modelo entrenando una cantidad pequeña de parámetros. La base preentrenada se comparte entre tareas y se conserva, para cada una, solo la información necesaria para reproducir su adaptación.

![[apuntes-22ebe8f10cc8-p0019-7e0c71f5721f.png]]

> En el esquema, la base ocupa GB y las adaptaciones específicas ocupan MB. Para usar la especialización de QA se carga la misma base junto con los parámetros PEFT correspondientes. Esta separación permite intercambiar especializaciones sin almacenar una copia completa por tarea.

##### 2.3. What PEFT Saves

> Al reducir los parámetros entrenables, disminuyen especialmente la memoria de sus gradientes y de los estados del optimizador, así como el tamaño de los archivos de adaptación. Algunas configuraciones actualizan un 5 % o menos del modelo y pueden entrenarse en una sola GPU. Estas cifras dependen del modelo y del método: PEFT no elimina el coste de cargar la base ni toda la memoria de activaciones.

> **Congelar un peso** significa mantener su valor durante el entrenamiento. El modelo sigue utilizándolo en el forward pass y, cuando hace falta obtener gradientes de otros parámetros, el cálculo puede tener que atravesar operaciones que contienen pesos congelados. Por tanto, congelar la base no equivale a eliminarla del cálculo.

#### 3. Families of PEFT Methods

| Family | Main idea | Examples |
| --- | --- | --- |
| **Selective** | Elegir un subconjunto de parámetros existentes y congelar el resto | Capas superiores, pesos de atención, biases mediante BitFit |
| **Additive** | Introducir componentes pequeños y entrenar sus nuevos parámetros | Adapters, soft prompts |
| **Reparameterization** | Expresar la adaptación mediante una parametrización compacta | Actualizaciones de bajo rango mediante LoRA |

> Dentro de los métodos selectivos se puede seleccionar por **profundidad** —qué capas se ajustan—, por **tipo de parámetro** —por ejemplo, atención— o por **parámetros individuales** —por ejemplo, biases—. En los métodos aditivos se conserva la base y se introduce un mecanismo de adaptación.

> Las categorías pueden solaparse. LoRA añade factores entrenables y, al mismo tiempo, representa una actualización mediante una parametrización de bajo rango. IA³ añade vectores que modifican activaciones y pueden absorberse en los pesos para inferencia. La clasificación ayuda a entender el mecanismo, pero no impone fronteras excluyentes.

### II. Selective Fine-Tuning: BitFit

#### 4. Bias-Only Adaptation

> **BitFit** actualiza únicamente los **biases** del modelo y congela las matrices de pesos. Para una transformación afín $z=xW+b$, se mantiene $W$ y se entrena $b$. Se adapta así el modelo modificando desplazamientos de sus transformaciones, con muy pocos parámetros entrenables.

> El orden de magnitud puede ser de unas centésimas de porcentaje del modelo: se presenta como referencia aproximadamente un **0,05 %**, mientras que las configuraciones BERT y RoBERTa consideradas más adelante usan un **0,08–0,09 %**. El porcentaje depende de cuántos biases tenga la arquitectura y de qué parámetros incluya la selección.

> La selección se puede expresar mediante los nombres de los parámetros. En este esquema, `Optimizer` representa la clase de optimizador elegida por quien entrena el modelo. El filtrado supone que los nombres de los biases contienen `"bias"`.

```python
def configure_bitfit(model, Optimizer):
    for name, parameter in model.named_parameters():
        parameter.requires_grad_("bias" in name)

    params = (
        p for n, p in model.named_parameters()
        if "bias" in n
    )
    optimizer = Optimizer(params)
    return optimizer
```

> Hay dos decisiones coordinadas: declarar qué parámetros requieren gradiente y pasar esos parámetros al optimizador. Para guardar una adaptación BitFit se necesitan los biases ajustados de esa tarea junto con la base compartida.

#### 5. Biases inside a Transformer Block

> La existencia de un bias depende de la implementación. Las proyecciones de atención de la formulación original del Transformer se expresan sin biases, mientras que BERT incorpora biases en esas transformaciones. BitFit actúa sobre los parámetros que realmente existen en el modelo; no añade un bias a una proyección que carezca de él.

> Sea $X$ la matriz de representaciones de entrada, con un token por fila. Para la cabeza $i$ de atención:
>
> $$
> Q_i=XW_i^Q+b_i^Q,\qquad
> K_i=XW_i^K+b_i^K,\qquad
> V_i=XW_i^V+b_i^V.
> $$
>
> Los biases se suman a cada fila mediante broadcasting. La salida de esa cabeza es:
>
> $$
> A_i=\operatorname{softmax}\left(
> \frac{Q_iK_i^\top}{\sqrt{d_k}}
> \right)V_i.
> $$
>
> En esta notación, $A_i$ es la **salida de la cabeza**, no solo la matriz de probabilidades de atención. Con $h$ cabezas:
>
> $$
> H_{\mathrm{att}}=\operatorname{Concat}(A_1,\ldots,A_h)W^O+b^O,
> \qquad
> Y=\operatorname{LN}(X+H_{\mathrm{att}}).
> $$

> El bloque feed-forward contiene otras dos transformaciones afines:
>
> $$
> H_1=\operatorname{ReLU}(YW_{m1}+b_{m1}),
> \qquad
> H_2=H_1W_{m2}+b_{m2},
> $$
>
> $$
> \mathrm{out}=\operatorname{LN}(Y+H_2).
> $$
>
> BitFit permite entrenar los biases disponibles —incluidos los de otros módulos, como LayerNorm, cuando los selecciona el filtro— y mantiene congeladas las matrices. La expresión del bloque muestra por qué un conjunto pequeño de parámetros puede influir en distintas etapas del procesamiento.

#### 6. Performance and Limitations

##### 6.1. Comparison with Full Fine-Tuning

> En las siguientes configuraciones, BitFit consigue una media de GLUE próxima al ajuste completo pese a entrenar menos del 0,1 % de los parámetros:

| Model | Method | Trainable parameters | GLUE average |
| --- | --- | ---: | ---: |
| BERT-base | Full fine-tuning | 100 % | 82,3 |
| BERT-base | BitFit | 0,09 % | 82,4 |
| BERT-large | Full fine-tuning | 100 % | 84,1 |
| BERT-large | BitFit | 0,08 % | 84,2 |
| RoBERTa-base | Full fine-tuning | 100 % | 85,3 |
| RoBERTa-base | BitFit | 0,09 % | 84,6 |

> La media no implica que todos los problemas mejoren igual. En BERT-base, por ejemplo, RTE pasa de $70,5\pm0,6$ con ajuste completo a $72,3\pm0,9$ con BitFit, mientras que QQP pasa de $87,1\pm0,1$ a $84,0\pm0,2$. Hay que comprobar las tareas relevantes para el uso concreto.

##### 6.2. Which Biases Matter?

> Una ablación compara entrenar todos los biases con restringirse al bias de query, $b_q$, o al de la segunda transformación feed-forward, $b_{m2}$. También compara con entrenar una selección aleatoria de pesos del mismo tamaño.

| BERT-base adaptation | Trainable parameters | GLUE average |
| --- | ---: | ---: |
| Full fine-tuning | 100 % | 82,3 |
| All biases —BitFit— | 0,09 % | 82,4 |
| $b_{m2}$ and $b_q$ | 0,04 % | 81,1 |
| Only $b_{m2}$ | 0,03 % | 80,0 |
| Only $b_q$ | 0,01 % | 76,6 |
| Frozen model | 0 % | 62,1 |
| Random parameters, uniform selection | 0,09 % | 78,5 |
| Random rows or columns | 0,09 % | 79,5 |

> El resultado muestra que **qué se entrena importa**, además de cuántos parámetros se entrenan. Ajustar biases es más eficaz en esta comparación que seleccionar al azar la misma cantidad de parámetros. Reducir la selección a un único tipo de bias también limita la adaptación.

##### 6.3. Scaling to Larger Models

> BitFit no reproduce siempre el rendimiento del full fine-tuning. En GPT-3 de 175 mil millones de parámetros, los resultados de WikiSQL y SAMSum quedan por debajo del ajuste completo, aunque MNLI mejora. Por tanto, la conclusión es una limitación dependiente de la tarea, no una inferioridad universal de BitFit. La comparación completa se recoge junto con los resultados de LoRA.

> [!warning] Corrección
> En el material aparece «GPT-3, 375B», pero el tamaño correcto del modelo evaluado es **175B**, es decir, 175 mil millones de parámetros.
> Fuente de comprobación: [Artículo de LoRA](https://arxiv.org/html/2106.09685v2)

### III. Additive Fine-Tuning

#### 7. Adapters

##### 7.1. Bottleneck Architecture

> Un **adapter** es un módulo pequeño que se inserta en el modelo y cuyos parámetros se entrenan mientras la base permanece congelada. Una configuración habitual lo coloca después de atención y/o del bloque feed-forward.

![[apuntes-22ebe8f10cc8-p0029-88f2935e7a31.png]]

> El módulo realiza una proyección a una dimensión pequeña, aplica una no linealidad y vuelve a la dimensión original. Su conexión residual conserva una vía directa para la representación de entrada. De forma esquemática:
>
> $$
> \operatorname{Adapter}(z)
> =z+\operatorname{Up}\bigl(
> \sigma(\operatorname{Down}(z))
> \bigr).
> $$
>
> La dimensión del **bottleneck** es inferior a la de entrada, de modo que las proyecciones tienen pocos parámetros. Esto contrasta con el feed-forward habitual del Transformer, que suele expandir primero la dimensión antes de volver a reducirla.

> El siguiente pseudocódigo destaca la inserción del adapter. `SelfAttention`, `FFN`, `Adapter` y `LN` representan módulos ya definidos. Es un esquema compacto de colocación; el diagrama muestra con más detalle las conexiones residuales y las normalizaciones de las subcapas.

```python
def transformer_block_with_adapter(x):
    residual = x
    x = SelfAttention(x)
    x = FFN(x)
    x = Adapter(x)
    x = LN(x + residual)
    return x
```

##### 7.2. Parameter Efficiency and Task Performance

> Los adapters pueden conseguir un rendimiento próximo al ajuste completo entrenando menos de un **4 %** de los parámetros. La ubicación y el tamaño del módulo son decisiones de diseño: las variantes Pfeiffer y Houlsby no insertan exactamente los mismos componentes.

> Para BERT-base y una dimensión de bottleneck de 48, se obtiene la siguiente comparación. Cada columna conserva la métrica de su tarea; los números no deben interpretarse como una única accuracy común a todas ellas.

| Method | RTE | MRPC | STS-B | CoLA | SST-2 | QNLI | MNLI | QQP |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Full fine-tuning | 66,2 | 90,5 | 88,8 | 59,5 | 92,6 | 91,3 | 84,1 | 91,4 |
| Pfeiffer adapter | 70,8 | 89,7 | 89,0 | 58,9 | 92,2 | 91,3 | 84,1 | 90,5 |
| Houlsby adapter | 69,8 | 91,5 | 89,2 | 59,1 | 92,8 | 91,2 | 84,1 | 90,8 |

> Las diferencias son pequeñas en muchas tareas, pero no uniformes: una configuración puede mejorar RTE y perder algo en QQP. La eficiencia no depende de igualar exactamente todas las métricas del modelo ajustado por completo.

##### 7.3. Inference Latency

> Los adapters introducen operaciones adicionales y aumentan la profundidad efectiva del cálculo. Incluso con pocos parámetros nuevos pueden aumentar la latencia, porque el coste de ejecutar capas pequeñas no depende solo del número de pesos. El efecto es especialmente visible cuando el batch es pequeño y hay menos oportunidades de aprovechar el paralelismo de la GPU.

> En GPT-2 medium sobre una RTX 8000, las mediciones medias de 100 ejecuciones ilustran esta diferencia:

| Batch size / sequence length | Added parameters | Baseline latency | Adapter L | Adapter H |
| --- | ---: | ---: | ---: | ---: |
| 32 / 512 | 0,5 M | $1449,4\pm0,8$ ms | $1482,1\pm1,0$ ms —+2,2 %— | $1492,2\pm1,0$ ms —+3,0 %— |
| 16 / 256 | 11 M | $338,0\pm0,6$ ms | $354,8\pm0,5$ ms —+5,0 %— | $366,3\pm0,5$ ms —+8,4 %— |
| 1 / 128 | 11 M | $19,8\pm2,7$ ms | $23,9\pm2,1$ ms —+20,7 %— | $25,8\pm2,2$ ms —+30,3 %— |

> El número de parámetros entrenables, la memoria de entrenamiento y la latencia de inferencia son tres magnitudes distintas. Un método puede ahorrar mucho almacenamiento y, aun así, introducir un coste de inferencia apreciable.

#### 8. Prompt Tuning

##### 8.1. From Hard Prompts to Soft Prompts

> Un **hard prompt** es una secuencia de tokens de lenguaje: instrucciones, contexto o ejemplos que condicionan al modelo. El in-context learning aprovecha esta capacidad sin actualizar los pesos, tanto en zero-shot —sin ejemplos de la tarea en el prompt— como en few-shot —con unos pocos ejemplos—. Diseñar prompts eficaces puede ser difícil, porque la elección de palabras es discreta y el contexto disponible es limitado.

> **Prompt tuning** sustituye esa búsqueda de texto por el aprendizaje de un **soft prompt**: una secuencia de vectores continuos que se antepone a los embeddings de entrada. El modelo preentrenado queda congelado y solo se entrenan esos vectores.
>
> $$
> p=(x_1^s,\ldots,x_m^s),\qquad
> x=(x_1,\ldots,x_n).
> $$
>
> A_quí $m$ es la longitud del soft prompt, $n$ la de la entrada y cada $x_j^s$ tiene la misma dimensión $d_{\mathrm{model}}$ que un embedding del modelo. La secuencia que entra al Transformer contiene primero $p$ y después $x$.

![[apuntes-22ebe8f10cc8-p0040-4ccbc1fddb5d.png]]

> Los vectores verdes son parámetros entrenables. No tienen por qué corresponder a palabras interpretables ni a tokens concretos del vocabulario: el optimizador puede moverse directamente por el espacio continuo de embeddings.

##### 8.2. Training and Storage

> El procedimiento consiste en cargar y congelar el modelo, introducir $m$ embeddings entrenables, anteponerlos a cada entrada y calcular la pérdida de la tarea. Backpropagation actualiza el soft prompt manteniendo los pesos de la base.

> El número de parámetros del prompt es:
>
> $$
> N_{\mathrm{prompt}}=m\,d_{\mathrm{model}}.
> $$
>
> Longitudes de aproximadamente **5–100 tokens aprendidos** pueden ser suficientes en las configuraciones consideradas. Cada tarea conserva su propio prompt, que se carga junto con la misma base. El ahorro de almacenamiento es muy grande, aunque el prompt sigue ocupando posiciones y añade cálculo a la secuencia de entrada.

#### 9. The Effect of Model Scale and Prompt Length

##### 9.1. Larger Models Make Prompt Tuning More Competitive

![[apuntes-22ebe8f10cc8-p0043-04a5975b320b.png]]

> El eje horizontal representa el tamaño del modelo y el vertical el resultado en SuperGLUE. En la comparación con T5, prompt tuning —verde— queda por debajo del ajuste completo en modelos pequeños, pero se aproxima a él al crecer el modelo hasta el orden de $10^{10}$ parámetros.

> La gráfica distingue model tuning de una tarea, model tuning multitarea, prompt tuning y prompt design. La curva azul de hard prompts corresponde a modelos GPT-3, mientras que las curvas de ajuste emplean T5. Por ello, la figura ilustra tendencias de esos experimentos; no es una comparación controlada donde solo cambia la técnica y todo lo demás permanece idéntico.

##### 9.2. Prompt Length

![[apuntes-22ebe8f10cc8-p0045-c79039c82b04.png]]

> Las curvas comparan longitudes de **1, 5, 20, 100 y 150** embeddings entrenables. Los modelos pequeños suelen necesitar prompts más largos para obtener buenos resultados. A medida que crece el modelo, incluso un prompt muy corto puede resultar competitivo. Añadir longitud no garantiza una mejora monótona: 150 posiciones no supera siempre a 100.

> Para T5-XXL, con dimensión de embedding 4096, un prompt de cinco posiciones contiene:
>
> $$
> 5\cdot4096=20480
> $$
>
> parámetros, aproximadamente un **0,0002 %** del modelo. Esto muestra cuánto puede reducirse la adaptación almacenada por tarea. No significa que cinco posiciones alcancen exactamente el mejor valor de la gráfica: las longitudes superiores todavía pueden mejorar el resultado.

> [!warning] Corrección
> En el material aparece «T5-XL», asociado a cinco tokens, unos 20K parámetros y 0,0002 %, junto con una saturación en cinco tokens, pero la configuración correcta de esas cifras es **T5-XXL**: cinco tokens contienen 20480 parámetros, aproximadamente 0,00018 %. Cinco tokens ofrecen buen rendimiento, pero no implican saturación exacta; las ganancias al aumentar la longitud más allá de 20 son marginales en el análisis original.
> Fuente de comprobación: [Artículo de prompt tuning](https://arxiv.org/html/2104.08691v2)

### IV. Low-Rank Adaptation: LoRA

#### 10. A Linear Adaptation Example

##### 10.1. Full Fine-Tuning of a Small Matrix

> Consideremos una capa lineal con vectores fila:
>
> $$
> f_W(x)=xW,\qquad
> W_{\mathrm{initial}}=
> \begin{bmatrix}
> 1&1&1\\1&1&1\\1&1&1
> \end{bmatrix}.
> $$
>
> La matriz contiene nueve parámetros. Si $x=[x_1,x_2,x_3]$, la salida inicial es $[s,s,s]$, donde $s=x_1+x_2+x_3$.

> La tarea de adaptación quiere que la salida sea aproximadamente cero para las entradas de entrenamiento:

| Input $x$ | Target $y$ |
| --- | --- |
| $[1,2,-1]$ | $[0,0,0]$ |
| $[-2,1,3]$ | $[0,0,0]$ |
| $[0.5,-1,4]$ | $[0,0,0]$ |

> El conjunto supervisado se escribe $\{(x^{(i)},y^{(i)})\}_{i=1}^N$, y se usa una pérdida MSE entre las predicciones y sus objetivos.

> En el ajuste completo, cada paso de descenso por gradiente puede modificar los nueve valores:
>
> $$
> \delta W^{(t)}=-\eta\nabla_W\mathcal L(W^{(t)}),
> \qquad
> W^{(t+1)}=W^{(t)}+\delta W^{(t)}.
> $$
>
> $\eta$ es la tasa de aprendizaje y $\delta W^{(t)}$ el cambio de **un paso**. El cambio total tras adaptar el modelo es $\Delta W=W_{\mathrm{final}}-W_{\mathrm{initial}}$.

> Un resultado numérico del entrenamiento es:
>
> $$
> W_{\mathrm{final}}\approx
> \begin{bmatrix}
> -0.0001&-0.0001&-0.0001\\
> -0.0001&-0.0001&-0.0001\\
> 0.0027&0.0027&0.0027
> \end{bmatrix},
> $$
>
> $$
> \Delta W\approx
> \begin{bmatrix}
> -1.0001&-1.0001&-1.0001\\
> -1.0001&-1.0001&-1.0001\\
> -0.9973&-0.9973&-0.9973
> \end{bmatrix}.
> $$
>
> El cambio está próximo a una matriz cuyos elementos son todos $-1$. Esta aproximación permite ver que una actualización con nueve entradas puede tener una estructura muy simple.

##### 10.2. Factorizing the Update

> Para la aproximación $\Delta W\approx-\mathbf 1_{3\times3}$:
>
> $$
> A=
> \begin{bmatrix}-1\\-1\\-1\end{bmatrix},
> \qquad
> B=\begin{bmatrix}1&1&1\end{bmatrix},
> \qquad
> AB=
> \begin{bmatrix}
> -1&-1&-1\\-1&-1&-1\\-1&-1&-1
> \end{bmatrix}.
> $$
>
> Los factores contienen **seis parámetros** en vez de nueve. El producto tiene rango uno, porque todas sus columnas son iguales. Esta factorización corresponde a la aproximación idealizada del cambio, no a sustituir silenciosamente todos los valores del resultado numérico por $-1$.

> El **rango** de una matriz $M\in\mathbb R^{m\times n}$ se puede definir como la menor dimensión interna que permite factorizarla:
>
> $$
> \operatorname{rank}(M)=
> \min\left\{r:M=AB,\;
> A\in\mathbb R^{m\times r},\;
> B\in\mathbb R^{r\times n}\right\}.
> $$
>
> Para unos factores de dimensión interna $r$, el producto satisface $\operatorname{rank}(AB)\leq r$: no tiene que alcanzar exactamente ese rango. Una matriz es de **bajo rango** cuando su rango es mucho menor que $\min(m,n)$.

> La reducción es útil cuando la dimensión interna es pequeña respecto de las dimensiones originales. Un modelo grande puede necesitar una adaptación de menor complejidad que sus matrices preentrenadas; esa es la hipótesis que explota LoRA.

#### 11. Low-Rank Parameterization

> **LoRA —Low-Rank Adaptation—** conserva una matriz preentrenada $W$ y aprende el cambio mediante dos factores:
>
> $$
> W_{\mathrm{fine\text{-}tuned}}=W+\Delta W,
> \qquad
> \Delta W=AB,
> $$
>
> $$
> W\in\mathbb R^{d_{\mathrm{in}}\times d_{\mathrm{out}}},
> \quad
> A\in\mathbb R^{d_{\mathrm{in}}\times r},
> \quad
> B\in\mathbb R^{r\times d_{\mathrm{out}}},
> \quad
> r\ll\min(d_{\mathrm{in}},d_{\mathrm{out}}).
> $$
>
> Se conserva la convención de vectores fila: el forward se escribe $xW+(xA)B$. Con esta orientación, el producto de actualización es **$AB$**.

> La separación en dos ramas procede directamente de la distributividad y la asociatividad:
>
> $$
> y=x(W+AB)=xW+xAB=xW+(xA)B.
> $$
>
> Durante el entrenamiento no es necesario formar una matriz de actualización completa para cada entrada: se aplica primero el factor $A$ y después el factor $B$.

| Adaptation | Trainable parameters per matrix |
| --- | ---: |
| Full fine-tuning | $d_{\mathrm{in}}d_{\mathrm{out}}$ |
| LoRA | $r(d_{\mathrm{in}}+d_{\mathrm{out}})$ |

> Para $d_{\mathrm{in}}=1000$, $d_{\mathrm{out}}=5000$ y $r=10$, el ajuste completo entrena $5\,000\,000$ parámetros. LoRA entrena $10(1000+5000)=60\,000$, un **1,2 %** de esa matriz. El porcentaje se calcula respecto de la matriz elegida, no necesariamente respecto de todos los parámetros del modelo.

> LoRA restringe el cambio a matrices de rango como máximo $r$. No afirma que cualquier actualización completa pueda representarse con un rango pequeño. El rango es una decisión que equilibra capacidad de adaptación y coste.

#### 12. Training and Merging

##### 12.1. Step-by-Step Procedure

> **1. Elegir las matrices que se adaptarán.** En un Transformer pueden ser proyecciones de atención; el mecanismo también se puede aplicar a otras transformaciones lineales.
>
> **2. Cargar y congelar los pesos preentrenados.** La matriz $W$ se utiliza en el cálculo pero no se actualiza.
>
> **3. Añadir $A$ y $B$ con rango $r$.** Estas matrices son los parámetros nuevos de la adaptación.
>
> **4. Inicializar la rama LoRA sin modificar la función inicial.** Se puede inicializar $A$ con valores aleatorios pequeños y $B=0$, de modo que $AB=0$.
>
> **5. Preparar los ejemplos y sus objetivos.** Se mantiene la pérdida correspondiente a la tarea.
>
> **6. Ejecutar el forward:** $y=xW+(xA)B$. La rama congelada aporta la transformación original y la rama LoRA añade el cambio.
>
> **7. Calcular la pérdida** $\mathcal L(y,y_{\mathrm{target}})$.
>
> **8. Propagar los gradientes y actualizar solo $A$ y $B$.** Repetir los pasos de entrenamiento conforme al criterio previsto.
>
> **9. Guardar los factores o fusionarlos con la base** para realizar inferencia.

![[apuntes-22ebe8f10cc8-p0067-cf5665a18edd.png]]

> Inicializar una sola de las matrices a cero conserva la función preentrenada sin bloquear toda la adaptación. En el primer paso, con $B=0$, el gradiente de $A$ puede ser cero, mientras que $B$ puede recibir gradiente a través del factor aleatorio $A$. Por tanto, no se exige que ambos gradientes sean distintos de cero en todos los pasos.

> [!warning] Corrección
> En el material aparece $\partial\mathcal L/\partial W=0$ como consecuencia de congelar $W$, pero la expresión correcta para la actualización es **$\delta W=0$** porque ese parámetro no se entrena. La derivada matemática respecto de $W$ no tiene por qué ser cero; con `requires_grad=False` no se acumula su gradiente para actualizarlo.
> Fuente de comprobación: [Documentación de autograd de PyTorch](https://docs.pytorch.org/docs/2.9/notes/autograd.html#setting-requires-grad)

##### 12.2. Scaling the LoRA Branch

> Una variante incorpora el factor $\alpha/r$:
>
> $$
> y=xW+\frac{\alpha}{r}(xA)B,
> \qquad
> \Delta W=\frac{\alpha}{r}AB.
> $$
>
> $\alpha$ controla la escala de la actualización y $r$ es el rango elegido. Las expresiones anteriores sin factor explícito representan la versión simplificada con escala uno.

##### 12.3. Merging for Inference

> Después del entrenamiento se puede calcular una sola vez:
>
> $$
> W_{\mathrm{merged}}=W+AB
> $$
>
> o, si se usa escalado:
>
> $$
> W_{\mathrm{merged}}=W+\frac{\alpha}{r}AB.
> $$
>
> Entonces $y=xW_{\mathrm{merged}}$. La capa fusionada tiene la misma forma y las mismas operaciones que la capa original: no necesita ejecutar una rama adicional durante cada inferencia.

> El ahorro de almacenamiento por tarea se mantiene si se guardan $A$ y $B$ y se comparte la base. Guardar una copia completa de $W_{\mathrm{merged}}$ por tarea vuelve a introducir el coste de almacenamiento de esas copias. También es posible conservar las ramas separadas para intercambiar adaptaciones, pero en ese caso sí se ejecutan las operaciones adicionales.

#### 13. LoRA in Self-Attention

> El esquema siguiente incorpora LoRA en las proyecciones **query, key y value**. Las matrices preentrenadas `W_q`, `W_k` y `W_v` se proporcionan al constructor; cada una tiene forma $(d_{\mathrm{model}},d_{\mathrm{model}})$. Los factores se inicializan en el dispositivo y con el tipo de sus pesos correspondientes.

> El ejemplo representa **una cabeza de atención sin máscara**, para una entrada con última dimensión $d_{\mathrm{model}}$. La parte específica de LoRA es la formación de $Q$, $K$ y $V$; a continuación se aplica la atención estándar. No es una implementación completa de multi-head attention, que requeriría separar cabezas y añadir su proyección de salida.

```python
import torch
from torch import nn
from math import sqrt


class LoRASelfAttention(nn.Module):
    def __init__(self, d_model, rank, W_q, W_k, W_v):
        super().__init__()
        self.W_q = nn.Parameter(W_q, requires_grad=False)
        self.W_k = nn.Parameter(W_k, requires_grad=False)
        self.W_v = nn.Parameter(W_v, requires_grad=False)

        self.A_q = nn.Parameter(
            0.01 * torch.randn(
                d_model, rank, device=W_q.device, dtype=W_q.dtype
            )
        )
        self.B_q = nn.Parameter(
            torch.zeros(rank, d_model, device=W_q.device, dtype=W_q.dtype)
        )
        self.A_k = nn.Parameter(
            0.01 * torch.randn(
                d_model, rank, device=W_k.device, dtype=W_k.dtype
            )
        )
        self.B_k = nn.Parameter(
            torch.zeros(rank, d_model, device=W_k.device, dtype=W_k.dtype)
        )
        self.A_v = nn.Parameter(
            0.01 * torch.randn(
                d_model, rank, device=W_v.device, dtype=W_v.dtype
            )
        )
        self.B_v = nn.Parameter(
            torch.zeros(rank, d_model, device=W_v.device, dtype=W_v.dtype)
        )

    def forward(self, x):
        Q = x @ self.W_q + (x @ self.A_q) @ self.B_q
        K = x @ self.W_k + (x @ self.A_k) @ self.B_k
        V = x @ self.W_v + (x @ self.A_v) @ self.B_v

        scores = Q @ K.transpose(-2, -1)
        attention = torch.softmax(scores / sqrt(Q.shape[-1]), dim=-1)
        return attention @ V
```

> El código usa escala LoRA uno. Si se desea la variante escalada, cada término `(x @ A) @ B` se multiplica por $\alpha/r$. Los parámetros preentrenados no requieren gradiente y los seis factores nuevos sí; el optimizador debe actualizar únicamente los parámetros entrenables.

#### 14. Experimental Results

##### 14.1. GPT-3

> En esta comparación, **M** significa millones y **B** miles de millones de parámetros. WikiSQL mide la accuracy de la forma lógica y MNLI-m la accuracy en el conjunto matched; SAMSum usa ROUGE-1, ROUGE-2 y ROUGE-L. Prefix embedding y prefix layer son otras estrategias de adaptación por prefijos incluidas como referencias experimentales.

| Method | Trainable parameters | WikiSQL | MNLI | SAMSum R-1 / R-2 / R-L |
| --- | ---: | ---: | ---: | --- |
| Full fine-tuning | 175255,8 M | 73,8 | 89,5 | 52,0 / 28,0 / 44,5 |
| BitFit | 14,2 M | 71,3 | 91,0 | 51,3 / 27,4 / 43,5 |
| Prefix embedding | 3,2 M | 63,1 | 88,6 | 48,3 / 24,2 / 40,5 |
| Prefix layer | 20,2 M | 70,1 | 89,5 | 50,8 / 27,3 / 43,5 |
| Adapter H | 7,1 M | 71,9 | 89,8 | 53,0 / 28,9 / 44,8 |
| Adapter H | 40,1 M | 73,2 | 91,5 | 53,2 / 29,0 / 45,1 |
| LoRA | 4,7 M | 73,4 | 91,7 | 53,8 / 29,8 / 45,9 |
| LoRA | 37,7 M | 74,0 | 91,6 | 53,4 / 29,2 / 45,1 |

> LoRA puede alcanzar o superar los resultados del ajuste completo en varios de estos problemas con muchos menos parámetros entrenables. El presupuesto mayor no mejora todas las métricas: 37,7 M supera a 4,7 M en WikiSQL, pero no en MNLI ni SAMSum. Las variaciones típicas indicadas son de aproximadamente $\pm0,5$ en WikiSQL, $\pm0,1$ en MNLI y $\pm0,2/\pm0,2/\pm0,1$ en las tres métricas de SAMSum; diferencias pequeñas requieren prudencia al comparar.

> Rangos del orden de **1–8** pueden resultar eficaces en los experimentos de GPT-3, pero no garantizan el mismo resultado para cualquier modelo o tarea. También importa **qué proyecciones** se adaptan: el presupuesto total depende del rango, las dimensiones y el número de matrices seleccionadas.

> [!warning] Corrección
> En el material aparece una etiqueta «r = 4» para esta tabla y «only 2 %» junto al resultado de LoRA, pero las cifras correctas son aproximadamente **0,0027 %** para 4,7 M y **0,0215 %** para 37,7 M respecto de 175255,8 M. Tampoco hay un único rango cuatro: el presupuesto de 4,7 M emplea configuraciones de rango 1 o 2, y el de 37,7 M configuraciones de rango 8 o 2, según las proyecciones y la tarea.
> Fuente de comprobación: [Resultados y configuración experimental de LoRA](https://arxiv.org/html/2106.09685v2)

##### 14.2. Encoder Models and GLUE

> La misma idea de adaptación se aplica a modelos encoder. Las medias de GLUE resumen los resultados por tarea y permiten observar la relación entre rendimiento y parámetros entrenables:

| Model | Method | Trainable parameters | GLUE average |
| --- | --- | ---: | ---: |
| RoBERTa-base | Full fine-tuning | 125 M | 86,4 |
| RoBERTa-base | BitFit | 0,1 M | 85,2 |
| RoBERTa-base | Adapter D | 0,3 M | 84,4 |
| RoBERTa-base | Adapter D | 0,9 M | 85,4 |
| RoBERTa-base | LoRA | 0,3 M | 87,2 |
| RoBERTa-large | Full fine-tuning | 355 M | 88,9 |
| RoBERTa-large | LoRA | 0,8 M | 89,0 |
| DeBERTa-XXL | Full fine-tuning | 1500 M | 91,1 |
| DeBERTa-XXL | LoRA | 4,7 M | 91,3 |

> En RoBERTa-large, las ejecuciones marcadas con $\dagger$ corresponden a una comparación de adapters y LoRA bajo condiciones emparejadas:

| Method —matched setup— | Trainable parameters | GLUE average |
| --- | ---: | ---: |
| Adapter D | 3,0 M | 88,4 |
| Adapter D | 0,8 M | 87,9 |
| Adapter H | 6,0 M | 87,8 |
| Adapter H | 0,8 M | 86,4 |
| LoRA | 0,8 M | 88,6 |

> Estos resultados apoyan la posibilidad de una adaptación eficaz con pocas variables, pero las diferencias entre arquitecturas, tareas y configuraciones impiden convertir la tabla en una clasificación universal de métodos. Para una comparación directa conviene usar las ejecuciones con condiciones emparejadas.

### V. Activation Rescaling: IA³

#### 15. Inhibiting and Amplifying Inner Activations

##### 15.1. Three Trainable Vectors

> **IA³ —Infused Adapter by Inhibiting and Amplifying Inner Activations—** adapta el modelo mediante vectores que reescalan activaciones internas. En lugar de añadir una transformación densa nueva, aprende cuánto inhibir o amplificar cada componente de ciertas representaciones.

> Cada bloque adaptado incorpora tres vectores:
>
> $$
> l_k\in\mathbb R^{d_k},\qquad
> l_v\in\mathbb R^{d_v},\qquad
> l_{\mathrm{ff}}\in\mathbb R^{d_{\mathrm{ff}}}.
> $$
>
> $l_k$ actúa sobre keys, $l_v$ sobre values y $l_{\mathrm{ff}}$ sobre las activaciones intermedias del feed-forward. Son tres vectores **por bloque adaptado**, no tres vectores para todo el modelo. Para ese bloque se añaden $d_k+d_v+d_{\mathrm{ff}}$ parámetros.

> La operación $\odot$ es el producto elemento a elemento. Si $X$ tiene un token por fila, el vector se aplica por broadcasting a cada token:
>
> $$
> (l\odot X)_{t,j}=l_jX_{t,j}.
> $$
>
> Se reescala la dimensión de características, no la dimensión de tokens. Un componente puede reducir o aumentar la contribución de una característica; los factores aprendidos no están obligados a ser probabilidades.

##### 15.2. Initialization

> Los tres vectores se inicializan con **unos**. Como $\mathbf1\odot X=X$, el modelo adaptado produce inicialmente la misma función que la base. Durante el entrenamiento, solo se actualizan los vectores IA³ y se congelan los pesos preentrenados.

> La elección de identidad depende del mecanismo: IA³ empieza con unos porque multiplica activaciones; LoRA empieza con un producto cero porque suma una actualización.

##### 15.3. Rescaling Attention

> Con $Q=XW^Q$, $K=XW^K$ y $V=XW^V$, IA³ modifica la atención así:
>
> $$
> \operatorname{Attention}_{\mathrm{IA^3}}(Q,K,V)=
> \operatorname{softmax}\left(
> \frac{Q(l_k\odot K)^\top}{\sqrt{d_k}}
> \right)
> (l_v\odot V).
> $$
>
> Reescalar keys modifica los scores y, por tanto, la distribución de atención. Reescalar values modifica las representaciones que se combinan con esas probabilidades. Las queries permanecen sin este reescalado.

##### 15.4. Rescaling the Feed-Forward Layer

> Para un feed-forward expresado con ReLU:
>
> $$
> H_1=\operatorname{ReLU}(XW_1+b_1),
> \qquad
> \widetilde H_1=l_{\mathrm{ff}}\odot H_1,
> $$
>
> $$
> H_2=\widetilde H_1W_2+b_2,
> \qquad
> \mathrm{out}=\operatorname{LN}(X+H_2).
> $$
>
> IA³ reescala la activación **después de la no linealidad y antes de la segunda proyección**. El mismo mecanismo se puede ilustrar con GELU en lugar de ReLU; esa elección cambia la activación base, no el lugar donde se inserta el vector.

![[apuntes-22ebe8f10cc8-p0086-5f97d4f29e59.png]]

> En atención, los dos puntos de multiplicación corresponden a keys y values. En el feed-forward, el tercer punto de multiplicación aparece entre la no linealidad y la proyección de salida.

#### 16. IA³ Training Code

> El siguiente pseudocódigo usa PyTorch para representar un bloque con una cabeza de atención, sin máscara ni biases en las proyecciones. Los pesos `W_q`, `W_k`, `W_v`, `W_1` y `W_2` y los módulos de normalización `LN` están previamente definidos y congelados. Los vectores `l_k`, `l_v` y `l_ff` son parámetros entrenables inicializados con unos en el mismo dispositivo y tipo que los pesos.

> La entrada `x` es una matriz de forma $(T,d_{\mathrm{model}})$, por lo que `k.T` transpone tokens y características. En este esquema se supone $d_v=d_{\mathrm{model}}$ para poder sumar la salida de atención a su residual sin una proyección adicional. `d_k` es la dimensión de keys y `gelu` representa la no linealidad del feed-forward.

```python
import torch
from math import sqrt
from torch import nn
from torch.nn.functional import gelu

# W_q, W_k, W_v, W_1, W_2 y los módulos LN:
# pesos y módulos preentrenados, ya congelados.
d_k = W_k.shape[-1]
d_v = W_v.shape[-1]
d_ff = W_1.shape[-1]

l_k = nn.Parameter(
    torch.ones(d_k, device=W_k.device, dtype=W_k.dtype)
)
l_v = nn.Parameter(
    torch.ones(d_v, device=W_v.device, dtype=W_v.dtype)
)
l_ff = nn.Parameter(
    torch.ones(d_ff, device=W_1.device, dtype=W_1.dtype)
)


def softmax(scores):
    return torch.softmax(scores, dim=-1)


def ia3_self_attention(x):
    k = l_k * (x @ W_k)
    q = x @ W_q
    v = l_v * (x @ W_v)
    return softmax(q @ k.T / sqrt(d_k)) @ v


def transformer_block_with_ia3(x):
    residual = x
    x = ia3_self_attention(x)
    x = LN(x + residual)

    residual = x
    x = x @ W_1
    x = gelu(x)
    x = l_ff * x
    x = x @ W_2
    x = LN(x + residual)
    return x
```

> El optimizador de este bloque recibe únicamente `l_k`, `l_v` y `l_ff`. En un modelo con varios bloques se incluyen los vectores correspondientes a todos los bloques adaptados. El código muestra el reescalado; la estructura completa conserva los módulos, las máscaras y las proyecciones propios del Transformer utilizado.

#### 17. Merging IA³ into the Base Weights

##### 17.1. Diagonal Matrices

> Un producto elemento a elemento por un vector puede escribirse como un producto matricial usando una matriz diagonal. Para un vector fila $l=[l_1,l_2,l_3]$:
>
> $$
> D_l=\operatorname{diag}(l)=
> \begin{bmatrix}
> l_1&0&0\\
> 0&l_2&0\\
> 0&0&l_3
> \end{bmatrix}.
> $$
>
> Si $X$ contiene tokens por filas, $l\odot X=XD_l$. La multiplicación por la derecha reescala **columnas**: $(WD_l)_{ij}=W_{ij}l_j$. La multiplicación por la izquierda reescala **filas**: $(D_lW)_{ij}=l_iW_{ij}$.

##### 17.2. Keys and Values

> Para keys, la transformación completa se puede reagrupar:
>
> $$
> l_k\odot(XW^K)
> =(XW^K)\operatorname{diag}(l_k)
> =X\underbrace{\left(W^K\operatorname{diag}(l_k)\right)}_{W^K_{\mathrm{eff}}}.
> $$
>
> Por tanto:
>
> $$
> W^K_{\mathrm{eff}}=W^K\operatorname{diag}(l_k),
> \qquad
> W^V_{\mathrm{eff}}=W^V\operatorname{diag}(l_v).
> $$
>
> Los vectores reescalan las columnas de las matrices de proyección. Si la proyección incluye un bias, también debe reescalarse: $b^K_{\mathrm{eff}}=b^K\operatorname{diag}(l_k)$ y análogamente para values. El esquema sin biases solo necesita transformar las matrices.

##### 17.3. Feed-Forward Output Projection

> Como el vector se aplica **antes** de $W_2$, se fusiona en su lado izquierdo:
>
> $$
> (l_{\mathrm{ff}}\odot H_1)W_2
> =H_1\operatorname{diag}(l_{\mathrm{ff}})W_2
> =H_1W_{2,\mathrm{eff}},
> $$
>
> $$
> W_{2,\mathrm{eff}}
> =\operatorname{diag}(l_{\mathrm{ff}})W_2.
> $$
>
> A_quí se reescalan las filas de $W_2$. El bias de salida $b_2$, si existe, se suma después y permanece sin cambios. La no linealidad tampoco se altera: el reescalado se absorbe en la segunda matriz, situada después de ella.

| IA³ vector | Original operation | Merged weight | Scaling direction |
| --- | --- | --- | --- |
| $l_k$ | $l_k\odot(XW^K)$ | $W^K\operatorname{diag}(l_k)$ | Columnas de $W^K$ |
| $l_v$ | $l_v\odot(XW^V)$ | $W^V\operatorname{diag}(l_v)$ | Columnas de $W^V$ |
| $l_{\mathrm{ff}}$ | $(l_{\mathrm{ff}}\odot H_1)W_2$ | $\operatorname{diag}(l_{\mathrm{ff}})W_2$ | Filas de $W_2$ |

##### 17.4. Inference Code

> Terminada la adaptación, se calculan los pesos efectivos una vez y se utiliza el bloque estándar. Este código conserva las hipótesis de dimensiones y ausencia de biases del ejemplo anterior. `torch.no_grad()` evita construir un grafo para la preparación de los pesos de inferencia.

```python
with torch.no_grad():
    W_k_eff = W_k @ torch.diag(l_k)
    W_v_eff = W_v @ torch.diag(l_v)
    W_2_eff = torch.diag(l_ff) @ W_2


def self_attention_inference(x):
    k = x @ W_k_eff
    q = x @ W_q
    v = x @ W_v_eff
    return softmax(q @ k.T / sqrt(d_k)) @ v


def transformer_block_inference(x):
    residual = x
    x = self_attention_inference(x)
    x = LN(x + residual)

    residual = x
    x = x @ W_1
    x = gelu(x)
    x = x @ W_2_eff
    x = LN(x + residual)
    return x
```

> [!warning] Corrección
> En el material aparecen los fragmentos de bloque con adapter y de bloque de inferencia IA³ sin devolver su salida, pero la instrucción correcta al final de ambos es **`return x`**. Sin ella, una función Python que termina devuelve `None`, no la representación calculada.
> Fuente de comprobación: [Definición de funciones y return en Python](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)

> Una vez fusionados los vectores, el bloque ejecuta las mismas operaciones que la base, sin multiplicaciones IA³ adicionales por entrada. Como en LoRA, hay que distinguir almacenar una adaptación compacta de almacenar una copia completa de los pesos fusionados.

#### 18. Performance per Trainable Parameter

> En la comparación realizada sobre **T0 de 3B**, un Transformer encoder-decoder, IA³ ajusta aproximadamente un **0,02 %** de los parámetros. La gráfica sitúa cada método según el porcentaje actualizado y la accuracy obtenida:

![[apuntes-22ebe8f10cc8-p0090-12c4921edd53.png]]

> IA³ —estrella amarilla— alcanza una accuracy próxima a 65, frente a aproximadamente 63 de la referencia que actualiza todos los parámetros. La configuración de LoRA comparada usa del orden de **16 veces más parámetros entrenables** y obtiene un resultado algo inferior. La ventaja es específica de este experimento; no demuestra que IA³ supere siempre a LoRA o al full fine-tuning.

> El eje horizontal es logarítmico. Una posición más a la izquierda significa menor fracción entrenable y una posición más alta significa mayor resultado. La figura muestra que aumentar los parámetros actualizados no garantiza mejorar la accuracy y que el mecanismo de adaptación también determina qué puede aprenderse con un presupuesto pequeño.

### VI. Final Summary

> **PEFT adapta modelos preentrenados con pocos parámetros entrenables.** Puede ahorrar memoria de entrenamiento y, especialmente, almacenamiento por tarea, compartiendo una base congelada. No elimina el coste de cargar esa base ni garantiza igualar al ajuste completo en cualquier tarea.

| Method | What is trained | Adaptation mechanism | Inference implications |
| --- | --- | --- | --- |
| Full fine-tuning | Todos los parámetros | Modificar el modelo completo | Misma estructura; copia completa por especialización si se guardan por separado |
| BitFit | Biases existentes | Ajustar desplazamientos de transformaciones | Misma estructura; cargar los biases de la tarea |
| Adapters | Módulos de bottleneck | Añadir transformaciones pequeñas | Operaciones y profundidad adicionales |
| Prompt tuning | $m$ embeddings del soft prompt | Anteponer vectores continuos a la entrada | Secuencia de entrada más larga |
| LoRA | Factores $A$ y $B$ | $\Delta W=(\alpha/r)AB$, de rango como máximo $r$ | Sin rama adicional tras fusionar la actualización |
| IA³ | Vectores $l_k$, $l_v$, $l_{\mathrm{ff}}$ | Reescalar keys, values y activaciones feed-forward | Sin reescalados adicionales tras absorberlos en los pesos |

> Las expresiones que conviene recordar son:
>
> $$
> N_{\mathrm{prompt}}=m\,d_{\mathrm{model}},
> \qquad
> N_{\mathrm{LoRA}}=r(d_{\mathrm{in}}+d_{\mathrm{out}}),
> $$
>
> $$
> y_{\mathrm{LoRA}}
> =xW+\frac{\alpha}{r}(xA)B,
> \qquad
> W_{\mathrm{merged}}
> =W+\frac{\alpha}{r}AB,
> $$
>
> $$
> W^K_{\mathrm{eff}}=W^K\operatorname{diag}(l_k),
> \quad
> W^V_{\mathrm{eff}}=W^V\operatorname{diag}(l_v),
> \quad
> W_{2,\mathrm{eff}}=\operatorname{diag}(l_{\mathrm{ff}})W_2.
> $$

> La inicialización debe conservar el comportamiento preentrenado: **producto cero en LoRA y vectores de unos en IA³**. Congelar pesos impide actualizarlos; no demuestra que su derivada matemática sea cero.

> Para elegir una técnica hay que valorar conjuntamente **rendimiento en la tarea, parámetros entrenables, memoria, almacenamiento por especialización y latencia de inferencia**. Los resultados experimentales muestran que adaptaciones pequeñas pueden ser muy eficaces, pero la elección del mecanismo y la configuración importan tanto como el presupuesto.
