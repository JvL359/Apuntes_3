# Introducción a los Sistemas Dinámicos

# Enfoque

1. Fijar **qué es un sistema dinámico** y cómo lo representamos (entradas, salidas, variables internas).

2. Distinguir **estáticos vs. dinámicos** y ver por qué los dinámicos “tienen memoria”.

3. Presentar el **modelo matemático** que usaremos en el curso: ecuaciones diferenciales lineales con coeficientes constantes (LTI).

4. Recordar lo esencial de **números complejos** (formas, módulo, argumento y operaciones) para manejar respuestas senoidales, exponenciales y la notación de Laplace.

---

# Desarrollo

## 1) Sistema, señal y modelo (definiciones operativas)

- **Sistema**: cualquier realidad física de interés (eléctrico, mecánico, térmico, hidráulico, biológico, económico…). Trabajaremos con sistemas de muy distinta escala, desde un circuito hasta una red eléctrica. Las variables físicas (tensión, corriente; posición, velocidad; temperatura, etc.) se describen mediante **señales** $x(t)$ (funciones del tiempo).

- **Entrada** $u(t)$ y **salida** $y(t)$: clasificamos las señales por su papel causa–efecto. La **entrada** es la excitación impuesta; la **salida** es lo que queremos observar/controlar. Pueden existir **variables internas** (estados) de menor interés directo.

- **Señales típicas**: constantes, exponenciales, senoidales (a veces amortiguadas) y combinaciones lineales; serán nuestras “piezas de LEGO” para construir respuestas.

- **Modelo**: conjunto de ecuaciones (en este tema, ecuaciones diferenciales) que relacionan entradas, salidas y, si hace falta, estados. Un buen modelo captura lo esencial con la menor complejidad posible.

### Estáticos vs. dinámicos

- **Estático**: la salida depende solo del **valor actual** de la entrada. No almacena energía (no hay “memoria”). Ej: resistor puro (circuito puramente resistivo).

- **Dinámico**: la salida depende de **valores previos** de la entrada (porque hay almacenamiento de energía). Ej: circuito **RC**: la corriente y la tensión del condensador dependen de cómo venía cambiando la señal (derivadas), no solo de su valor actual. Por eso “recuerda” el pasado reciente.

> **Ejemplo ilustrativo**: RC serie con entrada $v_i(t)$ y salida $v_o(t)$ en el condensador. Aparecen una resistencia $R$ (disipa) y un condensador $C$ (almacena energía eléctrica). La presencia de $C$ confiere **dinámica**.

---

## 2) Cómo modelaremos: ecuaciones diferenciales LTI

En el curso trabajaremos con **modelos lineales e invariantes en el tiempo (LTI)** descritos por ecuaciones diferenciales lineales con coeficientes constantes:

			$\sum_{i=0}^{n} a_i \frac{d^i y(t)}{dt^i} \;=\; \sum_{j=0}^{m} b_j \frac{d^j u(t)}{dt^j}, \qquad a_n \neq 0,$

o, con notación compacta (y la notación de puntos para derivadas: $\dot{y}, \ddot{y}, \ldots$) cuando no haya ambigüedad. Estas ecuaciones aparecen de forma natural al **linealizar** modelos físicos y al aplicar leyes básicas (Kirchhoff en eléctricos; Newton en mecánicos) más **componentes almacenadores** (condensadores, bobinas; masas, resortes, etc.).

- **Linealidad** significa que rige el **principio de superposición** (suma de efectos).

- **Invariancia temporal**: las propiedades del sistema no cambian con el tiempo (los coeficientes $a_i, b_j$​ son constantes).

- **Orden** del sistema: el máximo orden de derivada en la salida $y$.

- **Condiciones iniciales** $y(0^-), \dot y(0^-), \ldots$ fijan la **respuesta libre** (debida a energía almacenada), mientras que la **respuesta forzada** viene de la entrada $u(t)$. (La separación libre/forzada se usará continuamente a partir del Tema 2 y 3).

> **Ejemplo RC** (continuación): aplicando leyes de circuito se obtiene un modelo de **primer orden** del tipo  $\tau \dot y(t)+(t)=K u(t), \ \ \tau=RC,  K=1,$  cuya solución total es “libre + forzada”. (Veremos su análisis detallado en Tema 5.)

---

## 3) Números complejos (herramientas del curso)

Usaremos complejos para: (i) representar senoidales de forma compacta, (ii) trabajar con **polos** y **ceros** en el plano complejo, (iii) manejar exponenciales complejas $e^{st}$ (Laplace), fasores y respuestas en frecuencia.

