## DpL-IGF 5. Machine Learning Basics - Maximum Likelihood Estimation
### I. Principio y Derivación de Máxima Verosimilitud

#### 1. Motivación del Principio

> El material plantea que, en vez de “adivinar” estimadores y luego analizar sesgo y varianza, interesa disponer de un **principio** que permita **derivar** funciones estimadoras “buenas” para distintos modelos; el principio más común es el de **máxima verosimilitud**.

#### 2. Planteamiento y Definición del Estimador

> Se considera un conjunto de (m) ejemplos (X={x^{(1)},\dots,x^{(m)}}) extraídos **independientemente** de la distribución verdadera (desconocida) (p_{\text{data}}(x)).  
> Se define una familia paramétrica (p_{\text{model}}(x;\theta)) sobre el mismo espacio, indexada por (\theta).  
> El estimador de máxima verosimilitud se define como:  
> [  
> \theta_{\text{ML}}=\arg\max_{\theta}; p_{\text{model}}(X;\theta)  
> =\arg\max_{\theta}; \prod_{i=1}^{m} p_{\text{model}}(x^{(i)};\theta).  
> ]

#### 3. Log-Verosimilitud y Forma de Expectativa Empírica

> El producto de muchas probabilidades es poco conveniente (por ejemplo, por **subdesbordamiento numérico**), así que el texto toma logaritmos para convertir el producto en suma sin cambiar el (\arg\max).  
> [  
> \theta_{\text{ML}}=\arg\max_{\theta}; \sum_{i=1}^{m}\log p_{\text{model}}(x^{(i)};\theta).  
> ]  
> Como el (\arg\max) no cambia al reescalar, se divide por (m) y se expresa como esperanza respecto a la distribución empírica (\hat{p}_{\text{data}}) definida por el training set:  
> [  
> \theta_{\text{ML}}=\arg\max_{\theta}; \mathbb{E}_{x\sim \hat{p}_{\text{data}}}\log p_{\text{model}}(x;\theta).  
> ]

#### 4. Interpretación con Divergencia KL y Entropía Cruzada

> El material interpreta máxima verosimilitud como minimizar la disimilitud entre (\hat{p}_{\text{data}}) y (p_{\text{model}}) medida por la divergencia KL:  
> [  
> D_{\text{KL}}(\hat{p}_{\text{data}}|p_{\text{model}})  
> =\mathbb{E}_{x\sim \hat{p}_{\text{data}}}\big[\log \hat{p}_{\text{data}}(x)-\log p_{\text{model}}(x)\big].  
> ]  
> Como el término (\mathbb{E}_{x\sim \hat{p}_{\text{data}}}[\log \hat{p}_{\text{data}}(x)]) no depende del modelo, minimizar KL equivale a minimizar:  
> [  
> -\mathbb{E}_{x\sim \hat{p}_{\text{data}}}\big[\log p_{\text{model}}(x)\big],  
> ]  
> que es equivalente a maximizar la log-verosimilitud empírica.  
> El texto afirma que esto corresponde exactamente a minimizar la **entropía cruzada** entre distribuciones, y aclara que **cualquier** pérdida que sea una **log-verosimilitud negativa** es una entropía cruzada (no solo Bernoulli/softmax).  
> También pone el ejemplo: el **MSE** es la entropía cruzada entre la distribución empírica y un **modelo Gaussiano**.

#### 5. NLL en Software y Nota sobre Valores del Objetivo

> El material señala que, aunque el (\theta) óptimo coincide maximizando verosimilitud o minimizando KL, los **valores** de las funciones objetivo difieren.  
> En software, se suele formular como minimizar un coste: máxima verosimilitud se convierte en minimizar la **log-verosimilitud negativa (NLL)**, o equivalentemente minimizar la **entropía cruzada**.  
> La perspectiva de KL ayuda porque KL tiene mínimo conocido 0, mientras que la NLL puede llegar a ser **negativa** cuando (x) es real-valuado.

---

### II. Log-Verosimilitud Condicional y Error Cuadrático Medio

#### 1. Generalización a Probabilidades Condicionales

> El material generaliza el estimador al caso en que se quiere estimar una probabilidad condicional (P(y\mid x;\theta)) para predecir (y) dado (x), que es el caso más común en aprendizaje supervisado.  
> Si (X) son inputs y (Y) targets observados:  
> [  
> \theta_{\text{ML}}=\arg\max_{\theta}; P(Y\mid X;\theta).  
> ]  
> Asumiendo ejemplos i.i.d., se descompone como:  
> [  
> \theta_{\text{ML}}=\arg\max_{\theta}; \sum_{i=1}^{m}\log P(y^{(i)}\mid x^{(i)};\theta).  
> ]

#### 2. Ejemplo: Regresión Lineal como Máxima Verosimilitud

> El texto reinterpreta la regresión lineal (antes motivada como minimizar MSE “más o menos arbitrariamente”) como un procedimiento de máxima verosimilitud: el modelo produce una distribución condicional (p(y\mid x)), no solo una predicción puntual (\hat{y}).  
> Para recuperar el mismo algoritmo, se define:  
> [  
> p(y\mid x)=\mathcal{N}\big(y;\hat{y}(x;w),\sigma^{2}\big),  
> ]  
> donde (\hat{y}(x;w)) predice la media Gaussiana y (\sigma^{2}) se fija como constante elegida por el usuario.

#### 3. Relación Entre Log-Verosimilitud y MSE

> Con i.i.d., la log-verosimilitud condicional es (\sum_{i=1}^{m}\log p(y^{(i)}\mid x^{(i)};\theta)).  
> En el caso Gaussiano, el material la desarrolla como:  
> [  
> \sum_{i=1}^{m}\log p(y^{(i)}\mid x^{(i)};\theta)  
> = -m\log\sigma - \frac{m}{2}\log(2\pi);-;\sum_{i=1}^{m}\frac{\lVert \hat{y}^{(i)}-y^{(i)}\rVert^{2}}{2\sigma^{2}}.  
> ]  
> Y compara con el error cuadrático medio de entrenamiento:  
> [  
> \mathrm{MSE}_{\text{train}}=\frac{1}{m}\sum_{i=1}^{m}\lVert \hat{y}^{(i)}-y^{(i)}\rVert^{2}.  
> ]  
> Conclusión del material: maximizar la log-verosimilitud respecto a (w) produce el **mismo** estimado de (w) que minimizar MSE; los criterios tienen valores distintos pero el **óptimo está en el mismo punto**.

