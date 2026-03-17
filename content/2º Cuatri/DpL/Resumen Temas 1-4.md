## Tema 1 - Frameworks
### I. Python
#### 1. Introducción
> En python vamos a trabajar con paquetes o módulos, con la siguiente estructura:
```text
package/
|-- __init__.py
|-- moduleA.py
|-- subpackage1/
	|-- __init__.py
	|-- moduleX.py
	|-- moduleY.py
|-- subpackage2/
	|-- __init__.py
	|--moduleZ.py
```
> También será obligatorio formatear bien el código en PEP-8 (guía de buen estilo de código), que consiste en: documentar correctamente las funciones (DocStrings); tipar correctamente las variables; y declarar correctamente a variables, funciones/métodos, y clases (minúsculas/mayúsculas, guiones bajos, etc). Para comprobar esto usaremos `my[py]` para el tipado de variables, y `Black` para el formateo del código.
#### 2. Diferentes Recursos
##### 2.1. POO
> En este tipo de programación podemos ver diferentes tipos de métodos:
> - Métodos de Instancia: tienen la referencia `self`, operan a nivel de instancia (cada instancia es independiente), y se ejecutan con `class_instance.instance_method()`.
> - Métodos de Clase: van con el decorador `@classmethod` y tienen la referencia `cls`, operan a nivel de clase (todas las instancias contribuyen), y se ejecutan con `class.class_method()`.
> - Métodos Estáticos: van con el decorador `@staticmethod` y no tienen ni referencia `self` ni `cls`, operan a nivel fuera de clase y de instancia, y se ejecutan con `class.static_method()`.
##### 2.2. Callable Objects
> Son clases que pueden ser llamadas como si fueran una función. Requieren de la implementación de un `__call__(self)` para poder ser llamados desde fuera.
##### 2.3. Iteradores
> Implementan los métodos `__iter__()` y `__next__()` para poder recorrer una secuencia. 
##### 2.4. Generadores
> Es un iterador que implementa `yield`, que es como un return pero en vez de salir, para y sigue.
##### 2.5. Excepciones
> Se usan para escapar código que pueda dar fallos y se separa en casos:
```python
try:
	print("Try running this.")
except:
	print("Run this if there is an error above.")
else:
	print("Run this code if there is no error above.")
finally:
	print("Always run this code no matter what.")
```
##### 2.6. Decoradores
> Funciones que añaden funcionalidad extra a otras funciones.

### II. Numpy Arrays
#### 1. Definición
> Representación de objetos en formato lista, pero mucho más eficientes que las listas convencionales de python nativo. Los bucles no se tienen que programar, ya que vienen internos en `numpy` aportando una velocidad mucho mayor.
#### 2. Programación Vectorizada
> Los arrays tienen dimensiones modificables, se pueden hacer múltiples operaciones que se aplican a todos los elementos del array. Existen funciones de agregación como `max, sum, avg, ...`. También tienen **indexación** permite acceder o modificar elementos concretos de un array mediante sus índices, y **slicing** que permite seleccionar un subconjunto o porción del array especificando un rango de posiciones.
#### 3. Indexado y Slicing
> El indexado de los arrays es de un solo elemento (corchete `[]`) y separando por comas los índices de cada dimensión. 
> El slicing de los arrays funciona de la siguiente manera: `[i:j:k, l:m:n, ...]` el primer set corresponde a la _dimensión 0_, el segundo a la _dimensión 1_, y así hasta la _dimensión n_. En cada set, el primer índice corresponde al primer elemento inclusivo que se va a tomar, el segundo índice corresponde al último elemento no inclusivo que se va a tomar, y el tercer índice indica el salto entre elementos.
```python
# 1. Indexado
x = np.array([[10, 20, 30], [40, 50, 60]])
x[1, 2] = 99   
>>> [[10, 20, 30], [40, 50, 99]]

# 2. Slicing
x = np.arange(10)
>>> [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
x[1:7:2]
>>> [1, 3, 5]
```

