## D2DpL 2. Preliminaries
### I. Visión General del Capítulo
#### 1. Habilidades Previas Necesarias
> Para “sumergirte” en Deep Learning, el capítulo enumera habilidades de supervivencia:
> - i) Técnicas para **almacenar y manipular datos**.
> - ii) Librerías para **ingerir y preprocesar datos** de varias fuentes.
> - iii) Operaciones básicas de **álgebra lineal** aplicadas a datos de alta dimensión.
> - iv) El “mínimo” de **cálculo** para saber en qué dirección ajustar parámetros para reducir la **función de pérdida**.
> - v) Capacidad de **computar derivadas automáticamente** (para “olvidar” gran parte del cálculo).
> - vi) Fluidez básica en **probabilidad** para razonar bajo incertidumbre.
> - vii) Aptitud para **buscar en la documentación oficial** cuando te bloquees.
#### 2. Propósito del Capítulo
> El capítulo se plantea como una **introducción rápida** a los fundamentos necesarios para seguir la mayoría del contenido técnico posterior del libro.

### II. Manipulación de Datos

#### 1. Tensores Como Estructura Central
> Para trabajar con datos en el ordenador se necesitan dos cosas: **(i) adquirir datos** y **(ii) procesarlos**una vez dentro del sistema.  
> El fragmento introduce los **arreglos n-dimensionales**, también llamados **tensores**.
> - **Vector**: tensor 1D (un eje).
> - **Matriz**: tensor 2D (dos ejes).
> - **Tensor de orden k**: cuando (k > 2), se usa el término general (sin nombre especializado).
#### 2. Tensor en Frameworks Modernos
> El texto compara la clase tensor de frameworks modernos con `ndarray` de NumPy: se parece, pero añade dos “killer features”:
> - Soporte de **diferenciación automática**.
> - Uso de **GPU** para acelerar cómputo numérico (mientras NumPy corre solo en CPU).

### III. Creación y Forma de Tensores en PyTorch

#### 1. Importación de la Librería
> El fragmento usa PyTorch y recuerda que el nombre del paquete es `torch`.
```python
import torch
```
#### 2. Creación con `arange` y Tipo de Dato
> `torch.arange(n)` crea un vector con valores espaciados uniformemente desde 0 (incluido) hasta (n) (no incluido), con paso 1 por defecto.  
> El ejemplo fuerza `dtype=torch.float32`.
```python
x = torch.arange(12, dtype=torch.float32)
```
> Cada valor es un **elemento** del tensor; el ejemplo contiene 12 elementos.
#### 3. Tamaño Total: `numel`
> Para inspeccionar el número total de elementos, se usa el método `numel()`.
```python
x.numel()
>>> 12
```
#### 4. Forma: `shape`
> La **forma** (longitud en cada eje) se consulta con el atributo `shape`.  
> En un vector, la forma tiene un único valor (equivalente al tamaño).
```python
x.shape
```
#### 5. Cambio de Forma: `reshape`
> `reshape` permite cambiar la forma **sin alterar** tamaño ni valores.  
> Ejemplo: vector de forma `(12,)` a matriz de forma `(3, 4)`.  
> El texto remarca el orden “por filas”: los elementos se colocan fila a fila (p. ej., `x[3] == X[0, 3]`).
```python
X = x.reshape(3, 4)
```
#### 6. Inferencia Automática con `-1` en `reshape`
> No hace falta especificar toda la forma si ya se conoce el tamaño total.  
> Para inferir automáticamente una dimensión se usa `-1` (ej.: `x.reshape(-1, 4)` o `x.reshape(3, -1)`).
#### 7. Inicialización Común: `zeros`, `ones`, `randn`
> Tensores con valores constantes:
> - Todo ceros con `torch.zeros((2, 3, 4))`.
> - Todo unos con `torch.ones((2, 3, 4))`.  
>     Muestreo aleatorio independiente por elemento: `torch.randn(3, 4)` genera una matriz con valores de una **Gaussiana estándar** (media 0, desviación típica 1), y el texto lo conecta con la inicialización de parámetros en redes neuronales.
#### 8. Creación Desde Listas Python: `torch.tensor`
> También se puede construir un tensor proporcionando valores explícitos mediante listas (posiblemente anidadas).  
> En una matriz, la lista externa corresponde al eje 0 y la interna al eje 1.
```python
torch.tensor([[2, 1, 4, 3],
              [1, 2, 3, 4],
              [4, 3, 2, 1]])
```

### IV. Indexación y Slicing
#### 1. Lectura con Índices y Rangos
> Acceso como en listas Python: indexación desde 0.
> - Indexación negativa: posiciones relativas al final.
> - Slicing `X[start:stop]`: incluye `start` y excluye `stop`.  
>     Regla importante: si solo se especifica un índice/slice en un tensor de orden (k), se aplica sobre el eje 0.  
>     Ejemplos del texto: `X[-1]` selecciona la última fila; `X[1:3]` selecciona segunda y tercera fila.
#### 2. Escritura y Asignación
> Se pueden escribir elementos concretos con índices: por ejemplo `X[1, 2] = 17`.  
> Para asignar el mismo valor a múltiples elementos, se indexa en el lado izquierdo; ejemplo: `X[:2, :] = 12` asigna a las dos primeras filas.  
> El texto aclara que esto aplica a vectores, matrices y tensores de más dimensiones.

### V. Operaciones con Tensores
#### 1. Operaciones Elemento a Elemento
> Tras construir tensores y acceder a sus elementos, el fragmento introduce operaciones matemáticas.  
> **Operaciones elemento a elemento**: aplican una operación escalar a cada elemento.
> - Operadores escalares unarios: firma (f: \mathbb{R} \rightarrow \mathbb{R}).
> - Operadores escalares binarios: firma (f: \mathbb{R}, \mathbb{R} \rightarrow \mathbb{R}).  
>     Levantar (lift) un operador escalar binario a vectores del mismo tamaño: para (c = F(u, v)), cada componente cumple (c_i \leftarrow f(u_i, v_i)).  
>     Operadores aritméticos estándar `+`, `-`, `*`, `/`, `**` están disponibles como operaciones elemento a elemento para tensores de igual forma.
```python
x = torch.tensor([1.0, 2, 4, 8])
y = torch.tensor([2, 2, 2, 2])
x + y, x - y, x * y, x / y, x ** y
```
#### 2. Operaciones de Álgebra Lineal
> Además de operaciones elemento a elemento, el texto menciona productos punto y multiplicación matricial, indicando que se elaborarán en la Sección 2.3.
#### 3. Concatenación: `torch.cat`
> Se pueden concatenar tensores apilándolos “end-to-end”, indicando el eje `dim` para concatenar.  
> El ejemplo compara concatenar por filas (`dim=0`) frente a por columnas (`dim=1`).
```python
X = torch.arange(12, dtype=torch.float32).reshape((3, 4))
Y = torch.tensor([[2.0, 1, 4, 3],
                  [1, 2, 3, 4],
                  [4, 3, 2, 1]])
torch.cat((X, Y), dim=0), torch.cat((X, Y), dim=1)
```
> El texto explica el efecto sobre longitudes: al concatenar por filas, se suman longitudes del eje 0; por columnas, se suman longitudes del eje 1.
#### 4. Tensores Lógicos y Reducciones
> Ejemplo de tensor binario (booleano) con una comparación: `X == Y` evalúa igualdad por posición ((i, j)), dando `True` si son iguales y `False` si no.  
> Sumar todos los elementos: `X.sum()` devuelve un tensor con un único elemento.

