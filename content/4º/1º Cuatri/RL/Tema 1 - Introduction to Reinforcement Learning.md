---
estado: pendiente de revisión
---

### I. Introducción al aprendizaje por refuerzo

#### 1. Aprender mediante interacción

> El **aprendizaje por refuerzo** (*reinforcement learning*, RL) estudia cómo un **agente** aprende a elegir acciones al interactuar con un **entorno**. Cada decisión produce una **recompensa** que evalúa su resultado. El objetivo no es acertar una etiqueta conocida de antemano, sino aprender una forma de actuar que acumule buenos resultados a lo largo del tiempo.

> La intuición es la del ensayo y error: una acción prometedora se repite, pero también conviene probar alternativas porque una recompensa inmediata no revela por sí sola cuál es la mejor decisión. Las escenas de supervivencia que introducen el tema sirven para ilustrar esa búsqueda de conductas favorables a partir de la experiencia.

> La **dopamina** es un neurotransmisor relacionado con el sistema biológico de recompensa; se mencionan las neuronas dopaminérgicas del área tegmental ventral (**ATV**) como analogía para motivar el papel de la realimentación. En RL, la recompensa es una señal matemática del problema, no una descripción literal de cómo funciona el cerebro.

#### 2. RL en el mapa del aprendizaje automático

| Enfoque | Información que guía el aprendizaje | Pregunta principal |
| --- | --- | --- |
| Aprendizaje supervisado | Ejemplos con etiquetas | ¿Qué salida corresponde a una entrada? |
| Aprendizaje no supervisado | Datos sin etiquetas | ¿Qué estructura contienen los datos? |
| Aprendizaje por refuerzo | Experiencia obtenida al actuar y recompensas | ¿Qué acción conviene elegir para lograr un buen resultado? |

> La diferencia decisiva es que en RL el agente **interviene** en la generación de su experiencia. Sus acciones determinan qué recompensas observará y, en el caso general, qué estados encontrará más adelante. Una recompensa evalúa la acción, pero no indica necesariamente cuál habría sido la mejor entre todas las alternativas.

#### 3. Evolución y aplicaciones

> A finales de los años ochenta convergieron tres líneas de investigación: el **control óptimo** mediante programación dinámica, el aprendizaje por **ensayo y error** estudiado en psicología animal y los métodos de **diferencia temporal**, que conectan ideas de las dos anteriores. La dificultad para escalar a problemas grandes fue durante mucho tiempo una limitación importante.

> La publicación de **DQN** por Mnih y colaboradores en 2015 mostró el potencial de combinar redes profundas con RL para el control a partir de observaciones complejas. Después aparecieron variantes como **Double DQN** y sistemas de juego como **AlphaGo** y **AlphaZero**. Herramientas como `gym` y `baselines` facilitaron construir y comparar experimentos.

> Otro ejemplo de aplicación es el ajuste de modelos de lenguaje mediante **realimentación humana** (*RLHF*). El esquema mostrado sigue tres pasos: primero se ajusta un modelo con demostraciones supervisadas; después se entrena un modelo de recompensa con comparaciones ordenadas por personas; finalmente se optimiza la política generadora frente a esa recompensa mediante **PPO**. La función de recompensa aprendida sirve como señal de entrenamiento para mejorar las respuestas.

