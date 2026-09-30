---
estado: pendiente de revisión
---

### I. Semantic Segmentation

#### 1. Pixel-Level Prediction

##### 1.1. Task and Output

> **Semantic segmentation** asigna una clase a **cada píxel** de la imagen. Frente a las *bounding boxes* de object detection, produce fronteras espaciales detalladas: un mismo mapa puede distinguir, por ejemplo, cielo, césped, árboles y animales. Todos los píxeles de una misma clase comparten etiqueta; esta tarea por sí sola no separa dos objetos distintos de esa clase.

> Para una imagen de altura $H$ y anchura $W$ con $C$ clases, la red debe devolver $C$ puntuaciones por posición espacial: un tensor $H\times W\times C$. Una **softmax sobre los canales** convierte esas puntuaciones en probabilidades cuya suma, en cada píxel, es $1$. La clase predicha es la de mayor probabilidad. Si en una posición los canales «gato» y «fondo» valen $0.61$ y $0.39$, respectivamente, el píxel se etiqueta como gato.

##### 1.2. Naive Sliding-Window Approach

> Un primer intento consiste en extraer un parche centrado en cada píxel, clasificar su centro con una CNN y recomponer el mapa de etiquetas. Un parche grande aporta más **contexto**, pero puede diluir los detalles útiles para clasificar con precisión el píxel central; uno pequeño preserva esos detalles, pero ve menos contexto. Además, hacen falta aproximadamente $HW$ pasadas de clasificación y se recalculan muchas características de parches solapados. Es más eficiente compartir los rasgos convolucionales y clasificar todos los píxeles en una misma pasada.

#### 2. Transposed Convolution and Upsampling

##### 2.1. Basic Operation

> Las convoluciones y el *pooling* suelen conservar o reducir la resolución. Para volver de un mapa compacto a una predicción por píxel se utiliza **transposed convolution**. Sin considerar canales, cada valor de entrada $X_{ij}$ multiplica un kernel $K$; el bloque $X_{ij}K$ se coloca en la salida en la posición correspondiente a $(i,j)$ y las contribuciones que se solapan se **suman**. El nombre «transpuesta» alude a la matriz de la operación convolucional, no a invertir exactamente una convolución previa.

> Con entrada $n_h\times n_w$, kernel $k_h\times k_w$, *stride* $1$ y *padding* $0$, la salida mide $(n_h+k_h-1)\times(n_w+k_w-1)$. Como ejemplo, tomamos la misma matriz para entrada y kernel:

$$
X=K=\begin{pmatrix}0&1\\2&3\end{pmatrix},\qquad
X\ast^{-1}K
=\begin{pmatrix}0&0&1\\0&4&6\\4&12&9\end{pmatrix}.
$$

> Por ejemplo, el valor central $4$ suma la contribución $1\cdot2$ del bloque situado arriba a la derecha y $2\cdot1$ del bloque situado abajo a la izquierda. Esta superposición explica que la operación no sea una simple inserción de ceros.

##### 2.2. Padding, Stride, and Channels

> En esta descripción de la convolución transpuesta, el **padding** $p$ recorta $p$ filas y columnas en cada borde de la salida sin recortar; con $p=1$, el ejemplo $3\times3$ anterior se reduce al valor central $(4)$. El **stride** $s$ determina cuánto se separan las posiciones donde se colocan los bloques $X_{ij}K$: se empieza en $(is,js)$. Para un único valor de *stride* y *padding* en ambas dimensiones, sin `output_padding`, las dimensiones son

$$
H_{\mathrm{out}}=(H_{\mathrm{in}}-1)s-2p+k_h,\qquad
W_{\mathrm{out}}=(W_{\mathrm{in}}-1)s-2p+k_w.
$$

> Si la altura y la anchura usan *padding* distinto, se sustituye $p$ por $p_h$ y $p_w$, respectivamente. Así, con la misma $X$ y $K$, $s=2$ y $p=0$ se obtiene una salida $4\times4$; la contribución de $X_{0,1}=1$ empieza dos columnas después de la de $X_{0,0}=0$:

$$
X\ast^{-1}_{s=2}K=
\begin{pmatrix}
0&0&0&1\\
0&0&2&3\\
0&2&0&3\\
4&6&6&9
\end{pmatrix}.
$$