### VI. Broadcasting
#### 1. Idea y Procedimiento en Dos Pasos
> Broadcasting permite operaciones elemento a elemento incluso si las formas no coinciden, bajo ciertas condiciones.  
> Procedimiento descrito:
> - i) Expandir uno o ambos arrays copiando elementos a lo largo de ejes de longitud 1 hasta que tengan la misma forma.
> - ii) Ejecutar la operación elemento a elemento sobre los arrays resultantes.  
>     Ejemplo: `a` de forma ($3 \times 1$) y `b` de forma ($1 \times 2$) se convierten efectivamente en ($3 \times 2$) al replicar `a` por columnas y `b` por filas, antes de sumar.
```python
a = torch.arange(3).reshape((3, 1))
b = torch.arange(2).reshape((1, 2))
a + b
```

### VII. Ahorro de Memoria
#### 1. Por Qué `Y = Y + X` Puede Ser Problemático
> Ejecutar operaciones puede asignar nueva memoria para los resultados.  
> El ejemplo: `Y = X + Y` hace que `Y` apunte a un nuevo bloque de memoria (se “desreferencia” el anterior).  
> Se usa `id()` para mostrar que, tras `Y = Y + X`, `id(Y)` cambia porque primero se crea el resultado y luego `Y` pasa a referenciarlo.  
> Motivos de indeseabilidad según el texto:
> - Evitar asignaciones innecesarias (especialmente con cientos de MB de parámetros actualizados muchas veces por segundo).
> - Si múltiples variables apuntan a los mismos parámetros, no actualizar “in-place” puede provocar fugas de memoria o referencias a parámetros obsoletos.
#### 2. Actualizaciones In-Place con Slicing
> Actualización in-place propuesta: asignar a un tensor ya asignado usando slicing: `Y[:] = <expression>`.  
> Ejemplo con `zeros_like` para crear `Z` con la misma forma que `Y`, y luego sobrescribir su contenido sin cambiar el `id(Z)`.
```python
Z = torch.zeros_like(Y)
Z[:] = X + Y
```
#### 3. Atajos In-Place con `+=`
> Si `X` no se reutiliza después, el fragmento sugiere `X[:] = X + Y` o `X += Y` para reducir overhead de memoria; en el ejemplo `X += Y` mantiene el mismo `id(X)`.

### VIII. Conversión a Otros Objetos de Python
#### 1. Interoperabilidad con NumPy
> Convertir entre tensor de PyTorch y array de NumPy es directo: `A = X.numpy()` y `B = torch.from_numpy(A)`.  
> El texto afirma que **comparten memoria subyacente**: una operación in-place sobre uno también cambia el otro.
```python
A = X.numpy()
B = torch.from_numpy(A)
type(A), type(B)
```
#### 2. Conversión a Escalar Python
> Para un tensor de tamaño 1, se puede obtener un escalar con `item()` o con funciones built-in como `float()` e `int()`.
```python
a = torch.tensor([3.5])
a, a.item(), float(a), int(a)
```

### IX. Resumen del Fragmento
#### 1. Qué Te Llevas
> El fragmento resume que la clase tensor es la interfaz principal para almacenar y manipular datos en librerías de deep learning, destacando:
> - Rutinas de **construcción**.
> - **Indexación** y **slicing**.
> - Operaciones matemáticas básicas.
> - **Broadcasting**.
> - Asignación eficiente en memoria (**in-place**).
> - Conversión hacia/desde otros objetos Python (p. ej., NumPy).
#### 2. Checklist de Verificación Rápida
> Antes de dar por “controlada” esta parte, comprueba que puedes:
> - Crear tensores con `arange`, `zeros`, `ones`, `randn`, y desde listas con `torch.tensor`.
> - Explicar y usar `shape`, `numel`, `reshape` (incluyendo `-1`).
> - Leer y escribir con indexación/slicing (incluyendo asignación por rangos).
> - Distinguir operaciones elemento a elemento, concatenación con `cat`, y saber qué hace `X.sum()`.
> - Describir el procedimiento de broadcasting en dos pasos y reconocer el patrón                               ($3\times1 + 1\times2 \rightarrow 3\times2$).
> - Justificar por qué `+=` y `Y[:] = ...` ahorran memoria frente a `Y = Y + X` (según lo explicado con `id()`).
> - Convertir entre PyTorch y NumPy y saber que comparten memoria (implicación: cuidado con in-place).


---

## D2DpL 6. Builders Guide
### I. Contexto y Objetivo del Capítulo
#### 1. Rol del Software en Deep Learning
> El capítulo explica que, además de datos masivos y hardware potente, las **herramientas software** han sido claves en el progreso del deep learning: permiten **prototipar rápido**, reutilizar componentes estándar y mantener la opción de hacer modificaciones “de bajo nivel”.  
> También describe una evolución hacia **abstracciones cada vez más altas**: de pensar en neuronas → capas → bloques más gruesos (patrones repetidos de capas).
#### 2. Qué Cubre el Capítulo
> El objetivo es “levantar el capó” del framework para pasar de usuario final a “power user”. Se centra en:
> - **Construcción de modelos**
> - **Acceso e inicialización de parámetros**
> - **Diseño de capas y bloques personalizados**
> - **Guardar y cargar modelos**
> - **Uso de GPUs** para acelerar cómputo  
>     Nota del material: no introduce nuevos modelos ni datasets, pero los capítulos avanzados dependen de estas técnicas.

