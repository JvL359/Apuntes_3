
# Enfoque

1. Presentar la **definición** de la Transformada de Laplace.

2. Explicar cómo convierte derivadas/condiciones iniciales en términos algebraicos.
 
3. Exponer las **propiedades fundamentales** (linealidad, derivadas, integrales, retardos, multiplicación por t).

4. Estudiar los **teoremas del valor inicial y final**.

5. Ver cómo aplicamos Laplace a la **resolución de ecuaciones diferenciales** y a la definición de **función de transferencia** (Tema 3).

---

# Desarrollo

## 1) Definición de Transformada de Laplace

Para una señal $x(t)$, su transformada de Laplace es: $$X(s) = \mathcal{L}\{x(t)\} = \int_{0^-}^{\infty} x(t) e^{-st}\, dt$$
- Se pasa del dominio temporal $t$ al dominio complejo $s = \sigma + j\omega$.

- La integral empieza en $0^-$ para incluir condiciones iniciales (valores justo antes de $t=0$).

- Las señales de interés en este curso (exponenciales, senoidales, escalones) **sí tienen transformada**.

- La mayoría serán **causales**: $x(t)=0$ para $t<0$. Esto simplifica mucho los cálculos.

---

## 2) Propiedades básicas

- **Linealidad**: 
            $\mathcal{L}\{Ax_1(t)+Bx_2(t)\} = A X_1(s)+B X_2(s)$

- **Derivadas** (clave para transformar ecuaciones diferenciales):
		    $\mathcal{L}\{\dot x(t)\} = sX(s) - x(0^-)$
		    $\mathcal{L}\{x^{(n)}(t)\} = s^n X(s) - s^{n-1}x(0^-) - \dots - x^{(n-1)}(0^-)$
			Las derivadas se convierten en **potencias de s** más **condiciones iniciales**.

- **Integral**: 
			$\mathcal{L}\left\{ \int_0^t x(\tau)\,d\tau \right\} = \frac{X(s)}{s}$

- **Retardo**: 
			$\mathcal{L}\{x(t-t_0)\} = e^{-st_0}X(s), \quad t_0>0$

- **Multiplicación por t**: 
			$\mathcal{L}\{t x(t)\} = -\frac{dX(s)}{ds}$
		    Generalización: $\mathcal{L}\{t^n x(t)\} = (-1)^n \frac{d^n X(s)}{ds^n}$.

---

## 3) Teoremas de valores

- **Valor inicial**: 
			$x(0^+) = \lim_{s\to\infty} \ sX(s)$.
		    Útil para comprobar condiciones iniciales.

- **Valor final** (solo si el límite existe y el sistema es estable): 
			$x(\infty) = \lim_{s\to 0} \ sX(s)$

Estos teoremas conectan directamente el comportamiento en tiempo con la expresión en s.

---

## 4) Tablas de transformadas frecuentes

Algunas señales base:

- Escalón unitario $u(t)$: $\mathcal{L}\{1\} = \frac{1}{s}$

- Exponencial $e^{-at}u(t)$): $\frac{1}{s+a}, \quad \Re(s)>-a$

- Seno y coseno: $\mathcal{L}\{\sin(\omega t)\} = \frac{\omega}{s^2+\omega^2} \ , \quad \mathcal{L}\{\cos(\omega t)\} = \frac{s}{s^2+\omega^2}$

- Delta de Dirac $\delta(t)$: $\mathcal{L}\{\delta(t)\} = 1$L

Estas funciones serán la base de todas las entradas que estudiemos.

---

## 5) Resolución de ecuaciones diferenciales con Laplace

   Dado un modelo LTI: 
			$a_n y^{(n)}(t)+\dots+a_0 y(t) = b_m u^{(m)}(t)+\dots+b_0 u(t)$

1. Aplicar Laplace: se convierten derivadas en polinomios de s más condiciones iniciales.

2. Reorganizar: obtener $Y(s)$ en función de $U(s)$ y condiciones iniciales.

3. Separar:
    - **Respuesta forzada**: depende de $U(s)$.
    - **Respuesta libre**: depende de condiciones iniciales.

4. Aplicar antitransformada para volver a $y(t)$.

---

# Ejemplo ilustrativo

   Ecuación de un circuito RC:
			$\dot y(t)+\frac{1}{RC}y(t)=\frac{1}{RC}u(t), \quad y(0)=y_0$

1. Aplicamos Laplace: 
			$sY(s)-y(0)+\frac{1}{RC}Y(s)=\frac{1}{RC}U(s)$

2. Reordenamos:
			$Y(s)=\frac{1}{RC}\frac{U(s)}{s+1/RC} + \frac{y(0)}{s+1/RC}$​
		- Primer término → **respuesta forzada**.
		- Segundo término → **respuesta libre**.

3. La antitransformada da la clásica respuesta exponencial.

---

# Conclusión

La **Transformada de Laplace** es el puente entre el mundo temporal y el algebraico:

- Convierte ecuaciones diferenciales en polinomios de s.

- Permite separar respuesta libre y forzada.

- Introduce de forma natural la **función de transferencia** $G(s)=Y(s)/U(s)$, que será nuestro modelo principal a partir del Tema 3.


---

# Qué queda establecido

- Definición rigurosa de la transformada de Laplace.

- Propiedades clave: linealidad, derivadas, integral, retardo, multiplicación por t.

- Teoremas de valor inicial y final.

- Tablas básicas (escalón, exponencial, seno, coseno, delta).

- Procedimiento para resolver ecuaciones diferenciales y separar respuesta libre/forzada.


