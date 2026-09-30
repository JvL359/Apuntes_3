---
estado: pendiente de revisión
---

### I. From 2D Images to 3D and Video

#### 1. New Spatial and Temporal Dimensions

> Una imagen describe posiciones de **altura y anchura**; si es RGB, incorpora además tres canales de color. Una escena 3D añade una dimensión espacial de **profundidad** y puede describirse, por ejemplo, mediante un volumen $(D,H,W)$. Un vídeo añade **tiempo**: es una secuencia de $T$ imágenes, habitualmente representada como $(T,C,H,W)$ si se explicitan los canales.

> Profundidad y tiempo son dimensiones distintas aunque ambas permitan usar operadores sobre tensores de cuatro ejes sin contar el lote. La primera localiza geometría en el espacio; la segunda describe movimiento y cambios de la escena. Elegir la representación determina qué información queda explícita, cuánto cuesta almacenarla y qué arquitectura puede procesarla.

#### 2. 3D Representations

##### 2.1. Depth Maps

> Un **depth map** asocia a cada píxel de la imagen un único valor de profundidad: su forma espacial es $H\times W$ y tiene **un canal**. Los valores pequeños representan puntos cercanos a la cámara y los grandes puntos lejanos. Se utiliza, por ejemplo, para estimar la disposición 3D de una escena o apoyar la navegación y la estimación de pose. Los tonos de gris o colores de un mapa visualizado son una codificación gráfica de esos valores, no una dimensión adicional del dato.

##### 2.2. Surface Normals

> Un **surface normal map** guarda en cada píxel un vector $\vec n=(n_x,n_y,n_z)$ perpendicular a la superficie visible. Su forma es $3\times H\times W$: describe la **orientación local**, mientras que el mapa de profundidad describe la **distancia** a la cámara. Las componentes pueden mostrarse como canales RGB para visualizar cambios de orientación; esos colores no son el color real de la superficie. Las normales permiten razonar sobre geometría local, iluminación y sombreado.

##### 2.3. Implicit Functions

> Una **implicit function** $f(x,y,z)$ define continuamente una superficie como su conjunto de ceros:

$$
\mathcal S=\{(x,y,z)\in\mathbb R^3:f(x,y,z)=0\}.
$$

> Por ejemplo, $x^2+y^2+z^2-r^2=0$ describe la esfera de radio $r$ centrada en el origen. Con una convención de signo adecuada, $f<0$ señala el interior y $f>0$ el exterior. La ecuación $x^2+y^2-4=0$ forma un cilindro circular en 3D porque no depende de $z$; $x^2+y^2-z^2=0$ forma un cono doble. La función puede evaluarse en cualquier punto, sin fijar una cuadrícula, aunque reconstruir una superficie densa exige muchas evaluaciones o un muestreo adaptado.

> Una función implícita con signo **no tiene por qué medir distancia euclídea**. En la esfera, $x^2+y^2+z^2-r^2$ tiene el signo y el conjunto de ceros correctos, mientras que la distancia euclídea firmada a su superficie es

$$
d(x,y,z)=\sqrt{x^2+y^2+z^2}-r.
$$

