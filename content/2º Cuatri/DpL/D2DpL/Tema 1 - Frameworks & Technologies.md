## D2DpL 2. Preliminaries
### I. Visión General del Capítulo

#### 1. Habilidades Previas Necesarias

> Para “sumergirte” en Deep Learning, el capítulo enumera habilidades de supervivencia:
> 
> - (i) Técnicas para **almacenar y manipular datos**.
>     
> - (ii) Librerías para **ingerir y preprocesar datos** de varias fuentes.
>     
> - (iii) Operaciones básicas de **álgebra lineal** aplicadas a datos de alta dimensión.
>     
> - (iv) El “mínimo” de **cálculo** para saber en qué dirección ajustar parámetros para reducir la **función de pérdida**.
>     
> - (v) Capacidad de **computar derivadas automáticamente** (para “olvidar” gran parte del cálculo).
>     
> - (vi) Fluidez básica en **probabilidad** para razonar bajo incertidumbre.
>     
> - (vii) Aptitud para **buscar en la documentación oficial** cuando te bloquees.
>     

#### 2. Propósito del Capítulo

> El capítulo se plantea como una **introducción rápida** a los fundamentos necesarios para seguir la mayoría del contenido técnico posterior del libro.

---

### II. Manipulación de Datos

#### 1. Tensores Como Estructura Central

> Para trabajar con datos en el ordenador se necesitan dos cosas: **(i) adquirir datos** y **(ii) procesarlos** una vez dentro del sistema.  
> El fragmento introduce los **arreglos n-dimensionales**, también llamados **tensores**.
> 
> - **Vector**: tensor 1D (un eje).
>     
> - **Matriz**: tensor 2D (dos ejes).
>     
> - **Tensor de orden k**: cuando (k > 2), se usa el término general (sin nombre especializado).
>     

#### 2. Tensor en Frameworks Modernos

> El texto compara la clase tensor de frameworks modernos con `ndarray` de NumPy: se parece, pero añade dos “killer features”:
> 
> - Soporte de **diferenciación automática**.
>     
> - Uso de **GPU** para acelerar cómputo numérico (mientras NumPy corre solo en CPU).
>     

---

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
> 
```python
x.numel()
```

#### 4. Forma: `shape`

> La **forma** (longitud en cada eje) se consulta con el atributo `shape`.  
> En un vector, la forma tiene un único valor (equivalente al tamaño).
> 
```python
x.shape
```

#### 5. Cambio de Forma: `reshape`

> `reshape` permite cambiar la forma **sin alterar** tamaño ni valores.  
> Ejemplo: vector de forma `(12,)` a matriz de forma `(3, 4)`.  
> El texto remarca el orden “por filas”: los elementos se colocan fila a fila (p. ej., `x[3] == X[0, 3]`).
> 
```python
X = x.reshape(3, 4)
```

#### 6. Inferencia Automática con `-1` en `reshape`

> No hace falta especificar toda la forma si ya se conoce el tamaño total.  
> Para inferir automáticamente una dimensión se usa `-1` (ej.: `x.reshape(-1, 4)` o `x.reshape(3, -1)`).

#### 7. Inicialización Común: `zeros`, `ones`, `randn`

> Tensores con valores constantes:
> 
> - Todo ceros con `torch.zeros((2, 3, 4))`.
>     
> - Todo unos con `torch.ones((2, 3, 4))`.  
>     Muestreo aleatorio independiente por elemento: `torch.randn(3, 4)` genera una matriz con valores de una **Gaussiana estándar** (media 0, desviación típica 1), y el texto lo conecta con la inicialización de parámetros en redes neuronales.
>     

#### 8. Creación Desde Listas Python: `torch.tensor`

> También se puede construir un tensor proporcionando valores explícitos mediante listas (posiblemente anidadas).  
> En una matriz, la lista externa corresponde al eje 0 y la interna al eje 1.
> 
```python
torch.tensor([[2, 1, 4, 3],
              [1, 2, 3, 4],
              [4, 3, 2, 1]])
```

---

### IV. Indexación y Slicing

#### 1. Lectura con Índices y Rangos

> Acceso como en listas Python: indexación desde 0.
> 
> - Indexación negativa: posiciones relativas al final.
>     
> - Slicing `X[start:stop]`: incluye `start` y excluye `stop`.  
>     Regla importante: si solo se especifica un índice/slice en un tensor de orden (k), se aplica sobre el eje 0.  
>     Ejemplos del texto: `X[-1]` selecciona la última fila; `X[1:3]` selecciona segunda y tercera fila.
>     

#### 2. Escritura y Asignación

> Se pueden escribir elementos concretos con índices: por ejemplo `X[1, 2] = 17`.  
> Para asignar el mismo valor a múltiples elementos, se indexa en el lado izquierdo; ejemplo: `X[:2, :] = 12` asigna a las dos primeras filas.  
> El texto aclara que esto aplica a vectores, matrices y tensores de más dimensiones.

---

### V. Operaciones con Tensores

#### 1. Operaciones Elemento a Elemento

> Tras construir tensores y acceder a sus elementos, el fragmento introduce operaciones matemáticas.  
> **Operaciones elemento a elemento**: aplican una operación escalar a cada elemento.
> 
> - Operadores escalares unarios: firma (f: \mathbb{R} \rightarrow \mathbb{R}).
>     
> - Operadores escalares binarios: firma (f: \mathbb{R}, \mathbb{R} \rightarrow \mathbb{R}).  
>     Levantar (lift) un operador escalar binario a vectores del mismo tamaño: para (c = F(u, v)), cada componente cumple (c_i \leftarrow f(u_i, v_i)).  
>     Operadores aritméticos estándar `+`, `-`, `*`, `/`, `**` están disponibles como operaciones elemento a elemento para tensores de igual forma.
>     
> 
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
> 
```python
X = torch.arange(12, dtype=torch.float32).reshape((3, 4))
Y = torch.tensor([[2.0, 1, 4, 3],
                  [1, 2, 3, 4],
                  [4, 3, 2, 1]])
torch.cat((X, Y), dim=0), torch.cat((X, Y), dim=1)
```
> 
> El texto explica el efecto sobre longitudes: al concatenar por filas, se suman longitudes del eje 0; por columnas, se suman longitudes del eje 1.

