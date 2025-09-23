### I. ¿Qué es la Geometría Computacional?

1. Definición 
> La **Geometría Computacional (GC)** es la disciplina que estudia el diseño y análisis de algoritmos para resolver **problemas geométricos**.  
> Ejemplo: calcular la envolvente convexa de un conjunto de puntos, encontrar intersecciones, etc.

2. Orígenes
> Se podría decir que comienza con **Euclides**, cuando un problema geométrico se resuelve mediante pasos correctos y finitos. En **1902** aparece el concepto de _complejidad de resolución_ (todavía no computacional). El término **“Geometría Computacional” lo introduce M. I. Shamos en 1975**.

3. Nueva Visión de la Geometría 
> Con los ordenadores, los objetos geométricos se representan como estructuras de datos. Los métodos clásicos se convierten en algoritmos eficientes.

4. Ejemplo Ilustrativo
> Problema simple: encontrar un punto en una recta que minimice distancias → solución clásica con simetría (sin interés para GC).
> Problema de GC: dado un conjunto de n puntos (granjas), hallar el círculo mínimo que los contiene → aquí entra la necesidad de algoritmos eficientes.

### II. Aplicaciones de la GC

- **Informática gráfica** → modelado y renderizado de objetos.

- **Reconstrucción de modelos 3D** → ingeniería, medicina, arqueología.

- **Visión artificial** → reconocimiento de formas e interpretación de imágenes.

- **Sistemas de Información Geográfica (SIG)** → análisis de mapas y datos espaciales.

- **Robótica** → planificación de trayectorias y detección de colisiones.

- **Biología molecular** → estudio de estructuras de proteínas y ADN.

- **Astrofísica** → simulación de cuerpos celestes.

- **Diseño asistido por ordenador (CAD/CAM)** → arquitectura, fabricación industrial.

### III. Terminología
> Este apartado introduce el **lenguaje básico** de la GC. Se divide en tres bloques:

1. Elementos Geométricos Básicos
###### 1.1. Punto
> Un punto en el plano se puede representar como un **vector en ℝ²**, en **coordenadas cartesianas** o **polares**. Si $p=(x,y)$ y en polares $p=(r,\alpha),$ entonces:
> 	De cartesianas a polares:  $r_p = \sqrt{x_p^2 + y_p^2}, \quad \alpha_p = \arctan(y_p/x_p)$ 
> 	De polares a cartesianas: $x = r \cdot \cos(\alpha), \quad y = r \cdot \sin(\alpha)$
###### 1.2. Segmento AB
> Dados dos puntos $A$ y $B$, el segmento es el conjunto: $AB = \{ (1-\lambda)A + \lambda B \mid 0 \leq \lambda \leq 1 \}$
###### 1.3. Poligonal
> Una **cadena poligonal** es la unión de segmentos consecutivos dados por una lista ordenada de puntos $\{v_1, v_2, \dots, v_n\}.$ 
> 	**Poligonal simple:** sus lados solo se cortan en **extremos adyacentes**.
> 	**Poligonal cerrada:** Cuando además $v_n$​ se conecta con $v_1.$
###### 1.4. Polígono P 
> Es el conjunto del **interior** más la **poligonal cerrada**. Se usan:   
> 	$\mathrm{Int}(P)$ (interior), $\mathrm{Fr}(P)=\partial P$ (frontera), $\mathrm{Ext}(P)$ (exterior).  
> 	**Vértices:** un vértice es convexo si su ángulo interior es $\leq 180$ y es cóncavo si este es $>180.$
> 	**Nota de orientación:** salvo indicación en contra, $P$ viene dado por la lista cíclica $(v_1,\dots,v_n)$ **con orientación positiva** (antihoraria). Tras $v_n$​ sigue $v_1.$ 

2. Familias Notables de Polígonos
###### 2.1. Convexo
> Para todo par de puntos $x,y \in P,$ el segmento $xy \subseteq P.$
> Interpretación: todo punto del polígono se “ve” interiormente con cualquier otro.
###### 2.2. Estrellado
> Existe un punto $x \in P$ tal que **ve a todos los demás puntos del polígono**.
> El conjunto de tales puntos se llama **núcleo**: $Ker(P) = \{ x \in P \mid xy \subseteq P, \forall y \in P \}$
> Propiedades:
    - Si $P$ es convexo → $Ker(P)=P.$
    - Si $P$ es estrellado → $Ker(P) \neq \emptyset.$
    - Si un vértice está en $Ker(P),$ el polígono es un **abanico**.
###### 2.3. DVL (Débilmente Visible desde un Lado)
> Existe un lado $l$ tal que **cada punto del polígono** es visible desde algún punto de $l$.
> Metáfora: basta una barra fluorescente en $l$ para iluminar todo el interior.
###### 2.4. DVE (Débilmente Visible desde el Exterior)
> Para cada punto $x \in \partial P,$ existe un rayo que sale de $x$ y **no corta el interior del polígono**.
> Metáfora: una fortaleza donde un guardia en el muro siempre puede mirar al horizonte.
###### 2.5. Monótono (respecto a una dirección D)
> Sea una dirección $D$. El polígono $P$ es monótono respecto a $D$ si cualquier recta ortogonal a $D$ corta al polígono en **un único intervalo conexo** (o ninguno).
> Interpretación: se puede “barrer” el polígono con líneas ortogonales a $D$ sin que aparezcan varios intervalos separados.

