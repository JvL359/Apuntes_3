# Transformada de Laplace

# Enfoque

1. Presentar la **definición** de la Transformada de Laplace.
    
2. Explicar cómo convierte derivadas/condiciones iniciales en términos algebraicos.
    
3. Exponer las **propiedades fundamentales** (linealidad, derivadas, integrales, retardos, multiplicación por ttt).
    
4. Estudiar los **teoremas del valor inicial y final**.
    
5. Ver cómo aplicamos Laplace a la **resolución de ecuaciones diferenciales** y a la definición de **función de transferencia** (Tema 3).
    

---

# Desarrollo

## 1) Definición de Transformada de Laplace

Para una señal x(t)x(t)x(t), su transformada de Laplace es:

X(s)=L{x(t)}=∫0−∞x(t)e−st dtX(s) = \mathcal{L}\{x(t)\} = \int_{0^-}^{\infty} x(t) e^{-st}\, dtX(s)=L{x(t)}=∫0−∞​x(t)e−stdt

- Se pasa del dominio temporal ttt al dominio complejo s=σ+jωs = \sigma + j\omegas=σ+jω.
    
- La integral empieza en 0−0^-0− para incluir condiciones iniciales (valores justo antes de t=0t=0t=0).
    
- Las señales de interés en este curso (exponenciales, senoidales, escalones) **sí tienen transformada**.
    
- La mayoría serán **causales**: x(t)=0x(t)=0x(t)=0 para t<0t<0t<0. Esto simplifica mucho los cálculos.
    

---

## 2) Propiedades básicas

- **Linealidad**:
    
    L{Ax1(t)+Bx2(t)}=AX1(s)+BX2(s)\mathcal{L}\{Ax_1(t)+Bx_2(t)\} = A X_1(s)+B X_2(s)L{Ax1​(t)+Bx2​(t)}=AX1​(s)+BX2​(s)
- **Derivadas** (clave para transformar ecuaciones diferenciales):
    
    L{x˙(t)}=sX(s)−x(0−)\mathcal{L}\{\dot x(t)\} = sX(s) - x(0^-)L{x˙(t)}=sX(s)−x(0−) L{x(n)(t)}=snX(s)−sn−1x(0−)−⋯−x(n−1)(0−)\mathcal{L}\{x^{(n)}(t)\} = s^n X(s) - s^{n-1}x(0^-) - \dots - x^{(n-1)}(0^-)L{x(n)(t)}=snX(s)−sn−1x(0−)−⋯−x(n−1)(0−)
    
    ⇒ Las derivadas se convierten en **potencias de sss** más **condiciones iniciales**.
    
- **Integral**:
    
    L{∫0tx(τ) dτ}=X(s)s\mathcal{L}\left\{ \int_0^t x(\tau)\,d\tau \right\} = \frac{X(s)}{s}L{∫0t​x(τ)dτ}=sX(s)​
- **Retardo**:
    
    L{x(t−t0)}=e−st0X(s),t0>0\mathcal{L}\{x(t-t_0)\} = e^{-st_0}X(s), \quad t_0>0L{x(t−t0​)}=e−st0​X(s),t0​>0
- **Multiplicación por ttt**:
    
    L{tx(t)}=−dX(s)ds\mathcal{L}\{t x(t)\} = -\frac{dX(s)}{ds}L{tx(t)}=−dsdX(s)​
    
    Generalización: L{tnx(t)}=(−1)ndnX(s)dsn\mathcal{L}\{t^n x(t)\} = (-1)^n \frac{d^n X(s)}{ds^n}L{tnx(t)}=(−1)ndsndnX(s)​.
    

---

## 3) Teoremas de valores

- **Valor inicial**:
    
    x(0+)=lim⁡s→∞sX(s)x(0^+) = \lim_{s\to\infty} sX(s)x(0+)=s→∞lim​sX(s)
    
    Útil para comprobar condiciones iniciales.
    
- **Valor final** (solo si el límite existe y el sistema es estable):
    
    x(∞)=lim⁡s→0sX(s)x(\infty) = \lim_{s\to 0} sX(s)x(∞)=s→0lim​sX(s)

Estos teoremas conectan directamente el comportamiento en tiempo con la expresión en sss.

