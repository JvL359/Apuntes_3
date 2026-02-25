### I. Modelado de Lenguaje y Motivación
#### 1. Problema de Modelado de Lenguaje
> Se estudia el problema de **construir un modelo de lenguaje (LM)** a partir de un conjunto de **oraciones de ejemplo** (datos).  
> El tema introduce primero la **definición general** de LM y después los **modelos n-gram**, como el tipo más simple obtenido desde datos.
#### 2. Modelos de Lenguaje Como Predictores de la Siguiente Palabra
> Un LM observa una **secuencia de palabras** y plantea: **“¿qué palabra es más probable que venga después?”**  
> Dado un contexto como “she was a”, el LM asigna probabilidades a posibles continuaciones (por ejemplo, $p(\text{woman}\mid \text{she was a})$, $p(\text{doctor}\mid \text{she was a})$, etc.).  
> El material señala que esta predicción “internaliza”:
> - Conocimiento del mundo (ej.: “Spain’s capital is …”)
> - Sintaxis (ej.: “she …” → $p(\text{speaks}\mid \text{she}) > p(\text{speak}\mid \text{she})$)
> - Restricciones semánticas (ej.: “I ate an …”)
#### 3. Modelos de Lenguaje Como Máquinas de “Fill-in-the-Blank”
> El material describe los LMs modernos como **máquinas de completar huecos**: completan texto prediciendo una palabra siguiente plausible.  
> Ejemplo tipo “fill-in-the-blank” (se muestra un texto sobre París) para ilustrar que el modelo asigna probabilidades a posibles siguientes palabras y elige una que encaje con el contexto.
#### 4. Demos Enlazadas en el Material
> El PDF incluye enlaces a demos, que sirven para “ver” el comportamiento del LM:
> - Demo de un LM (“dec-viz” en HuggingFace).
> - Demo/playground de n-gram LMs (“Kind off... Link to demo”).

### II. Definiciones Formales de Modelos de Lenguaje
#### 1. Vocabulario y Secuencias de Palabras
> **Vocabulario $V$**: conjunto fijo y finito de símbolos (palabras/tokens). 
> - Ejemplo: $V={\text{the, a, man, telescope, dog, 1925, Madrid, …}}$  
> **Secuencia de palabras sobre $V$**: cualquier secuencia finita $(w_1,\dots,w_n)$ con $w_i\in V$ y $n\in\mathbb{N}$.
#### 2. Oraciones con Tokens Especiales BOS/EOS
> Se introducen tokens especiales:
> - **BOS**: inicio de oración
> - **EOS**: fin de oración  
> Una **oración** es una secuencia $(\text{BOS}, w_1,\dots,w_n,\text{EOS})$, donde $(w_1,\dots,w_n)$ es una secuencia sobre $V$.
> Además de definir las oraciones como $(\text{BOS}, w_1,\dots,w_n,\text{EOS})$, el material **denota por $\bar V$** el conjunto de todas las oraciones de esa forma.
#### 3. Definición de Modelo de Lenguaje
> Un **modelo de lenguaje** sobre un vocabulario $V$ asigna, a cada secuencia finita, una **distribución de probabilidad sobre la siguiente palabra**.  
> Formalmente, para cualquier secuencia $(w_1,\dots,w_n)$ con $w_i\in V$, define:
> - $p(w_{n+1}\mid \text{BOS}, w_1,\dots,w_n)$, con $w_{n+1}\in V\cup{\text{EOS}}$.

