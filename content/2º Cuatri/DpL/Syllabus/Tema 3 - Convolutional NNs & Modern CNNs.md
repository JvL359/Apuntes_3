## D2DpL 7. Convolutional Neural Networks
### I. Introducción Previa
#### 1. Problema: Tratar Imágenes Como Vectores “Aplana” su Estructura
> Las imágenes son una **rejilla 2D de píxeles** (y, en color, con varios valores por píxel). En capítulos anteriores, se **ignoró** esta estructura espacial al **aplanar** la imagen y pasarla por un MLP totalmente conectado, lo que hace que el modelo sea **invariante al orden** de las features (podrías permutar píxeles y el MLP “no lo sabe”).  
> La motivación del capítulo: usar el conocimiento previo de que **píxeles cercanos suelen estar relacionados** para construir modelos más eficientes. (Material: inicio del Cap. 7)
#### 2. Qué Aporta una CNN y Por Qué es Relevante
> El capítulo introduce las **Convolutional Neural Networks (CNNs)** como familia diseñada para explotar la estructura espacial de imágenes; se resaltan dos ventajas prácticas:
> - **Eficiencia estadística** (menos parámetros que una fully-connected comparable).
> - **Eficiencia computacional** (convoluciones fáciles de paralelizar en GPU).  
>     También se menciona que CNNs se usan ampliamente en visión y se han adaptado a secuencias 1D (audio, texto, series temporales) y otros dominios (p. ej., grafos). (Material: inicio del Cap. 7)
#### 3. Mapa del Capítulo (Estructura “Tipo Índice”)
> El capítulo sigue este recorrido:
> - **7.1**: motivación y derivación “desde principios” (invariancia por traslación y localidad) hasta llegar a convoluciones.
> - **7.2**: operación práctica en imágenes (correlación cruzada “llamada” convolución), tamaño de salida, capas conv, ejemplo de detección de bordes y conceptos de **feature map** y **receptive field**.
> - **7.3**: control del tamaño con **padding** y **stride**.
> - **7.4**: **múltiples canales** (entrada/salida) y **convolución 1×1**.
> - **7.5**: **pooling** para agregación y reducción espacial.
> - **7.6**: ejemplo completo con **LeNet** y entrenamiento en Fashion-MNIST. (Material: inicio del Cap. 7)

### II. 7.1 de Capas Totalmente Conectadas a Convoluciones
#### 1. Motivación: Datos Tabulares vs Datos Perceptuales de Alta Dimensión
> El material distingue **datos tabulares** (filas=ejemplos, columnas=features sin estructura a priori) de datos perceptuales (imágenes), donde un MLP “sin estructura” se vuelve **inviable** por número de parámetros.  
> Ejemplo del texto: una foto de **1 megapíxel** (10⁶ entradas). Incluso reduciendo agresivamente a **1000** unidades ocultas, una sola capa fully-connected tendría **10⁹ parámetros** (10⁶×10³), haciendo el aprendizaje impracticable en cómputo/datos. (Material: 7.1)
#### 2. Invariancia y Localidad: Requisitos de Diseño para Visión
> Se proponen desiderata (con el ejemplo tipo “Where’s Waldo”):
> 1. **Translation invariance / equivariance**: detectar el mismo patrón aunque aparezca en otra posición.
> 2. **Locality**: las primeras capas deben fijarse en **regiones locales**, no en píxeles lejanos.
> 3. Capas más profundas deben capturar **dependencias de mayor alcance** agregando información progresivamente. (Material: 7.1.1)
#### 3. Restringir un MLP Hasta Llegar a una Convolución
> Se parte de entradas 2D **X** y representaciones ocultas 2D **H** (misma forma). Una fully-connected “2D” usa un tensor de pesos de 4º orden:  
> [  
> [H]_{i,j} = [U]_{i,j} + \sum_k \sum_l [W]_{i,j,k,l} [X]_{k,l}  
> = [U]_{i,j} + \sum_a \sum_b [V]_{i,j,a,b}[X]_{i+a, j+b}.  
> ]  
> **Problema**: para imagen 1000×1000 → H 1000×1000, esto exigiría ~10¹² parámetros.
> 
> - **Translation invariance** fuerza que los parámetros no dependan de (i,j): ([V]_{i,j,a,b}=[V]_{a,b}) y el sesgo sea constante (u). Entonces:  
>     [  
>     [H]_{i,j} = u + \sum_a \sum_b [V]_{a,b}[X]_{i+a, j+b}.  
>     ]
> - **Locality** fuerza ([V]_{a,b}=0) fuera de un rango (|a|>\Delta) o (|b|>\Delta), quedando:  
>     [  
>     [H]_{i,j} = u + \sum_{a=-\Delta}^{\Delta} \sum_{b=-\Delta}^{\Delta} [V]_{a,b}[X]_{i+a, j+b}.  
>     ]  
>     Resultado: pasas de millones/billones de parámetros a **~4\Delta^2** (con (\Delta) típicamente < 10), imponiendo sesgo inductivo (localidad + traslación). (Material: 7.1.2)
#### 4. Convolución Matemática vs Operación Usada en Redes
> Se recuerda la definición matemática de convolución:  
> [  
> (f * g)(x)=\int f(z)g(x-z),dz  
> ]  
> y su versión discreta (1D y 2D):  
> [  
> (f_g)(i)=\sum_a f(a)g(i-a), \quad (f_g)(i,j)=\sum_a\sum_b f(a,b)g(i-a,j-b).  
> ]  
> Comparando con la ecuación anterior, el material señala que lo presentado como “convolución” en (7.1.3) se parece más a una **cross-correlation** por el uso de ((i+a, j+b)) frente a ((i-a, j-b)), diferencia considerada principalmente notacional para redes (se retoma en 7.2). (Material: 7.1.3)
#### 5. Canales: de Imágenes RGB a Tensores 3D
> Una imagen RGB no es 2D sino un tensor 3D (alto×ancho×canal). Se indexa ( [X]_{i,j,k} ).  
> Para soportar múltiples canales en entrada y salida, el kernel se extiende a ( [V]_{a,b,c,d} ), y:  
> [  
> [H]_{i,j,d}=\sum_{a=-\Delta}^{\Delta}\sum_{b=-\Delta}^{\Delta}\sum_c [V]_{a,b,c,d}[X]_{i+a,j+b,c}.  
> ]  
> Aquí **d** recorre los canales de salida (feature maps). (Material: 7.1.4)
#### 6. Resumen y Ejercicios
> Resumen del material: CNNs se derivan imponiendo **translation invariance** + **locality**, reduciendo drásticamente complejidad; los **canales** recuperan expresividad; se mencionan antecedentes tempranos (p. ej., Neocognitron).  
> Ejercicios (muestra): (\Delta=0) como MLP por píxel/canales; cuestiones sobre audio/texto; efectos de bordes; simetría de la convolución. (Material: 7.1.5–7.1.6)

