### I. Clasificación de Texto y Planteamiento

#### 1. Definición de la Tarea de Clasificación de Texto

> La **clasificación de texto** es la tarea de **asignar una etiqueta/clase a un texto**.  
> Definición formal del material: sea un vocabulario $V$ y sea $$D={(w_1,\dots,w_n)\mid n\in\mathbb{N}, w_i\in V}$$el conjunto de documentos (cada documento es una secuencia finita de palabras de $V$).  
> La tarea consiste en:
> - **Input**: un documento $d\in D$ y un conjunto fijo de clases $C={c_1,\dots,c_J}$.
> - **Output**: una clase predicha $\hat c\in C$ para el documento $d$.
#### 2. Decisión de Clasificación en un Clasificador Probabilístico
> Para un **clasificador probabilístico** y un documento (d), la decisión se toma seleccionando la clase más probable:  $\hat c = \arg\max_{c\in C} P(c\mid d)$.  
#### 3. Ejemplo de Clasificador Probabilístico en Acción (Modelo Preentrenado)
> El material ilustra la idea usando un modelo preentrenado para **sentiment analysis** (ejemplo con DistilBERT finetuneado en SST-2): se tokeniza el texto, se obtienen **logits**, se aplica **softmax** para probabilidades y se decide la clase con $\arg\max$.  
> Ejemplo 1 (texto positivo) y salida mostrada: probabilidad muy alta de _Positive_.  
> Ejemplo 2 (texto negativo) y salida mostrada: probabilidad muy alta de _Negative_.
#### 4. Familias de Clasificadores Probabilísticos
> El material menciona varias familias (entre otras):
> - **Logistic regression**
> - **Neural networks**
> - **Naive Bayes**  

### II. Representación Bag-of-Words
#### 1. Motivación: Convertir Documentos a Vectores
> El material plantea el problema: **logistic regression** toma como entrada vectores reales $x\in\mathbb{R}^k$, pero en clasificación de texto la entrada natural es un documento $d=(w_1,\dots,w_n)$.  
> Pregunta central: ¿Cómo representamos $d$ como un vector real $x_d$? Una solución simple y común: **Bag-of-Words**.
#### 2. Definición de Bag-of-Words (BoW)
> La representación **Bag-of-Words** transforma un documento $d$ en un vector $x_d\in\mathbb{R}^{|V|}$.
> - Cada posición del vector corresponde a una palabra del vocabulario $V$.
> - El componente $x^d_j$ indica cuántas veces aparece la j-ésima palabra del vocabulario en el documento $d: x^d_j=\text{número de ocurrencias de la palabra }j\text{ en }d$
#### 3. Pros y Contras de BoW
> Ventajas que destaca el material:
> - **Simple**, **interpretable** y **fácil de computar**.
> - Captura **multiplicidad** (cuántas veces aparece una palabra).  
> 
> Desventajas:
> - **Ignora completamente el orden** de palabras.
> - Por ignorar el orden, frases distintas pueden mapear al **mismo vector** (ej.: “This movie is great and not too long” vs “This movie is long and not too great”).
> - También es común ignorar **puntuación** en BoW (_¡_,  _;_,  etc.).
#### 4. Orden y Puntuación Importan
> El material incluye una diapositiva (imagen) donde dos frases difieren por puntuación (cambia el significado), pero al ignorar puntuación podrían acabar con el **mismo BoW**, ilustrando la limitación.
#### 5. Cuándo BoW Puede Ser Suficiente
> El material señala que BoW puede bastar en tareas simples: por ejemplo, en clasificación de noticias, un documento puede detectarse como financiero si aparecen frecuentemente palabras como “stocks”, “trade” o “investors”.

