# Enfoque

1. Pasar de la **ecuación diferencial LTI** al dominio s para **definir G(s)G(s)G(s)** con total rigor.

2. Distinguir **respuesta libre** y **respuesta forzada** en s.

3. Entender **polos, ceros, estabilidad** y cómo determinan el tipo de respuesta.

4. Ver el **régimen permanente** ante entradas **constantes** y **senoidales**.

5. Manejar el **álgebra de diagramas de bloques** (serie, paralelo, realimentación).

6. Tratar **cancelaciones** entre polos y ceros (y sus “casualidades”).

---

# Desarrollo

## 1) De la E.D. LTI a la **función de transferencia**

Un sistema LTI (lineal e invariante en el tiempo) queda descrito por

$a_n y^{(n)}(t)+\cdots+a_1 \dot y(t)+a_0 y(t) = b_m u^{(m)}(t)+\cdots+b_1 \dot u(t)+b_0 u(t)$

Aplicando Laplace (con condiciones iniciales distintas de cero en general) se obtiene

$A(s)\,Y(s)=B(s)\,U(s)+C(s),$

donde $A(s)=a_n s^n+\cdots+a_1 s + a_0,$​ $B(s)=b_m s^m+\cdots+b_1 s + b_0,$ y $C(s)$ recoge **todas** las condiciones iniciales.  
**Definición:** con condiciones iniciales nulas, la **función de transferencia** es

$G(s)=\frac{Y(s)}{U(s)}=\frac{B(s)}{A(s)}$

En general: $Y(s)=\underbrace{G(s)\,U(s)}_{\text{forzada}}+\underbrace{\frac{C(s)}{A(s)}}_{\text{libre}}$

Esto fija el papel de $G(s)$ como modelo “entrada–salida” en s.

## 2) Respuesta libre y forzada; polos, ceros y estabilidad

- **Polos**: raíces de $A(s)=0$. **Ceros**: raíces de $B(s)=0$.

- La **respuesta libre** depende solo de $C(s)/A(s)$ (condiciones iniciales) y, por tanto, **de los polos**.

- La **respuesta forzada** es $G(s)U(s)$G: su forma en tiempo también está determinada por **polos** (y se ve afectada por **ceros**, p. ej. derivaciones o ceros en RHP).

- **Estabilidad (BIBO)**: para sistemas LTI causales, requerimos **todos los polos en el semiplano izquierdo** ($\Re\{p_i\}<0$). Polos repetidos generan términos con factores en t (p. ej. $t e^{p t}$).

## 3) Régimen permanente: entradas constante y senoidal

Si el sistema es estable:

- **Entrada constante** $u(t)=U_0$​: el valor final es $y(\infty)=G(0)\,U_0,$ de modo que la **ganancia estática** G(0)G(0)G(0) dicta el régimen permanente ante escalón/constante.

- **Entrada senoidal** $u(t)=\hat U\sin(\omega t)$: el régimen permanente es senoidal a la **misma frecuencia** con **amplitud** $|G(j\omega)|\,\hat U$ y **fase** $\arg G(j\omega)$. Esta es la base de la respuesta en frecuencia (módulo–fase).

## 4) Álgebra de **diagramas de bloques**

Nos permite **componer** subsistemas (cada bloque con su $G(s)$) y obtener una única FT equivalente:

- **Serie**: $G_{\text{eq}}(s)=G_2(s)\,G_1(s)$.

- **Paralelo**: $G_{\text{eq}}(s)=G_1(s)+G_2(s)$.

- **Realimentación unitaria** (negativa): $G_{\text{cl}}(s)=\frac{G(s)}{1+G(s)H(s)}\quad\text{(con \(H(s)\) en el lazo)}$.

Estas reglas permiten simplificar sistemas complejos y leer cómo cambian polos/ceros y la estabilidad en lazo cerrado.

## 5) Forma polos–ceros y **cancelaciones** (“casualidades”)

Es útil expresar $G(s)$ como $G(s)=k\,\frac{\prod_i (s-z_i)}{\prod_j (s-p_j)}$

Si **un cero y un polo coinciden**, se **elimina** el término asociado (residuo cero):

- $z_b = p_a$​: _orden no mínimo_; un “modo” físico de la planta queda oculto en $G(s)$. _No_ puede reconstruirse la E.D. solo desde $G(s)$. Ese término desaparece de **toda respuesta forzada**, aunque puede seguir en la **libre** (y si es permanente, es crítico).