### III. PyTorch
#### 1. Tensores
##### 1.1. Definición
> Son arrays como los de numpy pero optimizados para deep learning, ya que se pueden cargar en CPU o en GPU para acelerar las operaciones.
##### 1.2. Memoria
> En PyTorch, un tensor se almacena internamente en un **buffer unidimensional de memoria** llamado _storage_, que contiene todos los valores numéricos. La forma (_shape_) del tensor indica cómo se organizan esos valores en dimensiones.
> Para recorrer ese almacenamiento se utilizan los **strides**, que indican cuántas posiciones en memoria hay que saltar para avanzar en cada dimensión del tensor.  
> Por ejemplo, en una matriz de tamaño `(3,3)` el _stride_ es `(3,1)`: avanzar una fila implica saltar **3 posiciones** en memoria, mientras que avanzar una columna implica saltar **1 posición**.
> Además, un tensor puede empezar en una posición concreta del almacenamiento mediante un **offset**, que indica el índice inicial dentro del _storage_.
> Un tensor es **contiguo** cuando sus elementos están almacenados consecutivamente en memoria siguiendo el orden de sus dimensiones (cuando el stride acaba en 1). En caso contrario, puede compartir almacenamiento con otros tensores y no estar organizado de forma contigua. ![[Pasted image 20260315165645.png]]
##### 1.3. Shapes y View vs Clone
> La **shape** indica las dimensiones del tensor, mientras que el **storage** es la memoria donde se guardan realmente sus datos. Una **view** es un tensor con distinta forma o dimensionalidad que **comparte el mismo storage** que el original, por lo que no copia datos ni reserva memoria nueva. Así, `view()` crea una nueva vista sobre los mismos datos, de modo que los cambios afectan a ambos tensores. En cambio, `clone()` crea una **copia independiente** en memoria, por lo que modificar uno no afecta al otro.
##### 1.4. Reshape
> `reshape()` permite cambiar la **shape** de un tensor sin cambiar sus datos. Su funcionamiento es parecido a `view()`, pero es más flexible, ya que puede devolver **una view o una copia** dependiendo de cómo estén organizados los datos en memoria.
> Si el tensor es **contiguo** y la nueva forma puede obtenerse ajustando únicamente los **strides**, entonces `reshape()` devuelve una **view**, sin copiar datos. En cambio, si el tensor es **no contiguo** y la nueva forma requiere reordenar los datos en memoria, `reshape()` crea una **copia** en un nuevo bloque de memoria contiguo.
> Por esta razón, `reshape()` puede resultar ambiguo: a veces comparte almacenamiento con el tensor original y otras veces no. Si se quiere controlar este comportamiento de forma explícita, puede usarse `clone().view()` en su lugar.
> En general, operaciones como `transpose()` pueden hacer que un tensor deje de ser contiguo, y en ese caso un `reshape()` posterior puede necesitar copiar los datos.
##### 1.5. Indexing y Slicing
> En PyTorch, el indexado y el slicing siguen prácticamente la misma sintaxis que en NumPy. El **indexado** permite acceder o modificar elementos concretos mediante corchetes `[]`, separando por comas los índices de cada dimensión. También se pueden usar **índices negativos** para acceder a elementos desde el final.
> El **slicing** funciona como `[i:j:k, l:m:n, ...]`: cada set de índices corresponde a una dimensión del tensor. En cada uno, el primer valor indica el índice inicial inclusivo, el segundo el índice final no inclusivo y el tercero el salto entre elementos. Si en un tensor de varias dimensiones solo se especifica un índice o un slice, este se aplica sobre la **dimensión 0**.
> Como particularidad importante en PyTorch, muchas operaciones de indexado y slicing devuelven una **view** del tensor original, es decir, un tensor que puede compartir el mismo almacenamiento en memoria.
##### 1.6. BroadCasting
> Esta técnica de pytorch permite realizar operaciones `element wise` entre tensores aunque no tengan las mismas dimensiones, haciendo que los tensores más pequeños se reescalan automáticamente para ello.
> Sigue una serie de reglas:
> - Empieza comparando las dimensiones finales.
> - Las dimensiones deben ser iguales o una de ellas debe ser 1.
> - Las dimensiones que faltan se consideran de tamaño 1. 
> 
> ![[Pasted image 20260315165748.png]]
##### 1.7. Operaciones In-Place 
> Este tipo de operaciones modifican los datos del tensor original. Se suelen identificar con un `_` al final, como con `add_()` o `sub_()`. Estas evitan crear un nuevo tensor nuevo para ahorrar memoria y reducir el coste computacional. 
> Los puntos a tener en cuenta son:
> - Pueden sobrescribir datos de forma inesperada.
> - Deben usarse con cuidado si el tensor original se necesita en otra parte.
> - Las operaciones no in-place son más seguras a la hora de depurar y reutilizar datos.
```python
# 1. Not In-Place
prev_id = id(Y)
Y = Y + X
assert(id(Y), prev_id)
>>> False

# 2. In-Place
prev_id = id(X)
X += Y
assert(id(X), prev_id)
>>> True
```
##### 1.8. From Numpy Array to Torch Tensor
> Tenemos 3 formas diferentes de hacerlo:
> - **`from_numpy()`:** Crea un tensor, directamente a partir de un array de numpy, que comparte memoria con el array (no se copian los datos), por lo que cambios en el array se reflejan en el tensor, y viceversa.
> - **`tensor()`:** Crea un tensor a partir de distintos tipos de datos (listas o arrays de numpy). Siempre copia los datos, creando un tensor nuevo, por lo que los cambios en los datos originales no afectan al tensor ni viceversa.
> - **`as_tensor()`:** Convierte distintos tipos de datos (listas o arrays de numpy), en un tensor que comparte memoria solo si el origen es un array de NumPy y el tipo de dato coincide y en caso contrario, hace una copia de los datos.
#### 2. Optimización de Redes Neuronales
> Para obtener un buen ajuste, el error de entrenamiento debe minimizarse y ser similar al error de test; es decir, hay que minimizar el error de test teniendo en cuenta lo siguiente:
> - Si el error de test >> error de entrenamiento → error de alta varianza.
> - Si el error de entrenamiento ≈ error de test >> 0 → error de alto sesgo.
> 
> Un buen ajuste proviene de una buena elección de los hiperparámetros del modelo. Queremos elegir aquellos hiperparámetros que minimicen el error de test.
> Sin embargo, no podemos conocer el error de test durante el proceso de entrenamiento, por lo que se estima mediante **validación cruzada** para optimizar los hiperparámetros. Para cada partición, se entrena un modelo con una combinación dada de hiperparámetros. En general, las redes neuronales se entrenan usando alguna variante del **descenso por gradiente (GD)**. ![[Pasted image 20260315171418.png]]
> ![[Pasted image 20260315172039.png]]
> ![[Pasted image 20260315171731.png]]
#### 3. Funcionalidades y Mecánicas de PyTorch
##### 3.1. Autodiff-Autograd
> La **diferenciación automática** es una técnica utilizada para calcular gradientes (derivadas parciales) de tensores de forma eficiente.
> En PyTorch, `torch.autograd` sigue las operaciones realizadas sobre tensores que tienen `requires_grad=True`.
> Los gradientes se calculan mediante **retro-propagación** a través de las operaciones registradas, en lugar de derivar y programar manualmente las derivadas. ![[Pasted image 20260315173237.png]]
##### 3.2. Grafo Computacional
> Es un **grafo acíclico dirigido (DAG)** en el que cada nodo corresponde a una operación o a un tensor. Cuando realizas operaciones sobre tensores con `requires_grad=True`, PyTorch construye este grafo de forma interna. Tiene `leaf nodes` que son el inicio (no tienen nada antes, tanto inputs como pesos). Internamente se guarda la derivada de cada bloque en esta estructura, y con la regla de la cadena se calcula de forma backward el resultado del gradiente.
> ![[Pasted image 20260315174115.png]]
##### 3.3. Forward y Backward
> - **Forward Pass:** es el proceso de pasar los datos de entrada a través de la red (serie de operaciones) para obtener la salida o predicción. Durante este proceso, pytorch almacena resultados intermedios para utilizarlos posteriormente en el backward pass.
> - **Backward Pass:** es el proceso mediante el cual, a partir del error o función de pérdida, se calculan los gradientes de esa salida respecto a los parámetros del modelo. Durante este proceso, pytorch recorre en sentido inverso el grafo computacional construido en el forward pass y aplica la regla de la cadena para obtener las derivadas parciales de cada operación. Los resultados intermedios almacenados durante el forward pass se utilizan ahora para poder calcular esos gradientes de forma eficiente. 
>   Por último, el backward solo se puede llamar desde un escalar, por un tema de dimensiones, ya que habría varias derivadas parciales en vez de una única en cada iteración. Si el resultado final son varios elementos, se unifican haciendo una suma ponderada o similar para reducirlo.  ![[Pasted image 20260315174721.png]]![[Pasted image 20260315174746.png]]
##### 3.4. Gradiente de un Tensor
> En pytorch, un tensor puede almacenar su **gradiente** en el atributo `.grad` (que no se reinicia después de cada iteración), siempre que tenga activado `requires_grad=True`. Al crear este tipo de tensores, el gradiente es inicialmente `None`, y solo se calcula cuando se ejecuta la retro-propagación con `.backward()`.
> Si un tensor se obtiene a partir de operaciones sobre otros tensores, pytorch guarda en `grad_fn` la **función** que lo generó dentro del grafo computacional. En cambio, si el tensor ha sido creado directamente por el usuario, entonces `grad_fn` es `None`. Por defecto, `.backward()` espera una **salida escalar**. Si la salida no es escalar, es necesario proporcionar un tensor de gradientes que indique cómo contribuye cada componente al gradiente final; en este caso, pasar `gradient=torch.ones(len(y))` es equivalente a aplicar `y.sum().backward()`.
> Además, pytorch **no reinicia automáticamente** los gradientes: cuando se calcula un nuevo gradiente, este se acumula sobre el valor anterior. Por eso, si se quiere volver a calcular desde cero, hay que resetearlos explícitamente con `.grad.zero_()`.
> Generalmente no se permiten in-place operations con grafos porque podemos modificar un aspecto que cambia la derivada.
> Por último, `detach()` crea un nuevo tensor que **deja de estar conectado al grafo computacional**, por lo que ya no será seguido por `autograd` ni participará en el cálculo de gradientes. Aun así, el tensor desacoplado comparte el mismo _storage_ que el original, por lo que cambios _in-place_ en uno pueden verse reflejados en el otro.
##### 3.5. Acceso y Flujo de los Gradientes
> En pytorch, por defecto los gradientes se almacenan solo en los **leaf tensors**, es decir, en los tensores hoja del grafo computacional. Los tensores intermedios o **non-leaf tensors**, que son el resultado de operaciones sobre otros tensores, no guardan su gradiente en `.grad` salvo que se indique explícitamente con `.retain_grad()`.
> Además, las operaciones **in-place** no están permitidas durante el cálculo de `.backward()` cuando interfieren con la construcción correcta del grafo, ya que al no crear nueva memoria pueden provocar errores o inconsistencias en el cálculo de gradientes.
> Si se quiere **detener el flujo de gradiente** en un tensor intermedio, no se debe usar `.requires_grad_(False)` sobre un **non-leaf tensor**. En su lugar, hay que usar `.detach()`, que separa ese tensor del grafo computacional y evita que los gradientes sigan propagándose a través de él.
> Por último, pytorch permite **personalizar el flujo de gradientes** mediante `torch.autograd.Function`, definiendo manualmente las funciones `forward()` y `backward()`. Esto permite controlar de forma explícita cómo se calcula la salida y cómo se propagan los gradientes en operaciones personalizadas.
##### 3.6. Maneras de Trabajar con/sin Gradientes
> En pytorch, el modo por defecto es trabajar **con gradientes**, de manera que las operaciones sobre tensores con `requires_grad=True` se registran en el grafo computacional para poder usar después `.backward()`.
> Para trabajar **sin gradientes**, puede usarse `torch.no_grad()`, que desactiva temporalmente el cálculo de gradientes dentro de su ámbito. Esto evita registrar operaciones en el grafo, acelera la **inferencia** y reduce el uso de memoria. Puede usarse como **context manager** (`with torch.no_grad():`) y como **decorador** (`@torch.no_grad()`).
> Una opción todavía más eficiente es `torch.inference_mode()`, que también desactiva el cálculo de gradientes, pero además evita el seguimiento de la historia computacional y el **version   tracking**, reduciendo aún más la sobrecarga. Por eso está especialmente pensado para **inferencia**, evaluación del modelo y procesamiento de datos. También puede usarse como **context manager** o decorador.
> Si en algún punto se necesita volver a activar explícitamente el cálculo de gradientes, puede usarse `torch.enable_grad()`, que re-habilita el autograd dentro de su ámbito. Suele emplearse junto con `no_grad` o con otros mecanismos de control del autograd.
> En resumen, el modo **default** se usa normalmente en el _forward pass_ de entrenamiento; `no_grad` resulta útil cuando no se quiere registrar operaciones pero los tensores creados todavía pueden usarse más adelante en modo gradiente; e `inference_mode` es la opción más eficiente para evaluación e inferencia, aunque más restrictiva. ![[Pasted image 20260315181348.png]]
#### 4. Implementaciones Prácticas
##### 4.1. Modules
> En pytorch, **`nn.Module`** es la **clase base** para todos los módulos de redes neuronales. Proporciona una estructura conveniente para **definir y organizar capas**, **registrar automáticamente parámetros** para su optimización y mover el modelo entre **CPU y GPU** mediante `.to(device)`.
> El patrón habitual consiste en definir la arquitectura en `__init__()`, llamando primero a `super().__init__()`, y declarando ahí los **submódulos** de la red, como capas `Linear`, `Conv2d` u otras. Después, en `forward()`, se especifica cómo fluye la entrada a través de esos submódulos para producir la salida.
> Un modelo puede implementarse creando una clase que herede de `nn.Module`. Por ejemplo, en un MLP se definen sus capas en `__init__()` y en `forward()` se encadenan las operaciones necesarias para obtener la salida.
> Cuando las capas se aplican simplemente **una detrás de otra**, puede utilizarse un modelo secuencial mediante `torch.nn.Sequential`, que organiza una secuencia de módulos ejecutados en orden.
> Además, pytorch permite **personalizar completamente el método `forward()`**, incluyendo reutilización de capas, uso de parámetros constantes y estructuras de control como condicionales o bucles. Esto da flexibilidad para construir arquitecturas más complejas que una simple secuencia lineal de capas.
##### 4.2. Parameters
> En pytorch, un **`Parameter`** es una subclase de `Tensor` diseñada para usarse dentro de `nn.Module`. Cuando se asigna como atributo de un módulo, queda **registrado automáticamente como parámetro** del modelo, por lo que aparecerá en `model.parameters()` y podrá ser optimizado, por ejemplo, mediante un optimizador. En cambio, un tensor normal asignado como atributo no se registra de esta forma.
> Los `Parameter` se utilizan para representar los **parámetros aprendibles** del modelo, como los **pesos** y **bias** de capas `Linear`, `Conv2d`, etc. Cada parámetro tiene asociados sus valores numéricos y también su gradiente, accesible mediante el atributo `.grad`.
> Para inspeccionar los parámetros de un modelo, puede utilizarse `state_dict()`, que devuelve un diccionario de python que asocia cada parámetro (y también los _buffers_ del modelo) con su tensor correspondiente. Este mecanismo también existe en los optimizadores, donde `optimizer.state_dict()` almacena tanto hiperparámetros como estados internos del optimizador. Por ello, `state_dict()` es fundamental para **guardar y cargar modelos**.
> En modelos definidos con `Sequential`, se puede acceder a una capa por índice y consultar sus parámetros con `.state_dict()`. Además, para acceder a todos los parámetros de un módulo de una vez puede usarse `.named_parameters()`, que devuelve pares **(nombre, parámetro)**.
> En resumen, los `Parameter` son los tensores que contienen los valores entrenables del modelo y que pytorch registra automáticamente para su seguimiento, inspección y optimización.
##### 4.3. Inicializaciones
> En pytorch, la **lazy initialization** aplaza la forma y la inicialización de los parámetros hasta que haya suficiente información disponible. En capas como `nn.LazyLinear`, los pesos y bias quedan inicialmente como **no inicializados**.
> Esto es útil cuando la dimensión de entrada **no se conoce al crear el modelo**. En el primer `forward()`, pytorch **infiere automáticamente** esa dimensión e inicializa los parámetros. Antes de eso aparecen como `UninitializedParameter`; después, ya tienen su forma definitiva.
##### 4.4. Guardar Tensores
> En pytorch, `torch.save()` permite **serializar y guardar** objetos como tensores, diccionarios o modelos completos. El guardado puede hacerse en una **ruta de archivo** o en un **buffer en memoria**, y posteriormente recuperarse con `torch.load()`. Este mecanismo es útil para hacer **checkpointing** y para almacenar pesos o tensores intermedios.
> Para guardar un modelo, puede usarse su `state_dict()`, que es la opción recomendada en las diapositivas: se guarda con `torch.save(model.state_dict(), PATH)` y después se carga con `model.load_state_dict(torch.load(PATH, weights_only=True))`.
> También puede guardarse el **modelo completo** con `torch.save(model, PATH)` y recuperarse con `torch.load(PATH, weights_only=False)`, aunque en ese caso debe existir la definición de la clase del modelo al cargarlo.
> Para salir del prototipado y pasar a despliegue, pytorch distingue entre **Eager Mode** y **Script Mode**. `TorchScript` permite convertir el modelo a un formato más estático y portable, mediante `torch.jit.script(model)` o `torch.jit.trace(model, example_inputs)`, y después guardarlo directamente con `.save()` y cargarlo con `torch.jit.load()`.
> Además, en PyTorch 2.x aparece `torch.compile`, orientado a **mejorar el rendimiento** en entrenamiento e inferencia manteniendo la semántica de Eager Mode. Según las diapositivas, `torch.compile` está enfocado en velocidad dentro de python, mientras que **TorchScript** está más orientado a **despliegue y portabilidad** en entornos sin python.
##### 4.5. Device
> En pytorch, un tensor se almacena en un **device**, normalmente **CPU** o **GPU**, y puede moverse entre dispositivos con el método `.to(device)`. La GPU suele utilizarse para acelerar operaciones matriciales, mientras que la CPU es más adecuada para tareas secuenciales o con menor paralelismo. La localización de un tensor puede consultarse mediante su atributo `.device`.
> Cuando se trabaja con varios dispositivos, cada uno tiene su **propio espacio de memoria**. Por eso, para operar con varios tensores a la vez, **todos deben estar en el mismo device**. Si un tensor está en otra GPU, hay que copiarlo explícitamente antes de operar con él. En consecuencia, los dispositivos **no comparten memoria automáticamente**, y los datos deben moverse al lugar donde se realiza el cálculo.
##### 4.6. Data
> En pytorch, la gestión de datos se organiza principalmente mediante las clases **`Dataset`** y **`DataLoader`**. Primero, se define una clase `Dataset`, que indica cómo se almacenan y recuperan las muestras; después, a partir de ella, se crean los conjuntos de entrenamiento, validación y test, y finalmente se instancian los `DataLoader` correspondientes.
> En un `Dataset` suelen definirse tres métodos principales: `__init__()`, para guardar los datos o las rutas a los ficheros; `__len__()`, para indicar el número de muestras; y `__getitem__()`, para especificar cómo recuperar la entrada y la salida asociadas a un índice concreto.
> El **`DataLoader`** se encarga de extraer los datos del `Dataset` y suministrarlos al modelo en forma de **batches** durante el entrenamiento o la validación. Cada vez que se itera sobre él, devuelve un lote de datos.
> Entre sus argumentos más importantes están `batch_size`, que fija el tamaño del lote; `shuffle`, que indica si se mezclan las muestras en cada época; `num_workers`, que controla cuántos subprocesos se usan para cargar los datos; y `drop_last`, que decide si se descarta el último batch cuando queda incompleto. Si `drop_last=False`, el último lote puede ser más pequeño.
##### 4.7. Loops
> En pytorch, el entrenamiento de un modelo se organiza mediante un **training loop** y, normalmente, un **validation loop**. En el bucle de entrenamiento, primero se pone el modelo en modo entrenamiento con `model.train()`, se pasan los datos al **device** correcto, se obtienen las salidas del modelo, se calcula la pérdida, se reinician los gradientes con `optimizer.zero_grad()`, se ejecuta la retro-propagación con `loss.backward()` y finalmente se actualizan los parámetros con `optimizer.step()`.
> En el **validation loop**, el modelo se pone en modo evaluación con `model.eval()` y se usa `torch.no_grad()` para desactivar el cálculo de gradientes. En este bucle solo se pasan las entradas por el modelo y se calcula la pérdida o las métricas, pero **no se optimiza el modelo ni se calculan gradientes**.
> En resumen, el bucle de entrenamiento sirve para **actualizar los parámetros** del modelo, mientras que el de validación sirve para **evaluar su rendimiento** sin modificarlo.
##### 4.8. Modos
> En pytorch, `model.train()` pone el modelo en **modo entrenamiento**, activando comportamientos específicos de esta fase. Por ejemplo, **Dropout** desactiva aleatoriamente neuronas como regularización y **BatchNorm** actualiza sus estadísticas usando el batch actual.
> En cambio, `model.eval()` pone el modelo en **modo evaluación**, desactivando esos comportamientos de entrenamiento. En este modo, **Dropout** deja de introducir aleatoriedad y **BatchNorm** usa las estadísticas acumuladas, produciendo salidas más estables y consistentes para inferencia.
> Además, durante evaluación suele usarse `torch.no_grad()`, que evita calcular gradientes, reduce el uso de memoria y acelera el cómputo. Por tanto, `model.eval()` y `torch.no_grad()` **no son lo mismo**: `eval()` cambia el comportamiento de ciertas capas, mientras que `no_grad()` desactiva el cálculo de gradientes.
##### 4.9. TensorBoard
> **TensorBoard** es una herramienta de visualización, originalmente asociada a TensorFlow, pero que también puede utilizarse en PyTorch. Permite mostrar **paneles interactivos** con métricas del entrenamiento, como la **loss**, la **accuracy** y otras magnitudes relevantes, facilitando el seguimiento y análisis del comportamiento del modelo.

