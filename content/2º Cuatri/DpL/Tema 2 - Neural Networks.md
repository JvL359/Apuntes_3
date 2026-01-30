### I. Introducción
#### 1. Neurona
> Inicialmente se inspiraron en las neuronas humanas, que en vez de con impulsos eléctricos, funcionan con inputs. El primer modelo es el `perceptrón` que es la aplicación de una función lineal. Sus ecuaciones son: $y = f(w \cdot X + b)$.
> El primer problema del perceptrón es que no es capaz de resolver un problema no lineal (`XOR`).
> Este problema se resuelve añadiendo una neurona intermedia (capa oculta) con una función no lineal entre una neurona y la otra. 

### II. Capas FeedForward 
#### 1. Definición de Red Lineal
> Una red lineal es un conjunto de capas (neuronas) conectadas entre sí por funciones de activación (no lineales)
> Vamos a tener que los inputs tienen una dimensión `(batch, input_dim)`, que pasan por las capas de la red (lineal -> activación -> lineal ->  . . .), y dan unos outputs de `(batch, output_dim)`.
> Ecuaciones (equivalentes) de la red: $Y = (WX^T + b)^T$ o $Y = XW^T + b$ .

### III. Regresión y Clasificación
#### 1. Regresión Lineal
> Predecir un número, bla bla, función de pérdida: bla bla
#### 2.
> Hay distintos casos, binary classes, multi classes, y multi label (clasificar)
> - binary: sacamos solo un número que si es mayor que un cierto umbral se clasifica como positivo, y si es menor como negativo.
> - multi class: es un vector tan grande como el numero de clases, se predice el mayor de ese vector
> - multi label: igual que binary porque cada predicción es una binaria, pero varias veces.
#### 3. Flatten Input
> Sirve para aplanar (siempre a partir de la dimensión 1 xq la 0 es el batch) un input que tenga más de 2 dimensiones, mejor usar `torch.nn.flatten`.
#### 4. Seudo-Probabilidades
> Los outputs de la última neurona se llaman `logits` (los números previos a la `softmax` también).
> Para simular probabilidades, se escalan los logits a seudo-probabilidades. La sigmoide (fórmula) la usaremos para clasificación binaria, y la softmax (fórmula) para multi clase. Sirven para escalar los datos al rango `(0, 1)`. Aquí también cuidado con a qué dimensión se aplican las funciones.
> Problema de underflow: si el denominador se acerca mucho a 0, el ordenador no detecta la diferencia, lo marca como 0 y entonces le asigna `Nan/inf`, por lo que haremos su integración para pasar las divisiones a restas. Por esto la capa final es lineal.
#### 5. Regresión Logística
> poca cosa

### IV. Funciones de Pérdida
#### 1. Log Likelihood
> no a ful pero saber que para regresión se deriva el MSE, y para clasificación la cross entropy.
> Propiedades Max Log Likelihood:
> - Consistency -> dada una cantidad infinita de datos, con este método se va a encontrar los mejores parámetros
> - Efficiency -> parando las iteraciones en un cierto punto, se habrá mejorado más que con otra medida.
> Condiciones de consistencia:
> - rellenar con diapo
> - rellenar con diapo
#### 2. PyTorch
> En regresión hay:
> - MAE -> no da peso a los outliers de forma significativa, pero no está definido en 0, esto afecta al gradiente, ya que si no está definido en todos los puntos, en el entrenamiento pueden darse saltos y que el modelo se quede atascado y el resultado final será peor que con otra función de pérdida.
> - MSE -> Lo bueno es que está definido en 0, lo malo es que se da un peso muy significativo a los outliers.
> - Huber Loss -> Para hacer una combinación de MAE (bien outliers) y MSE (bien definida), se hace una función a trozos, cerca del 0 se usa el MSE y si no el MAE.
> En clasificación hay:
> - Binary/Label cross entropy
> 	- BCE Loss -> espera los outputs de la sigmoide (0-1)
> 	- BCE with logits -> espera los logits (antes de la sigmoide)
> - Cross entropy -> siempre espera logits (última capa siempre lineal)

