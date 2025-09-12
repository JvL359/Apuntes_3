### I. Conceptos Preliminares
> Este bloque introduce las **herramientas fundamentales** que luego se usan en la formulación de problemas de optimización lineal y entera.

1. Tipos de Variables
En un modelo de optimización, las **variables de decisión** pueden ser de distintos tipos:

- **Variables continuas (ℝ):**  
    Pueden tomar cualquier valor real dentro de un intervalo.  
    Ejemplo:
    - Cantidad de helado producido (kg).
    - Temperatura de un congelador (grados).

- **Variables enteras (ℤ):**  
    Solo pueden tomar valores enteros (positivos, negativos o ambos).  
    Ejemplo:
    - Número de productos fabricados.
    - Número de empleados contratados.

- **Variables binarias (0-1):**  
    Solo pueden valer 0 o 1.  
    Ejemplo:
    - Abrir o no una planta de producción.
    - Asignar o no una tarea a un trabajador.

 > **Idea clave:** 
 >- LP (Linear Programming): todas las variables son continuas.
 >- IP (Integer Programming): todas las variables son enteras.
 >- BIP (Binary Integer Programming): todas son binarias.
 >- **MIP (Mixed Integer Programming):** mezcla de variables enteras/binarias y continuas.
 >- **MILP (Mixed Integer Linear Programming):** igual que MIP, pero con **función objetivo y restricciones lineales**.
 
2. Uso de conjuntos en ecuaciones
En problemas reales, trabajamos con **colecciones de objetos (conjuntos)**.  

Por ejemplo:
- Conjunto de productos $i \in I = \{1,2,\dots,n\}$.
- Conjunto de trabajadores $j \in J = \{1,2,\dots,m\}$.

Con ellos escribimos restricciones de forma compacta: $\sum_{i \in I} x_i \leq Q$
En lugar de escribir todas las desigualdades una por una.

> Esto permite que un modelo sea **escalable**: puedes resolver un problema con 5 o con 5.000 elementos sin cambiar la estructura.

3. Factibilidad y Optimalidad
En todo problema de optimización lineal distinguimos dos aspectos fundamentales:

- **Factibilidad:**  
    Una solución es **factible** si cumple todas las restricciones.  
    Ejemplo: en el problema de transporte, una asignación de camiones que respeta las capacidades y demandas.

- **Optimalidad:**  
    Una solución es **óptima** si, siendo factible, alcanza el mejor valor posible de la función objetivo (mínimo coste o máximo beneficio).


> [!warning] Casos posibles:
> 1. **Infeasible:** no hay ninguna solución que cumpla las restricciones.
> 2. **Unbounded:** la función objetivo puede crecer indefinidamente (sin cota superior/inferior).
> 3. **Óptimo alcanzado:** existe una solución factible que maximiza/minimiza el objetivo.

4. Variables enteras y binarias: codificación
A veces necesitamos representar una **variable entera** con un conjunto de binarias.

Ejemplo:  
Queremos modelar una variable entera $x$ con valores entre 0 y 5. Podemos usar 3 variables binarias: $y_0, y_1, y_2$​.
Teniendo $x = y_0 + 2y_1 + 4y_2,$ donde cada $y_i \in \{0,1\}$.

> Esto permite que los **solvers** manejen enteros complejos transformándolos en combinaciones binarias, que son más eficientes para los algoritmos de ramificación y acotamiento.

5. Clasificación resumida

| Tipo de Modelo | Variables | Función Objetivo | Restricciones |
| -------------- | --------- | ---------------- | ------------- |
| LP             | Continuas | Lineal           | Lineales      |
| IP             | Enteras   | Lineal           | Lineales      |
| BIP            | Binarias  | Lineal           | Lineales      |
| MIP            | E + C     | Lineal           | Lineales      |
| MILP           | E + C     | Lineal           | Lineales      |

### II. Problemas Arquetipo
> Los **problemas arquetípicos** son modelos clásicos de la Investigación Operativa. Aunque en la práctica no siempre aparecen tal cual, **muchos problemas reales pueden reducirse o inspirarse en ellos**. Sirven como “plantillas” para modelar.

1. Diet Problem
**Objetivo:** minimizar el coste de una dieta que cubra unos requisitos mínimos de nutrientes.

- **Conjuntos**  
    $i \in I = \{1,2,…,n\}$ → alimentos.

- **Parámetros**
    - $C_i$: coste por unidad de alimento $i$.
    - $V_i$​: valor de nutriente aportado por alimento $i$.
    - $B$: cantidad mínima de nutriente requerida.

- **Variables**  
    $x_i \geq 0$x: cantidad de alimento iii a elegir.

- **Modelo matemático**
	$\text{min } \sum_{i=1}^{n} C_i x_i$  s.a.  $\sum_{i=1}^{n} V_i x_i \geq B \quad x_i \geq 0 \quad \forall i$

> Es un **problema continuo** (LP). Muy útil para introducir el concepto de **mínimo coste bajo restricciones**.





> [!tip] **Resumen práctico**



