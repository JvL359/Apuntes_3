### 1. Ecuaciones de Bellman

Política estocástica equiprobable.

La función de valor viene dada por:

$$
V_\pi(s)
=
\sum_a \pi(a|s)
\sum_{s'} p(s'|s,a)
\left[
r + \gamma V_\pi(s')
\right]
$$

Como el entorno es determinista:

$$
p(s'|s,a)=1
$$

y además:

$$
V(T)=0
$$

### Estado $s_6$

$$
V_\pi(s_6)
=
0.5\cdot 1\cdot
\left(r_s+0.9V_\pi(s_2)\right)
+
0.5\cdot 1\cdot
\left(5+0.9\cdot0\right)
$$

Por tanto:

$$
\boxed{
V_\pi(s_6)
=
0.5\left(r_s+0.9V_\pi(s_2)\right)+2.5
}
$$

### Estado $s_{10}$

$$
V_\pi(s_{10})
=
0.5\cdot1\cdot
\left(r_s+0.9V_\pi(s_6)\right)
+
0.5\cdot1\cdot
\left(r_s+0.9V_\pi(s_{14})\right)
$$

Por tanto:

$$
\boxed{
V_\pi(s_{10})
=
0.5\left(r_s+0.9V_\pi(s_6)\right)
+
0.5\left(r_s+0.9V_\pi(s_{14})\right)
}
$$

### Estado $s_5$

$$
V_\pi(s_5)
=
0.5\cdot1\cdot
\left(r_s+0.9V_\pi(s_{10})\right)
+
0.5\cdot1\cdot
\left(-5+0.9\cdot0\right)
$$

Por tanto:

$$
\boxed{
V_\pi(s_5)
=
0.5\left(r_s+0.9V_\pi(s_{10})\right)-2.5
}
$$

---

## 2. Rango de valores de $r_s$

Para este apartado:

$$
r_{\text{obs}}=-5,
\qquad
r_{\text{goal}}=+5,
\qquad
\gamma=1
$$

Queremos determinar el rango de valores de $r_s$ para el que la política óptima lleva al agente a la celda objetivo **lo antes posible** desde todos los estados desde los que el objetivo es alcanzable.

Los estados desde los que el objetivo **no** es alcanzable son:

$$
s_1,\;s_{15},\;s_{16},\;s_{18},\;s_{19}
$$

Al ser:

$$
\gamma=1
$$

no hay deterioro de las recompensas debido al descuento.

Algunas relaciones entre los valores de los estados son:

$$
V^*(s_7)=5
$$

$$
V^*(s_3)=r_s+V^*(s_7)
$$

$$
V^*(s_2)=r_s+V^*(s_7)
$$

$$
V^*(s_{17})=r_s+V^*(s_{14})
$$

$$
V^*(s_6)
=
\max\left(
5,\;
r_s+V^*(s_2)
\right)
$$

$$
V^*(s_{11})=r_s+V^*(s_7)
$$

$$
V^*(s_{14})=5
$$

$$
V^*(s_{13})=r_s+V^*(s_{11})
$$

$$
V^*(s_{10})
=
\max\left(
r_s+V^*(s_6),\;
r_s+V^*(s_{14})
\right)
$$

$$
V^*(s_9)=r_s+V^*(s_{13})
$$

$$
V^*(s_{12})=r_s+V^*(s_9)
$$

$$
V^*(s_8)=r_s+V^*(s_5)
$$

$$
V^*(s_5)
=
\max\left(
r_s+V^*(s_{10}),\;
-5
\right)
$$

$$
V^*(s_4)=r_s+V^*(s_9)
$$

$$
V^*(s_0)=r_s+V^*(s_5)
$$

### Desarrollo de los máximos

Para $s_6$:

$$
V^*(s_6)
=
\max\left(
5,\;
r_s+V^*(s_2)
\right)
$$

Como:

$$
V^*(s_2)=r_s+5
$$

entonces:

$$
V^*(s_6)
=
\boxed{
\max(5,\;2r_s+5)
}
$$

Si:

$$
r_s\leq0
$$

se elige el camino directo al objetivo.

En cambio, si:

$$
r_s>0
$$

se cumple:

$$
2r_s+5>5
$$

por lo que compensa dar una vuelta más para acumular recompensas $r_s$.

Esta condición proporciona el **límite superior**:

$$
r_s<0
$$

Para $s_{10}$:

$$
V^*(s_{10})
=
\max\left(
r_s+V^*(s_6),\;
r_s+V^*(s_{14})
\right)
$$

Sustituyendo:

$$
V^*(s_{10})
=
\max\left(
r_s+\max(5,2r_s+5),\;
r_s+5
\right)
$$

Para $r_s\leq0$:

$$
V^*(s_{10})=r_s+5
$$

mientras que para $r_s>0$ aparece el término:

$$
3r_s+5
$$

favoreciendo caminos más largos.


### Límite inferior

Hay que comprobar también los estados en los que puede resultar más rentable caer en un obstáculo que continuar hasta el objetivo.

Por ejemplo:

$$
V^*(s_5)
=
\max(-5,\;2r_s+5)
$$

Otro caso:

$$
V^*(s_8)
=
\max(3r_s+5,\;-5)
$$

y de forma similar:

$$
V^*(s_9)
=
\max(-5,\;3r_s+5)
$$

Para $s_{17}$:

$$
V^*(s_{17})
=
\max(r_s+5,\;-5)
$$

El caso más restrictivo es $s_{12}$:

$$
V^*(s_{12})
=
\max(4r_s+5,\;-5)
$$

Para que compense alcanzar el objetivo:

$$
4r_s+5>-5
$$

$$
4r_s>-10
$$

$$
r_s>-2.5
$$

Por tanto, el **límite inferior** es:

$$
r_s>-2.5
$$

### Resultado

Combinando ambos extremos:

$$
\boxed{
-2.5<r_s<0
}
$$

es decir:

$$
\boxed{
r_s\in(-2.5,0)
}
$$

Si $r_s>0$, el agente prefiere caminos más largos para acumular más recompensas $r_s$. Esto se observa, por ejemplo, en:

$$
V^*(s_6)=\max(5,2r_s+5)
$$

donde para $r_s>0$ se elige el camino más largo. Este comportamiento se propaga posteriormente a otros estados, como $s_{10}$.

Si:

$$
r_s<-2.5
$$

en $s_{12}$ resulta mejor obtener la recompensa $-5$ correspondiente a terminar el episodio que seguir avanzando hasta el objetivo.

---

## 3. ¿Existe una única política óptima?

No.

Por ejemplo, al llegar a $s_{10}$ tenemos dos acciones que proporcionan el mismo retorno:

$$
V^*(s_{10})
=
\max(r_s+5,\;r_s+5)
$$

Por tanto, existen dos decisiones distintas que llevan al mismo retorno óptimo.

En consecuencia:

$$
\boxed{\text{La política óptima no es única}}
$$