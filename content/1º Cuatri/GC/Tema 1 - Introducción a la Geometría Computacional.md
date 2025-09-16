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
> - Si $\Delta > 0$ → orientación positiva (contraria al reloj).
> - Si $\Delta < 0$→ orientación negativa (sentido horario).
> - Si $\Delta = 0$ → puntos alineados.
###### 3.2. Aplicaciones
> **Localización de un punto respecto a una recta**
    Con $\Delta(p_1,p_2,q)$sabemos si $q$ está a la izquierda, derecha o sobre la recta.
> **Comparación de ángulos con π**
	Evita cálculos trigonométricos aproximados.      
>**Clasificación de vértices en un polígono**
    Si $\Delta(v_{i-1}, v_i, v_{i+1}) \geq 0$ → vértice **convexo**.
    Si es $<0$→ vértice **cóncavo**.
> **Área de un polígono**
    Para $P=(v_0,v_1,...,v_{n-1}):$ $Área(P) = \frac{1}{2} \sum_{i=0}^{n-1} \Delta(v_0, v_i, v_{i+1})$




