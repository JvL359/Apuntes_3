### I. Optimization Algorithms
#### 1. Fundamentos y Motivación de la Optimización
> En deep learning, **optimizar** no significa solo reducir la pérdida en entrenamiento, sino hacerlo de forma que el modelo también **generalice bien** a datos no vistos. Por eso hay que distinguir entre:
> - **Error de entrenamiento / riesgo empírico**: pérdida media sobre el conjunto de entrenamiento.
> - **Error de generalización / riesgo**: pérdida esperada sobre la distribución real de los datos.
> 
> El mínimo del riesgo empírico no tiene por qué coincidir con el mínimo del riesgo real, así que minimizar muy bien la loss de train no garantiza el mejor rendimiento en validación o test. ![[Pasted image 20260319192500.png]]
> 
> Uno de los principales problemas al optimizar redes profundas es el de los **vanishing gradients**.  
> Cuando las derivadas se vuelven muy pequeñas durante backpropagation, las actualizaciones de los pesos casi desaparecen y el aprendizaje se ralentiza o incluso se detiene. Esto ocurre especialmente con activaciones saturables como `tanh`, cuya derivada: $f'(x)=1-\tanh^2(x)$ se aproxima a cero para valores grandes de $x$. ![[Pasted image 20260319192607.png]]
> 
> La idea básica del **gradient descent** parte de una aproximación de Taylor. En una dimensión, si queremos minimizar una función $f:\mathbb{R}\to\mathbb{R}$, actualizamos: $x \leftarrow x - \eta f'(x)$ donde $\eta$ es la **learning rate**. En varias dimensiones, para una función $f:\mathbb{R}^d\to\mathbb{R}$, la regla pasa a ser: $\mathbf{x} \leftarrow \mathbf{x} - \eta \nabla f(\mathbf{x})$ con: $$\nabla f(\mathbf{x})= \left[\frac{\partial f}{\partial x_1}, \frac{\partial f}{\partial x_2}, \dots, \frac{\partial f}{\partial x_d} \right]^T$$El gradiente marca la dirección de máximo crecimiento, así que $-\nabla f(\mathbf{x})$ define la dirección de descenso más pronunciado.
> 
> El **learning rate** controla el tamaño del paso:
> - Si es **demasiado pequeña**, la convergencia es muy lenta.
> - Si es **demasiado grande**, el algoritmo puede oscilar o divergir.
> - Si está bien ajustada, el descenso es estable y eficiente.
> ![[Pasted image 20260319192713.png]]
> 
> Otro problema importante es que en funciones **no convexas** puede haber muchos mínimos locales. En ese caso, el punto al que llega el algoritmo depende de la inicialización y de el learning rate. En deep learning esto es habitual, porque las funciones objetivo suelen ser altamente no convexas. ![[Pasted image 20260319192756.png]]
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
> - $\eta$ es el learning rate.
> 
> Su coste computacional pasa a ser $O(1)$. Además, el gradiente estocástico es un estimador insesgado del gradiente completo: $$\mathbb{E}_i \nabla f(\mathbf{x}_i)=\frac{1}{n}\sum_{i=1}^{n}\nabla f(\mathbf{x}_i)=\nabla f(\mathbf{x})$$
> - **Mini-Batch Gradient Descent (MBGD)**  
> Aunque SGD es insesgado, puede necesitar demasiadas iteraciones. Para equilibrar coste y estabilidad, se usa un subconjunto o batch de muestras: $$\mathbf{x}\leftarrow \mathbf{x}-\eta \frac{1}{|\mathcal{B}_t|}\sum_{i\in |\mathcal{B}_t|}\nabla f(\mathbf{x}_i)$$donde $\mathcal{B}_t$ es el batch usado en la iteración $t$
>![[Pasted image 20260319193045.png]] El coste computacional es: $O(b) \ \text{con } b \ll n$ por lo que MBGD queda en mitad entre GD y SGD:
> - **GD:** usa todo el dataset, trayectoria más estable.
> - **SGD:** usa una sola muestra, trayectoria más ruidosa.
> - **MBGD:** usa un lote pequeño, combinando eficiencia y mayor estabilidad que SGD.
#### 3. Dynamic Learning Rate
> Un **learning rate dinámico** sustituye la tasa fija $\eta$ por una función dependiente del tiempo $\eta(t)$.
> La motivación es que una tasa de aprendizaje fija presenta varios problemas:
> - si $\eta$ es muy pequeña, la convergencia es muy lenta
> - si $\eta$ es muy grande, la optimización puede oscilar o divergir
> Además, en métodos como **SGD** y **MBGD**, el ruido en la estimación del gradiente introduce variabilidad en la convergencia.
> 
> Por ello, se ajusta $\eta$ a lo largo del entrenamiento para combinar **convergencia rápida al principio**, y **estabilidad cerca del mínimo**. Las estrategias son las siguientes:
>
> **Piecewise Constant**:  $$\eta(t)=\eta_i,\quad \text{si } t_i \le t < t_{i+1}$$**Exponential Decay**:  $$\eta(t)=\eta_0\cdot e^{-\lambda t}$$**Polynomial Decay**:  $$\eta(t)=\eta_0\cdot (\beta t+1)^{-\alpha}$$donde una elección común es $\alpha=0.5$.
> 
> En comparación, los esquemas **piecewise constant** son simples y muy usados, el **exponential decay** puede reducir la learning rate demasiado pronto, y el **polynomial decay** destaca por equilibrar velocidad y estabilidad de convergencia. ![[Pasted image 20260319194057.png]]![[Pasted image 20260319194123.png]]
> 
> En resumen, la idea de esta sección es que **hacer evolucionar la learning rate durante el entrenamiento suele dar un comportamiento más robusto que mantenerla fija**.
#### 4. Momentum
> En SGD y MBGD los gradientes pueden ser ruidosos. Si el learning rate disminuye demasiado rápido, la convergencia se frena; si disminuye demasiado poco, el ruido puede alejar la optimización del óptimo. La idea de _momentum_ es usar el historial de gradientes para suavizar la trayectoria y hacer el proceso más estable.
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
> El ejemplo: $f(x)=0.1x_1^2+2x_2^2$  muestra precisamente este comportamiento: con ciertos valores de $\eta$ el método puede oscilar o incluso divergir. Momentum ayuda a amortiguar estas oscilaciones y a avanzar de forma más consistente hacia el mínimo. ![[Pasted image 20260319194217.png]]
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
#### 5. Nesterov Accelerated Gradient
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
> Por ello, Nesterov suele anticipar mejor la trayectoria de descenso, ya que con Momentum acumula inercia y añade una corrección anticipada sobre esa inercia. ![[Pasted image 20260319194359.png]]
#### 6. Adagrad
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
#### 7. RMSProp
> **RMSProp** es un método de optimización adaptativo diseñado para corregir una limitación importante de Adagrad: en Adagrad, el estado acumulado crece sin límite y eso hace que la tasa de aprendizaje efectiva se vuelva demasiado pequeña con el paso de las iteraciones.
> 
> Su _idea principal_ es no acumular todos los gradientes cuadrados desde el inicio, sino usar una *media móvil exponencial* o _leaky average_. De este modo, el algoritmo da más peso a los gradientes recientes y evita que la acumulación crezca indefinidamente.
> En Adagrad, el estado $s_t$ crece sin control, que provoca una reducción excesiva de el learning rate efectivo. Entonces RMSProp separa la adaptatividad por coordenada del problema de una decadencia irreversible del step.
> 
> La _acumulación del estado_ en RMSProp es: $$s_t \leftarrow \beta s_{t-1} + (1-\beta)g_t^2$$donde $s_t$ representa la acumulación de gradientes cuadrados en forma de media móvil, y $\beta \in [0,1]$ controla cuánto peso se da al pasado.
> 
> La _regla de actualización_ es: $$x_t \leftarrow x_{t-1} - \frac{\eta}{\sqrt{s_t}+\epsilon}\cdot g_t$$donde:
> - $\eta$ es el learning rate global
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
#### 8. Adam
> **Adam** combina varias ideas de los métodos vistos anteriormente en un único optimizador. Toma de **Momentum** la media móvil de los gradientes para estabilizar y acelerar la dirección de descenso, y de **RMSProp** la media móvil de los gradientes cuadrados para reescalar cada coordenada de forma adaptativa.
> 
> Entonces con Adam se trata de reunir en un solo método lo que ya sabemos que funciona bien. Hasta este punto hemos visto que:
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
> - valores típicos: $\beta_1 = 0.9, \ \beta_2 = 0.999$
> 
> Un detalle importante de Adam es la **bias correction**. Como al inicio se parte de $v_0=0$ y $s_0=0$, las primeras estimaciones quedan sesgadas hacia cero. Para corregir ese sesgo, Adam usa: $$\hat{v}_t = \frac{v_t}{1-(\beta_1)^t}, \qquad \hat{s}_t = \frac{s_t}{1-(\beta_2)^t}$$Esta corrección compensa el sesgo introducido por la inicialización, es especialmente importante en las primeras iteraciones y permite obtener estimaciones más precisas de ambos momentos
> 
> Después, Adam reescala el gradiente combinando ambas cantidades: $$g_t'=\frac{\eta \hat{v}_t}{\sqrt{\hat{s}_t}+\epsilon}$$y actualiza los parámetros con: $$x_t \leftarrow x_{t-1} - g_t'$$Es decir, Adam usa una dirección suavizada por el primer momento, una normalización adaptativa por coordenada mediante el segundo momento, y una corrección del sesgo inicial para que ambas estimaciones no empiecen demasiado pequeñas.
> 
> En resumen, **Adam** puede verse como una combinación de **Momentum + RMSProp + bias correction**. Por eso suele funcionar bien en la práctica: suaviza la dirección del descenso, adapta el tamaño del paso en cada coordenada y corrige el sesgo de las medias móviles en las primeras iteraciones.
#### 9. Overfitting & Underfitting
> Al optimizar una red neuronal no basta con reducir el error de entrenamiento. El objetivo real es obtener un modelo que **ajuste bien** y que además **generalice** correctamente a datos no vistos.
> 
> Distinguimos tres situaciones: ![[Pasted image 20260319194528.png]]
> - **Underfitted**: ajuste insuficiente, asociado a **high bias error**.
> - **Good fit / robust**: equilibrio adecuado entre bias y variance.
> - **Overfitted**: ajuste excesivo al entrenamiento, asociado a **high variance error**.
> 
> La idea central es que, para tener un buen modelo, el **training error** debe ser pequeño, pero también debe ser **similar al test error**. En otras palabras, no solo importa minimizar el error de entrenamiento, sino también minimizar el error de generalización.
> 
> La interpretación es que:
> ![[Pasted image 20260319194557.png]]
> - Si **test error $\gg$ training error**, entonces hay **high variance error** y aparece un **generalization gap** grande.
> - Si **training error $\approx$ test error $\gg 0$**, entonces el problema es de **high bias error**.
> 
> Cuando se representa el error frente a la **capacidad** del modelo, se observa este comportamiento:
> - En la zona de **underfitting**, el modelo tiene poca capacidad y no logra capturar bien la estructura de los datos.
> - A medida que aumenta la capacidad, el error baja hasta llegar a una **capacidad óptima**.
> - Si seguimos aumentando la capacidad, entramos en la zona de **overfitting**, donde el error de entrenamiento puede seguir bajando pero el error de generalización empieza a subir.
> 
> Aquí entra el balance **bias-variance**: ![[Pasted image 20260319194635.png]]
> - El **bias** disminuye cuando aumenta la capacidad del modelo.
> - La **variance** aumenta cuando la capacidad crece demasiado.
> - El **generalization error** resulta del equilibrio entre ambas, y alcanza su mínimo cerca de la **optimal capacity**.
> 
> En resumen, **underfitting** significa que el modelo es demasiado simple y comete error alto tanto en entrenamiento como en test. **Overfitting** significa que el modelo aprende demasiado bien el entrenamiento pero pierde capacidad de generalización. El punto deseable es un ajuste intermedio, donde el error total sea mínimo y la diferencia entre entrenamiento y test se mantenga controlada.
### II. Normalization
#### 1. Vanishing & Exploding Gradients
> Estos son los problemas que las técnicas de normalización intentan aliviar: los **vanishing gradients** y los **exploding gradients** durante la retropropagación.
> 
> Los **vanishing gradients** aparecen cuando los gradientes se vuelven demasiado pequeños al propagarse hacia atrás por la red. Como consecuencia, las actualizaciones de los parámetros son mínimas y el entrenamiento se vuelve muy lento o incluso se detiene, especialmente en redes profundas.
> Los **exploding gradients** aparecen cuando los gradientes crecen sin control. Esto provoca inestabilidad numérica, hace que los parámetros diverjan y puede terminar haciendo fallar el entrenamiento del modelo.
> 
> En el caso de los **exploding gradients**, los síntomas más claros son:
> - picos repentinos en la función de pérdida durante el entrenamiento,
> - valores de gradiente muy grandes en capas concretas.
> Para detectarlos, podemos representar la evolución de la loss durante el entrenamiento, y monitorizar la magnitud de pesos y gradientes capa a capa, .
> 
> En el caso de los **vanishing gradients**, los síntomas típicos son:
> - convergencia extremadamente lenta o estancamiento,
> - gradientes cercanos a cero en las primeras capas.
> Para detectarlos, podemos observar si la función de pérdida entra en una meseta, y analizar las magnitudes de gradiente por capa para comprobar si van disminuyendo excesivamente.
> 
> En resumen, esta subsección sirve como motivación: antes de estudiar **normalization**, hay que entender que en redes profundas el flujo del gradiente puede degradarse. La normalización aparece precisamente como una herramienta para hacer el entrenamiento más estable y evitar que los gradientes desaparezcan o exploten.
#### 2. Batch-Norm
> **Batch Normalization** es una técnica diseñada para *estabilizar y acelerar el entrenamiento* de redes profundas. Aparece situada típicamente entre una capa convolucional y la activación, siguiendo el esquema: $$\text{Conv} \rightarrow \text{BN} \rightarrow \text{ReLU}$$La idea básica es **normalizar las activaciones dentro de un mini-batch**. Esto evita desplazamientos en las activaciones, reduce la dependencia respecto a la inicialización, ayuda a prevenir _vanishing_ y _exploding gradients_, y además actúa como regularizador. ![[Pasted image 20260319194844.png]]
> 
> En una capa convolucional, si el batch de activaciones tiene forma $$B \times W \times H \times C$$donde $B$ es el tamaño de batch, $W,H$ son las dimensiones espaciales y $C$ el número de canales, Batch-Norm calcula la media y la varianza **por canal**: $$\mu_c=\frac{1}{BWH}\sum_{k,x,y} Z_{k,x,y,c}$$$$\sigma_c^2=\frac{1}{BWH}\sum_{k,x,y}(Z_{k,x,y,c}-\mu_c)^2$$Por tanto:
> - $\mu_{c}$ es la media calculada para un canal concreto, usando todas las muestras del mini-batch y todas las posiciones espaciales.
> - $\sigma^2_{c}$ es la varianza calculada para ese mismo canal, sobre todas las muestras del mini-batch y todas las posiciones espaciales.
> 
> Después, cada activación se normaliza usando esas estadísticas: $$\hat{Z}_{k,x,y,c}=\frac{Z_{k,x,y,c}-\mu_c}{\sqrt{\sigma_c^2+\epsilon}}$$donde $\epsilon$ es una constante pequeña que aporta estabilidad numérica.
> 
> Una vez obtenidos estos valores normalizados, Batch-Norm no se limita a dejar la salida con media 0 y varianza 1, sino que introduce dos parámetros entrenables por canal para recuperar capacidad de representación: $$Y_i=\gamma \hat{Z}_i+\beta$$donde $\gamma$ escala la activación normalizada y $\beta$ la desplaza.
> 
> Durante la **inferencia**, las estadísticas del batch pueden no ser fiables, especialmente si el batch es muy pequeño. Por eso no se usan directamente las medias y varianzas del batch actual, sino estimaciones acumuladas durante entrenamiento. Estas medias móviles se actualizan con: $$\mu_{c,\text{running}}=\alpha \mu_{\text{running}}+(1-\alpha)\mu_c$$$$\sigma^2_{c,\text{running}}=\alpha \sigma^2_{\text{running}}+(1-\alpha)\sigma_c^2$$Por tanto:
>- $\mu_{c, \text{running}}$ es la media acumulada o media móvil del canal $c$, estimada durante el entrenamiento y usada en inferencia.
>- $\sigma^2_{c, \text{running}}$ es la varianza acumulada o varianza móvil del canal $c$, estimada durante el entrenamiento y usada en inferencia.
> De este modo, el modelo dispone de estadísticas más estables para evaluación.
> 
> Aun así, Batch-Norm también tiene **limitaciones**, ya que introduce coste computacional adicional, no funciona bien con tamaños de batch muy pequeños, introduce dependencia entre muestras del mismo batch, y no es adecuado para modelos recurrentes cuando las estadísticas cambian mucho entre batches.
> 
> En resumen, Batch-Norm normaliza activaciones a nivel de mini-batch para hacer el entrenamiento más estable y rápido, pero su eficacia depende bastante del tamaño del batch y del tipo de arquitectura.
#### 3. Layer-Norm
> **Layer Normalization** es una técnica de normalización que, a diferencia de Batch-Norm, **no normaliza a través del batch**, sino **a través de las dimensiones de características de cada muestra individual**. De igual manera que *Batch-Norm*, aparece colocada dentro del bloque: $$\text{Conv} \rightarrow \text{LN} \rightarrow \text{ReLU}$$La idea principal es que cada entrada se normaliza **de manera independiente**, usando sus propias estadísticas. Por eso resulta especialmente útil cuando el tamaño de batch es pequeño o cuando las estadísticas entre batches cambian mucho. ![[Pasted image 20260319194932.png]]
> 
> Si la entrada es un tensor: $$Z \in \mathbb{R}^{B \times W \times H \times C}$$entonces Layer-Norm normaliza cada muestra $k$ a lo largo de todas sus dimensiones espaciales y de canal. La activación normalizada viene dada por: $$\hat{Z}_{k,x,y,c}=\frac{Z_{k,x,y,c}-\mu_k}{\sigma_k}$$donde la media y la varianza para cada muestra son: $$\mu_k=\frac{1}{WHC}\sum_{x,y,c} Z_{k,x,y,c}$$ $$\sigma_k^2=\frac{1}{WHC}\sum_{x,y,c}(Z_{k,x,y,c}-\mu_k)^2$$Por tanto:
> - $\mu_k$ es la media calculada sobre todas las características de una única entrada.
> - $\sigma_k^2$ es la varianza calculada sobre todas las características de esa misma entrada.
> 
> Por tanto, Layer-Norm garantiza que **cada muestra tenga activaciones con media cero y varianza unidad** a través de sus canales y dimensiones internas.
> 
> La *diferencia clave frente a Batch-Norm* es que Batch-Norm normaliza a través de la dimensión batch, y por eso necesita batches suficientemente grandes para obtener estadísticas estables. Mientras que *Layer-Norm* normaliza a través de las características de cada muestra, por lo que **no depende del tamaño de batch**.
> Esto hace que Layer-Norm esté mejor adaptada a **batches pequeños**, **modelos recurrentes**, y **transformers**, donde las estadísticas de batch pueden variar mucho.
> 
> Sus ventajas principales son que:
> - funciona bien en modelos secuenciales
> - no requiere batch grande para comportarse de forma estable
> - evita el coste de mantener estadísticas de batch durante entrenamiento e inferencia
> - consigue activaciones con media 0 y varianza 1 sin depender de otras muestras del batch
> 
> En resumen, **Layer-Norm normaliza cada muestra por separado**, mientras que **Batch-Norm normaliza usando el batch completo**. Por eso Layer-Norm es más adecuada cuando no se puede asumir estabilidad estadística entre batches.
#### 4. Instance-Norm
> **Instance Normalization** es una técnica de normalización aplicada **a cada imagen individual** de un batch. Su arquitectura es la misma que anteriores: $$\text{Conv} \rightarrow \text{IN} \rightarrow \text{ReLU}$$A diferencia de **Batch-Norm**, que normaliza a partir de las estadísticas del batch completo, **Instance-Norm normaliza cada muestra por separado** y además lo hace **canal a canal**, usando únicamente las dimensiones espaciales de cada canal. ![[Pasted image 20260319195931.png]]
> Si la entrada es un tensor: $$Z \in \mathbb{R}^{B \times W \times H \times C}$$ entonces Instance-Norm normaliza cada activación según: $$\hat{Z}_{k,x,y,c}=\frac{Z_{k,x,y,c}-\mu_{kc}}{\sigma_{kc}}$$donde, para cada muestra $k$ y cada canal $c$, la media y la varianza se calculan sobre las dimensiones espaciales: $$\mu_{kc}=\frac{1}{WH}\sum_{x,y} Z_{k,x,y,c}$$$$\sigma^2_{kc}=\frac{1}{WH}\sum_{x,y}(Z_{k,x,y,c}-\mu_{kc})^2$$Por tanto:
> - $\mu_{kc}$ es la media de un canal concreto en una muestra concreta.
> - $\sigma^2_{kc}$ es la varianza de ese canal en esa muestra.
> 
> Comparando las tres normalizaciones vistas:
> - **Batch-Norm:** normaliza sobre el batch para cada característica.
> - **Layer-Norm:** normaliza sobre todas las características de una sola muestra.
> - **Instance-Norm:** normaliza sobre las dimensiones espaciales de cada característica, de forma independiente para cada muestra.
> 
> En cuanto a su uso, **Instance-Norm** aparece sobre todo en tareas donde importa mantener estadísticas individuales de cada imagen, especialmente en **style transfer** y **image synthesis**
> La idea es que cada instancia se normaliza de forma autónoma, lo que resulta útil cuando el estilo o la apariencia concreta de cada imagen tiene mucho peso.
> Como observación final, **no se usa demasiado**, porque puede dar **estadísticas inestables**.
> 
> En resumen, **Instance-Norm** normaliza **por instancia y por canal**, usando solo la información espacial de cada mapa de características, y por eso resulta especialmente adecuada en problemas de generación y transferencia de estilo.
#### 5. Group-Norm
> **Group Normalization** normaliza las activaciones *dentro de grupos de canales*, situándose a medio camino entre *Layer-Norm* e *Instance-Norm*. Su arquitectura es la misma que las anteriores: $$\text{Conv} \rightarrow \text{GN} \rightarrow \text{ReLU}$$La idea principal es **dividir los canales en G grupos** y calcular la normalización de manera independiente dentro de cada grupo. Así, no usa estadísticas del batch completo como **Batch-Norm** pero tampoco mezcla todos los canales de una muestra como hace **Layer-Norm**. ![[Pasted image 20260319200327.png]]
> 
> Si la entrada es un tensor: $$Z \in \mathbb{R}^{B \times W \times H \times C}$$se divide la dimensión de canales en G grupos. Para cada muestra $k$ y cada grupo $g$ y se calcula:  $$\mu_{kg}=\frac{1}{WHG}\sum_{c=gG}^{(g+1)G-1}\sum_{x,y} Z_{k,x,y,c}$$$$\sigma^2_{kg}=\frac{1}{WHG}\sum_{c=gG}^{(g+1)G-1}\sum_{x,y}(Z_{k,x,y,c}-\mu_{kg})^2$$donde $g=\left[ c/G \right]$ y $G$ es el número de grupos. Por tanto:
> - $\mu_{kg}$ es la media calculada sobre todas las posiciones espaciales y todos los canales del grupo $g$ en la muestra $k$.
> - $\sigma^2_{kg}$ es la varianza calculada sobre esas mismas activaciones, es decir, sobre todas las posiciones espaciales y todos los canales del grupo $g$ en la muestra $k$.
> 
> Una vez calculadas la media y la varianza del grupo, la salida normalizada se obtiene como: $$\hat{Z}_{k,x,y,c}=\frac{Z_{k,x,y,c}-\mu_{kg}}{\sigma_{kg}}$$El funcionamiento, por tanto, es:
> 1. Dividir los canales en $G$ grupos.
> 2. Calcular media y varianza dentro de cada grupo.
> 3. Normalizar cada activación usando las estadísticas de su grupo.
> 
> Group-Norm tiene dos resultados importantes, produce **estadísticas más estables que Instance Normalization** cuando $G=C$, y a diferencia de Layer-Norm, **no fuerza a todos los canales a compartir una única estadística** cuando $G=1$.
> 
> Comparativa Final:
> ![[Pasted image 20260319200357.png]]
> - **Batch-Norm** usa estadísticas del batch y funciona peor con batch sizes pequeños,
> - **Layer-Norm** normaliza sobre todos los canales de una muestra, sin distinguir grupos,
> - **Instance-Norm** normaliza por muestra y por canal,
> - **Group-Norm** busca un compromiso, normalizando **por grupos de canales**.
> 
> En resumen, **Group-Norm** introduce una normalización más flexible que **Layer-Norm** y más estable que **Instance-Norm**, evitando además la dependencia fuerte del tamaño de batch característica de **Batch-Norm**.
#### 6. Where to Add
> Una cuestión práctica importante en redes con normalización es **dónde colocar la capa de normalización** respecto a la convolución y la activación. Hay dos posibilidades principales: 
> **Opción A:**  $$\text{Conv} \rightarrow \text{Norm} \rightarrow \text{ReLU}$$**Opción B:**  $$\text{ReLU} \rightarrow \text{Norm} \rightarrow \text{Conv}$$En la **Opción A**, primero se aplica la convolución, después la normalización y finalmente la activación. Es la disposición más habitual. Sus ventajas son que la convolución puede prescindir del sesgo, ya que la normalización elimina el desplazamiento de la media, y ayuda a estabilizar el entrenamiento al reducir el cambio en las activaciones internas. Como inconveniente, después de normalizar se aplica **ReLU**, por lo que una parte de las activaciones puede quedar anulada a cero, con la consiguiente posible pérdida de información.
> En la **Opción B**, primero se aplica la activación, luego la normalización y después la convolución. Sus ventajas son que al aplicar **ReLU antes de normalizar**, se evita la posible pérdida de información asociada a anular activaciones justo después de la normalización, y tras Batch-Norm, los ajustes de escala y sesgo pueden considerarse opcionales.
> 
> En cualquier caso, ambas configuraciones son **válidas** y pueden funcionar bien en práctica. Sin embargo, **Option A** es la más usada en arquitecturas modernas de deep learning, y **Option B** simplifica algunos aspectos de implementación, pero es menos frecuente.
> 
> Como conclusión la disposición estándar en CNNs modernas es la **Opción A**, es decir, aplicar la normalización **después de la convolución y antes de la activación**.