### II. Capas y Módulos
#### 1. De Neuronas a Módulos
> El material recalca que **neurona**, **capa** y **modelo completo** comparten la misma “plantilla” conceptual:
> - i) toman entradas
> - ii) producen salidas
> - iii) tienen parámetros ajustables (si aplica)  
>     Motivo para introducir **módulos**: en arquitecturas con cientos de capas (ej. ResNet-152) aparecen **patrones repetidos**; implementar capa a capa se vuelve tedioso.  
>     Idea clave: un **módulo** puede ser una capa, un bloque de varias capas o el modelo entero, y se pueden **componer recursivamente** para construir redes complejas con código compacto.

#### 2. Qué Es un Módulo en PyTorch
> Desde el punto de vista de programación, un módulo es una **clase** (subclase de `nn.Module`) que:
> - define `forward` (propagación hacia delante)
> - almacena los parámetros necesarios (si los hay)  
>     El texto indica que no hace falta implementar backprop manualmente: gracias a **autodiferenciación**, normalmente solo te ocupas de `forward` y de declarar/guardar parámetros.
#### 3. `nn.Sequential` Como Módulo Encadenador
> `nn.Sequential` es un tipo especial de `Module` que mantiene una lista ordenada de submódulos y ejecuta su `forward` encadenándolos (salida de uno → entrada del siguiente).  
> El material menciona que `net(X)` es un atajo de `net.__call__(X)`.
```python
import torch
from torch import nn

net = nn.Sequential(nn.LazyLinear(256), nn.ReLU(), nn.LazyLinear(10))
X = torch.rand(2, 20)
net(X).shape
```
#### 4. Módulo Personalizado
> El texto resume lo que “debe proporcionar” un módulo:
> 1. ingerir datos en `forward`
> 2. devolver una salida (posiblemente con forma distinta)
> 3. permitir gradientes respecto a la entrada (típicamente automático)
> 4. almacenar y dar acceso a parámetros necesarios
> 5. inicializar parámetros si hace falta  
>     Ejemplo: implementar un MLP como clase que hereda de `nn.Module`, definiendo `__init__` y `forward`.
```python
import torch
from torch import nn
from torch.nn import functional as F

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden = nn.LazyLinear(256)
        self.out = nn.LazyLinear(10)

    def forward(self, X):
        return self.out(F.relu(self.hidden(X)))

net = MLP()
X = torch.rand(2, 20)
net(X).shape
```
#### 5. Implementación Conceptual de un `Sequential`
> Para entender `Sequential`, el material construye `MySequential` con dos ideas: 
> 	i) ir añadiendo módulos
> 	ii) recorrerlos en `forward` en el orden de inserción.  
> La justificación importante: el framework “sabe” qué submódulos has añadido y por tanto puede **inicializar parámetros** correctamente.
```python
from torch import nn

class MySequential(nn.Module):
    def __init__(self, *args):
        super().__init__()
        for idx, module in enumerate(args):
            self.add_module(str(idx), module)

    def forward(self, X):
        for module in self.children():
            X = module(X)
        return X
```
#### 6. Ejecutar Código Arbitrario en `forward`
> El material avisa: no todas las arquitecturas son una “cadena” simple; a veces necesitas **control de flujo** o **operaciones matemáticas arbitrarias** dentro de `forward`.  
> Introduce el ejemplo de “parámetros constantes”: tensores usados en el cómputo que **no se actualizan** por optimización (no son parámetros del modelo).  
> Ejemplo `FixedHiddenMLP`: usa un `rand_weight` fijo, reutiliza una misma capa (`self.linear`) y mete un `while` que normaliza hasta cumplir una condición, devolviendo un escalar (`X.sum()`).
```python
import torch
from torch import nn
from torch.nn import functional as F

class FixedHiddenMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.rand_weight = torch.rand((20, 20))
        self.linear = nn.LazyLinear(20)

    def forward(self, X):
        X = self.linear(X)
        X = F.relu(X @ self.rand_weight + 1)
        X = self.linear(X)
        while X.abs().sum() > 1:
            X /= 2
        return X.sum()
```
#### 7. Resumen de la Sección y Ejercicios
> Resumen del material:
> - una capa puede ser un módulo
> - muchas capas pueden formar un módulo
> - muchos módulos pueden formar un módulo
> - un módulo puede contener código, y gestiona “housekeeping” (inicialización y backprop)
> - concatenaciones secuenciales se manejan con `Sequential`  
>     Ejercicios propuestos: problemas de guardar módulos en listas Python, construir un “módulo paralelo” que concatene salidas, y una función fábrica para instanciar múltiples copias de una red.

### III. Gestión de Parámetros
#### 1. Motivación
> Tras elegir arquitectura e hiperparámetros, entrenas para minimizar la pérdida; luego necesitas los parámetros para predecir, reutilizar, guardar a disco o inspeccionar.  
> El material enfatiza que normalmente el framework abstrae detalles, pero en arquitecturas no estándar conviene saber declarar/manipular parámetros.
#### 2. Acceso a Parámetros
> En un `Sequential`, puedes acceder a capas por índice (`net[i]`) y a sus parámetros vía atributos o `state_dict()`.  
> El ejemplo muestra que una capa fully-connected tiene típicamente `weight` y `bias`.  
> Los parámetros son objetos complejos (`Parameter`) con valores, gradientes y metadatos; por eso se accede al valor numérico explícito (p. ej., `.data`).  
> Antes de backprop, el gradiente puede estar sin inicializar (`None`).  
> Para listar todos los parámetros (útil en módulos anidados), se usa `named_parameters()`.
```python
import torch
from torch import nn

net = nn.Sequential(nn.LazyLinear(8), nn.ReLU(), nn.LazyLinear(1))
X = torch.rand(size=(2, 4))
net(X)

net[2].state_dict()
[(name, param.shape) for name, param in net.named_parameters()]
```
#### 3. Parámetros Compartidos
> El material muestra “tied parameters”: reutilizar exactamente el **mismo objeto capa** en dos posiciones del modelo para que compartan tensores de pesos.  
> Observación importante: al estar “atados”, no solo tienen el mismo valor: son el **mismo tensor**; si modificas uno, cambia el otro.  
> Respecto a gradientes: al compartir parámetros, los gradientes de las rutas que usan ese parámetro se **acumulan** durante backprop.
```python
import torch
from torch import nn

shared = nn.LazyLinear(8)
net = nn.Sequential(
    nn.LazyLinear(8), nn.ReLU(),
    shared, nn.ReLU(),
    shared, nn.ReLU(),
    nn.LazyLinear(1)
)

X = torch.rand(size=(2, 4))
net(X)
```
#### 4. Resumen y Ejercicios
> Resumen del material: hay varias formas de **acceder** a parámetros y de **atar/compartir** parámetros.  
> Ejercicios: acceder a parámetros en `NestMLP`, entrenar un MLP con capa compartida observando parámetros/gradientes, y discutir por qué compartir parámetros puede ser buena idea.