- $z_u = p_a$: cierto **tipo de entrada** (p. ej. una forma específica) **no excita** ese modo.

- $z_c = p_a$​: ciertas **condiciones iniciales** “anulan” un modo.

- $z_b = p_u$: una **FT** suprime el efecto de un **tipo de entrada** (útil para **filtros supresores**).

- **Polos múltiples** **refuerzan** el modo (aparecen factores en t). Caso especial: $p_a=p_u$ puede producir **salida no acotada** ante entrada acotada (polo doble en el eje imaginario).  
    Estas “casualidades” explican **por qué** a veces un modo “desaparece” o queda realzado según la **entrada** o las **C.I.**.

## 6) Ejemplo rápido: RC como bloque de 1er orden

Para un RC con salida en el condensador: $G(s)=\frac{1}{1+\tau s},\quad \tau=RC$

- **Polo** en s=−1/τs=-1/\taus=−1/τ (estable si R,C>0R,C>0R,C>0).

- **Ganancia estática** $G(0)=1$ ⇒ ante escalón $U_0$​, $y(\infty)=U_0$​.

- **Respuesta senoidal**: $|G(j\omega)|=\frac{1}{\sqrt{1+(\omega\tau)^2}},$ $\arg G(j\omega)=-\arctan(\omega\tau)$.  
    Este bloque aparece constantemente en composición serie/paralelo/realimentación.

---

# Comprobación

1. **Separación libre/forzada**  
    Desde $A(s)Y=B(s)U+C(s)$: $Y=G\,U+\frac{C}{A}$

Si pongo $U=0$, queda la **libre**; si pongo $C=0$, queda la **forzada**. Cuadra con la definición de $G(s)$

2. **Valor final** (entrada constante, sistema estable)  
    y(∞)=lim⁡s→0s Y(s)=lim⁡s→0s G(s)U0s=G(0) U0\displaystyle y(\infty)=\lim_{s\to 0} s\,Y(s)=\lim_{s\to 0} s\,G(s)\frac{U_0}{s}=G(0)\,U_0y(∞)=s→0lim​sY(s)=s→0lim​sG(s)sU0​​=G(0)U0​. Coincide con lo afirmado. ✔️
	
3. **Estabilidad**  
    El RC tiene polo en −1/τ<0-1/\tau<0−1/τ<0 ⇒ estable. Si un diagrama en realimentación mueve polos al semiplano derecho, lazo cerrado **inestable**. ✔️
    
4. **Cancelación**  
    Si interconecto un bloque con cero en −1/τ-1/\tau−1/τ en **serie** con el RC (polo −1/τ-1/\tau−1/τ), ese modo puede **cancelarse** en GeqG_{\text{eq}}Geq​. Según el caso, puede desaparecer del término forzado, pero **no necesariamente** de la respuesta libre. ✔️
    

---

# Conclusión

- G(s)=B(s)A(s)G(s)=\dfrac{B(s)}{A(s)}G(s)=A(s)B(s)​ modela la relación **entrada–salida** con C.I. nulas; en general Y=G U+C/AY=G\,U+C/AY=GU+C/A.
    
- **Polos** dictan la **dinámica** (modos), **ceros** moldean la forzada y pueden producir **derivaciones** y **cancelaciones**.
    
- El **régimen permanente** con entrada constante y senoidal se lee de G(0)G(0)G(0) y G(jω)G(j\omega)G(jω).
    
- Los **diagramas de bloques** permiten sintetizar y simplificar sistemas complejos y estudiar la **realimentación**.
    

---

# Qué queda establecido

- **Definición operativa** de **función de transferencia** G(s)G(s)G(s) y su derivación desde la E.D. LTI.
    
- **Descomposición** de la respuesta en **libre** y **forzada**.
    
- **Polos, ceros y estabilidad**; lectura del régimen permanente (constante y senoidal) vía G(0)G(0)G(0) y G(jω)G(j\omega)G(jω).
    
- **Álgebra de bloques** (serie, paralelo, realimentación) para obtener GeqG_{\text{eq}}Geq​.
    
- **Cancelaciones** y “casualidades” (qué términos desaparecen o se refuerzan y en qué condiciones).