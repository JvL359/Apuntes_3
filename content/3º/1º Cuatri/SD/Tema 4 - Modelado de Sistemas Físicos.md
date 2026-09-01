### I. Introducción al Modelado de Sistemas Físicos

#### Idea central
El propósito de este tema es **construir modelos matemáticos** de sistemas físicos reales (eléctricos, mecánicos, térmicos, hidráulicos) que luego podamos analizar con las herramientas de sistemas dinámicos.  
El modelo que buscamos debe ser suficientemente **sencillo** para trabajar con él, pero lo bastante **preciso** para capturar la dinámica esencial.
La herramienta final a la que queremos llegar en todos los casos es la **función de transferencia** $G(s)=\frac{Y(s)}{U(s)}$​, que describe cómo la salida responde a una entrada.

#### Objetivos del modelado
1. **Relacionar variables físicas** de entrada y salida (tensión, fuerza, temperatura, caudal…) mediante ecuaciones diferenciales.

2. **Identificar elementos básicos** de almacenamiento de energía (condensadores, bobinas, masas, muelles, depósitos, etc.) y disipación (resistencias, amortiguadores, pérdidas térmicas…).

3. **Unificar la representación** de diferentes dominios físicos gracias a analogías (electromecánicas, electrohidráulicas…).

4. **Obtener G(s)G(s)G(s)** a partir de las leyes fundamentales (Kirchhoff en eléctricos, Newton en mecánicos, balances de energía en térmicos, ecuaciones de caudal en hidráulicos).

#### Estrategia de trabajo
El proceso de modelado sigue siempre el mismo guion:
1. **Plantear ecuaciones físicas**
    - Ley de Ohm, leyes de Kirchhoff (eléctrico).
    - $F=ma$, relaciones muelle-amortiguador (mecánico).
    - $Q = C \frac{dT}{dt}$​, flujos de calor (térmico).
    - $Q = C \frac{dp}{dt}$​, relaciones de caudal y presión (hidráulico).

2. **Expresar en forma de ecuación diferencial** que vincule la salida y la entrada.

3. **Transformar con Laplace** → relación algebraica en $s$.

4. **Aislar la función de transferencia** $G(s)$.

#### Comentarios clave
- El **mismo patrón matemático** aparece en dominios distintos:
    - Un circuito RC, un sistema masa–amortiguador o un sistema térmico con pérdidas tienen ecuaciones equivalentes de primer orden.
    - De forma análoga, sistemas con dos almacenadores (RLC, masa–resorte–amortiguador, depósito con inercia de caudal) conducen a **segundo orden**.

- Esto justifica el uso de **analogías eléctricas**: modelar un sistema no eléctrico como si fuese un circuito simplifica mucho el análisis.

- El objetivo no es solo obtener $G(s)$, sino también **interpretar físicamente polos, ceros y constantes de tiempo**: cada término está asociado a un mecanismo físico (almacenamiento o disipación).

### II. Circuitos eléctricos

#### Idea central
Los **circuitos eléctricos** son el punto de partida del modelado porque:
1. Su descripción se basa en **leyes muy sistemáticas** (Kirchhoff, constitutivas de los componentes).

2. Sus ecuaciones son directamente diferenciales → fáciles de trasladar a Laplace y obtener la función de transferencia.

3. Son el **modelo de referencia** para establecer analogías con sistemas mecánicos, térmicos e hidráulicos.

#### Elementos básicos y sus ecuaciones
- **Resistencia R**: disipa energía →  $v_R(t) = R\, i_R(t)$

- **Inductancia L**: almacena energía magnética →  $v_L(t) = L \frac{di_L}{dt}$
- **Condensador C**: almacena energía eléctrica →  $.i_C(t) = C \frac{dv_C}{dt}$

>[!note]  
>resistencia → disipación, bobina/capacitor → almacenamiento. Esta clasificación se repetirá en mecánica (amortiguador, masa, resorte) y en térmica (resistencias y capacidades térmicas).

---

#### Método de modelado

1. **Aplicar leyes de Kirchhoff**
    - **LKC (corrientes)**: suma de corrientes que entran en un nodo = 0.
    - **LKV (tensiones)**: suma de tensiones en un lazo cerrado = 0.

2. **Sustituir ecuaciones de los elementos** (R, L, C).

3. **Formar ecuación diferencial** entre entrada (tensión o corriente aplicada) y salida (tensión en un elemento o corriente).

4. **Transformar con Laplace** → obtener relación $Y(s)/U(s) = G(s)$

#### Ejemplos clave
##### 1. Circuito RC en serie (salida: tensión en el condensador)
- Ecuación diferencial:  $R C \frac{dv_C}{dt} + v_C(t) = v_{in}(t)$

- Función de transferencia:  $G(s) = \frac{V_C(s)}{V_{in}(s)} = \frac{1}{1 + RC\,s}$

- Tipo: **primer orden** con constante de tiempo $\tau = RC$

##### 2. Circuito RL en serie (salida: corriente)
- Ecuación:  $L \frac{di}{dt} + R i(t) = v_{in}(t)$

- Función de transferencia:  $G(s) = \frac{I(s)}{V_{in}(s)} = \frac{1}{Ls+R}$

- **Primer orden**, polo en  $-R/L$

##### 3. Circuito RLC en serie (salida: tensión en CCC)
- Ecuación:  $L C \frac{d^2 v_C}{dt^2} + R C \frac{dv_C}{dt} + v_C(t) = v_{in}(t)$

- Función de transferencia:  $G(s) = \frac{V_C(s)}{V_{in}(s)} = \frac{1}{LC s^2 + RC s + 1}$

- **Segundo orden**, con parámetros:
    - frecuencia natural  $\omega_n = 1/\sqrt{LC}$​
    - factor de amortiguamiento $\zeta = \tfrac{R}{2}\sqrt{C/L}$

Esto conecta directamente con lo que veremos en el **Tema 6 (sistemas de segundo orden)**.

#### Comentario final
- Los circuitos eléctricos son un **laboratorio matemático** perfecto: las ecuaciones se derivan de reglas sencillas, y las soluciones son representativas de la dinámica en cualquier dominio físico.

- Cada **constante de tiempo** o **polo** tiene interpretación física directa (resistencia disipa, condensador/inductor almacenan).

- Este apartado prepara el terreno para las **analogías electromecánicas**: masa ↔ inductancia, resorte ↔ condensador, amortiguador ↔ resistencia. 

### III. 