---

### III. Propiedades de Máxima Verosimilitud

#### 1. Optimalidad Asintótica y Tasa de Convergencia

> El material afirma que el principal atractivo del estimador de máxima verosimilitud es que puede mostrarse “el mejor” **asintóticamente** ((m\to\infty)) en términos de su **tasa de convergencia** al crecer (m).

#### 2. Consistencia y Condiciones

> Bajo condiciones apropiadas, el estimador de máxima verosimilitud es **consistente**: cuando el número de ejemplos tiende a infinito, el estimado del parámetro converge al valor verdadero.  
> El texto lista estas condiciones:
> 
> - La distribución verdadera (p_{\text{data}}) debe estar dentro de la familia del modelo (p_{\text{model}}(\cdot;\theta)).
>     
> - (p_{\text{data}}) debe corresponder a **exactamente un** valor de (\theta); si no, máxima verosimilitud puede recuperar el (p_{\text{data}}) correcto pero no determinar qué (\theta) lo generó.
>     

#### 3. Eficiencia Estadística y Cota de Cramér-Rao

> El material indica que hay otros principios inductivos además de máxima verosimilitud; muchos también son consistentes, pero pueden diferir en **eficiencia estadística** (por ejemplo, lograr menor error de generalización para un (m) fijo, o requerir menos ejemplos para un nivel dado).  
> En el caso paramétrico, la eficiencia se estudia midiendo cercanía al parámetro verdadero mediante el **MSE esperado del parámetro** (esperanza sobre (m) muestras de entrenamiento).  
> Para (m) grande, la **cota inferior de Cramér-Rao** (Rao, 1945; Cramér, 1946) muestra que ningún estimador consistente tiene un MSE menor que el de máxima verosimilitud.

#### 4. Implicación Práctica y Regularización con Pocos Datos

> Por consistencia y eficiencia, el material concluye que máxima verosimilitud suele considerarse el estimador preferido en _machine learning_.  
> Si el número de ejemplos es suficientemente pequeño como para inducir **sobreajuste**, se pueden usar estrategias de **regularización** (p. ej., _weight decay_) para obtener una versión **sesgada** de máxima verosimilitud con **menor varianza** cuando los datos de entrenamiento son limitados.

---

## DpL-IGF 6. Deep Feedforward Networks - Bernouilli & Multinouilli Ouptut Distribution

### I. Sigmoid Units for Bernoulli Output Distributions

#### 1. Problema: Predecir una Variable Binaria con una Distribución Bernoulli

> El material plantea el caso de tareas donde hay que predecir una variable binaria (y) (p. ej., clasificación con dos clases) y propone definir una **distribución Bernoulli** sobre (y) condicionada en (x).  
> Una Bernoulli queda determinada por un único número: la red solo necesita predecir (P(y=1\mid x)), que debe estar en ([0,1]).

#### 2. Por Qué No Usar una Unidad Lineal Recortada

> El texto considera usar una unidad lineal y **recortarla** para forzar una probabilidad válida:  
> [  
> P(y=1\mid x)=\max{0,\min{1,w^\top h+b}}.  
> ]  
> Aunque esto define una distribución condicional válida, el material advierte que entrenar con descenso por gradiente sería inefectivo: cuando (w^\top h+b) cae fuera de ([0,1]), el gradiente del output respecto a los parámetros se vuelve **0**, y el aprendizaje pierde señal para mejorar.

#### 3. Unidad Sigmoide y Variable Logit

> La alternativa recomendada es usar **salida sigmoide** junto con máxima verosimilitud:  
> [  
> \hat{y}=\sigma(w^\top h+b).  
> ]  
> El material descompone la operación en dos pasos: primero una capa lineal produce (z=w^\top h+b), luego la sigmoide convierte (z) en una probabilidad.  
> El texto motiva la sigmoide construyendo una distribución no normalizada (\tilde{P}(y)) con log-probabilidades lineales en (y) y (z), exponenciando y normalizando para obtener una Bernoulli controlada por una transformación sigmoidal de (z):  
> [  
> \log \tilde{P}(y)=yz,\quad \tilde{P}(y)=\exp(yz),\quad  
> P(y)=\frac{\exp(yz)}{\sum_{y'=0}^{1}\exp(y'z)},\quad  
> P(y)=\sigma((2y-1)z).  
> ]  
> El texto indica que las distribuciones basadas en “exponenciar y normalizar” son comunes en modelado estadístico, y que (z) (que define la distribución binaria) se denomina **logit**.

#### 4. Máxima Verosimilitud y Pérdida en Forma de Softplus

> El material subraya que esta parametrización en _log-space_ encaja de forma natural con máxima verosimilitud porque la pérdida (-\log P(y\mid x)) “deshace” el (\exp) asociado a la sigmoide.  
> Para una Bernoulli parametrizada con sigmoide, la pérdida de máxima verosimilitud queda:  
> [  
> J(\theta)=-\log P(y\mid x)  
> =-\log \sigma((2y-1)z)  
> =\zeta((1-2y)z),  
> ]  
> donde (\zeta) es la función **softplus** (usando propiedades citadas por el material).

#### 5. Saturación y Gradientes: Por Qué NLL Es Preferible a MSE

> Al reescribir la pérdida con softplus, el material explica que la saturación solo ocurre cuando ((1-2y)z) es muy negativo, es decir, **solo cuando el modelo ya acierta**:
> 
> - (y=1) y (z) muy positivo, o
>     
> - (y=0) y (z) muy negativo.  
>     Cuando (z) tiene el signo incorrecto, el argumento ((1-2y)z) se simplifica a (|z|); para (|z|) grande con signo incorrecto, softplus se aproxima a (|z|) y su derivada respecto a (z) se aproxima a (\mathrm{sign}(z)), por lo que **no reduce** el gradiente incluso si (z) es “extremadamente incorrecto”.  
>     El texto contrasta esto con usar otras pérdidas (p. ej., MSE): la pérdida puede saturar cada vez que (\sigma(z)) satura (hacia 0 o 1), haciendo que el gradiente se vuelva demasiado pequeño **tanto si el modelo acierta como si falla**. Por eso, el material afirma que máxima verosimilitud es “casi siempre” la opción preferida para entrenar salidas sigmoides.
>     

