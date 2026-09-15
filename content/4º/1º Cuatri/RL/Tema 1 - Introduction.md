
---
estado: pendiente de revisión
---

### I. Introducción al Aprendizaje por Refuerzo

#### 1. Intuición y evolución

> El **Aprendizaje por Refuerzo** (*Reinforcement Learning*, RL) aborda problemas de toma de decisiones secuenciales en los que un agente aprende a actuar a partir de la **experiencia** y de la realimentación evaluativa que recibe del entorno.

> La dopamina ilustra la conexión entre la recompensa y el aprendizaje: es un neurotransmisor ligado al sistema de recompensa, y las neuronas dopaminérgicas se encuentran en el área tegmental ventral (ATV). Esta relación ofrece una intuición biológica para entender por qué la señal de recompensa puede guiar el comportamiento.

> A finales de los años ochenta confluyeron tres líneas de investigación que dieron forma al RL:

- **Control óptimo**, especialmente la programación dinámica.
- **Aprendizaje por ensayo y error**, procedente de la psicología del aprendizaje animal.
- **Diferencia temporal**, que relaciona las dos aproximaciones anteriores.

> Durante años, la dificultad para escalar a problemas grandes limitó estas técnicas. En 2015, el modelo **DQN** mostró que combinar RL con redes profundas podía superar parte de esas limitaciones. A partir de ahí se desarrollaron variantes de DQN y sistemas como AlphaGo, AlphaZero y AlphaFold. Herramientas como `gym` y `baselines` aceleraron la experimentación con RL, que también se ha aplicado a mejorar modelos de lenguaje como GPT-3.

#### 2. Aplicaciones

> El RL se está extendiendo a ámbitos donde la fiabilidad es importante, incluido el industrial. Algunos ejemplos de problemas que pueden formularse como bandits son:

- Optimización de publicidad en tiempo real y recomendación personalizada de noticias.
- Medicina personalizada y pruebas clínicas.
- Decisiones de cartera en finanzas.

### II. El esquema general de RL

#### 1. Interacción entre agente y entorno

> En el instante $t$, el **agente** selecciona una acción $a_t$. El **entorno** procesa esa acción mediante un proceso de transición de estado y un proceso de recompensa; como resultado devuelve el nuevo estado $s_{t+1}$ y la recompensa $r_{t+1}$.

> Por tanto, en el entorno general de RL hay varios estados y las acciones del agente pueden llevarlo de uno a otro. Las acciones no solo determinan la recompensa: también pueden modificar el estado futuro del entorno.

#### 2. Simplificación: bandits de $k$ brazos

> Antes de tratar el entorno general, estudiamos el **bandit multibrazo**. En esta simplificación se elimina el proceso de transición de estados: el agente elige una acción y el proceso de recompensa devuelve $r_{t+1}$. El objetivo es decidir qué brazo conviene seleccionar, sin tener que modelar consecuencias sobre estados futuros.

> Esta configuración permite introducir de forma controlada los conceptos de recompensa, valores, métodos de evaluación y exploración frente a explotación.

### III. Recompensa y valoración de acciones

#### 1. Valor verdadero y valor estimado

> En cada paso recibimos una recompensa asociada a la acción anterior. Para comparar acciones, les asignamos un escalar denominado **valor de la acción**. El valor verdadero de la acción $a$ es la recompensa esperada condicionada a haber elegido esa acción:

$$
q_*(a) = \mathbb{E}[R_t \mid A_t = a]
$$

> Por ejemplo, si cada brazo representa una marca de jamón y cada cliente proporciona una valoración, $q_*(a)$ sería la valoración media real de cada marca. Sin embargo, esa media real no se conoce de antemano: en el instante $t$ se trabaja con una estimación $Q_t(a)$, obtenida a partir de las observaciones disponibles.

> En el ejemplo, la política **greedy** selecciona la acción de mayor valor verdadero:

$$
a_t = \arg\max_a q_*(a)
$$

> En la práctica, como $q_*(a)$ no es conocido, se toma como referencia la estimación disponible. Esta política aprovecha la información actual, pero puede dejar de probar acciones cuya estimación inicial sea baja o incierta.

#### 2. Promedio de la muestra

> Una forma directa de evaluar una acción es calcular el promedio de las recompensas observadas. Esta estimación puede actualizarse incrementalmente sin guardar todas las muestras:

$$
Q_{n+1} = Q_n + \frac{1}{n}\left[R_n - Q_n\right]
$$

> La actualización sigue una estructura transversal en RL:

$$
\text{NewEstimate} \leftarrow \text{OldEstimate} + \text{StepSize}\left[\text{Target} - \text{OldEstimate}\right]
$$

> El término entre corchetes es el error entre la recompensa observada y la estimación actual. La nueva estimación corrige la anterior en una fracción marcada por el tamaño de paso.

#### 3. Tamaño de paso constante y convergencia

> En lugar de usar $1/n$, podemos emplear un tamaño de paso constante $\alpha$:

$$
Q_{n+1} = Q_n + \alpha\left[R_n - Q_n\right]
$$

> Al desarrollar esta recurrencia se obtiene un promedio ponderado exponencialmente por recencia: las recompensas más recientes pesan más. Esto es útil cuando interesa que la estimación responda a nueva información.