### III. Generalization Techniques
#### 1. Data Augmentation
> Surge como respuesta a un síntoma claro de **overfitting**: pequeños cambios en la imagen pueden producir grandes cambios en la salida del modelo. En ese caso, el modelo necesita ver más variedad de ejemplos. Como etiquetar nuevas imágenes reales es costoso, la idea es **crear nuevas muestras sintéticas a partir de las ya disponibles**, manteniendo la misma etiqueta.
> 
> En lugar de recoger y anotar más datos, se aplican **transformaciones** sobre las imágenes originales para generar nuevas versiones del mismo ejemplo. Así, a partir de una imagen etiquetada como _dog_, se pueden construir varias imágenes transformadas que siguen teniendo la misma etiqueta _dog_.
> 
> **Tipos de augmentación:** flip, shift, scale, rotate, saturation, brightness, y tint / hue. ![[Pasted image 20260320104258.png]]
> 
> La idea de fondo es que el modelo aprenda a ser más robusto frente a estas variaciones, en lugar de memorizar únicamente la apariencia exacta de las imágenes de entrenamiento.
> 
> Además, tenemos **Unsupervised Data Augmentation**, que es una técnica de aprendizaje **semi-supervisado** que aprovecha datos **no etiquetados**:
> 1. se aplica una transformación a una imagen,
> 2. la imagen original y la aumentada se pasan por la **misma red**,
> 3. se comparan ambas salidas para imponer **consistencia**.
> 
> Esta consistencia se fuerza mediante una **consistency loss**, que minimiza la diferencia entre las predicciones de la imagen original y la transformada. Con ello, el modelo aprende que su salida debería mantenerse estable ante transformaciones como rotaciones, flips o cambios de color, mejorando así su **robustez** y su **generalización**.
#### 2. Early Stopping
> **Early Stopping** consiste en detener el entrenamiento cuando el rendimiento en **validación** deja de mejorar, aunque el error de entrenamiento siga bajando.
> 
> La idea principal es que el entrenamiento no debe continuar indefinidamente: si el **validation error** empieza a aumentar mientras el **training error** sigue disminuyendo, eso indica que el modelo está empezando a **sobreajustar** los datos de entrenamiento. Por tanto, el punto óptimo de parada se identifica monitorizando la **validation loss**.
> 
> En este sentido, Early Stopping ayuda a **prevenir overfitting**, **mejorar la generalización**, y **seleccionar automáticamente** un punto razonable de entrenamiento. ![[Pasted image 20260320104339.png]]
> 
> Un concepto importante es la **patience**, que define el número de épocas o pasos consecutivos en los que se permite que la validación empeore antes de detener el entrenamiento. Esto evita parar demasiado pronto por pequeñas fluctuaciones en la validation loss y da al modelo margen para recuperarse de inestabilidades temporales.
> 
> El procedimiento básico con _patience_ es:
> 1. Entrenar el modelo durante varias iteraciones,
> 2. Monitorizar la **validation loss** en cada evaluación,
> 3. Si la pérdida de validación empeora durante $p$ pasos consecutivos, detener el entrenamiento,
> 4. Devolver los **mejores parámetros** encontrados.
> 
> **Early Stopping** actúa como un regularizador implícito que evita que los pesos lleguen a configuraciones excesivamente complejas, favorece soluciones más simples, y tiende a producir modelos con mejor capacidad de generalización.
> 
> Sin embargo, también existe el riesgo contrario: **parar demasiado pronto**. Si se interrumpe el entrenamiento antes de tiempo, el modelo puede quedar en **underfitting**, es decir, sin haber aprendido lo suficiente de los datos. Una señal de ello es que la **validation loss todavía siga disminuyendo**, lo que indica que aún hay margen de mejora.
> 
> En resumen, Early Stopping busca un equilibrio: **ni entrenar tanto como para sobreajustar, ni detenerse tan pronto que el modelo se quede corto**.
#### 3. Dropout
> **Dropout** es una técnica de **regularización** diseñada para prevenir el **overfitting** desactivando aleatoriamente neuronas durante el entrenamiento con probabilidad $p$.
> La idea es que, en cada paso de entrenamiento, una parte de las unidades no participa en el cálculo. Esto obliga a la red a no depender demasiado de neuronas concretas y a aprender **representaciones redundantes y más robustas**, mejorando así la **generalización**. ![[Pasted image 20260320104438.png]]
> 
> El mecanismo puede entenderse así: si una capa tiene 100 neuronas con activación 1 y aplicamos dropout con $p=0.4$, durante entrenamiento solo permanecerán activas, en media, unas **60 neuronas**. En inferencia, en cambio, **no se aplica dropout**, por lo que participan todas las neuronas.  ![[Pasted image 20260320104510.png]]
> Como al eliminar neuronas disminuye la suma de activaciones, durante entrenamiento se compensa reescalando las activaciones por: $$\frac{1}{1-p}$$De este modo se mantiene aproximadamente la misma magnitud esperada entre entrenamiento e inferencia. Es decir, la salida se reescala para que sea consistente con la fase de evaluación.  ![[Pasted image 20260320104611.png]]
> 
> Dropout se usa sobre todo **antes de capas fully connected / linear**, para mejorar la generalización, y **antes de capas convolucionales 1x1** en algunas arquitecturas. ![[Pasted image 20260320104744.png]]
> En cambio, **no se recomienda antes de convoluciones generales**, porque en imágenes existe una fuerte **correlación espacial** y el efecto de dropout ahí suele ser menos adecuado.  
> 
> En resumen, Dropout introduce ruido controlado durante el entrenamiento, reduce la coadaptación entre neuronas y actúa como una técnica efectiva para mejorar la capacidad de generalización del modelo.
#### 4. Residual Connections
> Las **residual connections** o **skip connections** se introducen para aliviar los problemas de optimización de redes profundas. Al aumentar la profundidad aparecen dificultades como **vanishing gradients** y **degradation**, y simplemente apilar más capas **sin anidarlas no garantiza** una mejora del rendimiento. Por eso, sin normalización la profundidad máxima está en **10–12 capas convolucionales**, y con normalización puede llegar a **20–30 capas**, pero aun así siguen existiendo problemas de entrenamiento. ![[Pasted image 20260320112702.png]]
> 
> La idea central del bloque residual es que la capa no aprenda directamente una transformación completa, sino un **incremento respecto a la identidad**. La formulación es: $$f(x)=g(x)+x$$donde $g(x)$ es la **residual mapping**. Así, el bloque aprende una corrección sobre la entrada en lugar de reconstruir toda la función desde cero. ![[Pasted image 20260320105714.png]]
> 
> Esta formulación hace que una red profunda pueda comportarse, como mínimo, tan bien como una más superficial, porque siempre existe el camino identidad. Por eso las residual connections ayudan a que aumentar la profundidad **expanda** la clase de funciones de forma más útil y evitan parte de la degradación observada en redes muy profundas.
> 
> En el caso convolucional, si la entrada y la salida del bloque no tienen la misma forma, se puede usar una **convolución 1×1** en la rama residual para igualar dimensiones. Es decir, la conexión identidad deja de ser una identidad pura y pasa a ser una proyección que adapta el número de canales o el tamaño necesario para poder realizar la suma. ![[Pasted image 20260320105655.png]]
> 
> Desde el punto de vista del entrenamiento, una ventaja fundamental es que el **gradiente puede fluir a través de la conexión residual** hacia capas anteriores. Esto suaviza el proceso de optimización y hace el paisaje de pérdida más favorable que en arquitecturas sin skip connections. ![[Pasted image 20260320105601.png]]
> 
> Con residual connections, las redes profundas pueden alcanzar profundidades mucho mayores (incluso del orden de **1000 capas**) sin la misma pérdida de generalización que sufrirían arquitecturas profundas sin este mecanismo. ![[Pasted image 20260320105416.png]]
> 
> Sobre **dónde añadir la conexión residual**, inicialmente se añadía antes de la activación de salida, pero experimentalmente resultó mejor dejar la conexión residual lo más cercana posible a una **función identidad**. Por eso las variantes modernas favorecen configuraciones donde la rama skip altera lo mínimo posible la señal. ![[Pasted image 20260320105056.png]]
> 
> En resumen, las **residual connections** combaten los problemas de optimización en redes profundas, permiten aprender una **corrección** sobre la identidad en vez de una transformación completa, facilitan el flujo del gradiente hacia capas tempranas, y hacen viable entrenar redes mucho más profundas.
#### 5. Learning Rates Schedulers
> Los **learning rate schedulers** definen cómo evoluciona la tasa de aprendizaje durante el entrenamiento. No basta con fijar una $\eta$ constante, ya se ha visto que $\eta=\eta(t)$ puede ser necesaria para un entrenamiento adecuado, e incluso usando optimizadores avanzados como **Adam** puede seguir siendo útil personalizar esa evolución.
> 
> La idea es seguir una función de planificación $f(t)$ para el learning rate. Además, una estrategia **decreciente** no siempre tiene por qué ser estrictamente monótona: “decaying is not always good”, así que la forma concreta del scheduler depende del problema. ![[Pasted image 20260320113107.png]]
> 
> **Step-LR**
> Este primer scheduler reduce el learning rate en intervalos fijos. En este caso, la tasa de aprendizaje disminuye por un factor $\gamma$ cada cierto número de épocas definido por `step_size`. Resulta útil cuando una learning rate constante provoca convergencia lenta. ![[Pasted image 20260320113136.png]]
> 
> **MultiStep-LR**
> Esta variante más flexible también reduce el learning rate por un factor $\gamma$ pero no en intervalos regulares sino en **milestones predefinidos**. Así se obtiene un control más fino sobre en qué momentos bajar el learning rate. ![[Pasted image 20260320113150.png]]
> 
> **Exponential-LR**
> Aquí el learning rate decrece exponencialmente en cada época. La fórmula mostrada es:  $$lr_t = lr_{t-1}\cdot \gamma$$Este scheduler ayuda a reducir gradualmente el tamaño del paso para favorecer una convergencia más estable.
> ![[Pasted image 20260320113203.png]]
>
> **Learning Rate Warmup**
> Consiste en **aumentar gradualmente** el learning rate al inicio del entrenamiento. Su objetivo es evitar inestabilidad en las primeras etapas de la optimización. Se mencionan como estrategias habituales **linear** warmup, **cosine** warmup, y **cyclic** warmup. ![[Pasted image 20260320114308.png]]
> 
> **Reduce Learning Rate on Plateau**
> En este caso, el learning rate se reduce cuando una métrica de rendimiento deja de mejorar. El método usa **patience** para esperar durante cierto tiempo antes de reducirla, y así ajustar dinámicamente el learning rate cuando el entrenamiento entra en una meseta. ![[Pasted image 20260320114354.png]]
> 
> En conjunto una buena planificación del learning rate mejora la **convergencia** y la **estabilidad**, evita que una tasa demasiado alta produzca **oscilaciones o divergencia**, y evita que una tasa demasiado baja provoque **convergencia lenta**.
> 
> En resumen, los schedulers permiten controlar la evolución temporal de el learning rate para adaptar mejor el proceso de optimización a las distintas fases del entrenamiento: exploración inicial, estabilización y refinamiento final.
#### 6. Regularization
> La **regularización** añade una penalización a la función objetivo para controlar la complejidad del modelo a través de sus parámetros, mediante las **normas $L_p$** que miden el tamaño de un vector: $$L_p(x)=|x|_p=\left(\sum_{i=1}^{n}|x|^p\right)^{1/p}$$![[Pasted image 20260320114505.png]]
> La idea es tomar como referencia la función más simple y medir cuán compleja es una solución observando la magnitud de sus pesos.
> 
> Una primera opción es la **regularización L1** o **Lasso**, que añade a la pérdida la suma de los valores absolutos de los pesos: $$L_1(x)=|x|_1=\sum_{i=1}^{n}|x|$$$$\tilde{\mathcal{L}}(w)=\mathcal{L}(w)+\alpha|w|_1$$L1 **favorece la esparsidad**, porque empuja algunos pesos exactamente a cero. Por eso también se dice que promueve cierta **selección de características**. Geométricamente, su paisaje de optimización tiene **bordes afilados**, y las soluciones tienden a caer sobre los ejes, dando lugar a modelos dispersos. 
> ![[Pasted image 20260320114544.png]]
> 
> La otra opción principal es la **regularización L2** o **Ridge**, que añade la magnitud cuadrática de los pesos a la función de pérdida:  $$L_2(x)=|x|_2=\left(\sum_{i=1}^{n}|x|^2\right)^{1/2}$$$$\tilde{\mathcal{L}}(w)=\mathcal{L}(w)+\frac{\alpha}{2}\left(|w|_2\right)^2$$En este caso, la regularización no fuerza pesos exactamente nulos, sino que **evita valores extremos** y produce soluciones más **suaves** y **estables**. La optimización se vuelve **suave y convexo**, y los pesos se reparten de forma más uniforme en lugar de concentrarse en unos pocos coeficientes distintos de cero.
> ![[Pasted image 20260320114628.png]]
> 
> La comparación esencial entre ambas es que **L1** induce esparsidad y puede anular pesos, y **L2** reduce magnitudes grandes y reparte los pesos de forma más homogénea.
>  
> La **L2 regularization** añade explícitamente el término de penalización $\alpha|w|^2$ a la pérdida. Esto ayuda a reducir overfitting y favorece pesos pequeños, pero actúa modificando la **función objetivo**.
> El **weight decay**, en cambio, aplica un factor de decaimiento directamente sobre los pesos en cada paso de gradiente. Esto es equivalente a L2 bajo **SGD estándar**, pero **difiere en optimizadores adaptativos** como **Adam** o **RMSProp**, y reduce la magnitud de los parámetros de forma explícita a lo largo del entrenamiento.
> 
> En resumen, ambas técnicas buscan evitar el overfitting reduciendo el tamaño de los pesos, pero no lo hacen del mismo modo, **L2** modifica la **loss**, y **weight decay** modifica directamente la **actualización de los parámetros**.
#### 7. Ensembles
> Los **ensembles** o **model averaging** consisten en **entrenar múltiples modelos** para mejorar la generalización y después **promediar sus predicciones** para reducir la varianza.
> La idea básica es que distintos modelos cometen errores distintos. Si se combinan sus salidas, el resultado final suele ser más robusto que el de un único modelo.
> Es un proceso donde se entrena más de un modelo, cada modelo produce su propia predicción, las predicciones se combinan mediante un promedio o combinación ponderada, y se obtiene una predicción final con mejor rendimiento. ![[Pasted image 20260320114941.png]]
> 
> Históricamente, **antes del deep learning**, el model averaging se hacía usando **distintos subconjuntos de datos de entrenamiento**.  
> En **deep learning**, en cambio, se suelen obtener modelos diferentes mediante: **distintas inicializaciones aleatorias**, **data augmentation**, y la **convergencia hacia distintos mínimos locales**. En cuanto a su funcionamiento, cada modelo puede **sobreajustar de manera distinta**, el promedio entre modelos suele **reducir varianza**, normalmente puede aportar una mejora de 
> **1–3% en accuracy**, pero a costa de un **tiempo de entrenamiento más largo**. Hay dos esquemas principales, **Bagging** que es una combinación en **paralelo** de varios modelos, y **Boosting** que es una combinación **secuencial** de modelos. ![[Pasted image 20260320114842.png]]
> 
> Los ensembles son útiles cuando se busca exprimir el rendimiento final del sistema, especialmente **cuando la capacidad computacional lo permite**, y **cuando es importante obtener el último extra de precisión**. ![[Pasted image 20260320115047.png]]
> 
> En resumen, un ensemble no cambia la arquitectura básica de cada red, sino que combina varias redes entrenadas de forma diferente para conseguir una predicción final más estable y con mejor capacidad de generalización.
#### 8. Transfer Learning
> **Transfer Learning** consiste en reutilizar total o parcialmente un modelo ya entrenado para resolver una nueva tarea o trabajar sobre un nuevo dataset.
> 
> Primero se entrena un modelo $M$ para una tarea $T$ usando un dataset fuente $D_S$. Después, ese conocimiento puede reutilizarse de varias formas:
> - usar $M$ sobre un nuevo dataset $D_T$ para la misma tarea $T$,
> - usar parte de $M$ sobre el dataset original $D_S$ para una nueva tarea $T_n$,
> - usar parte de $M$ sobre un nuevo dataset $D_T$ para una nueva tarea $T_n$.
> 
> El caso más importante en deep learning es usar **modelos preentrenados**. Un problema práctico para esto sería entrenar desde cero redes grandes como **VGG16** puede no ser viable.
> 
> En particular, para clasificar **animales raros**, un dataset de solo unos cientos de imágenes no es suficiente para entrenar un modelo con más de **134 millones de parámetros**; mientras que para clasificar **animales comunes**, sí puede haber suficientes datos, pero entrenar desde cero sigue siendo costoso en tiempo. Por tanto, el entrenamiento completo de modelos grandes puede requerir demasiado tiempo y demasiados datos.
> 
> Por eso, la idea básica de transfer learning es: ![[Pasted image 20260320120410.png]]
> 1. **Pretraining** sobre un dataset grande y general.
> 2. **Transfer** del modelo preentrenado al problema objetivo.
> 3. **Fine-tuning** o adaptación final sobre el dataset específico de destino.
> 
> La intuición central es que las **capas tempranas** de una red aprenden **características de bajo nivel** y esas características pueden reutilizarse en nuevos dominios. Después, las capas más tardías o las capas fully connected pueden modificarse para adaptarse a la nueva tarea. ![[Pasted image 20260320120148.png]]
> 
> En otras palabras, transfer learning permite construir clasificadores que puedan entrenarse en **menos tiempo**, con **menos datos**, aprovechando pesos ya conocidos en lugar de empezar desde inicialización aleatoria.
> 
> **Aplicaciones** de transfer learning:
> - Aprendizaje a partir de **simulaciones** (por ejemplo, coches autónomos).
> - **Adaptación de dominio**.
> - Reconocimiento de voz para grupos o contextos con menos datos.
> - Adaptación entre idiomas para _few-shot learning_.
> - En NLP, reutilizar un modelo del lenguaje entrenado en grandes corpus y adaptarlo luego a documentos de un dominio concreto.
> 
> Finalmente, se muestra una **taxonomía** del transfer learning: ![[Pasted image 20260320115811.png]]
>
> En resumen, el **transfer learning** reutiliza conocimiento aprendido previamente para reducir el coste de entrenamiento y mejorar el aprendizaje en nuevas tareas o dominios, especialmente cuando los datos son escasos o entrenar desde cero resulta demasiado caro.