#### 4. Tensores Lógicos y Reducciones

> Ejemplo de tensor binario (booleano) con una comparación: `X == Y` evalúa igualdad por posición ((i, j)), dando `True` si son iguales y `False` si no.  
> Sumar todos los elementos: `X.sum()` devuelve un tensor con un único elemento.

---

### VI. Broadcasting

#### 1. Idea y Procedimiento en Dos Pasos

> Broadcasting permite operaciones elemento a elemento incluso si las formas no coinciden, bajo ciertas condiciones.  
> Procedimiento descrito:
> 
> - (i) Expandir uno o ambos arrays copiando elementos a lo largo de ejes de longitud 1 hasta que tengan la misma forma.
>     
> - (ii) Ejecutar la operación elemento a elemento sobre los arrays resultantes.  
>     Ejemplo: `a` de forma (3 \times 1) y `b` de forma (1 \times 2) se convierten efectivamente en (3 \times 2) al replicar `a` por columnas y `b` por filas, antes de sumar.
>     
> 
```python
a = torch.arange(3).reshape((3, 1))
b = torch.arange(2).reshape((1, 2))
a + b
```

---

### VII. Ahorro de Memoria

#### 1. Por Qué `Y = Y + X` Puede Ser Problemático

> Ejecutar operaciones puede asignar nueva memoria para los resultados.  
> El ejemplo: `Y = X + Y` hace que `Y` apunte a un nuevo bloque de memoria (se “desreferencia” el anterior).  
> Se usa `id()` para mostrar que, tras `Y = Y + X`, `id(Y)` cambia porque primero se crea el resultado y luego `Y` pasa a referenciarlo.  
> Motivos de indeseabilidad según el texto:
> 
> - Evitar asignaciones innecesarias (especialmente con cientos de MB de parámetros actualizados muchas veces por segundo).
>     
> - Si múltiples variables apuntan a los mismos parámetros, no actualizar “in-place” puede provocar fugas de memoria o referencias a parámetros obsoletos.
>     

#### 2. Actualizaciones In-Place con Slicing

> Actualización in-place propuesta: asignar a un tensor ya asignado usando slicing: `Y[:] = <expression>`.  
> Ejemplo con `zeros_like` para crear `Z` con la misma forma que `Y`, y luego sobrescribir su contenido sin cambiar el `id(Z)`.
> 
```python
Z = torch.zeros_like(Y)
Z[:] = X + Y
```

#### 3. Atajos In-Place con `+=`

> Si `X` no se reutiliza después, el fragmento sugiere `X[:] = X + Y` o `X += Y` para reducir overhead de memoria; en el ejemplo `X += Y` mantiene el mismo `id(X)`.

---

### VIII. Conversión a Otros Objetos de Python

#### 1. Interoperabilidad con NumPy

> Convertir entre tensor de PyTorch y array de NumPy es directo: `A = X.numpy()` y `B = torch.from_numpy(A)`.  
> El texto afirma que **comparten memoria subyacente**: una operación in-place sobre uno también cambia el otro.
> 
```python
A = X.numpy()
B = torch.from_numpy(A)
type(A), type(B)
```

#### 2. Conversión a Escalar Python

> Para un tensor de tamaño 1, se puede obtener un escalar con `item()` o con funciones built-in como `float()` e `int()`.
> 
```python
a = torch.tensor([3.5])
a, a.item(), float(a), int(a)
```

---

### IX. Resumen del Fragmento

#### 1. Qué Te Llevas

> El fragmento resume que la clase tensor es la interfaz principal para almacenar y manipular datos en librerías de deep learning, destacando:
> 
> - Rutinas de **construcción**.
>     
> - **Indexación** y **slicing**.
>     
> - Operaciones matemáticas básicas.
>     
> - **Broadcasting**.
>     
> - Asignación eficiente en memoria (**in-place**).
>     
> - Conversión hacia/desde otros objetos Python (p. ej., NumPy).
>     

#### 2. Checklist de Verificación Rápida

> Antes de dar por “controlada” esta parte, comprueba que puedes:
> 
> - Crear tensores con `arange`, `zeros`, `ones`, `randn`, y desde listas con `torch.tensor`.
>     
> - Explicar y usar `shape`, `numel`, `reshape` (incluyendo `-1`).
>     
> - Leer y escribir con indexación/slicing (incluyendo asignación por rangos).
>     
> - Distinguir operaciones elemento a elemento, concatenación con `cat`, y saber qué hace `X.sum()`.
>     
> - Describir el procedimiento de broadcasting en dos pasos y reconocer el patrón (3\times1 + 1\times2 \rightarrow 3\times2).
>     
> - Justificar por qué `+=` y `Y[:] = ...` ahorran memoria frente a `Y = Y + X` (según lo explicado con `id()`).
>     
> - Convertir entre PyTorch y NumPy y saber que comparten memoria (implicación: cuidado con in-place).
>     

---

## D2DpL 6. Builders Guide
### I. Contexto y Objetivo del Capítulo

#### 1. Rol del Software en Deep Learning

> El capítulo explica que, además de datos masivos y hardware potente, las **herramientas software** han sido claves en el progreso del deep learning: permiten **prototipar rápido**, reutilizar componentes estándar y mantener la opción de hacer modificaciones “de bajo nivel”.  
> También describe una evolución hacia **abstracciones cada vez más altas**: de pensar en neuronas → capas → bloques más gruesos (patrones repetidos de capas).