#### 6. Nota Numérica: Mejor Expresar la NLL en Función de (z)

> El material añade que (\log(\sigma(z))) está bien definido y es finito porque (\sigma(z)\in(0,1)) (intervalo abierto).  
> Aun así, en implementaciones software recomienda escribir la **log-verosimilitud negativa** como función de (z), no como función de (\hat{y}=\sigma(z)): si la sigmoide “underflow” a 0, entonces (\log \hat{y}) da (-\infty).

---

### II. Softmax Units for Multinoulli Output Distributions

#### 1. Cuándo Aparece Softmax y Qué Generaliza

> El material introduce softmax para representar una distribución sobre una variable discreta con (n) valores posibles, y lo presenta como una generalización de la sigmoide (usada para el caso binario).  
> Indica que softmax se usa principalmente como salida de un clasificador para modelar probabilidades sobre (n) clases, y más raramente dentro del modelo si se quiere que el modelo elija entre (n) opciones para alguna variable interna.

#### 2. De Bernoulli a Multinoulli: Vector de Probabilidades y Normalización

> En el caso binario se producía un único número (\hat{y}=P(y=1\mid x)) y se prefería predecir un logit (z=\log \tilde{P}(y=1\mid x)) para luego exponenciar y normalizar.  
> Para generalizar al caso con (n) valores, el modelo debe producir un vector (\hat{\mathbf{y}}) con (\hat{y}_i=P(y=i\mid x)), donde cada componente está en ([0,1]) y además (\sum_i \hat{y}_i=1).  
> El material aplica el mismo esquema: una capa lineal predice log-probabilidades no normalizadas y luego softmax exponencia y normaliza:  
> [  
> \mathbf{z}=W^\top h+b,\quad z_i=\log \tilde{P}(y=i\mid x),  
> ]  
> [  
> \mathrm{softmax}(\mathbf{z})_i=\frac{\exp(z_i)}{\sum_j \exp(z_j)}.  
> ]

#### 3. Log-Softmax y Por Qué Funciona Bien con Máxima Verosimilitud

> Para máxima log-verosimilitud con objetivo (y=i), se maximiza (\log P(y=i;\mathbf{z})=\log \mathrm{softmax}(\mathbf{z})_i).  
> El texto destaca que definir softmax con (\exp) es natural porque el (\log) del log-likelihood “deshace” ese (\exp):  
> [  
> \log \mathrm{softmax}(\mathbf{z})_i = z_i - \log \sum_j \exp(z_j).  
> ]  
> El material usa esta forma para argumentar sobre gradientes: el término (z_i) contribuye directamente al coste y **no puede saturar**, así que el aprendizaje puede progresar incluso si la contribución del segundo término se vuelve muy pequeña.  
> También da intuición del segundo término aproximando (\log \sum_j \exp(z_j)\approx \max_j z_j), y concluye que la NLL penaliza con fuerza la predicción incorrecta más “activa”. Si la clase correcta ya tiene el mayor (z), los términos se cancelan aproximadamente y el ejemplo aporta poco coste.

#### 4. Qué Aprende Softmax Bajo Máxima Verosimilitud Sin Regularizar

> El material afirma que, globalmente, la máxima verosimilitud sin regularizar empuja al modelo a que softmax prediga la fracción de cuentas observada en el training set (condicionada a (x)):  
> [  
> \mathrm{softmax}(\mathbf{z}(x;\theta))_i \approx  
> \frac{\sum_{j=1}^{m}\mathbf{1}_{y^{(j)}=i,\ x^{(j)}=x}}  
> {\sum_{j=1}^{m}\mathbf{1}_{x^{(j)}=x}}.  
> ]  
> Lo justifica diciendo que máxima verosimilitud es un estimador consistente si la familia de modelos puede representar la distribución de entrenamiento; en la práctica, capacidad limitada y optimización imperfecta hacen que solo se aproxime.

#### 5. Por Qué Otras Pérdidas (p. ej., MSE) Funcionan Peor con Softmax

> El texto señala que muchas funciones objetivo distintas de la log-verosimilitud no funcionan tan bien con softmax: si no usan un (\log) para “deshacer” el (\exp), cuando el argumento de (\exp) es muy negativo el gradiente puede desaparecer y el modelo deja de aprender.  
> En particular, el material afirma que el error cuadrático es una mala pérdida para unidades softmax y puede fallar incluso cuando el modelo hace predicciones incorrectas con alta confianza (citando Bridle, 1990).

#### 6. Saturación de Softmax y Variante Numéricamente Estable

> Como la sigmoide, softmax puede saturar, pero aquí la saturación depende de que las diferencias entre entradas se vuelvan extremas.  
> El material destaca una propiedad clave: softmax es invariante a sumar la misma constante a todos los inputs:  
> [  
> \mathrm{softmax}(\mathbf{z})=\mathrm{softmax}(\mathbf{z}+c).  
> ]  
> Con esa invariancia deriva una forma numéricamente estable:  
> [  
> \mathrm{softmax}(\mathbf{z})=\mathrm{softmax}(\mathbf{z}-\max_i z_i).  
> ]  
> Usando esta reformulación, el texto describe la saturación: un output (\mathrm{softmax}(\mathbf{z})_i) tiende a 1 cuando (z_i) es el máximo y está muy por encima del resto; y tiende a 0 cuando (z_i) no es máximo y el máximo es mucho mayor.

#### 7. Parametrización: Versión Sobreparametrizada vs. Restringida

