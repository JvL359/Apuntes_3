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

		$a_n y^{(n)}(t)+\cdots+a_1 \dot y(t)+a_0 y(t) = b_m u^{(m)}(t)+\cdots+b_1 \dot u(t)+b_0 u(t)$.

Aplicando Laplace (con condiciones iniciales distintas de cero en general) se obtiene

A(s) Y(s)=B(s) U(s)+C(s),A(s)\,Y(s)=B(s)\,U(s)+C(s),A(s)Y(s)=B(s)U(s)+C(s),

donde A(s)=ansn+⋯+a1s+a0A(s)=a_n s^n+\cdots+a_1 s + a_0A(s)=an​sn+⋯+a1​s+a0​, B(s)=bmsm+⋯+b1s+b0B(s)=b_m s^m+\cdots+b_1 s + b_0B(s)=bm​sm+⋯+b1​s+b0​, y C(s)C(s)C(s) recoge **todas** las condiciones iniciales.  
**Definición:** con condiciones iniciales nulas, la **función de transferencia** es

G(s)=Y(s)U(s)=B(s)A(s).G(s)=\frac{Y(s)}{U(s)}=\frac{B(s)}{A(s)}.G(s)=U(s)Y(s)​=A(s)B(s)​.

En general,

Y(s)=G(s) U(s)⏟forzada+C(s)A(s)⏟libre.Y(s)=\underbrace{G(s)\,U(s)}_{\text{forzada}}+\underbrace{\frac{C(s)}{A(s)}}_{\text{libre}}.Y(s)=forzadaG(s)U(s)​​+libreA(s)C(s)​​​.

Esto fija el papel de G(s)G(s)G(s) como modelo “entrada–salida” en sss.

## 2) Respuesta libre y forzada; polos, ceros y estabilidad

- **Polos**: raíces de A(s)=0A(s)=0A(s)=0. **Ceros**: raíces de B(s)=0B(s)=0B(s)=0.
    
- La **respuesta libre** depende solo de C(s)/A(s)C(s)/A(s)C(s)/A(s) (condiciones iniciales) y, por tanto, **de los polos**.
    
- La **respuesta forzada** es G(s)U(s)G(s)U(s)G(s)U(s): su forma en tiempo también está determinada por **polos** (y se ve afectada por **ceros**, p. ej. derivaciones o ceros en RHP).
    
- **Estabilidad (BIBO)**: para sistemas LTI causales, requerimos **todos los polos en el semiplano izquierdo** (ℜ{pi}<0\Re\{p_i\}<0ℜ{pi​}<0). Polos repetidos generan términos con factores en ttt (p. ej. teptt e^{p t}tept).
    

## 3) Régimen permanente: entradas constante y senoidal

Si el sistema es estable:

- **Entrada constante** u(t)=U0u(t)=U_0u(t)=U0​: el valor final es
    

y(∞)=G(0) U0,y(\infty)=G(0)\,U_0,y(∞)=G(0)U0​,

de modo que la **ganancia estática** G(0)G(0)G(0) dicta el régimen permanente ante escalón/constante.

- **Entrada senoidal** u(t)=U^sin⁡(ωt)u(t)=\hat U\sin(\omega t)u(t)=U^sin(ωt): el régimen permanente es senoidal a la **misma frecuencia** con **amplitud** ∣G(jω)∣ U^|G(j\omega)|\,\hat U∣G(jω)∣U^ y **fase** arg⁡G(jω)\arg G(j\omega)argG(jω). Esta es la base de la respuesta en frecuencia (módulo–fase).
    

## 4) Álgebra de **diagramas de bloques**

Nos permite **componer** subsistemas (cada bloque con su G(s)G(s)G(s)) y obtener una única FT equivalente:

- **Serie**: Geq(s)=G2(s) G1(s)G_{\text{eq}}(s)=G_2(s)\,G_1(s)Geq​(s)=G2​(s)G1​(s).
    
