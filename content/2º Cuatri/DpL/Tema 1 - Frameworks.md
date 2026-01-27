### I. Python
#### 1. Pros y Contras
> Es fácil, intuitivo y muy flexible a los cambios, pero no se compila lo que hace que sea muy lento. Usamos python como interfaz de librerías que están programadas en otros lenguajes para ser más rápidas.
#### 2. Como Usarlo
> Hay que ejecutar todo como módulos, los notebooks los deberíamos de dejar aparte ya que no puedes debuguear y limita otras funcionalidades, solo lo usaremos en el caso exploratorio.
#### 3. Módulos
> Estructura mínima que ejecutamos, se pueden apilar entre sí para construir unos más grandes. Por ejemplo, en las prácticas vamos a tener una carpeta src con cada módulo de la práctica. Importante para convertir una carpeta en un módulo hay que crear un *`__init__.py`*, que se queda vacío, solo sirve para modificar imports. 
> La forma más fácil es un *import absoluto*, que es la que vamos a hacer la mayoría de veces.
> Para tratar un proyecto como un módulo tenemos que abrir la carpeta madre, no una superior, por ejemplo si tenemos *`Labs/Lab1/Modulos.py`*, debemos abrir **`Lab1` y no `Labs`** porque Lab1 no es un módulo ejecutable sino la carpeta madre contenedora de los módulos.
> Como norma los archivos finales que se van a ejecutar van a estar ubicados en `Lab/src` como en el siguiente ejemplo: *`Lab/src/main.py`* se ejecuta con *`python - m src.main`*
```python
# src/main.py
def main():
	...
	
if __name__ == "__main__":
	main()
```
#### 4. Type Hinting
> Se usa para especificar los tipados de variables del código, inputs y outputs de las funciones, etc (como en C#)
![[Pasted image 20260116180047.png]]
> Esto ayuda a detectar errores antes de ejecutar el programa, y también fuerza a la buena práctica de no cambiar el tipo de las variables ya definidas, creando variables nuevas del nuevo tipo deseado. Aunque haya veces que no sea necesario es recomendable ponerlo en la mayor cantidad de variables posibles. 
> Para comprobar los tipos usaremos *`my[py]`* con el comando `mypy --cache-dir=/dev/null`.
#### 5. Pep-8 Coding
> Usando `Black` se formateo el código para dejarlo "bonito" y bien formateado, vamos a tener un archivo `pyproject.toml` para que Black siga unas reglas fijas de formateo (esta es otra razón por la que abrir Lab1 y no Labs)

> [!warning] Warning
>  Cuidado con los entornos de anaconda, mejor usar los de python con 
>  `python -m venv nombre` 
#### 6. Tipos de Métodos de Clases
###### 6.1. Instance Methods
> Métodos normales que tienen la referencia `self`. Se ejecutan con `class_instance.method()`.
###### 6.2. Static Methods
> Métodos que no requieren de una instancia para ser llamados. Se ejecutan con `Class.method()`
###### 6.3. Class Method
> Métodos que RELLENAR
#### 7. Callable Objects
> Requieren de la implementación de un `__call__` para poder ser llamados desde fuera.
#### 8. Excepciones
> Try-Except-Else-Finally: 
> - Try: Se *intenta* ejecutar A
> - Except: Si no se puede, se ejecuta B
> - Else: Si no se ha ejecutado B, se ejecuta C
> - Finally: Siempre se ejecuta D
#### 9. Iteradores
> a
#### 10. Generadores
> a
#### 11. Decoradores
> a

### II. Git
#### 1.


### III. Arrays
#### 1. Definición
> Representación de objetos en formato 'lista', pero mucho más eficientes que las listas convencionales de python nativo. Los bucles no se tienen que programar, vienen internos en `numpy` aportando una velocidad mucho mayor.
#### 2. Programación Vectorizada
> Los arrays tienen dimensiones modificables, se pueden hacer múltiples operaciones que se aplican a todos los elementos del array. Existen funciones de agregación como `max, sum, avg, ...`. También tienen `indexación` para acceder o modificar uno o varios elementos del array, que no hay que confundir con `slicing` que captura un "trozo" del array. 
#### 3. Indexado Booleano
> A partir de un array de `n` dimensiones se puede crear una `máscara booleana` que devuelve un array, de las mismas dimensiones que el original, rellenado con `True|False` según una condición impuesta (ej. valor > 3).
#### 4. BroadCasting
> En las operaciones de arrays, los operandos no tienen que tener las mismas dimensiones, la propia operación se encarga de reescalar el segundo para devolver la dimensión correcta. 
> Pero hay que tener mucho cuidado con no especificar las dimensiones del objeto que se va a reescalar para que lo haga bien (ej. (100) se convierte en (1, 100) no en (100, 1))
### IV. PyTorch Introduction
#### 1. Instalación
> Seguir la guía de las diapos para que no pete.
#### 2. Tensores
> Son unos arrays "aumentados". Para una inicialización vacía mejor usar `empty`. También tienen métodos de indexado y slicing como los arrays.
#### 3. Almacenamiento
> Mejor usar view siempre para saber qué estamos haciendo con el tensor. Pueden almacenarse de manera contigua o no. Los contiguos almacenan la última dimensión toda seguida. Esto se modela con un `stride`, que marca los saltos a la siguiente dimensión, por ejemplo en una matriz `3x3` su stride es `(3, 1)` porque para cambiar de fila es un salto de 3 elementos y para cambiar de columna es un salto de 1 elemento.
#### 4. View vs Clone
> View solo se puede cuando el tensor es contiguo (stride terminado en 1: `(..., 1)`).
> Clone crea una copia del objeto en una dirección de memoria nueva.
> Basic slices: son views, que cambian el tensor original ya que comparten memoria.
> Advanced slices: son clones, que no cambian el tensor original ya que copian el original en otro sitio de la memoria.
#### 5. Contigüidad
> Esto es que en la última dimensión, los elementos vayan seguidos, lo que facilita y acelera realizar operaciones.
#### 6. In-Place Operations
> ejemplo base python: 
```python
# Operación normal
a = init
a = a + b # crea un nuevo objeto (menos eficiente)

# Operación In-Place
a = init
a += b # actualiza el objeto ya existente (más eficiente)
```
#### 7. Tensores de Numpy vs PyTorch
> La memoria es compartida, si se cambia el tensor se cambia el array.
> En pytorch hay que tener cuidado con el import, que es mejor poner `torch.tensor()` con _tensor_ en minúsculas, para que mantenga el tipo de dato inicial siempre.
#### 8. AutoDiff y AutoGrad
> - Forward: como se predice el ouptup.
> - Backward: como se consigue el gradiente desde el output hacia atrás. 
> - Grafo Computacional: es la estructura que se construye automáticamente, y que será luego usada por el backward. Tiene `leaf nodes` que son el inicio (donde termina el backward), de normal no se necesitan gradientes intermedios. Todos los nodos que no tienen nada antes (tanto inputs como pesos) son nodos hoja. Una vez tenemos el mapa hay varias maneras, hacer las operaciones de alante hacia atrás o al revés. Internamente se guarda la derivada de cada bloque, y con la regla de la cadena se calcula de forma backward (más eficiente que forward por las dimensiones) el resultado del gradiente.
> - IMPORTANTE: el backward solo se puede llamar desde un escalar, también por tema de dimensiones, ya que habría varias derivadas parciales en vez de una única en cada iteración. Si el resultado final son varios elementos, se unifican haciendo una suma ponderada o algo del estilo para reducirlo a un escalar. Hay funciones que hacen automáticamente esta ponderación pero también se puede hacer a mano.
> 
> Los tensores tienen una variable asociada `.requires_grad_(True)` (que acabe en `_` quiere decir que modifica el tensor original), que activa su reconocimiento en el backward. Su gradiente se calcula en `.grad`, que NO se borra por defecto después de la iteración, ya que como el gradiente se acumula se estaría considerando un valor de otra iteración con los pesos actuales que pueden ser distintos y haciendo que el valor obtenido sea erróneo.
> También tienen una grad function `grad_fn` que indica la función aplicada en ese instante, que sirve para mirar de donde viene y que operación tiene que hacer (en el primero es None xq es un nodo hoja).
> Si queremos sacar algo del grafo computacional se usa el `detach` que crea un tensor separado del grafo actual, creando un nuevo nodo hoja de un nuevo grafo computacional. Por ejemplo, para pasar un tensor a numpy hace falta hacer detach.
> Los hijos de un nodo hoja que tiene el `requires_grad` en `True` también lo tienen activado.
> **POSIBLE PREGUTNA: QUE HACE REQUIRES_GRAD : EVITAR QUE SE CALCULE O EVITAR QUE SE GUARDE -> EVITAR QUE SE GUARDE PORQUE SI QUE SE CALCULA PERO NO LO DEVUELVE.**
> También está `retains_grad` que si está en `True` hace que no se borren los gradientes intermedios  y los guarda, se lo pones al final (de la derecha) y se auto pone en el resto.
> No se permiten in-place operations con grafos porque podemos modificar un aspecto que cambia la derivada (en el += no afecta? pero en el \*= si). -- Mirar ejemplos en las diapos de cuando si o cuando no --. 
> Ejemplo de autograd diapo 95

#### COSA DE LA PRACTICA
> en los constructores hay que poner super inits, parametros: torch.nn.parameter (con random), mejor inference_mode que grad no sé que, copiar la linea de la gpu y pasar todo a la gpu en bucle training o bucle test. dataset y dataload, dataset -> carga cada elemento, dataload -> batches, siempre con 3 métodos (diapo "DATASET"). DataLoader, para entrenar de batches en batches, le pasamos el dataset y le damos el tamaño y el shuffle (en train siempre true), num worker (4 y ya), drop last para quitar batches incompletos. copiar el training loop.

### V. PyTorch API
#### 1. Modules
> Un module (`nn.module`) es un callable en el que hay que definir siempre su innit (con un super()) y un forward. No solo los modelos heredan de module, también las funciones de pérdida, en ese caso vamos a ver que el forward aparte de inputs tiene también targets.
#### 2. MLP
> Distintos formas de llamar a las capas: 
> - `nn.module`
> - `torch.nn.functional` -> capas que no necesitan de una clase, cuando se llama a una de esas capas hay que pasarle tanto los inputs como los parámetros. Nosotros no lo vamos a ver, solo lo usamos para las no linealidades.
> Para una secuencia de capas podemos usar `Sequential` para marcar que una va detrás de otra.
#### 3. State Dicts
> Son diccionarios que representan todo lo que tiene guardado el modelo interiormente. Se pueden acceder de varias maneras (funciones de parámetros)
#### 4. Lazy Initialitation
> En este tipo de capas solo vamos a indicamos la dimensión de salida, es un poquito más eficiente. Solo se puede acceder a ellos después de haber hecho una predicción
#### 5. Parámetros del Modelo
> Se guardan en `torch.nn.parameters()` con `nn.Parameter` (que puedes activar o no su gradiente, predeterninado si)
> Preferiblemente usar la `inicialización de xabier`
#### 6. Buffers del modelo
> al cambiar varias cosas del modelo tambien se cambian aqui (cpu a gpu, float a double, ...)
#### 7. Guardar y Cargar Tensores
> se usa `torch.save` poniendo `tensor.pt` (se pone .pt por convención)
> para cargar importante poner `weights_only=True` 
> IMPORTANTE: antes de entregar guardar siempre en la cpu con `tensor.cpu()`
#### 8. Formas de Guardar Modelos
> 1. State Dict `load_sate_dict()`: se guardan los parámetros del modelo, es sencillo, no error, no limitaciones, pero seguimos teniendo que definir el modelo en tiempo de ejecución porque hay que inicializarlo y cargarse los pesos. Se guardan con `torch.save(model.state_dict, PATH)`
> 2. Modelo Entero `load()`: el modelo se guarda con pickle, que es muy inestable porque se fija en la estructura de archivos en vez de en los elementos, está bien para experimentar uno solo. Se guarda con `torch.save(model, PATH)`
> 3. TorchScript `jit.load()`: te da una traza de cómo se ejecuta el modelo, pasamos de eager mode a script mode. Aquí el modelo no se puede debuguear por dentro, pero el modelo funciona en cualquier sitio (tanto a nivel de estructura como a nivel de lenguaje). Se guarda con `torch.jit.script(model)`
#### 9. Cambio del Estado de los Gradientes
> podemos usar 2 estructuras:
> - `with torch.estado_grad():` que todo lo que vaya dentro se actualizará su estado
> - usar un decorador `@torch.estado_grad` antes de una función.
> en `estado_grad()` se puede poner:
> 1. `enable_grad()` ->
> 2. `no_grad` ->
> 3. `inference_mode()` -> si creo un tensor así no se puede activar su gradiente nunca
#### 10. Compilar
> `torch.compile` -> para crear una versión compilada del modelo, que va a ser más rápido. En vez de tener que ejecutar código pytorch, va a intentar crear una versión optimizada en c++ que no se puede debuguear (se guardan los pesos sin compilar). Se usa para que el training sea más corto.
#### 11. Device
> CPU -> pocos nucleos muy potentes para pocas tareas complejas
> GPU -> muchos nucleos normales para muchas tareas
> Al hacer cualquier operación todos los tensores tienen que estar en el mismo device, normalmente al entrenar se pasa el modelo a la gpu y luego los inputs.
#### 12. Dataset y DataLoader
> Nos permiten cargar datos de una manera flexible y genérica.
> Dataset nos dice como cargar cada elemento de nuestros datos, tiene el constructor en el que puedes poner los datos en si, tiene  __ len __ con la longitud de los inputs, get item como tenemos que sacar los elementos en función de indices (en el constructor tiene que ordenarse si no lo está), puede devolver de todo siempre que sea algo numérico int, float o un tensor.
> DataLoader, carga un montón de elementos y de la forma designada por Dataset, en batches, los podemos poner con shuffle, y se puede poner drop_last
#### 13. Loops
> Ponemos tantos elementos como haya en el get item.


### VI. 
