### I. Introduction
#### 1. Problemas de las capas lineales
> Escala de los parámetros: con modelos muy profundos y cosas más complicadas, el número de parámetros va a aumentar exponencialmente.
> No partido a la forma de los datos: los píxeles del alrededor tienen más importancia que los de lejos, con las lineales esta relación no se coge.
#### 2. Solución
> Otro tipo de redes: Convolucionales, que son tolerantes ante algunas transformaciones de imágenes (ej. no es lo mismo en una lineal tener a un perro a la izquierda o a la derecha en una imagen).
> Vamos a tener un filtro que vamos a ir arrastrando a toda la imagen, se tienen unos pesos compartidos en todo la imagen. Los filtros recogen la información cercana (un píxel y sus vecinos). Se van a usar varias capas de convoluciones, el modelo va a sacar características de la imagen como texturas o bordes, al ir aplicando varias convoluciones, los filtros están viendo partes considerables del modelo, y al final del modelo ven distintos objetos. 
### II. Capas Convolucionales
#### 1. Kernel
> Es un filtro que arrastramos a lo largo de la imagen, tiene anchura y altura. Se van a multiplicarse cada uno de los elementos del kernel, se van a sumar en una feature map. Arrastrando el kernel se va generando el feature map con el que se quitan columnas y filas (dependiendo de las dimensiones del kernel). Este tiene tanta profundidad como los canales de la imagen, todos los elementos de los canales se suman, (rgb -> 3 canales), por lo que vamos a tener un 3x3x3 con un kernel 3x3. El feature map de salida tendrá solo un canal. 
> kernel altura anchura y profundidad, se desliza una posicion (overlap) a la vez y el resultado de las multiplicaciones se convierte en una posicion del feature map.
#### 2. Feature Map & Receptive Field
> rellenar con dos diapos
> El receptive field es la ventana a la que estas mirando EXCLUSIVAMENTE, no yendo para atrás.
#### 3. Varios Canales
> Se aplican `n` kernels para conseguir `n` canales de salida, esto sirve porque la información puede estar repartida en los distintos canales. Todos los kernels leen todos los canales. Esto funciona en la práctica con un tensor de 4 dimensiones: altura, anchura, canales entrada, canales salida.
#### 4. Pooling
> Sirve para reducir el tamaño de la imagen, la gracia es que alguna vez no queremos aplicar convolución porque la imagen es muy grande, esto xq la convolucion sería demasiado lenta.
> Parecido pero:
> 1) no se multiplican pesos, solo se hace una función de agregación (mean, max) y con eso generamos el siguiente valor
> 2) no se reducen los canales, porque se pierde información, devuelve el mismo nº que tuviera la entrada. no se forma una columna por cada canal.
> 
> El average se utiliza para reducir la dimensionalidad al principio del modelo, y también al final del todo (global average pooling) para cuando hay más canales de salida que los que traía la imagen incial, para reducir los features map a un vector para poder clasificar. Sustituye al flatten ya que hace la media de todos los valores de cada feature map -> All convolutional net.
> Resumen: una red con varias convoluciones, al principio una imagen con canales, cada convolucion va a tener varios kernels, que van a reducir la imagen inicial poco a poco, y a la vez se aumnetan los canales poco a poco para que el modelo separa las características en diferentes canales para que clasifique mejor. En las últimas capas si se ha reducido todos los features maps a un punto (un vector entre todos) se pueden clasificar directamente, si no, se puede aplicar GAP que es más cómodo y escalable a varios tamaños de imagen, con el que también se obtiene el vector con un valor por feature map al que se puede pasar una lineal para predecir.
> 
> Max Pool: solo se utiliza como no linealidad o para reducir dimensionalidad intermedia, no hay uno teóricamente mejor.
#### 5. Estructura
> Vamos a tener una convolución (lineal), una activación, y (a veces) un pooling (mejor en las primeras capas). Al principio el kernel mira a 3x3, en la segunda está mirando a una sección 3x3 en el feature map, entonces está mirando a más de 3x3 de la imagen original (5x5 en este caso), ya que está mirando a varios elementos del feature map, y cada elemento único del feature map mira a varios elementos (compartidos, por eso no es 3x3x3) de la imagen original o feature map anterior.
#### 6. Padding
> Un problema de las convoluciones es que se pasan pocas veces por los píxeles de las esquinas y por los del centro muchas, por lo que si hay información importante ahí se está perdiendo.
> El padding es añadir relleno a la imagen (aumentar el tamaño de la imagen con ceros). También se puede usar para mantener la dimensión entre capa y capa y que no se reduzca. 
##### PRACTICA
> Fold y unfold: operaciones que desenrollan las secciones de la imagen. El unfold pone en una sola dimension cada sección (ventana) para hacerlo sin for.