3. Area Signada de un Triángulo
###### 3.1. Definición
> Dados 3 puntos $p_1=(x_1,y_1), p_2=(x_2,y_2), p_3=(x_3,y_3),$ definimos $\Delta(p_1,p_2,p_3) = \frac{1}{2} \cdot \begin{vmatrix} x_1 & y_1 & 1 \\ x_2 & y_2 & 1 \\ x_3 & y_3 & 1 \end{vmatrix}.$
> Respecto de la recta $p_1p_2$ el punto $p_3$ se encuentra:
> - Si $\Delta > 0$ → orientación positiva (contraria al reloj).
> - Si $\Delta < 0$→ orientación negativa (sentido horario).
> - Si $\Delta = 0$ → puntos alineados.
###### 3.2. Aplicaciones
> **Localización de un punto respecto a una recta**
    Con $\Delta(p_1,p_2,q)$ sabemos si $q$ está a la izquierda, derecha o sobre la recta.
> **Comparación de ángulos con π**
	Evita cálculos trigonométricos aproximados.      
>**Clasificación de vértices en un polígono**
    Si $\Delta(v_{i-1}, v_i, v_{i+1}) \geq 0$ → vértice **convexo**.
    Si es $<0$→ vértice **cóncavo**.
> **Área de un polígono**
    Para $P=(v_0,v_1,...,v_{n-1}):$ $Área(P) = \frac{1}{2} \sum_{i=0}^{n-1} \Delta(v_0, v_i, v_{i+1})$

### IV. Complejidad
> Cuando tenemos un problema geométrico, **pueden existir varios algoritmos distintos para resolverlo**. La _complejidad algorítmica_ es la herramienta que usamos para **compararlos objetivamente**, midiendo cuántos recursos consumen:
> 	- **Tiempo**: número de operaciones elementales.
> 	- **Espacio**: memoria usada.
> El interés está en el comportamiento cuando el tamaño de entrada n es grande → **análisis asintótico**.

1. Notación y definiciones
> Se define $T(n)$: tiempo de ejecución en función del tamaño de entrada n.
> 	- **O(f(n))**: cota superior (en el peor caso).
> 	- **Ω(f(n))**: cota inferior (mejor caso).
> 	- **Θ(f(n))**: orden exacto (cuando O y Ω coinciden).
> Ejemplo:  Si $T(n)=3n^2+5n$, entonces $T(n)=Θ(n^2).$

2. Tipos de análisis
> - **Peor caso:** entrada más desfavorable → garantiza que el algoritmo nunca será peor que eso.    
> - **Caso medio (esperado):** promedio sobre todas las entradas posibles, considerando probabilidades.
> En este curso, casi siempre se usa **peor caso** por ser más seguro.

3. Reglas Prácticas
###### 3.1. Suma de fragmentos:  
> Si $T_1(n)=O(f(n))$  y  $T_2(n)=O(g(n))$, entonces  $T(n)=T_1(n)+T_2(n)=O(\max(f(n),g(n)))$
    Nos quedamos con el dominante
    
###### 3.2. Constantes:  
> $O(c\cdot f(n))=O(f(n))$.
    
###### 3.3. Operaciones básicas (asignación, suma, comparación):  
> $O(1)$.
    
###### 3.4. Condicional:
> $O(\max(f(n),g(n)))$  porque solo se ejecuta una rama.
###### 3.5. Recursividad:
> - Ejemplo 1: $T(n)=c+T(n-1)$ → expansión → $O(n)$.
> - Ejemplo 2 (divide y vencerás): $T(n)=2T(n/2)+cn$  que se resuelve en $O(n\log n)$.

### V. Operaciones Básicas
> a

1. Intersección de Segmentos
> Dados dos segmentos $ab$ y $cd$, queremos saber si se cortan en algún punto (intersección **propia**) o si comparten un extremo (intersección **impropia**).
> Para que $ab$ y $cd$ se corten:
> 	1. Los puntos no deben ser **colineales**.
> 	2. $d$ debe estar a la **izquierda** de $ab$ y $c$ a la **derecha** (o al revés).
> 	3. Simétricamente, $a$ debe estar a la **derecha** de $cd$  y $b$ a la **izquierda** (o al revés).
> **Casos borde:**
> 	- Intersección impropia: ocurre cuando un extremo coincide con un punto del otro segmento.
> 	- Segmentos colineales solapados requieren un test adicional de proyección.

2. Cálculo de Diagonales
> Una **diagonal interna** conecta dos vértices del polígono y queda completamente en el interior. Es fundamental para **triangulación**.
> 1. En un **vértice convexo**: la diagonal es interna si:
    - $v_{i-1}$​ está a la izquierda de $v_i v_j$  y  $v_{i+1}$​ está a la derecha de $v_i v_j$​.
> 2. En un **vértice cóncavo**: la diagonal es interna si **no** ocurre que:
    - $v_{i-1}$​ está a la derecha de $v_i v_j$ ​ y  $v_{i+1}$​ está a la izquierda de $v_i v_j$​.
> Además, hay que comprobar que la diagonal **no interseca con ninguna arista del polígono**.

3. Cálculo de Tangentes
###### 3.1. Tangente desde un punto a un polígono convexo
> Dado un punto exterior $q$ y un vértice $v_i$​:  
> El segmento $qv_i$​ es tangente a $P$ si se cumple la condición XOR:
> 	- $q$ está a la izquierda de $v_{i-1}v_i$.
> 	- $q$ está a la izquierda de $v_iv_{i+1}$​.
###### 3.2. Tangentes comunes a dos polígonos convexos
> **Problema**: hallar las dos rectas tangentes que tocan ambos polígonos y no cortan sus interiores.
> **Algoritmo** (esquemático):
> 	1. Escoger el vértice más a la derecha de $A$ y el más a la izquierda de $B$.
> 	2. Ajustar hasta encontrar las tangentes comunes con pruebas de orientación.
> 	3. Complejidad: **O(n+m)**.