### III. 7.2 Convoluciones para Imágenes
#### 1. Operación Central: Cross-Correlation 2D
> Se aclara que las “convolutional layers” en DL implementan **cross-correlation**: deslizar una ventana (kernel) sobre la entrada, multiplicar elemento a elemento y sumar para producir cada escalar de salida.  
> Ejemplo numérico (Fig. 7.2.1): para entrada 3×3 y kernel 2×2, la salida es 2×2 con valores calculados como sumas de productos. (Material: 7.2.1)
#### 2. Tamaño de Salida sin Padding
> Si la entrada es (n_h \times n_w) y el kernel (k_h \times k_w), la salida (sin padding) es:  
> [  
> (n_h-k_h+1)\times(n_w-k_w+1).  
> ]  
> Se anticipa que el **padding** permitirá mantener tamaños. (Material: 7.2.1)
```python
def corr2d(X, K): #@save
    """Compute 2D cross-correlation."""
    h, w = K.shape
    Y = torch.zeros((X.shape[0] - h + 1, X.shape[1] - w + 1))
    for i in range(Y.shape[0]):
        for j in range(Y.shape[1]):
            Y[i, j] = (X[i:i + h, j:j + w] * K).sum()
    return Y
```
#### 3. Capa Convolucional 2D: Parámetros y Forward
> Una capa conv (según el ejemplo del texto) usa como parámetros:
> - **kernel** (pesos)
> - **bias escalar**  
>     y define el forward como cross-correlation + bias. (Material: 7.2.2)
```python
class Conv2D(nn.Module):
    def __init__(self, kernel_size):
        super().__init__()
        self.weight = nn.Parameter(torch.rand(kernel_size))
        self.bias = nn.Parameter(torch.zeros(1))

    def forward(self, x):
        return corr2d(x, self.weight) + self.bias
```
#### 4. Ejemplo: Detección de Bordes y Aprender un Kernel
> Se construye una “imagen” binaria (6×8) con una franja negra central. Con el kernel (K=[1,-1]) (1×2) la salida detecta bordes horizontales: **+1** en transición blanco→negro y **−1** en negro→blanco.  
> Luego se muestra que, inicializando un `nn.LazyConv2d` (sin bias) y minimizando error cuadrático, el kernel se **aprende** a partir de pares (X,Y), convergiendo cerca de ([1,-1]). (Material: 7.2.3–7.2.4)
#### 5. Convolución vs Cross-Correlation en DL
> Si se quisiera “convolución estricta” (matemática), basta con **voltear** el kernel horizontal y verticalmente y hacer cross-correlation.  
> Punto clave: como los kernels se **aprenden**, el resultado del modelo es equivalente (cambia el kernel aprendido por el kernel volteado), por lo que el texto mantiene la terminología estándar llamándolo “convolution”. (Material: 7.2.5)
#### 6. Feature Map y Receptive Field
> - La salida de una conv se denomina a veces **feature map**.
>     
> - **Receptive field** de un elemento (x) en una capa: todos los elementos de capas previas que pueden afectarlo en forward. Puede ser mayor que el kernel individual cuando apilas capas (más profundidad → receptive field efectivo mayor). (Material: 7.2.6)
#### 7. Resumen y Ejercicios
> Resumen: la operación es local y optimizable en hardware; con múltiples canales se generaliza a operaciones “tipo matriz-matriz” entre canales; esta localidad facilita acelerar cómputo y ha sido clave para resultados modernos en visión.  
> Ejercicios (muestra): diseñar kernels (derivadas, blur), gradientes en `Conv2D`, representar cross-correlation como multiplicación matricial. (Material: 7.2.7–7.2.8)

### IV. 7.3 Relleno y Stride
#### 1. Por Qué Hace Falta Padding
> Sin padding, cada conv “recorta” bordes: tras muchas capas, la representación se encoge mucho y se pierde información en contornos.  
> Se introduce **padding** como herramienta para evitar esa reducción y para usar más uniformemente píxeles (Fig. 7.3.1–7.3.2). (Material: 7.3)
#### 2. Fórmula de Tamaño con Padding
> Si añades (p_h) filas y (p_w) columnas de padding (repartidas arriba/abajo e izquierda/derecha), entonces:  
> [  
> (n_h-k_h+p_h+1)\times(n_w-k_w+p_w+1).  
> ]  
> Caso típico para mantener tamaño: (p_h=k_h-1,; p_w=k_w-1). Se enfatiza que kernels impares (1,3,5,7) facilitan padding simétrico y una interpretación “centrada” de (Y[i,j]). (Material: 7.3.1)
```python
def comp_conv2d(conv2d, X):
    # (1, 1) indicates that batch size and the number of channels are both 1
    X = X.reshape((1, 1) + X.shape)
    Y = conv2d(X)
    # Strip the first two dimensions: examples and channels
    return Y.reshape(Y.shape[2:])
```
#### 3. Stride: Desplazar la Ventana en Saltos
> **Stride** es cuántas filas/columnas avanzas por desplazamiento de la ventana. Aumentarlo sirve para **downsampling** o eficiencia.  
> Con stride ((s_h,s_w)), el tamaño de salida es:  
> [  
> \left\lfloor\frac{n_h-k_h+p_h+s_h}{s_h}\right\rfloor \times  
> \left\lfloor\frac{n_w-k_w+p_w+s_w}{s_w}\right\rfloor.  
> ]  
> Se muestran ejemplos donde stride 2 reduce la resolución a la mitad en alto y ancho. (Material: 7.3.2)
#### 4. Resumen y Ejercicios
> Resumen: padding se usa para evitar shrinkage y equilibrar uso de píxeles; stride reduce resolución (por defecto: padding 0, stride 1). Se menciona que el zero-padding es computacionalmente conveniente y puede introducir información posicional implícita (“whitespace”).  
> Ejercicios (muestra): calcular shapes para parámetros dados; mirror padding; beneficios computacionales/estadísticos de stride>1. (Material: 7.3.3–7.3.4)

### V. 7.4 Múltiples Canales de Entrada y Salida
#### 1. Múltiples Canales de Entrada
> Si la entrada tiene (c_i) canales, el kernel debe tener también (c_i) “rebanadas” (una por canal). Con ventana (k_h\times k_w), el kernel pasa a tener forma (c_i\times k_h\times k_w).  
> La salida (un canal) se obtiene sumando las cross-correlations por canal (suma sobre canales). (Material: 7.4.1)
```python
def corr2d_multi_in(X, K):
    # Iterate through the 0th dimension (channel) of K first, then add them up
    return sum(d2l.corr2d(x, k) for x, k in zip(X, K))
```
#### 2. Múltiples Canales de Salida
> Para obtener (c_o) canales de salida, se apilan (c_o) kernels (cada uno de forma (c_i\times k_h\times k_w)), dando un tensor de kernel de forma (c_o\times c_i\times k_h\times k_w).  
> Cada canal de salida usa **todos** los canales de entrada (con su kernel correspondiente). (Material: 7.4.2)
```python
def corr2d_multi_in_out(X, K):
    # Iterate through the 0th dimension of K, and each time, perform
    # cross-correlation operations with input X. All of the results are
    # stacked together
    return torch.stack([corr2d_multi_in(X, k) for k in K], 0)
```
#### 3. Convolución 1×1
> Un kernel 1×1 no mezcla información espacial (alto/ancho), solo opera en **canales**: cada píxel se transforma por una combinación lineal de sus (c_i) valores hacia (c_o) salidas, con pesos compartidos en todas las posiciones.  
> Interpretación del material: es como una **fully-connected por píxel** (con pesos atados entre posiciones), con (c_o\times c_i) pesos (+ bias). Además, se recuerda que suele ir seguida de no linealidades, por lo que no siempre se “absorbe” en otra conv. (Material: 7.4.3)
```python
def corr2d_multi_in_out_1x1(X, K):
    c_i, h, w = X.shape
    c_o = K.shape[0]
    X = X.reshape((c_i, h * w))
    K = K.reshape((c_o, c_i))
    # Matrix multiplication in the fully connected layer
    Y = torch.matmul(K, X)
    return Y.reshape((c_o, h, w))
```
#### 4. Discusión: Coste Computacional
> El coste para una conv (k\times k) sobre imagen (h\times w) es (O(h\cdot w\cdot k^2)); con canales (c_i,c_o) pasa a (O(h\cdot w\cdot k^2\cdot c_i\cdot c_o)).  
> Ejemplo del texto: 256×256, kernel 5×5, 128 canales entrada y salida → **>53 mil millones** de operaciones (contando multiplicaciones y sumas por separado). (Material: 7.4.4)
#### 5. Ejercicios
> Ejercicios (muestra): composición de convoluciones; coste/memoria forward/backward; factor de incremento al doblar canales; expresar conv como multiplicación matricial; discusión sobre implementación eficiente. (Material: 7.4.5)

### VI. 7.5 Pooling
#### 1. Motivación: Representación Global e Invariancia a Pequeñas Traslaciones
> Para tareas globales (p. ej., “¿hay un gato?”), las últimas unidades deben ser sensibles a toda la entrada; esto se logra **agregando** información y produciendo mapas cada vez más “gruesos”.  
> Además, para features locales (p. ej., bordes), interesa mitigar sensibilidad exacta a la posición: un desplazamiento de 1 píxel puede cambiar mucho la salida de una conv.  
> Se introducen **pooling layers** con dos objetivos: (i) reducir sensibilidad a ubicación y (ii) hacer **downsampling espacial**. (Material: 7.5)
#### 2. Max-Pooling y Average Pooling
> Pooling usa una ventana deslizante como conv, pero **sin parámetros** (sin kernel): es determinista.
> - **Average pooling**: promedia valores en la ventana (analogía con downsampling con mejor SNR al combinar vecinos).
> - **Max-pooling**: toma el máximo; el material indica que “en casi todos los casos” es preferible a average pooling.  
>     Ejemplo (Fig. 7.5.1): con ventana 2×2 se obtiene cada salida como el máximo de los 4 elementos (ecuación 7.5.1). (Material: 7.5.1)
```python
def pool2d(X, pool_size, mode='max'):
    p_h, p_w = pool_size
    Y = torch.zeros((X.shape[0] - p_h + 1, X.shape[1] - p_w + 1))
    for i in range(Y.shape[0]):
        for j in range(Y.shape[1]):
            if mode == 'max':
                Y[i, j] = X[i: i + p_h, j: j + p_w].max()
            elif mode == 'avg':
                Y[i, j] = X[i: i + p_h, j: j + p_w].mean()
    return Y
```
#### 3. Padding, Stride y Canales en Pooling
> - Padding y stride aplican igual que en conv; frameworks suelen poner stride=pool_size por defecto, pero se puede fijar manualmente (`nn.MaxPool2d(..., padding=..., stride=...)`).
> - Pooling es **indiferente a canales**: opera **por canal** y mantiene el número de canales (no suma sobre canales como conv). (Material: 7.5.2–7.5.3)
#### 4. Resumen y Ejercicios
> Resumen: pooling agrega en ventanas; hereda semántica de padding/stride; no cambia canales; max-pooling aporta cierta invariancia; elección común: ventana 2×2 para reducir resolución espacial a 1/4. Se mencionan variantes (stochastic pooling, fractional max-pooling) y se alude a alternativas más “refinadas” de agregación (p. ej., atención).  
> Ejercicios (muestra): average pooling como conv; imposibilidad de max-pooling con solo conv; implementar max con ReLU; coste computacional; comparación max vs avg; softmax pooling. (Material: 7.5.4–7.5.5)

