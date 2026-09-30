---
estado: pendiente de revisión
---

### I. Programación dinámica y predicción

#### 1. Problemas que aborda

> La **programación dinámica** aplica las ecuaciones de Bellman a un proceso de decisión de Markov cuyo modelo se conoce. El modelo proporciona $p(s',r\mid s,a)$, la probabilidad de llegar a $s'$ y recibir $r$ al ejecutar $a$ en $s$. Con ella se calculan expectativas sobre todas las transiciones posibles, en lugar de depender de una transición observada.

- **Predicción:** calcular $v_\pi$ y, si interesa, $q_\pi$ para una política $\pi$ fija.
- **Control:** buscar una política $\pi_*$ que maximice el valor.
- **Planificación:** realizar esa búsqueda usando explícitamente el modelo del entorno.

> La pieza común es una actualización de Bellman: estimamos el valor de un estado a partir de la recompensa inmediata y de los valores estimados de los estados siguientes.

#### 2. Ecuaciones de Bellman para una política

> Si $\pi(a\mid s)$ es la probabilidad de elegir $a$ en $s$ y $\gamma$ es el factor de descuento, el valor de estado de $\pi$ satisface:

$$
v_\pi(s)=\sum_a\pi(a\mid s)\sum_{s',r}p(s',r\mid s,a)\bigl[r+\gamma v_\pi(s')\bigr].
$$

> El valor de ejecutar primero una acción concreta y seguir después $\pi$ es:

$$
q_\pi(s,a)=\sum_{s',r}p(s',r\mid s,a)\bigl[r+\gamma v_\pi(s')\bigr].
$$

> Estas expresiones conectan predicción y control: la primera evalúa la política actual; la segunda permite comparar sus acciones con alternativas. En los procedimientos siguientes, $\mathcal S$ contiene los estados no terminales, $\mathcal S^+$ incluye también el terminal y se fija $V(\text{terminal})=0$.

#### 3. Evaluación iterativa de una política

> Resolver de una vez todo el sistema de ecuaciones de Bellman puede resultar costoso. La **evaluación iterativa** parte de valores $V(s)$ arbitrarios y aplica repetidamente el respaldo de Bellman de la política hasta que un barrido apenas cambie la estimación.

> Para cada $s\in\mathcal S$, se guarda el valor anterior $v\leftarrow V(s)$ y se actualiza:

$$
V(s)\leftarrow\sum_a\pi(a\mid s)\sum_{s',r}p(s',r\mid s,a)\bigl[r+\gamma V(s')\bigr].
$$

> Al comenzar cada barrido se pone $\Delta\leftarrow0$. Tras cada estado se calcula $\Delta\leftarrow\max\{\Delta,|v-V(s)|\}$, y se detiene el proceso cuando $\Delta<\theta$, con $\theta>0$ pequeño. El pseudocódigo actualiza $V$ **sobre la marcha**: un estado posterior del mismo barrido puede utilizar un valor ya renovado. Al detenerse se obtiene $V\approx v_\pi$; $\theta$ controla el criterio práctico de parada, no convierte la aproximación en una igualdad exacta.

> Cuando $\pi$ es determinista, la suma sobre acciones desaparece y se usa directamente $a=\pi(s)$. Una vez calculado $v_\pi$, la segunda ecuación de Bellman permite obtener $q_\pi(s,a)$ y comparar acciones.

### II. Mejora de políticas y control

#### 4. Teorema de mejora de la política

> Supongamos una política determinista $\pi$ y otra $\pi'$ que solo elige una acción distinta en un estado $s$. Si tomar allí la acción nueva y continuar después con $\pi$ vale al menos tanto como seguir $\pi$ desde el principio,

$$
q_\pi\bigl(s,\pi'(s)\bigr)\geq v_\pi(s),
$$

> entonces seguir $\pi'$ no empeora el valor de ningún estado:

$$
v_{\pi'}(x)\geq v_\pi(x)\qquad\text{para todo }x\in\mathcal S.
$$

> La comparación $q_\pi(s,\pi'(s))$ evalúa **un primer cambio de acción** usando el valor de la política antigua para el futuro. El teorema extiende esa mejora a seguir la nueva política. Su versión general aplica la condición $q_\pi(x,\pi'(x))\geq v_\pi(x)$ a todos los estados $x$; si existe una mejora estricta, las políticas no tienen el mismo valor en todos los estados.

> [!warning] Corrección
> En el material se afirma que $\pi$ es igual o mejor que $\pi'$ después de escribir $q_\pi(s,\pi'(s))\geq v_\pi(s)$. El sentido correcto es $v_{\pi'}(x)\geq v_\pi(x)$: la política mejorada es $\pi'$.
> Fuente de comprobación: [Sutton y Barto, Reinforcement Learning: An Introduction](https://www.incompleteideas.net/book/bookdraft2018mar21.pdf).

#### 5. Operador de mejora greedy

> Una forma directa de satisfacer la condición del teorema consiste en elegir, en cada estado, una acción que maximice el valor de acción calculado con la política actual:

$$
\pi'(s)\doteq\operatorname*{arg\,max}_{a}q_\pi(s,a)
=\operatorname*{arg\,max}_{a}\sum_{s',r}p(s',r\mid s,a)\bigl[r+\gamma v_\pi(s')\bigr].
$$

> La política resultante es **greedy respecto a $v_\pi$** y puede hacerse determinista escogiendo una sola acción entre las empatadas. La elección entre empates debe ser consistente al ejecutar el algoritmo para que una mera alternancia entre acciones de igual valor no parezca una mejora nueva.

#### 6. Iteración de políticas

> La **iteración de políticas** alterna dos operaciones: evaluar la política vigente y mejorarla de forma greedy. El esquema conceptual es $\pi_0\xrightarrow{\mathrm E}v_{\pi_0}\xrightarrow{\mathrm I}\pi_1\xrightarrow{\mathrm E}v_{\pi_1}\xrightarrow{\mathrm I}\cdots\xrightarrow{\mathrm I}\pi_*$.

1. Inicializar $V(s)$ y una acción $\pi(s)\in\mathcal A(s)$ para cada $s\in\mathcal S$.
2. **Evaluar:** repetir barridos de Bellman de la política determinista hasta que $\Delta<\theta$:
   $$
   V(s)\leftarrow\sum_{s',r}p\bigl(s',r\mid s,\pi(s)\bigr)\bigl[r+\gamma V(s')\bigr].
   $$
3. **Mejorar:** guardar la acción anterior en cada estado y sustituirla por
   $$
   \pi(s)\leftarrow\operatorname*{arg\,max}_{a}\sum_{s',r}p(s',r\mid s,a)\bigl[r+\gamma V(s')\bigr].
   $$
4. Si ninguna acción cambia, detenerse; en caso contrario, volver a evaluar la política nueva.

> Si la evaluación es exacta y la mejora greedy ya no cambia la política, se ha alcanzado una política óptima: su valor satisface también la ecuación de optimalidad de Bellman. El pseudocódigo usa $\theta>0$ y, por tanto, devuelve en la práctica aproximaciones $V\approx v_*$ y $\pi\approx\pi_*$; una evaluación imprecisa puede afectar a la decisión de mejora.

#### 7. Ejemplo: cuadrícula de $4\times4$

> La cuadrícula tiene estados terminales en las dos esquinas grises, cuatro acciones cardinales y recompensa $-1$ en cada transición. Se evalúa repetidamente una **política aleatoria** y, junto a cada aproximación $v_k$, se muestra la política greedy respecto a ella. Las flechas múltiples representan empates entre acciones.

![[Pasted image 20260930174000.png]]

> En los barridos síncronos de la figura, $v_0=0$ y $v_1$ vale $-1$ en cada estado no terminal. Al seguir evaluando la política aleatoria, sus estimaciones cambian; sin embargo, la política greedy ya es óptima en $k=3$. El límite $v_\infty$ mostrado sigue siendo el **valor de la política aleatoria**, no $v_*$. Esto ilustra que una política mejorada puede estabilizarse antes de que termine la evaluación de la política anterior.

### III. Iteración de valor

#### 8. Idea y actualización de Bellman óptima

> La iteración de políticas espera a evaluar la política antes de realizar una nueva mejora. La **iteración de valor** adelanta la mejora: en cada actualización de estado elige directamente la acción de mayor retorno estimado. Así combina, en el mismo respaldo, estimación de valor y maximización.

$$
V(s)\leftarrow\max_a\sum_{s',r}p(s',r\mid s,a)\bigl[r+\gamma V(s')\bigr].
$$

> El punto fijo de esta actualización es $v_*$, pues satisface la ecuación de optimalidad de Bellman. Si se escriben barridos síncronos, la relación conceptual es $V_{k+1}=T_*V_k$, donde $T_*$ es el operador definido por el máximo anterior. El pseudocódigo de las diapositivas, como el de evaluación, actualiza los estados sobre la marcha.

#### 9. Algoritmo y extracción de la política

> Se inicializa $V(s)$ arbitrariamente en los estados no terminales y se mantiene $V(\text{terminal})=0$. En cada barrido se pone $\Delta=0$; para cada estado se guarda $v=V(s)$, se aplica el máximo de Bellman y se actualiza $\Delta=\max\{\Delta,|v-V(s)|\}$. Se repiten barridos hasta que $\Delta<\theta$.

> Después se obtiene una política determinista greedy respecto al valor estimado:

$$
\pi(s)=\operatorname*{arg\,max}_a\sum_{s',r}p(s',r\mid s,a)\bigl[r+\gamma V(s')\bigr].
$$

> En un MDP finito descontado, la repetición de la actualización converge asintóticamente a $v_*$; con un umbral de parada positivo se trabaja con una aproximación. La política extraída se aproxima a una política óptima. Las condiciones de convergencia deben comprobarse también cuando se trabaja sin descuento en episodios con terminación.

#### 10. Relación con la iteración de políticas

| Procedimiento | Respaldo de valor | Momento de la mejora |
|---|---|---|
| Evaluación de política | Promedio según $\pi(a\mid s)$ | No modifica $\pi$. |
| Iteración de políticas | Evalúa la política actual hasta el criterio de parada. | Aplica después una mejora greedy a todos los estados. |
| Iteración de valor | Maximiza sobre acciones en cada actualización. | La mejora está incorporada en cada respaldo; la política se extrae al final. |

> La iteración de valor evita completar una evaluación de política en cada ciclo, pero puede necesitar más barridos para converger. La iteración de políticas puede estabilizar la política en pocas mejoras a costa de evaluaciones más largas. No hay una ventaja universal en velocidad: depende del problema y del trabajo que exige cada barrido.

### IV. Iteración de política generalizada

#### 11. Evaluación y mejora intercaladas

> La **iteración de política generalizada** agrupa los métodos que hacen interactuar evaluación y mejora con distintos ritmos o reglas. La evaluación acerca $V$ al valor de la política actual; la mejora acerca la política a una greedy respecto al valor disponible. Después de mejorar $\pi$, el valor previamente calculado deja de corresponder exactamente a la nueva política y debe volver a ajustarse.

![[Pasted image 20260930174001.png]]

> En el diagrama, la línea superior representa los pares que cumplen $v=v_\pi$ y la inferior los que cumplen $\pi=\operatorname{greedy}(v)$. Las flechas alternan ambas tendencias y se acercan al par $(v_*,\pi_*)$. La iteración de políticas y la iteración de valor son dos maneras de organizar esta interacción. Otras reglas, incluidas algunas heurísticas, buscan modificar el comportamiento de convergencia; la misma idea está detrás de muchos algoritmos de aprendizaje por refuerzo.

#### 12. Resumen Final

> La predicción fija una política y resuelve aproximadamente su ecuación de Bellman mediante evaluación iterativa. El teorema de mejora permite construir una política greedy cuyo valor no es inferior al de la anterior. La iteración de políticas repite evaluación y mejora hasta la estabilidad; la iteración de valor incorpora el máximo en cada respaldo y extrae la política al final. La iteración de política generalizada reúne estas formas de alternar estimación y mejora.
