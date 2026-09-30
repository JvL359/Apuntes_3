---
estado: pendiente de revisión
---

### I. Decisiones secuenciales y modelo MDP

#### 1. De la recompensa inmediata al resultado futuro

> Una acción puede proporcionar una recompensa alta ahora y, sin embargo, impedir recompensas mayores después. En un problema de **decisión secuencial** interesa la secuencia de acciones y el **retorno** que produce, no solo el resultado de un paso aislado. Un **proceso de decisión de Markov** (*Markov decision process*, **MDP**) ofrece un modelo para razonar sobre estas decisiones bajo incertidumbre.

> La navegación hacia un destino ilustra la diferencia: un movimiento aparentemente ventajoso puede dejar al agente en una zona desfavorable. La elección óptima debe considerar tanto la recompensa que sigue a la acción como las situaciones a las que puede conducir.

#### 2. Interacción entre agente y entorno

> En cada paso, el **agente** observa un estado $S_k$ y elige una acción $A_k$. El **entorno** responde con una recompensa $R_{k+1}$ y un nuevo estado $S_{k+1}$. La trayectoria se ordena como

$$
S_0,A_0,R_1,S_1,A_1,R_2,S_2,\ldots
$$

> El estado resume la situación desde la que se decide; la acción representa la elección del agente; la recompensa evalúa la transición. Cuando se utilizan índices $t$ en las expresiones siguientes, estos designan los mismos pasos de interacción que los índices $k$.

#### 3. Componentes y propiedad de Markov

> En este tema se estudian **MDP finitos**: los conjuntos de estados, acciones y recompensas son finitos. Los estados pertenecen a un conjunto $\mathcal S$, las acciones disponibles pueden depender del estado y pertenecen a $\mathcal A(s)$, y las recompensas pertenecen a $\mathcal R\subset\mathbb R$:

$$
S_t\in\mathcal S,\qquad
A_t\in\mathcal A(s),\qquad
R_{t+1}\in\mathcal R\subset\mathbb R.
$$

> La **propiedad de Markov** significa que, conocidos el estado actual y la acción elegida, la distribución del siguiente estado y de la recompensa no necesita el historial completo. Esto exige que el estado contenga la información relevante para predecir la transición. La incertidumbre permanece en el resultado de la acción; lo que cambia es qué información basta para describirla.

### II. Dinámica del MDP

#### 4. Probabilidades de transición y recompensa

> La **dinámica** del MDP se especifica mediante la probabilidad conjunta de llegar a $s'$ y recibir $r$ al partir de $s$ y ejecutar $a$. Con la indexación empleada en la definición:

