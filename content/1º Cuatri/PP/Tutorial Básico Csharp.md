### I. Introducción a C\#

1. Hello World
> El programa **“Hello World”** es el ejemplo clásico para empezar en cualquier lenguaje de programación. En C#, nos enseña la estructura básica de un programa:
> - `using System;` importa librerías necesarias para usar la consola.
> - `class Program` define la clase principal.
> - `static void Main()` es el **punto de entrada** del programa, donde comienza la ejecución.
> - `Console.WriteLine("Hola Mundo");` muestra un mensaje en la pantalla.
> Este ejemplo sencillo es la base para entender cómo se organizan los programas en C#.
```csharp
using System;

class Program
{
    static void Main()
    {
        Console.WriteLine("Hola Mundo");
    }
}
```

2. Variables y Tipos de Datos
> Las **variables** son espacios en memoria donde guardamos información para poder usarla en el programa. Cada variable tiene un **tipo de dato**, que indica qué clase de información puede almacenar. En C# existen tipos numéricos como `int` (enteros), `float` y `double` (decimales), `string` para texto y `bool` para valores lógicos (`true` o `false`).
> Al declarar una variable, debemos indicar su tipo, lo que hace que C# sea un lenguaje de **tipado estático**. Además, se pueden mostrar en consola concatenando cadenas con `+` o usando **interpolación de cadenas** (`$"..."`), que hace el código más legible.
```cs
using System;

class Program
{
    static void Main()
    {
        // Variables básicas
        int edad = 25;           // Número entero
        float altura = 1.75f;    // Número decimal (se marca con 'f')
        double peso = 68.5;      // Decimal con más precisión
        string nombre = "Ana";   // Texto
        bool esMayor = true;     // Verdadero/Falso

        // Mostrar datos en consola
        Console.WriteLine("Nombre: " + nombre);
        Console.WriteLine("Edad: " + edad);
        Console.WriteLine("Altura: " + altura + "m");
        Console.WriteLine("Peso: " + peso + "kg");
        Console.WriteLine("¿Es mayor de edad?: " + esMayor);

        // Interpolación de cadenas (más limpio)
        Console.WriteLine($"{nombre} tiene {edad} años, mide {altura}m y pesa                   {peso}kg.");
    }
}
```

3. Operadores Básicos
> Los **operadores** son símbolos que permiten realizar operaciones sobre variables y valores. En C# existen operadores aritméticos (`+`, `-`, `*`, `/`, `%`) para cálculos matemáticos, y operadores relacionales (`>`, `<`, `==`, `!=`) que comparan valores y devuelven un resultado booleano (`true` o `false`). Gracias a ellos podemos manipular datos, hacer cálculos y tomar decisiones en función de condiciones lógicas.
```cs
using System;

class Program
{
	static void Main()
	{
		int a = 10;
		int b = 3;
		
		Console.WriteLine(a + b); // 13
		Console.WriteLine(a - b); // 7
		Console.WriteLine(a * b); // 30
		Console.WriteLine(a / b); // 3 (división entera)
		Console.WriteLine(a % b); // 1 (resto de la división)
		bool resultado = (a > b); // true
	}
}
```

4. Condicionales
> Las **condicionales** permiten que el programa tome **decisiones** según se cumpla o no una condición. En C# se utiliza `if` para ejecutar un bloque de código cuando la condición es verdadera, y `else` para manejar el caso contrario. También se puede usar `else if` para evaluar varias condiciones de forma encadenada. Este mecanismo hace que el programa se adapte a diferentes situaciones y no siga siempre el mismo flujo de ejecución.
```cs
using System;

class Program
{
	static void Main()
	{
		int edad = 20;
	
		if (edad >= 18)
		{
		    Console.WriteLine("Eres mayor de edad");
		}
		else
		{
		    Console.WriteLine("Eres menor de edad");
		}
	}
}
```

5. Bucles
> Los **bucles** permiten repetir un bloque de instrucciones varias veces de forma automática, evitando escribir el mismo código de manera repetida. En C# los más comunes son:
> - **for**, cuando sabemos cuántas veces queremos iterar.
> - **while**, que repite mientras una condición sea verdadera. 
> - **foreach**, pensado para recorrer colecciones (como arrays o listas) de manera sencilla.  
> Gracias a los bucles, podemos automatizar tareas repetitivas y recorrer estructuras de datos de forma más eficiente.
```cs
using System;

class Program
{
	static void Main()
	{
		// For: sabemos cuántas veces repetimos
		for (int i = 0; i < 5; i++)
		{
		    Console.WriteLine("Repetición " + i);
		}
		
		// While: se repite mientras la condición sea verdadera
		int contador = 0;
		while (contador < 3)
		{
		    Console.WriteLine("Contando: " + contador);
		    contador++;
		}
		
		// Foreach: recorre colecciones
		string[] frutas = { "Manzana", "Banana", "Naranja" };
		foreach (string fruta in frutas)
		{
		    Console.WriteLine(fruta);
		}
	}
}
```