#### 2. Qué Cubre el Capítulo

> El objetivo es “levantar el capó” del framework para pasar de usuario final a “power user”. Se centra en:
> 
> - **Construcción de modelos**
>     
> - **Acceso e inicialización de parámetros**
>     
> - **Diseño de capas y bloques personalizados**
>     
> - **Guardar y cargar modelos**
>     
> - **Uso de GPUs** para acelerar cómputo  
>     Nota del material: no introduce nuevos modelos ni datasets, pero los capítulos avanzados dependen de estas técnicas.
>     

---

### II. Capas y Módulos

#### 1. De Neuronas a Módulos

> El material recalca que **neurona**, **capa** y **modelo completo** comparten la misma “plantilla” conceptual:
> 
> - (i) toman entradas
>     
> - (ii) producen salidas
>     
> - (iii) tienen parámetros ajustables (si aplica)  
>     Motivo para introducir **módulos**: en arquitecturas con cientos de capas (ej. ResNet-152) aparecen **patrones repetidos**; implementar capa a capa se vuelve tedioso.  
>     Idea clave: un **módulo** puede ser una capa, un bloque de varias capas o el modelo entero, y se pueden **componer recursivamente** para construir redes complejas con código compacto.
>     

#### 2. Qué Es un Módulo en PyTorch

> Desde el punto de vista de programación, un módulo es una **clase** (subclase de `nn.Module`) que:
> 
> - define `forward` (propagación hacia delante)
>     
> - almacena los parámetros necesarios (si los hay)  
>     El texto indica que no hace falta implementar backprop manualmente: gracias a **autodiferenciación**, normalmente solo te ocupas de `forward` y de declarar/guardar parámetros.
>     

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
> 
> 1. ingerir datos en `forward`
>     
> 2. devolver una salida (posiblemente con forma distinta)
>     
> 3. permitir gradientes respecto a la entrada (típicamente automático)
>     
> 4. almacenar y dar acceso a parámetros necesarios
>     
> 5. inicializar parámetros si hace falta  
>     Ejemplo: implementar un MLP como clase que hereda de `nn.Module`, definiendo `__init__` y `forward`.
>     

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

> Para entender `Sequential`, el material construye `MySequential` con dos ideas: (i) ir añadiendo módulos, y (ii) recorrerlos en `forward` en el orden de inserción.  
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
> 
> - una capa puede ser un módulo
>     
> - muchas capas pueden formar un módulo
>     
> - muchos módulos pueden formar un módulo
>     
> - un módulo puede contener código, y gestiona “housekeeping” (inicialización y backprop)
>     
> - concatenaciones secuenciales se manejan con `Sequential`  
>     Ejercicios propuestos: problemas de guardar módulos en listas Python, construir un “módulo paralelo” que concatene salidas, y una función fábrica para instanciar múltiples copias de una red.
>     

---

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

---

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

> El material propone una distribución “extraña” para cada peso (w):  
> [  
> w \sim  
> \begin{cases}  
> U(5,10) & \text{con prob. } \tfrac{1}{4} \  
> 0 & \text{con prob. } \tfrac{1}{2} \  
> U(-10,-5) & \text{con prob. } \tfrac{1}{4}  
> \end{cases}  
> ]  
> Luego implementa una función que inicializa con uniforme en ([-10,10]) y “enmascara” (pone a 0) los valores con (|w| < 5).  
> También remarca que siempre puedes **tocar parámetros directamente** vía `.data`.

#### 4. Resumen y Ejercicios

> Resumen del material: se puede inicializar con métodos **built-in** y **custom**.  
> Ejercicio: buscar en la documentación online más inicializadores incorporados.

---

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

---

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

---

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

---

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

---

### IX. Checklist de Repaso del Capítulo

#### 1. Dominio Mínimo Operativo

> Antes de “dar por controlado” este capítulo, asegúrate de poder:
> 
> - Explicar qué es un `Module` y por qué permite componer capas/bloques/modelos recursivamente.
>     
> - Implementar un módulo propio (constructor + `forward`) y razonar qué deja resuelto autograd.
>     
> - Acceder a parámetros con `state_dict`, atributos (`weight`, `bias`) y recorrerlos con `named_parameters`.
>     
> - Implementar o reconocer “tied parameters” (misma capa reutilizada) y entender qué implica para gradientes.
>     
> - Aplicar inicialización con `net.apply(...)` y distinguir built-in vs custom (incluida la idea de enmascarar pesos).
>     
> - Explicar “lazy initialization”: cuándo aparecen parámetros no inicializados y cómo se inicializan tras el primer forward.
>     
> - Diseñar capas custom sin parámetros y con parámetros usando `nn.Parameter`.
>     
> - Guardar/cargar tensores y guardar/cargar parámetros de modelos con `state_dict` (arquitectura reconstruida en código).
>     
> - Trabajar con devices: crear tensores/modelos en GPU, mover datos, y justificar por qué minimizar transferencias es crítico.

## D2DpL 3. Linear Neural Networks for Regression
### I. Redes Neuronales Lineales para Regresión

#### 1. Motivación y Alcance del Capítulo

> Antes de hacer redes “profundas”, el material propone implementar **redes poco profundas** donde las entradas conectan directamente con las salidas, para centrarse en lo esencial del entrenamiento: **parametrizar la capa de salida**, **manejar datos**, **definir una pérdida** y **entrenar**.  
> También justifica estudiar modelos lineales (p. ej., regresión lineal) porque son **métodos clásicos** muy usados como **baselines** al justificar arquitecturas más complejas.

#### 2. Problema de Regresión y Terminología

