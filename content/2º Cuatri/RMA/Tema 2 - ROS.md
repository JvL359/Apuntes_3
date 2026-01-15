### I. Introducción
#### 1. Qué es?
> - Un conjunto de _librerías y herramientas_ para desarrollar aplicaciones robóticas
> - Está construido sobre estándares abiertos, siendo un software de _código abierto (open source)_ con una licencia permisiva (_ROS 2:_ Apache 2.0; _ROS 1:_ BSD modificada de 3 cláusulas)
> - Comparte _características_ con:
> 	- **Middlewares** -> Serialización _marshalling_ y bajo acoplamiento _loose coupling_
> 	- **Frameworks** -> Funciones _callbacks_ para mensajes y _utility classes_
> 	- **Sistemas operativos** -> Abstracción de hardware y gestión de paquetes
> - Se puede _integrar_ con sistemas operativos _en tiempo real_ (Real Time Operating Systems o RTOS)
> - Es una _comunidad global_ con un vasto ecosistema
> - Tiene un fuerte _apoyo de la industria_ -> Technical Steering Commitee
> - Este software se puede ver dividido en 4 aspectos:
> 	- **Fontanería** -> Gestión de procesos, Comunicación entre procesos, Drivers de hardware
> 	- **Herramientas** -> Simulación, Visualización, Registro de datos
> 	- **Librerías** -> Percepción, Control y manipulación, Navegación, etc ...
> 	- **Ecosistema** -> Paquetes y distribuciones, Documentación y tutoriales
#### 2. Un Poco de Historia
> - **2007:** Willow Garage (2006–2014) presenta **ROS**, inspirado en desarrollos previos del **Stanford Artificial Intelligence Laboratory (SAIL)**.
> - **2013:** El mantenimiento pasa a manos de **Open Robotics**.
>     - **2022:** La rama comercial (**OSRC**) es adquirida por **Intrinsic** (compañía de Alphabet).
>     - **ROS** y **Gazebo** se mantienen independientes en la **OSRF**.
> - **Diciembre de 2017:** Se lanza la **primera distribución de ROS 2**.
> - Actualmente, **ROS** es el estándar _de facto_ para el desarrollo de robots en **investigación e industria**.
#### 3. Distribuciones con Soporte
> - Una **distribución de ROS** es un conjunto de paquetes “congelados” en una **versión concreta**.
> - Se publica una distribución cada **23 de mayo** (Día Mundial de las Tortugas).
> - Las distribuciones de **años pares** tienen **soporte extendido** (≈ **5 años**, como Ubuntu LTS).
> - **ROS 2 Humble Hawksbill (LTS):**
>     - **Lanzamiento:** 23/05/2022
>     - **Fin de soporte:** mayo 2027
>     - **Plataformas:** Ubuntu 22.04 y Windows 10+
#### 4. ROS 2 vs ROS 1
> **ROS 2 (Humble Hawksbill)** vs **ROS 1 (Noetic Ninjemys)**, en lo esencial:
> - **Sistemas Operativos:** ROS 2 → Linux y Windows (nivel 1) + macOS (nivel 3) / ROS 1 → Linux.
> - **Lenguajes:** ROS 2 → C++17, Python 3.10 / ROS 1 → C++14, Python 3.8 (antes solo 2.x).
> - **Compilación:** ROS 2 → `colcon` / ROS 1 → `catkin`.
> - **Arquitectura:** ROS 2 → **distribuida** / ROS 1 → **maestro/esclavo**.
> - **Tiempo Real:** ROS 2 puede combinarse con **RTOS** / ROS 1 **no** soporta desarrollo de software de tiempo real.
> - **ROS Bridge:** permite **comunicar** código no portado de ROS 1 con ROS 2.
#### 5. Filosofía de ROS 2
> - **Comunicación entre Iguales:** procesos que intercambian información mediante una **API predefinida**.
> - **Distribuido:** programas ejecutándose en **varios ordenadores** y comunicándose por **red**.
> - **Multilenguaje:** puedes usar cualquier lenguaje con librería cliente.
>     - Soporte oficial: **C++ y Python**.
>     - Comunidad: Ada, C, Java (y Android), .NET (C#), Node.js, Rust, Flutter, Dart.
>     - Terceros: **MATLAB ROS Toolbox**.
> - **Ligero:** añade una capa pequeña para integrar librerías; fácil de integrar con otros frameworks y simuladores.
#### 6. Objetivos de ROS 2
> - Mejorar la **calidad** del diseño y de la implementación de la arquitectura.
> - Incrementar la **fiabilidad** de los sistemas desarrollados.
> - Permitir **control en tiempo real** y ejecución **determinista**.
> - Facilitar **validación**, **verificación** y **certificación**.
> - Aumentar la **flexibilidad** de la comunicación entre robots.
> - Soportar sistemas **empotrados (embedded)** → **micro-ROS**.
#### 7. Arquitectura de ROS 2

> ROS 2 se organiza en **capas**, separando el código del usuario de la comunicación subyacente:
> - **User Code** (tu aplicación) usa librerías cliente: **rclpy (Python)**, **rclcpp (C++)** o clientes de terceros (p. ej., Java/Ada).
> - Esas librerías pasan por **rcl (ROS Client Library)** y luego por **rmw (ROS Middleware)**.
> - **rmw** oculta qué implementación concreta de comunicación se usa (abstracción).
> - La comunicación se apoya en **DDS** (modelo publicación/suscripción, descentralizado), mediante distintas implementaciones (p. ej., **eProsima Fast DDS** por defecto, RTI Connext, OpenSplice).
> - Funciona sobre **Ubuntu, Windows y macOS**.  
>     **Nota práctica:** suele usarse **rclcpp** si se necesita eficiencia/tiempos de respuesta rápidos y **rclpy** para prototipar y reducir tiempos de desarrollo.
#### 8. ROS - Industrial
> Proyecto que pretende extender las capacidades de ROS a hardware y aplicaciones industriales.
#### 9. Herramientas de Visualización y Depuración
###### 9.1. RViz
> Herramienta para **visualizar** y **depurar** información del robot en 3D (estado, sensores, frames, etc.) con el comando **`rviz2`**.
###### 9.2. rqt
> Conjunto de herramientas gráficas para **inspección y depuración** (por ejemplo, ver la estructura de nodos y mensajes o revisar logs) con el comando **`rqt`**.
#### 10. Simuladores con Soporte ROS
> Ejemplos de simuladores que pueden integrarse con ROS: **Gazebo**, **CoppeliaSim**, **Webots**, **CARLA**, **Unity** y **NVIDIA Isaac Sim**.  
###### 10.1. Gazebo
> - Conjunto de **librerías open-source** para simulación (durante un tiempo se llamó **Ignition**).
> - Incluye módulos como **gz-gui**, **gz-math**, **gz-rendering**, etc.  
> - La aplicación más conocida construida con este framework es **Gazebo Sim**.
> - Sus distribuciones de **años impares** tienen **soporte extendido (5 años)**.
> - 
### II. Comandos de ROS 2

#### 1. Sistema de Archivos
![[Pasted image 20260115174533.png]]
###### 1.1. Espacio de Trabajo
> Un **espacio de trabajo (workspace)** es el “contenedor” donde organizas tus proyectos de ROS 2: básicamente un **repositorio de paquetes**.  
> La estructura mínima incluye una carpeta **`src/`**, donde se colocan los paquetes.
```py
# Crear un Espacio de Trabajo (Linux)
mkdir <espacio_de_trabajo>        # ej.: mkdir sim_ws
mkdir <espacio_de_trabajo>/src    # ej.: mkdir sim_ws/src
```
###### 1.2. Paquete
> Un **paquete (package)** es una **colección de archivos y carpetas** con un propósito común.  
> Puede incluir **código**, librerías, datos, documentación y tests. Elementos típicos:
> - `src/`: código fuente en C/C++.
> - `include/<nombre_del_paquete>/`: cabeceras C/C++.
> - `<nombre_del_paquete>/`: código Python (incluye `__init__.py`).
> - `package.xml`: metadatos (nombre, versión, mantenedor, descripción, licencia, dependencias…) según **REP-0140**.
> - `CMakeLists.txt`: compilación (paquetes C++).
> - `setup.py`: instalación (paquetes Python).
> - `setup.cfg`: ayuda a localizar paquetes Python y lanzar ejecutables sin especificar ruta.
> - `README`, `LICENSE`: descripción y licencia.
```py
# Crear un Paquete de Python (ejecutar src, p.ej. sim_ws/src)
ros2 pkg create --build-type ament_python <nombre_del_paquete>
ros2 pkg create --build-type ament_python --node-name <nombre_del_nodo> <nombre_del_paquete>  # crea también plantilla de nodo
```