### VII. 7.6 Convolutional Neural Networks (LeNet)
#### 1. Contexto e Historia
> Tras softmax regression y MLP sobre Fashion-MNIST (aplanando 28×28 a 784), ahora se propone mantener estructura espacial con CNNs y obtener modelos más parsimoniosos (menos parámetros).  
> Se introduce **LeNet** (LeNet-5) como una de las primeras CNNs con gran impacto: diseñada para reconocer dígitos manuscritos; se menciona que alcanzó <1% de error por dígito y tuvo despliegue en cajeros/depósitos. (Material: 7.6)
#### 2. Arquitectura de LeNet
> LeNet tiene dos partes:
> - **Convolutional encoder**: 2 bloques conv.
> - **Dense block**: 3 capas fully-connected.  
>     Cada bloque conv usa: **conv + sigmoid + average pooling** (nota histórica: ReLU y max-pooling aún no se habían “descubierto” para este uso, según el texto).  
>     Detalles:
> - Conv1: kernel 5×5, **6** canales de salida.
> - Conv2: kernel 5×5, **16** canales de salida.
> - Pooling: 2×2 stride 2 (reduce área espacial por factor 4).
> - Fully-connected: **120 → 84 → 10** (10 clases).  
>     Se recuerda el formato 4D (batch, channel, height, width) a la salida del bloque conv y la necesidad de **flatten** antes del bloque denso. (Material: 7.6.1)
```python
def init_cnn(module): #@save
    """Initialize weights for CNNs."""
    if type(module) == nn.Linear or type(module) == nn.Conv2d:
        nn.init.xavier_uniform_(module.weight)

class LeNet(d2l.Classifier): #@save
    """The LeNet-5 model."""
    def __init__(self, lr=0.1, num_classes=10):
        super().__init__()
        self.save_hyperparameters()
        self.net = nn.Sequential(
            nn.LazyConv2d(6, kernel_size=5, padding=2), nn.Sigmoid(),
            nn.AvgPool2d(kernel_size=2, stride=2),
            nn.LazyConv2d(16, kernel_size=5), nn.Sigmoid(),
            nn.AvgPool2d(kernel_size=2, stride=2),
            nn.Flatten(),
            nn.LazyLinear(120), nn.Sigmoid(),
            nn.LazyLinear(84), nn.Sigmoid(),
            nn.LazyLinear(num_classes))
```
#### 3. Inspección de Shapes y Observaciones del Texto
> El material imprime shapes por capa y destaca:
> - La primera conv usa **padding=2** para compensar la reducción que produciría el kernel 5×5, manteniendo 28×28 tras conv1.
> - La segunda conv **sin padding** reduce alto/ancho en 4 píxeles (28→10 tras conv+pool según la traza mostrada).
> - Canales: 1→6→16; cada pooling reduce alto/ancho a la mitad; luego las fully-connected reducen dimensionalidad hasta 10 clases.  
>     Nota histórica adicional: el tamaño 28×28 en MNIST proviene de recortar escaneos 32×32 para ahorrar espacio (~30% menos). (Material: 7.6.1, traza de shapes)
#### 4. Entrenamiento (Fashion-MNIST)
> Se propone entrenar LeNet en Fashion-MNIST. El texto recuerda que, aunque CNNs tienen menos parámetros, pueden ser más costosas que MLPs de profundidad similar porque cada parámetro participa en más multiplicaciones; se sugiere usar GPU si está disponible.  
> Se indica que `d2l.Trainer` gestiona detalles y que se usa **cross-entropy** minimizada con **minibatch SGD**. (Material: 7.6.2)
```python
trainer = d2l.Trainer(max_epochs=10, num_gpus=1)
data = d2l.FashionMNIST(batch_size=128)
model = LeNet(lr=0.1)
model.apply_init([next(iter(data.get_dataloader(True)))[0]], init_cnn)
trainer.fit(model, data)
```
#### 5. Resumen y Ejercicios
> Resumen: el capítulo conecta MLPs (años 80) con CNNs (90s/2000s); LeNet-5 sigue siendo una referencia y se sugiere comparar su rendimiento con MLPs y arquitecturas modernas (p. ej., ResNet en el capítulo siguiente del libro). Se enfatiza la facilidad moderna de implementación frente a lo que antes requería meses de ingeniería. (Material: 7.6.3)  
> Ejercicios (muestra): “modernizar” LeNet (avg→max pooling, sigmoid/softmax→ReLU según indica el texto), ajustar tamaños (kernels, canales, nº capas), probar en MNIST, visualizar activaciones de capas 1 y 2 con distintas entradas. (Material: 7.6.4)

---

## D2DpL 8. Modern Convolutional Neural Networks

### I. Introducción Previa
#### 1. Objetivo del Capítulo y Alcance
> Este capítulo hace un “tour” (necesariamente incompleto) por **arquitecturas modernas de CNNs**, presentadas **en orden cronológico**. Su relevancia es doble: (i) se usan directamente en visión, y (ii) sirven como **extractores de características** para tareas como _tracking, segmentación, detección_ o _estilo_.  
> También se enfatiza que el rendimiento depende fuertemente de **arquitectura + hiperparámetros**, y que muchas ideas aquí (p. ej., **batch normalization** y **conexiones residuales**) han acabado aplicándose fuera de visión por computador.

#### 2. Arquitecturas que se Recorren (Página de Contenido)

> El capítulo recorre (entre otras) las siguientes familias/ideas: **AlexNet**, **VGG**, **NiN**, **GoogLeNet/Inception**, **Batch Normalization**, **ResNet**, **ResNeXt**, **DenseNet**, y finalmente una sección sobre **diseño/exploración de espacios de arquitecturas** (RegNetX/Y).

#### 3. Contexto de Tendencia (Nota del Capítulo)

> Se indica que, aunque las CNNs dominaron visión por sus **sesgos inductivos** (localidad e invariancia a traslación), **Transformers** han pasado a liderar en clasificación a gran escala; parte del argumento se relaciona con la disponibilidad de datasets enormes y con el coste computacional.

---

### II. 8.1 Redes Convolucionales Profundas (AlexNet)

#### 8.1.1 Contexto: De LeNet a AlexNet

> Se presenta AlexNet como un punto de inflexión (2012): una CNN profunda entrenada eficazmente en GPU, que gana ImageNet con margen y muestra que **features aprendidas** pueden superar _features_ diseñadas manualmente.

#### 8.1.2 Diseño de la Arquitectura

> Diferencias clave frente a LeNet:
> 
> - **Más profunda**: 8 capas (5 convolucionales + 2 fully-connected ocultas + 1 fully-connected de salida).
>     
> - **Ventanas grandes al inicio** por ImageNet: primera conv de **11×11**, luego **5×5** y después **3×3**.
>     
> - **Max-pooling** tras la 1ª, 2ª y 5ª conv (ventana 3×3, stride 2).
>     
> - **Muchas más canales** que LeNet (≈10× en conv).
>     
> - “Talón de Aquiles” de eficiencia: dos capas fully-connected enormes (4096 salidas) que en el diseño original requerían casi 1GB de parámetros (motivando el reparto en 2 GPUs en 2012).
>     

#### 8.1.3 Activaciones, Regularización y Preprocesado