6. Funciones
> Las **funciones** (también llamadas métodos estáticos si se definen con `static`) son bloques de código que realizan una tarea específica. Sirven para **organizar y reutilizar lógica**, evitando repetir instrucciones en varias partes del programa. Una función puede recibir **parámetros** como entrada y devolver un **valor de salida**, o simplemente ejecutar acciones. En C#, se definen dentro de una clase y pueden ser llamadas desde el método principal `Main` u otros métodos del programa.
```cs
using System;

class Program
{
	static void Main()
    {
        Saludar("Ana");
        int suma = Sumar(5, 7);
        Console.WriteLine("La suma es: " + suma);
    }

    static void Saludar(string nombre)
    {
        Console.WriteLine($"Hola, {nombre}!");
    }

    static int Sumar(int x, int y)
    {
        return x + y;
    }
}
```

7. Clases y Objetos I
###### 7.1. Visibilidad
> Definen **quién puede acceder** a un miembro (variable, método, clase).
> - `public`: accesible desde cualquier parte.
> - `private`: solo accesible dentro de la misma clase.
> - `protected`: accesible en la clase y en sus herederas.
> - `internal`: accesible solo dentro del mismo ensamblado/proyecto.
```cs
using System;

class Persona
{
    public string Nombre;    // visible en todos lados
    private int edad;        // solo dentro de la clase
    protected string Apodo;  // accesible en clases hijas
}
```
###### 7.2. Constructores
> Un **constructor** es un método especial de una clase que se ejecuta automáticamente al crear un objeto con `new`. Su función principal es **inicializar los atributos del objeto**, dándoles valores iniciales.
> A diferencia de otros métodos, no tiene tipo de retorno y siempre se llama igual que la clase. Si no se define ninguno, C# crea un **constructor por defecto** sin parámetros. También es posible tener varios constructores con diferentes parámetros (**sobrecarga**) para dar flexibilidad al crear objetos.
```cs
using System;

class Persona
{
    public string Nombre { get; set; }
    public int Edad { get; set; }

    public Persona(string nombre, int edad) // constructor
    {
        Nombre = nombre;
        Edad = edad;
    }
}

class Program
{
    static void Main()
    {
        Persona p = new Persona("Ana", 25);
        Console.WriteLine($"{p.Nombre}, {p.Edad} años");
    }
}
```
###### 7.3. Palabra Clave: this
> `this` es una palabra clave que se refiere al **objeto actual** dentro de su propia clase. Se usa principalmente para diferenciar entre variables de instancia y parámetros con el mismo nombre, o para pasar la referencia del objeto actual a otros métodos. En resumen, permite que un objeto “hable de sí mismo” dentro de su código.
```cs
using System;

class Persona
{
    private string nombre;

    public Persona(string nombre)
    {
        this.nombre = nombre; // "this" se refiere al campo de la clase
    }
}
```
###### 7.4. Métodos: instancia y estático
> Los **métodos** son funciones definidas dentro de una clase que representan acciones o comportamientos que los objetos pueden realizar. Pueden recibir parámetros, devolver valores o simplemente ejecutar instrucciones. Son la forma de organizar la lógica dentro de una clase y de interactuar con sus datos. Existen **métodos de instancia**, que requieren crear un objeto para poder usarlos, y **métodos estáticos**, que pertenecen directamente a la clase y pueden llamarse sin necesidad de instanciarla.
```cs
using System;

class Calculadora
{
    public int Sumar(int a, int b) => a + b; // de instancia

    public static int Restar(int a, int b) => a - b; // estático
}

class Program
{
    static void Main()
    {
        Calculadora calc = new Calculadora();
        Console.WriteLine(calc.Sumar(5, 3));

        Console.WriteLine(Calculadora.Restar(10, 4)); // sin crear objeto
    }
}
```
###### 7.5. Propiedades: Getters y Setters
> Los **getters y setters** permiten controlar cómo se accede y modifica un campo privado de una clase. En C# se implementan mediante **propiedades**, que actúan como una interfaz segura para leer (`get`) y asignar (`set`) valores. Esto ayuda a proteger los datos internos de la clase (**encapsulación**) y aplicar validaciones si es necesario.
```cs
using System;

class Persona
{
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
```
###### 7.6. Herencia
> La **herencia** permite que una clase (llamada “hija” o derivada) reutilice y extienda el código de otra clase (llamada “padre” o base). Gracias a esto, se evitan repeticiones, se favorece la reutilización de código y se organizan las clases en jerarquías más claras.
```cs
using System;

class Animal
{
    public void Dormir() => Console.WriteLine("Zzz...");
}

class Perro : Animal
{
    public void Ladrar() => Console.WriteLine("Guau!");
}
```
###### 7.7. Herencia: Sobreescritura (override)
> Cuando una clase hija hereda un método de la clase padre, puede **redefinirlo** usando la palabra clave `override`. A esto se le llama **sobreescritura**. Permite cambiar el comportamiento heredado para adaptarlo a la lógica de la clase hija, manteniendo la misma firma del método.
```cs
using System;

class Animal
{
    public virtual void HacerSonido() => Console.WriteLine("Sonido genérico");
}

class Perro : Animal
{
    public override void HacerSonido() => Console.WriteLine("Guau!");
}
```
###### 7.8. Clases Abstractas
> Una **clase abstracta** es una clase que no puede instanciarse directamente. Sirve como **plantilla** para que otras clases hereden de ella. Puede incluir métodos normales y también **métodos abstractos**, que obligan a las clases hijas a proporcionar su propia implementación.
```cs
using System;

abstract class Animal
{
    public abstract void HacerSonido(); // sin implementación
}

class Gato : Animal
{
    public override void HacerSonido() => Console.WriteLine("Miau");
}
```
###### 7.9. Polimorfismo
> El **polimorfismo** permite que un mismo método pueda comportarse de distintas maneras según el tipo de objeto que lo use. En C#, se consigue mediante herencia y sobreescritura. Esto hace posible tratar a distintos objetos de manera uniforme, aumentando la flexibilidad del código.
```cs
using System;

class Animal
{
    public virtual void HacerSonido()
    {
        Console.WriteLine("Sonido genérico");
    }
}

class Gato : Animal
{
    public override void HacerSonido()
    {
        Console.WriteLine("Miau");
    }
}

class Perro : Animal
{
    public override void HacerSonido()
    {
        Console.WriteLine("Guau");
    }
}

class Program
{
    static void Main()
    {
        Animal a1 = new Gato();
        Animal a2 = new Perro();

        a1.HacerSonido(); // Miau
        a2.HacerSonido(); // Guau
    }
}
```
###### 7.10. Interfaces
> Una **interfaz** define un contrato que especifica qué métodos o propiedades debe tener una clase, pero sin dar implementación. Las clases que implementan esa interfaz están obligadas a cumplir el contrato. Esto permite crear sistemas más flexibles y modulares, ya que diferentes clases pueden compartir la misma interfaz aunque tengan implementaciones distintas.
```cs
using System;

interface IVehiculo
{
    void Conducir();
}

class Coche : IVehiculo
{
    public void Conducir() => Console.WriteLine("Conduciendo...");
}
```
###### 7.11. Delegados
> Un **delegado** es un tipo que actúa como referencia a un método. Permite asignar funciones a variables y ejecutarlas de forma dinámica, incluso en cadena (multicast). Se usan mucho en eventos y en programación orientada a la flexibilidad, ya que permiten decidir qué método ejecutar en tiempo de ejecución.
```cs
using System;

Action saludar = () => Console.WriteLine("Hola!");
saludar();
```
###### 7.12. Null
> En C#, los **tipos de referencia** (como `string` o clases) pueden no apuntar a ningún objeto en memoria, y en ese caso su valor es `null`. Esto significa que la variable existe, pero no tiene un objeto asignado. Es importante comprobarlo antes de usar la variable para evitar errores como el famoso _NullReferenceException_.
```cs
using System;

string texto = null;

if (texto == null)
    Console.WriteLine("Está vacío");
```
###### 7.13. None (Null vs Null-able)
> Los **tipos de valor** (como `int`, `double` o `bool`) normalmente no aceptan `null`. Para permitirlo, se usa el modificador `?`, lo que los convierte en **nullable types**. Esto resulta útil cuando un dato puede ser opcional o desconocido. Ejemplo: `int? edad = null;`. De esta forma podemos representar “sin valor” en un tipo que normalmente no lo permite.
```cs
using System;

int? edad = null;  // Nullable int
if (edad.HasValue)
    Console.WriteLine(edad.Value);
else
    Console.WriteLine("No tiene valor");
```


El tutorial continua en [[Tutorial Avanzado Csharp]]
