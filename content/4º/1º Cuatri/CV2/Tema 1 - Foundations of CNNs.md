---
estado: pendiente de revisión
---

### I. Computer Vision Concepts

#### 1. Context and Convolutional Networks

##### 1.1. From Handcrafted Features to Learned Representations

> La visión artificial clásica dependía de descriptores diseñados a mano, como **SIFT** y **HOG**. Funcionaban en escenarios controlados, pero podían fallar ante cambios de iluminación, deformaciones, oclusiones y fondos complejos. Las **Convolutional Neural Networks (CNNs)** aprenden los extractores de rasgos directamente de los píxeles mediante entrenamiento de extremo a extremo. El avance de las GPU y la disponibilidad de conjuntos grandes y etiquetados, como ImageNet, impulsaron este cambio.

> Una CNN transforma gradualmente patrones locales, como bordes y texturas, en representaciones que permiten reconocer partes y objetos. Esa capacidad sustenta aplicaciones como la percepción de vehículos, el análisis de imágenes médicas y los modelos visuales multimodales.

##### 1.2. Convolutional Operation

> Una capa convolucional desplaza un **kernel** por la entrada. En cada posición multiplica los valores de una ventana local por los pesos del filtro, suma los productos de todos los canales de entrada y añade un sesgo. Cada filtro produce un canal de salida o *feature map*. Aunque se hable de «convolución», la operación usada habitualmente es una **correlación cruzada**: el kernel no se invierte espacialmente. Al aprenderse sus pesos, esta convención no reduce la capacidad expresiva de la capa.

> Sean $X\in\mathbb{R}^{C_{\mathrm{in}}\times H\times W}$, su versión con $p$ ceros a cada lado $\tilde X\in\mathbb{R}^{C_{\mathrm{in}}\times(H+2p)\times(W+2p)}$, los filtros $K\in\mathbb{R}^{C_{\mathrm{out}}\times C_{\mathrm{in}}\times k\times k}$ y un sesgo $b_c$ por canal de salida. La salida tiene forma $Y\in\mathbb{R}^{C_{\mathrm{out}}\times H'\times W'}$. Con los índices espaciales desde cero, **stride** $s$ y **dilation** $d$, su valor en el canal $c$ y la posición $(i,j)$ es:

$$
Y_{c,i,j}=b_c+\sum_{\ell=1}^{C_{\mathrm{in}}}\sum_{m=0}^{k-1}\sum_{n=0}^{k-1}
\tilde X_{\ell,\,is+md,\,js+nd}\,K_{c,\ell,m,n}.
$$