---

## Tema 2 - Foundations of Neural Networks
### I. Introduction
#### 1. Idea y Contexto
> Las **redes neuronales artificiales** surgen como una inspiración simplificada del funcionamiento de las neuronas biológicas. La idea básica es combinar varias **entradas** con unos **pesos**, aplicar una suma y después una **función de activación** para obtener una salida.
> Un único perceptrón o neurona artificial puede modelar relaciones sencillas, pero resulta limitado cuando el problema es más complejo. Por ello, se combinan varias neuronas en una **red neuronal artificial**, capaz de representar comportamientos más ricos y aproximar funciones más complejas.
> En este tema se parte de la neurona artificial como bloque básico para entender cómo se construyen redes neuronales y por qué estas permiten resolver problemas que un único modelo lineal no puede capturar.

### II. FeedForward Layer
#### 1. Multi Layer Perceptron (MLP)
> Un **Multi Layer Perceptron (MLP)** es una red neuronal formada por una **capa de entrada**, una o varias **capas ocultas** y una **capa de salida**. Cada capa aplica una transformación lineal a sus entradas y, después, una **función de activación** para introducir no linealidad.
> La idea principal es que una sola neurona o una sola transformación lineal tienen capacidad limitada, mientras que al **combinar varias neuronas en capas** se pueden modelar relaciones más complejas entre las variables de entrada y la salida. En general, las capas ocultas suelen usar activaciones no lineales, mientras que la capa de salida utiliza una activación acorde al problema.
#### 2. Capa y Detalles
> Una **feedforward layer** o capa densa recibe un vector —o un batch de vectores— y aplica una **transformación lineal** de la forma `Z = XW^T + b`, donde `X` representa la entrada, `W` los pesos y `b` el sesgo. Después, a ese resultado se le aplica una **función de activación** elemento a elemento: `A = φ(Z)`.
> El número de parámetros de la capa viene dado por los **pesos** y los **biases**, es decir, `d_in × d_out + d_out`, donde `d_in` es la dimensión de entrada y `d_out` el número de neuronas de salida. Entre las activaciones más habituales aparecen **sigmoid**, **ReLU**, **tanh** y **softmax**. Además, la inicialización de los pesos y el proceso de entrenamiento son importantes para que la red aprenda correctamente.