### IV. Inicialización de Parámetros
#### 1. Inicialización Por Defecto y `nn.init`
> El material indica que PyTorch inicializa pesos y sesgos por defecto con una distribución uniforme cuyo rango depende de dimensiones de entrada/salida, y que `nn.init` ofrece protocolos comunes.
#### 2. Inicializadores Incorporados
> Ejemplo 1: inicializar pesos con Gaussiana (`std=0.01`) y sesgos a cero, aplicándolo a todo el modelo vía `net.apply(init_fn)`.  
> Ejemplo 2: inicializar a constante (pesos a 1, sesgos a 0).  
> Ejemplo 3: inicializar distintos bloques de forma distinta (primera capa con Xavier; segunda capa a constante 42).
```python
import torch
from torch import nn

net = nn.Sequential(nn.LazyLinear(8), nn.ReLU(), nn.LazyLinear(1))
X = torch.rand(size=(2, 4))
net(X)

def init_normal(module):
    if type(module) == nn.Linear:
        nn.init.normal_(module.weight, mean=0, std=0.01)
        nn.init.zeros_(module.bias)

net.apply(init_normal)
```
#### 3. Inicialización Personalizada
> El material propone una distribución “extraña” para cada peso `w`: $$w \sim \begin{cases} U(5,10) & \text{con prob. } \tfrac{1}{4} \\ 0 & \text{con prob. } \tfrac{1}{2} \\ U(-10,-5) & \text{con prob. } \tfrac{1}{4} \end{cases}$$Luego implementa una función que inicializa con uniforme en ([-10,10]) y “enmascara” (pone a 0) los valores con (`|w| < 5`).  
> También remarca que siempre puedes **tocar parámetros directamente** vía `.data`.
#### 4. Resumen y Ejercicios
> Resumen del material: se puede inicializar con métodos **built-in** y **custom**.  
> Ejercicio: buscar en la documentación online más inicializadores incorporados.

### V. Inicialización Perezosa
#### 1. Qué Problema Resuelve
> El material destaca comportamientos “contraintuitivos” que sí funcionan: definir redes sin fijar dimensionalidad de entrada, apilar capas sin saber la salida previa e incluso “inicializar” antes de conocer cuántos parámetros hay.  
> La clave: el framework **difere la inicialización** hasta el **primer pase de datos**, inferiendo formas “sobre la marcha”.  
> Se ilustra que antes del primer forward puede aparecer `<UninitializedParameter>`, y tras pasar datos se concretan las formas (ej., el peso de la primera capa pasa a tener forma `[256, 20]` si la entrada tiene dimensión 20).
```python
import torch
from torch import nn

net = nn.Sequential(nn.LazyLinear(256), nn.ReLU(), nn.LazyLinear(10))
net[0].weight  # antes del primer forward

X = torch.rand(2, 20)
net(X)
net[0].weight.shape
```
#### 2. “Dry Run” para Inferir Formas e Inicializar
> El material define un método que hace un forward con inputs “dummy” para inferir formas y, opcionalmente, aplicar un inicializador.
#### 3. Resumen y Ejercicios
> Resumen del material: la inicialización perezosa facilita modificar arquitecturas y evita errores típicos de dimensiones; para forzarla, pasa datos por el modelo.  
> Ejercicios: qué pasa si fijas solo dimensiones de la primera capa, qué pasa con dimensiones inconsistentes, y qué hacer con entradas de dimensionalidad variable (pista: parameter tying).

### VI. Capas Personalizadas
#### 1. Motivación
> El material conecta el éxito del deep learning con la disponibilidad de muchas capas; pero tarde o temprano necesitarás una capa que no exista y tendrás que construirla.
#### 2. Capas sin Parámetros
> Ejemplo `CenteredLayer`: resta la media a la entrada; basta heredar de `nn.Module` e implementar `forward`.  
> Se verifica que funciona y que, al pasar datos aleatorios por una red que termina con `CenteredLayer`, la media de la salida es ~0 (con pequeño error numérico).
```python
import torch
from torch import nn

class CenteredLayer(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, X):
        return X - X.mean()

layer = CenteredLayer()
layer(torch.tensor([1.0, 2, 3, 4, 5]))
```
#### 3. Capas con Parámetros
> Para capas entrenables, el material recomienda crear parámetros con utilidades built-in (gestión de acceso, inicialización, compartición, guardado/carga).  
> Ejemplo `MyLinear`: implementa una capa tipo fully-connected con dos parámetros (`weight`, `bias`) mediante `nn.Parameter`, y mete ReLU por defecto.
```python
import torch
from torch import nn
from torch.nn import functional as F

class MyLinear(nn.Module):
    def __init__(self, in_units, units):
        super().__init__()
        self.weight = nn.Parameter(torch.randn(in_units, units))
        self.bias = nn.Parameter(torch.randn(units,))

    def forward(self, X):
        linear = torch.matmul(X, self.weight.data) + self.bias.data
        return F.relu(linear)

linear = MyLinear(5, 3)
linear(torch.rand(2, 5))
```
#### 4. Resumen y Ejercicios
> Resumen del material: puedes diseñar capas heredando de la clase base; pueden no tener parámetros o tener parámetros locales creados con funciones built-in.  
> Ejercicios: diseñar una capa con reducción tensórica (se da una expresión) y una capa que devuelva la mitad “líder” de coeficientes de Fourier.