> La **regresión** busca predecir un **valor numérico** (ejemplos: precios de casas, stocks, demanda, etc.).  
> En terminología de ML:
> 
> - **Training Set**: dataset de entrenamiento.
>     
> - **Example / Sample**: cada fila.
>     
> - **Label / Target**: lo que se predice.
>     
> - **Features / Covariates**: variables de entrada usadas para predecir.
>     

#### 3. Supuestos y Notación

> Regresión lineal parte de supuestos: relación aproximadamente lineal entre features (x) y target (y), y desviaciones debidas a **ruido** (habitualmente modelado como Gaussiano).  
> Notación: (n) ejemplos; superíndices para enumerar ejemplos/targets; subíndices para coordenadas. En concreto, (x^{(i)}) es el ejemplo (i)-ésimo y (x^{(i)}_j) su coordenada (j).

#### 4. Modelo Lineal

> Para un ejemplo, el modelo es una función afín ( \hat{y} = w^\top x + b).  
> Para el dataset completo, se usa la **matriz de diseño** (X \in \mathbb{R}^{n \times d}) y las predicciones se expresan como:  
> [  
> \hat{y} = Xw + b \quad (3.1.4)  
> ]  
> donde al sumar un vector y un escalar se aplica **broadcasting**.

#### 5. Función de Pérdida y Objetivo

> La pérdida típica en regresión es el **error cuadrático** (squared error). Para un ejemplo (i):  
> [  
> l^{(i)}(w,b) = \frac{1}{2}(\hat{y}^{(i)} - y^{(i)})^2 \quad (3.1.5)  
> ]  
> La constante (1/2) es “conveniente” porque se cancela al derivar.  
> El error empírico medio sobre el training set:  
> [  
> L(w,b)=\frac{1}{n}\sum_{i=1}^{n} l^{(i)}(w,b)  
> =\frac{1}{n}\sum_{i=1}^{n}\frac{1}{2}(w^\top x^{(i)}+b-y^{(i)})^2 \quad (3.1.6)  
> ]  
> Objetivo de entrenamiento:  
> [  
> (w^*,b^*)=\arg\min_{w,b} L(w,b) \quad (3.1.7)  
> ]

#### 6. Solución Analítica (Normal Equation)

> En regresión lineal puede obtenerse una solución analítica (en training), derivando y anulando el gradiente:  
> [  
> \partial_w \lVert y - Xw\rVert^2 = 2X^\top(Xw-y)=0 \Rightarrow X^\top y = X^\top X w \quad (3.1.8)  
> ]  
> y por tanto:  
> [  
> w^*=(X^\top X)^{-1}X^\top y \quad (3.1.9)  
> ]  
> La unicidad requiere que (X^\top X) sea invertible (columnas de (X) linealmente independientes / full rank).  
> El material avisa: no hay que “acostumbrarse” a soluciones analíticas; en deep learning casi siempre entrenaremos con métodos iterativos.

#### 7. Descenso de Gradiente Estocástico por Minibatches

> El capítulo contrasta: **full-batch gradient descent** (lento porque requiere pasar por todo el dataset antes de cada update) vs **SGD** (un ejemplo por update, con inconvenientes computacionales/estadísticos).  
> Solución intermedia: **minibatches** (típicamente tamaño entre 32 y 256, preferiblemente múltiplo de una potencia de 2).  
> Regla de actualización (minibatch SGD):  
> [  
> (w,b)\leftarrow (w,b) - \eta \frac{1}{|B|}\sum_{i\in B_t}\partial_{(w,b)},l^{(i)}(w,b)\quad (3.1.10)  
> ]  
> Para pérdidas cuadráticas y transformaciones afines, el material da la expansión cerrada:  
> [  
> w \leftarrow w - \frac{\eta}{|B|}\sum_{i\in B_t} x^{(i)}(w^\top x^{(i)}+b-y^{(i)})  
> ]  
> [  
> b \leftarrow b - \frac{\eta}{|B|}\sum_{i\in B_t} (w^\top x^{(i)}+b-y^{(i)}) \quad (3.1.11)  
> ]  
> El texto introduce el término **hiperparámetros** para parámetros fijados por el usuario (p. ej., (\eta), (|B|)) y comenta que la calidad suele evaluarse en un **validation set** separado.

#### 8. Predicción y Generalización

> Tras entrenar, se usan (\hat{w},\hat{b}) para **predecir** etiquetas de ejemplos no vistos. El material recomienda usar “prediction” y advierte que “inference” se usa con significados distintos en otras literaturas, lo cual puede crear confusión.  
> El texto introduce **generalization** como el reto de predecir bien en datos no vistos.

#### 9. Vectorización para Velocidad

> Entrenar suele procesar **minibatches completos**: para ser eficiente hay que **vectorizar** y aprovechar librerías rápidas de álgebra lineal, evitando bucles `for` en Python.  
> El material muestra un microbenchmark sumando dos vectores (10k dims): un bucle tarda órdenes de magnitud más que `a + b`.  
> Beneficios mencionados: speedups de orden de magnitud, menos cálculos manuales, menos errores y más portabilidad.

#### 10. Distribución Normal y Pérdida Cuadrática

> El capítulo conecta regresión lineal con la **Normal/Gaussiana**. Define la densidad:  
> [  
> p(x)=\frac{1}{\sqrt{2\pi\sigma^2}}\exp\left(-\frac{1}{2\sigma^2}(x-\mu)^2\right)\quad (3.1.12)  
> ]  
> Asume un modelo de observación con ruido gaussiano:  
> [  
> y = w^\top x + b + \epsilon,\quad \epsilon\sim \mathcal{N}(0,\sigma^2)\quad (3.1.13)  
> ]  
> Con máxima verosimilitud, se minimiza el **negative log-likelihood**; si (\sigma) es fijo, la parte relevante queda proporcional al **squared error**, por lo que **minimizar MSE equivale a MLE** bajo ruido gaussiano aditivo.