> [!warning] Corrección
> En los apuntes se presenta $x^2+y^2+z^2-r$ como distancia a la esfera. Falta la raíz cuadrada: la distancia euclídea firmada para una esfera centrada en el origen es $\sqrt{x^2+y^2+z^2}-r$.
> Fuente de comprobación: [Hart, *Sphere Tracing: A Geometric Method for the Antialiased Ray Tracing of Implicit Surfaces*](https://graphics.stanford.edu/courses/cs348b-20-spring-content/uploads/hart.pdf).

##### 2.4. Voxels

> Un **voxel** es la celda de una cuadrícula volumétrica regular, análoga al píxel en 2D. Un volumen de resolución $V$ por eje tiene $V\times V\times V$ celdas. Cada una puede almacenar solo ocupación o varios atributos, como color, densidad o temperatura; con $n$ valores por celda, la forma es $V\times V\times V\times n$. La regularidad facilita las convoluciones 3D, pero el número de celdas y el consumo de memoria crecen **cúbicamente** con la resolución, incluso si gran parte del espacio está vacío.

##### 2.5. Point Clouds

> Una **point cloud** representa una forma como un conjunto de $P$ puntos con coordenadas $(x,y,z)$, opcionalmente acompañadas de color, intensidad o normales. Solo almacena posiciones muestreadas, por lo que suele ser más ligera y flexible que una cuadrícula densa de voxels. A cambio, carece de vecindad y orden regulares: una CNN convencional no puede tratar directamente la lista como una rejilla espacial. Permutar el orden de los puntos no debería cambiar la clase predicha para la nube.

### II. 3D Processing and Representation Prediction

#### 3. 3D Convolutions

##### 3.1. Input, Kernels, and Output

> Una **3D convolution** extiende la convolución 2D al eje de profundidad de un volumen o al eje temporal de un vídeo. En la convención de PyTorch, la entrada sin lote tiene forma $(C_{\mathrm{in}},D,H,W)$ y, con lote, $(N,C_{\mathrm{in}},D,H,W)$; para vídeo se sustituye $D$ por $T$. Los pesos de una capa con $C_{\mathrm{out}}$ filtros tienen forma

$$
(C_{\mathrm{out}},C_{\mathrm{in}},K_D,K_H,K_W).
$$

> Cada kernel recorre profundidad, altura y anchura y combina todos los canales de entrada conectados, pero **no se desplaza a lo largo del eje de canales**. Así puede aprender relaciones espaciales volumétricas o patrones de movimiento locales entre fotogramas. Los kernels y los mapas intermedios ocupan más memoria y requieren más operaciones que sus análogos 2D.

##### 3.2. Output Dimensions and 3D Pooling

> Con *stride* $S=(S_D,S_H,S_W)$, *padding* $P=(P_D,P_H,P_W)$ y *dilation* $\delta=(\delta_D,\delta_H,\delta_W)$, cada dimensión de salida se calcula como en 2D, incluyendo ahora profundidad:

$$
\begin{aligned}
D_{\mathrm{out}}&=\left\lfloor
\frac{D+2P_D-\delta_D(K_D-1)-1}{S_D}+1
\right\rfloor,\\
H_{\mathrm{out}}&=\left\lfloor
\frac{H+2P_H-\delta_H(K_H-1)-1}{S_H}+1
\right\rfloor,\\
W_{\mathrm{out}}&=\left\lfloor
\frac{W+2P_W-\delta_W(K_W-1)-1}{S_W}+1
\right\rfloor.
\end{aligned}
$$

> El tensor de salida mide $(C_{\mathrm{out}},D_{\mathrm{out}},H_{\mathrm{out}},W_{\mathrm{out}})$, o $(C_{\mathrm{out}},T_{\mathrm{out}},H_{\mathrm{out}},W_{\mathrm{out}})$ en vídeo, sin contar el lote. **Max pooling 3D** toma el máximo de cada bloque espacial o espaciotemporal; **average pooling 3D** calcula su media. Con la misma geometría de kernel, *stride* y *padding*, reducen las dimensiones de forma análoga a la convolución, pero no aprenden filtros. En un bloque $K_D\times K_H\times K_W$, la media pondera cada posición por $1/(K_DK_HK_W)$.

#### 4. Predicting 3D Representations

##### 4.1. Depth Prediction and Scale-Invariant Loss

> Para predecir profundidad desde una imagen RGB se puede usar una **FCN** con una salida de un canal y una pérdida de regresión por píxel, como el error cuadrático medio. La dificultad es que una imagen aislada puede mostrar un objeto pequeño y cercano igual que uno grande y lejano: su **escala absoluta** no siempre se deduce de la proyección. La figura muestra esta ambigüedad.

![[Pasted image 20260930140100.png]]

> Cuando importa más la estructura relativa que la escala absoluta, se usa una **scale-invariant loss**. Para profundidades reales $y_{ij}>0$, predicciones $\hat y_{ij}>0$, $N=HW$ y $0\leq\lambda\leq1$, se define

$$
\mathcal L(y,\hat y)=
\frac1N\sum_{i=1}^{H}\sum_{j=1}^{W}
\big(\log y_{ij}-\log\hat y_{ij}\big)^2
-\frac{\lambda}{N^2}
\left(\sum_{i=1}^{H}\sum_{j=1}^{W}
(\log y_{ij}-\log\hat y_{ij})\right)^2.
$$

> El primer término penaliza el error logarítmico de cada píxel y el segundo compensa un desplazamiento común de todos esos errores. Con $\lambda=0$ la escala influye por completo; entre $0$ y $1$ la compensación es parcial; con $\lambda=1$ la pérdida es invariante al cambio global $\hat y_{ij}\mapsto c\hat y_{ij}$ para $c>0$. El logaritmo es esencial para convertir ese cambio multiplicativo en un desplazamiento común.

##### 4.2. Surface Normal Prediction

> La predicción de normales también puede usar una FCN, ahora con **tres canales de salida** por píxel. Para comparar direcciones se utiliza **cosine distance** entre la normal real $\vec y_{ij}$ y la predicha $\vec{\hat y}_{ij}$, ambas no nulas:

$$
\mathcal L(y,\hat y)=\frac1{HW}
\sum_{i=1}^{H}\sum_{j=1}^{W}
\left(1-
\frac{\vec y_{ij}\cdot\vec{\hat y}_{ij}}
{\|\vec y_{ij}\|_2\|\vec{\hat y}_{ij}\|_2}
\right).
$$

> Una dirección coincidente aporta $0$; una perpendicular, $1$; y una opuesta, $2$. Esta pérdida atiende a la orientación y evita que la magnitud del vector domine la comparación.

##### 4.3. Implicit Fields and Voxel Classification

> Para **aproximar una función implícita** se muestrean puntos $(x,y,z)$ del espacio, se calcula para cada uno la etiqueta deseada —por ejemplo, una distancia firmada— y se entrena un modelo de regresión que devuelve **un escalar por punto**. Después puede consultarse el modelo en nuevas coordenadas y buscar el nivel $f=0$.

> Para **clasificar un objeto voxelizado**, una red puede recibir el volumen completo, aplicar convoluciones y opcionalmente *pooling* 3D, aplanar sus características y usar una MLP para obtener un vector de puntuaciones de clase. La pérdida es cross-entropy multiclase o binary cross-entropy para una decisión binaria. Esta salida única clasifica el **objeto representado por el volumen**; una etiqueta para cada voxel exigiría una salida densa diferente.

##### 4.4. Point Cloud Classification

> Para clasificar una nube de $P$ puntos, se aplica **la misma MLP a cada punto** para obtener un vector de $D$ rasgos: una matriz $P\times D$. Después se agrega sobre el eje de puntos mediante **máximo o media**, y otra MLP transforma el vector agregado en puntuaciones de clase. Una agregación simétrica da la misma salida aunque se permute el orden de los puntos. El diagrama muestra que la salida del *max pooling* ya no depende de $P$.

![[Pasted image 20260930140101.png]]

> Como en la clasificación del volumen, la pérdida puede ser cross-entropy multiclase o binary cross-entropy. Una MLP aplicada directamente a una lista aplanada de coordenadas no incorpora por sí misma esa invariancia al orden.

### III. 3D Shape Evaluation and Generation

#### 5. Shape Comparison Metrics

##### 5.1. Intersection over Union (IoU)

> Para dos conjuntos de voxels ocupados $P$ y $Q$, **IoU** mide cuánto solapan:

$$
d_{\mathrm{IoU}}(P,Q)=\frac{|P\cap Q|}{|P\cup Q|}.
$$

> Vale $1$ si la ocupación coincide y se acerca a $0$ cuando apenas hay intersección. Una estructura muy fina puede estar geométricamente cerca de la predicción y, por un pequeño desplazamiento, tener IoU casi nula. En una nube de puntos dispersos, la intersección exacta de coordenadas suele ser vacía: para usar solapamiento volumétrico hay que representar regiones ocupadas o reconstruir sólidos.

> [!warning] Corrección
> El material afirma que IoU solo puede aplicarse a voxels. También se define para el **volumen** de dos sólidos o mallas cerradas: la intersección y la unión se miden por volumen, sin exigir una rejilla voxelizada.
> Fuente de comprobación: [Paschalidou et al., evaluación de volumetric IoU para mallas 3D](https://www.cvlibs.net/publications/Paschalidou2021CVPR_supplementary.pdf).

##### 5.2. Chamfer Distance

> La **Chamfer distance** compara dos conjuntos finitos de puntos sin correspondencias conocidas. Para cada punto de $P$ busca el más cercano en $Q$, hace lo mismo en sentido contrario y suma ambas medias de distancias euclídeas **al cuadrado**:

$$
d_C(P,Q)=
\frac1{|P|}\sum_{p\in P}\min_{q\in Q}\|p-q\|_2^2
+
\frac1{|Q|}\sum_{q\in Q}\min_{p\in P}\|q-p\|_2^2.
$$

> Es **simétrica** y vale $0$ si los dos conjuntos coinciden. Para comparar mallas u otras representaciones se pueden muestrear puntos de sus superficies. También se emplea como pérdida durante el entrenamiento, pues admite gradientes salvo en cambios de vecino más cercano o empates. Su limitación es que puntos atípicos alejados pueden aumentar mucho el valor, especialmente con distancias cuadráticas.

##### 5.3. F1 Score at a Distance Threshold

> El **F1 score** evalúa cobertura con una tolerancia espacial $\delta>0$. Sea $P$ el conjunto predicho y $G$ el real. La **precision** es la fracción de puntos predichos a distancia como máximo $\delta$ de algún punto real; el **recall** es la fracción de puntos reales a distancia como máximo $\delta$ de algún punto predicho:

$$
\begin{aligned}
\mathrm{precision}_{\delta}
&=\frac{|\{p\in P:\min_{g\in G}\|p-g\|_2\leq\delta\}|}{|P|},\\
\mathrm{recall}_{\delta}
&=\frac{|\{g\in G:\min_{p\in P}\|g-p\|_2\leq\delta\}|}{|G|},\\
F1_{\delta}
&=2\frac{\mathrm{precision}_{\delta}\,\mathrm{recall}_{\delta}}
{\mathrm{precision}_{\delta}+\mathrm{recall}_{\delta}}.
\end{aligned}
$$

> Si ambas fracciones son cero, se toma $F1_\delta=0$. Una tolerancia puede fijarse, por ejemplo, como un porcentaje del tamaño del objeto. El resultado es sensible a $\delta$: no se deben comparar puntuaciones calculadas con umbrales distintos. En el ejemplo visual, precision $=3/4$ y recall $=2/3$ dan un F1 próximo a $0.70$.

##### 5.4. Choosing a Metric

> Las tres métricas responden a preguntas diferentes. En la figura, dos farolas finas casi coinciden pero no se superponen: **IoU** puede ser cercana a $0$, **Chamfer** pequeña y **F1** cercana a $1$ si $\delta$ cubre el pequeño desplazamiento. Ninguna puntuación debe interpretarse sin saber si mide volumen, distancia media o cobertura tolerante.

![[Pasted image 20260930140102.png]]

| Métrica | Comparación principal | Mejor valor | Limitación destacada |
| --- | --- | --- | --- |
| IoU | Solapamiento de regiones ocupadas. | $1$ | Penaliza mucho desplazamientos de estructuras finas. |
| Chamfer | Distancia entre puntos cercanos en ambos sentidos. | $0$ | Sensible a puntos atípicos. |
| $F1_\delta$ | Precision y recall dentro de una tolerancia. | $1$ | Depende del umbral $\delta$. |

#### 6. Datasets and Point Cloud Generation

##### 6.1. 3D Datasets

> **ShapeNet** reúne más de $50\,000$ modelos 3D sintéticos organizados en unas $55$ categorías, normalmente como mallas poligonales; resulta útil para clasificación, segmentación y reconstrucción. **ShapeNetCore** proporciona un subconjunto más consistente y **ShapeNetSem** añade anotaciones semánticas. **Pix3D** reúne más de $10\,000$ imágenes reales de objetos vinculadas a modelos 3D alineados y datos de pose de cámara, máscaras y puntos clave; permite estudiar recuperación de formas y vistas nuevas desde imágenes. ShapeNet ofrece geometría curada y variada; Pix3D introduce iluminación, oclusiones y ruido reales.

##### 6.2. Generating a Point Cloud from an Image

> Una arquitectura de reconstrucción puede extraer primero características de una imagen mediante una CNN 2D y dividirse después en **dos ramas**. Una rama *fully connected* predice $P_1$ puntos globales, de forma $P_1\times3$, para representar la estructura general. La otra rama convolucional predice $P_2$ puntos locales por posición de un mapa $H''\times W''$: parte de $3P_2\times H''\times W''$ y reorganiza la salida como $(H''W''P_2)\times3$.

> Al concatenar las ramas se obtiene una nube de $(P_1+H''W''P_2)\times3$ que combina forma global y detalles locales. La **Chamfer distance** entre esta nube y la real puede servir como pérdida de entrenamiento. En el esquema, los puntos rojos proceden de la rama global y los azules de la local.

![[Pasted image 20260930140103.png]]

### IV. Video Understanding

#### 7. Action Recognition and Fusion Strategies

##### 7.1. Video Data and the Task

> Un vídeo de $T$ fotogramas RGB tiene forma $(T,3,H,W)$ antes del lote. El eje temporal aporta movimiento y evolución de objetos, pero multiplica almacenamiento y cálculo. A $30$ fotogramas por segundo, un minuto de vídeo RGB $1920\times1080$ sin comprimir ocupa alrededor de $11$ GB; por ello suele reducirse resolución o frecuencia de muestreo. También aparecen cambios de iluminación, desenfoque por movimiento y oclusiones, y reunir etiquetas fiables para secuencias es costoso.

> **Action recognition** asigna una clase a una actividad, como correr o saltar, a partir de una secuencia. Existe variación **intraclase** —personas, velocidades, cámaras e iluminación distintas para una misma acción— e **interclase** —acciones visualmente parecidas, como comer y beber—. Una imagen aislada puede reconocer objetos presentes, pero para distinguir ciertas acciones hace falta observar su evolución temporal.

##### 7.2. Single-Frame CNN

> El punto de partida es clasificar cada fotograma, o una muestra de ellos, con una CNN 2D y combinar las puntuaciones mediante una **fusion layer**, por ejemplo promediándolas. Es un *baseline* sencillo y admite un número variable de fotogramas cuando la agregación es una media. Su límite es que cada predicción individual ve solo la apariencia estática y no compara explícitamente movimientos entre fotogramas.

##### 7.3. Late Fusion

> En **late fusion** se procesa cada fotograma con la misma CNN 2D y se combinan después sus características. Si cada salida tiene forma $(D,H',W')$, los $T$ mapas forman $(T,D,H',W')$. Una variante aplana y concatena todos los rasgos, de tamaño $TDH'W'$, antes de una MLP; otra promedia sobre $T$, $H'$ y $W'$ para obtener un vector de tamaño $D$ y reducir memoria. En ambos casos la fusión reúne información visual de alto nivel, pero la CNN individual no aprende comparaciones de movimiento de bajo nivel entre fotogramas.

##### 7.4. Early Fusion

> En **early fusion** se concatenan los fotogramas sobre el eje de canales **antes** de la CNN: $(T,3,H,W)\rightarrow(3T,H,W)$. La primera convolución 2D puede combinar información de distintos instantes; después la red continúa como clasificador 2D. Esta representación exige un $T$ fijado por los canales de entrada y puede tener demasiados canales cuando la secuencia es larga. Además, el lugar temporal de un evento queda ligado a canales concretos.

##### 7.5. 3D CNN and C3D

> Una **3D CNN** conserva separado el eje temporal: recibe $(C,T,H,W)$ en formato de convolución 3D y aplica kernels y *pooling* que recorren tiempo y espacio. Así aprende patrones de movimiento locales a lo largo de varias capas. **C3D** es un ejemplo con convoluciones $3\times3\times3$, reducción progresiva y una cabeza de clasificación; el primer *pooling* puede preservar la longitud temporal antes de reducirla en niveles posteriores.

> Este tratamiento es costoso: en las configuraciones comparadas, el coste es de aproximadamente $0.7$ GFLOP para AlexNet, $13.6$ para VGG-16 y $39.5$ para C3D bajo sus configuraciones respectivas. La convolución temporal aporta **tolerancia** a pequeños desplazamientos de la acción en el tiempo, pero no garantiza invariancia temporal perfecta. Una CNN de fotogramas con promedio temporal admite longitudes variables; una 3D CNN también puede hacerlo si agrega temporalmente antes del clasificador, mientras que aplanar todos los instantes hacia una MLP fija exige longitud constante.

#### 8. Motion and Two-Stream Models

##### 8.1. Optical Flow

> **Optical flow** estima el desplazamiento aparente de píxeles entre fotogramas consecutivos. En una posición $(x,y)$ del instante $t$, $\mathbf F_t(x,y)=(u_t,v_t)$ indica el vector hacia la posición correspondiente $(x+u_t,y+v_t)$ del siguiente fotograma. Bajo la hipótesis aproximada de constancia de brillo, la intensidad satisface

$$
I_t(x,y)\approx I_{t+1}(x+u_t,y+v_t).
$$

> El flujo aporta dirección y magnitud de movimiento. Con $T$ fotogramas consecutivos se obtienen como máximo $T-1$ campos entre pares adyacentes. Métodos como TV-L1 o RAFT pueden estimarlos, aunque el cálculo añade coste y sus errores afectan a los modelos posteriores.

> [!warning] Corrección
> En el material aparece $I_{t+1}(x,y)=I_t(x,y)+\mathbf F_t(x,y)=(x_t+dx_t,y_t+dy_t)$. Una intensidad de imagen no puede sumarse a un vector de desplazamiento. El flujo desplaza la **coordenada** a $(x+u_t,y+v_t)$; la relación entre intensidades es la aproximación de constancia de brillo escrita arriba.
> Fuente de comprobación: [documentación oficial de OpenCV sobre optical flow](https://docs.opencv.org/4.12.0/d4/dee/tutorial_optical_flow.html).

##### 8.2. Two-Stream Flow Networks

> Una **two-stream flow network** combina una rama **spatial** alimentada con RGB, que aprende apariencia y objetos, y una rama **temporal** alimentada con flujo óptico, que aprende movimiento. Los $T-1$ flujos de dos componentes pueden apilarse como $2(T-1)$ canales de tamaño $H\times W$ para una CNN 2D. La rama RGB puede usar varios esquemas de vídeo o, para ahorrar cálculo, un fotograma representativo.

> Las dos ramas pueden fusionar sus características por concatenación seguida de una MLP o combinar puntuaciones predichas por separado. El diagrama muestra la primera posibilidad. La separación aprovecha redes 2D preentrenadas y hace explícita la información de movimiento, a costa de calcular flujo y mantener dos ramas; el rendimiento depende de la calidad del flujo.

![[Pasted image 20260930140104.png]]

##### 8.3. Inflated 3D ConvNets (I3D)

> **I3D** adapta filtros preentrenados 2D a 3D añadiendo una dimensión temporal. Si $W^{2D}\in\mathbb R^{C_{\mathrm{out}}\times C_{\mathrm{in}}\times K_H\times K_W}$ y se elige un kernel temporal de tamaño $K_T$, cada rebanada se inicializa como

$$
W^{3D}[:,:,t,:,:]=\frac{1}{K_T}W^{2D},
\qquad t=0,\ldots,K_T-1.
$$

> En una ventana temporal válida cuyos $K_T$ fotogramas son idénticos, las $K_T$ respuestas iguales se suman y reproducen la respuesta inicial del filtro 2D; sin el factor $1/K_T$ quedaría multiplicada por $K_T$. Es solo una **inicialización**: durante el aprendizaje las rebanadas pueden divergir y captar movimiento. El esquema ilustra la copia y el reparto de pesos.

![[Pasted image 20260930140105.png]]

#### 9. Benchmarks and Long-Term Temporal Models

##### 9.1. Sports-1M and Short-Clip Comparison

> **Sports-1M** reúne alrededor de un millón de vídeos deportivos de duración media cercana a cinco minutos y unas quinientas categorías. Sus etiquetas se obtuvieron automáticamente de metadatos, por lo que pueden contener ruido y un vídeo puede tener varias etiquetas. Por restricciones de distribución se facilitan identificadores, no los vídeos, cuya disponibilidad depende de la plataforma. En esta comparación se usa **top-5 accuracy**: acierto si una etiqueta verdadera figura entre las cinco puntuaciones más altas.

| Modelo | Sports-1M top-5 accuracy |
| --- | ---: |
| Single-frame CNN | 77.7 % |
| Early fusion | 76.8 % |
| Late fusion | 78.7 % |
| 3D CNN | 80.2 % |
| C3D | 84.4 % |

> Estos valores comparan configuraciones concretas en ese conjunto; muestran que incorporar tiempo puede ayudar, sin establecer una jerarquía universal para todos los datos y presupuestos de cómputo.

##### 9.2. CNN and LSTM

> Las CNN temporales anteriores se centran en patrones de clips relativamente cortos. Para modelar dependencias más largas, una CNN 2D puede extraer un vector de características por fotograma y una **LSTM** procesar esos vectores secuencialmente. La CNN puede entrenarse conjuntamente o mantenerse fija para abaratar el entrenamiento. Una cabeza sobre el último estado produce una predicción por vídeo; cabezas sobre varios estados permiten predicciones por fotograma, útiles si cambian las acciones durante la secuencia.

##### 9.3. SlowFast Networks

> **SlowFast** usa dos rutas temporales complementarias. La ruta **Slow** procesa menos fotogramas y más canales para recoger apariencia y semántica; la **Fast** procesa cambios rápidos con mayor frecuencia temporal y menos canales. Si un mapa Slow tiene forma $(C,T,H,W)$, el correspondiente Fast puede describirse como $(\beta C,\alpha T,H,W)$, con valores típicos $\alpha=8$ y $\beta=1/8$; también se ha estudiado $\beta=1/6$. Conexiones laterales fusionan rasgos entre rutas en varias etapas, como muestra el esquema.

![[Pasted image 20260930140106.png]]

> [!warning] Corrección
> Una diapositiva dice que la ruta Fast tiene «$\beta$ veces más canales» y a la vez fija $\beta=1/8$. La relación correcta es $C_{\mathrm{Fast}}=\beta C_{\mathrm{Slow}}$: con $\beta=1/8$, Fast tiene **una octava parte** de los canales de Slow.
> Fuente de comprobación: [artículo original de SlowFast Networks](https://arxiv.org/abs/1812.03982).

##### 9.4. Kinetics-400 Comparison

> Otra comparación utiliza **top-1 accuracy** en Kinetics-400 y distingue entrenamiento desde cero de preentrenamiento en ImageNet. Todos los modelos de esa comparación usan una base Inception CNN:

| Modelo | Desde cero | Con preentrenamiento |
| --- | ---: | ---: |
| Per-frame CNN | 57.9 % | 62.2 % |
| CNN + LSTM | 53.9 % | 63.3 % |
| Two-stream CNN | 62.8 % | 65.6 % |
| Inflated CNN | 68.4 % | 71.1 % |
| Two-stream inflated CNN | 71.6 % | 74.2 % |

> El preentrenamiento mejora los resultados de todas las configuraciones mostradas. En este experimento, la combinación de dos flujos con convoluciones infladas logra el valor más alto; la comparación no mide por sí sola coste, latencia ni generalización fuera del conjunto.

#### 10. Other Video Tasks

> **Temporal Action Localization (TAL)** busca **cuándo** ocurre una acción en un vídeo largo: devuelve intervalos $[\mathrm{inicio},\mathrm{fin}]$ y etiquetas, incluso si hay varias acciones o se solapan. **Spatio-Temporal Action Detection** busca además **dónde** ocurre: asocia la acción a una persona u objeto localizado mediante cajas en los fotogramas pertinentes. La segunda tarea combina las dificultades de delimitar el intervalo temporal con las de detectar y seguir al actor en la imagen.

### V. Exercises

#### 11. Proposed Exercises

> Se conservan los diez enunciados como actividades, sin desarrollar soluciones nuevas.

1. **3D Convolution Arithmetic:** hallar la forma exacta tras aplicar $64$ filtros $3\times7\times7$ a un vídeo $(T,C,H,W)=(16,3,112,112)$, con *stride* $(1,2,2)$, sin *padding* y con *dilation* normal.
2. **Manual 3D Convolution:** escoger un kernel entero $2\times2\times2$ y calcular a mano el primer corte temporal y espacial de salida para una entrada de un canal $3\times1\times5\times5$, *stride* $1$ y *padding* $0$.
3. **Kernel Inflation:** construir un kernel 3D de profundidad temporal $5$ a partir de uno 2D $3\times3$ preentrenado y justificar su respuesta inicial sobre un vídeo estático.
4. **Scale-Invariant Loss:** demostrar que, para $\lambda=1$, multiplicar todas las profundidades predichas por una constante positiva no cambia la pérdida.
5. **Surface Normal Distances:** calcular la distancia coseno para normales unitarias alineadas, perpendiculares y opuestas.
6. **Memory Complexity:** comparar el número de voxels de un espacio de $100\,\mathrm m$ por eje con resolución de $0.1\,\mathrm m$ y los puntos de una esfera hueca central de radio $10\,\mathrm m$ muestreada a $100$ puntos por metro cuadrado.
7. **Chamfer Distance:** demostrar simetría y valor cero para conjuntos idénticos, y explicar la sensibilidad a un punto aislado lejano.
8. **Point Cloud Metrics:** implementar en Python el $F1_\delta$ de dos nubes de puntos usando un umbral de distancia $\delta$.
9. **Point Clouds:** analizar por qué una MLP sobre coordenadas aplanadas depende del orden y cómo una MLP compartida por punto seguida de *max pooling* evita esa dependencia.
10. **Video Architecture Baselines:** escribir pseudocódigo PyTorch para late fusion con promedio temporal, early fusion y 3D CNN a partir de $(B,T,C,H,W)$; comparar parámetros y captura de movimiento local.

### VI. Final Summary

> La elección entre **depth maps**, normales, funciones implícitas, voxels y nubes de puntos equilibra información geométrica, continuidad, regularidad y memoria. Las convoluciones y el *pooling* 3D procesan volumen o tiempo; las pérdidas deben corresponder a la salida: regresión y compensación de escala para profundidad, distancia coseno para normales y distancias o cobertura para formas. IoU mide solapamiento, Chamfer proximidad de puntos y $F1_\delta$ cobertura con tolerancia.

> En vídeo, la fusión de fotogramas puede hacerse antes o después de una CNN 2D, mientras que una CNN 3D aprende patrones espaciotemporales directamente. Las redes de dos flujos combinan apariencia y optical flow; I3D infla filtros 2D; CNN+LSTM modela secuencias más largas y SlowFast reparte el análisis entre dos velocidades temporales. TAL añade localización en el tiempo y la detección espaciotemporal añade también la localización en la imagen.