> [!warning] Corrección
> En el material, los sumatorios espaciales van de $1$ a $k$, pero las posiciones de entrada se escriben $is+md$ y $js+nd$; con $d>1$ esto desplaza indebidamente la primera muestra. Con índices espaciales desde cero, los sumatorios correctos van de $0$ a $k-1$, como en la expresión anterior.
> Fuente de comprobación: [Documentación oficial de TensorFlow sobre convolución](https://www.tensorflow.org/api_docs/python/tf/nn/convolution).

> El esquema muestra qué píxeles de una ventana contribuyen a un valor de salida. Por ejemplo, para la esquina superior izquierda se multiplican los nueve valores destacados por el kernel $3\times3$ y se suma el sesgo.

![[Pasted image 20260930105700.png]]

> En el ejemplo multicanal, $X$ tiene forma $(2,3,3)$, hay tres filtros de forma $(2,2,2)$, $b=(1,-1,0)$ y se usa $s=1$, $p=0$, $d=1$. Por tanto, $Y$ tiene forma $(3,2,2)$. Los datos son:

$$
X_1=\begin{bmatrix}1&0&2\\0&1&1\\2&1&0\end{bmatrix},
\qquad
X_2=\begin{bmatrix}0&2&1\\1&0&1\\0&1&2\end{bmatrix}.
$$

$$
\begin{aligned}
K_{1,1}&=\begin{bmatrix}1&0\\-1&1\end{bmatrix},&
K_{1,2}&=\begin{bmatrix}0&2\\1&0\end{bmatrix},\\
K_{2,1}&=\begin{bmatrix}2&1\\0&-1\end{bmatrix},&
K_{2,2}&=\begin{bmatrix}1&0\\0&1\end{bmatrix},\\
K_{3,1}&=\begin{bmatrix}0&1\\1&0\end{bmatrix},&
K_{3,2}&=\begin{bmatrix}-1&0\\0&2\end{bmatrix}.
\end{aligned}
$$

> El primer valor del primer mapa suma las dos ventanas y el sesgo: $Y_{1,0,0}=1+(1\cdot1+0\cdot0+0\cdot(-1)+1\cdot1)+(0\cdot0+2\cdot2+1\cdot1+0\cdot0)=8$. Repitiendo la operación en cada posición y para cada filtro:

$$
Y_1=\begin{bmatrix}8&3\\0&4\end{bmatrix},\qquad
Y_2=\begin{bmatrix}0&3\\1&4\end{bmatrix},\qquad
Y_3=\begin{bmatrix}0&3\\4&6\end{bmatrix}.
$$

##### 1.3. Padding, Stride and Dilation

> El **padding** $p$ añade ceros alrededor de la imagen y permite calcular salidas cerca del borde. El **stride** $s$ determina cuánto avanza el kernel entre posiciones: un valor mayor reduce la resolución espacial de la salida. La **dilation** $d$ separa los elementos del kernel, amplía la región observada y no añade pesos. Para un kernel $k\times k$, su lado efectivo es $k_{\mathrm{eff}}=d(k-1)+1$.

> Con los mismos valores en ambas dimensiones, el número de posiciones válidas del kernel determina la forma espacial de $Y$:

$$
H'=\left\lfloor\frac{H+2p-d(k-1)-1}{s}\right\rfloor+1,
\qquad
W'=\left\lfloor\frac{W+2p-d(k-1)-1}{s}\right\rfloor+1.
$$

> Así, $p$ controla cuánta información de borde puede conservarse, $s$ controla el muestreo espacial y $d$ controla el alcance del filtro. La fórmula presupone padding simétrico y un kernel cuadrado.

##### 1.4. Structural Properties

> La convolución aprovecha tres propiedades de las imágenes:

- **Local connectivity:** cada activación depende de una vecindad pequeña, donde los píxeles próximos suelen estar relacionados.
- **Parameter sharing:** el mismo filtro se aplica en todas las posiciones. Puede detectar un patrón donde aparezca y usa muchos menos pesos que conectar cada salida con toda la imagen.
- **Translation equivariance:** para una convolución de stride unitario, ignorando los bordes, desplazar la entrada desplaza del mismo modo su mapa de rasgos: $\operatorname{Conv}(T_\Delta X)=T_\Delta\operatorname{Conv}(X)$. El patrón detectado se conserva y cambia su posición.

> **Equivarianza** no significa que la salida sea idéntica tras trasladar la imagen: significa que se traslada con ella. Operaciones posteriores, como *pooling*, pueden reducir la sensibilidad de la predicción final a pequeños desplazamientos.

#### 2. Features and Receptive Field

##### 2.1. Features along the Network

> Las primeras capas detectan bordes, esquinas, colores y texturas. Las capas intermedias combinan esos rasgos en curvas, formas y partes de objetos. Las profundas integran regiones más amplias y forman representaciones semánticas de objetos o clases. A medida que aumenta la abstracción, disminuye la facilidad para interpretar visualmente cada activación.

> La figura ilustra esa progresión con rasgos de bajo nivel, partes faciales y estructuras faciales completas.

![[Pasted image 20260930105701.png]]

##### 2.2. Receptive Field

> El **receptive field** teórico de una activación es la región de la imagen de entrada que puede influir en ella. Si todas las convoluciones tienen $s_i=1$ y $d_i=1$, cada capa de kernel $k_i$ aumenta el lado del campo receptivo en $k_i-1$. Contando desde la entrada con $RF_0=1$:

$$
RF_L=RF_{L-1}+(k_L-1)
=1+\sum_{i=1}^{L}(k_i-1).
$$

> Para $L$ convoluciones con un mismo tamaño $k$, $RF_L=1+L(k-1)$. Dos capas $3\times3$ consecutivas dan $RF_1=3$ y $RF_2=5$: una unidad de la segunda salida depende de una región $3\times3$ de la capa anterior; la unión de esas ventanas solapadas cubre $5\times5$ píxeles de la entrada.

> En la figura, «Layer 1» es la propia entrada, «Layer 2» es la primera salida y «Layer 3» la segunda. Las regiones coloreadas permiten seguir hacia atrás la contribución de cada capa.

![[Pasted image 20260930105702.png]]

> El campo receptivo crece junto con la complejidad de los rasgos: las capas superficiales ven detalles locales; las intermedias, partes; las profundas, un contexto más amplio. El **receptive field** efectivo es la parte que más influye realmente en una red entrenada y puede ser menor que el teórico.

#### 3. Data Augmentation

##### 3.1. Rationale and Basic Transformations

> **Data augmentation** genera durante el entrenamiento variantes de una muestra para reducir la memorización de píxeles concretos y mejorar la generalización. Las transformaciones deben respetar la semántica de la tarea: un recorte, giro o cambio de iluminación solo conserva la etiqueta cuando no elimina ni altera lo que se quiere reconocer. Al muestrear variantes aleatorias en cada época, la red ve más configuraciones sin recopilar nuevas imágenes.

- **Geometric transformations:** recorte y cambio de escala, reflejos, rotaciones y transformaciones afines; cambian la posición de los píxeles y favorecen robustez ante variaciones espaciales.
- **Photometric transformations:** cambios de brillo, contraste, saturación o tono, conversión a gris cuando sea apropiada, ruido gaussiano y desenfoque; modifican intensidades sin cambiar las coordenadas.

> Una transformación afín puede escribirse con coordenadas homogéneas. Los parámetros $a,b,c,d,e,f$ combinan cambios lineales y traslación:

$$
\begin{bmatrix}x'\\y'\\1\end{bmatrix}
=
\begin{bmatrix}a&b&c\\d&e&f\\0&0&1\end{bmatrix}
\begin{bmatrix}x\\y\\1\end{bmatrix}.
$$

> El ruido gaussiano añade una perturbación $\varepsilon\sim\mathcal N(0,\sigma^2)$; el desenfoque gaussiano atenúa detalles de alta frecuencia. Ambas técnicas evitan depender demasiado de particularidades del sensor.

##### 3.2. Occlusion and Sample Mixing

> **Cutout** o **Random Erasing** oculta una región rectangular para que el modelo no dependa de una única pista local. **Mixup** mezcla dos imágenes y también sus etiquetas con $\lambda\sim\operatorname{Beta}(\alpha,\alpha)$:

$$
\tilde x=\lambda x_i+(1-\lambda)x_j,
\qquad
\tilde y=\lambda y_i+(1-\lambda)y_j.
$$

> **CutMix** sustituye una región de $x_i$ por píxeles de $x_j$ mediante una máscara binaria $M$. La proporción $\lambda$ de píxeles conservados de $x_i$ determina la mezcla de etiquetas:

$$
\tilde x=M\odot x_i+(1-M)\odot x_j,
\qquad
\tilde y=\lambda y_i+(1-\lambda)y_j.
$$

> Estas técnicas obligan a aprovechar más contexto visual. Mixup, en particular, suaviza la transición entre clases; el aumento de datos en conjunto favorece representaciones menos sensibles a variaciones irrelevantes de la entrada.

### II. Computer Vision Architectures

#### 4. Standard CNN Baseline

> La arquitectura básica alterna **convolution**, **ReLU** y **pooling** para extraer rasgos y reducir la resolución. Después aplica **flatten** a los mapas finales y un **Multi-Layer Perceptron (MLP)** de capas **fully connected (FC)** para clasificar: $\text{CNN/ReLU/Pooling}\rightarrow\text{Flatten}\rightarrow\text{MLP}$. Es fácil de interpretar, pero el vector aplanado puede hacer muy grandes las capas densas; aumentar la profundidad también complica la optimización.

#### 5. AlexNet (2012)

> **AlexNet** impulsó el aprendizaje profundo en visión tras su resultado en ImageNet 2012. Encadena cinco capas convolucionales y tres FC. En el esquema, comienza con una convolución $11\times11$ de stride $4$, sigue con una $5\times5$ y tres $3\times3$, intercala *max pooling* y termina con dos capas FC de 4096 unidades antes de clasificar. Popularizó **ReLU** para acelerar la convergencia y mitigar la desaparición del gradiente frente a activaciones saturantes, **dropout** en las capas densas para reducir el sobreajuste, el entrenamiento paralelo en GPU y el aumento de datos mediante recortes, cambios de escala y reflejos.

#### 6. VGGNet (2014)

> **VGGNet** usa bloques homogéneos de convoluciones $3\times3$ con stride $1$, ReLU y *max pooling*. Sus variantes VGG-16 y VGG-19 tienen 16 y 19 capas con pesos; el esquema aumenta progresivamente los canales de 64 a 128, 256 y 512 mientras el *pooling* reduce la resolución. Dos convoluciones $3\times3$ apiladas alcanzan un campo receptivo de $5\times5$ con menos parámetros que una sola $5\times5$ para el mismo número de canales, e introducen una no linealidad adicional. La repetición de bloques simplifica el diseño y facilita reutilizar la red como extractor.

#### 7. GoogLeNet / Inception v1 (2014)

##### 7.1. Inception Modules and Bottlenecks

> **GoogLeNet** combina operaciones paralelas dentro de cada **Inception module**: convoluciones $1\times1$, $3\times3$ y $5\times5$, junto con *max pooling*. Concatena los resultados por canales para captar patrones a varias escalas. La red encadena estos módulos en lugar de limitarse a una única secuencia de filtros del mismo tamaño.

> Las convoluciones $1\times1$ reducen el número de canales antes de las ramas $3\times3$ y $5\times5$, que son más costosas; otra proyección puede seguir al *pooling*. El esquema compara el módulo directo con el que incorpora estas reducciones.

![[Pasted image 20260930105703.png]]

##### 7.2. Global Average Pooling and Auxiliary Classifiers

> Al final, **Global Average Pooling (GAP)** resume cada mapa espacial en un escalar y reduce la necesidad de grandes capas FC. Durante el entrenamiento, dos **auxiliary classifiers** intermedios aportan pérdidas adicionales y una vía más corta para el gradiente. En el esquema mostrado, la pérdida total es $\mathcal L=\mathcal L_F+0.3\mathcal L_1+0.3\mathcal L_2$, donde $\mathcal L_F$ corresponde a la salida principal. Las ramas auxiliares se descartan en inferencia.

#### 8. ResNet (2015)

> Al añadir capas a una red ya profunda puede aumentar incluso el error de **entrenamiento**: es el problema de degradación. **ResNet** facilita aprender una corrección sobre la entrada de cada bloque mediante una **residual connection**. Si la transformación deseada es $H(x)$, se aprende $F(x)=H(x)-x$ y la salida queda $y=F(x)+x$.

> El diagrama muestra la rama de capas con pesos y el camino de identidad que se suma a su salida.

![[Pasted image 20260930105704.png]]

> Para el caso escalar, la regla de la cadena hace explícita la vía directa del gradiente:

$$
\frac{\partial\mathcal L}{\partial x}
=\frac{\partial\mathcal L}{\partial y}\frac{\partial y}{\partial x}
=\frac{\partial\mathcal L}{\partial y}
\left(\frac{\partial F(x)}{\partial x}+1\right)
=\frac{\partial\mathcal L}{\partial y}
+\frac{\partial\mathcal L}{\partial y}\frac{\partial F(x)}{\partial x}.
$$

> El término $+1$ permite que parte de la señal retroceda aun cuando la derivada de $F$ sea pequeña. Si el bloque añadido no resulta útil, puede aproximar $F(x)=0$ y conservar la identidad. Este diseño hizo posible entrenar redes mucho más profundas, como variantes de 101 y 152 capas.

#### 9. DenseNet (2017)

> **DenseNet** conecta cada capa de un bloque con todas las anteriores mediante **concatenación** de mapas de rasgos. Así, las capas profundas reutilizan directamente rasgos de bajo nivel y solo necesitan añadir un número pequeño de mapas nuevos; ese número lo controla el **growth rate**. La concatenación conserva los mapas previos como canales separados.

> La figura presenta la red como sucesión de bloques densos y **transition layers**, que combinan convolución y *pooling* entre bloques. También amplía un bloque para mostrar las conexiones desde las salidas anteriores hacia las capas posteriores.

![[Pasted image 20260930105705.png]]

> Esta reutilización favorece el flujo de información y la eficiencia en parámetros. Frente a la suma residual $F(x)+x$ de ResNet, aquí las características anteriores se acumulan por canales para que cada capa pueda acceder a ellas.

### III. Transfer Learning

#### 10. Transferring Knowledge

> **Transfer learning** reutiliza pesos aprendidos en una tarea de origen para comenzar otra tarea relacionada. Un modelo preentrenado con muchos datos puede aportar detectores visuales útiles cuando el conjunto objetivo es pequeño o entrenar desde cero sería costoso. Se conserva su **backbone** como extractor y se adapta la salida al número de clases del nuevo problema.

> Hay dos formas principales de aprovecharlo. Como **fixed feature extractor**, se congelan los pesos del backbone y se entrena un nuevo clasificador sobre sus rasgos. En **fine-tuning**, se sustituye la cabeza de clasificación y se siguen ajustando algunas capas o toda la red, normalmente empezando por la cabeza. La elección depende de la cantidad de datos y de la semejanza entre los dominios.

#### 11. Fine-Tuning Selection Guide

| Datos objetivo | Dominio similar al preentrenamiento | Dominio diferente al preentrenamiento |
|---|---|---|
| Muchos | Entrenar primero la nueva cabeza y, si los recursos lo permiten, descongelar progresivamente más capas. | Ajustar todas las capas; si la distancia entre dominios es grande y hay datos y cómputo suficientes, considerar entrenamiento desde cero o pesos de un dominio más próximo. |
| Pocos | Congelar el backbone y entrenar un clasificador final, interno o externo, sobre sus rasgos. | Explorar rasgos de capas intermedias con el backbone congelado y valorar otro modelo o una estrategia de *few-shot learning*. |

> Esta tabla es una **heurística de partida**, no una garantía de rendimiento. En todos los casos, la cabeza nueva debe tener tantas salidas como clases objetivo; después se decide qué pesos preentrenados conservar fijos y cuáles actualizar.

### IV. Exercises

#### 12. Proposed Exercises

> Los siguientes enunciados sirven para practicar el tema. Se mantienen sin soluciones añadidas.

1. **Computer vision architectures:** elaborar una tabla de las arquitecturas estudiadas con su año, innovaciones y estructura principal.
2. **Fine-tuning:** adaptar una ResNet-18 preentrenada en PyTorch a MNIST: entrada de un canal y $28\times28$ píxeles, diez clases, capa de entrada y cabeza nuevas; considerar ampliar la imagen para evitar una reducción espacial excesiva.
3. **Convolutional arithmetic:** calcular la forma de salida para $(C_{\mathrm{in}},H,W)=(3,224,224)$, 64 filtros $7\times7$, $s=2$, $p=3$ y $d=1$.
4. **Gradient flow in ResNets:** explicar mediante $\partial\mathcal L/\partial x$ la contribución del término $+1$ de una conexión residual.
5. **Receptive field:** para cinco convoluciones $3\times3$, con $s=d=1$, desarrollar $RF_5$ capa a capa y dibujar su expansión hacia la entrada.
6. **Transfer learning strategy:** elegir una estrategia para 400 radiografías etiquetadas de una enfermedad ósea rara a partir de pesos preentrenados en ImageNet.
7. **Data augmentation:** definir en PyTorch, con `torchvision.transforms`, recorte aleatorio, reflejo horizontal y cambios aleatorios de color; visualizar imagen original y transformada.
8. **Feature extraction:** cargar `vgg16` preentrenada en PyTorch, congelar sus parámetros convolucionales y sustituir la última capa FC para obtener diez clases.

### V. Final Summary

> Las CNN explotan vecindades locales y filtros compartidos para construir rasgos jerárquicos. **Padding**, **stride** y **dilation** determinan el tamaño de los mapas y la región observada; el campo receptivo explica cómo las capas profundas reúnen contexto. **Data augmentation** reduce la dependencia de ejemplos concretos siempre que las transformaciones respeten la tarea.

> AlexNet y VGGNet profundizan el esquema convolución–clasificador; GoogLeNet procesa varias escalas con módulos Inception; ResNet usa sumas residuales para optimizar redes profundas; DenseNet concatena rasgos para reutilizarlos. Con **transfer learning**, un backbone preentrenado puede mantenerse fijo o ajustarse según el volumen de datos y la similitud del nuevo dominio.