### III. Regresión Logística para Clasificación Binaria
#### 1. Planteamiento del Problema
> Dado un vector del documento $x\in\mathbb{R}^n$, el objetivo es predecir una clase $y\in{0,1}$.  
> En logistic regression se combinan:
> - un vector de pesos $\theta\in\mathbb{R}^n$
> - un sesgo $b\in\mathbb{R})$ para computar $P(y\mid x)$.
#### 2. Definición del Clasificador y Función Sigmoide
> Definición del material:  $$P(y=1\mid x)=\sigma(z),\quad z=\theta\cdot x+b=\left(\sum_{j=1}^{n}\theta_j x_j\right)+b$$donde $\sigma:\mathbb{R}\to(0,1)$ es la sigmoide: $\sigma(z)=\frac{1}{1+e^{-z}}$  
> 
> Decisión de clasificación (umbral 0.5):  $decision(x)=\begin{cases}1 & \text{si } P(y=1\mid x)>0.5 \\0 & \text{en otro caso}\end{cases}$
#### 3. Intuición de la Sigmoide
> La sigmoide transforma $z=\sum_j \theta_j x_j + b$ a un valor en $(0,1)$ que se interpreta como probabilidad.
> - $z$ grande y positivo $\Rightarrow$ probabilidad cercana a 1 (alta confianza en clase 1).
> - $z$ pequeño y negativo $\Rightarrow$ probabilidad cercana a 0 (alta confianza en clase 0).
> - $z=0 \Rightarrow \sigma(0)=0.5$ incertidumbre.
#### 4. Quiz: Sentiment Analysis con BoW y Logistic Regression
> Setup del material: vocabulario con 8 “tokens” (incluye “!”) y documento “I loved this stupid movie!”.  
> Pesos y sesgo: $b=0$  y  $\theta=[0,1.5,0,-0.5,0,0,0,-0.1]$  
> Solución mostrada:
> - Vector BoW:  $x=[1,1,1,1,1,0,0,1]$
> - Suma ponderada: $z=\sum_{i=1}^{8}\theta_i x_i=0+1.5+0-0.5+0+0+0-0.1=0.9$  
> - Probabilidad: $\sigma(0.9)\approx 0.71$.
> - Decisión: como $\sigma(z)>0.5$, clase positiva (1).
#### 5. Interpretación de Pesos en Sentiment Analysis
> Con BoW, los pesos $\theta_i$ se interpretan así:
> - $\theta_i$ grande y positivo $\Rightarrow$ palabra indica sentimiento positivo (“nice”, “love”, “thrilling”…).
> - $\theta_i$ grande y negativo $\Rightarrow$ palabra indica sentimiento negativo (“bad”, “hate”, “boring”…).
> - $\theta_i\approx 0$ $\Rightarrow$ impacto pequeño o nulo (palabras neutras como “and”, “of”…).
#### 6. Ejemplo: IMDB Dataset
> El material presenta IMDB como dataset clásico de sentiment analysis con **50K** reseñas, etiquetadas como positivas o negativas.  
> Incluye un ejemplo de reseña negativa y lista palabras con mayores conteos en su BoW (ej.: “stick”, “fans”, “film”, “awful”, “movie”…).  
> Tras entrenar una logistic regression a ~**85%** de accuracy, el material muestra ejemplos de palabras con pesos altos positivos y negativos, y palabras “neutras” con peso (casi) 0.
#### 7. Aprender Parámetros: Máxima Verosimilitud y Cross-Entropy
> Objetivo: aprender (\theta) y (b) para que, en cada ejemplo $(x,y)$, el modelo asigne alta probabilidad a la clase correcta.  
> El modelo define: $$P(y=1\mid x)=\sigma(\theta\cdot x+b),\quad P(y=0\mid x)=1-\sigma(\theta\cdot x+b)$$Para entrenar se usa **negative log-likelihood**, también llamada **cross-entropy loss**; minimizarla equivale a maximizar la likelihood de los datos.
#### 8. Caso de Un Ejemplo: Objetivo de Máxima Verosimilitud
> Para un solo ejemplo $(x,y)$, el material define $(\theta^*,b^*)$ como los parámetros que maximizan la probabilidad de la etiqueta observada.
> - Si $y=1:$ $(\theta^*,b^*)=\arg\max_{(\theta,b)} P(y=1\mid x)=\arg\max_{(\theta,b)} \sigma(x\cdot\theta+b)$  
> - Si $y=0:$ $(\theta^*,b^*)=\arg\max_{(\theta,b)} P(y=0\mid x)=\arg\max_{(\theta,b)} \left(1-\sigma(x\cdot\theta+b)\right)$
#### 9. De Máxima Verosimilitud a Negative Log-Likelihood
> El material hace la cadena de equivalencias (para un ejemplo):  
	$\arg\max_{(\theta,b)} P_{\theta,b}(y\mid x) =\arg\max_{(\theta,b)} \log P_{\theta,b}(y\mid x) =$  
	$=\arg\min_{(\theta,b)} -\log P_{\theta,b}(y\mid x)  =\arg\min_{(\theta,b)} L_{CE}(x,y)$  