### III. Probabilidad de una Oración y Estimación por Conteos
#### 1. Probabilidad de Oración Mediante Regla de la Cadena
> El LM no asigna “directamente” probabilidad a oraciones, pero a partir de probabilidades de siguiente palabra se puede calcular la probabilidad de una oración completa.  
> Por la **regla de la cadena**:
> - $p(\text{BOS}, w_1,\dots,w_n)=p(\text{BOS})\prod_{i=1}^{n} p(w_i\mid \text{BOS}, w_1,\dots,w_{i-1})$  
>     El material fija $p(\text{BOS})=1$ (toda oración empieza con BOS).
#### 2. Ejemplo de Probabilidad de Oración
> Para “BOS Biking is fun EOS” (vamos a poner "BOS" como "+" y "EOS" como "-")
> $p(\text{+}, \text{Biking}, \text{is}, \text{fun}, \text{-}) =$
> $p(\text{+})\cdot p(\text{Biking}\mid \text{+})\cdot p(\text{is}\mid \text{+},\text{Biking})\cdot p(\text{fun}\mid \text{+},\text{Biking},\text{is})\cdot p(\text{-}\mid \text{+},\text{Biking},\text{is},\text{fun})$
#### 3. Estimación de $p(w\mid c)$ con Frecuencia Relativa
> Idea base: estimar la probabilidad de una continuación mirando **cuántas veces** aparece en un corpus.  
> Para un contexto $c$ (ej.: “she was a”) y una palabra $w$ (ej.: “woman”): $$p(w\mid c)\approx \dfrac{\text{veces que }c\text{ va seguido de }w}{\text{veces que}c\text{ va seguido de alguna palabra}}$$Ejemplo en _Pride and Prejudice_:
> - $\text{count}(\text{“she was a ”})=7$
> - $\text{count}(\text{“she was a woman”})=1$
> - $p(\text{woman}\mid \text{she was a})=\dfrac{1}{7}\approx 0.14$
#### 4. Procedimiento General de Estimación por Conteos
> Para estimar $p(w_n\mid w_1,\dots,w_{n-1})$ con $w_n\in V\cup{\text{EOS}}$, el material propone:
> - (1) Tomar un **corpus** (conjunto grande de documentos).
> - (2) Dividir en oraciones y añadir **BOS** al inicio y **EOS** al final.
> - (3) Contar $\text{count}(w_1,\dots,w_{n-1},w_n)$.
> - (4) Contar el total del contexto: $\sum_{w\in V\cup{\text{EOS}}} \text{count}(w_1,\dots,w_{n-1},w)$.
> - (5) Definir:
>      $p(w_n\mid w_1,\dots,w_{n-1})=\dfrac{\text{count}(w_1,\dots,w_{n-1},w_n)}{\sum_{w\in V\cup{\text{EOS}}} \text{count}(w_1,\dots,w_{n-1},w)}$

### IV. Modelos N-Gram y Supuesto Markoviano
#### 1. Limitación de Contextos Largos y Problema de Conteos Cero
> El material advierte que, para contextos largos (ej.: de 11 palabras), el número de contextos posibles crece como $|V|^{11}$.  
> Con $|V|=100{,}000=10^5$, eso implicaría hasta $10^{55}$ contextos posibles: la mayoría no aparece en el corpus → **conteos cero**.  
> Consecuencia: secuencias “aceptables” pueden tener probabilidad estimada 0 (ejemplo con “a kid who had a dream”).
> El material enfatiza que **ni siquiera la web entera** es suficiente para estimar bien conteos de secuencias “algo largas”.  
> - Ejemplo: la secuencia “the water in the Atlantic sea is so beautifully blue” devuelve **0 resultados** en Google, ilustrando conteos cero incluso “a gran escala”.
#### 2. Supuesto Markoviano Para N-Grams
> Para mitigar el problema anterior, los n-grams hacen un supuesto de independencia: la probabilidad de la siguiente palabra depende solo de un número **fijo y pequeño** de palabras previas.  
> Casos mencionados:
> - **Bigram (n=2)**: $p(w_m\mid w_1,\dots,w_{m-1})\approx p(w_m\mid w_{m-1})$
> - **Trigram (n=3)**: $p(w_m\mid w_1,\dots,w_{m-1})\approx p(w_m\mid w_{m-2},w_{m-1})$
#### 3. Definición de Modelo de Lenguaje N-Gram
> Un **n-gram LM** aplica el supuesto Markoviano:
> 	$p(w_m\mid w_1,\dots,w_{m-1}) \approx p(w_m\mid w_{m-(n-1)},\dots,w_{m-1})$  
> Y estima esa probabilidad por conteos (frecuencia relativa) usando solo el contexto de longitud $n-1$:
> 	$p(w_m\mid w_{m-(n-1)},\dots,w_{m-1})=\dfrac{\text{count}(w_{m-(n-1)},\dots,w_{m-1},w_m)}{\sum_{w\in V\cup{\text{EOS}}}\text{count}(w_{m-(n-1)},\dots,w_{m-1},w)}$  
> Ejemplo que da el material (trigram):
> 	$p(\text{dream}\mid \text{a kid who had a})\approx p(\text{dream}\mid \text{had a})=\dfrac{\text{count}(\text{had a dream})}{\sum_{w\in V\cup{\text{EOS}}}\text{count}(\text{had a }w)}$
#### 4. Palabras Iniciales y Uso de Múltiples BOS
> Problema: si el modelo condiciona en $n-1$ palabras, al inicio de oración “faltan” palabras previas.  
> Solución del material:
> - Poner **$n-1$ tokens BOS** al comienzo de cada oración.  
>     En trigram ($n=3$):
> - “BOS I like black coffee EOS” se transforma en “BOS BOS I like black coffee EOS”. Así:
> 	$p(I\mid \text{BOS},\text{BOS})=\dfrac{\text{count}(\text{BOS},\text{BOS},I)}{\text{count}(\text{BOS},\text{BOS})}$  
> Además, el material fija $p(\text{BOS})=1$.
#### 5. Por Qué “N-Gram”
> Un **n-gram** es una secuencia de **n palabras consecutivas** en una oración.  
> El material ilustra:
> - Unigramas ($n=1$): “This”, “is”, “a”, “sentence”
> - Bigramas ($n=2$): “This is”, “is a”, “a sentence”
> - Trigramas ($n=3$): “This is a”, “is a sentence”
> El material añade explícitamente que los n-gram LMs **asignan probabilidades basándose únicamente en conteos de frecuencia** de n-grams.

