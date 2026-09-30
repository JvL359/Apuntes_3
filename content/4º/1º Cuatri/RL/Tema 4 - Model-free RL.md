---
estado: pendiente de revisión
---

### I. Aprendizaje por refuerzo sin modelo

#### 1. Del modelo a la experiencia

> La programación dinámica calcula respaldos de Bellman con la distribución de transición $p(s',r\mid s,a)$. En **aprendizaje por refuerzo sin modelo** no conocemos esa distribución: recibimos una secuencia de experiencia $(S_t,A_t,R_{t+1},S_{t+1})$ y estimamos los valores a partir de ella. La propiedad de Markov sigue siendo el supuesto habitual para interpretar el estado y justificar los respaldos temporales.

> El retorno episódico y los dos valores que queremos estimar son:

$$
G_t=\sum_{k=0}^{T-t-1}\gamma^kR_{t+k+1},\qquad
v_\pi(s)=\mathbb E_\pi[G_t\mid S_t=s],\qquad
q_\pi(s,a)=\mathbb E_\pi[G_t\mid S_t=s,A_t=a].
$$

> Para **predicción** fijamos $\pi$ y estimamos $v_\pi$ o $q_\pi$. Para **control** estimamos valores de acción y mejoramos la política usando $Q(s,a)$; disponer solo de valores de estado exigiría conocer el modelo para comparar acciones mediante sus transiciones. La mejora necesita **exploración**: si una acción nunca se prueba, su valor no puede estimarse a partir de la experiencia.

> Los métodos de este tema conservan una forma común de actualización, con paso de aprendizaje $0<\alpha\leq1$:

$$
\text{estimación nueva}
\leftarrow\text{estimación anterior}
+\alpha\bigl[\text{objetivo}-\text{estimación anterior}\bigr].
$$

### II. Predicción con Monte Carlo y diferencias temporales

#### 2. Monte Carlo de primera visita

> **Monte Carlo (MC)** estima valores promediando retornos completos observados al seguir $\pi$. No calcula una expectativa con $p(s',r\mid s,a)$ ni usa una estimación del estado siguiente en su objetivo: espera a conocer el resultado del episodio. Para evaluar estados, el objetivo de una visita a $S_t$ es $G_t$.

> En el algoritmo de **primera visita** se inicializan $V(s)$ y una lista vacía de retornos para cada estado. Por cada episodio generado con $\pi$:

1. Recorrerlo hacia atrás desde $t=T-1$ con $G\leftarrow\gamma G+R_{t+1}$, partiendo de $G=0$.
2. Si $S_t$ no apareció antes en ese mismo episodio, añadir $G$ a la lista de retornos de $S_t$.
3. Sustituir $V(S_t)$ por el promedio de su lista y repetir con nuevos episodios.

> La condición del segundo paso selecciona la **primera visita cronológica**, aunque el episodio se recorra hacia atrás. Para estimar $q_\pi(s,a)$ se promedian del mismo modo los retornos de las primeras visitas a cada par estado–acción. En la cuadrícula ilustrativa, una trayectoria $1\to2\to5\to6\to T$ con recompensa $-1$ en cada transición aporta un retorno para cada estado visitado.

#### 3. Cobertura de acciones y políticas ε-soft

> MC con retorno completo se aplica directamente a tareas episódicas. Sus objetivos no se apoyan en un valor estimado y, para una política fija y visitas suficientes, el promedio estima la expectativa del retorno; a cambio, la variabilidad de episodios completos puede producir **alta varianza** y aprendizaje lento. Una política determinista puede dejar acciones sin visitar, de modo que el promedio de sus retornos ni siquiera exista.

> Una política **ε-soft** asigna a toda acción posible una probabilidad al menos $\varepsilon/|\mathcal A(s)|$, con $\varepsilon>0$. Una política **ε-greedy** es un caso: elige una acción $A^*$ de máximo $Q(s,a)$, rompe empates arbitrariamente y reparte la exploración así:

$$
\pi(a\mid s)=
\begin{cases}
1-\varepsilon+\dfrac{\varepsilon}{|\mathcal A(s)|},&a=A^*,\\[4pt]
\dfrac{\varepsilon}{|\mathcal A(s)|},&a\ne A^*.
\end{cases}
$$

> Esta probabilidad evita que las acciones no greedy queden excluidas de las visitas. Para estimar todos los pares hacen falta además suficientes episodios y condiciones que permitan alcanzarlos. Con $\varepsilon$ fijo, la mejora se considera dentro de la familia ε-soft.

> [!warning] Corrección
> El material define ε-soft solo como probabilidad no nula de cada acción y habla de convergencia a una política óptima sin matiz. Con un $\varepsilon$ fijo, ε-soft exige $\pi(a\mid s)\geq\varepsilon/|\mathcal A(s)|$ y la optimalidad garantizada por la mejora es **entre las políticas ε-soft**, no necesariamente entre todas las políticas.
> Fuente de comprobación: [Sutton y Barto, Reinforcement Learning: An Introduction](https://www.incompleteideas.net/book/bookdraft2018mar21.pdf).

#### 4. TD(0): aprender antes de que termine el episodio

> La ecuación de Bellman escribe el retorno esperado como recompensa inmediata más valor del estado siguiente. **TD(0)** reemplaza ese valor desconocido por la estimación actual $V(S_{t+1})$: es *bootstrapping*. Las reglas de predicción MC y TD muestran la diferencia de objetivo:

$$
\begin{aligned}
\text{MC:}\quad
V(S_t)&\leftarrow V(S_t)+\alpha\bigl[G_t-V(S_t)\bigr],\\
\text{TD(0):}\quad
V(S_t)&\leftarrow V(S_t)+\alpha\bigl[R_{t+1}+\gamma V(S_{t+1})-V(S_t)\bigr].
\end{aligned}
$$

> La cantidad entre corchetes en TD es el **error de diferencia temporal**:

$$
\delta_t=R_{t+1}+\gamma V(S_{t+1})-V(S_t).
$$

> Compara lo que se esperaba del estado actual con el objetivo construido tras observar una recompensa y el estado siguiente. En un estado terminal se usa $V(\text{terminal})=0$. El algoritmo tabular inicializa $V$, sigue la política $\pi$, observa una transición, aplica esta actualización y continúa desde $S_{t+1}$ hasta terminar el episodio. Puede actualizar tras **cada paso**, sin conocer el resto del retorno.

#### 5. Ejemplo del trayecto a casa

> Durante un viaje se revisa la predicción del tiempo total: $30$, $40$, $35$, $40$ y $43$ minutos; la duración observada al llegar es de $43$ minutos. MC espera al tiempo final y desplaza todas las predicciones previas hacia $43$; TD desplaza cada predicción hacia la estimación disponible en la situación siguiente. Así, una predicción puede aprender antes de conocer el resultado final.

![[Pasted image 20260930181000.png]]

> Las flechas de la izquierda apuntan al resultado final; las de la derecha conectan predicciones consecutivas. El ejemplo ilustra la diferencia entre **retorno observado** y **objetivo con bootstrapping**, sin que sea necesario disponer de un modelo de tránsito.

#### 6. MC, TD y programación dinámica

| Método | Información usada en un respaldo | Momento en que puede actualizar | Modelo |
|---|---|---|---|
| MC | Una trayectoria muestreada hasta el final del episodio: $G_t$. | Tras observar el retorno completo. | No |
| TD(0) | Una transición muestreada y $V(S_{t+1})$. | Después de cada transición. | No |
| Programación dinámica | Expectativa sobre todas las transiciones posibles y valores sucesores. | En cada barrido de Bellman. | Sí |

> Vistos como respaldos, **TD(0)** tiene poca profundidad y una sola rama observada; **MC** sigue una rama hasta el final; la **programación dinámica** se extiende a todas las ramas posibles a un paso. MC no necesita un respaldo de un paso basado en la propiedad de Markov, pero requiere episodios completos y presenta más varianza. TD usa el supuesto de Markov y reduce la varianza al hacer bootstrapping, que puede introducir sesgo durante el aprendizaje; sus garantías dependen del caso tabular o de aproximación usado. TD también sirve para tareas continuas en las que no se espera un final de episodio. La búsqueda exhaustiva, que ocupa el otro extremo del esquema de respaldos, explora todas las ramas hasta el final y suele tener un coste prohibitivo.

### III. Control sin modelo

#### 7. Control Monte Carlo on-policy

> La **iteración de política generalizada** permite alternar estimación de $Q$ y mejora de $\pi$ sin completar una evaluación exacta. En control MC es natural mejorar tras un solo episodio. El algoritmo de primera visita *on-policy* comienza con una política ε-soft, valores $Q(s,a)$ y listas de retornos vacías para cada par.

1. Generar un episodio siguiendo la propia $\pi$.
2. Recorrerlo hacia atrás, calcular cada $G_t$ y, en la primera visita cronológica a $(S_t,A_t)$, añadir ese retorno y actualizar $Q(S_t,A_t)$ con el promedio.
3. Hallar $A^*=\arg\max_aQ(S_t,a)$ y hacer la política ε-greedy en los estados visitados mediante la distribución anterior.
4. Repetir la generación, evaluación y mejora con la política actualizada.

> Mantener probabilidad positiva para las demás acciones permite seguir estimando sus valores. Con $\varepsilon$ fijo, el objetivo de optimalidad queda restringido a la clase ε-soft; reducir la exploración exige una pauta compatible con visitas suficientes.

#### 8. On-policy, off-policy y muestreo de importancia

> En **on-policy**, la política cuyos valores se aprenden y la que genera datos son la misma, $\pi$. En **off-policy**, se evalúa o mejora una política objetivo $\pi$ usando episodios producidos por otra política de comportamiento $\mu$. El promedio directo de esos episodios estima valores bajo $\mu$, no bajo $\pi$.

> El **muestreo de importancia** corrige la diferencia de probabilidades de las acciones futuras sin necesitar el modelo del entorno. Para un valor de acción, porque $A_t=a$ ya está condicionado, la razón del resto del episodio es:

$$
\rho_{t+1:T-1}
=\prod_{k=t+1}^{T-1}
\frac{\pi(A_k\mid S_k)}{\mu(A_k\mid S_k)},
\qquad
q_\pi(s,a)
=\mathbb E_\mu\!\left[\rho_{t+1:T-1}G_t
\mid S_t=s,A_t=a\right].
$$

> Es imprescindible que $\mu$ permita las acciones que $\pi$ puede elegir; de otro modo, faltan trayectorias que reponderar. Las razones pueden variar mucho y elevar la varianza. Este mecanismo pertenece al control MC off-policy; Q-learning utiliza otro objetivo de un paso y no requiere estas razones en su actualización básica.

#### 9. Sarsa: control TD on-policy

> **Sarsa** actualiza $Q(S_t,A_t)$ con la recompensa y el valor de la **siguiente acción realmente elegida** $A_{t+1}$ por la política de comportamiento, normalmente ε-greedy. Su nombre recoge la secuencia $(S_t,A_t,R_{t+1},S_{t+1},A_{t+1})$:

$$
Q(S_t,A_t)\leftarrow Q(S_t,A_t)
+\alpha\bigl[R_{t+1}+\gamma Q(S_{t+1},A_{t+1})-Q(S_t,A_t)\bigr].
$$

> Se inicializa $Q(s,a)$, con $Q(\text{terminal},\cdot)=0$. En cada episodio se elige una acción inicial con la política derivada de $Q$; tras ejecutarla, se observa $R_{t+1},S_{t+1}$, se elige $A_{t+1}$ con esa misma política, se actualiza $Q$ y se continúa desde el nuevo par hasta llegar al terminal. Cuando la transición acaba el episodio, el término de valor siguiente es cero. La política que se evalúa y mejora es también la que explora: por eso Sarsa es on-policy.

> En *Windy Gridworld*, las trayectorias están afectadas por viento. El gráfico de episodios completados frente a pasos de interacción muestra cómo Sarsa va aprendiendo a alcanzar la meta con más frecuencia a medida que acumula experiencia.

#### 10. Q-learning: control TD off-policy

> **Q-learning** puede generar experiencia con una política ε-greedy respecto a $Q$, pero actualiza hacia una política objetivo greedy. En el objetivo no aparece la acción exploratoria que se elegirá en $S_{t+1}$: aparece el mayor valor estimado en ese estado.

$$
Q(S_t,A_t)\leftarrow Q(S_t,A_t)
+\alpha\bigl[R_{t+1}+\gamma\max_aQ(S_{t+1},a)-Q(S_t,A_t)\bigr].
$$

> El procedimiento inicializa $Q(s,a)$ y $Q(\text{terminal},\cdot)=0$; por cada transición elige $A_t$ con la política de comportamiento, observa recompensa y estado siguiente, aplica la ecuación y continúa hasta el terminal. El contraste con Sarsa está en el **objetivo TD**: Sarsa usa $Q(S_{t+1},A_{t+1})$ de la acción que se seguirá; Q-learning usa $\max_aQ(S_{t+1},a)$ aunque la política de comportamiento pueda explorar.

#### 11. Comparación en Cliff Walking

> En *Cliff Walking*, cada paso ordinario da $-1$ y caer al precipicio da $-100$. Con exploración ε-greedy persistente, Sarsa aprende una ruta alejada del precipicio porque sus objetivos incluyen el riesgo de las acciones exploratorias posteriores. Q-learning aprende el valor de la ruta greedy más corta junto al precipicio, pero durante el entrenamiento la exploración todavía puede causar caídas.

![[Pasted image 20260930181001.png]]

> La curva de retorno por episodio favorece a Sarsa en este experimento de entrenamiento: el recorrido más corto de la política objetivo no coincide con el mejor retorno mientras se ejecuta una política que sigue explorando.

#### 12. Sesgo de maximización y Double Q-learning

> El máximo de varias estimaciones ruidosas tiende a seleccionar una estimación demasiado alta. En Q-learning, **selección** y **evaluación** de la acción siguiente usan el mismo $Q$; esto produce sesgo de maximización cuando los valores todavía son inciertos. **Double Q-learning** mantiene dos tablas, $Q_1$ y $Q_2$, para separar ambas funciones.

> La acción de comportamiento se elige ε-greedy respecto a $Q_1+Q_2$. Después de cada transición se actualiza aleatoriamente una sola tabla. Si se actualiza $Q_1$, la propia $Q_1$ escoge la acción siguiente y $Q_2$ la valora:

$$
Q_1(S_t,A_t)\leftarrow Q_1(S_t,A_t)
+\alpha\Bigl[
R_{t+1}
+\gamma Q_2\bigl(S_{t+1},\operatorname*{arg\,max}_aQ_1(S_{t+1},a)\bigr)
-Q_1(S_t,A_t)
\Bigr].
$$

> En la otra mitad de las actualizaciones se intercambian los papeles:

$$
Q_2(S_t,A_t)\leftarrow Q_2(S_t,A_t)
+\alpha\Bigl[
R_{t+1}
+\gamma Q_1\bigl(S_{t+1},\operatorname*{arg\,max}_aQ_2(S_{t+1},a)\bigr)
-Q_2(S_t,A_t)
\Bigr].
$$

> En el ejemplo, desde $A$ ir a la derecha termina con retorno $0$; ir a $B$ conduce a varias acciones con recompensas aleatorias de distribución $\mathcal N(-0{,}1,1)$, todas de media negativa. La curva, promediada sobre muchas ejecuciones con $\varepsilon=0{,}1$, muestra que Q-learning elige la izquierda demasiado a menudo por el máximo sobre estimaciones ruidosas, mientras Double Q-learning se aproxima antes al $5\%$ mínimo de elección izquierda impuesto por la exploración ε-greedy.

![[Pasted image 20260930181002.png]]

### IV. Retornos a varios pasos

#### 13. Del TD de un paso al retorno a n pasos

> MC utiliza todo el retorno y TD(0) hace bootstrapping después de una transición. Entre ambos se puede esperar $n$ transiciones y usar entonces un valor estimado. Con la notación de las diapositivas, el **retorno a $n$ pasos** para predicción es:

$$
G_{t:t+n}\doteq
R_{t+1}+\gamma R_{t+2}+\cdots+\gamma^{n-1}R_{t+n}
+\gamma^n V_{t+n-1}(S_{t+n}),
$$

> y la actualización se realiza cuando se dispone de ese objetivo:

$$
V_{t+n}(S_t)\doteq
V_{t+n-1}(S_t)
+\alpha\bigl[G_{t:t+n}-V_{t+n-1}(S_t)\bigr].
$$

> Con $n=1$ recuperamos TD(0). Si el episodio termina antes de completar $n$ pasos, se suman únicamente las recompensas disponibles y no se añade un valor terminal; si se espera hasta el final, el objetivo es MC. Por ejemplo, con $n=10$ no se puede actualizar el estado inicial hasta observar diez transiciones o la terminación del episodio.

#### 14. Elegir n: sesgo, varianza y propagación

> $n$ es un **hiperparámetro**. Un $n$ pequeño introduce antes el valor estimado: suele tener más sesgo inicial y menos varianza, pero una recompensa nueva afecta directamente a menos estados anteriores. Un $n$ mayor hace llegar esa recompensa más atrás en una misma experiencia y reduce el uso de bootstrapping, a costa de más espera y varianza.

> El esquema de *random walk* parte de $C$ entre dos terminales: salir por la derecha da recompensa $1$ y por la izquierda, $0$. El gráfico utiliza una variante de 19 estados y representa el error cuadrático medio de los primeros diez episodios frente a $\alpha$ para distintos $n$. El mejor resultado de ese experimento aparece con un valor intermedio de $n$ y una tasa de aprendizaje compatible; no existe un $n$ universalmente óptimo.

![[Pasted image 20260930181003.png]]

#### 15. Sarsa a n pasos

> Para control *on-policy* se aplica la misma idea a valores de acción. Si $T$ es el instante terminal y $\tau$ el instante cuyo par se actualizará, el objetivo del algoritmo es:

$$
G=
\sum_{i=\tau+1}^{\min(\tau+n,T)}
\gamma^{i-\tau-1}R_i
+
\begin{cases}
\gamma^nQ(S_{\tau+n},A_{\tau+n}),&\tau+n<T,\\
0,&\tau+n\geq T,
\end{cases}
$$

$$
Q(S_\tau,A_\tau)\leftarrow
Q(S_\tau,A_\tau)+\alpha\bigl[G-Q(S_\tau,A_\tau)\bigr].
$$

> Al comenzar cada episodio se guardan $S_0$ y $A_0\sim\pi(\cdot\mid S_0)$ y se pone $T=\infty$. En cada instante $t$ se ejecuta $A_t$, se almacena $R_{t+1}$ y $S_{t+1}$ y, si el estado no es terminal, se elige $A_{t+1}$ con $\pi$. Después se calcula $\tau=t-n+1$; cuando $\tau\geq0$ se construye $G$, se actualiza el par $(S_\tau,A_\tau)$ y se mantiene $\pi$ ε-greedy respecto a $Q$. Tras llegar al terminal todavía se procesan los pares pendientes hasta $\tau=T-1$.

> La cuadrícula visualiza una consecuencia: una recompensa positiva al llegar a $G$ refuerza solo la última acción con Sarsa de un paso, mientras que Sarsa a diez pasos refuerza hasta las diez acciones anteriores de esa misma trayectoria.

![[Pasted image 20260930181004.png]]

### V. TD(λ) y trazas de elegibilidad

#### 16. Combinar retornos de distintos horizontes

> También podemos combinar horizontes en lugar de fijar un único $n$: por ejemplo, $\tfrac12G_{t:t+2}+\tfrac12G_{t:t+4}$. **TD(λ)** mezcla todos los retornos a $n$ pasos con pesos geométricos, para $0\leq\lambda\leq1$:

$$
G_t^\lambda\doteq
(1-\lambda)\sum_{n=1}^{\infty}\lambda^{n-1}G_{t:t+n}.
$$

> El retorno $\lambda$ sirve como objetivo en $V(S_t)\leftarrow V(S_t)+\alpha[G_t^\lambda-V(S_t)]$. En un episodio que termina en $T$, el terminal es absorbente y los horizontes que llegan a él comparten el mismo retorno completo $G_t$; por eso la mezcla se escribe sin una suma infinita efectiva:

$$
G_t^\lambda=
(1-\lambda)\sum_{n=1}^{T-t-1}\lambda^{n-1}G_{t:t+n}
+\lambda^{T-t-1}G_t.
$$

> El peso del retorno de tres pasos es $(1-\lambda)\lambda^2$; el del retorno final agrupa la masa restante. Los pesos suman uno. Con $\lambda=0$ queda TD de un paso; con $\lambda=1$, el retorno completo de MC.

![[Pasted image 20260930181005.png]]

#### 17. Interpretación hacia adelante y hacia atrás

> La **interpretación hacia adelante** calcula para cada estado visitado el retorno $G_t^\lambda$ mirando las recompensas futuras. En la versión episódica descrita aquí se espera al final, se actualiza hacia ese retorno y no se vuelve a modificar esa visita: es una realización *offline*. Sirve para entender la mezcla de horizontes, pero retrasa las actualizaciones.

> La **interpretación hacia atrás** reordena las contribuciones del retorno $\lambda$: utiliza el error TD de cada transición cuando ocurre y reparte su efecto a estados visitados previamente. Las **trazas de elegibilidad** registran cuánto corresponde todavía a cada estado: aumentan al visitarlo y decaen con el tiempo. Combinan, por tanto, frecuencia y recencia, como en el ejemplo de varios timbres anteriores a una luz y una descarga.

#### 18. Trazas tabulares y actualización TD(λ)

> Se inicializa cada traza en cero al comenzar el episodio. La traza acumulativa del estado $s$ y la actualización de valor son:

$$
z_t(s)=\gamma\lambda z_{t-1}(s)+\mathbf 1(S_t=s),
\qquad
\delta_t=R_{t+1}+\gamma V(S_{t+1})-V(S_t),
$$

$$
V(s)\leftarrow V(s)+\alpha\,\delta_t\,z_t(s)
\qquad\text{para cada }s.
$$

> La visita actual añade $1$; una visita anterior conserva una fracción $\gamma\lambda$ de su peso en el paso siguiente. Si un estado se visitó varias veces, las contribuciones se acumulan. Un único error $\delta_t$ actualiza inmediatamente todos los estados con traza no nula, en proporción a su elegibilidad. Así se propaga información hacia atrás sin esperar a reconstruir un retorno completo para cada visita.

#### 19. De la tabla a la aproximación de función

> En una tabla puede verse $V(s)$ como una función lineal de pesos con codificación **one-hot**: el gradiente respecto a los pesos vale $1$ en la coordenada del estado actual y $0$ en las demás. Ese indicador es el término que se añade a la traza tabular.

> Para una función diferenciable $\hat v(s,\boldsymbol w)$, la traza pasa a ser un vector y las diapositivas dan la actualización general:

$$
\boldsymbol z_t\doteq
\gamma\lambda\boldsymbol z_{t-1}
+\nabla_{\boldsymbol w}\hat v(S_t,\boldsymbol w_t),
\qquad
\boldsymbol w_{t+1}=
\boldsymbol w_t+\alpha\,\delta_t\,\boldsymbol z_t.
$$

> El parámetro $\lambda$ regula el peso de información futura y la duración de las trazas, con un compromiso entre sesgo y varianza que puede acelerar el aprendizaje inicial. La actualización de pesos depende de $\delta_t$; al extender la idea a control, su objetivo de un paso debe definirse de acuerdo con el algoritmo utilizado, como Sarsa o Q-learning.

#### 20. Resumen Final

> Sin modelo, los valores se aprenden de episodios y transiciones. MC usa retornos completos y necesita cobertura de estados y acciones; TD(0) actualiza tras una transición mediante bootstrapping. Para control, MC alterna estimación y mejora ε-greedy; Sarsa aprende con la siguiente acción de la política que explora y Q-learning usa el máximo de la política objetivo. Double Q-learning separa selección y evaluación para reducir el sesgo de maximización. Los retornos a $n$ pasos y TD(λ) conectan objetivos cortos y completos; las trazas de elegibilidad permiten propagar cada error TD a visitas anteriores.