#### 10. Definición de Binary Cross-Entropy (Un Ejemplo)
> Para etiquetas $y\in{0,1}$, la pérdida BCE del material es:  
> $L_{BCE}(x,y)= \begin{cases} -\log P(y=1\mid x) & \text{si } y=1 \\ -\log P(y=0\mid x) & \text{si } y=0 \end{cases}$
#### 11. Quiz: Cálculo de la Pérdida en el Ejemplo
> Usando el ejemplo anterior con $P(y=1\mid x)=0.71$ (y log natural $\ln$):
> - Si $y=1: L_{BCE}(x,y)=-\ln(0.71)\approx 0.34$  
> - Si $y=0: L_{BCE}(x,y)=-\ln(1-0.71)=-\ln(0.29)\approx 1.23$  
#### 12. BCE para N Ejemplos
> Para un dataset $D={(x^{(1)},y^{(1)}),\dots,(x^{(N)},y^{(N)})}$, la pérdida media:  
	$L_{BCE}(D)=\frac{1}{N}\sum_{i=1}^{N} L_{BCE}(x^{(i)},y^{(i)})$  
#### 13. Optimización: Stochastic Gradient Descent
> El material propone minimizar la pérdida con **gradient descent / SGD**: calcular el gradiente tras cada ejemplo y actualizar $\theta$ y $b$ en la dirección opuesta al gradiente.  
> Pseudocódigo: inicializar $\theta,b$; repetir por epochs; recorrer ejemplos; actualizar: $\theta\leftarrow \theta-\alpha\nabla_\theta L_{CE}(x^{(i)},y^{(i)})), \quad b\leftarrow b-\alpha\nabla_b L_{CE}(x^{(i)},y^{(i)})$.
#### 14. Gradientes de la BCE para Logistic Regression
> Fórmulas dadas en el material (para un ejemplo $(x,y)$):  
	$\frac{\partial L_{CE}(x,y)}{\partial \theta_j}=\left(\sigma(\theta\cdot x+b)-y\right)x_j,\qquad   \frac{\partial L_{CE}(x,y)}{\partial b}=\sigma(\theta\cdot x+b)-y$
> Gradientes en vector:  
	$\nabla_\theta L_{CE}(x,y)=\left(\sigma(\theta\cdot x+b)-y\right)x,\quad \nabla_b L_{CE}(x,y)=\sigma(\theta\cdot x+b)-y$
#### 15. Interpretación del Término del Gradiente
> El material reescribe el término como $(P(y=1\mid x)-y)\cdot x_j$ y lo interpreta como “**cómo de equivocado** está el modelo” por la presencia de la feature $x_j$.
> - Caso $y=0$, $x_j\neq 0$: si el modelo asigna probabilidad a clase 1, el término es positivo; al restarlo, $\theta_j$ baja y se reduce $P(y=1\mid x)$ para ese ejemplo.
> - Caso $y=1$, $x_j\neq 0$: si el modelo asigna probabilidad a clase 0, el término es negativo; al restarlo, $\theta_j$ sube y aumenta $P(y=1\mid x)$.
#### 16. Quiz: Gradientes en “I loved this stupid movie!”
> Para $\sigma(\theta\cdot x+b)=0.71$ y $x=[1,1,1,1,1,0,0,1]$:
> - Si $y=1: \nabla_\theta = -0.29\cdot x = [-0.29,-0.29,-0.29,-0.29,-0.29,0,0,-0.29],\quad \nabla_b=-0.29$  
> - Si $y=0 \nabla_\theta = 0.71\cdot x = [0.71,0.71,0.71,0.71,0.71,0,0,0.71],\quad \nabla_b=0.71$ 
#### 17. Quiz: Actualización de Pesos con $\alpha=0.1$
> Con pesos iniciales $\theta=[0,1.5,0,-0.5,0,0,0,-0.1]$ y $b=0$, el material muestra:
> - Si $y=1 \theta_{new}=[0.029,1.529,0.029,-0.471,0.029,0,0,-0.071],\quad b_{new}=0.029$
> - Si $y=0: \theta_{new}=[-0.071,1.429,-0.071,-0.571,-0.071,0,0,-0.171],\quad b_{new}=-0.071$.  
#### 18. Resumen de Regresión Logística (Según el Material)
> - Logistic regression mapea $x$ a $\sigma(\theta\cdot x+b)$, con $\theta$ y $b$ entrenables.
> - Decide $y=1$ si $\sigma(\theta\cdot x+b)>0.5$.
> - Se entrena minimizando cross-entropy con SGD.