> - Sustituye **sigmoid → ReLU**: se argumenta por (i) cómputo más simple y (ii) facilitar entrenamiento al evitar regiones con gradiente casi 0 típicas de sigmoid cerca de 0/1.
>     
> - Control de capacidad con **dropout** (especialmente en fully-connected).
>     
> - Aumenta robustez con **data augmentation** (p. ej., _flipping, clipping, cambios de color_).
>     

#### 8.1.4 Entrenamiento en el Material

> Para el ejemplo didáctico, se entrena en **Fashion-MNIST**, pero se reescala a **224×224** para respetar la arquitectura (se indica explícitamente que no es una práctica “inteligente” porque aumenta coste sin añadir información).  
> Configuración mostrada: `lr=0.01`, `batch_size=128`, `max_epochs=10`, y entrenamiento más lento que LeNet por profundidad/anchura/resolución.

#### 8.1.5 Discusión y Ejercicios

> - **Entrenamiento “Fiel” a AlexNet (pero Ineficiente).** En el ejemplo didáctico se reescala Fashion-MNIST a **224×224** para ser fiel a la arquitectura, aunque el propio texto remarca que esto **aumenta el coste** sin añadir información útil; por eso el entrenamiento es **mucho más lento** que en LeNet debido a (i) red más profunda y ancha, (ii) mayor resolución y (iii) convoluciones más costosas.
> 
> - **Mejoras Críticas Respecto a LeNet.** Se enfatiza que AlexNet se parece mucho a LeNet “en espíritu”, pero con mejoras decisivas: **ReLU** (facilita el entrenamiento) y **dropout** (mejora la precisión y regulariza).
> 
> - **Talón de Aquiles de Eficiencia (Fully-Connected Finales).** El texto destaca que las dos capas ocultas finales requieren matrices de tamaño **6400×4096** y **4096×4096**, lo que equivale a **164 MB** de memoria y **81 MFLOPs** de cómputo, un coste relevante para dispositivos pequeños. Además, en el diseño original se menciona que estas capas requerían **casi 1 GB** de parámetros y motivaron repartir el modelo en **dos GPUs** en 2012.
> 
> - **Poca Señal de Overfitting Pese a Muchísimos Parámetros.** Se remarca que, aunque el número de parámetros de las dos últimas capas supera ampliamente el tamaño del dataset usado en el ejemplo (más de **40 millones** de parámetros frente a **60k** imágenes), **apenas hay overfitting**: las pérdidas de entrenamiento y validación son casi idénticas durante el entrenamiento. El texto lo atribuye a la **regularización** (p. ej., dropout) inherente al diseño.
> 
> - **Tooling: Salto Histórico.** Se subraya que lo que en 2012 habría sido “meses de trabajo” ahora puede hacerse en “una docena de líneas” con frameworks modernos; se menciona la falta de herramientas eficientes en aquella época (p. ej., antes de la disponibilidad de frameworks hoy comunes) como un freno a la adopción.
> 
> - **Ejercicios del Material (Ideas Clave).**
>   - Analizar **huella de memoria** y **coste computacional** separando convoluciones vs fully-connected.
>   - Estudiar cómo afecta **memoria/bandwidth/latencia** a entrenamiento e inferencia.
>   - Explicar por qué ya no se reportan benchmarks en AlexNet como referencia principal.
>   - Simplificar AlexNet para 28×28 o diseñar un modelo mejor que opere directamente sobre 28×28.
>   - Variar **batch size** y medir throughput, precisión y memoria GPU.
>   - Probar aplicar **dropout** y **ReLU** a LeNet.
>   - “Romper” regularización: intentar forzar **overfitting** y razonar qué componente habría que cambiar/eliminar.


---

### III. 8.2 Redes Usando Bloques (VGG)
#### 8.2.1 Motivación: de Capas “Ad Hoc” a Bloques Repetibles
> - **Por Qué Pasar a Diseñar con Bloques.** El material dice que AlexNet aportó evidencia empírica de que CNNs profundas funcionan bien, pero **no ofrecía una plantilla general** para guiar diseños posteriores. Por ello, a partir de aquí se introducen **heurísticas de diseño** para construir redes profundas.
> 
> - **Analogía con Diseño de Chips (VLSI).** Se compara el progreso con VLSI: de colocar **transistores** → elementos lógicos → **bloques**. De forma análoga, el diseño de redes ha evolucionado de neuronas individuales → capas → **bloques** (patrones repetibles de capas).
> 
> - **Evolución hacia Reutilización de Modelos.** El texto añade que, con el tiempo, esta abstracción ha avanzado hasta reutilizar **modelos entrenados completos** para tareas relacionadas; a estos modelos grandes preentrenados se les denomina **foundation models**.
> 
> - **Idea Operativa.** La clave práctica es que los **bloques repetibles** se implementan fácilmente en frameworks modernos mediante **bucles** y **subrutinas**, haciendo el diseño más sistemático y menos artesanal.

#### 8.2.2 Bloques VGG

> - **Bloque Básico y Problema de Fondo.** Un patrón clásico en CNNs es repetir: (i) convolución con padding (mantener resolución), (ii) no linealidad (p. ej., ReLU), (iii) pooling (p. ej., max-pooling) para reducir resolución. El problema es que la resolución espacial puede caer **demasiado rápido**: el texto señala un límite duro de orden **log₂(d)** capas convolucionales antes de “agotar” dimensiones; para ImageNet, de este modo sería imposible superar ~**8 capas** convolucionales.
> 
> - **Idea de VGG: Varias Convoluciones Antes de Submuestrear.** Simonyan y Zisserman proponen agrupar **múltiples convoluciones** entre pasos de downsampling (max-pooling), formando un **bloque**. El objetivo era estudiar si conviene más **profundidad** o **anchura**; su análisis concluye que redes **profundas y estrechas** superan significativamente a las más superficiales.
> 
> - **Equivalencia Receptiva y Comparación de Parámetros.** El material destaca que aplicar **dos 3×3** “toca” los mismos píxeles que una **5×5**. Además, una 5×5 usa ~**25·c²** parámetros, mientras que **tres 3×3** usan **3·9·c²** (mismo orden), favoreciendo apilar convoluciones pequeñas. A partir de aquí, apilar **3×3** se convierte en un “gold standard”.
> 
> - **Definición del Bloque VGG (Concreto).** Un bloque VGG consiste en:
>   - Varias convoluciones **3×3** con **padding=1** (mantiene alto y ancho),
>   - Con **ReLU** tras cada convolución,
>   - Seguidas de **max-pooling 2×2 stride 2**, que **divide entre 2** la resolución tras el bloque.


#### 8.2.3 Red VGG Como Familia (VGG-11)

> - VGG se separa en: **parte convolucional/pooling** + **parte fully-connected** similar a AlexNet.
>     
> - Se parametriza con `arch`: lista de tuplas (nº conv, nº canales) por bloque → **familia de redes**.
>     
> - Configuración clásica descrita: 5 bloques conv; los 2 primeros con 1 conv, los 3 últimos con 2 conv; canales empiezan en 64 y se doblan hasta 512; por ello se conoce como **VGG-11**.
>     
> - Se observa el patrón de **reducir H×W a la mitad por bloque** hasta 7×7 antes del _flatten_.
>     

#### 8.2.4 Entrenamiento en el Material

> Para Fashion-MNIST se entrena una variante con menos canales (por coste), manteniendo el esquema general; se usa también `resize=(224,224)` y se reporta poco _overfitting_ (train/val loss cercanas).

#### 8.2.5 Resumen y Ejercicios

> Se argumenta que VGG introduce propiedades “modernas”: **bloques de múltiples conv**, preferencia por **profundo y estrecho**, y **familias** con trade-off velocidad–precisión; además se destaca la facilidad de ensamblaje en frameworks modernos.  
> Ejercicios: comparar parámetros y FLOPs vs AlexNet, reducir coste de fully-connected, construir VGG-16/19 (según paper), y evitar _upsampling_ 224×224 ajustando arquitectura.

---

### IV. 8.3 Network in Network (NiN)

#### 8.3.1 Idea Central (NiN Blocks)