### III. Regression & Classification
#### 1. Regression

> La **regresión** es un problema fundamental de **aprendizaje supervisado** en el que se busca **predecir valores continuos** a partir de unas variables de entrada. Dado un vector de características $x \in \mathbb{R}^d$, el objetivo es aprender una función $f:\mathbb{R}^d \to \mathbb{R}$. En su versión más simple, la **regresión lineal** modela esta relación como una combinación lineal de las entradas: $\hat{y} = \mathbf{w}^\top \mathbf{x} + b$.  
> En esta formulación, los parámetros a aprender son los **pesos** $\mathbf{w}$ y el **sesgo** $b$. Para ajustar el modelo se define una función de pérdida, en estas diapositivas el **error cuadrático medio (MSE)**: $$L(w,b)=\frac{1}{2n}\sum_{i=1}^{n}(\hat{y}^{(i)}-y^{(i)})^2$$y el objetivo de optimización consiste en encontrar los valores $w^*, b^*$ que minimizan dicha pérdida. 
> La regresión lineal puede resolverse de dos formas principales. Por un lado, existe una **solución analítica cerrada** basada en ecuaciones matriciales, $\mathbf{w} = (X^\top X)^{-1}X^\top y$, aunque su coste puede hacerla poco práctica cuando la dimensión es grande. Por otro lado, puede resolverse de forma **iterativa** mediante **descenso por gradiente**, actualizando los parámetros con las reglas $w←w−η∂L∂ww \leftarrow w - \eta \frac{\partial L}{\partial w}w←w−η∂w∂L​ y b←b−η∂L∂bb \leftarrow b - \eta \frac{\partial L}{\partial b}b←b−η∂b∂L$​. Esta segunda opción es la más relevante en Deep Learning, ya que constituye la base del entrenamiento de redes neuronales.
> Conceptualmente, la regresión lineal puede verse como una **red neuronal de una sola capa**. A partir de ahí, al introducir **múltiples salidas** y, sobre todo, al **apilar capas con no linealidades**, se obtienen redes neuronales capaces de modelar relaciones mucho más complejas. Las diapositivas conectan esta idea con el **teorema de aproximación universal**, según el cual una red con suficientes unidades ocultas y una no linealidad adecuada puede aproximar cualquier función continua.


### IV. Loss Functions & Non Linearities




### V. Initialization & Optimization