#### 11. Regresión Lineal Como Red Neuronal

> El material representa la regresión lineal como una **red neuronal de una sola capa fully-connected**: cada feature es una neurona de entrada conectada al output.  
> Se menciona la Fig. 3.1.2: patrón de conectividad (no valores concretos de pesos/bias).

#### 12. Biología (Analogía)

> Se incluye una analogía con neuronas biológicas (Fig. 3.1.3): dendritas reciben inputs (x_i), sinapsis ponderan con (w_i), se agrega como suma ponderada (y=\sum_i x_i w_i + b), y puede aplicarse no linealidad (\sigma(y)).

---

### II. Diseño Orientado a Objetos para Implementación

#### 1. Idea General de la API

> El material propone una **arquitectura orientada a objetos** para estructurar implementaciones, porque los mismos componentes (data, modelo, pérdida, optimización) reaparecen continuamente.  
> Diseño a alto nivel: tres clases:
> 
> - `Module`: modelos, pérdidas y optimización.
>     
> - `DataModule`: data loaders (train/val).
>     
> - `Trainer`: combina ambos y ejecuta entrenamiento.
>     

#### 2. Utilidades para Notebooks: `add_to_class` y `HyperParameters`

> Problema en notebooks: las definiciones de clases largas dañan la legibilidad; solución: añadir métodos a una clase después de definirla con un decorador `add_to_class`.  
> `HyperParameters` guarda argumentos de `__init__` como atributos mediante `save_hyperparameters(...)` (implementación diferida a una sección posterior).  
> Se muestra que puede ignorar ciertos argumentos (`ignore=[...]`).

#### 3. Clase `Module`

> `Module` (base de modelos) requiere, como mínimo: almacenar parámetros en `__init__`, un `training_step` que devuelve pérdida para un batch, y `configure_optimizers` que devuelve el optimizador; opcionalmente `validation_step`.  
> Es subclase de `nn.Module`; llamar `a(X)` invoca `forward` vía `__call__`.

#### 4. Clase `DataModule`

> `DataModule` encapsula preparación/lectura de datos: `train_dataloader` y `val_dataloader` devuelven generadores de batches; `get_dataloader(train)` define el comportamiento.

#### 5. Clase `Trainer`

> `Trainer.fit(model, data)` itera `max_epochs` y coordina: preparar datos, preparar modelo y ejecutar el loop por épocas (la implementación se va enriqueciendo más adelante).  
> En el resumen se remarca que las implementaciones completas se guardan en la librería D2L para favorecer modularidad (cambiar optimizador/modelo/dataset sin reescribir todo).

---

### III. Datos Sintéticos para Regresión

#### 1. Por Qué Usar Datos Sintéticos

> Aunque no importen “intrínsecamente” los patrones artificiales, sirven para docencia: evaluar algoritmos y verificar que la implementación recupera parámetros conocidos a priori.

#### 2. Generación del Dataset

> Se generan (1000) ejemplos con (2) features (X \in \mathbb{R}^{1000\times 2}) muestreadas de una normal estándar, y labels con:  
> [  
> y = Xw + b + \epsilon \quad (3.3.1)  
> ]  
> con (\epsilon\sim \mathcal{N}(0, 0.01^2)).  
> Se implementa como `SyntheticRegressionData`, subclase de `d2l.DataModule`, guardando hiperparámetros con `save_hyperparameters()`.

```python
class SyntheticRegressionData(d2l.DataModule): #@save
    """Synthetic data for linear regression."""
    def __init__(self, w, b, noise=0.01, num_train=1000, num_val=1000,
                 batch_size=32):
        super().__init__()
        self.save_hyperparameters()
        n = num_train + num_val
        self.X = torch.randn(n, len(w))
        noise = torch.randn(n, 1) * noise
        self.y = torch.matmul(self.X, w.reshape((-1, 1))) + b + noise
```

#### 3. Lectura del Dataset y Minibatches

> Entrenar requiere múltiples pasadas; se implementa `get_dataloader(train)` que: en train **baraja índices** y en valid usa un orden determinista, y va devolviendo minibatches `(X_batch, y_batch)`.

```python
@d2l.add_to_class(SyntheticRegressionData)
def get_dataloader(self, train):
    if train:
        indices = list(range(0, self.num_train))
        random.shuffle(indices)
    else:
        indices = list(range(self.num_train, self.num_train + self.num_val))
    for i in range(0, len(indices), self.batch_size):
        batch_indices = torch.tensor(indices[i: i + self.batch_size])
        yield self.X[batch_indices], self.y[batch_indices]
```

#### 4. Data Loader Conciso con API del Framework

> La iteración manual es didáctica pero ineficiente (carga en memoria + accesos aleatorios). Se propone usar `TensorDataset` + `DataLoader` y encapsularlo en `get_tensorloader(...)`, más eficiente y con utilidades extra como `__len__`.

```python
@d2l.add_to_class(d2l.DataModule) #@save
def get_tensorloader(self, tensors, train, indices=slice(0, None)):
    tensors = tuple(a[indices] for a in tensors)
    dataset = torch.utils.data.TensorDataset(*tensors)
    return torch.utils.data.DataLoader(dataset, self.batch_size, shuffle=train)

@d2l.add_to_class(SyntheticRegressionData) #@save
def get_dataloader(self, train):
    i = slice(0, self.num_train) if train else slice(self.num_train, None)
    return self.get_tensorloader((self.X, self.y), train, i)
```

---

### IV. Implementación de Regresión Lineal desde Cero

#### 1. Definición del Modelo y Parámetros

> Se define `LinearRegressionScratch` como subclase de `d2l.Module`. Inicializa:
> 
> - (w\sim \mathcal{N}(0,\sigma^2)) con (\sigma=0.01) por defecto.
>     
> - (b=0).
>     
> - Ambos con `requires_grad=True`.  
>     El forward implementa (Xw + b) y usa broadcasting al sumar el escalar (b) al vector.
>     

