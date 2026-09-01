### III. Corrutinas, Delegados y Eventos
> En C# y Unity existen mecanismos que amplían la flexibilidad de los programas. Las **corrutinas** permiten ejecutar funciones que pueden **pausarse y reanudarse** en momentos concretos, muy útiles para programar comportamientos en el tiempo dentro de videojuegos (esperas, animaciones, secuencias).
> Por otro lado, los **delegados** son tipos que permiten **almacenar referencias a métodos** y ejecutarlos de forma dinámica. Gracias a ellos se pueden crear **acciones configurables**, eventos y sistemas modulares. Unity y C# los usan ampliamente para el manejo de **acciones, eventos y callbacks**.

1. Corrutinas
> Una **corrutina** es una función especial en Unity que devuelve `IEnumerator` y puede contener la instrucción `yield return`. Esto permite pausar su ejecución y reanudarla más adelante, después de un cierto tiempo o de un evento en el ciclo de juego. Son ideales para programar **acciones en secuencia**, como esperar unos segundos, mover un objeto poco a poco o mostrar mensajes con pausas.
```cs
using System.Collections;
using UnityEngine;

public class EjemploCorrutina : MonoBehaviour
{
    void Start()
    {
        // Inicia la corrutina
        StartCoroutine(MostrarMensajes());
    }

    IEnumerator MostrarMensajes()
    {
        Debug.Log("Mensaje 1");
        yield return new WaitForSeconds(2); // espera 2 segundos
        Debug.Log("Mensaje 2");
        yield return new WaitForSeconds(2);
        Debug.Log("Mensaje 3");
    }
}
```

2. Delegados 
###### 2.1. Básico
>  Un **delegado** es un tipo que apunta a un método. Actúa como un “puente” que permite asignar funciones a variables y ejecutarlas en tiempo de ejecución. Los delegados pueden almacenar uno o varios métodos (multicast), lo que facilita el diseño de programas **desacoplados y flexibles**, donde no hace falta conocer de antemano qué método se ejecutará.
```cs
using System;

class Program
{
    // Definición de un delegado
    public delegate void MiDelegado(string mensaje);

    static void Main()
    {
        // Asignación de un método al delegado
        MiDelegado d = MostrarMensaje;
        d("Hola desde un delegado");

        // Multicast: se pueden agregar más métodos
        d += MensajeEnMayusculas;
        d("Probando multicast");
    }

    static void MostrarMensaje(string msg)
    {
        Console.WriteLine("Normal: " + msg);
    }

    static void MensajeEnMayusculas(string msg)
    {
        Console.WriteLine("Mayúsculas: " + msg.ToUpper());
    }
}
```
###### 2.2. Genérico (Action)
> `Action` es un tipo de delegado genérico predefinido en C#. Representa un método que **no devuelve valor** (`void`) y que puede tener de 0 a 16 parámetros. Simplifica la creación de delegados porque no es necesario definirlos manualmente. Se usa mucho para **callbacks** o pasar funciones como parámetros de forma rápida y limpia.
```cs
using System;

class Program
{
    static void Main()
    {
        // Action sin parámetros
        Action saludar = () => Console.WriteLine("Hola!");
        saludar();

        // Action con parámetros
        Action<string> mostrar = (texto) => Console.WriteLine("Texto: " + texto);
        mostrar("Probando Action");
    }
}
```

3. Eventos
> Los **eventos** en C# se construyen sobre delegados. Se declaran con la palabra clave `event` y siguen el patrón de **publicación–suscripción**: un objeto “publica” el evento y otros pueden **suscribirse** para reaccionar cuando ocurre. El delegado más usado para eventos es `EventHandler`, que recibe el objeto que dispara el evento y unos argumentos opcionales (`EventArgs`). Este sistema es fundamental para construir programas **reactivos y modulares**, donde distintas partes del código se comunican sin estar fuertemente acopladas.
```cs
using System;

class Publicador
{
    public event EventHandler EventoOcurrio;

    public void DispararEvento()
    {
        Console.WriteLine("Evento lanzado");
        EventoOcurrio?.Invoke(this, EventArgs.Empty);
    }
}

class Suscriptor
{
    public void ManejarEvento(object sender, EventArgs e)
    {
        Console.WriteLine("Evento recibido por el suscriptor.");
    }
}

class Program
{
    static void Main()
    {
        var pub = new Publicador();
        var sub = new Suscriptor();

        // Suscribirse al evento
        pub.EventoOcurrio += sub.ManejarEvento;

        pub.DispararEvento();
    }
}
```