### VII. Entrada y Salida de Archivos
#### 1. Por Qué Guardar y Cargar
> Motivaciones del material: guardar resultados para uso posterior (incluido despliegue) y hacer **checkpointing** durante entrenamientos largos para evitar perder días de cómputo.
#### 2. Guardar y Cargar Tensores
> Para tensores individuales se usa `torch.save`/`torch.load`; también puedes guardar listas y diccionarios de tensores (útil para pesos).
```python
import torch

x = torch.arange(4)
torch.save(x, "x-file")
x2 = torch.load("x-file")

y = torch.zeros(4)
torch.save([x, y], "x-files")
x2, y2 = torch.load("x-files")

mydict = {"x": x, "y": y}
torch.save(mydict, "mydict")
mydict2 = torch.load("mydict")
```
#### 3. Guardar y Cargar Parámetros de un Modelo
> Punto crítico del material: se guardan **parámetros**, no “el modelo completo”. La arquitectura puede contener código arbitrario y no se serializa igual de natural; por eso, para restaurar: (i) recreas la arquitectura en código y (ii) cargas `state_dict`.  
> Se ilustra que, con mismos parámetros, para la misma entrada, el clon produce exactamente la misma salida (comparación booleana `True`).
```python
import torch
from torch import nn
from torch.nn import functional as F

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden = nn.LazyLinear(256)
        self.output = nn.LazyLinear(10)

    def forward(self, x):
        return self.output(F.relu(self.hidden(x)))

net = MLP()
X = torch.randn(size=(2, 20))
Y = net(X)

torch.save(net.state_dict(), "mlp.params")

clone = MLP()
clone.load_state_dict(torch.load("mlp.params"))
clone.eval()
Y_clone = clone(X)
Y_clone == Y
```
#### 4. Resumen y Ejercicios
> Resumen del material: `save/load` sirven para tensores; redes completas se guardan como diccionario de parámetros; la arquitectura se reconstruye en código.  
> Ejercicios: beneficios prácticos de guardar parámetros (aunque no despliegues), reutilización parcial de redes en otra arquitectura, y cómo guardar arquitectura+parámetros (con restricciones).

### VIII. GPUs
#### 1. Contexto y Preparación
> El material introduce GPUs resaltando el crecimiento de rendimiento (factor 1000 por década desde 2000) y que hay demanda fuerte de esa computación.  
> Para usar una GPU NVIDIA: tener GPU instalada, drivers, CUDA, y usar `nvidia-smi` para ver información de la tarjeta.
#### 2. Dispositivos y Contextos
> En PyTorch, cada tensor vive en un **device** (también llamado “context” en el texto). Por defecto, CPU; otros contextos típicos son GPUs.  
> Regla esencial: para operar con varios tensores en una operación (ej., suma), deben estar en el **mismo device**, o el runtime falla.
```python
import torch

x = torch.tensor([1, 2, 3])
x.device
```
#### 3. Crear Tensores en GPU y Copiar Entre GPUs
> Puedes crear tensores directamente en GPU especificando el device al crearlos; cada tensor en GPU consume memoria de esa GPU (vigilar límites).  
> Si tienes varias GPUs, se puede crear `X` en GPU0 y `Y` en GPU1; para computar `X + Y`, debes mover uno al device del otro (ej., mover `X` a GPU1).  
> El material añade una optimización: si un tensor ya está en el device destino, `Z.cuda(1)` devuelve el propio objeto (no copia).
#### 4. Notas de Rendimiento y Errores Típicos
> Mensaje fuerte del material: **transferir datos entre devices es lento** (mucho más que computar), y además dificulta paralelización (sincronizaciones/esperas).  
> Regla práctica mencionada: muchas operaciones pequeñas son peores que una grande; y varias operaciones “en bloque” suelen ser mejores que muchas sueltas intercaladas.  
> Además: imprimir tensores o convertir a NumPy desde GPU provoca copias a memoria principal y puede introducir overhead adicional (incluye mención al “global interpreter lock”).
#### 5. Modelos en GPU
> Un modelo puede moverse a GPU con `.to(device=...)`, y si la entrada está en GPU, el cálculo se hace en GPU.  
> Se verifica que los parámetros del modelo quedan en el mismo device.
```python
import torch
from torch import nn

net = nn.Sequential(nn.LazyLinear(1))
net = net.to(device=torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))
```
#### 6. Resumen y Ejercicios
> Resumen del material: puedes especificar CPU/GPU para almacenamiento y cálculo; por defecto CPU; todas las entradas de una operación deben estar en el mismo device; mover datos “sin cuidado” puede destruir rendimiento (ej., loguear pérdidas en CPU/NumPy cada minibatch).  
> Ejercicios: comparar velocidad CPU vs GPU en multiplicación de matrices, leer/escribir parámetros en GPU, medir impacto de loguear uno a uno vs log en GPU y transferir al final, y paralelizar multiplicaciones en dos GPUs vs secuencial en una.

### IX. Checklist de Repaso del Capítulo
#### 1. Dominio Mínimo Operativo
> Antes de “dar por controlado” este capítulo, asegúrate de poder:
> - Explicar qué es un `Module` y por qué permite componer capas/bloques/modelos recursivamente.
> - Implementar un módulo propio (constructor + `forward`) y razonar qué deja resuelto autograd.
> - Acceder a parámetros con `state_dict`, atributos (`weight`, `bias`) y recorrerlos con `named_parameters`.
> - Implementar o reconocer “tied parameters” (misma capa reutilizada) y entender qué implica para gradientes.
> - Aplicar inicialización con `net.apply(...)` y distinguir built-in vs custom (incluida la idea de enmascarar pesos).
> - Explicar “lazy initialization”: cuándo aparecen parámetros no inicializados y cómo se inicializan tras el primer forward.
> - Diseñar capas custom sin parámetros y con parámetros usando `nn.Parameter`.
> - Guardar/cargar tensores y guardar/cargar parámetros de modelos con `state_dict` (arquitectura reconstruida en código).
> - Trabajar con devices: crear tensores/modelos en GPU, mover datos, y justificar por qué minimizar transferencias es crítico.


---

## DpL-wPyTorch 3. It Starts With a Tensor
### I. Visión General del Capítulo
#### 1. Idea Central del Capítulo
> El capítulo parte de una idea: en deep learning, los sistemas **transforman datos** de una representación a otra (p. ej., imágenes → etiquetas, texto → texto). Esa transformación se aprende extrayendo regularidades de ejemplos.  
> En ese marco, el capítulo introduce la estructura básica para manejar números en PyTorch: el **tensor**.
#### 2. Qué Cubre el Capítulo
> El propio capítulo enumera sus objetivos:
> - Entender **tensores** como estructura de datos básica en PyTorch.
> - **Indexar** y **operar** con tensores.
> - Interoperar con **NumPy** (arrays multidimensionales).
> - Mover cómputo a **GPU** para velocidad.