### III. Padding (CONFIGURACIONES)
#### 1. Padding
> Tiene dos razones de ser: 
> 1) en los bordes se pasan menos veces con el kernel por lo que se pierde información
> 2) se puede controlar mejor si queremos que las dimensiones no se reduzcan entre cada capa
> Consiste en rellenar columnas y filas (bordes) de ceros 
#### 2. Dilation
> Como de separados están los valores del kernel (>0 kernel no compacto), esto hace que el kernel pueda mirar a una región más grande de la imagen, sirve para escanear la imagen más rápido y en menos capas acaban viendo toda la imagen. La relación entre el receptive field y la dilation es proporcional.
#### 3. Groups
> Se puede usar para dividir en grupos los canales de entrada, por lo que cada kernel no va a tener toda la profundidad de la imagen original, va a tener la profundidad del grupo que se le asigne. Para buscar información global es más dificil, pero se reduce el número de parámetros y por lo tanto menos costoso para entrenar. Para reducir complejidad mejor usar groups que reducir el número de canales. Esto no cambia el receptive field, ya que solo modifica la agrupación de canales, solo se ven afectados los parámetros del modelo.
#### 4. Striding
> Hay que buscar que aumente el número de canales finales respecto a los iniciales, que esto no significa que en cada capa se tengan que aumentar, se tiene que ver como tendencia global (se reducen las características).
> 
#### 5. Convoluciones
> Los kernels hay que mantenerlos medianamente pequeños (3x3), el patrón de diseño correcto es empezar con 7x7 o con maxpool para reducir la dimension inicial, y luego repetir mucho los patrones.
> - 1x1: se utiliza para cambiar el número de canales a menor pasando de 3 a 1, ya que luego disminuyen mucho el número de patrones.
> Dos tipos de flujo:
> - Conv -> ... -> Conv -> Flatten -> Lineal -> ... -> Lineal -> Softmax
> - Conv -> AvgPool -> Lineal -> Softmax
##### Buen ejercicio
> intentar hacer esta convolución con group

### IV. Otros Modelos
>Los modelos que tenemos que hacer nosotros deberían de ser más anchos en vez de más profundos, ya que no tenemos la cantidad suficiente de datos para aprovechar la profundidad. Al tener pocos datos es posible que salga overfitting con más profundidad, mientras que con más anchura, se "prueban varios caminos" para llegar al resultado.
#### 1. Lenet-5
> a
#### 2. AlexNet
> a

### V. Profundidad
#### 1. Problema
> Al pasarse con la profundidad el modelo puede ni entrenar, por exploding y vanishing gradients, por lo que al hacer el forward y backward, la señal mandada va a ser prácticamente 0 y peta. Por lo que más de 16 capas no deberíamos de poner ya que los resultados van a ser peores.
#### 2. Data Augmentation
> Esto se puede usar para ayudar a llegar a los thresholds requeridos. Aleatoriamente se hace alguna transformación a las imágenes que le entran al modelo. Se aplica a posiciones, color y escala, para dar robustez al modelo. Se puede usar torch vision y usar transform para aplicarlo (random flip, crop, etc), se les indica una probabilidad que corresponde con la probabilidad de que se aplique la transformación o no, imagen a imagen dentro de un batch. Suele subir el accuracy en un ~5%.
### VI. Convolutions not 2D
#### 1. RANDOM - Up Convolutions
> Hemos empezado con un modelo de embudo en el que se reducen las dimensiones iniciales hasta poder clasificar. Pero para otras tareas no podemos ceñirnos a disminuir sin parar, para algunas habrá que tener una salida del mismo tamaño inicial. Para esto se utiliza una U Net, que empieza reduciendo dimensionalidad, forzando al modelo a que comprima la información, y luego se descomprime. Esto se utiliza en general para hacer máscaras, detección de objetos, etc.
> Utiliza dos tipos de capas:
> - Up Convolutions: Es como la inversa de la convolución, que con su operación diferente aumenta la imagen en vez de disminuirla
> - UnPoolings: Si estamos reduciendo, cogemos un máximo, y en el lado contrario aumentamos a partir de ese valor, y el resto o se interpolan o se dejan a 0.
#### 2. Convolution 1D
> Se pueden usar en lugar de RNNs, aquí el kernel  se desliza en una sola dimension. Por ejemplo con palabras, en una frase de 9 palabras, pues el kernel va de 3 en 3 palabras. La profundidad de este kernel es la dimensión del embedding (representación vectorial de cada una de las palabras).
> Cuando estamos en NLP o Forecasting interesa mirar solo al pasado, aquí se usa la convolución para que solo mire a los instantes del pasado para explicar/predecir lo siguiente.
#### 3. Convolution 3D
> Se utilizan por ejemplo en escáneres de tórax, que es en objetos 3d, o en videos, que haciendo un sampling de los frames, se puede emplear una convolución, y esta si que pilla la dimensión temporal. 

##### PREGUNTAS
> O tenemos fors prohibidos o nos fijan usar uno. Aquí entra el papel de UNFOLD y FOLD.
> - Unfold: 
> - Fold: 
> Son operaciones NO inversas si hay overlapping, ya que al poner valores luego se suman, por lo que la entrada en general no es la misma que la salida.