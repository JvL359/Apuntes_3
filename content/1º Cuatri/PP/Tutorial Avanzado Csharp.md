### II. C\# Avanzado

1. Colecciones
> Las **colecciones** son estructuras de datos que permiten **almacenar y organizar varios valores** bajo una sola variable. A diferencia de las variables simples, que solo guardan un valor, las colecciones agrupan muchos datos, facilitando su manipulación.
> En C# existen diferentes tipos de colecciones, cada una con sus ventajas y casos de uso.
###### 1.1. Arrays
> Un **array** es una colección de tamaño fijo que almacena varios elementos del mismo tipo en posiciones consecutivas de memoria. Cada elemento se accede mediante un **índice** que empieza en 0. Son útiles cuando sabemos de antemano cuántos elementos vamos a manejar.
```cs
using System;

class Program
{
    static void Main()
    {
        int[] numeros = new int[5]; // Array de tamaño fijo
        numeros[0] = 10;
        numeros[1] = 20;
        numeros[2] = 30;
        numeros[3] = 40;
        numeros[4] = 50;

        Console.WriteLine("Contenido del array:");
        for (int i = 0; i < numeros.Length; i++)
        {
            Console.WriteLine(numeros[i]);
        }
    }
}
```
###### 1.2. Matrices Multidimensionales
> Las **matrices multidimensionales** son arrays con más de una dimensión, como tablas o cuadrículas. En C#, se representan con varias comas dentro de los corchetes (`[,]`). Son muy útiles para trabajar con datos organizados en filas y columnas, como tableros o tablas numéricas.
```cs
using System;

class Program
{
    static void Main()
    {
        int[,] matriz = new int[2, 3] 
        {
            {1, 2, 3},
            {4, 5, 6}
        };

        Console.WriteLine("Matriz 2x3:");
        for (int fila = 0; fila < 2; fila++)
        {
            for (int col = 0; col < 3; col++)
            {
                Console.Write(matriz[fila, col] + " ");
            }
            Console.WriteLine();
        }
    }
}
```
###### 1.3. Matrices Escalonadas (Jagged Arrays)
> Una **matriz escalonada** es un array de arrays, lo que significa que cada fila puede tener un tamaño diferente. Esto permite representar estructuras irregulares, como una lista de listas en la que cada elemento contiene una colección con distinta cantidad de datos.
```cs
using System;

class Program
{
    static void Main()
    {
        int[][] jagged = new int[3][]; 
        jagged[0] = new int[] { 1, 2 };
        jagged[1] = new int[] { 3, 4, 5 };
        jagged[2] = new int[] { 6 };

        Console.WriteLine("Matriz escalonada:");
        for (int i = 0; i < jagged.Length; i++)
        {
            Console.Write("Fila " + i + ": ");
            for (int j = 0; j < jagged[i].Length; j++)
            {
                Console.Write(jagged[i][j] + " ");
            }
            Console.WriteLine();
        }
    }
}
```
###### 1.4. Listas
> Una **lista** (`List<T>`) es una colección dinámica que puede cambiar de tamaño en tiempo de ejecución. A diferencia de los arrays, no necesitamos indicar su longitud al declararla. Permiten agregar, eliminar y recorrer elementos de forma flexible, siendo una de las colecciones más utilizadas en C#.
```cs
using System;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        List<string> frutas = new List<string>();
        frutas.Add("Manzana");
        frutas.Add("Banana");
        frutas.Add("Naranja");

        Console.WriteLine("Lista de frutas:");
        foreach (string fruta in frutas)
        {
            Console.WriteLine(fruta);
        }

        frutas.Remove("Banana"); // Eliminar elemento
        Console.WriteLine("\nDespués de eliminar Banana:");
        frutas.ForEach(Console.WriteLine);
    }
}
```
###### 1.5. Diccionarios
> Un **diccionario** es una colección que almacena pares **clave–valor**. Las claves deben ser únicas y permiten acceder rápidamente a los valores asociados. Son ideales cuando queremos buscar datos de forma eficiente, como consultar el nombre de un estudiante a partir de su ID.
```cs
using System;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        Dictionary<int, string> estudiantes = new Dictionary<int, string>();
        estudiantes.Add(1, "Ana");
        estudiantes.Add(2, "Luis");
        estudiantes.Add(3, "Marta");

        Console.WriteLine("Diccionario de estudiantes:");
        foreach (var par in estudiantes)
        {
            Console.WriteLine($"ID: {par.Key}, Nombre: {par.Value}");
        }

        Console.WriteLine("\nAcceso por clave -> ID 2:");
        Console.WriteLine(estudiantes[2]);
    }
}
```
###### 1.6. Bucle Foreach
> El **bucle `foreach`** permite recorrer los elementos de una colección de manera sencilla, sin necesidad de usar índices. Se utiliza mucho en arrays, listas y diccionarios, ya que simplifica el código y hace que sea más legible al iterar sobre los datos.
```cs
using System;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        string[] colores = { "Rojo", "Verde", "Azul" };

        Console.WriteLine("Array con foreach:");
        foreach (string color in colores)
        {
            Console.WriteLine(color);
        }

        List<int> numeros = new List<int> { 1, 2, 3, 4, 5 };

        Console.WriteLine("\nLista con foreach:");
        foreach (int n in numeros)
        {
            Console.WriteLine(n);
        }
    }
}
```