### II. Mundo Como Números en Coma Flotante
#### 1. Representaciones Intermedias en Redes Neuronales
> Una red neuronal aprende una transformación por etapas: entre capas aparecen **representaciones intermedias** (colecciones de números en coma flotante) que capturan estructura relevante del input (ej.: en visión, representaciones tempranas pueden parecer detección de bordes/texturas, y más profundas capturan estructuras más complejas).  
> También se remarca un principio: **inputs similares deberían inducir representaciones similares**, especialmente en niveles más profundos (figura del capítulo).
#### 2. Qué Es un Tensor en Este Contexto
> En este libro, “tensor” **no** se usa con las connotaciones de física (espacios, sistemas de referencia, etc.). Aquí significa la **generalización de vectores y matrices a N dimensiones**, equivalente a “array multidimensional”.  
> La **dimensionalidad** coincide con el número de índices necesarios para referirse a un escalar dentro del tensor.

### III. Tensores Como Arrays Multidimensionales
#### 1. De Listas Python a Tensores
> El capítulo empieza comparando el acceso por índice en listas (índices desde 0, asignación por índice) con el acceso por índice en tensores.
```python
a = [1.0, 2.0, 1.0]
a[0]
a[2] = 3.0
```
#### 2. Construcción de Tensores Básicos
> Se muestra la creación de un tensor 1D con `torch.ones(3)` y cómo se indexa/convierte un escalar tensor a `float`.
```python
import torch
a = torch.ones(3)
a[1]
float(a[1])
a[2] = 2.0
```
#### 3. Esencia de los Tensores: Memoria y Eficiencia
> Diferencia conceptual clave:
> - Listas/tuplas Python son colecciones de **objetos Python** (cada elemento suele estar asignado por separado en memoria).
> - Tensores de PyTorch (y arrays de NumPy) son **vistas** sobre bloques de memoria (típicamente) **contiguos**, con tipos numéricos C “sin boxing”.
> Consecuencia que el texto cuantifica: un tensor 1D de 1,000,000 floats de 32 bits ocupa exactamente 4,000,000 bytes contiguos (más un overhead pequeño de metadatos como dimensiones y tipo).
#### 4. Ejemplo Guiado: Puntos 2D
> Se usa un ejemplo didáctico (triángulo 2D) para pasar de una codificación 1D (x,y intercalados) a una representación 2D (cada fila es un punto y cada columna una coordenada).
```python
points = torch.tensor([4.0, 1.0, 5.0, 3.0, 2.0, 1.0])
float(points[0]), float(points[1])

points = torch.tensor([[4.0, 1.0], [5.0, 3.0], [2.0, 1.0]])
points.shape
points[0, 1]
points[0]
```
> El capítulo subraya que al hacer `points[0]` se obtiene **otra vista** del mismo dato subyacente (no “copia” por defecto), y lo retomará más adelante al hablar de views y storage.

### IV. Indexación y Slicing de Tensores
#### 1. Rango de Índices al Estilo Python
> Se recuerda el slicing tipo `start:stop:step` y se muestra que PyTorch permite aplicar slicing **por dimensión** (igual que NumPy).
```python
points[1:]
points[1:, :]
points[1:, 0]
points[None]
```
> Se menciona que además existe **advanced indexing** y se aplaza al siguiente capítulo.

### V. Tensores con Nombres
#### 1. Motivación
> Problema: al transformar datos (p. ej., imágenes con dimensiones como batch/canales/alto/ancho), recordar el orden exacto de ejes es fácil de romper y genera errores de alineación.
#### 2. Ejemplo: Pasar a Escala de Grises y Broadcasting
> Se construye un ejemplo con un tensor de imagen `img_t` y un batch `batch_t`. Se muestra:
> - Media “ingenua” contando desde el final (`mean(-3)`) para promediar canales.
> - Media ponderada usando pesos RGB y **broadcasting** (haciendo `unsqueeze`).
> - Alternativa con `einsum` (mini-lenguaje de índices), pero el libro avisa que no se usará después.
```python
img_t = torch.randn(3, 5, 5)              # [channels, rows, columns]
weights = torch.tensor([0.2126, 0.7152, 0.0722])

batch_t = torch.randn(2, 3, 5, 5)         # [batch, channels, rows, columns]
img_gray_naive = img_t.mean(-3)
batch_gray_naive = batch_t.mean(-3)

unsqueezed_weights = weights.unsqueeze(-1).unsqueeze_(-1)
img_gray_weighted = (img_t * unsqueezed_weights).sum(-3)
batch_gray_weighted = (batch_t * unsqueezed_weights).sum(-3)

img_gray_weighted_fancy = torch.einsum('...chw,c->...hw', img_t, weights)
batch_gray_weighted_fancy = torch.einsum('...chw,c->...hw', batch_t, weights)
```
#### 3. Named Tensors: Qué Aportan y Limitaciones
> PyTorch añadió (en el momento de escritura del libro) **named tensors** como característica experimental: puedes asignar nombres a ejes, y entonces PyTorch también comprueba **coherencia de nombres** al operar.  
> Puntos prácticos que muestra el capítulo:
> - Crear tensores con `names=[...]`.
> - Añadir nombres a un tensor existente con `refine_names(..., ...)`.
> - Alinear explícitamente dimensiones con `align_as`.
> - Reducir por dimensión nombrada con `sum('channels')`.
> - Si se combinan dimensiones con nombres incompatibles, aparece un error.
> - Para volver al mundo “sin nombres”, se usa `rename(None)`.
> - Dada su naturaleza experimental, el libro decide **no usarlos** en el resto.
```python
weights_named = torch.tensor([0.2126, 0.7152, 0.0722], names=['channels'])

img_named = img_t.refine_names(..., 'channels', 'rows', 'columns')
weights_aligned = weights_named.align_as(img_named)
gray_named = (img_named * weights_aligned).sum('channels')
gray_plain = gray_named.rename(None)
```