> El material indica dos maneras de producir (\mathbf{z}): la más común es que una capa previa produzca todos los elementos de (\mathbf{z}) (p. ej., (\mathbf{z}=W^\top h+b)).  
> Señala que esto **sobreparametriza** la distribución: la restricción de que las probabilidades suman 1 implica que bastan (n-1) parámetros; se podría fijar un elemento, por ejemplo imponer (z_n=0).  
> También afirma que definir (P(y=1\mid x)=\sigma(z)) equivale a definir (P(y=1\mid x)=\mathrm{softmax}(\mathbf{z})_1) con un (\mathbf{z}) bidimensional y (z_1=0).  
> Ambas formulaciones describen el mismo conjunto de distribuciones pero con dinámicas de aprendizaje distintas; en la práctica suele haber poca diferencia y es más simple implementar la versión sobreparametrizada.

#### 8. Intuición Extra del Texto: Competencia y Nombre “Softmax”

> Desde un punto de vista neurocientífico, el material interpreta softmax como un mecanismo de “competencia” porque las salidas suman 1: subir una implica bajar otras, análogo a la inhibición lateral; en el extremo se vuelve tipo _winner-take-all_.  
> El texto comenta que el nombre puede confundir: está más relacionado con (\arg\max) que con (\max); “soft” viene de que softmax es continua y diferenciable, a diferencia de (\arg\max) (one-hot), y menciona que podría llamarse “softargmax”, pero el nombre actual es convención arraigada.


## D2DpL 3. Linear Neural Networks for Regression
### I. Redes Neuronales Lineales para Regresión

#### 1. Motivación y Alcance del Capítulo

> Antes de hacer redes “profundas”, el material propone implementar **redes poco profundas** donde las entradas conectan directamente con las salidas, para centrarse en lo esencial del entrenamiento: **parametrizar la capa de salida**, **manejar datos**, **definir una pérdida** y **entrenar**.  
> También justifica estudiar modelos lineales (p. ej., regresión lineal) porque son **métodos clásicos** muy usados como **baselines** al justificar arquitecturas más complejas.

#### 2. Problema de Regresión y Terminología

> La **regresión** busca predecir un **valor numérico** (ejemplos: precios de casas, stocks, demanda, etc.).  
> En terminología de ML:
> 
> - **Training Set**: dataset de entrenamiento.
>     
> - **Example / Sample**: cada fila.
>     
> - **Label / Target**: lo que se predice.
>     
> - **Features / Covariates**: variables de entrada usadas para predecir.
>     

#### 3. Supuestos y Notación

> Regresión lineal parte de supuestos: relación aproximadamente lineal entre features (x) y target (y), y desviaciones debidas a **ruido** (habitualmente modelado como Gaussiano).  
> Notación: (n) ejemplos; superíndices para enumerar ejemplos/targets; subíndices para coordenadas. En concreto, (x^{(i)}) es el ejemplo (i)-ésimo y (x^{(i)}_j) su coordenada (j).

#### 4. Modelo Lineal

> Para un ejemplo, el modelo es una función afín ( \hat{y} = w^\top x + b).  
> Para el dataset completo, se usa la **matriz de diseño** (X \in \mathbb{R}^{n \times d}) y las predicciones se expresan como:  
> [  
> \hat{y} = Xw + b \quad (3.1.4)  
> ]  
> donde al sumar un vector y un escalar se aplica **broadcasting**.

#### 5. Función de Pérdida y Objetivo

> La pérdida típica en regresión es el **error cuadrático** (squared error). Para un ejemplo (i):  
> [  
> l^{(i)}(w,b) = \frac{1}{2}(\hat{y}^{(i)} - y^{(i)})^2 \quad (3.1.5)  
> ]  
> La constante (1/2) es “conveniente” porque se cancela al derivar.  
> El error empírico medio sobre el training set:  
> [  
> L(w,b)=\frac{1}{n}\sum_{i=1}^{n} l^{(i)}(w,b)  
> =\frac{1}{n}\sum_{i=1}^{n}\frac{1}{2}(w^\top x^{(i)}+b-y^{(i)})^2 \quad (3.1.6)  
> ]  
> Objetivo de entrenamiento:  
> [  
> (w^*,b^*)=\arg\min_{w,b} L(w,b) \quad (3.1.7)  
> ]

#### 6. Solución Analítica (Normal Equation)

> En regresión lineal puede obtenerse una solución analítica (en training), derivando y anulando el gradiente:  
> [  
> \partial_w \lVert y - Xw\rVert^2 = 2X^\top(Xw-y)=0 \Rightarrow X^\top y = X^\top X w \quad (3.1.8)  
> ]  
> y por tanto:  
> [  
> w^*=(X^\top X)^{-1}X^\top y \quad (3.1.9)  
> ]  
> La unicidad requiere que (X^\top X) sea invertible (columnas de (X) linealmente independientes / full rank).  
> El material avisa: no hay que “acostumbrarse” a soluciones analíticas; en deep learning casi siempre entrenaremos con métodos iterativos.

#### 7. Descenso de Gradiente Estocástico por Minibatches

> El capítulo contrasta: **full-batch gradient descent** (lento porque requiere pasar por todo el dataset antes de cada update) vs **SGD** (un ejemplo por update, con inconvenientes computacionales/estadísticos).  
> Solución intermedia: **minibatches** (típicamente tamaño entre 32 y 256, preferiblemente múltiplo de una potencia de 2).  
> Regla de actualización (minibatch SGD):  
> [  
> (w,b)\leftarrow (w,b) - \eta \frac{1}{|B|}\sum_{i\in B_t}\partial_{(w,b)},l^{(i)}(w,b)\quad (3.1.10)  
> ]  
> Para pérdidas cuadráticas y transformaciones afines, el material da la expansión cerrada:  
> [  
> w \leftarrow w - \frac{\eta}{|B|}\sum_{i\in B_t} x^{(i)}(w^\top x^{(i)}+b-y^{(i)})  
> ]  
> [  
> b \leftarrow b - \frac{\eta}{|B|}\sum_{i\in B_t} (w^\top x^{(i)}+b-y^{(i)}) \quad (3.1.11)  
> ]  
> El texto introduce el término **hiperparámetros** para parámetros fijados por el usuario (p. ej., (\eta), (|B|)) y comenta que la calidad suele evaluarse en un **validation set** separado.

#### 8. Predicción y Generalización

