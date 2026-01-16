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



### V.
#### 1.


### VI. PyTorch API