- **Formas**
    - **Cartesiana/binómica**: $z=x+j y$.
    
    - **Polar (módulo–argumento)**: $z=r e^{j\theta}=r(cos⁡\theta+jsin⁡\theta)$
    
    - **Parte real/imaginaria, módulo y argumento**:  $\operatorname{Re}\{z\}=x,\;\operatorname{Im}\{z\}=y$
    
    - **Módulo y argumento**: $r=|z|=\sqrt{x^2+y^2},\; \theta=\arg z$

- **Valores principales**  
    El argumento no es único: $\theta + 2k\pi$. Usamos **valor principal** en $(-\pi,\pi]$ y, en aplicaciones de control, es común preferir fases negativas para evitar saltos aparentes en $\pm\pi$. **Cuidado frecuente**: no usar $arctan⁡(y/x)$ a ciegas; emplear **atan2(y,x)** para obtener el cuadrante correcto.

- **Operaciones**
    - Sumas/restas: cómodas en **cartesiana**.
    
    - Productos/cocientes/potencias/raíces: cómodos en **polar**: 
		    $z_1 z_2 = (r_1 r_2)e^{j(\theta_1+\theta_2)}, \quad \frac{z_1}{z_2} = \frac{r_1}{r_2} e^{j(\theta_1-\theta_2)}, \quad z^n = r^n e^{jn\theta}.$        
		    Para **raíces n-ésimas**: $z_k^{1/n} = r^{1/n} e^{j\frac{\theta + 2\pi k}{n}}, \quad k = 0, \ldots, n-1.$
    
    - **Desigualdad triangular**: $|z_1 + z_2| \leq |z_1| + |z_2|.$ (Recordatorio útil al acotar magnitudes).

> **Interpretación geométrica**: los complejos viven en el **plano complejo** (eje real y eje imaginario). La **suma** se entiende como suma de vectores; el **producto** rota y escala (suma de argumentos y producto de módulos). Esto es clave al interpretar **polos/ceros** en el plano $s = \sigma+j\omega$

---

# Comprobación (mini-ejercicios guiados)

### A) ¿Es dinámico o estático?

Tienes un **resistor** con tensión $v(t)$ e intensidad $i(t)=v(t)/R$.

- Depende solo del valor **instantáneo** de $v(t)$ ⇒ **estático**, **sin memoria**.  
    Ahora añade un **condensador** $C$: $i_C(t)=C\,\dot v_C(t)$.

- Aparece una derivada ⇒ salida depende de cómo cambiaba antes ⇒ **dinámico**. ✔️

### B) Modelo RC serie (entrada $v_i$​, salida $v_C$)

Ley de mallas y relación del condensador ⇒ $RC\,\dot v_C(t)+v_C(t)=v_i(t)$.

Es un **sistema LTI de 1er orden**, $\tau=RC$, **estable** si $R,C>0$. Con paso a escalón, la salida sube **exponencialmente** hacia el valor final con constante de tiempo $\tau$. (Analizaremos su respuesta cuantitativa en Tema 5). ✔️

### C) Complejos: de cartesianas a polares y raíces

Sea $z=-1+j\sqrt{3}$.

- Módulo: $r=\sqrt{(-1)^2+(\sqrt{3})^2}=2$.

- Argumento **principal** (cuadrante II): $\theta=\operatorname{atan2}(\sqrt{3},-1)=2\pi/3$.

- Forma polar: $z=2\,e^{j2\pi/3}$.

- Raíces cúbicas: $z_k^{1/3}=2^{1/3}e^{j(2\pi/3+2\pi k)/3},$  $k=0,1,2$.  
    Verifica que las tres raíces están separadas $120^\circ$ en el plano. ✔️

---

# Conclusión

En el **Tema 1** fijamos el idioma de todo el curso:

- qué entendemos por **sistema** y **señales** (entrada/salida),

- cómo distinguir **estáticos** (sin memoria) de **dinámicos** (con almacenamiento de energía),

- qué **modelo LTI** usaremos (ecuaciones diferenciales lineales con coeficientes constantes),

- y el **kit de herramientas complejas** imprescindible para analizar senoidales, polos/ceros y trabajar en el plano s.

Esto nos prepara para introducir la **Transformada de Laplace** (Tema 2), la **Función de Transferencia** (Tema 3) y el análisis de **primer/segundo orden** (Temas 5 y 6).

---

# Qué queda establecido

- **Sistema/Señal/Modelo**: definiciones, roles de **entrada/salida** y existencia de **variables internas**.

- **Dinámico ≠ estático**: el primero **almacena energía** y su salida depende del pasado (ejemplos RC/elementos C,L); el segundo no.

- **Modelo base del curso**: ecuaciones diferenciales **LTI** (linealidad + invariancia temporal), orden, condiciones iniciales y separación **libre/forzada**.

- **Complejos**: formas, módulo, **argumento principal**, uso de **atan2**, operaciones (producto/cociente/potencias/raíces) y lectura geométrica en el plano complejo.


Siguiente tema en [[Tema 2]]