> - **Patrón Común Previo (LeNet/AlexNet/VGG).** El material resume que estas redes siguen el patrón: extraer features con convoluciones/pooling y luego post-procesar con **fully-connected** al final.
> 
> - **Dos Problemas del Patrón.**
>   - **(1) Explosión de Parámetros al Final.** Las fully-connected finales consumen enormes cantidades de parámetros. El texto pone como ejemplo que incluso un modelo como **VGG-11** necesita una matriz “monstruosa” que ocupa ~**400 MB** en FP32, lo que es un problema serio para móviles/embebidos.
>   - **(2) No Puedes Meter FC Antes “sin Romper” la Estructura.** Añadir fully-connected antes destruiría la estructura espacial y además podría requerir todavía más memoria.
> 
> - **Solución NiN (Insight del Material).** Los bloques NiN resuelven ambos problemas con una estrategia simple:
>   - **(i)** usar convoluciones **1×1** para añadir **no linealidad local** entre canales (por localización),
>   - **(ii)** usar **global average pooling** para integrar información de todas las localizaciones al final.
>   - Nota explícita del texto: el global average pooling **no sería efectivo** sin las no linealidades añadidas.
> 
> - **Interpretación Operativa de 1×1.** El material recuerda que una 1×1 puede verse como una capa fully-connected aplicada **independientemente en cada píxel** (por cada (h,w)), actuando sobre el vector de canales.


#### 8.3.2 Modelo NiN y Reducción de Parámetros

> - **Tamaños Iniciales como AlexNet.** NiN usa los mismos tamaños de kernel iniciales que AlexNet: **11×11**, **5×5** y **3×3**, y los números de canales de salida se alinean con los de AlexNet.
> 
> - **Pooling Tras Cada Bloque.** Cada bloque NiN va seguido de un **max-pooling 3×3** con **stride 2**.
> 
> - **Sin Fully-Connected al Final.** La diferencia estructural clave es que NiN **evita completamente** capas fully-connected:
>   - utiliza un bloque NiN cuyo número de canales de salida es **igual al número de clases**,
>   - y después aplica **global average pooling**,
>   - produciendo directamente un **vector de logits**.
> 
> - **Trade-off Declarado.** Este diseño **reduce significativamente** el número de parámetros necesarios, aunque el texto advierte que puede ser a costa de **aumentar** el tiempo de entrenamiento.


#### 8.3.3 Entrenamiento en el Material

> Se entrena en Fashion-MNIST con `resize=(224,224)`; se muestra un ajuste con `lr=0.05`, `batch_size=128`, `max_epochs=10`.

#### 8.3.4 Resumen y Ejercicios

> - Se recalca que la gran reducción de parámetros viene de eliminar las fully-connected gigantes y sustituirlas por **global average pooling**.
>     
> - Se destaca que 1×1 conv + global average pooling influyeron en diseños posteriores.  
>     Ejercicios: variar nº de 1×1 conv por bloque, sustituir 1×1 por 3×3, reemplazar global average pooling por fully-connected y medir impacto (velocidad/parámetros/precisión), etc.
>     

---

### V. 8.4 Redes Multi-Rama (GoogLeNet)

#### 8.4.1 Contexto y Patrón Stem–Body–Head

> Se presenta GoogLeNet (ganador ImageNet 2014) como combinación de ideas de NiN, bloques repetidos y mezcla de kernels. Se destaca que cristaliza una separación clara entre: **stem (ingesta)**, **body (procesamiento)** y **head (predicción)**, patrón que se mantiene en diseños posteriores.

#### 8.4.2 Cuerpo con Bloques Inception (Idea)

> La contribución clave del cuerpo es resolver “qué kernel elegir” concatenando **ramas múltiples**; el material menciona que se usa una versión simplificada (sin pérdidas intermedias del diseño original) por mejoras modernas de entrenamiento.  
> En la construcción concreta del modelo, se discute cómo se asignan canales a ramas y cómo se usan reducciones intermedias para controlar dimensionalidad/coste en ramas más caras.

#### 8.4.3 Esqueleto del Modelo (Módulos b1–b5)

> Se implementa por módulos:
> 
> - **b1 (stem)**: conv 7×7 con 64 canales, stride 2, padding 3 + ReLU + max-pooling.
>     
> - **b2**: conv 1×1 (64 canales) → conv 3×3 (192 canales) + max-pooling.
>     
> - **b3/b4/b5**: secuencias de bloques tipo Inception y max-pooling entre módulos; al final se aplica **global average pooling** (como en NiN) y una capa final para clases.

#### 8.4.4 Entrenamiento en el Material

> Se entrena en Fashion-MNIST reescalado a **96×96**, con `lr=0.01`, `batch_size=128`, `max_epochs=10`, y se muestra inicialización y ajuste con `Trainer`.

#### 8.4.5 Discusión y Ejercicios

> - **Más Precisión con Menor Coste.** El material afirma como rasgo clave que GoogLeNet es **más barato de computar** que sus predecesores y a la vez ofrece **mejor precisión**, marcando un giro hacia un diseño deliberado que intercambia coste de evaluación por reducción de error.
> 
> - **Diseño Manual y Complejidad.** También se remarca que GoogLeNet es computacionalmente complejo y tiene muchos hiperparámetros relativamente “arbitrarios” (canales, número de bloques antes de reducir dimensionalidad, partición de capacidad entre ramas, etc.).
> 
> - **Contexto Histórico: Falta de Herramientas.** Parte de esa “arbitrariedad” se atribuye a que, cuando se introdujo GoogLeNet, todavía no había herramientas maduras para definición automática de redes o exploración sistemática de arquitecturas. El texto menciona que hoy damos por hecho que un framework infiere dimensionalidades automáticamente, pero entonces muchas configuraciones debían especificarse explícitamente, ralentizando la experimentación; además, los primeros intentos de exploración eran caros y tendían a fuerza bruta / estrategias genéticas y similares.
> 
> - **Bloques como Unidad de Experimentación.** Se presenta como inicio de experimentar a nivel de **bloques** con hiperparámetros de diseño, tema que se retoma explícitamente en la Sección 8.8.
> 
> - **Ejercicios del Material (Ideas).**
>   - Implementar iteraciones históricas (p. ej., añadir batch norm, ajustar Inception, label smoothing, añadir residuales).
>   - Determinar el tamaño mínimo de imagen para que funcione.
>   - Diseñar una versión para 28×28 modificando stem/body/head si hiciera falta.
>   - Comparar tamaño de parámetros y cómputo con AlexNet/VGG/NiN.


---

### VI. 8.5 Normalización por Lotes (Batch Normalization)

#### 8.5.1 Entrenamiento de Redes Profundas

> Entrenar redes profundas puede ser difícil por problemas de convergencia; **batch normalization** se presenta como una técnica popular y efectiva que **acelera la convergencia** y, junto con **bloques residuales** (Sección 8.6), ha hecho rutinario entrenar redes con **más de 100 capas**. Además, tiene un efecto de **regularización** “serendípico”.
> 
> El texto conecta BN con una idea clásica de _preprocesado_: al trabajar con datos reales, es habitual **estandarizar** _features_ para que tengan **media cero** y **varianza unidad** (y variantes como normalizar a norma 1 o media cero por observación) para mantener el problema “bien controlado”.
> 
> La motivación clave es trasladar este principio al interior de la red: controlar la escala/centrado de activaciones intermedias para facilitar la optimización. La transformación central se expresa como:
> 
> [  
> \mathrm{BN}(\mathbf{x}) = \boldsymbol{\gamma} \odot \frac{\mathbf{x}-\boldsymbol{\mu}_\mathcal{B}}{\sqrt{\boldsymbol{\sigma}^2_\mathcal{B}+\epsilon}} + \boldsymbol{\beta}  
> ]
> 
> Donde (\boldsymbol{\mu}_\mathcal{B}) y (\boldsymbol{\sigma}^2_\mathcal{B}) se estiman en el minibatch (\mathcal{B}), (\epsilon>0) evita divisiones por cero y (\boldsymbol{\gamma}, \boldsymbol{\beta}) son parámetros aprendibles de **escala** y **desplazamiento**.

#### 8.5.2 Capas de Batch Normalization