$$
p(s',r\mid s,a)
\doteq
\Pr\{S_t=s',R_t=r\mid S_{t-1}=s,A_{t-1}=a\}.
$$

> Fijados $s$ y $a$, los valores $p(s',r\mid s,a)$ forman una distribución: son no negativos y suman uno sobre todos los pares posibles $(s',r)$. La probabilidad de un estado siguiente se obtiene sumando sobre las recompensas:

$$
\sum_{s',r}p(s',r\mid s,a)=1,
\qquad
\Pr(S_t=s'\mid S_{t-1}=s,A_{t-1}=a)
=\sum_r p(s',r\mid s,a).
$$

> El modelo une transición y recompensa porque dos resultados con el mismo estado siguiente pueden llevar distintas recompensas. Si la recompensa posible para una transición está fijada, la distribución se simplifica y solo hay que repartir la probabilidad entre los estados siguientes.

#### 5. Cuadrícula de ocho estados

> Una cuadrícula de $3\times3$ contiene ocho estados no terminales, numerados del $1$ al $8$, y un estado terminal $T$. Desde cada estado no terminal hay cuatro acciones: arriba, abajo, izquierda y derecha. En este ejemplo, todas las transiciones consideradas proporcionan recompensa $-1$.

![[Pasted image 20260930171400.png]]

> La figura organiza los ocho estados **no terminales** y cuatro acciones por estado. Fijar un par $(s,a)$ selecciona una distribución de destinos, representada en la estructura con ejes de estado actual, acción y estado siguiente. Para describir una transición que acaba el episodio también hay que considerar el destino $T$.

![[Pasted image 20260930171401.png]]

> [!warning] Corrección
> En el material aparece que cada par $(s,a)$ tiene una distribución de ocho valores porque hay ocho estados, pero la cuadrícula también puede transitar al terminal $T$. La dinámica completa debe contemplar $s'\in\mathcal S^+=\mathcal S\cup\{T\}$ como posible destino; por tanto, hay hasta nueve destinos distintos, aunque algunos tengan probabilidad cero.
> Fuente de comprobación: [Sutton y Barto, Reinforcement Learning: An Introduction, capítulo 3](https://www.incompleteideas.net/book/bookdraft2018mar21.pdf).

> Las siguientes probabilidades quedan planteadas para analizar la cuadrícula:

- $p(5,-1\mid 2,\text{abajo})=?$
- $p(5,-1\mid 2,\text{izquierda})=?$
- $p(5,0\mid 2,\text{abajo})=?$
- $p(3,-1\mid 3,\text{derecha})=?$

### III. Retorno y política

#### 6. Episodios y retorno

> La **recompensa** $R_{t+1}$ evalúa un paso; el **retorno** $G_t$ combina las recompensas futuras desde el instante $t$. Si la interacción termina en el paso $T$, el retorno de un episodio es

$$
G_t\doteq R_{t+1}+R_{t+2}+R_{t+3}+\cdots+R_T.
$$

> Esta suma explica por qué conviene mirar más allá de la recompensa inmediata. El diseño de la señal de recompensa importa: un agente que optimiza el retorno perseguirá exactamente el objetivo que esa señal codifique, aunque no coincida con la intención original si se diseñó mal.

#### 7. Descuento y forma recursiva

> En una tarea sin final, la suma de recompensas puede no converger. El **retorno descontado** asigna a cada recompensa un peso $\gamma^k$ según lo lejos que esté en el futuro:

$$
\begin{aligned}
G_t
&\doteq R_{t+1}+\gamma R_{t+2}+\gamma^2R_{t+3}+\cdots\\
&=\sum_{k=0}^{\infty}\gamma^kR_{t+k+1}\\
&=R_{t+1}+\gamma G_{t+1}.
\end{aligned}
$$

> El parámetro $\gamma$ es el **factor de descuento**. Con recompensas acotadas, $0\leq\gamma<1$ hace converger la suma de una tarea continua. Cuando $\gamma=0$ solo cuenta la recompensa inmediata; al aumentar $\gamma$, pesan más las recompensas futuras. En episodios finitos, la suma puede estar bien definida incluso sin descuento.

> La última igualdad es decisiva: el retorno desde $t$ equivale a la primera recompensa más el retorno desde $t+1$ descontado. Esta descomposición hará posible expresar los valores de forma recursiva.

#### 8. Política de actuación

> Una **política** $\pi$ asigna a cada estado una distribución de probabilidad sobre las acciones disponibles:

$$
\pi(a\mid s)\doteq \Pr(A_t=a\mid S_t=s),
\qquad
\sum_{a\in\mathcal A(s)}\pi(a\mid s)=1.
$$

> La política puede ser **estocástica**: un mismo estado no obliga siempre a elegir la misma acción. En el ejemplo de la cuadrícula, una política uniforme en el estado $3$ asigna probabilidad $0{,}25$ a cada una de las cuatro direcciones. Una política determinista es el caso particular en que una acción tiene probabilidad uno.

### IV. Funciones de valor y ecuación de Bellman

#### 9. Valor de estado y valor de acción

> Las **funciones de valor** relacionan estados y acciones con el retorno que se espera obtener al seguir una política $\pi$. El **valor de estado** evalúa empezar en $s$ y actuar después según $\pi$:

$$
v_\pi(s)
\doteq
\mathbb E_\pi[G_t\mid S_t=s]
=
\mathbb E_\pi\left[
\sum_{k=0}^{\infty}\gamma^kR_{t+k+1}
\;\middle|\;S_t=s
\right].
$$

> El **valor de acción** evalúa empezar en $s$, tomar primero la acción $a$ y seguir después $\pi$:

$$
q_\pi(s,a)
\doteq
\mathbb E_\pi[G_t\mid S_t=s,A_t=a]
=
\mathbb E_\pi\left[
\sum_{k=0}^{\infty}\gamma^kR_{t+k+1}
\;\middle|\;S_t=s,A_t=a
\right].
$$

> En un episodio, la suma de recompensas se detiene al alcanzar $T$; en una tarea continua se emplea el retorno descontado.

> Por tanto, $v_\pi$ promedia el resultado de todas las acciones según sus probabilidades en la política, mientras que $q_\pi$ fija la primera acción. Ambos valores dependen de la **política seguida después**: un mismo estado puede tener distinto valor bajo políticas diferentes. La relación entre ellos es

$$
v_\pi(s)=\sum_a\pi(a\mid s)q_\pi(s,a).
$$

#### 10. Derivación de la ecuación de Bellman para $v_\pi$

> Sustituimos la descomposición del retorno $G_t=R_{t+1}+\gamma G_{t+1}$ en la definición del valor de estado. Después separamos dos fuentes de incertidumbre: qué acción elige la política y qué par $(s',r)$ produce la dinámica.

$$
\begin{aligned}
v_\pi(s)
&=\mathbb E_\pi[G_t\mid S_t=s]\\
&=\mathbb E_\pi[R_{t+1}+\gamma G_{t+1}\mid S_t=s]\\
&=\sum_a\pi(a\mid s)\sum_{s',r}p(s',r\mid s,a)
  \left[r+\gamma\mathbb E_\pi[G_{t+1}\mid S_{t+1}=s']\right]\\
&=\sum_a\pi(a\mid s)\sum_{s',r}p(s',r\mid s,a)
  \left[r+\gamma v_\pi(s')\right].
\end{aligned}
$$

> Esta es la **ecuación de Bellman de expectativa** para $v_\pi$. Cada posible acción aporta según $\pi(a\mid s)$; cada resultado de esa acción aporta según $p(s',r\mid s,a)$. Dentro del corchete aparecen la recompensa inmediata $r$ y el valor futuro del siguiente estado, descontado por $\gamma$.

> Si el siguiente estado es el terminal $T$, ya no hay continuación del episodio y se toma $v_\pi(T)=0$ para ese término.

> La misma descomposición, con la primera acción fijada, da una expresión útil para $q_\pi$:

$$
q_\pi(s,a)
=\sum_{s',r}p(s',r\mid s,a)
  \left[r+\gamma v_\pi(s')\right].
$$

> Juntas, ambas ecuaciones muestran cómo una política y la dinámica inducen valores que se sostienen recursivamente: el valor de un estado depende de los valores de los estados a los que puede llevar.

### V. Cuadrículas y diagramas de backup

#### 11. Navegación hacia un estado terminal

> En la cuadrícula de navegación se puede mover al **norte, sur, este u oeste**. El objetivo es alcanzar el estado terminal $T$, que representa un puerto, lo antes posible. Cada movimiento ordinario recibe recompensa $-1$; cuando se intenta salir por un borde se rebota en la celda de contorno. Entrar en la celda del **remolino** produce recompensa $-5$.

![[Pasted image 20260930171402.png]]

> El esquema señala dos zonas de viento y el remolino. Al moverse **en la dirección del viento**, existe una probabilidad $0{,}25$ de avanzar dos celdas. Al moverse **en sentido contrario**, existe una probabilidad $0{,}25$ de no desplazarse. Estas excepciones hacen que una misma acción pueda tener más de un estado siguiente y, por ello, deba representarse mediante probabilidades de transición.

#### 12. Lectura de un diagrama de backup

> Un **diagrama de backup** despliega desde un estado las acciones disponibles y los resultados de un paso. La rama de cada acción lleva a una recompensa y a un estado siguiente. El diagrama del estado $1$ muestra las cuatro direcciones y sus transiciones: norte y oeste rebotan en $1$, sur lleva a $5$ y este lleva a $2$; todas las ramas mostradas tienen recompensa $-1$.

![[Pasted image 20260930171403.png]]

> Al usar el diagrama en una ecuación de valor, se ponderan las ramas de resultado por sus probabilidades y se incorpora el valor futuro de cada estado siguiente. Si se evalúa una política, las acciones también se ponderan por $\pi(a\mid s)$.

> **Ejercicio propuesto:** representa el diagrama de *backup* para el estado $3$.

#### 13. El sistema de ecuaciones de Bellman

> Al escribir la ecuación de Bellman para todos los estados de una cuadrícula finita y una **política fijada**, se obtiene un **sistema de ecuaciones**: cada valor $v_\pi(s)$ aparece relacionado con valores de estados sucesores. La formulación exige conocer las probabilidades de transición, las recompensas, el factor de descuento y la política que se evalúa.

> Para la cuadrícula inicial de ocho estados se plantean estas cuestiones:

- ¿Cuántos valores de estado pueden definirse y qué tipo de funciones se manejan?
- ¿Cómo puede encontrarse una solución del sistema?
- ¿Qué ventajas e inconvenientes presentan las alternativas?

### VI. Condiciones de optimalidad

#### 14. Valor de estado óptimo

> Una política **óptima** $\pi_*$ alcanza los mejores valores posibles. Se usa una estrella para señalar las funciones de valor óptimas, $v_*$ y $q_*$. Para cada estado, $v_*(s)$ corresponde al mejor retorno esperado que puede lograrse desde él:

$$
v_*(s)
=\max_{a\in\mathcal A(s)}q_{\pi_*}(s,a).
$$

> En la ecuación de Bellman de **optimalidad**, el promedio sobre las acciones de una política concreta se sustituye por un **máximo** sobre las acciones disponibles. La incertidumbre del entorno sigue tratándose mediante esperanza:

$$
\begin{aligned}
v_*(s)
&=\max_a\mathbb E\!\left[
R_{t+1}+\gamma v_*(S_{t+1})
\mid S_t=s,A_t=a
\right]\\
&=\max_a\sum_{s',r}p(s',r\mid s,a)
  \left[r+\gamma v_*(s')\right].
\end{aligned}
$$

> El orden es importante: para cada acción se promedian sus posibles resultados; **después** se elige la acción cuyo promedio es mayor. No se elige retrospectivamente una acción distinta para cada resultado aleatorio de una misma transición.

#### 15. Valor de acción óptimo

> El **valor de acción óptimo** fija la primera acción $a$ y supone que, tras llegar al siguiente estado, se actuará de forma óptima:

$$
q_*(s,a)
=
\mathbb E\!\left[
R_{t+1}+\gamma v_*(S_{t+1})
\mid S_t=s,A_t=a
\right].
$$

> Al expandir la esperanza con la dinámica y relacionar los dos valores óptimos se obtiene

$$
q_*(s,a)
=\sum_{s',r}p(s',r\mid s,a)
  \left[r+\gamma v_*(s')\right],
\qquad
v_*(s)=\max_{a\in\mathcal A(s)}q_*(s,a).
$$

![[Pasted image 20260930171404.png]]

> En el diagrama de $v_*$, el estado $s$ abre las acciones posibles: se evalúan sus resultados y se toma el **máximo entre acciones**. En el de $q_*$, la primera acción ya está fijada; después de cada posible estado siguiente $s'$ aparece el máximo que corresponde a continuar óptimamente. Los nodos de resultado representan la incertidumbre de la dinámica, mientras que los máximos representan decisiones del agente.

### VII. Resumen Final

#### 16. Relaciones esenciales

> Un MDP finito combina estados, acciones, recompensas y una dinámica $p(s',r\mid s,a)$. El agente no optimiza una recompensa aislada, sino un **retorno** que reúne recompensas futuras; el descuento permite tratar tareas continuas y hace posible la descomposición recursiva $G_t=R_{t+1}+\gamma G_{t+1}$.

> Una política $\pi(a\mid s)$ determina cómo se actúa. Sus funciones $v_\pi(s)$ y $q_\pi(s,a)$ miden el retorno esperado desde un estado o desde un par estado–acción. La ecuación de Bellman enlaza cada valor con la recompensa de un paso y los valores de los estados sucesores.

> En la evaluación de una política se **promedian** sus acciones; en la optimalidad se **maximiza** sobre las acciones, manteniendo la esperanza sobre los resultados aleatorios del entorno. Las cuadrículas y los diagramas de *backup* muestran cómo se traduce esa diferencia a transiciones concretas.