> Tras entrenar, se usan (\hat{w},\hat{b}) para **predecir** etiquetas de ejemplos no vistos. El material recomienda usar “prediction” y advierte que “inference” se usa con significados distintos en otras literaturas, lo cual puede crear confusión.  
> El texto introduce **generalization** como el reto de predecir bien en datos no vistos.

#### 9. Vectorización para Velocidad

> Entrenar suele procesar **minibatches completos**: para ser eficiente hay que **vectorizar** y aprovechar librerías rápidas de álgebra lineal, evitando bucles `for` en Python.  
> El material muestra un microbenchmark sumando dos vectores (10k dims): un bucle tarda órdenes de magnitud más que `a + b`.  
> Beneficios mencionados: speedups de orden de magnitud, menos cálculos manuales, menos errores y más portabilidad.

#### 10. Distribución Normal y Pérdida Cuadrática

> El capítulo conecta regresión lineal con la **Normal/Gaussiana**. Define la densidad:  
> [  
> p(x)=\frac{1}{\sqrt{2\pi\sigma^2}}\exp\left(-\frac{1}{2\sigma^2}(x-\mu)^2\right)\quad (3.1.12)  
> ]  
> Asume un modelo de observación con ruido gaussiano:  
> [  
> y = w^\top x + b + \epsilon,\quad \epsilon\sim \mathcal{N}(0,\sigma^2)\quad (3.1.13)  
> ]  
> Con máxima verosimilitud, se minimiza el **negative log-likelihood**; si (\sigma) es fijo, la parte relevante queda proporcional al **squared error**, por lo que **minimizar MSE equivale a MLE** bajo ruido gaussiano aditivo.

#### 11. Regresión Lineal Como Red Neuronal

> El material representa la regresión lineal como una **red neuronal de una sola capa fully-connected**: cada feature es una neurona de entrada conectada al output.  
> Se menciona la Fig. 3.1.2: patrón de conectividad (no valores concretos de pesos/bias).

#### 12. Biología (Analogía)

> Se incluye una analogía con neuronas biológicas (Fig. 3.1.3): dendritas reciben inputs (x_i), sinapsis ponderan con (w_i), se agrega como suma ponderada (y=\sum_i x_i w_i + b), y puede aplicarse no linealidad (\sigma(y)).

---

### II. Diseño Orientado a Objetos para Implementación

#### 1. Idea General de la API

> El material propone una **arquitectura orientada a objetos** para estructurar implementaciones, porque los mismos componentes (data, modelo, pérdida, optimización) reaparecen continuamente.  
> Diseño a alto nivel: tres clases:
> 
> - `Module`: modelos, pérdidas y optimización.
>     
> - `DataModule`: data loaders (train/val).
>     
> - `Trainer`: combina ambos y ejecuta entrenamiento.
>     

#### 2. Utilidades para Notebooks: `add_to_class` y `HyperParameters`

> Problema en notebooks: las definiciones de clases largas dañan la legibilidad; solución: añadir métodos a una clase después de definirla con un decorador `add_to_class`.  
> `HyperParameters` guarda argumentos de `__init__` como atributos mediante `save_hyperparameters(...)` (implementación diferida a una sección posterior).  
> Se muestra que puede ignorar ciertos argumentos (`ignore=[...]`).

#### 3. Clase `Module`

> `Module` (base de modelos) requiere, como mínimo: almacenar parámetros en `__init__`, un `training_step` que devuelve pérdida para un batch, y `configure_optimizers` que devuelve el optimizador; opcionalmente `validation_step`.  
> Es subclase de `nn.Module`; llamar `a(X)` invoca `forward` vía `__call__`.

#### 4. Clase `DataModule`

> `DataModule` encapsula preparación/lectura de datos: `train_dataloader` y `val_dataloader` devuelven generadores de batches; `get_dataloader(train)` define el comportamiento.

#### 5. Clase `Trainer`

> `Trainer.fit(model, data)` itera `max_epochs` y coordina: preparar datos, preparar modelo y ejecutar el loop por épocas (la implementación se va enriqueciendo más adelante).  
> En el resumen se remarca que las implementaciones completas se guardan en la librería D2L para favorecer modularidad (cambiar optimizador/modelo/dataset sin reescribir todo).

---

### III. Datos Sintéticos para Regresión

#### 1. Por Qué Usar Datos Sintéticos

> Aunque no importen “intrínsecamente” los patrones artificiales, sirven para docencia: evaluar algoritmos y verificar que la implementación recupera parámetros conocidos a priori.

#### 2. Generación del Dataset

> Se generan (1000) ejemplos con (2) features (X \in \mathbb{R}^{1000\times 2}) muestreadas de una normal estándar, y labels con:  
> [  
> y = Xw + b + \epsilon \quad (3.3.1)  
> ]  
> con (\epsilon\sim \mathcal{N}(0, 0.01^2)).  
> Se implementa como `SyntheticRegressionData`, subclase de `d2l.DataModule`, guardando hiperparámetros con `save_hyperparameters()`.

```python
class SyntheticRegressionData(d2l.DataModule): #@save
    """Synthetic data for linear regression."""
    def __init__(self, w, b, noise=0.01, num_train=1000, num_val=1000,
                 batch_size=32):
        super().__init__()
        self.save_hyperparameters()
        n = num_train + num_val
        self.X = torch.randn(n, len(w))
        noise = torch.randn(n, 1) * noise
        self.y = torch.matmul(self.X, w.reshape((-1, 1))) + b + noise
```

#### 3. Lectura del Dataset y Minibatches

> Entrenar requiere múltiples pasadas; se implementa `get_dataloader(train)` que: en train **baraja índices** y en valid usa un orden determinista, y va devolviendo minibatches `(X_batch, y_batch)`.

```python
@d2l.add_to_class(SyntheticRegressionData)
def get_dataloader(self, train):
    if train:
        indices = list(range(0, self.num_train))
        random.shuffle(indices)
    else:
        indices = list(range(self.num_train, self.num_train + self.num_val))
    for i in range(0, len(indices), self.batch_size):
        batch_indices = torch.tensor(indices[i: i + self.batch_size])
        yield self.X[batch_indices], self.y[batch_indices]
```

#### 4. Data Loader Conciso con API del Framework