> **Capas Fully-Connected.** Para un minibatch (\mathcal{B}) de tamaño (m), el material define:
> 
> [  
> \boldsymbol{\mu}_\mathcal{B} \stackrel{\mathrm{def}}{=} \frac{1}{m}\sum_{i=1}^m \mathbf{x}_i,\qquad  
> \boldsymbol{\sigma}_\mathcal{B}^2 \stackrel{\mathrm{def}}{=} \frac{1}{m}\sum_{i=1}^m(\mathbf{x}_i-\boldsymbol{\mu}_\mathcal{B})^2  
> ]
> 
> y la normalización por ejemplo queda:
> 
> [  
> \hat{\mathbf{x}}_i = \frac{\mathbf{x}_i-\boldsymbol{\mu}_\mathcal{B}}{\sqrt{\boldsymbol{\sigma}_\mathcal{B}^2+\epsilon}}  
> ]
> 
> Tras esto se aplica el **re-escalado y desplazamiento** con (\boldsymbol{\gamma},\boldsymbol{\beta}) (la ecuación de BN). El texto recuerda explícitamente que **media y varianza se computan en el mismo minibatch** al que se aplica la transformación.
> 
> **Capas Convolucionales.** Se aplica BN **después de la convolución y antes de la activación**, pero (a diferencia de FC) se hace **por canal**, agregando estadísticas sobre **todas las localizaciones espaciales**. Si hay (m) ejemplos y para cada canal la salida tiene alto (p) y ancho (q), BN se calcula sobre los (m\cdot p\cdot q) elementos por canal, usando la **misma media/varianza dentro del canal** para normalizar cada localización. Cada canal tiene sus propios parámetros de escala y desplazamiento.
> 
> **Layer Normalization (Contraste).** El material introduce layer norm como alternativa motivada por casos donde el tamaño de minibatch puede ser pequeño: se aplica **por observación**, no depende del minibatch ni cambia entre entrenamiento y test. Para (\mathbf{x}\in\mathbb{R}^n):
> 
> [  
> \mathrm{LN}(\mathbf{x})=\frac{\mathbf{x}-\hat{\mu}}{\hat{\sigma}},\quad  
> \hat{\mu}\stackrel{\mathrm{def}}{=}\frac{1}{n}\sum_{i=1}^n x_i,\quad  
> \hat{\sigma}^2\stackrel{\mathrm{def}}{=}\frac{1}{n}\sum_{i=1}^n(x_i-\hat{\mu})^2+\epsilon  
> ]
> 
> Se destaca como ventaja práctica que (ignorando (\epsilon)) LN es aproximadamente **invariante a escala**: (\mathrm{LN}(\mathbf{x})\approx \mathrm{LN}(\alpha\mathbf{x})) para (\alpha\neq 0), lo que ayuda a prevenir divergencia.

#### 8.5.3 Implementación Desde Cero

> El material implementa `batch_norm` desde cero con dos regímenes:
> 
> - **Predicción (test):** usa `moving_mean` y `moving_var` acumuladas por media móvil para obtener (X_{\text{hat}}).
>     
> - **Entrenamiento:** calcula media y varianza según la forma de (X):
>     
>     - si (X) es 2D (FC), media/varianza en la dimensión de _features_;
>         
>     - si (X) es 4D (Conv2D), media/varianza por canal agregando sobre ((\text{batch}, H, W)) (con `keepdim=True` para _broadcasting_).
>         
> 
> Luego escala y desplaza con (Y=\gamma X_{\text{hat}}+\beta) y actualiza estadísticas con **media móvil** controlada por `momentum` (aclarando que este “momentum” **no** es el del optimizador, aunque se use el mismo nombre por convención de APIs).
> 
> Se remarca el patrón de diseño: (i) matemática en una función (`batch_norm`) y (ii) una capa `BatchNorm` que hace _bookkeeping_ (dispositivo, buffers, inicialización, medias móviles).

#### 8.5.4 LeNet con Batch Normalization

> Se aplica BN en un LeNet “tradicional” recordando la regla: **BN va después de conv/FC y antes de la activación**. Se construye `BNLeNetScratch` insertando `BatchNorm` tras `LazyConv2d` y `LazyLinear`, y se entrena en Fashion-MNIST con `max_epochs=10`, `batch_size=128` y `lr=0.1` (con GPU). Luego se inspeccionan (\gamma) y (\beta) aprendidos en la primera capa BN.

#### 8.5.5 Implementación Concisa

> Se sustituye la implementación manual por las capas del framework (`LazyBatchNorm2d`, `LazyBatchNorm1d`), manteniendo una estructura casi idéntica del modelo. El texto subraya que la variante de alto nivel corre **mucho más rápido** por estar compilada (C++/CUDA) frente a la versión interpretada en Python.

#### 8.5.6 Discusión

> El material insiste en separar **intuiciones** de **hechos establecidos**: aunque se suele decir que BN “suaviza” el paisaje de optimización, no hay una explicación cerrada (y ni siquiera se entiende plenamente por qué MLPs/CNNs generalizan tan bien).
> 
> Se comenta además la controversia sobre “**internal covariate shift**” como explicación (incluyendo debates en la literatura y en discurso más amplio), y se menciona que hay autores que proponen explicaciones alternativas, incluso afirmando que BN funciona pese a comportarse de forma opuesta a lo argumentado originalmente.
> 
> Puntos prácticos que el texto pide recordar:
> 
> - En entrenamiento, BN ajusta continuamente salidas intermedias usando media y desviación típica del minibatch para estabilizar activaciones.
>     
> - BN difiere entre capas FC y conv; para conv, layer norm puede ser alternativa a veces.
>     
> - Como dropout, BN se comporta distinto en entrenamiento vs predicción.
>     
> - BN ayuda a regularizar y mejorar convergencia; pero reducir internal covariate shift **no parece** una explicación válida.
>     
> - Para modelos más robustos y menos sensibles a perturbaciones, se sugiere considerar **eliminar BN** (según referencia citada en el texto).
>     

#### 8.5.7 Ejercicios

> 1. ¿Debe eliminarse el sesgo (_bias_) de la capa FC o conv antes de BN? ¿Por qué?
>     
> 2. Comparar _learning rates_ para LeNet con y sin BN: (i) graficar aumento de _val accuracy_; (ii) máximo LR antes de que falle la optimización.
>     
> 3. ¿Se necesita BN en cada capa? Experimentar.
>     
> 4. Implementar una versión “lite” que solo quite la media (o solo la varianza) y analizar comportamiento.
>     
> 5. Fijar (\beta) y (\gamma) y observar resultados.
>     

---

### VII. 8.6 Redes Residuales (ResNet) y ResNeXt

#### 8.6.1 Clases de Funciones

> El material motiva ResNet con una idea sobre **clases de funciones**: si al hacer una red más profunda la clase de funciones “no contiene” a la anterior, se puede empeorar por el mero hecho de aumentar profundidad. La formulación residual busca que aprender la identidad sea fácil (reformular como “aprender la corrección”).

#### 8.6.2 Bloques Residuales

> - **Qué Problema Ataca.** El texto argumenta que, si al aumentar profundidad no garantizas que la clase de funciones “nueva” contenga a la anterior, puedes empeorar. Para evitarlo, conviene que el modelo más grande pueda comportarse como el más pequeño (p. ej., aprendiendo la identidad).
> 
> - **Reformulación Residual.** Dado un mapeo deseado f(x), un bloque residual hace que el bloque dentro de la “caja” aprenda:
> 
>   - En red “directa”: aprender f(x) directamente.
>   - En residual: aprender g(x)=f(x)−x, y devolver x+g(x).
> 
> - **Caso Identidad: Por Qué Es Más Fácil.** Si el mapeo deseado es la identidad f(x)=x, entonces g(x)=0. El material dice que esto es más fácil de aprender: basta con empujar pesos/sesgos de las capas dentro del bloque hacia cero.
> 
> - **Conexión Residual (Atajo).** La línea que lleva x hasta el sumador es la **residual/shortcut connection**. Con estos atajos, las entradas pueden propagarse hacia delante más rápido a través de conexiones residuales entre capas.


#### 8.6.3 Modelo ResNet

> Se construye un **ResNet-18** con una organización por bloques (módulos `b1`–`b5`): un _stem_ inicial seguido de grupos de bloques residuales que van reduciendo resolución y aumentando canales, terminando con _global average pooling_ y una capa final para clasificación.

#### 8.6.4 Entrenamiento

> En el ejemplo didáctico se entrena el modelo sobre **Fashion-MNIST reescalado a 96×96**, usando el mismo patrón de entrenamiento que en secciones anteriores (con `Trainer`, `batch_size=128`, `max_epochs=10`, GPU).

#### 8.6.5 ResNeXt

> - **Motivación en el Material.** Se plantea el trade-off típico en ResNet dentro de un bloque: añadir no linealidad aumentando capas o aumentando anchura. ResNeXt introduce un eje adicional: **agregar transformaciones** mediante **grouped convolutions**.
> 
> - **Grouped Convolution: Ahorro en Cómputo y Parámetros.** El texto define grouped convolution como partir una conv de cᵢ→cₒ en g grupos de tamaño cᵢ/g, produciendo g salidas de tamaño cₒ/g. El coste proporcional baja de O(cᵢ·cₒ) a O(cᵢ·cₒ/g), es decir, es **g veces más rápido**; y el número de parámetros también se reduce en un factor **g** (g matrices pequeñas en lugar de una grande).
> 
> - **Problema y Arreglo: Mezcla entre Grupos.** La dificultad es que no se intercambia información entre grupos. ResNeXt lo corrige “encajando” la conv 3×3 agrupada entre dos conv **1×1**:
>   - pagas el coste O(c·b) en las 1×1,
>   - y solo O(b²/g) en la 3×3,
>   donde b es el número de canales intermedios (bottleneck).
> 
> - **Atajo Generalizado.** El material indica que la conexión residual puede **reemplazarse/generalizarse** por una conv **1×1** cuando hay que casar dimensiones (p. ej., al bajar resolución).
> 
> - **Nota Histórica.** Se menciona que la idea de grouped convolutions ya estaba en AlexNet: al repartir el modelo entre dos GPUs con memoria limitada, se trató cada GPU como su “propio canal” sin efectos adversos.