```python
class LinearRegressionScratch(d2l.Module): #@save
    """The linear regression model implemented from scratch."""
    def __init__(self, num_inputs, lr, sigma=0.01):
        super().__init__()
        self.save_hyperparameters()
        self.w = torch.normal(0, sigma, (num_inputs, 1), requires_grad=True)
        self.b = torch.zeros(1, requires_grad=True)

@d2l.add_to_class(LinearRegressionScratch) #@save
def forward(self, X):
    return torch.matmul(X, self.w) + self.b
```

#### 2. Definición de la Pérdida

> Se usa squared loss (3.1.5). En la implementación se ajusta la forma de (y) para que coincida con (y_{\hat{}}) y se devuelve la pérdida media del minibatch.

```python
@d2l.add_to_class(LinearRegressionScratch) #@save
def loss(self, y_hat, y):
    l = (y_hat - y) ** 2 / 2
    return l.mean()
```

#### 3. Algoritmo de Optimización: SGD

> Aunque regresión lineal tenga solución cerrada, aquí se usa minibatch SGD para enseñar el patrón general de entrenamiento de redes.  
> Como la pérdida es media sobre minibatch, el material indica que no hace falta ajustar el learning rate por batch size en esta implementación.  
> Se define una clase `SGD` con `step()` y `zero_grad()` (poner gradientes a cero antes del backprop).

```python
class SGD(d2l.HyperParameters): #@save
    """Minibatch stochastic gradient descent."""
    def __init__(self, params, lr):
        self.save_hyperparameters()
    def step(self):
        for param in self.params:
            param -= self.lr * param.grad
    def zero_grad(self):
        for param in self.params:
            if param.grad is not None:
                param.grad.zero_()

@d2l.add_to_class(LinearRegressionScratch) #@save
def configure_optimizers(self):
    return SGD([self.w, self.b], self.lr)
```

#### 4. Entrenamiento: Bucle por Épocas

> En cada epoch se recorre el train dataloader completo (pasar una vez por todos los ejemplos, asumiendo divisibilidad por batch size). En cada iteración: calcular pérdida, backprop, update.  
> El material registra `prepare_batch` y `fit_epoch` en `d2l.Trainer`; también pasa por validación una vez por epoch si hay `val_dataloader`.  
> Se menciona que (\text{lr}) y `max_epochs` son hiperparámetros, y que “en general” conviene un split en tres partes (train / selección de hiperparámetros / evaluación final), aunque aquí se omite por simplicidad.

```python
@d2l.add_to_class(d2l.Trainer) #@save
def prepare_batch(self, batch):
    return batch

@d2l.add_to_class(d2l.Trainer) #@save
def fit_epoch(self):
    self.model.train()
    for batch in self.train_dataloader:
        loss = self.model.training_step(self.prepare_batch(batch))
        self.optim.zero_grad()
        with torch.no_grad():
            loss.backward()
            if self.gradient_clip_val > 0:
                self.clip_gradients(self.gradient_clip_val, self.model)
            self.optim.step()
        self.train_batch_idx += 1
    if self.val_dataloader is None:
        return
    self.model.eval()
    for batch in self.val_dataloader:
        with torch.no_grad():
            self.model.validation_step(self.prepare_batch(batch))
        self.val_batch_idx += 1
```

#### 5. Evaluación Cualitativa (Parámetros Verdaderos vs Aprendidos)

> Como los datos son sintéticos, se conocen los parámetros verdaderos; se propone comparar con los aprendidos para verificar que el entrenamiento “recupera” valores cercanos.  
> El material matiza: en general (y más aún en modelos profundos) no suele haber soluciones únicas; en ML importa más predecir bien que recuperar “parámetros verdaderos”.

---

### V. Implementación Concisa de Regresión Lineal

#### 1. Motivación: APIs de Alto Nivel

> El material atribuye parte del “boom” del deep learning a herramientas open-source y a frameworks modernos (autodiferenciación + conveniencia de Python) que automatizan componentes repetitivos (data iterators, losses, optimizers, layers).

#### 2. Modelo con Capas Predefinidas

> Para operaciones estándar se usa una capa fully-connected predefinida (en PyTorch: `Linear`/`LazyLinear`). El texto recomienda `LazyLinear` para evitar especificar shapes de entrada.  
> `LinearRegression` usa `nn.LazyLinear(1)` y fija inicialización: pesos (\sim \mathcal{N}(0, 0.01)), bias a 0.

```python
class LinearRegression(d2l.Module): #@save
    """The linear regression model implemented with high-level APIs."""
    def __init__(self, lr):
        super().__init__()
        self.save_hyperparameters()
        self.net = nn.LazyLinear(1)
        self.net.weight.data.normal_(0, 0.01)
        self.net.bias.data.fill_(0)

@d2l.add_to_class(LinearRegression) #@save
def forward(self, X):
    return self.net(X)
```

#### 3. Pérdida con `MSELoss`

> `MSELoss` computa MSE (sin el factor (1/2) de (3.1.5)) y por defecto promedia sobre ejemplos; el material dice que es más rápido y más fácil que implementarla a mano.

```python
@d2l.add_to_class(LinearRegression) #@save
def loss(self, y_hat, y):
    fn = nn.MSELoss()
    return fn(y_hat, y)
```

#### 4. Optimización con `torch.optim.SGD`

> Para optimizar se instancia `torch.optim.SGD` sobre `self.parameters()` y el learning rate.

```python
@d2l.add_to_class(LinearRegression) #@save
def configure_optimizers(self):
    return torch.optim.SGD(self.parameters(), self.lr)
```

#### 5. Entrenamiento

