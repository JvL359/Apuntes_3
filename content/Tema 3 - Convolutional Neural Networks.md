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
> Vamos a tener una convolución (lineal), una activación, y (a veces) un pooling (mejor en las primeras capas). Al principio el kernel mira a 3x3, en la segunda está mirando a una sección 3x3 en el feature map, entonces está mirando a más de 3x3 de la imagen original (5x5 en este caso), ya que está mirando a varios elementos del feature map, y cada elemento único del feature map mira a varios elementos (compartidos, por eso no es 3x3x3) de la iamgen original o feature map anterior.
#### 6. Padding
> Un problema de las convoluciones es que se pasan pocas veces por los píxeles de las esquinas y por los del centro muchas, por lo que si hay información importante ahí se está perdiendo.
> El padding es añadir relleno a la imagen (aumentar el tamaño de la imagen con ceros). También se puede usar para mantener la dimensión entre capa y capa y que no se reduzca. 
##### PRACTICA
> Fold y unfold: operaciones que desenrollan las secciones de la imagen. El unfold pone en una sola dimension cada sección (ventana) para hacerlo sin for.