#### 8.6.6 Resumen y Discusión

> El material resume que los **bloques residuales** hacen práctico entrenar redes muy profundas, y que variantes como **ResNeXt** explotan la agregación (vía grupos) para mejorar diseños sin complicar excesivamente la plantilla del bloque.

#### 8.6.7 Ejercicios

> 1. Practicar con `ResNeXtBlock` y revisar salida a nivel de bloque/red; entender hiperparámetros de diseño.
>     
> 2. ¿Por qué ResNet funciona bien incluso cuando (f(x)=0)? Relacionarlo con identidad y facilidad de optimización.
>     
> 3. Comparar ResNet/ResNeXt con distintas profundidades/ancho y discutir coste vs precisión.
>     
> 4. Añadir operaciones tipo “shift” (se menciona ShiftNet como ejemplo) y estudiar impacto.
>     
> 5. Probar/variar cardinalidad en ResNeXt y analizar resultados.
>     

---

### VIII. 8.7 Redes Densamente Conectadas (DenseNet)

#### 8.7.1 De ResNet a DenseNet

> DenseNet reemplaza la suma residual por **concatenación** de características: cada capa recibe como entrada todas las salidas previas concatenadas. El material contrasta explícitamente:
> 
> - ResNet: (\mathbf{x}_\ell = f_\ell(\mathbf{x}_{\ell-1}) + \mathbf{x}_{\ell-1}).
>     
> - DenseNet: (\mathbf{x}_\ell = H_\ell([\mathbf{x}_0,\mathbf{x}_1,\dots,\mathbf{x}_{\ell-1}])), donde ([\cdot]) denota concatenación.
>     
> 
> La motivación práctica es promover **reutilización de _features_** y facilitar flujo de información/gradiente al conectar densamente capas.

#### 8.7.2 Bloques Densos

> Un **dense block** apila varias capas donde cada nueva capa produce un número fijo de mapas de características (la **growth rate**) y estos se concatenan con todo lo anterior, haciendo crecer el número de canales conforme avanza el bloque.

#### 8.7.3 Capas de Transición

> Entre dense blocks se insertan **transition layers** para controlar el crecimiento: típicamente una conv (1\times1) para reducir canales y un _pooling_ para reducir resolución, evitando explosión de coste/memoria.

#### 8.7.4 Modelo DenseNet

> El modelo se construye como: capa inicial → secuencia de (dense block → transition layer) → bloque final → _global average pooling_ → capa lineal de salida.

#### 8.7.5 Entrenamiento

> Se entrena sobre Fashion-MNIST reescalado a 96×96 con el mismo esquema de entrenamiento estándar del capítulo (con `Trainer`, `batch_size=128`, `max_epochs=10`, GPU).

#### 8.7.6 Resumen y Discusión

> El texto destaca como ventaja que DenseNet es **eficiente en parámetros** gracias a la reutilización de representaciones, pero avisa de un coste importante: el diseño con concatenaciones tiende a requerir **mucho consumo de memoria GPU**.

#### 8.7.7 Ejercicios

> 1. ¿Por qué es buena idea usar **capas de transición** en DenseNet? (Discusión sobre control de crecimiento).
>     
> 2. Se menciona la propuesta de añadir conexiones densas en MLPs (citado como idea en la literatura): discutir pros/contras y qué habría que adaptar.
>     

---

### IX. 8.8 Diseño de Arquitecturas Convolucionales

#### 8.8.0 Contexto y Motivación del Diseño de Arquitecturas Convolucionales

> - **De Tour Histórico a Ingeniería de Redes.** El material abre 8.8 diciendo que las arquitecturas previas han dependido mucho de la intuición/creatividad humana, y que ese “network engineering” ha sido muy exitoso.
> 
> - **Resumen de Aportes (Según el Texto).**
>   - Desde AlexNet se populariza apilar bloques para construir redes muy profundas.
>   - VGG populariza el uso de **3×3** como patrón dominante.
>   - NiN muestra que **1×1** añade no linealidades locales útiles y que el “head” puede agregarse con **global average pooling**.
>   - GoogLeNet introduce **multi-ramas** combinando ventajas de VGG y NiN en Inception.
>   - ResNet cambia el sesgo inductivo hacia el **mapeo identidad** (haciendo posible redes muy profundas).
>   - ResNeXt añade **grouped convolutions** para mejorar el trade-off parámetros–cómputo.
>   - Se menciona SENet como mecanismo de atención global por canal para transferir información de forma eficiente.
> 
> - **Por Qué No Se Trata NAS Aquí.** El texto dice que se omite NAS porque suele ser de coste enorme (búsqueda fuerza bruta, genéticos, RL, etc.). NAS elige una arquitectura dentro de un espacio y devuelve una **instancia única**; se cita EfficientNets como resultado notable.
> 
> - **Objetivo de 8.8.** Pasar de “arquitecturas una a una” a **espacios de diseño** y estrategias más sistemáticas (lo que conduce a RegNetX/Y).

#### 8.8.1 Espacio de Diseño AnyNet

> El material presenta una estrategia (inspirada en Radosavovic et al.) que combina diseño manual y NAS: operar sobre **distribuciones de redes** y optimizar dichas distribuciones, buscando que muchas redes muestreadas sean buenas y que el soporte sea conciso.
> 
> **Estructura AnyNet:** patrón **stem–body–head**. El _stem_ toma imágenes RGB con una conv (3\times3) stride 2 + batch norm para **halvar resolución**, generando (c_0) canales. El _body_ reduce (para ImageNet) de 224×224 a 7×7 a través de **4 stages**, cada uno con stride efectivo 2; el _head_ usa _global average pooling_ + capa fully-connected para clasificación.
> 
> El _body_ se organiza en **stages** formados por bloques (en el material, tipo ResNeXt): el primer bloque de un stage reduce resolución (stride 2) y requiere conv (1\times1) en la rama residual para casar dimensiones; luego siguen bloques sin cambio de resolución/canales. Se define además el **bottleneck ratio** (k_i) (nota: el texto dice que “no es realmente efectivo” y conviene omitirlo) y el número de grupos (g_i) por stage.
> 
> **Hiperparámetros del espacio:** (c_0,\dots,c_4) (anchos), (d_1,\dots,d_4) (profundidades por stage), (k_1,\dots,k_4) (bottleneck ratios), (g_1,\dots,g_4) (group widths). En total: **17 parámetros**, haciendo el espacio enorme.

#### 8.8.2 Distribuciones y Parámetros de Espacios de Diseño

> Se argumenta que buscar la “mejor” configuración exhaustivamente es inviable (con solo 2 opciones por parámetro serían (2^{17}=131072) combinaciones) y además aporta poco conocimiento transferible.
> 
> El enfoque se apoya en cuatro supuestos: (1) existen principios generales (muchas buenas redes, no una aguja única); (2) no hace falta entrenar a convergencia para discriminar (multi-fidelity con proxies); (3) lo hallado a pequeña escala generaliza; (4) el efecto de aspectos del diseño se puede factorizar aproximadamente.
> 
> Para comparar elecciones se propone evaluar **distribuciones de error** mediante CDF:
> 
> [  
> F(e,p)\stackrel{\mathrm{def}}{=}\mathbb{P}_{\text{net}\sim p}{e(\text{net})\le e},\qquad  
> \hat{F}(e,Z)=\frac{1}{n}\sum_{i=1}^n \mathbf{1}(e_i\le e)  
> ]
> 
> El texto afirma que si la CDF de una elección **mayoriza** a otra, es superior (o indiferente si empata). Con este criterio se muestran simplificaciones: **atar** (k_i=k) no afecta a la distribución, **atar** (g_i=g) tampoco; en cambio imponer que el ancho por stage **aumente** mejora, y que la profundidad por stage **aumente** también mejora (según comparación de CDFs en Fig. 8.8.2).

#### 8.8.3 RegNet