> También puede usarse un tamaño de paso variable $\alpha_n(a)$. Para la convergencia, sus valores deben cumplir:

$$
\sum_{n=1}^{\infty}\alpha_n(a)=\infty
\qquad \text{y} \qquad
\sum_{n=1}^{\infty}\alpha_n^2(a)<\infty
$$

### IV. Exploración y explotación

#### 1. El dilema

> **Explotar** consiste en seleccionar la acción que actualmente parece mejor; **explorar** consiste en probar alternativas para mejorar las estimaciones. Una política exclusivamente greedy puede quedarse con una estimación incorrecta, mientras que explorar demasiado reduce la recompensa inmediata.

#### 2. Políticas $\varepsilon$-greedy

> Una política $\varepsilon$-greedy introduce exploración aleatoria. Si hay $n$ acciones, la acción greedy se elige con probabilidad $1-\frac{n-1}{n}\varepsilon$, y cada una de las restantes con probabilidad $\frac{\varepsilon}{n}$.

> En el banco de pruebas de 10 brazos, cada $q_*(a)$ se muestrea de $\mathcal{N}(0,1)$ y la recompensa de cada acción sigue $\mathcal{N}(q_*(a),1)$. Al comparar 2000 ejecuciones con evaluación por promedio de la muestra, $\varepsilon=0.1$ obtiene un mayor rendimiento promedio y un mayor porcentaje de acciones óptimas que $\varepsilon=0.01$ y que la estrategia greedy ($\varepsilon=0$).

#### 3. Valores iniciales optimistas

> Los **valores iniciales optimistas** fijan estimaciones iniciales elevadas. Una política greedy tenderá entonces a probar acciones todavía no evaluadas, por lo que los valores iniciales actúan como mecanismo de exploración.

> En el experimento mostrado, la configuración optimista y greedy ($Q_1=5$, $\varepsilon=0$) supera con el tiempo a una configuración realista $\varepsilon$-greedy ($Q_1=0$, $\varepsilon=0.1$). Es un enfoque de exploración eficaz, pero es insensible a los cambios que se produzcan en el entorno después de un tiempo.

#### 4. Límites de confianza superiores

> El método de **límites de confianza superiores** (*Upper Confidence Bound*, UCB) selecciona la acción que maximiza una combinación de su estimación actual y un término de incertidumbre:

$$
A_t \doteq \arg\max_a\left[Q_t(a) + c\sqrt{\frac{\ln t}{N_t(a)}}\right]
$$

> $N_t(a)$ contabiliza cuántas veces se ha seleccionado la acción $a$. Por ello, las acciones poco probadas reciben una bonificación de exploración mayor. El parámetro $c$ controla cuánto se valora esa incertidumbre.

> UCB suele rendir mejor que $\varepsilon$-greedy en el banco de pruebas mostrado. Igual que los valores iniciales optimistas, es insensible a cambios tardíos del entorno y resulta difícil de extender a configuraciones generales de RL con espacios de acciones complejos y aproximación de funciones.

#### 5. Bandits asociativos y entorno general

> En un **bandit asociativo** la elección puede depender de la información de estado disponible, pero no hay transición de estado causada por la acción. En el entorno general de RL sí existe esa transición: la acción $a_t$ afecta tanto a la recompensa $r_{t+1}$ como al estado siguiente $s_{t+1}$.

#### 6. Bandits de gradiente

> Los **bandits de gradiente** no representan directamente el valor de cada acción, sino una preferencia $H_t(a)$. Estas preferencias se convierten en una política probabilística mediante una distribución *softmax*:

$$
\Pr\{A_t=a\} \doteq \frac{e^{H_t(a)}}{\sum_{b=1}^{k}e^{H_t(b)}} \doteq \pi_t(a)
$$

> La política se aprende mediante ascenso de gradiente. Para la acción seleccionada $A_t$ y para el resto de acciones, las actualizaciones son:

$$
H_{t+1}(A_t) \doteq H_t(A_t) + \alpha\left(R_t-\bar{R}_t\right)\left(1-\pi_t(A_t)\right)
$$

$$
H_{t+1}(a) \doteq H_t(a) - \alpha\left(R_t-\bar{R}_t\right)\pi_t(a),
\qquad \text{para todo } a \ne A_t
$$

> $\bar{R}_t$ funciona como línea base. En la comparación mostrada, emplearla mejora el porcentaje de acciones óptimas frente a usar la misma regla sin línea base.

### V. Resumen Final

> RL aprende decisiones a partir de la interacción con un entorno y de las recompensas obtenidas. Los bandits de $k$ brazos aíslan el problema de elegir acciones al eliminar las transiciones de estado, lo que permite estudiar valores de acción y métodos de actualización incrementales.

> La elección de una política exige equilibrar explotación y exploración. $\varepsilon$-greedy explora al azar, los valores iniciales optimistas inducen exploración al inicio y UCB la dirige hacia acciones inciertas. Los bandits de gradiente representan directamente una política probabilística y ajustan sus preferencias por ascenso de gradiente, pudiendo usar una línea base para mejorar el aprendizaje.