> La iteración manual es didáctica pero ineficiente (carga en memoria + accesos aleatorios). Se propone usar `TensorDataset` + `DataLoader` y encapsularlo en `get_tensorloader(...)`, más eficiente y con utilidades extra como `__len__`.

```python
@d2l.add_to_class(d2l.DataModule) #@save
def get_tensorloader(self, tensors, train, indices=slice(0, None)):
    tensors = tuple(a[indices] for a in tensors)
    dataset = torch.utils.data.TensorDataset(*tensors)
    return torch.utils.data.DataLoader(dataset, self.batch_size, shuffle=train)

@d2l.add_to_class(SyntheticRegressionData) #@save
def get_dataloader(self, train):
    i = slice(0, self.num_train) if train else slice(self.num_train, None)
    return self.get_tensorloader((self.X, self.y), train, i)
```

---

### IV. Implementación de Regresión Lineal desde Cero

#### 1. Definición del Modelo y Parámetros

> Se define `LinearRegressionScratch` como subclase de `d2l.Module`. Inicializa:
> 
> - (w\sim \mathcal{N}(0,\sigma^2)) con (\sigma=0.01) por defecto.
>     
> - (b=0).
>     
> - Ambos con `requires_grad=True`.  
>     El forward implementa (Xw + b) y usa broadcasting al sumar el escalar (b) al vector.
>     

```python
class LinearRegressionScratch(d2l.Module): #@save
    """The linear regression model implemented from scratch."""
    def __init__(self, num_inputs, lr, sigma=0.01):
        super().__init__()
        self.save_hyperparameters()
        self.w = torch.normal(0, sigma, (num_inputs, 1), requires_grad=True)
        self.b = torch.zeros(1, requires_grad=True)

@d2l.add_to_class(LinearRegressionScratch) #@save
def forward(self, X):
    return torch.matmul(X, self.w) + self.b
```

#### 2. Definición de la Pérdida

> Se usa squared loss (3.1.5). En la implementación se ajusta la forma de (y) para que coincida con (y_{\hat{}}) y se devuelve la pérdida media del minibatch.

```python
@d2l.add_to_class(LinearRegressionScratch) #@save
def loss(self, y_hat, y):
    l = (y_hat - y) ** 2 / 2
    return l.mean()
```

#### 3. Algoritmo de Optimización: SGD

> Aunque regresión lineal tenga solución cerrada, aquí se usa minibatch SGD para enseñar el patrón general de entrenamiento de redes.  
> Como la pérdida es media sobre minibatch, el material indica que no hace falta ajustar el learning rate por batch size en esta implementación.  
> Se define una clase `SGD` con `step()` y `zero_grad()` (poner gradientes a cero antes del backprop).

```python
class SGD(d2l.HyperParameters): #@save
    """Minibatch stochastic gradient descent."""
    def __init__(self, params, lr):
        self.save_hyperparameters()
    def step(self):
        for param in self.params:
            param -= self.lr * param.grad
    def zero_grad(self):
        for param in self.params:
            if param.grad is not None:
                param.grad.zero_()

@d2l.add_to_class(LinearRegressionScratch) #@save
def configure_optimizers(self):
    return SGD([self.w, self.b], self.lr)
```

#### 4. Entrenamiento: Bucle por Épocas

> En cada epoch se recorre el train dataloader completo (pasar una vez por todos los ejemplos, asumiendo divisibilidad por batch size). En cada iteración: calcular pérdida, backprop, update.  
> El material registra `prepare_batch` y `fit_epoch` en `d2l.Trainer`; también pasa por validación una vez por epoch si hay `val_dataloader`.  
> Se menciona que (\text{lr}) y `max_epochs` son hiperparámetros, y que “en general” conviene un split en tres partes (train / selección de hiperparámetros / evaluación final), aunque aquí se omite por simplicidad.

```python
@d2l.add_to_class(d2l.Trainer) #@save
def prepare_batch(self, batch):
    return batch

@d2l.add_to_class(d2l.Trainer) #@save
def fit_epoch(self):
    self.model.train()
    for batch in self.train_dataloader:
        loss = self.model.training_step(self.prepare_batch(batch))
        self.optim.zero_grad()
        with torch.no_grad():
            loss.backward()
            if self.gradient_clip_val > 0:
                self.clip_gradients(self.gradient_clip_val, self.model)
            self.optim.step()
        self.train_batch_idx += 1
    if self.val_dataloader is None:
        return
    self.model.eval()
    for batch in self.val_dataloader:
        with torch.no_grad():
            self.model.validation_step(self.prepare_batch(batch))
        self.val_batch_idx += 1
```

#### 5. Evaluación Cualitativa (Parámetros Verdaderos vs Aprendidos)

> Como los datos son sintéticos, se conocen los parámetros verdaderos; se propone comparar con los aprendidos para verificar que el entrenamiento “recupera” valores cercanos.  
> El material matiza: en general (y más aún en modelos profundos) no suele haber soluciones únicas; en ML importa más predecir bien que recuperar “parámetros verdaderos”.

---

### V. Implementación Concisa de Regresión Lineal

#### 1. Motivación: APIs de Alto Nivel

> El material atribuye parte del “boom” del deep learning a herramientas open-source y a frameworks modernos (autodiferenciación + conveniencia de Python) que automatizan componentes repetitivos (data iterators, losses, optimizers, layers).

#### 2. Modelo con Capas Predefinidas

> Para operaciones estándar se usa una capa fully-connected predefinida (en PyTorch: `Linear`/`LazyLinear`). El texto recomienda `LazyLinear` para evitar especificar shapes de entrada.  
> `LinearRegression` usa `nn.LazyLinear(1)` y fija inicialización: pesos (\sim \mathcal{N}(0, 0.01)), bias a 0.

```python
class LinearRegression(d2l.Module): #@save
    """The linear regression model implemented with high-level APIs."""
    def __init__(self, lr):
        super().__init__()
        self.save_hyperparameters()
        self.net = nn.LazyLinear(1)
        self.net.weight.data.normal_(0, 0.01)
        self.net.bias.data.fill_(0)

@d2l.add_to_class(LinearRegression) #@save
def forward(self, X):
    return self.net(X)
```