> El material recalca que, aunque el modelo y componentes auxiliares se simplifican, el **training loop** sigue la misma estructura (se llama a `fit`, apoyándose en `fit_epoch`).

---

### VI. Generalización

#### 1. Error de Entrenamiento y Error de Generalización

> En aprendizaje supervisado estándar, el material asume que datos de **entrenamiento** y **test** se extraen de manera independiente de la **misma distribución** (supuesto **IID**). Sin este tipo de supuesto, no habría base para extrapolar de (P(X,Y)) a otra distribución (Q(X,Y)).
> 
> Diferencia clave:
> 
> - **Error de entrenamiento** (R_{\text{emp}}): estadístico calculado sobre el dataset de entrenamiento.
>     
> - **Error de generalización** (R): **esperanza** respecto a la distribución subyacente (P); intuitivamente, lo que verías sobre un “flujo infinito” de datos nuevos de la misma distribución.
>     
> 
> Definiciones formales (misma notación que en la Sección 3.1):  
> [  
> R_{\text{emp}}[X,y,f] = \frac{1}{n}\sum_{i=1}^{n} l\big(x^{(i)}, y^{(i)}, f(x^{(i)})\big) \quad (3.6.1)  
> ]  
> [  
> R[p,f] = \mathbb{E}_{(x,y)\sim P},[l(x,y,f(x))] = \int!!\int l(x,y,f(x)),p(x,y),dx,dy \quad (3.6.2)  
> ]
> 
> Problema práctico: **no podemos calcular (R) exactamente** (no conocemos (p(x,y)) y no podemos muestrear infinitos datos). Por eso se estima aplicando el modelo a un **test set independiente** (o conjunto retenido) usando la misma fórmula que para el error empírico.
> 
> Matiz importante: al evaluar en test, el clasificador/modelo se considera **fijo** (no depende de la muestra de test), así que estimar su error es “solo” un problema de **estimar una media**; en cambio, el modelo sí depende del training set, y por eso el training error suele ser un **estimador sesgado** del error poblacional.

#### 2. Complejidad del Modelo y Por Qué el Training Error No Basta

> En teoría “clásica”, con modelos simples y datos abundantes, training y generalization tienden a estar cerca; con modelos más complejos y/o menos datos, esperas que el training error baje pero que crezca el **generalization gap**.
> 
> Caso extremo: si tu clase de modelos puede ajustar **etiquetas arbitrarias** (incluso aleatorias), entonces encajar perfecto el training set no te permite concluir nada fiable sobre generalización (podrías estar cerca de “adivinar al azar” fuera de muestra).
> 
> Mensaje fuerte del material: **bajo training error no implica necesariamente bajo error de generalización**, pero tampoco implica necesariamente que generalice mal; lo único seguro es que el training error por sí solo **no certifica** generalización. En modelos muy potentes (menciona deep nets), hay que apoyarse más en datos retenidos; el error sobre holdout/validation se llama **validation error**.
> 
> Sobre “qué es complejidad”: no es trivial. A veces más parámetros ⇒ más capacidad de ajustar etiquetas arbitrarias, pero no siempre (ej.: kernel methods con infinitos parámetros controlados por otros medios). Una noción útil es el **rango de valores** que pueden tomar los parámetros.
> 
> El material conecta esto con la idea de **falsabilidad** (Popper): una hipótesis que explica “cualquier cosa” no informa realmente sobre el mundo; preferimos hipótesis que podrían fallar en principio pero que aun así encajan los datos observados.

#### 3. Underfitting u Overfitting

> Al comparar **training error** vs **validation error**, el material destaca dos situaciones comunes:
> 
> - **Underfitting**: training y validation son ambos altos, con **poca brecha**. Si el modelo no logra bajar el training error, suele indicar que es demasiado **simple / poco expresivo**; como el gap ((R_{\text{emp}}-R)) es pequeño, “podrías permitirte” un modelo más complejo.
>     
> - **Overfitting**: training mucho más bajo que validation, indicando un gap grande.
>     
> 
> Matiz del material: overfitting **no siempre es “malo”**; a menudo (especialmente en deep learning) los mejores modelos predicen mucho mejor en training que en holdout. Lo importante es bajar el **error de generalización**; el gap importa en la medida en que impida ese objetivo. Si el training error es 0, entonces el gap coincide exactamente con el error de generalización y solo avanzas reduciendo el gap.

#### 4. Ajuste de Curvas Polinómicas Como Ejemplo

> Para ilustrar intuición clásica sobre complejidad y overfitting, el material propone **regresión polinómica** con una sola feature (x):  
> [  
> \hat{y}=\sum_{i=0}^{d} x^i w_i \quad (3.6.3)  
> ]
> 
> Interpretación: es regresión lineal donde las features son (x^i), los pesos son (w_i) y el sesgo es (w_0) porque (x^0=1). Se puede usar squared error como loss.
> 
> Relación grado–complejidad: un polinomio de mayor grado es más complejo (más parámetros y mayor “rango de selección” de funciones). Con el training set fijo, aumentar el grado no empeora el training error (como mucho lo deja igual). Además, si cada ejemplo tiene un (x) distinto, un polinomio con grado igual al número de ejemplos puede ajustar el training set perfectamente.

#### 5. Tamaño del Dataset

> A igualdad de modelo: con **menos muestras** es más probable (y más severo) el overfitting; al aumentar datos, típicamente baja el error de generalización, y “en general, más datos nunca perjudican”.
> 
> Regla cualitativa del material: para una tarea y distribución fijadas, la complejidad del modelo no debería crecer más rápido que la cantidad de datos; con más datos puedes intentar modelos más complejos, pero sin datos suficientes es difícil batir modelos simples. Menciona que en muchas tareas deep learning supera a modelos lineales cuando hay **muchos miles** de ejemplos, y atribuye parte del éxito actual a la disponibilidad de datasets masivos.

#### 6. Selección de Modelos