---

## 4) Tablas de transformadas frecuentes

Algunas señales base:

- Escalón unitario u(t)u(t)u(t):  
      L{1}=1s\; \mathcal{L}\{1\} = \frac{1}{s}L{1}=s1​
    
- Exponencial e−atu(t)e^{-at}u(t)e−atu(t):  
      1s+a,ℜ(s)>−a\; \frac{1}{s+a}, \quad \Re(s)>-as+a1​,ℜ(s)>−a
    
- Seno y coseno:  
      L{sin⁡(ωt)}=ωs2+ω2\; \mathcal{L}\{\sin(\omega t)\} = \frac{\omega}{s^2+\omega^2}L{sin(ωt)}=s2+ω2ω​  
      L{cos⁡(ωt)}=ss2+ω2\; \mathcal{L}\{\cos(\omega t)\} = \frac{s}{s^2+\omega^2}L{cos(ωt)}=s2+ω2s​
    
- Delta de Dirac δ(t)\delta(t)δ(t):  
      L{δ(t)}=1\; \mathcal{L}\{\delta(t)\} = 1L{δ(t)}=1
    

Estas funciones serán la base de todas las entradas que estudiemos.

---

## 5) Resolución de ecuaciones diferenciales con Laplace

Dado un modelo LTI:

any(n)(t)+⋯+a0y(t)=bmu(m)(t)+⋯+b0u(t)a_n y^{(n)}(t)+\dots+a_0 y(t) = b_m u^{(m)}(t)+\dots+b_0 u(t)an​y(n)(t)+⋯+a0​y(t)=bm​u(m)(t)+⋯+b0​u(t)

1. Aplicar Laplace:  
    se convierten derivadas en polinomios de sss más condiciones iniciales.
    
2. Reorganizar:  
    obtener Y(s)Y(s)Y(s) en función de U(s)U(s)U(s) y condiciones iniciales.
    
3. Separar:
    
    - **Respuesta forzada**: depende de U(s)U(s)U(s).
        
    - **Respuesta libre**: depende de condiciones iniciales.
        
4. Aplicar antitransformada para volver a y(t)y(t)y(t).
    

---

# Ejemplo ilustrativo

Ecuación de un circuito RC:

y˙(t)+1RCy(t)=1RCu(t),y(0)=y0\dot y(t)+\frac{1}{RC}y(t)=\frac{1}{RC}u(t), \quad y(0)=y_0y˙​(t)+RC1​y(t)=RC1​u(t),y(0)=y0​

1. Aplicamos Laplace:
    

sY(s)−y(0)+1RCY(s)=1RCU(s)sY(s)-y(0)+\frac{1}{RC}Y(s)=\frac{1}{RC}U(s)sY(s)−y(0)+RC1​Y(s)=RC1​U(s)

2. Reordenamos:
    

Y(s)=1RCU(s)s+1/RC+y(0)s+1/RCY(s)=\frac{1}{RC}\frac{U(s)}{s+1/RC} + \frac{y(0)}{s+1/RC}Y(s)=RC1​s+1/RCU(s)​+s+1/RCy(0)​

- Primer término → **respuesta forzada**.
    
- Segundo término → **respuesta libre**.
    

3. La antitransformada da la clásica respuesta exponencial.
    

---

# Conclusión

La **Transformada de Laplace** es el puente entre el mundo temporal y el algebraico:

- Convierte ecuaciones diferenciales en polinomios de sss.
    
- Permite separar respuesta libre y forzada.
    
- Introduce de forma natural la **función de transferencia** G(s)=Y(s)/U(s)G(s)=Y(s)/U(s)G(s)=Y(s)/U(s), que será nuestro modelo principal a partir del Tema 3.
    

---

# Qué queda establecido

- Definición rigurosa de la transformada de Laplace.
    
- Propiedades clave: linealidad, derivadas, integral, retardo, multiplicación por ttt.
    
- Teoremas de valor inicial y final.
    
- Tablas básicas (escalón, exponencial, seno, coseno, delta).
    
- Procedimiento para resolver ecuaciones diferenciales y separar respuesta libre/forzada.


Siguiente tema en [[Tema 2]]