#### 3. Pérdida con `MSELoss`

> `MSELoss` computa MSE (sin el factor (1/2) de (3.1.5)) y por defecto promedia sobre ejemplos; el material dice que es más rápido y más fácil que implementarla a mano.

```python
@d2l.add_to_class(LinearRegression) #@save
def loss(self, y_hat, y):
    fn = nn.MSELoss()
    return fn(y_hat, y)
```

#### 4. Optimización con `torch.optim.SGD`

> Para optimizar se instancia `torch.optim.SGD` sobre `self.parameters()` y el learning rate.

```python
@d2l.add_to_class(LinearRegression) #@save
def configure_optimizers(self):
    return torch.optim.SGD(self.parameters(), self.lr)
```

#### 5. Entrenamiento

> El material recalca que, aunque el modelo y componentes auxiliares se simplifican, el **training loop** sigue la misma estructura (se llama a `fit`, apoyándose en `fit_epoch`).

---

### VI. Generalización

#### 1. Error de Entrenamiento y Error de Generalización

> En aprendizaje supervisado estándar, el material asume que datos de **entrenamiento** y **test** se extraen de manera independiente de la **misma distribución** (supuesto **IID**). Sin este tipo de supuesto, no habría base para extrapolar de (P(X,Y)) a otra distribución (Q(X,Y)).
> 
> Diferencia clave:
> 
> - **Error de entrenamiento** (R_{\text{emp}}): estadístico calculado sobre el dataset de entrenamiento.
>     
> - **Error de generalización** (R): **esperanza** respecto a la distribución subyacente (P); intuitivamente, lo que verías sobre un “flujo infinito” de datos nuevos de la misma distribución.
>     
> 
> Definiciones formales (misma notación que en la Sección 3.1):  
> [  
> R_{\text{emp}}[X,y,f] = \frac{1}{n}\sum_{i=1}^{n} l\big(x^{(i)}, y^{(i)}, f(x^{(i)})\big) \quad (3.6.1)  
> ]  
> [  
> R[p,f] = \mathbb{E}_{(x,y)\sim P},[l(x,y,f(x))] = \int!!\int l(x,y,f(x)),p(x,y),dx,dy \quad (3.6.2)  
> ]
> 
> Problema práctico: **no podemos calcular (R) exactamente** (no conocemos (p(x,y)) y no podemos muestrear infinitos datos). Por eso se estima aplicando el modelo a un **test set independiente** (o conjunto retenido) usando la misma fórmula que para el error empírico.
> 
> Matiz importante: al evaluar en test, el clasificador/modelo se considera **fijo** (no depende de la muestra de test), así que estimar su error es “solo” un problema de **estimar una media**; en cambio, el modelo sí depende del training set, y por eso el training error suele ser un **estimador sesgado** del error poblacional.

#### 2. Complejidad del Modelo y Por Qué el Training Error No Basta

> En teoría “clásica”, con modelos simples y datos abundantes, training y generalization tienden a estar cerca; con modelos más complejos y/o menos datos, esperas que el training error baje pero que crezca el **generalization gap**.
> 
> Caso extremo: si tu clase de modelos puede ajustar **etiquetas arbitrarias** (incluso aleatorias), entonces encajar perfecto el training set no te permite concluir nada fiable sobre generalización (podrías estar cerca de “adivinar al azar” fuera de muestra).
> 
> Mensaje fuerte del material: **bajo training error no implica necesariamente bajo error de generalización**, pero tampoco implica necesariamente que generalice mal; lo único seguro es que el training error por sí solo **no certifica** generalización. En modelos muy potentes (menciona deep nets), hay que apoyarse más en datos retenidos; el error sobre holdout/validation se llama **validation error**.
> 
> Sobre “qué es complejidad”: no es trivial. A veces más parámetros ⇒ más capacidad de ajustar etiquetas arbitrarias, pero no siempre (ej.: kernel methods con infinitos parámetros controlados por otros medios). Una noción útil es el **rango de valores** que pueden tomar los parámetros.
> 
> El material conecta esto con la idea de **falsabilidad** (Popper): una hipótesis que explica “cualquier cosa” no informa realmente sobre el mundo; preferimos hipótesis que podrían fallar en principio pero que aun así encajan los datos observados.

#### 3. Underfitting u Overfitting

> Al comparar **training error** vs **validation error**, el material destaca dos situaciones comunes:
> 
> - **Underfitting**: training y validation son ambos altos, con **poca brecha**. Si el modelo no logra bajar el training error, suele indicar que es demasiado **simple / poco expresivo**; como el gap ((R_{\text{emp}}-R)) es pequeño, “podrías permitirte” un modelo más complejo.
>     
> - **Overfitting**: training mucho más bajo que validation, indicando un gap grande.
>     
> 
> Matiz del material: overfitting **no siempre es “malo”**; a menudo (especialmente en deep learning) los mejores modelos predicen mucho mejor en training que en holdout. Lo importante es bajar el **error de generalización**; el gap importa en la medida en que impida ese objetivo. Si el training error es 0, entonces el gap coincide exactamente con el error de generalización y solo avanzas reduciendo el gap.

#### 4. Ajuste de Curvas Polinómicas Como Ejemplo

> Para ilustrar intuición clásica sobre complejidad y overfitting, el material propone **regresión polinómica** con una sola feature (x):  
> [  
> \hat{y}=\sum_{i=0}^{d} x^i w_i \quad (3.6.3)  
> ]
> 
> Interpretación: es regresión lineal donde las features son (x^i), los pesos son (w_i) y el sesgo es (w_0) porque (x^0=1). Se puede usar squared error como loss.
> 
> Relación grado–complejidad: un polinomio de mayor grado es más complejo (más parámetros y mayor “rango de selección” de funciones). Con el training set fijo, aumentar el grado no empeora el training error (como mucho lo deja igual). Además, si cada ejemplo tiene un (x) distinto, un polinomio con grado igual al número de ejemplos puede ajustar el training set perfectamente.

#### 5. Tamaño del Dataset

