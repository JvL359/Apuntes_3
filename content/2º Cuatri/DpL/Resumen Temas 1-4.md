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
> Un tensor es **contiguo** cuando sus elementos están almacenados consecutivamente en memoria siguiendo el orden de sus dimensiones (cuando el stride acaba en 1). En caso contrario, puede compartir almacenamiento con otros tensores y no estar organizado de forma contigua.
##### 1.3. Shapes y View vs Clone
> La **shape** indica las dimensiones del tensor, mientras que el **storage** es la memoria donde se guardan realmente sus datos. Una **view** es un tensor con distinta forma o dimensionalidad que **comparte el mismo storage** que el original, por lo que no copia datos ni reserva memoria nueva. Así, `view()` crea una nueva vista sobre los mismos datos, de modo que los cambios afectan a ambos tensores. En cambio, `clone()` crea una **copia independiente** en memoria, por lo que modificar uno no afecta al otro.
##### 1.4. Reshape
> `reshape()` permite cambiar la **shape** de un tensor sin cambiar sus datos. Su funcionamiento es parecido a `view()`, pero es más flexible, ya que puede devolver **una view o una copia** dependiendo de cómo estén organizados los datos en memoria.
> Si el tensor es **contiguo** y la nueva forma puede obtenerse ajustando únicamente los **strides**, entonces `reshape()` devuelve una **view**, sin copiar datos. En cambio, si el tensor es **no contiguo** y la nueva forma requiere reordenar los datos en memoria, `reshape()` crea una **copia** en un nuevo bloque de memoria contiguo.
> Por esta razón, `reshape()` puede resultar ambiguo: a veces comparte almacenamiento con el tensor original y otras veces no. Si se quiere controlar este comportamiento de forma explícita, puede usarse `clone().view()` en su lugar.
> En general, operaciones como `transpose()` pueden hacer que un tensor deje de ser contiguo, y en ese caso un `reshape()` posterior puede necesitar copiar los datos.
> (Material: _Deep Learning Frameworks_, diapositivas “Reshape”, “Reshape Details (View vs. Copy)”, “Example: Reshape Gives a View” y “Example: Reshape Gives a Copy”)
##### 1.5. Indexing y Slicing
> Rellenar
##### 1.6. BroadCasting
> Rellenar
##### 1.7. Operaciones In-place 
> Rellenar
##### 1.8. From Numpy Array to Torch Tensor
> Rellenar
#### 2. Optimización de Redes Neuronales
> Rellenar
#### 3. Funcionalidades y Mecánicas de PyTorch
##### 3.1. Autodiff-Autograd
> Rellenar
##### 3.2. Grafo Computacional
> Rellenar
##### 3.3. Forward y Backward
> Rellenar
##### 3.4. Gradiente de un Tensor
> Rellenar
##### 3.5. Acceso y Flujo de los Gradientes
> Rellenar
##### 3.6. Maneras de Trabajar con/sin Gradientes
> Rellenar
#### 4. Implementaciones Prácticas
##### 4.1. Modules
> Rellenar
##### 4.2. Parameters
> Rellenar
##### 4.3. Inicializaciones
> Rellenar
##### 4.4. Guardar Tensores
> Rellenar
> Hasta Compile
##### 4.5. Device
> Rellenar
##### 4.6. Data
> Rellenar
##### 4.7. Loops
> Rellenar
##### 4.8. Modos
> Rellenar
##### 4.9. TensorBoard
> Rellenar