> En la práctica, se elige el modelo final tras comparar varios que difieren en arquitectura, objetivo, features, preprocesado, learning rates, etc.; a esto se le llama **model selection**.
> 
> Principio: **no se debe tocar el test set** hasta haber fijado todos los hiperparámetros; si lo usas para seleccionar, puedes “sobreajustar el test” y entonces pierdes el árbitro final.
> 
> Pero tampoco basta con training para seleccionar, porque no puedes estimar generalización sobre los mismos datos con los que entrenas. Por eso se introduce un **validation set** adicional (split en tres: train/val/test).
> 
> Nota práctica del material: en el mundo real el test se reutiliza con frecuencia, y las fronteras entre validation y test pueden volverse ambiguas. En los experimentos del libro (si no se dice lo contrario), en realidad se trabaja con **training + validation**, sin “true test set”; por tanto, la “accuracy” reportada es realmente **validation accuracy**, no test accuracy.

#### 7. Validación Cruzada

> Si el training data es escaso y no puedes reservar suficiente validation, una solución popular es **(K)-fold cross-validation**:
> 
> - dividir el training original en (K) subconjuntos no solapados
>     
> - repetir (K) veces: entrenar con (K-1) folds y validar en el fold restante
>     
> - estimar training y validation errors promediando sobre los (K) experimentos
>     

#### 8. Resumen de la Sección

> Reglas “de pulgar” que deja el material:
> 
> 1. Usar validation sets (o (K)-fold cross-validation) para model selection.
>     
> 2. Modelos más complejos suelen requerir más datos.
>     
> 3. Nociones relevantes de complejidad incluyen número de parámetros **y** el rango de valores permitidos.
>     
> 4. Manteniendo lo demás igual, más datos casi siempre mejoran generalización.
>     
> 5. Todo este discurso presupone el supuesto IID; si hay shift entre train y test, no puedes decir nada sin suposiciones adicionales.
>     

#### 9. Ejercicios Propuestos

> El material propone, entre otros: cuándo se puede resolver exactamente regresión polinómica; ejemplos donde IID no aplica; cuándo esperar training error 0 o generalization error 0; por qué (K)-fold es caro y por qué su estimación puede estar sesgada; y reflexiones sobre VC dimension como medida de complejidad.

---

### VII. Decaimiento de Pesos

#### 1. Actualización con Penalización (\ell_2) y “Weight Decay”

> El material contrasta (\ell_2) vs (\ell_1): las penalizaciones (\ell_1) tienden a concentrar pesos en pocas features (selección de variables), mientras que (\ell_2) “encoge” pesos de forma continua.  
> Para regresión con regularización (\ell_2), da el update de SGD:  
> [  
> w \leftarrow (1-\eta\lambda)w - \frac{\eta}{|B|}\sum_{i\in B} x^{(i)}(w^\top x^{(i)}+b-y^{(i)})\quad (3.7.3)  
> ]  
> Interpretación del texto: además del término de ajuste por error, se **reduce** (w) hacia 0, de ahí el nombre **weight decay**. (\lambda) controla la fuerza de la restricción: menor (\lambda) → menos constrain; mayor (\lambda) → más constrain.  
> Se comenta que regularizar el bias puede variar; a menudo no se regulariza.

#### 2. Ejemplo Sintético de Alta Dimensión

> Se ilustra el beneficio con un caso sintético:  
> [  
> y = 0.05 + \sum_{i=1}^{d} 0.01 x_i + \epsilon,\quad \epsilon\sim \mathcal{N}(0,0.01^2)\quad (3.7.4)  
> ]  
> El ejemplo fuerza overfitting aumentando dimensionalidad a (d=200) y usando un training set pequeño (20 ejemplos).

```python
class Data(d2l.DataModule):
    def __init__(self, num_train, num_val, num_inputs, batch_size):
        self.save_hyperparameters()
        n = num_train + num_val
        self.X = torch.randn(n, num_inputs)
        noise = torch.randn(n, 1) * 0.01
        w, b = torch.ones((num_inputs, 1)) * 0.01, 0.05
        self.y = torch.matmul(self.X, w) + b + noise
    def get_dataloader(self, train):
        i = slice(0, self.num_train) if train else slice(self.num_train, None)
        return self.get_tensorloader([self.X, self.y], train, i)
```

#### 3. Contenido Parcial del Resto de la Sección

> El fragmento recuperado indica que después se aborda la “Implementation from Scratch” añadiendo la penalización (\ell_2) a la pérdida original, pero **no dispongo aquí del texto completo** para detallarlo paso a paso.

---

### VIII. Checklist de Verificación

#### 1. Lo Que Deberías Poder Hacer Tras Este Fragmento

> - Formular el modelo ( \hat{y}=w^\top x + b ) y su forma matricial ( \hat{y}=Xw+b ).
>     
> - Escribir y justificar la squared loss (3.1.5) y el objetivo empírico (3.1.6–3.1.7).
>     
> - Derivar/interpretar la solución analítica (3.1.8–3.1.9) y su condición de full rank.
>     
> - Explicar minibatch SGD y escribir updates (3.1.10–3.1.11).
>     
> - Justificar por qué vectorizar acelera (benchmark bucle vs `a + b`).
>     
> - Explicar la equivalencia MSE ↔ MLE bajo ruido gaussiano.
>     
> - Implementar (o entender) `SyntheticRegressionData`, `LinearRegressionScratch` y la versión concisa con `LazyLinear`, `MSELoss`, `torch.optim.SGD`.
>     
> - Interpretar “weight decay” como encogimiento de (w) y reconocer el update (3.7.3).
>     

---

Si quieres, en el siguiente mensaje puedo **reintentar** extraer la Sección 3.6 (Generalization) y completar esa parte manteniendo el mismo formato (sin cambiar nada del resto).