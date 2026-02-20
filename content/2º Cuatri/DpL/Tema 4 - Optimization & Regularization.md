### I. Algoritmos de Optimización
#### 1. Problema de SGD
> Hay que tener mucho cuidado con el learning rate, ya que es muy sensible porque al pasarse (muy grande) se puede no llegar a la solución óptima, y al quedarse corto (muy pequeño) tarda demasiado.
> Con esto surge el método del momento, para que la trayectoria sea algo más directo. Hasta ahora actualizábamos el peso cada vez que hacíamos una predicción borrando el gradiente anterior. Esto lleva a problemas con un gradiente ruidoso, que puede alejarnos del óptimo y ralentizar el entrenamiento. Por lo que añadimos un término de momento, normalmente es el ratio por la velocidad, y 1 - el momento es lo que se multiplica por el gradiente. Con el gradiente entonces vamos a actualizar la velocidad, y con eso el parámetro. Entonces con este parámetro un gradiente ruidoso solo modifica la velocidad pero no toda la tendencia, haciendo el proceso más directo y rápido. Un momento muy grande hace que cada gradiente es menos importante, sino que la tendencia pese más. Uno demasiado grande puede causar que te estanques en la optimización, y uno muy pequeño lleva a que no ayude mucho y siga siendo ruidoso. 
> En resumen, la optimización se supone que es mejor y más eficiente.
#### 2. Problemas del Momento
> problemas: en realidad la actualización se hace previamente a mirar la tendencia, por lo que surge la idea de calcular el gradiente incluyendo directamente la tendencia a los pesos.
> - Classical Momentum: simplemente sumar tendencia al gradiente calculado solo con el peso.
> - Nesterov Momentum: calcular el gradiente con la tendencia ya incluida, sumada al peso.
> Todo esto está sujeto a los datos y al modelo, no hay nada definitivo.
#### 3. ADAGRAD
> Podemos tener otro problema, que se actualicen los parámetros de maneras muy diferentes, unos mucho y otros muy poco. Esto lleva a la idea de que el learning rate no sea el mismo siempre. Con esto surgen los adaptive learning rates.
> Este tiene un término que es la raíz de la suma cuadrada de todos los gradientes pasados. con lo que nos queda lo que se va a optimizar ese parámetro. Cuanto más se haya optimizado ya, más bajo debería ser el learning rate, y viceversa.
> También se llama velocidad a esta suma cuadrada.
> Con esto AdaGrad recorre una trayectoria de optimización más recta
#### RMSPROP
> En este tipo, es una extensión de AdaGrad, que añade que se puede volver para atrás, por lo que puede disminuir y aumentar el learning rate, ahora ya no es siempre menor. Con la fórmula es si el gradiente es más pequeño que v_t (aunque se de más peso a v_t). Si un parámetro llega a una zona donde no se actualiza, el gradiente se vuelve muy pequeño y por lo tanto el learning rate volvería a subir. Haciendo que pueda salir de mínimos locales. Con Beta 0 es AdaGrad y con Beta 1 es SGD.
#### ADAM
> Este combina el término de momento como el del learning rate adaptativo, esto genera dos términos con dos parámetros, uno actúa en el término del momento, y otro en los learning rates adaptables. Todo esto se juna en una función final. 
> Aparte de esto se añade también algo para arreglar la inicialización de parámetros:
> Se elevan las betas a la iteración actual, conforme pasen las iteraciones va a tender a que el denominador (de estos nuevos parámetros) sea 1, por lo que al principio si se escala más grande, y al final no se reescala. Esto consigue que aunque los pesos iniciales sean muy bajos, la optimización no se ralentice por que la suma de gradientes sea muy baja.
> Aunque este algoritmo sea el "mejor" no significa que si o si vaya a dar mejores resultados que SGD, por lo que es todo una prueba experimental.
> Este tiene dos versiones ADAM y ADAMW, el W es por que incluye un término de los pesos en la función de pérdida imitando regularización L2.
##### PRACTICA 3
> No tocar estos parámetros de optimización hasta tener el modelo bien avanzado porque se supone que ya están bien conseguidos.

### II. Overfitting y Underfitting
#### 1. Balance
> En general lo que pasa con los modelos es que los modelos simples sean underfitting, y cuando empleamos modelos más complejos se tiende al overfitting, que esto hace que la capacidad de generalización baje. Por lo que hay que encontrar un término medio.
> Vamos a tener dos errores:
> - bias -> tenemos un sesgo en el modelo y fallan en las predicciones consistentemente (under)
> - variance -> aprende cada dato sin conseguir generalización (overe)
> Al conseguir disminuir uno, aumentamos el otro, esto se conoce como bias variance trade of.
> Para estabilizarlos hay que conseguir que el modelo no se aprenda los datos "de memoria".
#### 2. Normalización
> Para la prevención de los vanishing y exploding gradients, podemos hacer normalización para conseguir que aunque tengamos datos con valores muy bajos o muy distintos (?)
> Para la detección de estos, podemos ver que la función de perdida se va hacia arriba (con un exploding), y con los vanishing la función de pérdida se queda estática. 
###### 2.1. Batch-Norm
> Vamos a normalizar en el entrenamiento (y no en validacion o test) por canal sobre cada batch. Cuando lleguen en validación nuevas imágenes, se tienen guardados unos valores de media y desviación que se han ido actualizando con running average. 
> Aquí cuanto mayor sea el batch size mejor porque así generaliza mejor en términos de elegir valores representativos de los parámetros.
> Beneficios: escalar bien los inputs (outliers, ...), escalar activaciones según vamos pasando capas para intentar prevenir problemas de gradiente, y a regularizar la red (prevenir overfitting).
> Malo: mezcla la información del gradiente de varios samples, problemas por propagación de NaNs o valores no representativos, se propaga todo, gradiente malo, activación, valores, ...
###### 2.2. Layer-Norm
> Vamos a normalizar todos los canales de un solo batch. Esto tiene sentido para que no tengamos el problema de los NaNs, no se traspasa a otras imágenes. Funciona bien para secuencias.
###### 2.3. Instance-Norm
> Esta se utiliza para otras aplicaciones de cv, y solo se normaliza un canal. Esto quita activaciones outlier en cada canal para poder "mezclar" imágenes. Esto en clasificación no se usa.
###### 2.4. Group-Norm
> Este se utiliza cuando el batch-norm no sirve porque el tamaño del batch es muy pequeño (layer e instance son un caso particular de group: 1 solo grupo y 1 grupo por canal), esto sirve para coger x canales del grupo.
> Este es más estable que instance-norm (como todos).
#### 3. Donde añadir
###### 3.1. Opción A
> Convolución -> Normalización -> ReLU
> Esto tiene le problema de que si muchos valores son negativos, después de la ReLU esos valores se vuelven 0 y se pierde la ~mitad de la información.
###### 3.2. Opción B
> Normalización -> Convolución -> ReLU
> Aquí se evita el problema de que directamente la mitad de la información se vuelva nula

AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
