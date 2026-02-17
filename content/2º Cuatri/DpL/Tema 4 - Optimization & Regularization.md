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