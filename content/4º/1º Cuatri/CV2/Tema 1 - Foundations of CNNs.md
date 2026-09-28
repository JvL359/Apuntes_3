---
estado: pendiente de revisión
---

### I. Computer Vision Concepts

#### 1. Convolution and feature maps

> Una **convolutional neural network** (CNN) transforma una imagen mediante filtros o *kernels* que se aplican localmente sobre sus píxeles. En cada posición, se realiza una suma ponderada entre la región de entrada y los pesos del kernel, se añade un sesgo y se obtiene un valor de salida. Cada kernel produce un **feature map** distinto, por lo que una misma imagen genera múltiples representaciones.

> En la práctica de las CNN se emplea normalmente **cross-correlation**, es decir, el kernel no se invierte antes de desplazarlo. Por ejemplo, para la región

$$
\begin{bmatrix}1&2&3\\5&6&7\\9&10&11\end{bmatrix}
$$

> y el kernel

$$
\begin{bmatrix}0&-1&0\\-1&5&-1\\0&-1&0\end{bmatrix}
$$

> con sesgo $5$, el primer valor de salida es

$$
1\cdot0+5\cdot(-1)+9\cdot0+2\cdot(-1)+6\cdot5+10\cdot(-1)+3\cdot0+7\cdot(-1)+11\cdot0+5=11
$$

> Así, los filtros pueden responder a patrones visuales distintos, como bordes, texturas u otras estructuras de la imagen.

#### 2. Padding, stride and dilation

> **Padding** añade valores, habitualmente ceros, alrededor de la imagen antes de aplicar el kernel. Permite que las regiones de borde participen en la convolución y controla el tamaño espacial de la salida. En el ejemplo mostrado, una entrada $6\times6$ recibe padding y pasa a $8\times8$; un kernel $3\times3$ produce entonces una salida $6\times6$.

> El **stride** es el desplazamiento del kernel entre dos posiciones consecutivas. Con `stride = 1` el filtro se mueve una celda y genera más posiciones de salida; con `stride = 2` avanza dos celdas y reduce la resolución espacial del feature map.

> La **dilation** separa las posiciones del kernel sobre la entrada. De este modo, un filtro observa una región más amplia sin aumentar el número de pesos del kernel, lo que amplía su campo de visión.

#### 3. Local connectivity and parameter sharing

> Una neurona convolucional se conecta solo a una región local de la entrada, no a todos sus píxeles. Esta **local connectivity** aprovecha que los patrones visuales cercanos están relacionados.

> Además, los mismos pesos de un kernel se aplican en todas las posiciones espaciales: esto es **parameter sharing**. El resultado es la **translation equivariance**: si un patrón se desplaza en la imagen, la respuesta del feature map se desplaza de forma correspondiente. Compartir parámetros reduce drásticamente el número de parámetros frente a una capa totalmente conectada.

#### 4. Receptive field and hierarchical features

> El **receptive field** de una activación es la región de la entrada original que puede influir en ella. Los receptive fields aumentan a medida que se apilan capas: si la capa 3 ve una región $3\times3$ de la capa 2 y esta ve una región $3\times3$ de la capa 1, una activación de la capa 3 ve una región $5\times5$ de la capa 1.

> Esta acumulación permite aprender características jerárquicas:

- Las capas iniciales detectan características de bajo nivel, como bordes y puntos oscuros.
- Las capas intermedias combinan esos patrones en partes, como ojos, orejas o nariz.
- Las capas profundas representan estructuras de alto nivel, como la estructura facial.

#### 5. Data augmentation

> **Data augmentation** crea entradas distintas a partir de un ejemplo manteniendo su misma etiqueta. Al aumentar la variedad efectiva de los datos, reduce el sobreajuste y mejora la capacidad de generalización.

### II. Computer Vision Architectures

#### 1. Standard CNN baseline

> Una CNN estándar sigue el flujo `CNN / ReLU / Pooling → Flatten → MLP`. Es una arquitectura simple e intuitiva, pero aumentar su profundidad puede provocar una explosión del número de parámetros, especialmente al aplanar las representaciones antes de la parte totalmente conectada.

#### 2. AlexNet and VGGNet

> **AlexNet** incorporó activaciones **ReLU** para acelerar la convergencia y **dropout** para reducir el sobreajuste.

> **VGGNet** utiliza filtros convolucionales pequeños de $3\times3$ y construye redes profundas; VGG-19 alcanza 19 capas. La repetición de filtros pequeños permite incrementar la profundidad manteniendo una estructura regular.

#### 3. GoogLeNet

> **GoogLeNet** busca eficiencia de parámetros mediante convoluciones $1\times1$ para reducir dimensionalidad y mediante el **Inception module**. Un módulo Inception procesa la misma entrada en ramas paralelas —convoluciones de distintos tamaños y *max pooling*— y concatena sus salidas en profundidad.

> La arquitectura incluye **auxiliary classifiers** en puntos intermedios, además del clasificador final. Estos clasificadores auxiliares acompañan al entrenamiento de una red profunda, mientras que los módulos Inception combinan información a distintas escalas espaciales.

#### 4. ResNet and DenseNet

> **ResNet** emplea **residual connections**, que permiten construir arquitecturas muy profundas. La conexión residual proporciona una ruta directa que suma o transporta información entre capas.

> **DenseNet** utiliza **dense connectivity**: las capas se conectan densamente, reutilizando representaciones previas. Esta conectividad busca eficiencia de parámetros.

### III. Transfer Learning

#### 1. Transferring knowledge

> **Transfer learning** parte de un modelo ya entrenado en vez de entrenar uno desde cero. El modelo preentrenado aporta representaciones aprendidas en el conjunto de datos de origen que pueden reutilizarse para una tarea o conjunto de datos objetivo.

#### 2. Fine-tuning and feature extraction

> En **fine-tuning**, se copia la arquitectura del modelo fuente al modelo objetivo y se reutilizan los pesos preentrenados. Las capas pueden mantenerse congeladas o ajustarse sobre el conjunto objetivo. Frente a la inicialización aleatoria y el entrenamiento desde cero, se aprovecha el conocimiento previo.

> Como **feature extractor**, el backbone preentrenado se congela y transforma la entrada en una nueva representación. Sobre ella se entrena únicamente un modelo nuevo —por ejemplo, un clasificador lineal, una regresión lineal o una red neuronal— que produce la salida y optimiza la pérdida.

#### 3. Choosing a transfer strategy

| Target dataset | Similar to the source dataset | Different from the source dataset |
| --- | --- | --- |
| **A lot of data** | Fine-tune some or all model layers. | Fine-tune all model layers or train from scratch. |
| **Little data** | Use a linear classifier on the final layer or use the backbone as a feature extractor. | Unfavorable scenario: extract features from intermediate layers or use another model or strategy. |

### IV. Final Summary

> CNNs use local convolutions, parameter sharing and increasing receptive fields to transform pixels into hierarchical visual features. Padding, stride and dilation control how the kernel samples the input, while data augmentation improves generalization.

> Standard CNNs motivated increasingly deep and efficient architectures: AlexNet, VGGNet, GoogLeNet, ResNet and DenseNet each address convergence, depth, multi-scale processing or parameter efficiency differently. Transfer learning reuses pretrained knowledge through fine-tuning or frozen feature extraction, with the appropriate choice determined by the similarity and size of the target dataset.
