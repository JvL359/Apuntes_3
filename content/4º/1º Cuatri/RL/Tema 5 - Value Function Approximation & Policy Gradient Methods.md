---
estado: pendiente de revisión
---

### I. Aproximación de funciones de valor

#### 1. RL a gran escala y generalización

> Los métodos tabulares almacenan un valor independiente para cada estado o par estado-acción. Funcionan cuando esos espacios son pequeños, pero dejan de ser prácticos en problemas como ajedrez, Go, navegación de vehículos autónomos o finanzas. El problema aparece tanto en la **memoria** necesaria como en la **cantidad de experiencia**: visitar muchas veces cada situación puede ser inviable.
>
> La **aproximación de funciones de valor** sustituye la tabla por una función parametrizada mediante un vector de pesos $w$:

$$
\hat v(s,w)\approx v_\pi(s),
\qquad
\hat q(s,a,w)\approx q_\pi(s,a).
$$

> En predicción, $\pi$ es la política cuyo valor queremos estimar. En control, también buscamos mejorar la política. Los parámetros compartidos permiten **generalizar**: la experiencia de un estado puede modificar las estimaciones de otros estados que tengan características similares. Esta transferencia reduce las necesidades de datos, aunque también puede transmitir errores entre estados.

#### 2. Representación del estado y tipos de aproximación

> Antes de aproximar un valor necesitamos una señal que represente el estado. Debe conservar información suficiente para predecir la siguiente transición y recompensa, dadas las acciones: esa es la idea de la **propiedad de Markov**. Una observación instantánea puede resultar insuficiente; por ejemplo, una imagen informa de la posición de un objeto, pero puede no identificar su velocidad.
>
> Podemos construir un vector de características $x(s)$ a partir de variables del entorno, de características diseñadas o de una representación aprendida. La elección determina qué estados distingue el aproximador y entre cuáles comparte información. Un modelo más potente no recupera automáticamente una variable relevante que nunca aparece en su entrada.

Las familias de aproximadores incluyen:

- **Combinaciones lineales de características**.
- **Redes neuronales**, que pueden aprender también la representación.
- Árboles de decisión y vecinos más cercanos.
- Bases de Fourier o Wavelet.

> Nos centramos en **aproximadores diferenciables**, porque permiten ajustar sus parámetros mediante gradientes. La diferenciabilidad se exige respecto a los pesos; las características de entrada pueden ser, por ejemplo, indicadores binarios.

#### 3. Descenso del gradiente y error cuadrático

> Sea $J(w)$ un coste escalar diferenciable que depende del vector $w=(w_1,\ldots,w_n)$. Su gradiente contiene las derivadas respecto a cada parámetro:

$$
\nabla_w J(w)=
\left[\frac{\partial J(w)}{\partial w_1},\ldots,
\frac{\partial J(w)}{\partial w_n}\right].
$$

> El **descenso del gradiente** mueve los pesos en sentido opuesto al gradiente para reducir el coste localmente. Usamos la convención siguiente, cuyo factor $1/2$ simplifica la derivada de un error cuadrático:

$$
\Delta w=-\frac12\alpha\nabla_w J(w),
\qquad w\leftarrow w+\Delta w,
\qquad \alpha>0.
$$

> Para evaluar una política fija, el objetivo ideal es minimizar el error cuadrático entre su valor real y la aproximación. La esperanza pondera los estados según la distribución considerada bajo $\pi$:

$$
J(w)=\mathbb E_\pi\left[
\bigl(v_\pi(S)-\hat v(S,w)\bigr)^2\right].
$$

> Como $v_\pi$ es fijo respecto a $w$, la regla de la cadena da:

$$
\begin{aligned}
\nabla_w J(w)
&=-2\mathbb E_\pi\left[
\bigl(v_\pi(S)-\hat v(S,w)\bigr)\nabla_w\hat v(S,w)\right],\\
\Delta w
&=\alpha\mathbb E_\pi\left[
\bigl(v_\pi(S)-\hat v(S,w)\bigr)\nabla_w\hat v(S,w)\right].
\end{aligned}
$$

> El **descenso del gradiente estocástico**, SGD, sustituye esa esperanza por una muestra:

$$
\Delta w=\alpha\bigl(v_\pi(S)-\hat v(S,w)\bigr)
\nabla_w\hat v(S,w).
$$

> La actualización combina tres elementos: **tamaño de paso**, **error de predicción** y **sensibilidad de la predicción a los pesos**. Si subestimamos el valor, movemos los parámetros en la dirección que aumenta la predicción; si lo sobreestimamos, hacemos el movimiento contrario. Cada muestra introduce ruido, pero su actualización esperada coincide con la del gradiente completo bajo el muestreo adecuado.

#### 4. Aproximación lineal y caso tabular

> La **aproximación lineal** representa el valor como una combinación de características. $x(s)$ y $w$ tienen la misma dimensión:

$$
\hat v(s,w)=x(s)^T w=\sum_j x_j(s)w_j.
$$

> El coste es cuadrático en los pesos y el gradiente del aproximador es especialmente sencillo:

$$
\begin{aligned}
J(w)&=\mathbb E_\pi\left[
\bigl(v_\pi(S)-x(S)^T w\bigr)^2\right],\\
\nabla_w\hat v(S,w)&=x(S),\\
\Delta w&=\alpha\bigl(v_\pi(S)-\hat v(S,w)\bigr)x(S).
\end{aligned}
$$

> Una característica nula no modifica su peso en esa muestra; una característica activa participa en la corrección. La función es lineal en $w$, aunque las características pueden depender de forma no lineal de las variables originales del estado. La convexidad del coste permite alcanzar un mínimo global bajo las condiciones apropiadas de muestreo y aprendizaje; puede haber varios vectores minimizadores si las características son redundantes.
>
> El **caso tabular** es un caso particular: usamos un vector **one-hot**, con una componente por estado y un único $1$ en la posición del estado observado. Entonces $x(s)^T w$ selecciona su peso, y $w$ almacena los valores de todos los estados. La representación puede expresar cualquier tabla sin error de aproximación estructural, pero pierde la generalización entre estados y conserva el problema de escalabilidad.

