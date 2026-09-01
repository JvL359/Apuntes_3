### I. Before RNNs
#### 1. Modelos Autoregresivos
> Queremos un modelo que prediga la probabilidad o valor del próximo valor. Con pocos datos funcionan bien y si hay que reentrenar mucho los modelos también. 
> Aquí nuestro input son secuencias y vamos a querer hacer un hidden state para predecir los siguientes elementos. Encodean la información principal en esas capas intermedias. 
> Se pueden entender como modelos probabilísticos de Markov, en el que la predicción en un instante temporal depende de todo lo anterior. Se va prediciendo de izquierda a derecha. 
> Las predicciones las vamos a hacer de step en step, aquí se va acumulando el error con cada predicción. Para solucionarlo, si no hay muchos datos y la predicción temporal es siempre la misma, podemos intentar sacar todos los saltos que necesitamos, si no pues tener muchos datos también funciona.
> A la hora de evaluarlos es importante evaluarlos en condiciones difíciles y no en las más fáciles. Es mejor hacer extrapolación que interpolación porque suele ser más difícil.
#### 2. Modelos de Lenguaje
> Aquí se predice la siguiente palabra de una secuencia. Tenemos N-gramas que funcionan con una ventana fija, pero tienen un problema que es que contar la frecuencia de las palabras no es suficiente porque no entiende y no aprende el significado de cada contexto.
#### 3. Perplexity
> En el peor caso de todos va a dar infinito y en el mejor caso es 1, el upper bound que todos los modelos deberían pasar es 1 / |v|. Ese peor caso es predecir 0 para cada una de las palabras que podemos predecir. Se usa el exponente para fijar un rango "bonito". En el caso aleatorio (misma probabilidad a todas las palabras) 

### II. Introduction
#### 1. Inputs
> One hot encoding: voy a tener un 1 donde corresponde y 0 en el resto de columnas, esto es poco eficiente ya que consumen mucha memoria en guardar tensores llenos de 0s, y también que a priori no tiene nada de información.
> Embeddings: estos son mejores ya que aportan información pudiéndose entrenar (preentrenamiento del modelo). Se suelen cargar embeddings preentrenados con muchos más datos de lo que podríamos hacer por nuestra cuenta

### III. RNNs
#### 1. Idea
> A partir de los inputs van a ir generando esos hidden states, y comparten los parámetros que son reutilizados en toda la RNN, cuando hacemos una predicción hay que esperar a que terminen todas las anteriores. En este tipo de capas, si medimos la carga computacional en comparación con otras, a pesar de tener menos parámetros, tardan más ya que tienes que esperar a tener el hidden state de la capa anterior listo. IMPORTANTE: EL HIDDEN STATE ES LO MISMO QUE EL OUTPUT. SI PREGUNTAN POR EL OUTPUT DE LA RNN ES SIN LA TRANSFORMACIÓN. 
