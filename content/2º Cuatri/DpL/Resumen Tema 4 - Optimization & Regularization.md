### I. Optimization Algorithms

#### 1. Fundamentos y Motivación de la Optimización
> En deep learning, **optimizar** no significa solo reducir la pérdida en entrenamiento, sino hacerlo de forma que el modelo también **generalice bien** a datos no vistos. Por eso hay que distinguir entre:
> - **Error de entrenamiento / riesgo empírico**: pérdida media sobre el conjunto de entrenamiento.
> - **Error de generalización / riesgo**: pérdida esperada sobre la distribución real de los datos.
> 
> El mínimo del riesgo empírico no tiene por qué coincidir con el mínimo del riesgo real, así que minimizar muy bien la loss de entrenamiento no garantiza el mejor rendimiento en validación o test.
> 
> Uno de los principales problemas al optimizar redes profundas es el de los **vanishing gradients**.  
> Cuando las derivadas se vuelven muy pequeñas durante backpropagation, las actualizaciones de los pesos casi desaparecen y el aprendizaje se ralentiza o incluso se detiene. Esto ocurre especialmente con activaciones saturables como `tanh`, cuya derivada: $f'(x)=1-\tanh^2(x)$ se aproxima a cero para valores grandes de $x$.
> 
> La idea básica del **gradient descent** parte de una aproximación de Taylor. En una dimensión, si queremos minimizar una función $f:\mathbb{R}\to\mathbb{R}$, actualizamos: $x \leftarrow x - \eta f'(x)$ donde $\eta$ es la **learning rate**. En varias dimensiones, para una función $f:\mathbb{R}^d\to\mathbb{R}$, la regla pasa a ser: $\mathbf{x} \leftarrow \mathbf{x} - \eta \nabla f(\mathbf{x})$ con: $$\nabla f(\mathbf{x})= \left[\frac{\partial f}{\partial x_1}, \frac{\partial f}{\partial x_2}, \dots, \frac{\partial f}{\partial x_d} \right]^T$$El gradiente marca la dirección de máximo crecimiento, así que $-\nabla f(\mathbf{x})$ define la dirección de descenso más pronunciado.
> 
> El **learning rate** controla el tamaño del paso:
> - Si es **demasiado pequeña**, la convergencia es muy lenta.
> - Si es **demasiado grande**, el algoritmo puede oscilar o divergir.
> - Si está bien ajustada, el descenso es estable y eficiente.
> 
> Otro problema importante es que en funciones **no convexas** puede haber muchos mínimos locales. En ese caso, el punto al que llega el algoritmo depende de la inicialización y de la learning rate. En deep learning esto es habitual, porque las funciones objetivo suelen ser altamente no convexas.
> 
> Para mejorar el descenso básico aparecen los **métodos adaptativos** y de **segundo orden**. La motivación es que una learning rate fija no siempre funciona bien en todas las direcciones del espacio de parámetros.
> 
> En métodos de segundo orden se usa: $$f(\mathbf{x}+\epsilon)=f(\mathbf{x})+\epsilon^{\top}\nabla f(\mathbf{x}) +\frac{1}{2}\epsilon^{\top}H\epsilon+O(|\epsilon|^3)$$ donde la $H$ es la matriz Hessiana $\mathbf{H}=\nabla^2 f(\mathbf{x})$ y se actualiza como $\mathbf{x}\leftarrow \mathbf{x}-H^{-1}\nabla f(\mathbf{x})$.
> 
> Este enfoque incorpora información de curvatura y puede acelerar la convergencia, pero tiene problemas:
> - Calcular e invertir la Hessiana es costoso.
> - En funciones no convexas, una Hessiana con curvatura negativa puede llevar a pasos incorrectos.
> 
> Para aliviar esto se plantean estrategias como usar una versión amortiguada con learning rate, modificar la Hessiana para evitar inversiones problemáticas, usar solo su diagonal como **preconditioning**: $$\mathbf{x} \leftarrow \mathbf{x} - \eta \ \text{diag}(\mathbf{H})^{-1}\nabla f(\mathbf{x})$$
> En resumen, la optimización en deep learning busca encontrar buenos parámetros minimizando una función de pérdida, pero debe enfrentarse a dificultades como gradientes que desaparecen, mínimos locales, curvaturas complicadas y el desajuste entre entrenamiento y generalización. Por eso los algoritmos de optimización son una pieza central del entrenamiento de redes profundas.
#### 2. Regular Types of Gradient Descents
> - **Gradient Descent (GD)**  
> En Gradient Descent, la función objetivo se define como el promedio de las pérdidas sobre todo el dataset de entrenamiento: $$f(\mathbf{x})=\frac{1}{n}\sum_{i=1}^{n} f(\mathbf{x}_i)$$y su gradiente se calcula como: $$\nabla f(\mathbf{x})=\frac{1}{n}\sum_{i=1}^{n}\nabla f(\mathbf{x}_i)$$Esto implica que cada actualización requiere recorrer todos los ejemplos, con un coste computacional $O(n)$ por iteración. Para datasets grandes, este coste puede resultar intratable.
> 
> - **Stochastic Gradient Descent (SGD)**  
> SGD reduce el coste aproximando el gradiente completo con el gradiente de una sola muestra. Su regla de actualización es: $$\mathbf{x}\leftarrow \mathbf{x}-\eta \nabla f(\mathbf{x}_i)$$donde:
> - $i \in {1,\dots,n}$ se elige uniformemente al azar.
> - $\eta$ es la learning rate.
> 
> Su coste computacional pasa a ser $O(1)$. Además, el gradiente estocástico es un estimador insesgado del gradiente completo: $$\mathbb{E}_i \nabla f(\mathbf{x}_i)=\frac{1}{n}\sum_{i=1}^{n}\nabla f(\mathbf{x}_i)=\nabla f(\mathbf{x})$$
> - **Mini-Batch Gradient Descent (MBGD)**  
> Aunque SGD es insesgado, puede necesitar demasiadas iteraciones. Para equilibrar coste y estabilidad, se usa un subconjunto o batch de muestras: $$\mathbf{x}\leftarrow \mathbf{x}-\eta \frac{1}{|\mathcal{B}_t|}\sum_{i\in |\mathcal{B}_t|}\nabla f(\mathbf{x}_i)$$donde $\mathcal{B}_t$ es el batch usado en la iteración $t$
> 
> El coste computacional es: $O(b) \ \text{con } b \ll n$ por lo que MBGD queda en mitad entre GD y SGD:
> - **GD:** usa todo el dataset, trayectoria más estable.
> - **SGD:** usa una sola muestra, trayectoria más ruidosa.
> - **MBGD:** usa un lote pequeño, combinando eficiencia y mayor estabilidad que SGD.
#### 3. Momentum
> En SGD y MBGD los gradientes pueden ser ruidosos. Si la learning rate disminuye demasiado rápido, la convergencia se frena; si disminuye demasiado poco, el ruido puede alejar la optimización del óptimo. La idea de _momentum_ es usar el historial de gradientes para suavizar la trayectoria y hacer el proceso más estable.
> 
> **Promedio con memoria (leaky average)**  
> En minibatch SGD, el gradiente en la iteración $t$ se estima como: $$g_{t,t-1}=\frac{1}{|\mathcal{B}_t|}\sum_{i\in \mathcal{B}_t}\partial_w f(x_i,w_{t-1}) = \frac{1}{|\mathcal{B}_t|}\sum_{i\in \mathcal{B}_t} h_{i,t-1}$$donde $\mathcal{B}_t$ es el minibatch en la iteración $t$, y $g_{t,t-1}$ es el gradiente promedio sobre ese batch.
> Para introducir memoria, se define una **velocidad**: $$v_t=\beta v_{t-1}+g_{t,t-1}$$donde:
> - $\beta \in (0,1)$ controla cuánto peso tienen los gradientes pasados.
> - $v_t$ acumula el historial de gradientes.
> 
> **Interpretación de la velocidad**  
> Si se desarrolla recursivamente: $$v_t=\beta^2 v_{t-2}+\beta g_{t-1,t-2}+g_{t,t-1} = \cdots = \sum_{\tau=0}^{t-1}\beta^\tau g_{t-\tau,t-\tau-1}$$Así, $v_t$ actúa como un promedio ponderado de gradientes pasados:
> - **$\beta$ grande**: promedio a más largo plazo.
> - **$\beta$ pequeño**: corrección más cercana a gradient descent estándar.
> 
> **Beneficios de Momentum**
> - *Mayor estabilidad en la dirección de descenso*: suaviza gradientes ruidosos y evita trayectorias demasiado erráticas.
> - *Mejor comportamiento en problemas mal condicionados*: resulta útil cuando distintas direcciones del espacio de parámetros progresan a velocidades muy diferentes, como en valles estrechos.
> - *Convergencia más rápida*: puede acelerar la optimización incluso en problemas convexos sin ruido.
> 
> **Problemas mal condicionados**  
> En valles estrechos, el gradiente transversal a las paredes puede ser mucho mayor que el gradiente en la dirección útil de descenso. Esto hace que la elección de learning rate sea muy sensible. 
> ![[Pasted image 20260319111437.png]]
> El ejemplo: $f(x)=0.1x_1^2+2x_2^2$  muestra precisamente este comportamiento: con ciertos valores de $\eta$ el método puede oscilar o incluso divergir. Momentum ayuda a amortiguar estas oscilaciones y a avanzar de forma más consistente hacia el mínimo.
> 
> **Método de Momentum**  
> Momentum ajusta la actualización de parámetros acumulando información de gradientes pasados en una variable de **velocidad**.
> La intuición es:
> - en direcciones donde los gradientes están bien alineados, **amplifica** el avance;
> - en direcciones donde los gradientes oscilan, **suaviza** esas oscilaciones y reduce el zigzag.
> 
> Sigue las siguientes ecuaciones: $$\mathbf{v_t \leftarrow \rho v_{t-1} - \eta_t g_{t,t-1}, \qquad x_t \leftarrow x_{t-1} + v_t}$$​donde:
> - $v_t$ es la velocidad, que acumula información histórica del gradiente
> - $g_{t,t-1}$​ es el gradiente en la iteración $t$
> - $\rho \in [0,1)$ es el factor de momentum
> - $\eta_t$ es el: learning rate en la iteración $t$
> 
> En el caso especial si $\rho = 0$ el método se reduce a descenso por gradiente estándar: $$x_t \leftarrow x_{t-1} - \eta_t g_{t,t-1}$$Se puede interpretar de forma práctica de la siguiente manera:
> - Si los gradientes apuntan repetidamente en una misma dirección, la velocidad crece y el método avanza más rápido.
> - Si los gradientes cambian de signo entre iteraciones, la acumulación amortigua la oscilación.
>
> Por lo tanto, Momentum puede verse como una extensión de gradient descent que introduce inercia en la trayectoria de optimización, haciendo el descenso más estable y más rápido en muchos problemas.
#### 4. Nesterov Accelerated Gradient
> **NAG** es una variante de _momentum_ que mejora la actualización usando una estimación “anticipada” de la posición futura del parámetro.
> 
> El *problema del momentum estándar* es que los parámetros se actualizan usando la velocidad acumulada. Sin embargo, el gradiente se calcula en la posición actual $x_{t-1}$​ sin tener en cuenta completamente el efecto de esa velocidad.
> Por eso la *idea principal de Nesterov* es que en lugar de evaluar el gradiente en $x_{t-1}$ se evalúa en una posición adelantada: $x_{t-1} + \rho v_{t-1}$. Así, el método “mira hacia delante” antes de corregir la trayectoria. Esto permite actualizaciones más informadas que el momentum clásico.
> 
> *Actualización de momentum estándar* $$v_t \leftarrow \rho v_{t-1} - \eta_t \nabla f(x_{t-1}), \qquad x_t \leftarrow x_{t-1} + v_t$$​*Actualización de Nesterov* $$v_t \leftarrow \rho v_{t-1} - \eta_t \nabla f(x_{t-1} + \rho v_{t-1}), \qquad x_t \leftarrow x_{t-1} + v_t$$​
> 
> La interpretación es que primero se estima hacia dónde empuja el momentum, después se calcula el gradiente en esa posición adelantada, y finalmente se corrige la actualización con esa información.
> 
> *Comparación con momentum*
> - **Momentum estándar**: calcula el gradiente en la posición actual.
> - **Nesterov**: calcula el gradiente en la posición “lookahead”.
> Por ello, Nesterov suele anticipar mejor la trayectoria de descenso, ya que con Momentum acumula inercia y añade una corrección anticipada sobre esa inercia.
#### 5. Adagrad
> **Adagrad** es un método de optimización adaptativo que ajusta la tasa de aprendizaje de cada parámetro de forma independiente a partir del historial de gradientes cuadrados acumulados.
> 
> Su *idea principal* es ir acumulando la magnitud de los gradientes al cuadrado para cada coordenada. Los parámetros que han recibido gradientes grandes muchas veces reducen su paso de actualización. Los parámetros con gradientes pequeños conservan una tasa de aprendizaje relativamente mayor.
> 
> La *acumulación del estado* es:  $$s(i,t+1)=s(i,t)+(\partial_i f(x))^2$$o, de forma vectorial: $$s_t=s_{t-1}+g_t^2$$ donde $s_t$ almacena la suma acumulada de gradientes cuadrados.
> 
> La *regla de actualización* es: $$x_t=x_{t-1}-\frac{\eta}{\sqrt{s_t}+\epsilon}\cdot g_t$$donde cada coordenada $x_i$ se actualiza con su propia tasa de aprendizaje efectiva y $\epsilon>0$ es una constante pequeña para evitar divisiones por cero.
> 
> *Ventaja en sparse features*
> - En problemas con _sparse features_, algunas características aparecen con mucha frecuencia y otras muy pocas veces.
> - Adagrad reduce el paso en coordenadas con gradientes grandes y frecuentes.
> - Mantiene pasos relativamente mayores en coordenadas con gradientes pequeños o infrecuentes.
> - Así equilibra el aprendizaje entre distintas características.
> 
> *Algoritmo paso a paso*
> 1. Inicializar $x_0=0, s_0=0$, tasa de aprendizaje $\eta$ y constante pequeña $\epsilon>0$
> 2. En cada iteración $t$
>    - Calcular el gradiente: $g_t=\nabla f(x_{t-1})$
>    - Acumular gradientes cuadrados: $s_t=s_{t-1}+g_t^2$ 
>    - Actualizar parámetros: $\large x_t=x_{t-1}-\frac{\eta}{\sqrt{s_t}+\epsilon}\cdot g_t$ 
> 3. Repetir hasta convergencia.
> 
> En resumen, Adagrad hace que la tasa de aprendizaje vaya decreciendo automáticamente en las direcciones donde ya se ha aprendido mucho. Por eso puede funcionar bien incluso con valores iniciales de $\eta$ relativamente grandes. No usa una única learning rate fija para todos los parámetros, sino que usa una learning rate adaptativa por coordenada basada en el historial acumulado de gradientes.
#### 6. RMSProp
> **RMSProp** es un método de optimización adaptativo diseñado para corregir una limitación importante de Adagrad: en Adagrad, el estado acumulado crece sin límite y eso hace que la tasa de aprendizaje efectiva se vuelva demasiado pequeña con el paso de las iteraciones.
> 
> Su _idea principal_ es no acumular todos los gradientes cuadrados desde el inicio, sino usar una *media móvil exponencial* o _leaky average_. De este modo, el algoritmo da más peso a los gradientes recientes y evita que la acumulación crezca indefinidamente.
> En Adagrad, el estado $s_t$ crece sin control, que provoca una reducción excesiva de la learning rate efectiva. Entonces RMSProp separa la adaptatividad por coordenada del problema de una decadencia irreversible del step.
> 
> La _acumulación del estado_ en RMSProp es: $$s_t \leftarrow \beta s_{t-1} + (1-\beta)g_t^2$$donde $s_t$ representa la acumulación de gradientes cuadrados en forma de media móvil, y $\beta \in [0,1]$ controla cuánto peso se da al pasado.
> 
> La _regla de actualización_ es: $$x_t \leftarrow x_{t-1} - \frac{\eta}{\sqrt{s_t}+\epsilon}\cdot g_t$$donde:
> - $\eta$ es la learning rate global
> - $\epsilon > 0$ es una constante pequeña para evitar divisiones por cero
> - $g_t$ es el gradiente en la iteración $t$
> 
> A nivel conceptual, RMSProp mantiene la misma filosofía básica que Adagrad: cada coordenada se actualiza con un paso distinto según la magnitud de sus gradientes. La diferencia es que ahora esa magnitud no se calcula con una suma acumulada total, sino con una media móvil que “olvida” progresivamente el pasado.
> 
> _Diferencia con Adagrad_
> - **Adagrad** usa una acumulación total de gradientes cuadrados.
> - **RMSProp** usa una acumulación controlada mediante media móvil exponencial.
> Por eso RMSProp evita que el learning rate efectivo se haga demasiado pequeña demasiado pronto.
> 
> En resumen, **RMSProp** conserva la adaptatividad por parámetro de Adagrad, pero introduce un mecanismo de control en el estado acumulado. Gracias a esa media móvil de gradientes cuadrados, el algoritmo sigue adaptando el tamaño del paso en cada coordenada sin sufrir la caída excesiva de la tasa de aprendizaje que aparece en Adagrad.
#### 7. Adam
> **Adam** combina varias ideas de los métodos vistos anteriormente en un único optimizador. Toma de **Momentum** la media móvil de los gradientes para estabilizar y acelerar la dirección de descenso, y de **RMSProp** la media móvil de los gradientes cuadrados para reescalar cada coordenada de forma adaptativa.
> 
> La motivación que aparece en las diapositivas es precisamente esa: reunir en un solo método lo que ya sabemos que funciona bien. Hasta este punto hemos visto que:
> - **SGD** suele ser más efectivo que GD en datasets grandes.
> - **MBGD** mejora la eficiencia usando subconjuntos y operaciones vectorizadas.
> - **Momentum** agrega historial de gradientes para acelerar la convergencia.
> - **Adagrad** introduce escalado por coordenada.
> - **RMSProp** desacopla ese escalado del problema de una learning rate que decrece sin control.
> 
> A partir de ahí, **Adam** construye dos estimaciones mediante medias móviles exponenciales:
> La _estimación de primer momento_ o término tipo momentum es:  $$v_t \leftarrow \beta_1 v_{t-1} + (1-\beta_1)g_t$$La _estimación de segundo momento_ es: $$s_t \leftarrow \beta_2 s_{t-1} + (1-\beta_2)g_t^2$$donde:
> - $g_t$ es el gradiente en la iteración $t$
> - $v_t$ acumula información de dirección
> - $s_t$ acumula información sobre la magnitud cuadrática del gradiente
> - valores típicos en las diapositivas: $\beta_1 = 0.9, \ \beta_2 = 0.999$
> 
> Un detalle importante de Adam es la **bias correction**. Como al inicio se parte de $v_0=0$ y $s_0=0$, las primeras estimaciones quedan sesgadas hacia cero. Para corregir ese sesgo, Adam usa: $$\hat{v}_t = \frac{v_t}{1-(\beta_1)^t}, \qquad \hat{s}_t = \frac{s_t}{1-(\beta_2)^t}$$Esta corrección compensa el sesgo introducido por la inicialización, es especialmente importante en las primeras iteraciones y permite obtener estimaciones más precisas de ambos momentos
> 
> Después, Adam reescala el gradiente combinando ambas cantidades: $$g_t'=\frac{\eta \hat{v}_t}{\sqrt{\hat{s}_t}+\epsilon}$$y actualiza los parámetros con: $$x_t \leftarrow x_{t-1} - g_t'$$Es decir, Adam usa una dirección suavizada por el primer momento, una normalización adaptativa por coordenada mediante el segundo momento, y una corrección del sesgo inicial para que ambas estimaciones no empiecen demasiado pequeñas.
> 
> En resumen, **Adam** puede verse como una combinación de **Momentum + RMSProp + bias correction**. Por eso suele funcionar bien en la práctica: suaviza la dirección del descenso, adapta el tamaño del paso en cada coordenada y corrige el sesgo de las medias móviles en las primeras iteraciones.

#### 8. Overfitting & Underfitting
> Rellenar
### II. Normalization
#### 1. Problem
> Rellenar
#### 2. Batch-Norm
> Rellenar
#### 3. Layer-Norm
> Rellenar
#### 4. Instance-Norm
> Rellenar
#### 5. Group-Norm
> Rellenar
#### 6. Where to Add
> Rellenar

### III. Rellenar Techniques
#### 1. Data Augmentation
> Rellenar
#### 2. Early Stopping
> Rellenar
#### 3. Dropout
> Rellenar
#### 4. Residual Connections
> Rellenar
#### 5. Learning Rates Schedulers 
> Rellenar
#### 6. Regularization
> Rellenar
#### 7. Ensembles
> Rellenar
#### 8. Transfer Learning
> Rellenar