> [!warning] Corrección
> En el material aparece AlphaFold agrupado con AlphaGo y AlphaZero como contribución al aprendizaje por refuerzo, pero AlphaFold es un sistema de predicción de estructuras de proteínas entrenado con aprendizaje supervisado y autodestilación, no un ejemplo de RL.
> Fuente de comprobación: [Jumper y colaboradores, Nature](https://www.nature.com/articles/s41586-021-03819-2).

> El RL también se aplica a decisiones industriales y de negocio en las que se obtiene información mientras se actúa. Entre los ejemplos del tema figuran la selección de anuncios y noticias, la medicina personalizada y los ensayos clínicos, y las decisiones de cartera. La formulación concreta de cada caso determina si basta un *bandit* o si es necesario modelar estados y consecuencias futuras.

### II. Interacción entre agente y entorno

#### 4. El ciclo general

> En el instante $t$, el agente recibe información sobre el estado $s_t$ y escoge una acción $a_t$. El entorno responde con una recompensa $r_{t+1}$ y un estado siguiente $s_{t+1}$. La interacción se repite: la nueva situación condiciona la próxima decisión.

![[Pasted image 20260930164500.png]]

> El esquema distingue dos componentes del entorno: el **proceso de recompensa**, que evalúa la acción, y el **proceso de transición de estado**, que determina la siguiente situación. Una acción puede afectar tanto a lo que se gana ahora como a las oportunidades futuras. Por ello, una decisión con recompensa inmediata alta no tiene por qué ser la mejor en un problema secuencial.

#### 5. La simplificación del bandit de $k$ brazos

> Para estudiar primero las decisiones sin consecuencias sobre el estado, se considera un **bandit de $k$ brazos** (*$k$-armed bandit*). En cada paso se elige una de $k$ acciones y se recibe una recompensa. Se elimina del problema el efecto de la acción sobre futuras transiciones de estado.

> Esta simplificación permite concentrarse en cuatro ideas básicas: **recompensa**, **valor de acción**, **estimación** de ese valor y equilibrio entre **exploración** y **explotación**. Puede representar, por ejemplo, la elección entre anuncios cuando interesa aprender cuál recibe mejor respuesta. La aplicación exige comprobar si el contexto y el estado futuro realmente pueden ignorarse.

### III. Valoración de acciones

#### 6. Valor verdadero y estimación

> En un bandit estacionario, el **valor verdadero** de la acción $a$ es la recompensa esperada al elegirla:

$$
q_*(a) \doteq \mathbb{E}[R_t\mid A_t=a].
$$

> $A_t$ representa la acción elegida y $R_t$ la recompensa usada en esta definición. El valor $q_*(a)$ es una propiedad desconocida de la distribución de recompensas: no se obtiene observando una única muestra. El agente mantiene una **estimación** $Q_t(a)$ basada en las recompensas que ha visto antes del paso $t$.

> En el ejemplo de las tres marcas de jamón, los valores verdaderos ilustrativos son $q_*(5J)=9{,}5$, $q_*(Jlt)=9{,}2$ y $q_*(Cv)=8{,}9$. Una valoración observada, como $9{,}7$ para 5J, $9{,}8$ para Joselito o $9{,}1$ para Covap, no coincide necesariamente con su media verdadera. Hay que aprender $Q_t(5J)$, $Q_t(Jlt)$ y $Q_t(Cv)$ a partir de las valoraciones obtenidas.

> Si se conocieran los valores verdaderos, la mejor acción del ejemplo sería $\arg\max_a q_*(a)$. El agente real solo dispone de estimaciones. La **política greedy** selecciona la acción con mayor valor estimado:

$$
A_t \doteq \arg\max_a Q_t(a).
$$

> [!warning] Corrección
> En el material aparece «política greedy: $a_t=\arg\max_a q_*(a)$», pero la regla que puede ejecutar el agente es $A_t=\arg\max_a Q_t(a)$; maximizar $q_*(a)$ describe la acción óptima si se conocen los valores verdaderos.
> Fuente de comprobación: [Sutton y Barto, Reinforcement Learning: An Introduction, sección 2.2](https://www.incompleteideas.net/book/bookdraft2018mar21.pdf).

#### 7. Promedio muestral e incremento

> Una estimación directa consiste en promediar todas las recompensas recibidas al elegir una acción. Si se ha elegido esa acción $n$ veces y se han observado $R_1,\ldots,R_n$, el promedio tras la observación $n$ es

$$
Q_{n+1}=\frac{1}{n}\sum_{i=1}^{n}R_i.
$$

> La misma estimación se puede actualizar sin almacenar toda la historia. Para $n>1$, usamos $\sum_{i=1}^{n-1}R_i=(n-1)Q_n$:

$$
\begin{aligned}
Q_{n+1}
&=\frac{(n-1)Q_n+R_n}{n}\\
&=Q_n+\frac{1}{n}\left[R_n-Q_n\right].
\end{aligned}
$$

> El término $R_n-Q_n$ es el **error de estimación** observado: si la recompensa supera la estimación, esta sube; si queda por debajo, baja. La actualización sigue una estructura que reaparece en RL:

$$
\text{NewEstimate}\leftarrow
\text{OldEstimate}+\text{StepSize}
\left[\text{Target}-\text{OldEstimate}\right].
$$

> La limitación del promedio muestral es que todas las observaciones conservan el mismo peso. Si las recompensas de una acción cambian con el tiempo, las muestras antiguas pueden retrasar la adaptación; además, el tamaño de paso $1/n$ disminuye conforme aumenta el número de elecciones.

#### 8. Paso constante y ponderación por recencia

> Para dar más importancia a la información reciente, se usa un **tamaño de paso constante** $\alpha$, normalmente entre $0$ y $1$:

$$
Q_{n+1}=Q_n+\alpha\left[R_n-Q_n\right]
       =(1-\alpha)Q_n+\alpha R_n.
$$

> Al sustituir de nuevo la misma expresión para $Q_n$ y repetir el proceso se obtiene

$$
Q_{n+1}
=(1-\alpha)^nQ_1+
\sum_{i=1}^{n}\alpha(1-\alpha)^{n-i}R_i.
$$

> Por tanto, el peso de una recompensa disminuye **exponencialmente con su antigüedad**. El método puede seguir cambios recientes del entorno porque mantiene un peso $\alpha$ para cada nueva recompensa. A cambio, con $\alpha$ constante la estimación continúa fluctuando alrededor del valor medio incluso en un entorno estacionario.

#### 9. Paso variable y condiciones de convergencia

> También puede elegirse un tamaño de paso $\alpha_n(a)$ diferente para cada acción y para cada actualización. Las condiciones indicadas para la convergencia de estimaciones estocásticas son

$$
\sum_{n=1}^{\infty}\alpha_n(a)=\infty,
\qquad
\sum_{n=1}^{\infty}\alpha_n^2(a)<\infty.
$$

> La primera condición impide que las actualizaciones acumuladas se agoten demasiado pronto; la segunda hace que el efecto acumulado del ruido sea limitado. El promedio muestral, con $\alpha_n(a)=1/n$ para la $n$-ésima muestra de $a$, satisface ambas. Estas condiciones se interpretan bajo las hipótesis de un problema estacionario y muestras apropiadas, no como una promesa de convergencia para cualquier entorno cambiante.

### IV. Exploración y explotación

#### 10. El dilema

> **Explotar** consiste en elegir la acción que parece mejor con la información actual. **Explorar** consiste en probar una acción incierta para obtener información que pueda mejorar decisiones posteriores. La dificultad es que cada paso dedicado a explorar puede reducir la recompensa inmediata, mientras que evitar la exploración puede dejar al agente atrapado en una alternativa inferior.

> Una política puramente greedy puede descartar una acción por unas primeras recompensas bajas aunque su valor verdadero sea alto. El problema no es solo estimar los brazos que se usan mucho: también hay que decidir **cuándo recoger evidencia sobre los poco probados**.

#### 11. Política $\varepsilon$-greedy

> La política **$\varepsilon$-greedy** elige una acción greedy con probabilidad $1-\varepsilon$ y, con probabilidad $\varepsilon$, selecciona una de las $n$ acciones uniformemente al azar (aquí $n=k$). Si hay una única acción greedy, su probabilidad total es

$$
P(\text{acción greedy})=1-\varepsilon+\frac{\varepsilon}{n}
=1-\frac{n-1}{n}\varepsilon,
$$

> mientras que cada una de las otras acciones tiene probabilidad $\varepsilon/n$. La acción greedy también puede salir en la elección aleatoria, de ahí el sumando $\varepsilon/n$. Para $\varepsilon=0$ se recupera la selección greedy; un $\varepsilon$ mayor dedica más pasos a explorar.

#### 12. Valores iniciales optimistas

> Otra manera de inducir exploración consiste en inicializar $Q_1(a)$ **por encima** de los valores que se esperan de las acciones. Una política greedy que acaba de probar un brazo puede ver disminuir su estimación y pasar a probar otro brazo todavía optimista. Así se exploran alternativas sin elegir acciones al azar en cada paso.

> En la comparación del tema se utiliza $Q_1=5$ y $\varepsilon=0$ frente a una inicialización $Q_1=0$ con $\varepsilon=0{,}1$, ambas con $\alpha=0{,}1$. El efecto exploratorio de la inicialización se va perdiendo cuando los valores se corrigen con experiencia: por eso este recurso no reacciona por sí solo a un cambio tardío del entorno.

#### 13. Límites de confianza superiores

> Los **límites de confianza superiores** (*upper confidence bounds*, **UCB**) añaden a la estimación una bonificación por incertidumbre. La selección del tema es

$$
A_t\doteq
\arg\max_a
\left[
Q_t(a)+c\sqrt{\frac{\ln t}{N_t(a)}}
\right],
$$

> donde $N_t(a)$ es el número de veces que se eligió $a$ antes de $t$ y $c$ controla la intensidad de la exploración. Para un brazo poco probado, el segundo término es grande; al acumular observaciones, disminuye. Cuando $N_t(a)=0$, la expresión se trata aparte, seleccionando los brazos aún no probados antes de aplicar la fórmula.

> UCB dirige la exploración hacia acciones que combinan buen valor estimado e incertidumbre. En el banco de pruebas estacionario del tema puede superar a $\varepsilon$-greedy. Su término de confianza se basa en el historial acumulado, por lo que también pierde sensibilidad a cambios tardíos; extender esta regla a espacios de acciones complejos y aproximación de funciones es difícil.

### V. Banco de pruebas de diez brazos

#### 14. Construcción del problema

> El **bandit de diez brazos** fija un banco de pruebas para comparar políticas. Se asigna a cada brazo un valor verdadero independiente $q_*(a)$ muestreado de una normal $\mathcal N(0,1)$. Después, al elegir $a$, la recompensa se extrae de $\mathcal N(q_*(a),1)$.

![[Pasted image 20260930164501.png]]

> Cada distribución vertical representa las recompensas posibles de un brazo: su centro es $q_*(a)$ y la dispersión hace que una muestra individual sea incierta. El algoritmo conoce las recompensas que obtiene, no los centros verdaderos. Los resultados siguientes agregan **2000 ejecuciones** y muestran el comportamiento a lo largo de **1000 pasos**.

#### 15. Comparación de $\varepsilon$-greedy

> Con evaluación mediante promedio muestral, se comparan $\varepsilon=0$, $\varepsilon=0{,}01$ y $\varepsilon=0{,}1$. La gráfica izquierda mide **recompensa media**; la derecha, el **porcentaje de elecciones de la acción óptima**, identificada mediante los valores verdaderos del banco de pruebas.

![[Pasted image 20260930164502.png]]

> La política puramente greedy mejora al principio, pero se estanca al dejar de investigar otros brazos. En este experimento, $\varepsilon=0{,}1$ aprende a elegir la acción óptima con mayor frecuencia y consigue mejor recompensa media en el horizonte mostrado. $\varepsilon=0{,}01$ progresa más lentamente: explora menos, pero continúa descubriendo acciones mejores.

#### 16. Efecto de la inicialización optimista

> Con un paso constante $\alpha=0{,}1$, la política greedy con $Q_1=5$ se compara con $\varepsilon$-greedy inicializada en $Q_1=0$. La métrica representada es el porcentaje de elecciones óptimas.

![[Pasted image 20260930164503.png]]

> El inicio optimista provoca una fase temprana de prueba de brazos y, tras ella, alcanza una proporción mayor de elecciones óptimas en este experimento. El descenso y posterior recuperación inicial de la curva optimista reflejan el ajuste de estimaciones exageradas. El resultado muestra el valor de explorar al principio; no implica que el mismo ajuste sirva para un entorno que cambia después.

#### 17. Comparación de UCB

> La comparación de **UCB con $c=2$** frente a **$\varepsilon$-greedy con $\varepsilon=0{,}1$** utiliza como eje vertical la recompensa media.

![[Pasted image 20260930164504.png]]

> En este banco de pruebas, UCB acaba por alcanzar una recompensa media mayor. La bonificación del recuento concentra las pruebas en brazos todavía inciertos, en vez de repartir toda la exploración uniformemente. La ventaja observada depende de esta configuración y de sus hipótesis de estacionariedad.

### VI. Del bandit asociativo al RL general

#### 18. Contexto y transición de estado

> Un **bandit asociativo** o *contextual bandit* añade una situación observable antes de escoger la acción. La decisión puede depender del estado o contexto recibido, y la recompensa de la acción puede variar entre contextos. Sin embargo, la acción sigue sin controlar la transición al contexto siguiente: afecta al **proceso de recompensa**, no al **proceso de transición de estado**.

![[Pasted image 20260930164505.png]]

> En el diagrama izquierdo, la flecha de la acción entra directamente en el proceso de recompensa y el cambio de estado queda separado. En el derecho, que representa el **RL general**, la acción entra en el entorno y puede afectar tanto a la recompensa como al siguiente estado. Esta diferencia introduce consecuencias futuras: el agente puede cambiar las situaciones con las que tendrá que interactuar.

### VII. Bandits de gradiente

#### 19. Preferencias y política probabilística

> Los **bandits de gradiente** no estiman necesariamente $q_*(a)$ para seleccionar directamente la mejor acción. Mantienen una **preferencia** $H_t(a)$ para cada brazo y la convierten en una política mediante *softmax*:

$$
\Pr\{A_t=a\}
=
\frac{e^{H_t(a)}}{\sum_{b=1}^{k}e^{H_t(b)}}
\doteq \pi_t(a).
$$

> Un valor mayor de $H_t(a)$ aumenta la probabilidad de elegir $a$, pero todas las acciones conservan una probabilidad positiva. Las preferencias son relativas: sumar la misma constante a todas no cambia $\pi_t$.

#### 20. Ascenso de gradiente y línea base

> Tras observar $R_t$, la política se ajusta con un paso $\alpha$ y una **línea base** $\bar R_t$, que representa la recompensa media previa. Para entender los signos de la actualización, la derivada del logaritmo de la política respecto de una preferencia es

$$
\frac{\partial \log \pi_t(A_t)}{\partial H_t(a)}
=
\mathbf{1}_{\{a=A_t\}}-\pi_t(a).
$$

> Multiplicar esta dirección por la ventaja observada $R_t-\bar R_t$ da las dos reglas del material:

$$
\begin{aligned}
H_{t+1}(A_t)
&=H_t(A_t)+\alpha(R_t-\bar R_t)\bigl(1-\pi_t(A_t)\bigr),\\
H_{t+1}(a)
&=H_t(a)-\alpha(R_t-\bar R_t)\pi_t(a),
\qquad a\ne A_t.
\end{aligned}
$$

> Si la recompensa supera la línea base, sube la preferencia por la acción elegida y bajan las otras; si queda por debajo, ocurre lo contrario. Restar $\bar R_t$ centra la señal de aprendizaje y hace que la actualización dependa del rendimiento **relativo**, no del nivel absoluto de las recompensas.

![[Pasted image 20260930164506.png]]

> En la comparación mostrada, las políticas **con línea base** alcanzan un mayor porcentaje de elecciones óptimas que las correspondientes políticas **sin línea base**, tanto para $\alpha=0{,}1$ como para $\alpha=0{,}4$. El gráfico también muestra que cambiar $\alpha$ modifica la rapidez y el comportamiento del aprendizaje; no existe una elección universal del tamaño de paso deducible de estas curvas.

### VIII. Resumen Final

#### 21. Relaciones esenciales

> El RL parte de un ciclo entre agente y entorno: las acciones producen recompensas y, en el problema general, alteran los estados futuros. El *bandit* elimina esta segunda consecuencia para estudiar la estimación de valores y la selección de acciones. Un *bandit* contextual incorpora información del estado, pero mantiene la transición independiente de la acción.

> El valor verdadero $q_*(a)$ define qué brazo es mejor, mientras que $Q_t(a)$ es lo que el agente puede aprender de sus muestras. El promedio muestral reduce el ruido en entornos estacionarios; el paso constante da más peso a la información reciente. La elección de acciones exige equilibrar explotación y exploración: $\varepsilon$-greedy usa pruebas aleatorias, los valores optimistas favorecen pruebas tempranas y UCB incorpora una bonificación por incertidumbre.

> Los bandits de gradiente representan directamente una política probabilística mediante preferencias y la actualizan a partir de recompensas relativas a una línea base. Las curvas del banco de pruebas ilustran cómo cambian la recompensa media y la frecuencia de selección óptima según el método y sus parámetros.