> El resultado es un espacio AnyNetX(_E) con principios de diseño explícitos:
> 
> - Compartir bottleneck ratio: (k_i=k) para todos los stages.
>     
> - Compartir group width: (g_i=g) para todos los stages.
>     
> - Ancho no decreciente por stage: (c_i \le c_{i+1}).
>     
> - Profundidad no decreciente por stage: (d_i \le d_{i+1}).
>     
> 
> Además, al estudiar las mejores redes de la distribución, se observa que el ancho ideal crece aproximadamente **lineal** con el índice de bloque: (c_j \approx c_0 + c_a j) (y se aproxima con una función por tramos al elegir un ancho constante por stage). Experimentalmente se indica que (k=1) rinde mejor (recomendación: **no usar bottleneck**).
> 
> Se da un ejemplo concreto (RegNetX32): (k=1), (g=16), `stem_channels=32`, con dos stages de canales ((32,80)) y profundidades ((4,6)). También se menciona que el mismo principio se mantiene al escalar y que aplica a diseños con SE (RegNetY).

#### 8.8.4 Entrenamiento (Ejemplo en el Material)

> El ejemplo entrena `RegNetX32` en Fashion-MNIST con `batch_size=128`, `resize=(96,96)`, `max_epochs=10` y GPU; en el snippet mostrado se instancia con `lr=0.05`.

#### 8.8.5 Discusión (Cierre del Capítulo)

> Se cierra contrastando sesgos inductivos de CNNs (localidad e invariancia a traslación) con el avance de **Transformers** en visión: se menciona que han superado a CNNs en clasificación a gran escala, que parte del progreso puede “backportearse” a CNNs con mayor coste, y que optimizaciones de hardware recientes han ampliado la ventaja hacia Transformers. También se relaciona con disponibilidad de grandes colecciones (p. ej., LAION) y se invita a capítulos posteriores para profundizar.

#### 8.8.6 Ejercicios

> 1. Revisar/derivar propiedades de la transformación por CDF (probability integral transform) y discutir uso para parametrizar espacios.
>     
> 2. Discusión sobre si conviene asumir covarianza de activaciones a rango completo y alternativas (aproximaciones).
>     
> 3. Explorar aproximaciones estructuradas (p. ej., bloque-diagonal) y su impacto.
>     
> 4. Diseñar variantes aumentando nº de _stages_ y analizar.
>     
> 5. Probar cambios “anti-principios” (mencionado como “VioNet”) y observar degradación.
>     
> 6. Extrapolar principios a MLPs y discutir límites.
>     

#### Tabla Comparativa de Arquitecturas (8.1–8.4, 8.6, 8.7) y Cierre con Ideas de Diseño
> **Tabla Comparativa (Resumen Operativo)**
> 
> |Arquitectura|Idea Estructural|Cómo Reduce Coste/Parámetros|Nota del Material|
> |---|---|---|---|
> |AlexNet (8.1)|5 conv + 2 FC ocultas grandes + ReLU + dropout|Coste alto en FC (matrices enormes); regulariza con dropout|Se reescala a 224×224 en Fashion-MNIST “por fidelidad”, aunque es ineficiente|
> |VGG (8.2)|Diseño por **bloques**: varias 3×3 antes de _pooling_|Bloques repetibles; familias con trade-off; pero computacionalmente exigente|VGG-11 como ejemplo de familia parametrizada por `arch`|
> |NiN (8.3)|**MLP por parche** con 1×1 conv + **global average pooling**|Elimina FC gigantes → muchos menos parámetros|Global average pooling como sustitución directa de FC final|
> |GoogLeNet (8.4)|**Multi-rama** (Inception), patrón stem–body–head|Control de coste vía diseño de ramas y reducciones intermedias|Se destaca como diseño deliberado para precisión con menor coste|
> |ResNet / ResNeXt (8.6)|**Bloques residuales** (atajo identidad + rama residual); ResNeXt añade **grupos**|ResNet facilita optimizar redes muy profundas sin “pagar” en parámetros por el atajo; ResNeXt explota **cardinalidad** vía convoluciones agrupadas para ganar capacidad con coste controlado|ResNeXt se formula como agregación homogénea (vía grouped conv) sobre el bloque residual|
> |DenseNet (8.7)|Conectividad **densa por concatenación**: cada capa ve todas las previas|Reutiliza _features_ → eficiencia en parámetros; pero puede ser muy exigente en **memoria GPU** por concatenaciones|Se subraya explícitamente el coste de memoria como trade-off importante|
> 
> **Cierre: Ideas de Diseño (8.8)**
> 
> - Plantilla **stem–body–head** y descomposición del _body_ en **stages** (bajando resolución progresivamente).
>     
> - Definir un **espacio de diseño** con hiperparámetros claros por stage: (c_i) (canales), (d_i) (bloques), (g_i) (grupos), (k_i) (bottleneck).
>     
> - Evitar búsqueda exhaustiva: evaluar **distribuciones de redes** (no una sola red) y comparar mediante CDF/empirical CDF.
>     
> - Reducir el espacio sin perder rendimiento: **atar** (k_i) y (g_i) entre stages; imponer **monotonía** de ancho/profundidad entre stages (mejora según comparación de CDFs).
>     
> - RegNet: anchos que crecen aproximadamente lineal con el índice de bloque ((c_j\approx c_0+c_a j)), aproximados por tramos por stage; recomendación empírica de (k=1) (sin bottleneck); extensión a RegNetY con SE.
>     
> - Cierre global: se contrasta la utilidad de sesgos inductivos de CNNs con la escalabilidad y rendimiento actual de Transformers en visión a gran escala.

##### ALTERNATIVA
#### Resumen Comparativo de Arquitecturas y Cierre con Ideas de Diseño

> **Arquitecturas (8.1–8.4, 8.6, 8.7): Qué Aporta Cada Una**
> 
> - **AlexNet (8.1)**  
>   - Plantilla: 5 conv + 2 fully-connected ocultas grandes + ReLU + dropout.  
>   - Punto crítico del material: las fully-connected finales son el “talón de Aquiles” por eficiencia (matrices enormes; coste notable en memoria y MFLOPs).  
>   - Observación del texto: pese a muchísimos parámetros frente al tamaño del dataset del ejemplo, hay **poco overfitting** por regularización (dropout).
> 
> - **VGG (8.2)**  
>   - Idea estructural: diseñar con **bloques repetibles** (varias 3×3 + ReLU antes de max-pooling).  
>   - Aporte: preferencia por redes **profundas y estrechas**; y VGG se presenta como **familia** parametrizable con trade-off velocidad–precisión.
> 
> - **NiN (8.3)**  
>   - Idea: 1×1 para no linealidad local por canal + **global average pooling** al final.  
>   - Efecto: elimina fully-connected gigantes; el texto destaca que así tiene **dramáticamente menos parámetros** (aunque puede aumentar tiempo de entrenamiento).
> 
> - **GoogLeNet / Inception (8.4)**  
>   - Idea: concatenar **múltiples ramas** con kernels distintos para evitar elegir uno solo.  
>   - Discusión del material: es **más barato de computar** que predecesores y mejora precisión; marca el inicio de diseño deliberado y experimentación a nivel de **bloque**.
> 
> - **ResNet / ResNeXt (8.6)**  
>   - ResNet: bloque residual aprende g(x)=f(x)−x y suma con x, facilitando aprender identidad y entrenar redes profundas.  
>   - ResNeXt: grouped convolutions con **reducción g×** en coste y parámetros, más 1×1 para mezclar entre grupos (bottleneck “sandwich”).
> 
> - **DenseNet (8.7)**  
>   - Idea: conexiones densas por **concatenación** (cada capa ve todas las previas).  
>   - Trade-off explícito del material: reutiliza features y es computacionalmente eficiente, pero induce **alto consumo de memoria GPU** por concatenaciones (y puede requerir implementaciones más eficientes en memoria).
> 
> **Cierre de Diseño (8.8): De Arquitecturas a Espacios**
> 
> - Plantilla base: **stem–body–head**, con el body organizado por **stages** que reducen resolución progresivamente.  
> - Definir un **espacio de diseño** con hiperparámetros por stage (anchos cᵢ, profundidades dᵢ, grupos gᵢ, bottleneck ratios kᵢ) y reconocer que el espacio es enorme.  
> - Idea metodológica: evitar buscar “una aguja” y comparar elecciones mediante **distribuciones de error** (CDF / empirical CDF), para poder simplificar el espacio sin perder rendimiento.  
> - Resultado: principios tipo RegNet (atar ciertos hiperparámetros, imponer monotonicidad de anchos/profundidades, y ejemplo concreto RegNetX32 con k=1, g=16, stem_channels=32, etc.).