2. Clases Avanzadas
> En C#, las **clases** son el corazón de la programación orientada a objetos. Una vez dominados los fundamentos (campos, constructores, herencia), es importante conocer características más avanzadas que permiten escribir **código más limpio, seguro y flexible**. Entre estas se incluyen:
> - **Propiedades**, para controlar cómo se accede a los datos internos.
> - **Miembros estáticos**, que pertenecen a la clase en lugar de a un objeto específico.
> - **Interfaces**, que definen contratos para garantizar que diferentes clases implementen ciertos métodos.
> - **Clases genéricas**, que permiten escribir código reutilizable para distintos tipos de datos.
> Estas herramientas enriquecen el diseño y hacen que el código sea más escalable y mantenible.
###### 2.1. Propiedades: Getters y Setter modernos
> Las **propiedades** son una forma moderna y segura de exponer campos privados de una clase. Reemplazan a los antiguos _getters_ y _setters_, permitiendo leer (`get`) o modificar (`set`) un valor de forma controlada. Pueden ser automáticas (sin lógica extra) o personalizadas (con validaciones). Mejoran la **encapsulación** y la legibilidad del código.
```cs
using System;

class Persona
{
    // Propiedad automática
    public string Nombre { get; set; }

    // Propiedad con lógica en el setter
    private int edad;
    public int Edad
    {
        get { return edad; }
        set
        {
            if (value >= 0) edad = value;
        }
    }
}

class Program
{
    static void Main()
    {
        Persona p = new Persona();
        p.Nombre = "Ana";
        p.Edad = 25;

        Console.WriteLine($"{p.Nombre}, {p.Edad} años");
    }
}
```
###### 2.2. Miembros estáticos (Static)
> Los miembros **estáticos** (`static`) pertenecen a la **clase** y no a las instancias. Esto significa que se pueden usar sin necesidad de crear un objeto. Son útiles para representar comportamientos o datos globales que no dependen de cada objeto, como en el caso de una clase `Calculadora` con métodos matemáticos.
```cs
using System;

class Calculadora
{
    // Método estático
    public static int Sumar(int a, int b)
    {
        return a + b;
    }
}

class Program
{
    static void Main()
    {
        // No hace falta instanciar la clase
        int resultado = Calculadora.Sumar(5, 7);
        Console.WriteLine("Resultado: " + resultado);
    }
}
```
###### 2.3. Interfaces
> Una **interfaz** define un **contrato** que especifica qué métodos debe implementar una clase, pero sin dar detalles de su funcionamiento. Permiten que distintas clases compartan una misma interfaz y se utilicen de forma uniforme, favoreciendo el **polimorfismo** y el diseño modular. En C#, una clase puede implementar varias interfaces, lo que aumenta la flexibilidad.
```cs
using System;

interface IVehiculo
{
    void Conducir();
}

class Coche : IVehiculo
{
    public void Conducir()
    {
        Console.WriteLine("Conduciendo un coche...");
    }
}

class Moto : IVehiculo
{
    public void Conducir()
    {
        Console.WriteLine("Conduciendo una moto...");
    }
}

class Program
{
    static void Main()
    {
        IVehiculo v1 = new Coche();
        IVehiculo v2 = new Moto();

        v1.Conducir();
        v2.Conducir();
    }
}
```
###### 2.4. Genéricos
> Las **clases genéricas** permiten definir clases y métodos que funcionan con diferentes tipos de datos sin duplicar código. Se declaran con un parámetro de tipo (`<T>`), que luego se sustituye por un tipo concreto al usarlas. Son muy útiles para crear estructuras de datos (como listas, pilas o colas) y para escribir código **reutilizable y seguro en tiempo de compilación**.
```cs
using System;

class Caja<T>
{
    private T contenido;

    public void Guardar(T valor)
    {
        contenido = valor;
    }

    public T Obtener()
    {
        return contenido;
    }
}

class Program
{
    static void Main()
    {
        Caja<int> cajaEnteros = new Caja<int>();
        cajaEnteros.Guardar(123);
        Console.WriteLine("Caja de enteros: " + cajaEnteros.Obtener());

        Caja<string> cajaTextos = new Caja<string>();
        cajaTextos.Guardar("Hola");
        Console.WriteLine("Caja de textos: " + cajaTextos.Obtener());
    }
}
```