### V. Ejemplos Guiados en Diapositivas
#### 1. Ejemplo de Corpus y Cálculo de $p(\text{better}\mid \text{dogs are})$
> Corpus (4 oraciones) usado en el material:
> - BOS dogs are loyal companions EOS
> - BOS birds chirp in the morning EOS
> - BOS dogs are better than cats EOS
> - BOS dogs are your best friend EOS  
> Se pide la distribución tras el contexto “dogs are \_\_\_”, en particular $p(\text{better}\mid \text{dogs are})$.  
> Pasos mostrados:
> - Numerador: $\text{count}(\text{dogs are better})=1$
> - Denominador: $\sum_{w\in V\cup{\text{EOS}}}\text{count}(\text{dogs are }w)=1+1+1=3$
> - Resultado: $p(\text{better}\mid \text{dogs are})=\dfrac{1}{3}$  
> Y la distribución completa para ese contexto queda:
> 	$p(\text{loyal}\mid \text{dogs are})=p(\text{better}\mid \text{dogs are})=p(\text{your}\mid \text{dogs are})=\dfrac{1}{3}$
#### 2. Quiz de Bigrama: Conteos, Probabilidades y Probabilidad de Oración
> Vocabulario: $V={a,b}$. Corpus con 4 oraciones:
> - BOS a a EOS
> - BOS a b EOS
> - BOS b a EOS
> - BOS b b EOS  
> 
>Conteos de bigramas que lista el material:
> - $count(BOS a)=2, count(BOS b)=2$
> - $count(a a)=1, count(a b)=1, count(a EOS)=2$
> - $count(b a)=1, count(b b)=1, count(b EOS)=2$  
> 
> Probabilidades condicionales que da el material (ejemplos):
> - $p(a\mid \text{BOS})=\tfrac{2}{4}=0.5$, $p(b\mid \text{BOS})=\tfrac{2}{4}=0.5$
> - $p(a\mid a)=\tfrac{1}{4}=0.25$, $p(b\mid a)=0.25$, $p(\text{EOS}\mid a)=0.5$
> - $p(a\mid b)=0.25$, $p(b\mid b)=0.25$, $p(\text{EOS}\mid b)=0.5$  
> 
> Probabilidad de “BOS a EOS”:
> - $p(\text{BOS } a \ \text{EOS})=p(a\mid \text{BOS})\cdot p(\text{EOS}\mid a)=(0.5)(0.5)=0.25$  
>     
> Probabilidad de “BOS a a b EOS”:
> - $p(\text{BOS } a\ a\ b\ \text{EOS})=p(a\mid \text{BOS})p(a\mid a)p(b\mid a)p(\text{EOS}\mid b)=(0.5)(0.25)(0.25)(0.5)=0.015625$
#### 3. Nota de Implementación (Diapositiva)
> El material incluye una sección de “code example” para implementar un **trigram model** sobre un corpus real y menciona un [**Notebook Lin**](https://colab.research.google.com/drive/1HeQmMZNv9Zd430knPSg6qq3Z9I7l3EKs?usp=sharing)

### VI. Limitaciones de N-Grams y “Parches” del Material
#### 1. Problema de Conteos Cero (De Nuevo)
> Incluso con trigramas pueden aparecer frases aceptables con probabilidad 0 si el n-grama relevante nunca aparece en el corpus (ejemplo con “el rey español”).  
> El material recalca la idea clave: “aceptable” $\nRightarrow$ “observado en el corpus”, así que el 0 es un artefacto de estimación.
#### 2. Fix 1: Smoothing (Laplace / Add-1 y Add-δ)
> Solución simple: **pretender** que se ha visto cada n-gram al menos una vez (sumar 1 a los conteos).  
> **Laplace / add-1 smoothing**:
> 	$p_{\text{add-1}}(w_n\mid w_1,\dots,w_{n-1})=\dfrac{\text{count}(w_1,\dots,w_{n-1},w_n)+1}{\sum_{w\in V\cup{\text{EOS}}}\text{count}(w_1,\dots,w_{n-1},w)+|V\cup{\text{EOS}}|}$  
> El material explica que al sumar al numerador hay que ajustar el denominador para que las probabilidades sigan sumando 1.  
>
> **Add-δ smoothing** (generalización):
> 	$p_{\text{add-}\delta}(w_n\mid w_1,\dots,w_{n-1})=\dfrac{\text{count}(w_1,\dots,w_{n-1},w_n)+\delta}{\sum_{w\in V\cup{\text{EOS}}}\text{count}(w_1,\dots,w_{n-1},w)+\delta|V\cup{\text{EOS}}|}$
> Además de la fórmula general, el material muestra el ejemplo concreto:  
> 	$p_{\text{add-1}}(\text{es}\mid \text{el rey español}) = \dfrac{\text{count} (\text{el rey español es}) + 1}{\sum_{w\in V\cup\{\text{EOS}\}} \text{count}(\text{el rey español } w) + |V\cup\{\text{EOS}\}|}$
#### 3. Fix 2: Backoff
> Otra opción del material: **backoff**. Idea operativa:
> - si puedes, usa el conteo de n-gram
> - si es 0, usa el de (n−1)-gram
> - si también falla, sigue bajando hasta unigram en el peor caso  
> El material ilustra el caso en un 4-gram: si $N(\text{cat on a})=0$, se “retrocede” a contextos más cortos.
#### 4. Problema de Dependencias a Largo Plazo (Topic Drift)
> En un trigram, solo se condiciona en las **dos últimas palabras**, así que el modelo “apenas recuerda” el tema y puede derivar (topic drift).  
> El material lo ejemplifica con un prompt “la base”, donde la generación pasa de “base militar” a “elecciones”.  
> Mensaje del material: la incapacidad de usar contextos largos y capturar dependencias a largo plazo es una limitación principal de n-grams.
#### 5. Problema de Generalización
> El material compara dos contextos similares:
> - “a doctor entered the”
> - “a nurse entered the”  
> En n-grams:
> - se tratan como **contextos independientes**
> - las probabilidades vienen de conteos no relacionados  
> Consecuencia: puede ocurrir que $p(\text{hospital}\mid \text{a doctor entered the})$ sea alta mientras $p(\text{hospital}\mid \text{a nurse entered the})$ sea 0 (o solo suavizada).  
> Idea que plantea el material: “¿no debería el conocimiento de un contexto informar al otro?” (n-grams no lo hacen).

### VII. Resumen Final del Tema
#### 1. Ideas Clave
> i) Un LM predice la **siguiente palabra** a partir de las anteriores.
> ii) Las probabilidades se pueden estimar con **conteos normalizados**: $$p(w_n\mid w_1,\dots,w_{n-1})=\dfrac{\text{count}(w_1,\dots,w_{n-1},w_n)}{\sum_{w\in V\cup{\text{EOS}}}\text{count}(w_1,\dots,w_{n-1},w)}$$iii) Un n-gram LM usa el supuesto Markoviano: depende solo de las **últimas $n-1$** palabras, y se estima por conteos de bigramas; en bigram: $$p(w_n\mid w_1,\dots,w_{n-1})\approx p(w_n\mid w_{n-1})$$Problemas técnicos (sparsity/zero counts) se pueden mitigar con **smoothing** y **backoff**, pero hay limitaciones fundamentales:
> - no manejan bien contextos largos
> - no generalizan a contextos no vistos/similares

Los apuntes continúan en [[Tema 2 - Text Classification I]]