### VI. Tipos de Elemento y `dtype`
#### 1. Por Qué Importa el Tipo Numérico
> Razones que da el libro para preferir tensores/arrays frente a tipos numéricos Python y listas:
> - En Python, los números son objetos (boxing) → ineficiente para millones de valores.
> - Las listas no traen operaciones numéricas vectorizadas eficientes (dot product, sumas vectoriales, etc.) ni layout de memoria optimizado.
> - El intérprete de Python es lento frente a código compilado para matemáticas masivas.  
>     Por eso PyTorch mantiene explícitamente el tipo numérico del tensor.
#### 2. `dtype`: Qué Es y Valores Típicos
> `dtype` define el tipo numérico y el tamaño en bytes (y si es entero con signo o no, como `uint8`). El capítulo lista:
> - `torch.float32` / `torch.float`
> - `torch.float64` / `torch.double`
> - `torch.float16` / `torch.half`
> - `torch.int8`, `torch.uint8`, `torch.int16`/`short`, `torch.int32`/`int`, `torch.int64`/`long`
> - `torch.bool`  
>     Y afirma que el **dtype por defecto** en PyTorch es **float32**.
#### 3. Elección Práctica de Tipos
> El libro destaca:
> - En redes neuronales, típicamente se computa con **32-bit float**; usar 64-bit suele aumentar coste sin mejorar precisión del modelo.
> - `float16` es útil sobre todo en GPUs modernas para reducir huella con impacto menor en precisión.
> - Tensores usados como índices suelen requerir **int64**.
> - Predicados (`points > 1.0`) producen tensores `bool`.
#### 4. Gestión del `dtype` en PyTorch
> El capítulo muestra tres vías:
> - Pasar `dtype=` al constructor.
> - Convertir con métodos tipo `.double()`, `.short()`.
> - Usar `.to(dtype=...)` (y señala que `to` comprueba si hace falta convertir).  
>     También indica que al mezclar tipos en operaciones, PyTorch promueve a un tipo “más grande”, así que si quieres cálculo en 32-bit debes vigilar los inputs.
```python
double_points = torch.ones(10, 2, dtype=torch.double)
short_points = torch.tensor([[1, 2], [3, 4]], dtype=torch.short)

short_points.dtype

double_points = torch.zeros(10, 2).double()
short_points = torch.ones(10, 2).short()

double_points = torch.zeros(10, 2).to(torch.double)
short_points = torch.ones(10, 2).to(dtype=torch.short)

points_64 = torch.rand(5, dtype=torch.double)
points_short = points_64.to(torch.short)
points_64 * points_short
```

### VII. API de Tensores
#### 1. Doble Forma: Función `torch.*` y Método del Tensor
> El libro enfatiza que la mayoría de operaciones existen como:
> - funciones en el módulo `torch`
> - métodos en el objeto tensor  
>     y son intercambiables (ej.: `torch.transpose(a, 0, 1)` vs `a.transpose(0, 1)`).
```python
a = torch.ones(3, 2)
a_t1 = torch.transpose(a, 0, 1)
a_t2 = a.transpose(0, 1)
```
#### 2. Cómo Está Organizada la Documentación
> El capítulo no lista todas las ops, pero dice que la documentación online está organizada en grupos: creación, indexado/slicing/reshape/stride, matemáticas (pointwise, reductions, comparaciones, espectrales, BLAS/LAPACK), muestreo aleatorio, serialización, paralelismo, etc.

### VIII. Storage y Views
#### 1. Idea Base: Storage y Vistas
> El capítulo define: los valores viven en un `torch.Storage` (array 1D contiguo de números). Un `Tensor` es una **vista** sobre ese storage que indexa con **offset** y **strides** por dimensión.  
> Consecuencia: múltiples tensores pueden referenciar el **mismo storage** con distintas formas/strides, y crear vistas puede ser barato incluso con datos grandes.
#### 2. Indexar un Storage y Efectos Laterales
> Se accede al storage con `.storage()`. El storage es 1D, aunque el tensor sea 2D/3D. Cambiar el storage cambia el tensor que lo referencia.
```python
points = torch.tensor([[4.0, 1.0], [5.0, 3.0], [2.0, 1.0]])
points_storage = points.storage()
points_storage[0]
points_storage[0] = 2.0
points
```
#### 3. Operaciones In-Place y Sufijo **`_`**
> Regla de nomenclatura: métodos que terminan en `_` operan **in-place**, modificando el tensor en vez de devolver uno nuevo (ej.: `zero_`). Los métodos sin `_` no modifican el original y devuelven un tensor nuevo.
```python
a = torch.ones(3, 2)
a.zero_()
a
```

### IX. Metadatos: Size, Offset y Stride
#### 1. Definiciones Operativas
> El capítulo define tres piezas que, junto con el storage, “definen” el tensor:
> - **Size/Shape**: cuántos elementos por dimensión.
> - **Storage Offset**: índice del primer elemento del tensor dentro del storage.
> - **Stride**: cuántos elementos del storage hay que “saltar” al incrementar el índice en cada dimensión.
#### 2. Subtensores Como Views (Sin Copiar)
> Ejemplo: `second_point = points[1]` es un subtensor que referencia el mismo storage con otro offset/stride. Se muestra que modificar el subtensor puede modificar el tensor original; si no lo quieres, usa `.clone()`.
```python
points = torch.tensor([[4.0, 1.0], [5.0, 3.0], [2.0, 1.0]])
second_point = points[1]
second_point.storage_offset()
second_point.size()
second_point.stride()

second_point[0] = 10.0
points

second_point = points[1].clone()
second_point[0] = 10.0
points
```
#### 3. Transposición Sin Copiar (2D y N-D)
> Se enseña que `.t()` es un atajo para transponer tensores 2D, y que la transposición puede lograrse cambiando strides (sin nueva memoria), verificando que comparten el mismo storage.
```python
points = torch.tensor([[4.0, 1.0], [5.0, 3.0], [2.0, 1.0]])
points_t = points.t()

id(points.storage()) == id(points_t.storage())
points.stride()
points_t.stride()
```
> Para más dimensiones, se usa `transpose(dim0, dim1)` intercambiando shape/stride en esas dimensiones.
```python
some_t = torch.ones(3, 4, 5)
transpose_t = some_t.transpose(0, 2)
some_t.shape, transpose_t.shape
some_t.stride(), transpose_t.stride()
```
#### 4. Contiguidad y `contiguous()`
> Definición práctica del libro: un tensor es **contiguous** si sus valores están dispuestos en storage “desde la dimensión más a la derecha hacia la izquierda” (por filas en 2D).  
> Se indica que algunas operaciones (ej.: `view`, mencionado como “próximo capítulo”) requieren contiguidad; si no, PyTorch pide llamar a `contiguous()`. Si ya es contiguo, `contiguous()` no hace nada.
```python
points = torch.tensor([[4.0, 1.0], [5.0, 3.0], [2.0, 1.0]])
points_t = points.t()
points.is_contiguous()
points_t.is_contiguous()

points_t_cont = points_t.contiguous()
points_t.stride(), points_t_cont.stride()
points_t.storage()
points_t_cont.storage()
```