3. Otros Conceptos: 
> Además de las estructuras básicas y la programación orientada a objetos, C# incluye características esenciales para escribir programas más robustos y seguros. Entre ellas están las **conversiones de tipos (casting)**, necesarias para trabajar con diferentes tipos de datos; el **manejo de excepciones**, que permite controlar errores sin que el programa se detenga inesperadamente; y los **tipos anulables (nullable types)**, que amplían la flexibilidad de los tipos de valor permitiendo que también puedan representar la ausencia de dato. Estos conceptos son claves para desarrollar aplicaciones reales de manera estable y confiable.
###### 3.1. Casting: Conversión de tipos
> El **casting** es el proceso de convertir un valor de un tipo de dato a otro. En C# puede ser:
> - **Implícito**, cuando la conversión es segura (ejemplo: de `int` a `double`).
> - **Explícito**, cuando existe riesgo de pérdida de información y se requiere indicar el tipo con paréntesis (ejemplo: de `double` a `int`).  
    También existen métodos de conversión como `int.Parse()` o `Convert.ToInt32()` para transformar datos entre tipos incompatibles, como texto a número.
```cs
using System;

class Program
{
    static void Main()
    {
        // Conversión implícita (de menor a mayor precisión)
        int numero = 100;
        double numeroGrande = numero;
        Console.WriteLine("Conversión implícita: " + numeroGrande);

        // Conversión explícita (necesita casting)
        double decimalGrande = 9.8;
        int entero = (int)decimalGrande; // pierde decimales
        Console.WriteLine("Conversión explícita: " + entero);

        // Conversión con métodos
        string texto = "123";
        int convertido = int.Parse(texto);
        Console.WriteLine("De texto a entero: " + convertido);
    }
}
```
###### 3.2. Excepciones: Try-Catch-Finally
> Las **excepciones** permiten manejar errores de forma controlada. En C# se usa un bloque `try` para ejecutar código que puede fallar, `catch` para capturar el error y reaccionar ante él, y `finally` para ejecutar instrucciones que deben realizarse siempre, ocurra o no un error. Esto hace que el programa no se detenga bruscamente y que podamos dar mensajes claros al usuario o tomar medidas de recuperación.
```cs
using System;

class Program
{
    static void Main()
    {
        try
        {
            Console.Write("Introduce un número: ");
            int numero = int.Parse(Console.ReadLine());
            Console.WriteLine("Número ingresado: " + numero);
        }
        catch (FormatException)
        {
            Console.WriteLine("Error: No ingresaste un número válido.");
        }
        catch (Exception ex)
        {
            Console.WriteLine("Error inesperado: " + ex.Message);
        }
        finally
        {
            Console.WriteLine("Bloque finally ejecutado siempre.");
        }
    }
}
```
###### 3.3. Nullables
> Los **tipos de valor** (como `int`, `double` o `bool`) normalmente no aceptan `null`. Para permitirlo, se usa el modificador `?`, convirtiéndolos en **nullable types** (ejemplo: `int?`). Estos permiten representar la ausencia de valor en tipos que normalmente siempre tienen uno. Además, C# ofrece el operador `??` (_null-coalescing_), que permite asignar un valor alternativo cuando la variable es `null`.
```cs
using System;

class Program
{
    static void Main()
    {
        int? edad = null; // Nullable int

        if (edad.HasValue)
        {
            Console.WriteLine("Edad: " + edad.Value);
        }
        else
        {
            Console.WriteLine("Edad no especificada.");
        }

        // Operador null-coalescing (??)
        int edadDefinitiva = edad ?? 18; // Si es null, toma 18
        Console.WriteLine("Edad final: " + edadDefinitiva);
    }
}
```

El tutorial sigue en [[Tutorial Extra]]