> [!warning] Corrección
> En el ejemplo con *stride* $2$, la entrada de la segunda fila y tercera columna aparece como $1$ en las diapositivas y como $3$ en los apuntes; su valor correcto es $2=1\cdot K_{1,0}$. La matriz anterior incorpora ese valor.
> Fuente de comprobación: [Dive into Deep Learning, Transposed Convolution](https://classic.d2l.ai/chapter_computer-vision/transposed-conv.html).

> Con varios canales, cada canal de salida recibe un kernel $k_h\times k_w$ por canal de entrada y suma sus contribuciones. Por tanto, los pesos relacionan canales de entrada y de salida además de posiciones espaciales; el *upsampling* no obliga a conservar el número de canales.

##### 2.3. Upsampling Methods and Initialization

> Los kernels de una convolución transpuesta se pueden iniciar aleatoriamente o con pesos que reproduzcan un método conocido de ampliación. Para pasar de $2\times2$ a $4\times4$ con *stride* $2$ y *padding* $0$, los siguientes kernels reproducen ambos métodos:

| Método | Kernel inicial | Interpretación |
| --- | --- | --- |
| **Bed of Nails** | $\begin{pmatrix}1&0\\0&0\end{pmatrix}$ | Conserva cada valor en una de las posiciones ampliadas y rellena las demás con cero. |
| **Nearest Neighbor** | $\begin{pmatrix}1&1\\1&1\end{pmatrix}$ | Replica cada valor en un bloque $2\times2$. |

> **Bilinear interpolation** calcula los nuevos valores a partir de vecinos próximos, de forma más gradual que nearest neighbor. Otra opción sin pesos aprendibles es **max unpooling**: durante *max pooling* se guardan los índices de los máximos; al ampliar, cada valor se devuelve a su posición original y las posiciones restantes se rellenan con cero. Los valores descartados por *max pooling* no se recuperan. El diagrama permite seguir los índices entre la reducción y la expansión.

![[Pasted image 20260930130100.png]]

#### 3. Segmentation Architectures

##### 3.1. Fully Convolutional Networks (FCNs)

> Una **Fully Convolutional Network (FCN)** transforma una imagen en un mapa de clases sin una cabeza de clasificación global. Primero extrae características con una CNN y reduce la resolución; después, una convolución $1\times1$ genera **un canal por clase**, y una o varias convoluciones transpuestas recuperan el tamaño espacial requerido. El resultado contiene las puntuaciones de todas las clases para cada píxel de la imagen de entrada.

> También se podrían conservar las dimensiones espaciales durante toda la red mediante kernels $1\times1$ o *padding* y clasificar al final, pero operar siempre a alta resolución es costoso. La ruta de reducción y posterior ampliación comparte rasgos y abarata el cálculo. El entrenamiento emplea **cross-entropy por píxel**: en cada posición se compara la distribución predicha sobre clases con su etiqueta real y se agregan las pérdidas de la imagen.

##### 3.2. U-Net and Skip Connections

> **U-Net** es una arquitectura de segmentación con un **encoder** de convoluciones y *max pooling* que reduce la resolución y reúne contexto, y un **decoder** que la aumenta para construir el mapa de salida. Su forma de U se debe a las conexiones entre niveles correspondientes de ambas rutas. En cada nivel del decoder se **concatenan** sus mapas de activación con los del encoder a la misma escala: el decoder combina información global con detalles locales que pueden haberse perdido en la contracción.

> En el esquema, las flechas horizontales son las **skip connections**. No realizan la suma residual característica de ResNet: transfieren y concatenan características, y pueden requerir un recorte para igualar dimensiones. La variante ilustrada usa convoluciones sin relleno y produce un mapa más pequeño que la imagen de entrada; otras elecciones de *padding* o una ampliación posterior permiten ajustar el tamaño de salida. Esta combinación resulta especialmente útil para delimitar contornos y se emplea, entre otros ámbitos, en imágenes biomédicas.

![[Pasted image 20260930130101.png]]

### II. Style Transfer

#### 4. Task and Method

##### 4.1. Images, Feature Extractor, and Optimization

> **Neural style transfer** combina el **contenido** de una imagen $x^C$ con el **estilo** de otra $x^S$ para obtener una imagen sintetizada $x$. El contenido corresponde a la estructura de la escena; el estilo recoge propiedades visuales como texturas, patrones y relaciones entre respuestas de los canales de una CNN.

> Se utiliza la **misma CNN preentrenada** para extraer características de $x^C$, $x^S$ y $x$. Sus pesos permanecen **congelados**: la única variable optimizada son los **píxeles de $x$**. Suele inicializarse $x=x^C$, aunque también se puede empezar con ruido, con $x^S$ o con una mezcla de ambas imágenes. Las capas elegidas para contenido y estilo son hiperparámetros.

> En cada iteración se hace una pasada de $x$ por la red, se calcula la pérdida y se retropropaga su gradiente hasta los píxeles de $x$. Las representaciones objetivo de $x^C$ y $x^S$ pueden calcularse y guardarse antes del bucle porque no cambian. Al terminar, la salida es la propia imagen optimizada. El esquema marca dónde se comparan contenido y estilo y dónde se aplica la regularización de variación total.

![[Pasted image 20260930130102.png]]

##### 4.2. Choosing Feature Layers

> Las capas cercanas a la entrada responden mejor a **detalles locales**, como bordes y texturas; las profundas recogen más **estructura global**. Por ello, se suele escoger una o dos capas profundas para la pérdida de contenido: usar capas muy tempranas preservaría demasiados detalles exactos de $x^C$. Para la pérdida de estilo se escogen varias capas distribuidas a distintas profundidades, de modo que participen patrones locales y globales.

#### 5. Style Transfer Losses

##### 5.1. Content Loss

> Denotamos por $n_C$ el número de mapas seleccionados para contenido y por $f_r(z)$ las activaciones de la capa seleccionada $r$ para la imagen $z$. Ese mapa tiene altura $H_r$, anchura $W_r$ y $C_r$ canales. La **content loss** es el error cuadrático medio entre las activaciones de $x$ y $x^C$, promediado también entre las capas seleccionadas:

$$
\mathcal L_C
=\frac{1}{n_C}\sum_{r=1}^{n_C}\frac{1}{C_rH_rW_r}
\sum_{c=1}^{C_r}\sum_{i=1}^{H_r}\sum_{j=1}^{W_r}
\left(f_r(x)_{ijc}-f_r(x^C)_{ijc}\right)^2.
$$

> Un valor pequeño indica que la imagen sintetizada activa de forma parecida las características de contenido elegidas. La comparación se hace en los **mapas internos** de la CNN, no directamente entre colores de píxeles.

##### 5.2. Gram Matrix and Style Loss

> Para una capa de estilo $r$, se aplana cada uno de sus $C_r$ canales de tamaño $H_r\times W_r$ como una fila de la matriz $X_r\in\mathbb R^{C_r\times H_rW_r}$. La **Gram matrix** normalizada tiene tamaño $C_r\times C_r$:

$$
G_r=\frac{X_rX_r^{\mathsf T}}{C_rH_rW_r},\qquad
(G_r)_{ij}=\frac{\mathbf x_i\cdot\mathbf x_j}{C_rH_rW_r}.
$$

> Cada entrada mide cuánto se activan conjuntamente dos canales, tras sumar sobre todas las posiciones. El mapa conserva así relaciones entre patrones sin exigir que aparezcan en los mismos píxeles. La matriz es simétrica; los términos diagonales miden la magnitud de activación de cada canal. En general, esta matriz de productos escalares **no equivale** a una matriz de coeficientes de correlación o de similitudes coseno: no se centran ni se normalizan individualmente los canales.

> [!warning] Corrección
> El ejercicio de matriz de Gram pide identificar $(G_r)_{ij}$ con la similitud coseno si los vectores de canal tienen norma $1$. Con la normalización $1/(C_rH_rW_r)$ definida aquí, en ese caso $(G_r)_{ij}=\cos(\mathbf x_i,\mathbf x_j)/(C_rH_rW_r)$: son proporcionales, pero no iguales.
> Fuente de comprobación: [tutorial oficial de PyTorch sobre la matriz de Gram](https://docs.pytorch.org/tutorials/advanced/neural_style_tutorial.html) y [definición de similitud coseno de scikit-learn](https://scikit-learn.org/stable/modules/metrics.html#cosine-similarity).

> Si $G_r$ corresponde a $x$, $G_r^S$ a $x^S$ y $n_S$ es el número de capas elegidas para estilo, su diferencia cuadrática media define

$$
\mathcal L_S
=\frac{1}{n_S}\sum_{r=1}^{n_S}\frac{1}{C_r^2}
\sum_{i=1}^{C_r}\sum_{j=1}^{C_r}
\left((G_r)_{ij}-(G_r^S)_{ij}\right)^2.
$$

> Las matrices $G_r^S$ se precalculan porque la imagen de estilo es fija. El factor $1/C_r^2$ promedia las entradas de cada matriz; modificar esa normalización cambia la escala de $\mathcal L_S$ y obliga a reconsiderar su peso en la pérdida total.

##### 5.3. Total Variation Loss

> La imagen sintetizada puede presentar ruido de alta frecuencia. La **total variation loss** penaliza las diferencias absolutas entre píxeles vecinos horizontales y verticales. Para $x$ con $C$ canales y tamaño $H\times W$:

$$
\begin{aligned}
\mathcal L_V
&=\frac{1}{N}\left(
\sum_{c=1}^{C}\sum_{i=1}^{H}\sum_{j=1}^{W-1}
|x_{c,i,j+1}-x_{c,i,j}| \\
&\hspace{5em}+
\sum_{c=1}^{C}\sum_{i=1}^{H-1}\sum_{j=1}^{W}
|x_{c,i+1,j}-x_{c,i,j}|
\right),\\
N&=C\big(H(W-1)+(H-1)W\big).
\end{aligned}
$$

> $N$ cuenta todas las comparaciones y convierte la suma en una media. Al reducir cambios bruscos entre vecinos, este término favorece una imagen más suave; un peso demasiado alto también puede borrar detalles que sí interesan.

##### 5.4. Combined Objective and Weight Balance

> La función optimizada es la suma ponderada de los tres términos:

$$
\mathcal L=\alpha\mathcal L_C+\beta\mathcal L_S+\gamma\mathcal L_V.
$$

> $\alpha$ controla la conservación del contenido, $\beta$ la fuerza del estilo y $\gamma$ la supresión del ruido. Se puede imponer $\alpha+\beta+\gamma=1$ para interpretar los pesos como proporciones, aunque **no es obligatorio**. La comparación visual muestra que al aumentar el peso relativo del estilo cambian más la textura y los colores; al favorecer el contenido se conserva mejor la estructura original. En el ejemplo de optimización, la pérdida cae con rapidez al comienzo y se estabiliza gradualmente mientras la imagen sintetizada va incorporando el estilo.

![[Pasted image 20260930130103.png]]

### III. Other Vision Tasks

#### 6. Segmentation Variants

##### 6.1. Classical Image Segmentation

> La **classical image segmentation** o segmentación no supervisada agrupa píxeles en regiones por propiedades visuales de bajo nivel, como color, textura o proximidad. No necesita etiquetas semánticas: puede dividir un perro en varias regiones distintas por sus tonos, sin identificar ninguna como «perro». Su resultado son **regiones visuales**, no necesariamente objetos completos.

##### 6.2. Instance and Panoptic Segmentation

> **Instance segmentation** predice una clase y una máscara separada para cada objeto contable (*thing*). Así, dos personas de la misma clase reciben identificadores distintos. Las regiones amorfas de fondo (*stuff*), como cielo, mar o carretera, normalmente quedan fuera de la formulación de instancias. **Panoptic segmentation** combina ambas ideas: todos los píxeles reciben una clase semántica y los que pertenecen a *things* reciben además un identificador de instancia.

| Tarea | Salida para varias personas | Tratamiento de *stuff* |
| --- | --- | --- |
| **Semantic segmentation** | Una máscara de clase «persona», sin distinguir individuos. | Clase por píxel. |
| **Instance segmentation** | Una máscara e identificador por persona. | No suele asignar instancias de *stuff*. |
| **Panoptic segmentation** | Clase e identificador por persona. | Clase por píxel, sin identificador de instancia. |

> La figura muestra cómo una misma escena cambia de representación: la salida semántica etiqueta las personas con la misma clase, la salida por instancias las separa y la panóptica conserva esa separación junto a cielo, mar y suelo.

![[Pasted image 20260930130104.png]]

#### 7. Keypoint Estimation

> **Keypoint estimation** localiza puntos estructurales relevantes de un objeto, normalmente como coordenadas $(x,y)$ de la imagen. En una persona pueden ser ojos, hombros, codos, muñecas, caderas, rodillas y tobillos; en otros objetos, esquinas u otros puntos de interés. Se puede detectar primero el objeto y predecir sus puntos, y opcionalmente conectarlos para formar un esqueleto. OpenPose, HRNet y MediaPipe son ejemplos de modelos o sistemas empleados para esta tarea.

### IV. Exercises

#### 8. Proposed Exercises

> Los siguientes enunciados reúnen las actividades propuestas, sin añadir soluciones.

1. **Naive Sliding-Window Segmentation:** implementar la clasificación del píxel central de cada parche $P\times P$ de una imagen $H\times W$ y discutir el coste y su viabilidad en tiempo real.
2. **Transposed Convolution Output Shape:** establecer la fórmula general para $H_{\mathrm{out}}\times W_{\mathrm{out}}$ y calcularla para entrada $7\times7$, kernel $4\times4$, *stride* $2$ y *padding* $1$.
3. **Transposed Convolution Implementation:** implementar desde cero en Python/PyTorch la operación 2D de un canal para $s=1$ y $p=0$, sin usar `torch.nn.ConvTranspose2d`.
4. **General Transposed Convolution:** extender la implementación anterior a *stride*, *padding* y números arbitrarios de canales de entrada y salida.
5. **Bed of Nails Initialization:** demostrar paso a paso, para una entrada $M=\begin{pmatrix}a&b\\c&d\end{pmatrix}$, el resultado con *stride* $2$, *padding* $0$ y kernel $\begin{pmatrix}1&0\\0&0\end{pmatrix}$.
6. **Nearest Neighbor Initialization:** repetir la demostración con kernel $\begin{pmatrix}1&1\\1&1\end{pmatrix}$ y compararlo con nearest neighbor.
7. **Traditional Upsampling Algorithms:** implementar *bed of nails*, nearest neighbor, interpolación bilineal y max unpooling para mapas $C\times H\times W$ y tamaños objetivo adecuados.
8. **Fully Convolutional Networks:** adaptar una ResNet-18 preentrenada sustituyendo la cabeza clasificadora por proyecciones $1\times1$ a $N$ clases y añadir convoluciones transpuestas hasta recuperar $H\times W$.
9. **U-Net Architecture:** implementar encoder, decoder y concatenaciones entre niveles; analizar el efecto de las *skip connections* sobre la memoria de CPU/GPU en la pasada directa y la retropropagación.
10. **Semantic Segmentation Training:** construir un entrenamiento completo en PyTorch con un conjunto de segmentación, como PASCAL VOC, Cityscapes u Oxford-IIIT Pet, y cross-entropy por píxel.
11. **Gram Matrix:** implementar la matriz de Gram normalizada de un mapa $C_r\times H_r\times W_r$ y analizar su relación con la similitud coseno al normalizar los vectores de canal.
12. **Style Transfer Loss:** implementar por separado las pérdidas de contenido, estilo y variación total para las capas e imagen seleccionadas.
13. **Style Transfer Training:** implementar el algoritmo con VGG-19 congelada, representaciones objetivo precalculadas y una imagen $x$ inicializada como $x^C$ y optimizada con Adam durante $200$ iteraciones.
14. **Style Transfer Loss Impact:** comparar $\alpha/\beta\in\{10^{-4},10^{-2},1,10^2,10^4\}$, inicialización con ruido frente a $x^C$ y $\gamma=0$ frente a $\gamma=10^{-3}$; documentar los cambios visuales.
15. **Comparative Analysis of Vision Tasks:** comparar requisitos de entrada, representación de salida, pérdidas y aplicaciones de segmentación semántica, por instancias y panóptica, y de estimación de puntos clave.

### V. Final Summary

> **Semantic segmentation** clasifica cada píxel. Para hacerlo de forma eficiente, una FCN comparte la extracción de rasgos, reduce resolución, proyecta a un canal por clase y la recupera mediante *upsampling*; U-Net añade conexiones entre encoder y decoder para conservar detalles de los contornos. La convolución transpuesta amplía un mapa distribuyendo cada valor por un kernel, con tamaño determinado por kernel, *stride* y *padding*.

> **Style transfer** optimiza los píxeles de una imagen con una CNN preentrenada y fija. La pérdida de contenido compara activaciones profundas; la de estilo compara matrices de Gram de varias capas; la variación total reduce ruido espacial. Sus pesos equilibran estructura, estilo y suavidad. La segmentación clásica agrupa regiones visuales, la segmentación por instancias separa objetos contables, la panóptica reúne clases e instancias y la estimación de puntos clave localiza partes estructurales.