### II. Predicción incremental con aproximación

#### 1. Monte Carlo: aprender a partir del retorno

> La expresión ideal contiene $v_\pi(S)$, que desconocemos. En RL disponemos de transiciones y recompensas, a partir de las cuales construimos objetivos de aprendizaje. En **Monte Carlo**, MC, el objetivo es el retorno observado:

$$
G_t=\sum_{k=t+1}^{T}\gamma^{k-t-1}R_k,
\qquad
\mathbb E_\pi[G_t\mid S_t=s]=v_\pi(s).
$$

> $T$ es el instante terminal. Para una política fija y episodios generados con ella, $G_t$ es un estimador **no sesgado**, pero puede ser **ruidoso** porque depende de toda la trayectoria restante. La experiencia produce pares estado-retorno $\langle S_t,G_t\rangle$; en el terminal el valor futuro es cero.

$$
\Delta w=\alpha\bigl(G_t-\hat v(S_t,w)\bigr)
\nabla_w\hat v(S_t,w).
$$

> En el caso lineal:

$$
\Delta w=\alpha\bigl(G_t-x(S_t)^T w\bigr)x(S_t).
$$

> MC utiliza objetivos obtenidos de las recompensas reales, sin **bootstrapping**. Hay que esperar a disponer del retorno antes de actualizar. En el caso lineal, el aprendizaje puede converger al mínimo global del error de predicción; eso significa la mejor aproximación dentro de la familia elegida y con la ponderación de estados considerada, no necesariamente reproducir exactamente $v_\pi$.
>
> Con aproximadores no lineales, el problema se parece al ajuste supervisado mediante SGD: se conserva la interpretación de gradiente, pero no la garantía general de mínimo global.

#### 2. TD(0): objetivos con bootstrapping y semigradientes

> **TD(0)** usa la recompensa inmediata y el valor estimado del siguiente estado. Su objetivo de un paso es:

$$
R_{t+1}+\gamma\hat v(S_{t+1},w).
$$

> Los pares de entrenamiento tienen la forma $\langle S_t,R_{t+1}+\gamma\hat v(S_{t+1},w)\rangle$. En la última transición, el objetivo se reduce a $R_T$, porque el siguiente estado es terminal.
>
> El objetivo incorpora **sesgo** cuando la estimación del siguiente estado es incorrecta, pero suele tener menor varianza que el retorno completo. Definiendo el **error TD**:

$$
\delta_t=R_{t+1}+\gamma\hat v(S_{t+1},w)-\hat v(S_t,w),
$$

> La actualización es:

$$
\Delta w=\alpha\delta_t\nabla_w\hat v(S_t,w),
\qquad
\Delta w=\alpha\delta_t x(S_t)
\quad\text{en el caso lineal}.
$$

> Es un **semigradiente**: tratamos el objetivo como fijo al calcular la actualización, aunque contiene $\hat v(S_{t+1},w)$ y también depende de $w$. Derivamos la predicción del estado actual, sin derivar el término de bootstrapping. Por ello, no estamos siguiendo el gradiente completo del error cuadrático de ese objetivo dependiente de los pesos.
>
> TD permite actualizar tras cada transición. En predicción on-policy con aproximación lineal y condiciones adecuadas, converge a un punto fijo de TD. Este punto no tiene por qué ser el minimizador del error cuadrático de valor que alcanza MC. Con otras combinaciones de muestreo y aproximación, los pesos pueden divergir.

#### 3. Convergencia y la tríada de inestabilidad

> Las propiedades de convergencia dependen del **algoritmo**, del **aproximador** y de si aprendemos **on-policy** u **off-policy**. La tabla resume la situación de los métodos de predicción clásicos bajo sus hipótesis de aprendizaje:

| Muestreo | Algoritmo | Tabular | Lineal | No lineal |
| --- | --- | --- | --- | --- |
| On-policy | MC | Sí | Sí | Sí, con el alcance de SGD |
| On-policy | TD(0) | Sí | Sí | Sin garantía general |
| Off-policy | MC | Sí | Sí | Sí, con el alcance de SGD y corrección off-policy |
| Off-policy | TD(0) | Sí | Sin garantía general | Sin garantía general |