- **Paralelo**: Geq(s)=G1(s)+G2(s)G_{\text{eq}}(s)=G_1(s)+G_2(s)Geq​(s)=G1​(s)+G2​(s) (si suman señales).
    
- **Realimentación unitaria** (negativa):
    

Gcl(s)=G(s)1+G(s)H(s)(con H(s) en el lazo).G_{\text{cl}}(s)=\frac{G(s)}{1+G(s)H(s)}\quad\text{(con \(H(s)\) en el lazo)}.Gcl​(s)=1+G(s)H(s)G(s)​(con H(s) en el lazo).

Estas reglas permiten simplificar sistemas complejos y leer cómo cambian polos/ceros y la estabilidad en lazo cerrado.

## 5) Forma polos–ceros y **cancelaciones** (“casualidades”)

Es útil expresar G(s)G(s)G(s) como

G(s)=k ∏i(s−zi)∏j(s−pj).G(s)=k\,\frac{\prod_i (s-z_i)}{\prod_j (s-p_j)}.G(s)=k∏j​(s−pj​)∏i​(s−zi​)​.

Si **un cero y un polo coinciden**, se **elimina** el término asociado (residuo cero):

- **zb=paz_b = p_azb​=pa​**: _orden no mínimo_; un “modo” físico de la planta queda oculto en G(s)G(s)G(s). _No_ puede reconstruirse la E.D. solo desde G(s)G(s)G(s). Ese término desaparece de **toda respuesta forzada**, aunque puede seguir en la **libre** (y si es permanente, es crítico).
    
- **zu=paz_u = p_azu​=pa​**: cierto **tipo de entrada** (p. ej. una forma específica) **no excita** ese modo.
    
- **zc=paz_c = p_azc​=pa​**: ciertas **condiciones iniciales** “anulan” un modo.
    
- **zb=puz_b = p_uzb​=pu​**: una **FT** suprime el efecto de un **tipo de entrada** (útil para **filtros supresores**).
    
- **Polos múltiples** **refuerzan** el modo (aparecen factores en ttt). Caso especial: **pa=pup_a=p_upa​=pu​** puede producir **salida no acotada** ante entrada acotada (polo doble en el eje imaginario).  
    Estas “casualidades” explican **por qué** a veces un modo “desaparece” o queda realzado según la **entrada** o las **C.I.**.
    

## 6) Ejemplo rápido: RC como bloque de 1er orden

Para un RC con salida en el condensador:

G(s)=11+τs,τ=RC.G(s)=\frac{1}{1+\tau s},\qquad \tau=RC.G(s)=1+τs1​,τ=RC.

- **Polo** en s=−1/τs=-1/\taus=−1/τ (estable si R,C>0R,C>0R,C>0).
    
- **Ganancia estática** G(0)=1G(0)=1G(0)=1 ⇒ ante escalón U0U_0U0​, y(∞)=U0y(\infty)=U_0y(∞)=U0​.
    
- **Respuesta senoidal**: ∣G(jω)∣=11+(ωτ)2|G(j\omega)|=\frac{1}{\sqrt{1+(\omega\tau)^2}}∣G(jω)∣=1+(ωτ)2​1​, arg⁡G(jω)=−arctan⁡(ωτ)\arg G(j\omega)=-\arctan(\omega\tau)argG(jω)=−arctan(ωτ).  
    Este bloque aparece constantemente en composición serie/paralelo/realimentación.
    

---

# Comprobación

1. **Separación libre/forzada**  
    Desde A(s)Y=B(s)U+C(s)A(s)Y=B(s)U+C(s)A(s)Y=B(s)U+C(s):
    

Y=G U+CA.Y=G\,U+\frac{C}{A}.Y=GU+AC​.

Si pongo U=0U=0U=0, queda la **libre**; si pongo C=0C=0C=0, queda la **forzada**. Cuadra con la definición de G(s)G(s)G(s). ✔️

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