### V. No Linealidades
#### 1. Limitaciones
> Mismo que en el primer apartado, si no se ponen no linealidades en realidad por mucha cosa lineal que haya solo hay una neurona, más simple o más compleja.
#### 2. Funciones de Activación
> - Sigmoide: lo malo es la región que define puede hacer que sature el gradiente.
> Al entrenar queremos varianza constante en las activaciones y también en los gradientes.
> 1) varianza de gradientes no constante
> 2) Exploding gradients -> gradientes demasiado grandes, la función de pérdida solo aumenta
>    Vanishing gradients -> gradientes demasiado pequeños por lo que no se actualizan los pesos
> - Tan H: "versión" de la sigmoide más ensanchada
> - ReLU: tiene 2 problemas, más grave que hay un punto no definido, el 0; y no tan grave la Dead ReLU, que todos los ejemplos con los que se quiere entrenar caen en la parte negativa, por lo que después de la ReLU todo es 0 y el gradiente también por lo que esa neurona no se actualiza nunca más. Para solucionarlo podemos: inicializar con cuidado y disminuir el learning rate. Alternativas mejores:
> 	- Leaky ReLU -> La pendiente en el lado negativo no es 0, es un poco negativa (-0.1)
> 	- Parameters ReLU -> se entrena el parámetro de la pendiente también
> 	- ELU -> Tiene una evolución progresiva para que el gradiente esté definido
> - Valor Absoluto: en CV tiene sentido porque no importa tanto el valor si no el contraste
> - Max Out: Se intentó hacer modelos más anchos en vez de más profundos, intentando modelar cualquier función y no tener tanta maraña entre las capas. Esta función en vez de seguir poniendo lineal -> no lineal, coge todas las lineales, coge sus respectivos máximos y luego les aplica la no linealidad. Se libra del catastrophe forgetting 
> Es un poco experimental cuál se acaba eligiendo (prueba y error)
> El shuffle es importante porque si no el modelo se olvida de lo que ha aprendido previamente por intentar aprender otra cosa, con el shuffle va aprendiendo todo poco a poco.

### VI. Inicialización
#### 1. Objetivos
> Conseguir varianza constante en las activaciones y en los gradientes. La inicialización de los pesos es crucial para esto, por ejemplo si inicializamos todo a 0 el gradiente siempre es 0 así que no podemos entrenar; si inicializamos todo constante realmente solo tenemos un parámetro, porque todos se actualizan de la misma manera. 
> Se deben de inicializar con varianza constante, se puede hacer con una normal, random, etc, pero esto tiene un problema que es que no lo garantiza. Por lo que para garantizarlo, la varianza ideal sería `1/input_dim`. Esto da lugar a la inicialización de Xabier: $W ~~ N(0, \frac{2}{d_x + d_y})$ 
> Otra inicialización es la de Kaiming, que tenemos un factor que divide a la mitad el no sé qué, y funciona "mejor" para las ReLU

### VII. Optimización
#### 1. Optimizador
> Elegir `Adam` o `Adam W` para que vaya mejor el modelo. 
#### 2. Descenso de Gradiente
> - Stochastic: Se aplica el descenso a cada elemento del data set, se va ejemplo a ejemplo, entonces el gradiente es muy ruidoso y no es deseable
> - Batch: Se aplica el gradiente a todos los datos a la vez, es más directo pero en algunos casos puede llevar a overfitting.
> - Mini-Batch: Es un punto medio, se coge un conjunto de ejemplos del dataset (p. ej. 64, 128) y se calcula el gradiente de batch en batch.
#### 3. Learning Rate
> poner foto diapo
> Se suele empezar en $10^{-3}$ y de ahí se va variando.
### VIII. Referencias
> Mirar diapo