> A igualdad de modelo: con **menos muestras** es más probable (y más severo) el overfitting; al aumentar datos, típicamente baja el error de generalización, y “en general, más datos nunca perjudican”.
> 
> Regla cualitativa del material: para una tarea y distribución fijadas, la complejidad del modelo no debería crecer más rápido que la cantidad de datos; con más datos puedes intentar modelos más complejos, pero sin datos suficientes es difícil batir modelos simples. Menciona que en muchas tareas deep learning supera a modelos lineales cuando hay **muchos miles** de ejemplos, y atribuye parte del éxito actual a la disponibilidad de datasets masivos.

#### 6. Selección de Modelos

> En la práctica, se elige el modelo final tras comparar varios que difieren en arquitectura, objetivo, features, preprocesado, learning rates, etc.; a esto se le llama **model selection**.
> 
> Principio: **no se debe tocar el test set** hasta haber fijado todos los hiperparámetros; si lo usas para seleccionar, puedes “sobreajustar el test” y entonces pierdes el árbitro final.
> 
> Pero tampoco basta con training para seleccionar, porque no puedes estimar generalización sobre los mismos datos con los que entrenas. Por eso se introduce un **validation set** adicional (split en tres: train/val/test).
> 
> Nota práctica del material: en el mundo real el test se reutiliza con frecuencia, y las fronteras entre validation y test pueden volverse ambiguas. En los experimentos del libro (si no se dice lo contrario), en realidad se trabaja con **training + validation**, sin “true test set”; por tanto, la “accuracy” reportada es realmente **validation accuracy**, no test accuracy.

#### 7. Validación Cruzada

> Si el training data es escaso y no puedes reservar suficiente validation, una solución popular es **(K)-fold cross-validation**:
> 
> - dividir el training original en (K) subconjuntos no solapados
>     
> - repetir (K) veces: entrenar con (K-1) folds y validar en el fold restante
>     
> - estimar training y validation errors promediando sobre los (K) experimentos
>     

#### 8. Resumen de la Sección

> Reglas “de pulgar” que deja el material:
> 
> 1. Usar validation sets (o (K)-fold cross-validation) para model selection.
>     
> 2. Modelos más complejos suelen requerir más datos.
>     
> 3. Nociones relevantes de complejidad incluyen número de parámetros **y** el rango de valores permitidos.
>     
> 4. Manteniendo lo demás igual, más datos casi siempre mejoran generalización.
>     
> 5. Todo este discurso presupone el supuesto IID; si hay shift entre train y test, no puedes decir nada sin suposiciones adicionales.
>     

#### 9. Ejercicios Propuestos

> El material propone, entre otros: cuándo se puede resolver exactamente regresión polinómica; ejemplos donde IID no aplica; cuándo esperar training error 0 o generalization error 0; por qué (K)-fold es caro y por qué su estimación puede estar sesgada; y reflexiones sobre VC dimension como medida de complejidad.

---

### VII. Decaimiento de Pesos

#### 1. Actualización con Penalización (\ell_2) y “Weight Decay”

> El material contrasta (\ell_2) vs (\ell_1): las penalizaciones (\ell_1) tienden a concentrar pesos en pocas features (selección de variables), mientras que (\ell_2) “encoge” pesos de forma continua.  
> Para regresión con regularización (\ell_2), da el update de SGD:  
> [  
> w \leftarrow (1-\eta\lambda)w - \frac{\eta}{|B|}\sum_{i\in B} x^{(i)}(w^\top x^{(i)}+b-y^{(i)})\quad (3.7.3)  
> ]  
> Interpretación del texto: además del término de ajuste por error, se **reduce** (w) hacia 0, de ahí el nombre **weight decay**. (\lambda) controla la fuerza de la restricción: menor (\lambda) → menos constrain; mayor (\lambda) → más constrain.  
> Se comenta que regularizar el bias puede variar; a menudo no se regulariza.

#### 2. Ejemplo Sintético de Alta Dimensión

> Se ilustra el beneficio con un caso sintético:  
> [  
> y = 0.05 + \sum_{i=1}^{d} 0.01 x_i + \epsilon,\quad \epsilon\sim \mathcal{N}(0,0.01^2)\quad (3.7.4)  
> ]  
> El ejemplo fuerza overfitting aumentando dimensionalidad a (d=200) y usando un training set pequeño (20 ejemplos).

```python
class Data(d2l.DataModule):
    def __init__(self, num_train, num_val, num_inputs, batch_size):
        self.save_hyperparameters()
        n = num_train + num_val
        self.X = torch.randn(n, num_inputs)
        noise = torch.randn(n, 1) * 0.01
        w, b = torch.ones((num_inputs, 1)) * 0.01, 0.05
        self.y = torch.matmul(self.X, w) + b + noise
    def get_dataloader(self, train):
        i = slice(0, self.num_train) if train else slice(self.num_train, None)
        return self.get_tensorloader([self.X, self.y], train, i)
```

#### 3. Contenido Parcial del Resto de la Sección

> El fragmento recuperado indica que después se aborda la “Implementation from Scratch” añadiendo la penalización (\ell_2) a la pérdida original, pero **no dispongo aquí del texto completo** para detallarlo paso a paso.

---

### VIII. Checklist de Verificación

#### 1. Lo Que Deberías Poder Hacer Tras Este Fragmento

> - Formular el modelo ( \hat{y}=w^\top x + b ) y su forma matricial ( \hat{y}=Xw+b ).
>     
> - Escribir y justificar la squared loss (3.1.5) y el objetivo empírico (3.1.6–3.1.7).
>     
> - Derivar/interpretar la solución analítica (3.1.8–3.1.9) y su condición de full rank.
>     
> - Explicar minibatch SGD y escribir updates (3.1.10–3.1.11).
>     
> - Justificar por qué vectorizar acelera (benchmark bucle vs `a + b`).
>     
> - Explicar la equivalencia MSE ↔ MLE bajo ruido gaussiano.
>     
> - Implementar (o entender) `SyntheticRegressionData`, `LinearRegressionScratch` y la versión concisa con `LazyLinear`, `MSELoss`, `torch.optim.SGD`.
>     
> - Interpretar “weight decay” como encogimiento de (w) y reconocer el update (3.7.3).
>     

---