### IV. Naive Bayes para Clasificación de Texto
#### 1. Regla de Bayes Aplicada a Documentos y Clases
> El material aplica Bayes: para documento $d$ y clase $c$,  $P(c\mid d)=\frac{P(d\mid c)P(c)}{P(d)}$  
#### 2. Decisión MAP y Simplificación
> La clase predicha se define como la de máxima probabilidad a posteriori: $$c_{MAP}=\arg\max_{c\in C}P(c\mid d)  
> =\arg\max_{c\in C}\frac{P(d\mid c)P(c)}{P(d)}  
> =\arg\max_{c\in C}P(d\mid c)P(c)$$Si $d$ es una secuencia $w_1,\dots,w_n$, entonces $P(d\mid c)=P(w_1,\dots,w_n\mid c)$
#### 3. Supuesto Naive Bayes (Independencia Condicional)
> Supuesto “naive”: la probabilidad de cada palabra en un documento de clase $c$ **no depende de qué otras palabras** estén en el documento.  
> Formalmente:  $$P(w_1,\dots,w_n\mid c)=\prod_{i=1}^{n}P(w_i\mid c)$$Con esto, la decisión queda:  $c_{NB}=\arg\max_{c\in C} P(c)\prod_{i=1}^{n}P(w_i\mid c)$, separando **prior** $P(c)$ y probabilidades condicionales $P(w_i\mid c)$.
#### 4. Estimación del Prior (P(c))
> Con training set $D={(d_1,c_1),\dots,(d_m,c_m)}$, el prior se estima como proporción de documentos de la clase: $P(c)=\frac{N_c}{m}$, donde $N_c$ es el número de documentos con etiqueta $c$ en el train y $m$ el total.
#### 5. Estimación de $P(w_k\mid c)$
> Para una palabra $w_k$ y clase $c$ $P(w_k\mid c)=\frac{count(w_k,c)}{\sum_{w\in V} count(w,c)}$, donde $count(w_k,c)$ es el número de ocurrencias de $w_k$ en documentos de clase $c$, y el denominador es el total de palabras (con repeticiones) en documentos de esa clase.
#### 6. Problema de Probabilidades Cero
> Si una palabra aparece en test pero nunca apareció en training para una clase, entonces $P(w\mid c)=0$, lo que anula todo el likelihood del documento para esa clase:  $$P(d\mid c)=\prod_i P(w_i\mid c)=0$$El material lo ilustra con la palabra “great” no observada en documentos positivos: “no haberla visto” no implica que sea imposible en un documento positivo.
#### 7. Fix: Additive Smoothing (Laplace / Add-1)
> Se aplica smoothing aditivo (como en language models): añadir $\delta$ a los conteos: $$P(w\mid c)=\frac{\delta + count(w,c)}{\sum_{w\in V}(\delta + count(w,c))}  
> =\frac{\delta + count(w,c)}{\delta|V|+\sum_{w\in V}count(w,c)}$$Si $\delta=1$, es **Laplace smoothing / Add-1**.
#### 8. Problema Numérico: Underflow y Solución con Log-Probabilities
> Multiplicar muchas probabilidades pequeñas puede causar **floating-point underflow**.  
> Solución: usar logs y que $\log(ab)=\log a + \log b$.  
> Como $\log$ es monótona creciente, no cambia el ranking de clases, y la decisión se reescribe:  
	$c_{NB}=\arg\max_{c\in C}\left(\log P(c)+\sum_{i=1}^{n}\log P(w_i\mid c)\right)$  
#### 9. Palabras Desconocidas (Out-of-Vocabulary)
> Si aparecen palabras en test que no están en training (fuera del vocabulario), el material indica: **se ignoran**.  
> Operativamente: se eliminan del documento de test (“pretend they weren’t there”).
#### 10. Quiz Guiado: Ejemplo Completo de NB con Add-One
> El material propone un mini-ejemplo de sentiment con clases (+) y (-), con 5 documentos de entrenamiento (3 negativos, 2 positivos) y un documento de test “predictable with no fun”.  
> Prior: $$ P(-)=\frac{3}{5},\quad P(+)=\frac{2}{5}$$Se usa decisión con logs:  $$c_{NB}=\arg\max_{c\in C}\left(\log P(c)+\sum_i \log P(w_i\mid c)\right)$$Resultado numérico mostrado por el material (sumas de log-probabilidades):
> - Para clase negativa: $\approx -9.7$
> - Para clase positiva: $\approx -10.3$  
> Por tanto, la clase predicha para el test es **negativa (-)** (porque $-9.7 > -10.3$).
#### 11. Resumen de Naive Bayes (Según el Material)
> i) Naive Bayes: método simple basado en **Bayes**.
> i)) Predice la clase con máxima probabilidad a posteriori (MAP): $$c_{MAP}=\arg\max_{c\in C}P(c\mid w_1,\dots,w_n)=\arg\max_{c\in C}P(w_1,\dots,w_n\mid c)P(c)$$iii) Supuesto NB: independencia condicional de palabras dado (c): $$P(w_1,\dots,w_n\mid c)=\prod_i P(w_i\mid c)$$iv) Priors y probabilidades condicionales se estiman con **conteos** en training.

Los apuntes continúan en [[Tema 3 - Word Embeddings]]