### X. Mover Tensores a la GPU
#### 1. Atributo `device` y Creación/Copia
> Además de `dtype`, un tensor tiene un **device** (dónde vive el dato: CPU o GPU). Se puede crear directamente en GPU con `device='cuda'` o mover un tensor con `.to(device='cuda')`.  
> El capítulo enfatiza que la API es prácticamente la misma en CPU y GPU, para escribir código agnóstico a dónde corre el “heavy compute”.
```python
points = torch.tensor([[4.0, 1.0], [5.0, 3.0], [2.0, 1.0]])
points_gpu = torch.tensor([[4.0, 1.0], [5.0, 3.0], [2.0, 1.0]], device='cuda')
points_gpu = points.to(device='cuda')
points_gpu = points.to(device='cuda:0')
```
#### 2. Persistencia en GPU y Volver a CPU
> El libro describe qué ocurre en una operación típica: se copia a GPU, se aloca un tensor resultado en GPU, y se devuelve un handle a ese tensor; el resultado **no vuelve** a CPU salvo que lo fuerces (p. ej., imprimir/acceder o mover explícitamente).  
> Para volver a CPU: `.to(device='cpu')` o `.cpu()`. Atajos: `.cuda()` / `.cuda(0)`.  
> También menciona que `to` permite cambiar **device y dtype** a la vez.
```python
points_gpu = 2 * points.to(device='cuda')
points_gpu = points_gpu + 4
points_cpu = points_gpu.to(device='cpu')

points_gpu = points.cuda()
points_gpu = points.cuda(0)
points_cpu = points_gpu.cpu()
```
> Nota contextual del propio texto (fecha de escritura): PyTorch se acelera principalmente con GPUs CUDA; menciona ROCm y TPU como soporte adicional con distintos grados de madurez en ese momento.

### XI. Interoperabilidad con NumPy
#### 1. Conversión y “Zero-Copy” en CPU
> Convertir a NumPy: `points.numpy()`. Convertir desde NumPy: `torch.from_numpy(...)`.  
> El capítulo afirma que en CPU la conversión comparte el mismo buffer (costo casi cero) y modificar el NumPy array modifica el tensor original. Si el tensor está en GPU, PyTorch hace una **copia** a CPU para crear el NumPy array.
```python
points = torch.ones(3, 4)
points_np = points.numpy()
points2 = torch.from_numpy(points_np)
```
> Nota del libro: dtype por defecto de NumPy suele ser 64-bit, mientras que en PyTorch es float32; se sugiere vigilar y convertir a `torch.float` cuando proceda.

### XII. Tensores “Generalizados” y Dispatcher
#### 1. Separación entre API y Backend
> El capítulo “levanta el capó”: la forma de almacenar datos está separada del **contrato del API tensor**; cualquier implementación que cumpla ese contrato puede considerarse tensor.  
> Se menciona un mecanismo de **dispatching**: PyTorch invoca kernels correctos según device y tipo, y eso permite otros tipos de tensores (ej.: sparse, quantized, u otros backends/hardware).

### XIII. Serialización de Tensores
#### 1. Guardar y Cargar con PyTorch
> Para persistir tensores, se usa `torch.save` y `torch.load`. El libro dice que usa `pickle` para el objeto tensor y código dedicado para el storage.  
> Advierte: el formato resultante no es interoperable fuera de PyTorch.
```python
torch.save(points, '../data/p1ch3/ourpoints.t')
points = torch.load('../data/p1ch3/ourpoints.t')

with open('../data/p1ch3/ourpoints.t','wb') as f:
    torch.save(points, f)

with open('../data/p1ch3/ourpoints.t','rb') as f:
    points = torch.load(f)
```
#### 2. Serialización Interoperable con HDF5 (h5py)
> Para interoperabilidad, propone HDF5 con `h5py`, que trabaja con NumPy arrays. Se guarda como dataset (clave, incluso anidada) y se puede **indexar en disco** sin cargar todo a memoria.  
> Al convertir desde HDF5 a tensor con `torch.from_numpy(dset[-2:])`, en este caso el texto indica que los datos se copian al storage del tensor.  
> También remarca que al cerrar el archivo HDF5, los datasets quedan inválidos.
```python
import h5py

f = h5py.File('../data/p1ch3/ourpoints.hdf5', 'w')
dset = f.create_dataset('coords', data=points.numpy())
f.close()

f = h5py.File('../data/p1ch3/ourpoints.hdf5', 'r')
dset = f['coords']
last_points = torch.from_numpy(dset[-2:])
f.close()
```

### XIV. Trampas Típicas del Capítulo
#### 1. Errores de “Vista” vs “Copia”
> Si extraes un subtensor (indexado/slicing), puede ser una **vista** sobre el mismo storage: modificarlo puede modificar el tensor original. Si quieres independencia, usa `.clone()`.
#### 2. Confusión con Contiguidad
> Un tensor transpuesto puede no ser contiguo; algunas operaciones requieren llamar a `contiguous()` para materializar un layout contiguo (con nuevo storage).
#### 3. Sorpresas con `dtype` al Mezclar Librerías
> NumPy tiende a usar 64-bit por defecto; PyTorch usa float32. Si mezclas sin vigilar, puedes acabar computando en float64 “sin querer”.
#### 4. GPU No Implica “Vuelve Solo” a CPU
> Tras operar en GPU, el resultado sigue en GPU; si necesitas CPU (o NumPy), debes moverlo explícitamente.

### XV. Checklist de Dominio
#### 1. Antes de Pasar al Siguiente Capítulo
> Comprueba que puedes, sin dudar:
> - Explicar “tensor” como array N-D y relacionarlo con representaciones en coma flotante.
> - Crear tensores (`ones`, `zeros`, `tensor([...])`), inspeccionar `shape` y hacer indexing/slicing por dimensión.
> - Entender broadcasting en el ejemplo de pesos RGB y por qué aparecen `unsqueeze`.
> - Decidir/convertir `dtype` y justificar por qué float32 es estándar en redes.
> - Explicar storage/view/offset/stride y predecir efectos laterales al modificar vistas.
> - Verificar contiguidad y usar `contiguous()` cuando sea necesario.
> - Mover tensores a GPU/CPU con `to`, `cuda`, `cpu` y entender qué se copia y qué no.
> - Convertir a/desde NumPy y saber cuándo hay buffer compartido vs copia.
> - Guardar/cargar con `torch.save/load` y, si hace falta interoperabilidad, usar HDF5 con `h5py`.

### XVI. Siguiente Paso Recomendado
#### 1. Práctica Dirigida con Ejercicios del Libro
> El capítulo propone ejercicios sobre predecir `size/offset/stride` tras `view` y slicing, y buscar operaciones matemáticas en `torch` (incluyendo versiones in-place con `_`). Si quieres, te los convierto en una “hoja de práctica” en formato Obsidian (pregunta → espacio para respuesta → solución).

Estos apuntes continúan en [[Tema 2 - Foundations of Neural Networks]]