> [!warning] Corrección
> En el material aparece «NO» para predicción MC off-policy con aproximación no lineal, pero la entrada correcta en la tabla de convergencia es «Sí», bajo las condiciones de SGD y de corrección del muestreo off-policy. Esto no garantiza un mínimo global con cualquier red neuronal.
> Fuente de comprobación: [David Silver — Value Function Approximation](https://web.stanford.edu/class/cme241/lecture_slides/david_silver_slides/FA.pdf)

> Un «Sí» exige condiciones apropiadas sobre cobertura, pasos de aprendizaje y regularidad del aproximador. Un «Sin garantía general» indica que existen casos problemáticos, no que el método falle en todos los problemas. En particular, aprender off-policy requiere corregir la diferencia entre la política que genera los datos y la que se evalúa.
>
> La **tríada de inestabilidad** combina:

1. **Aproximación de funciones**, que acopla las estimaciones de estados diferentes.
2. **Bootstrapping**, que usa estimaciones actuales para construir nuevos objetivos.
3. **Aprendizaje off-policy**, que aprende sobre una política distinta de la que produce la experiencia.

> Su combinación puede generar realimentación de errores y divergencia, incluso con aproximación lineal. El **contraejemplo de Baird** muestra que aumentar la cantidad de actualizaciones TD no implica acercarnos a una solución: los parámetros crecen en magnitud y oscilan en lugar de estabilizarse.

![[apuntes-28d7026beba9-p0014-d917f00ac132.png]]

> El eje vertical de la figura es logarítmico, con una ruptura alrededor de $\pm1$. Las curvas $\theta_k(i)$ representan parámetros del contraejemplo; esa $\theta$ es la notación de la figura, equivalente al papel de los pesos $w$ en nuestra explicación. Las oscilaciones alcanzan órdenes de magnitud cada vez mayores.

### III. Control con aproximación

#### 1. De valores de estado a valores de acción

> Para elegir acciones sin un modelo del entorno resulta útil aproximar directamente $q_\pi(S,A)$:

$$
\hat q(S,A,w)\approx q_\pi(S,A),
\qquad
J(w)=\mathbb E_\pi\left[
\bigl(q_\pi(S,A)-\hat q(S,A,w)\bigr)^2\right].
$$

> Si dispusiéramos del valor real, la actualización estocástica sería:

$$
\Delta w=\alpha\bigl(q_\pi(S,A)-\hat q(S,A,w)\bigr)
\nabla_w\hat q(S,A,w).
$$

> El control combina **evaluación** y **mejora de política**: ajustamos $\hat q$ con experiencia y usamos sus valores para actuar, por ejemplo con una política $\varepsilon$-greedy. A medida que cambian los pesos, cambia también la política y, con ella, la función de valor que intentamos aproximar. Esta interacción es la **iteración generalizada de políticas** y hace el control más delicado que evaluar una política fija.

#### 2. SARSA con aproximación

> **Episodic Semi-gradient SARSA** usa la acción realmente seleccionada en el siguiente estado. Requiere una parametrización diferenciable $\hat q:\mathcal S\times\mathcal A\times\mathbb R^d\to\mathbb R$, un tamaño de paso $\alpha>0$ y un parámetro de exploración pequeño $\varepsilon>0$. Inicializamos $w$ arbitrariamente, por ejemplo a cero.

Para cada episodio:

1. Inicializamos $S$ y elegimos $A$ mediante la política de comportamiento, por ejemplo $\varepsilon$-greedy respecto a $\hat q(S,\cdot,w)$.
2. Ejecutamos $A$ y observamos la recompensa $R$ y el siguiente estado $S'$.
3. Si $S'$ es terminal, aplicamos la actualización final y comenzamos otro episodio:

$$
w\leftarrow w+\alpha\bigl[R-\hat q(S,A,w)\bigr]
\nabla_w\hat q(S,A,w).
$$

4. Si $S'$ no es terminal, elegimos $A'$ con la misma política a partir de $\hat q(S',\cdot,w)$.
5. Actualizamos los pesos:

$$
w\leftarrow w+\alpha\left[
R+\gamma\hat q(S',A',w)-\hat q(S,A,w)\right]
\nabla_w\hat q(S,A,w).
$$

6. Asignamos $S\leftarrow S'$ y $A\leftarrow A'$ y repetimos desde el paso 2.

> Todos los términos del lado derecho se calculan con los pesos previos a la actualización. La acción $A'$ se elige antes de cambiar $w$ y será la siguiente acción ejecutada. El caso terminal evita elegir una acción inexistente y elimina el valor futuro.
>
> SARSA es **on-policy** y utiliza **bootstrapping**. La diferencia respecto al caso tabular está en que el error modifica los parámetros compartidos del aproximador, mediante $\nabla_w\hat q$, en lugar de una sola casilla. La meta es obtener una función de acción-valor útil para el control; la aproximación no garantiza alcanzar exactamente $q_*$.

#### 3. Q-learning y convergencia del control

> **Q-learning** introduce aprendizaje off-policy en el control con valores de acción. La actividad propuesta consiste en identificar las líneas de SARSA que cambiarían y definir su adaptación a Q-learning.
>
> Las garantías tabulares no se trasladan automáticamente a los aproximadores. Para el control clásico:

| Algoritmo | Tabular | Lineal | No lineal |
| --- | --- | --- | --- |
| MC Control | Sí | Puede oscilar cerca de una solución aproximadamente óptima | Sin garantía general |
| SARSA | Sí | Puede oscilar cerca de una solución aproximadamente óptima | Sin garantía general |
| Q-learning | Sí | Sin garantía general | Sin garantía general |

> El «Sí» tabular presupone las condiciones correspondientes de exploración y pasos de aprendizaje. En el caso lineal de MC Control y SARSA, acercarse a una buena función de valor no equivale a permanecer en un punto fijo: la mejora de política y la evaluación pueden seguir produciendo oscilaciones. En Q-learning, la combinación de aproximación, bootstrapping y off-policy reúne la tríada de inestabilidad.

#### 4. Trabajo de la práctica 3

El trabajo indicado para la práctica es:

- Leer el apartado de **tile coding** de la sección 9.5.4 de Sutton y Barto.
- Realizar los ejercicios con el código que se entregará para la práctica.

> Los ejercicios y su código no están incluidos en estos materiales. El encargo establece una lectura y un trabajo posterior; no aporta soluciones que deban incorporarse aquí.

### IV. Batch RL y repetición de experiencia

#### 1. Motivación del aprendizaje por lotes

> El aprendizaje incremental muestra a muestra es sencillo y tiene un coste bajo por actualización. Sin embargo, una muestra puede utilizarse una sola vez y descartarse. Además, las transiciones consecutivas están correlacionadas, y en los métodos con bootstrapping los objetivos pueden cambiar junto con el aproximador.
>
> **Batch RL** permite ajustar la función a un conjunto de experiencias. Al reutilizarlas, extraemos más aprendizaje de cada interacción y podemos mezclar muestras obtenidas en momentos diferentes. Esto ayuda a reducir las correlaciones temporales, aunque no elimina por sí solo todos los problemas de estabilidad.

#### 2. Predicción por mínimos cuadrados y experience replay

> Consideramos el conjunto de pares estado-valor de referencia:

$$
\mathcal D=\{\langle s_1,v_1^\pi\rangle,
\langle s_2,v_2^\pi\rangle,\ldots,
\langle s_T,v_T^\pi\rangle\}.
$$

> Aquí $T$ denota el número de muestras del conjunto. Los $v_t^\pi$ son objetivos de referencia para la política, que en la práctica pueden proceder de retornos observados. La predicción por **mínimos cuadrados** busca:

$$
LS(w)=\sum_{t=1}^{T}
\bigl(v_t^\pi-\hat v(s_t,w)\bigr)^2,
\qquad
w^\pi=\arg\min_w LS(w).
$$

> Si interpretamos $\mathcal D$ como una distribución empírica uniforme, su error cuadrático medio es $LS(w)/T$. Suma y media difieren por una constante positiva y tienen el mismo minimizador.
>
> **Experience replay**, o repetición de experiencia, muestrea repetidamente del conjunto almacenado:

$$
\langle s,v^\pi\rangle\sim\mathcal D,
\qquad
\Delta w=\alpha\bigl(v^\pi-\hat v(s,w)\bigr)
\nabla_w\hat v(s,w).
$$

> Repetimos muestreo y actualización para ajustar el aproximador a todo el dataset. En el problema lineal con objetivos fijos y condiciones adecuadas de SGD, el proceso alcanza una solución de mínimos cuadrados. Para un aproximador no lineal no se garantiza encontrar el mínimo global; si los objetivos se recalculan mediante bootstrapping, también hay que considerar su evolución.

#### 3. Solución directa en el caso lineal

> Cuando $\hat v(s,w)=x(s)^T w$, podemos obtener la solución sin realizar muchas pasadas de SGD. En el mínimo, la actualización esperada es cero:

$$
\mathbb E_{\mathcal D}[\Delta w]=0
\quad\Longrightarrow\quad
\alpha\sum_{t=1}^{T}x(s_t)
\bigl(v_t^\pi-x(s_t)^T w\bigr)=0.
$$

> El factor de normalización del muestreo y $\alpha$ no afectan a esta igualdad. Separando ambos términos obtenemos las **ecuaciones normales**:

$$
\left[\sum_{t=1}^{T}x(s_t)x(s_t)^T\right]w
=\sum_{t=1}^{T}x(s_t)v_t^\pi.
$$

> Si la matriz es invertible:

$$
w^\pi=
\left[\sum_{t=1}^{T}x(s_t)x(s_t)^T\right]^{-1}
\sum_{t=1}^{T}x(s_t)v_t^\pi.
$$

> La invertibilidad exige que las muestras aporten información suficiente sobre las características; con características redundantes puede no haber una solución única. Si hay $N$ características, la resolución matricial directa tiene un coste típico $O(N^3)$, además del coste de acumular los datos. La estrategia **Sherman–Morrison** permite actualizar una inversa mediante cambios de rango uno con coste $O(N^2)$ por actualización. Ese coste se refiere a la actualización incremental, no a procesar un dataset arbitrario completo en tiempo independiente de su tamaño.

### V. Deep Q-Networks

#### 1. Objetivo, estado y arquitectura

> **Deep Q-Networks**, DQN, combina Q-learning con una red neuronal que aproxima los valores de acción. Su aplicación a Atari mostró cómo aprender a partir de imágenes con una misma arquitectura y procedimiento de entrenamiento en juegos diferentes. Cada juego requiere su propio aprendizaje; usar la misma arquitectura no significa compartir unos únicos pesos entrenados para todos ellos.
>
> La representación del estado se obtiene de la **imagen actual apilada con las tres anteriores**. Los cuatro frames aportan información temporal, como desplazamientos, que una sola imagen puede perder. La intención es disponer de una entrada suficientemente informativa para aproximar el comportamiento de un estado de Markov.
>
> Las acciones son las acciones válidas del joystick. El aproximador descrito tiene **tres capas convolucionales**, seguidas de **dos capas fully connected**, con activaciones **ReLU** en las capas ocultas y una **salida lineal por acción**. La red aprende características visuales y valores $Q$ conjuntamente.

![[apuntes-28d7026beba9-p0030-c999a17c14d4.png]]

> El esquema representa el flujo desde píxeles a características convolucionales y valores de acción, simplificando la profundidad de los bloques. Las salidas son valores esperados de retorno para cada acción disponible, no probabilidades de una softmax. A partir de esos valores se construye la política de comportamiento.

#### 2. Replay, red objetivo y actualización

> DQN almacena transiciones $(s,a,r,s')$ en una memoria de experiencia $D$ y extrae minibatches mediante muestreo uniforme, $U(D)$. **Experience replay** permite reutilizar interacciones y reduce la dependencia entre muestras consecutivas. Para estabilizar los objetivos utiliza además una **red objetivo** con parámetros $\theta_i^-$, mantenidos fijos durante las actualizaciones de la red que se entrena, cuyos parámetros son $\theta_i$.
>
> Para una transición no terminal, definimos:

$$
y_i=r+\gamma\max_{a'}Q(s',a';\theta_i^-).
$$

> Si $s'$ es terminal, $y_i=r$. La pérdida de batch Q-learning es:

$$
L_i(\theta_i)=
\mathbb E_{(s,a,r,s')\sim U(D)}\left[
\left(r+\gamma\max_{a'}Q(s',a';\theta_i^-)
-Q(s,a;\theta_i)\right)^2\right],
$$

> usando el objetivo terminal correspondiente cuando proceda. Al derivar respecto a $\theta_i$, $y_i$ se mantiene fijo porque procede de $\theta_i^-$. Por la regla de la cadena:

$$
\begin{aligned}
\nabla_{\theta_i}L_i(\theta_i)
&=-2\mathbb E_{(s,a,r,s')\sim U(D)}\left[
\bigl(y_i-Q(s,a;\theta_i)\bigr)
\nabla_{\theta_i}Q(s,a;\theta_i)\right],\\
-\frac12\nabla_{\theta_i}L_i(\theta_i)
&=\mathbb E_{(s,a,r,s')\sim U(D)}\left[
\bigl(y_i-Q(s,a;\theta_i)\bigr)
\nabla_{\theta_i}Q(s,a;\theta_i)\right].
\end{aligned}
$$

> [!warning] Corrección
> En el material aparece $\mathbb E[(y_i-Q)\nabla_{\theta_i}Q]$ como gradiente de la pérdida cuadrática, pero la expresión correcta es $\nabla_{\theta_i}L_i=-2\mathbb E[(y_i-Q)\nabla_{\theta_i}Q]$. La expresión original corresponde a $-\tfrac12\nabla_{\theta_i}L_i$, la dirección de descenso con el factor constante absorbido en el tamaño de paso.
> Fuente de comprobación: [David Silver — Value Function Approximation](https://web.stanford.edu/class/cme241/lecture_slides/david_silver_slides/FA.pdf)

> Replay y red objetivo cumplen funciones distintas: el primero reutiliza y mezcla la experiencia; la segunda reduce los cambios simultáneos del objetivo y de la predicción. DQN conserva aproximación no lineal, bootstrapping y aprendizaje off-policy, por lo que estas medidas de estabilización no constituyen una garantía universal de convergencia.

#### 3. Monitorización del aprendizaje

> La puntuación media por episodio es una medida natural de rendimiento, pero puede ser muy ruidosa. Los **valores de acción estimados promedio**, medidos de forma consistente, pueden aportar una señal más suave sobre la evolución del aprendizaje.

![[apuntes-28d7026beba9-p0032-252cd6d3f631.png]]

> En la figura, la puntuación por episodio fluctúa mucho después de mejorar inicialmente, mientras que el promedio de $Q$ presenta una evolución más regular. Conviene observar indicadores complementarios: una estimación de valor suave facilita el seguimiento, aunque su aumento por sí solo no demuestra que la política consiga mejores recompensas reales.

#### 4. Rendimiento en Atari

> La comparación entre **DQN** y el mejor aproximador lineal muestra resultados muy distintos según el juego. DQN supera el nivel humano en varios, pero queda por debajo en otros. Alcanzar buenos resultados en una suite diversa demuestra la utilidad del método sin implicar dominio uniforme de todas sus tareas.

![[apuntes-28d7026beba9-p0033-1f069b1ad6a5.png]]

> Las barras azules corresponden a DQN y las grises al mejor método lineal de la comparación. Los porcentajes representan puntuaciones normalizadas respecto al rendimiento humano, no probabilidades de ganar; el $100\%$ marca la referencia humana. La ruptura del eje permite representar juegos con resultados muy altos junto a los demás. La heterogeneidad es parte esencial del resultado: una arquitectura común puede ser eficaz y seguir teniendo dificultades importantes en determinados entornos.

### VI. Métodos de gradiente de política

#### 1. Aprender directamente el comportamiento

> Hasta ahora, la política se obtenía a partir de los valores de acción aproximados. Los **Policy Gradient Methods**, o métodos de gradiente de política, parametrizan y aprenden directamente la distribución de acciones:

$$
\pi(a\mid s,\theta)=
\Pr\{A_t=a\mid S_t=s,\theta_t=\theta\}.
$$

> El vector $\theta$ determina la política. Buscamos maximizar una medida escalar de rendimiento $J(\theta)$ mediante **ascenso del gradiente**:

$$
\theta_{t+1}=\theta_t+\alpha\widehat{\nabla J(\theta_t)}.
$$

> El signo positivo responde a que queremos aumentar el rendimiento. El sombrero indica una estimación del gradiente obtenida a partir de la experiencia. Cuando el aprendizaje de la política se apoya en un estimador de valor que proporciona la señal de actualización, hablamos de **actor-critic**. Esta familia combina una política explícita con aprendizaje de valor; su clasificación como familia separada o como variante de gradiente de política depende de la taxonomía utilizada.

#### 2. Preferencias de acción y softmax

> Para un espacio finito de acciones, una parametrización habitual aprende **preferencias** $h(s,a,\theta)$ y las transforma en probabilidades mediante **softmax**:

$$
\pi(a\mid s,\theta)=
\frac{e^{h(s,a,\theta)}}{\sum_b e^{h(s,b,\theta)}}.
$$

> Cada preferencia es una puntuación real para una acción; el conjunto de puntuaciones forma el vector de preferencias. La softmax garantiza probabilidades positivas cuya suma es uno. Las preferencias pueden proceder de una función lineal o de una red neuronal profunda y no tienen por qué ser valores de acción.

Este enfoque aporta varias ventajas:

- **Flexibilidad estocástica:** puede repartir probabilidad entre acciones con mucha más libertad que una política $\varepsilon$-greedy.
- **Suavidad:** pequeños cambios en preferencias diferenciables generan pequeños cambios en probabilidades. En $\varepsilon$-greedy, un cambio en la acción de mayor valor puede provocar un salto en el reparto de probabilidad.
- **Complejidad adecuada al problema:** la política puede resultar más sencilla de aproximar que toda la función $q$.
- **Incorporación de conocimiento previo:** la parametrización de la política puede expresar estructuras o restricciones útiles del comportamiento.

> La suavidad facilita el ajuste, pero no garantiza por sí sola una política óptima. El conocimiento previo se incorpora aquí al diseño de la política; la recompensa sigue expresando el objetivo del problema, sin sustituirlo por instrucciones que impongan cómo debe actuar el agente.

#### 3. Objetivo episódico y teorema del gradiente de política

> Para un problema episódico con estado inicial $s_0$, tomamos como rendimiento:

$$
J(\theta)=v_{\pi_\theta}(s_0).
$$

> El rendimiento depende de las acciones elegidas y de los estados que llegan a visitarse. Cambiar $\theta$ modifica ambas cosas: la distribución de estados está determinada conjuntamente por la política y las transiciones del entorno. Diferenciar únicamente la probabilidad de una acción ignorando ese efecto sería insuficiente.
>
> El **Policy Gradient Theorem** permite expresar el gradiente sin derivar explícitamente la distribución de visitas:

$$
\nabla J(\theta)\propto
\sum_s\mu(s)\sum_a q_\pi(s,a)
\nabla_\theta\pi(a\mid s,\theta).
$$

> $\mu(s)$ representa la distribución de visitas relevante bajo la política actual y $q_\pi(s,a)$ su valor de acción. La distribución depende de $\theta$, aunque su derivada no aparezca en esta expresión del teorema. El gradiente $\nabla_\theta\pi$ indica cómo los parámetros cambian la probabilidad de cada acción.
>
> La proporcionalidad procede de la normalización de las visitas; el factor positivo de escala puede incorporarse al tamaño de paso. Por eso basta estimar una dirección proporcional al gradiente para actualizar la política.
>
> Las actualizaciones compactas de REINFORCE que siguen se interpretan directamente para el caso episódico **sin descuento**, $\gamma=1$. Con un objetivo descontado desde $s_0$, la distribución de visitas debe incorporar el descuento; al sumar actualizaciones de una trayectoria desde su inicio, aparece además la ponderación temporal $\gamma^t$. Esa ponderación no es una única constante que pueda absorberse en $\alpha$ para todos los pasos.

### VII. REINFORCE y reducción de varianza

#### 1. Del teorema a un gradiente estimable

> El teorema contiene una suma sobre todas las acciones. Podemos convertirla en una esperanza sobre acciones muestreadas de $\pi$ multiplicando y dividiendo por su probabilidad. Para las acciones del soporte de la política:

$$
\begin{aligned}
\sum_a q_\pi(S_t,a)\nabla_\theta\pi(a\mid S_t,\theta)
&=\sum_a\pi(a\mid S_t,\theta)q_\pi(S_t,a)
\frac{\nabla_\theta\pi(a\mid S_t,\theta)}{\pi(a\mid S_t,\theta)}.
\end{aligned}
$$

> Muestreando $A_t\sim\pi(\cdot\mid S_t,\theta)$ y usando $\mathbb E_\pi[G_t\mid S_t,A_t]=q_\pi(S_t,A_t)$:

$$
\begin{aligned}
\nabla J(\theta)
&\propto\mathbb E_\pi\left[
q_\pi(S_t,A_t)
\frac{\nabla_\theta\pi(A_t\mid S_t,\theta)}
{\pi(A_t\mid S_t,\theta)}\right]\\
&=\mathbb E_\pi\left[
G_t\frac{\nabla_\theta\pi(A_t\mid S_t,\theta)}
{\pi(A_t\mid S_t,\theta)}\right].
\end{aligned}
$$

> El cociente es la **score function** de la política:

$$
\nabla_\theta\ln\pi(A_t\mid S_t,\theta)
=\frac{\nabla_\theta\pi(A_t\mid S_t,\theta)}
{\pi(A_t\mid S_t,\theta)}.
$$

> Esta identidad permite trabajar con el logaritmo de la probabilidad de la acción elegida. La sustitución de $q_\pi$ por $G_t$ evita tener que conocer o aproximar explícitamente la función de acción-valor.

#### 2. Regla de actualización e interpretación

> **REINFORCE** aplica ascenso estocástico con el retorno observado:

$$
\begin{aligned}
\theta_{t+1}
&=\theta_t+\alpha G_t
\frac{\nabla_\theta\pi(A_t\mid S_t,\theta_t)}
{\pi(A_t\mid S_t,\theta_t)}\\
&=\theta_t+\alpha G_t
\nabla_\theta\ln\pi(A_t\mid S_t,\theta_t).
\end{aligned}
$$

> El retorno pondera la modificación de la probabilidad de la acción tomada. Un retorno positivo impulsa el movimiento que aumenta esa probabilidad; uno negativo impulsa el contrario. La mejora esperada surge de combinar muestras: un solo episodio no identifica con certeza qué acciones fueron mejores.
>
> REINFORCE es **on-policy**, porque la experiencia se genera con la política cuyo gradiente se estima, y es un método **Monte Carlo**, sin bootstrapping. En un episodio, recogemos la trayectoria con la política, esperamos al final para calcular los retornos y los usamos para sus actualizaciones. Hay que mantener la correspondencia entre la política que genera los datos y la que se utiliza para estimar el gradiente.
>
> Las actualizaciones requieren el retorno completo, por lo que no se realizan inmediatamente tras cada transición. Esto no convierte al método en *offline RL* en el sentido de aprender exclusivamente de un dataset fijo: REINFORCE puede recoger episodios nuevos durante el entrenamiento, aunque actualice después de cada episodio.

#### 3. Sensibilidad al tamaño de paso

> El retorno introduce varianza en el gradiente. El tamaño de paso debe equilibrar rapidez y estabilidad: aumentarlo no asegura aprender mejor. La comparación siguiente muestra el retorno inicial $G_0$ promedio sobre cien ejecuciones con distintos valores de $\alpha$.

![[apuntes-f906f4d988da-p0011-785f9cb059cd.png]]

> En este ejemplo, $\alpha=2^{-13}$ aprende más rápido que $2^{-14}$ y ambas curvas se acercan a la referencia $v_*(s_0)$. El paso mayor, $2^{-12}$, se queda alrededor de un rendimiento mucho peor. Son resultados de ese problema, no valores recomendados de $\alpha$ para cualquier entorno. Como las recompensas son negativas, acercarse a $-10$ representa una mejora respecto a $-40$.

#### 4. REINFORCE con baseline

> Podemos restar una **baseline**, o línea base, $b(s)$ al valor de acción sin cambiar el gradiente esperado:

$$
\nabla J(\theta)\propto
\sum_s\mu(s)\sum_a
\bigl(q_\pi(s,a)-b(s)\bigr)
\nabla_\theta\pi(a\mid s,\theta).
$$

> La condición esencial es que $b(s)$ **no dependa de la acción**. Para un estado fijo, su contribución se anula porque las probabilidades suman uno:

$$
\sum_a b(s)\nabla_\theta\pi(a\mid s,\theta)
=b(s)\nabla_\theta\sum_a\pi(a\mid s,\theta)
=b(s)\nabla_\theta 1=0.
$$

> La actualización queda:

$$
\theta_{t+1}=\theta_t+\alpha
\bigl(G_t-b(S_t)\bigr)
\nabla_\theta\ln\pi(A_t\mid S_t,\theta_t).
$$

> La baseline permite comparar el retorno con lo esperado en ese estado. Una acción puede reforzarse si su retorno supera la referencia aunque ambos sean negativos; por ejemplo, un retorno $-10$ frente a una baseline $-20$ produce una diferencia positiva. Una baseline bien elegida **reduce la varianza**; una arbitraria conserva la cancelación anterior, pero no necesariamente mejora la varianza.
>
> Una elección habitual es $b(s)=\hat v(s,w)$, aprendida mediante los retornos. La estimación de valor se ajusta con el error $G_t-\hat v(S_t,w)$, mientras la política usa ese error como señal comparativa. Al aprender ambas funciones necesitamos dos tamaños de paso, $\alpha^\theta$ y $\alpha^w$:

$$
\begin{aligned}
w&\leftarrow w+\alpha^w
\bigl(G_t-\hat v(S_t,w)\bigr)\nabla_w\hat v(S_t,w),\\
\theta&\leftarrow\theta+\alpha^\theta
\bigl(G_t-\hat v(S_t,w)\bigr)
\nabla_\theta\ln\pi(A_t\mid S_t,\theta).
\end{aligned}
$$

> Las dos actualizaciones utilizan la misma diferencia $G_t-\hat v(S_t,w)$, calculada antes de modificar los pesos. La señal del actor se calcula manteniendo la baseline como referencia, sin derivarla como parte de la score function. REINFORCE con baseline sigue usando el retorno completo: disponer de una estimación de valor para restar una referencia no introduce por sí solo el bootstrapping propio del actor-crítico.

![[apuntes-f906f4d988da-p0013-b75ffbbf838a.png]]

> La curva verde alcanza rápidamente un rendimiento próximo a $v_*(s_0)$, mientras REINFORCE sin baseline tarda muchos más episodios. La comparación ilustra la mejora que puede aportar la reducción de varianza. Los dos tamaños de paso de la variante con baseline controlan aprendizajes distintos y también deben ajustarse.

### VIII. Métodos actor-crítico

#### 1. Funciones del actor y del crítico

> **Actor-critic** reemplaza el retorno completo por una estimación que utiliza bootstrapping. El **actor**, parametrizado por $\theta$, representa la política y selecciona acciones. El **critic**, parametrizado por $w$, estima valores y proporciona la señal que orienta la actualización del actor.
>
> En la variante de un paso, el crítico estima $v(s)$, usa su valor como baseline y forma una estimación de $q(s,a)$ a partir de la recompensa y del siguiente estado. Esto permite actualizar tras cada transición. Se reduce normalmente la varianza respecto al retorno MC completo, a cambio de introducir sesgo por la aproximación del crítico; el resultado depende de la calidad de esa estimación.

![[apuntes-f906f4d988da-p0016-bc69f99022f8.png]]

> El entorno devuelve estados y recompensas. El actor utiliza el estado para elegir una acción; el crítico usa la transición para calcular un **error TD** $\delta$, que modifica tanto su propia estimación como la política. La recompensa y el error TD tienen papeles distintos: este último compara lo recibido con lo que se esperaba.

#### 2. Error TD como estimación de ventaja

> El retorno de un paso se escribe $G_{t:t+1}=R_{t+1}+\gamma\hat v(S_{t+1},w)$. Al restar la baseline del estado actual:

$$
\begin{aligned}
\theta_{t+1}
&=\theta_t+\alpha
\bigl(G_{t:t+1}-\hat v(S_t,w)\bigr)
\frac{\nabla_\theta\pi(A_t\mid S_t,\theta_t)}
{\pi(A_t\mid S_t,\theta_t)}\\
&=\theta_t+\alpha
\bigl(R_{t+1}+\gamma\hat v(S_{t+1},w)-\hat v(S_t,w)\bigr)
\nabla_\theta\ln\pi(A_t\mid S_t,\theta_t)\\
&=\theta_t+\alpha\delta_t
\nabla_\theta\ln\pi(A_t\mid S_t,\theta_t).
\end{aligned}
$$

> La **ventaja** de una acción compara su valor con el valor medio del estado: $q_\pi(s,a)-v_\pi(s)$. Si el crítico fuera exacto, la esperanza del error TD condicionada al estado y a la acción coincidiría con esa diferencia. Por eso $\delta_t$ sirve como una estimación de ventaja: con $\delta_t>0$, la transición resulta mejor de lo esperado y el actor aumenta la probabilidad de la acción elegida; con $\delta_t<0$, la reduce.
>
> Esta es la actualización local del actor utilizada en el algoritmo de un paso. Mantener $\gamma$ en el objetivo TD permite descontar el valor futuro del crítico; si se pretende estimar exactamente el gradiente del objetivo descontado desde $s_0$, también se aplica la ponderación temporal descrita antes.

#### 3. Algoritmo actor-crítico de ventaja a un paso

> Requerimos una política diferenciable $\pi_\theta$, un aproximador diferenciable $v_w$, parámetros iniciales $\theta$ y $w$, y tamaños de paso $\alpha$ para el actor y $\beta$ para el crítico. $v_w(S)$ es otra notación para la aproximación $\hat v(S,w)$.

Para cada episodio, inicializamos $S_0$ y repetimos:

1. Muestreamos $A_t\sim\pi_\theta(\cdot\mid S_t)$.
2. Ejecutamos la acción y observamos $R_{t+1}$ y $S_{t+1}$.
3. Calculamos el error TD con los pesos actuales:

$$
\delta_t=R_{t+1}+\gamma v_w(S_{t+1})-v_w(S_t).
$$

4. Actualizamos el crítico:

$$
w\leftarrow w+\beta\delta_t\nabla_w v_w(S_t).
$$

5. Actualizamos el actor usando el mismo error TD ya calculado:

$$
\theta\leftarrow\theta+\alpha\delta_t
\nabla_\theta\log\pi_\theta(A_t\mid S_t).
$$

6. Continuamos desde $S_{t+1}$; si es terminal, finalizamos el episodio e inicializamos el siguiente.

> En el terminal fijamos $v_w(S_{t+1})=0$, por lo que $\delta_t=R_{t+1}-v_w(S_t)$. Se efectúan las dos actualizaciones de esa última transición antes de reiniciar. El error se calcula antes de modificar los pesos y se reutiliza en ambos aprendizajes; no se recalcula con el crítico recién actualizado.
>
> El resultado son una política aprendida y un crítico que evalúa esa política. Sus procesos están acoplados: cambiar el actor modifica la experiencia y el valor que el crítico debe aprender. Los tamaños de paso permiten controlar cada aprendizaje por separado, y la actualización de un paso no garantiza por sí sola convergencia u optimalidad con cualquier parametrización.

### IX. Extensiones, estabilidad y acciones continuas

#### 1. Retornos más largos y experiencia condicionada por la política

> El enfoque puede utilizar el **retorno $\lambda$** e implementarse mediante **trazas de elegibilidad**. Esto conecta las actualizaciones de un paso con el uso de información de horizontes más largos y permite ajustar el equilibrio entre bootstrapping y retorno observado.
>
> En los métodos de gradiente de política, la política determina qué experiencia obtiene el agente. Una actualización brusca puede llevarlo a visitar estados poco útiles o a dejar de explorar comportamientos relevantes. El entrenamiento puede deteriorarse porque las siguientes actualizaciones se alimentan precisamente de esa nueva experiencia. El problema afecta a la dinámica completa de aprendizaje, además de al rendimiento inmediato de una política.

#### 2. Regularización de los cambios de política

> Para limitar movimientos excesivos podemos penalizar la diferencia entre la política anterior y la candidata. La **divergencia de Kullback–Leibler**, $D_{\mathrm{KL}}$, compara sus distribuciones de acciones. La idea de objetivo regularizado es:

$$
J-\eta D_{\mathrm{KL}},\qquad \eta>0.
$$

> Al maximizarlo, buscamos una mejora de rendimiento que compense el cambio de distribución. Un $\eta$ mayor penaliza más los movimientos grandes; uno menor deja más libertad. La KL no es una distancia simétrica: importa el orden de las distribuciones, y la comparación debe especificar cómo se consideran los estados.
>
> Esta intuición está detrás de **TRPO** y **PPO**: controlar cuánto cambia la política en cada actualización. La expresión anterior ilustra la idea de regularización; no define por sí sola todos los detalles de esos algoritmos ni implica que sus objetivos sean idénticos.

#### 3. Políticas para espacios de acción continuos

> Una alternativa para acciones continuas es **discretizarlas**, incluso con una resolución gruesa si resulta adecuada al problema. Los métodos de gradiente de política también permiten representar directamente una distribución continua y aprender sus parámetros.
>
> Para una acción escalar y una distribución normal, la política tiene densidad:

$$
\pi(a\mid s,\theta)=
\frac{1}{\sigma(s,\theta)\sqrt{2\pi}}
\exp\left[-\frac{\bigl(a-\mu(s,\theta)\bigr)^2}
{2\sigma(s,\theta)^2}\right].
$$

> $\mu(s,\theta)$ es la **media** y $\sigma(s,\theta)>0$ la **desviación típica**. Aquí $\mu$ representa la media de una normal, no la distribución de visitas del teorema. El aproximador produce esos parámetros en función del estado y se muestrea una acción de la distribución resultante.
>
> En un espacio continuo, $\pi(a\mid s,\theta)$ es una **densidad**, no la probabilidad de elegir exactamente un valor aislado. La probabilidad de un intervalo se obtiene integrando la densidad. La misma idea de score function permite calcular cómo ajustar los parámetros de la distribución para mejorar el rendimiento.

### X. Resumen Final

> La aproximación sustituye tablas por parámetros compartidos y permite generalizar a espacios grandes. Su utilidad depende tanto de la representación del estado como del método de aprendizaje. El caso tabular se recupera mediante características one-hot, sin generalización entre estados.
>
> **MC** aprende con retornos completos y sigue un gradiente de error de predicción; **TD** usa bootstrapping y semigradientes. La menor varianza y la actualización inmediata de TD se acompañan de sesgo y de riesgos de estabilidad. Aproximación, bootstrapping y off-policy forman la tríada especialmente problemática.
>
> En control, **SARSA** aprende de las acciones de su propia política y **Q-learning** separa el comportamiento del objetivo de aprendizaje. Las garantías tabulares no se heredan automáticamente al usar aproximadores. **Batch RL** y **experience replay** reutilizan datos; **DQN** combina replay, una red de valores de acción y objetivos calculados con una red fija temporalmente.
>
> Los métodos de **gradiente de política** aprenden directamente $\pi_\theta$ mediante ascenso del rendimiento. El teorema permite construir estimadores a partir de experiencia sin diferenciar explícitamente la distribución de visitas. **REINFORCE** usa $G_t\nabla\ln\pi$; una **baseline independiente de la acción** conserva el gradiente esperado y puede reducir su varianza.
>
> **Actor-critic** introduce bootstrapping y utiliza el error TD como estimación de ventaja para actualizar tras cada transición. Su actor y su crítico se influyen mutuamente. Controlar cambios de política ayuda a mantener experiencia útil; parametrizar distribuciones continuas extiende el mismo enfoque a acciones continuas.
