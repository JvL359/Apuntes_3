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
```python
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
```python
# Crear un Paquete de Python (ejecutar src, p.ej. sim_ws/src)
ros2 pkg create --build-type ament_python <nombre_del_paquete>
ros2 pkg create --build-type ament_python --node-name <nombre_del_nodo> <nombre_del_paquete>  # crea también plantilla de nodo
```
#### 2. Nodos
> Un **nodo (node)** es un **proceso** que realiza una **tarea concreta**.  
> Un sistema de control puede estar formado por **muchos nodos**, por ejemplo: adquirir datos de un sensor de distancia, capturar imágenes, controlar motores, localizar respecto al mapa, planificar rutas o mostrar el estado del sistema.  
> **Ventajas:**
> 	- Mayor **tolerancia a fallos** (un error afecta solo a parte del sistema).
> 	- Se **reduce la complejidad** frente a aplicaciones monolíticas.
```python
# Compilar Nodos (ejecutar desde la raíz del workspace, p. ej. sim_ws)
colcon build
colcon build --packages-select <nombre_del_paquete_1> <nombre_del_paquete_2>
colcon build --symlink-install  # útil en Python: cambios se actualizan al guardar

# Ejecutar Nodos (en cada terminal/pestaña, desde el workspace)
. install/setup.bash
source install/setup.bash

ros2 run <nombre_del_paquete> <nombre_del_nodo>  # p. ej., ros2 run amr_simulation coppeliasim_node

# Mostrar Información de Nodos
ros2 node list
ros2 node info <nombre_del_nodo>  # p. ej., ros2 node info /coppeliasim_node
```
#### 3. Topics
> Los nodos intercambian datos principalmente mediante **mensajes (messages)**.  
> Los mensajes se organizan en **temas (topics)** con **nombres únicos**:
> 	- Un nodo puede **publicar** mensajes en uno o varios topics.
> 	- Un nodo puede **suscribirse** a uno o varios topics.
> 	- Puede haber **varios publicadores y varios suscriptores** en el mismo topic.
```python
# Listar Temas
ros2 topic list
ros2 topic list -t      # muestra también el tipo de mensaje
ros2 topic list -v      # detalles: tipo + nº publicadores/suscriptores

# Info de un Tema
ros2 topic info <nombre_del_tema>     # p. ej., ros2 topic info /cmd_vel
ros2 topic info <nombre_del_tema> -v  # incluye info de QoS

# Ver datos y Estadísticos
ros2 topic echo <nombre_del_tema>     # p. ej., ros2 topic echo /cmd_vel
ros2 topic hz <nombre_del_tema>       # tasa de publicación

# Publicar (ver formato con -h)
ros2 topic pub <nombre_del_tema> <tipo_de_mensaje> <valores>
```
#### 4. Mensajes
> ROS proporciona muchos **mensajes predefinidos**, organizados en paquetes (ejemplos):
> - `builtin_interfaces/msg/` (Duration, Time)
> - `geometry_msgs/msg/` (Pose, PoseStamped, Quaternion, Twist, Vector3…)
> - `nav_msgs/msg/` (OccupancyGrid, Odometry, Path…)
> - `sensor_msgs/msg/` (BatteryState, Image, Imu, LaserScan, Range…)
> - `std_msgs/msg/` (Header, Bool, Byte, Float64, Int32, UInt32, String…)  
>     Además, se pueden crear **mensajes personalizados**.
```python
# Listar Mensajes
ros2 interface list -m

# Ver Interfaces de un Paquete
ros2 interface package <nombre_del_paquete>  # p. ej., ros2 interface package sensor_msgs

# Ver la Estructura de un Mensaje
ros2 interface show <tipo_de_mensaje>        # p. ej., ros2 interface show geometry_msgs/msg/Twist
```
#### 5. Topics & Mensajes
> Relación clave: un **topic** es el “canal” con nombre; el **mensaje** es el “formato” de lo que viaja por ese canal.  
> Por eso, al inspeccionar o publicar en un topic suele interesar ver **qué tipo de mensaje** usa y cuántos nodos están conectados (publicando/suscritos).
```python
# Ver Tipo y Conexiones de un Topic
ros2 topic list -t
ros2 topic info <nombre_del_tema>
ros2 topic info <nombre_del_tema> -v  # incluye QoS

# Ver Estructura del Tipo de mMnsaje Asociado
ros2 interface show <tipo_de_mensaje>

# Mostrar Datos del Topic
ros2 topic echo <nombre_del_tema>
```
#### 6. Ejemplo 1 - Publicación
###### 6.1. Publicación en Python
> La clase `MinimalPublisher` define un **nodo** que crea un **publicador** de mensajes `String` en el topic `"hello"`.  
> El parámetro `qos_profile=10` indica el **perfil de Calidad de Servicio (QoS)** usado por el publicador; en este ejemplo se usa como “profundidad” (tamaño de cola) y debe ser **compatible** con el del suscriptor para que la comunicación funcione como se espera.  
> Con `create_timer(timer_period_sec=0.5, ...)` se programa una publicación periódica cada **500 ms**.  
> Para depurar en terminal se usa `self.get_logger().info(...)`, que muestra trazas en tiempo real (más útil que `print` en este contexto).  
> Por último, en `main()` se inicializa ROS (`rclpy.init`), se crea el nodo y se mantiene ejecutándose con `rclpy.spin(...)` (equivalente a un `while True`) hasta recibir `Ctrl+C`, momento en el que se libera el nodo (`destroy_node`) y se cierra ROS (`rclpy.shutdown()`) (mejor no darle muchas veces seguidas para que la terminal no se enfade).
```python
import rclpy  
from rclpy.node import Node  
# Message types  
from std_msgs.msg import String # Example message (deprecated)
  
class MinimalPublisher(Node): # Nodes inherit from the base class Node  
	def __init__(self) -> None:  
		super().__init__("minimal_publisher") # Set the node name  
		# Publishers  
		self._publisher = self.create_publisher(  
			msg_type=String, topic="hello", qos_profile=10  
		)  
		# Create a timer to publish every 500 ms  
		self._timer = self.create_timer(  
			timer_period_sec=0.5, callback=self._timer_callback  
		)  
		
	def _timer_callback(self) -> None:  
		msg = String()  
		msg.data = "Hello, World!"  
		self._publisher.publish(msg)  
		
		# Log to the terminal with information (info) level  
		self.get_logger().info(f"Publishing: {msg.data}")

def main(args=None) -> None:  
	rclpy.init(args=args)  
	minimal_publisher = MinimalPublisher()  
	rclpy.spin(minimal_publisher)  
	# Destroy the node explicitly.  
	# Optional. Otherwise, it will be done automatically  
	# when the garbage collector destroys the node object.  
	minimal_publisher.destroy_node()  
	rclpy.shutdown() # Or rclpy.try_shutdown()  
	
if __name__ == "__main__":  
main()
```
###### 6.2. Suscripción en Python
> La clase `MinimalSubscriber` define un **nodo** que crea un **suscriptor** al topic `"hello"` con el mismo tipo de mensaje (`String`).
> - `create_subscription(...)` registra: **tipo de mensaje**, **topic**, **callback** y **QoS** (debe ser compatible con el publicador).
> - La función `_listener_callback(self, msg)` se ejecuta **cada vez que llega un mensaje**, y aquí se usa el logger para mostrar lo recibido: `I heard: ...`.
> - En `main()` se repite el patrón estándar: `rclpy.init` → crear nodo → `rclpy.spin` (espera “infinita”) → `destroy_node` y `rclpy.shutdown` al terminar con `Ctrl+C`.
```python
import rclpy  
from rclpy.node import Node  
# Message types  
from std_msgs.msg import String # Example message (deprecated)  

class MinimalSubscriber(Node): # Nodes inherit from the base class Node  
	def __init__(self) -> None:  
		super().__init__("minimal_subscriber") # Set the node name  
		# Subscribers (beware self._subscriptions is reserved)  
		self._subscriber = self.create_subscription(  
			msg_type=String,  
			topic="hello",  
			callback=self._listener_callback,  
			qos_profile=10,  
		)  
	def _listener_callback(self, msg: String) -> None:  
		# Log to the terminal with information (info) level  
		self.get_logger().info(f"I heard: {msg.data}")
		
def main(args=None) -> None:  
	rclpy.init(args=args)  
	minimal_subscriber = MinimalSubscriber()  
	rclpy.spin(minimal_subscriber)  
	# Destroy the node explicitly.  
	# Optional. Otherwise, it will be done automatically  
	# when the garbage collector destroys the node object.  
	minimal_subscriber.destroy_node()  
	rclpy.shutdown() # Or rclpy.try_shutdown()  
	
if __name__ == "__main__":  
main()		
```
###### 6.3. Configuración del Ejecutable en el Paquete `setup.py` 
> Este `setup.py` define cómo se **empaqueta e instala** un paquete de Python en ROS 2 y, sobre todo, cómo se registran sus **ejecutables**.  
> Lo importante para poder lanzar nodos con `ros2 run` es `entry_points["console_scripts"]:` ahí se mapea cada **nombre de ejecutable** (p. ej., `publisher_node`) a la función `main` del módulo correspondiente (`tutorial_pubsub_py.publisher_node:main`).  
> Además, `package_name`, `packages=find_packages(...)` y `data_files` aseguran que se instalan tanto el código como los ficheros necesarios para que ROS 2 reconozca el paquete (p. ej., `package.xml` y el recurso del índice).
```python
from setuptools import find_packages, setup  
package_name = "tutorial_pubsub_py" # Rellenar  
setup(  
	name=package_name,  
	version="1.0.0", # Rellenar  
	packages=find_packages(exclude=["test"]),  
	data_files=[  
		("share/ament_index/resource_index/packages", ["resource/" + package_name]),  
		("share/" + package_name, ["package.xml"]),  
	],  
	install_requires=["setuptools"],  
	zip_safe=True,  
	maintainer="Jaime Boal", # Rellenar  
	maintainer_email="jboal@comillas.edu", # Rellenar  
	description="Pub/sub tutorial for Autonomous Mobile Robots @ Comillas ICAI.", # Rellenar  
	license="Apache License 2.0", # Rellenar  
	tests_require=["pytest"],  
	entry_points={  
		"console_scripts": [ # Rellenar con la función inicial de todos los nodos del paquete  
			"publisher_node = tutorial_pubsub_py.publisher_node:main", # nombre_del_ejecutable = nombre_del_paquete.nombre_del_archivo_python:main  
			"subscriber_node = tutorial_pubsub_py.subscriber_node:main",  
		],  
	},  
)
```
#### 7. Servicios
> Los **servicios (services)** implementan comunicación **cliente/servidor** en ROS 2.
> - Se define un mensaje de **solicitud** y otro de **respuesta**, separados por `---` en un archivo `*.srv`.
> - El nodo que ofrece el servicio lo **anuncia** con un **nombre** concreto (nombre del servicio).
> - El nodo cliente envía la **solicitud** y espera la **respuesta de forma asíncrona**.
> Además, ROS incluye **servicios predefinidos** organizados en paquetes, por ejemplo:
> 	- `map_msgs/srv/` (p. ej., GetMapROI, GetPointMap, SaveMap…)
> 	- `nav_msgs/srv/` (GetMap, GetPlan, SetMap)
> 	- `sensor_msgs/srv/` (SetCameraInfo)
> 	- `std_srvs/srv/` (Empty, SetBool, Trigger…)
> 	- `tf2_msgs/srv/` (FrameGraph)  
> Se pueden listar todos los servicios con `ros2 interface list –s`.
> También es habitual crear **servicios personalizados**.
```python
# 1. Obtener el Mapa
nav_msgs/msg/GetMap
---
nav_msgs/OccupancyGrid map

# 2. Obtener el Plan de Ruta
nav_msgs/msg/GetPlan
geometry_msgs/PoseStamped start
geometry_msgs/PoseStamped goal
float tolerance
---
nav_msgs/Path plan

# 3. Establecer el Mapa Inicial
nav_msgs/msg/SetMap
nav_msgs/OccupancyGrid map
geometry_msgs/PoseWithCovarianceStamped initial_pose
---
bool success

# 4. Establecer la Info de Cámara
sensor_msgs/srv/SetCameraInfo
sensor_msgs/CameraInfo camera_info
---
bool success
string status_message

# 5. Servicio Vacío
std_srvs/srv/Empty
---

# 6. Activar o Desactivar (bool)
std_srvs/srv/SetBool
bool data  # Ej.: Activar hardware
---
bool success
string message

# 7. Disparar Acción y Devolver Estado
std_srvs/srv/Trigger
---
bool success
string message
```
#### 8. Ejemplo 2 - Servicio
###### 8.1. Servidor en Python
> Este nodo (`MinimalService`) implementa un **servidor de servicio** usando el tipo `AddTwoInts`. Al inicializarse, crea el servicio con `create_service`, indicando: el **tipo de servicio** (`srv_type`), el **nombre** con el que se anuncia (`srv_name="add_two_ints"`) y la **función callback** que se ejecutará cuando llegue una solicitud.  
> En `_add_two_ints_callback`, el servidor recibe un `request` (con campos `a` y `b`) y rellena el `response` (campo `sum`) con la suma. Además, se registra en terminal la solicitud recibida con `get_logger().info(...)`. Como en el resto de nodos, `rclpy.spin(...)` mantiene el servidor activo hasta `Ctrl+C`, y al terminar se liberan recursos con `destroy_node()` y `rclpy.shutdown()`.
```python
import rclpy  
from rclpy.node import Node  
from example_interfaces.srv import AddTwoInts  
class MinimalService(Node):  
	def __init__(self) -> None:  
		super().__init__("minimal_service")  
		# Services  
		self._service = self.create_service(  
			srv_type=AddTwoInts,  
			srv_name="add_two_ints",  
			callback=self._add_two_ints_callback  
		)  
	def _add_two_ints_callback(  
		self, request: AddTwoInts.Request, response: AddTwoInts.Response  
	):  
		response.sum = request.a + request.b  
		# Log to the terminal with information (info) level  
		self.get_logger().info(  
			f"Incoming request - a: {request.a} b: {request.b}"  
		)  
		return response

def main(args=None) -> None:  
	rclpy.init(args=args)  
	minimal_service = MinimalService()  
	rclpy.spin(minimal_service)  
	# Destroy the node explicitly.  
	# Optional. Otherwise, it will be done automatically  
	# when the garbage collector destroys the node object.  
	minimal_service.destroy_node()  
	rclpy.shutdown() # Or rclpy.try_shutdown()  
	
if __name__ == "__main__":  
main()
```
###### 8.2. Cliente en Python
> Este nodo (`MinimalClientAsync`) implementa un **cliente asíncrono** del servicio `add_two_ints` (mismo nombre que anuncia el servidor) usando `create_client`. Antes de enviar peticiones, espera a que el servicio esté disponible con `wait_for_service(timeout_sec=1.0)`, mostrando un mensaje si aún no existe.  
> La solicitud se construye con `AddTwoInts.Request()` y se envía con `call_async(self._request)`, que devuelve un `future` (resultado pendiente). En lugar de bloquearse esperando, el cliente registra un **callback de finalización** con `future.add_done_callback(...)`: cuando llega la respuesta, `_add_two_ints_callback` extrae el resultado (`future.result()`) y lo muestra por el logger. El patrón de ejecución vuelve a ser el estándar: `spin` para mantener el nodo vivo y `shutdown` para cerrar correctamente.
```python
import rclpy  
from rclpy.node import Node  
from example_interfaces.srv import AddTwoInts  

class MinimalClientAsync(Node):  
	def __init__(self) -> None:  
		super().__init__("minimal_client_async")  
		self._client_async = self.create_client(  
			srv_type=AddTwoInts,  
			srv_name="add_two_ints"  
		)  
		while not self._client_async.wait_for_service(timeout_sec=1.0):  
			self.get_logger().info("Service not available. Waiting...")  
		self._request = AddTwoInts.Request()  
		self._send_request() # Can be called anywhere else  
	def _send_request(self) -> None:  
		self._request.a = 41  
		self._request.b = 1  
		future = self._client_async.call_async(self._request)  
		future.add_done_callback(self._add_two_ints_callback)
	def _add_two_ints_callback(self, future) -> None:  
		response: AddTwoInts.Response = future.result()  
		self.get_logger().info(  
			"Result of add_two_ints: "  
			f"{self._request.a} + "  
			f"{self._request.b} = "  
			f"{response.sum}"  
		)  
		
def main(args=None) -> None:  
	rclpy.init(args=args)  
	minimal_client = MinimalClientAsync()  
	rclpy.spin(minimal_client)  
	# Destroy the node explicitly.  
	# Optional. Otherwise, it will be done automatically  
	# when the garbage collector destroys the node object.  
	minimal_client.destroy_node()  
	rclpy.shutdown() # Or rclpy.try_shutdown() 
	 
if __name__ == "__main__":  
main()
```
#### 9. Acciones
> Las **acciones (actions)** son un mecanismo similar a los **servicios**, pero pensado para **tareas que se extienden en el tiempo**.  
> Se diferencian porque **pueden cancelarse** y porque ofrecen **realimentación continua (feedback)** mientras la tarea está en ejecución, normalmente a través de un **tema (topic)**.  
> La interfaz de una acción se define en un fichero `*.action` y se estructura en **tres bloques** separados por `---`:
> 	- **Objetivo (goal):** lo que se pide hacer.
> 	- **Resultado (result):** lo que devuelve al terminar.
> 	- **Realimentación (feedback):** estado parcial mientras se ejecuta.  
> **Flujo típico:** el cliente envía el **objetivo**, el servidor **acepta** (o no) la tarea, durante la ejecución publica **feedback**, y al finalizar devuelve el **resultado**.  
> (no son muy importantes, solo saber que existen)
```python
# 0. Listar las Acciones (ros 2 cli)
ros2 interface list -a

# 1. Ejemplo de Acción: Rotación Absoluta (turtlesim)
turtlesim/action/RotateAbsolute
# Objetivo: Orientación Deseada en Radianes
float32 theta
---
# Resultado: Desplazamiento en Radianes Respecto a la Posición Inicial
float32 delta
---
# Realimentación: Rotación Pendiente en Radianes
float32 remaining

# 2. Ejemplo de Acción: Fibonacci (action_tutorials_interfaces)
action_tutorials_interfaces/action/Fibonacci
# Objetivo: Número de Elementos de la Sucesión Solicitado
int32 order
---
# Resultado: Secuencia con Todos los Elementos Solicitados
int32[] sequence
---
# Realimentación: Estado Actual de la Secuencia
int32[] partial_sequence
```
#### 10. Ejemplo 3 - Actions
###### 10.1. Servidor en Python
> Este nodo actúa como **servidor de acción** para la acción `Fibonacci` (nombre: `"fibonacci"`). Al recibir un **objetivo** (`order`), ejecuta la tarea en `_execute_callback`: inicializa el **feedback** con la secuencia parcial `[0, 1]`, va calculando nuevos términos de Fibonacci y, en cada iteración, publica la **realimentación** (`publish_feedback`) para que el cliente vea el progreso (aquí se simula tiempo de cómputo con `sleep(1)`).  
> Al terminar, marca el objetivo como completado (`goal_handle.succeed()`), construye el **resultado** final (`result.sequence`) con la secuencia completa y lo devuelve.
```python
import time  
import rclpy  
from rclpy.action import ActionServer  
from rclpy.node import Node  
from action_tutorials_interfaces.action import Fibonacci  

class FibonacciActionServer(Node):  
	def __init__(self):  
		super().__init__("fibonacci_action_server")  
		# Action servers  
		self._action_server = ActionServer(  
			self,  
			action_type=Fibonacci,  
			action_name="fibonacci",  
			execute_callback=self._execute_callback  
		)  
	def _execute_callback(self, goal_handle):  
		# Feedback  
		feedback_msg = Fibonacci.Feedback()  
		feedback_msg.partial_sequence = [0, 1]
		for i in range(1, goal_handle.request.order):  
			feedback_msg.partial_sequence.append(  
				feedback_msg.partial_sequence[i]  
				+ feedback_msg.partial_sequence[i - 1]  
			)  
			goal_handle.publish_feedback(feedback_msg)  
			time.sleep(1)  
		# Result  
		goal_handle.succeed()  
		result = Fibonacci.Result()  
		result.sequence = feedback_msg.partial_sequence  
		return result 
		 
def main(args=None):  
	rclpy.init(args=args)  
	fibonacci_action_server = FibonacciActionServer()  
	rclpy.spin(fibonacci_action_server)  
	fibonacci_action_server.destroy_node() # Optional  
	rclpy.shutdown() # Or rclpy.try_shutdown()  

if __name__ == "__main__":  
main()
```
###### 10.2. Cliente en Python
> Este nodo actúa como **cliente de acción**. Crea un `ActionClient` para la acción `Fibonacci` (nombre: `"fibonacci"`) y, en `send_goal`, construye el **mensaje de objetivo** (`Fibonacci.Goal`) fijando `order`. Luego espera a que el servidor esté disponible (`wait_for_server`) y envía el objetivo de forma **asíncrona** con `send_goal_async`, que devuelve un _future_ (la operación no bloquea por sí sola).  
> En `main`, se envía un objetivo (por ejemplo `10`) y se usa `rclpy.spin_until_future_complete(...)` para **esperar** a que el envío/gestión del objetivo complete; para gestionar **feedback** y el **resultado** normalmente se añaden _callbacks_ al _future_ (en este ejemplo se deja minimalista).
```python
import rclpy  
from rclpy.action import ActionClient  
from rclpy.node import Node  
from action_tutorials_interfaces.action import Fibonacci 
 
class FibonacciActionClient(Node):  
	def __init__(self):  
		super().__init__("fibonacci_action_client")  
		self._action_client = ActionClient(  
			self,  
			action_type=Fibonacci,  
			action_name="fibonacci"  
		)  
	def send_goal(self, order):  
		goal_msg = Fibonacci.Goal()  
		goal_msg.order = order  
		self._action_client.wait_for_server()  
	return self._action_client.send_goal_async(goal_msg)
	
def main(args=None):  
	rclpy.init(args=args)  
	action_client = FibonacciActionClient()  
	future = action_client.send_goal(10)  
	rclpy.spin_until_future_complete(action_client, future) 
	 
if __name__ == "__main__":  
main()
```
#### 11. Nodos con Ciclo de Vida
> También se llaman nodos gestionados (managed): permiten ahorrar recursos y orquestar el orden de arranque y ejecución.
> **4 Estados:**
> 	- **Sin configurar (unconfigured):** estado inicial; el nodo está creado, pero todavía no ha reservado/inicializado recursos (sensores, publicadores, parámetros, etc.).
> 	- **Inactivo (inactive):** nodo configurado pero “parado”; los callbacks y publicadores no están operativos (no publica ni procesa como en ejecución normal).
> 	- **Activo (active):** comportamiento de un nodo estándar; ya ejecuta callbacks, publica y responde con normalidad.
> 	- **Finalizado (finalized):** estado final; la única transición es destruir el nodo (no puede volver atrás).
> **Transiciones y Callbacks:** existen 7 transiciones y 6 callbacks asociados (configure/activate/deactivate/cleanup/shutdown/error). Las transiciones se pueden disparar desde el terminal o con un nodo dedicado (lifecycle manager), por ejemplo: `ros2 lifecycle set <nombre_del_nodo> <transición>` (p. ej. `ros2 lifecycle set /coppeliasim_node configure`).
```python
import rclpy  
from rclpy.lifecycle import (  
	LifecycleNode,  
	LifecycleState,  
	TransitionCallbackReturn,  
)  

class MinimalLifecycleNode(LifecycleNode): # Inherit from LifecycleNode  
	def __init__(self) -> None:  
		"""Called in response to the 'create()' transition.  
		The node is initialized in the 'unconfigured' state."""  
		super().__init__("minimal_lifecycle_node")  
	def on_configure(self, state: LifecycleState) -> TransitionCallbackReturn:  
		"""Called as response to the 'configure()' transition.  
		The node evolves from 'unconfigured' to 'inactive'."""  
		return super().on_configure(state) # TransitionCallbackReturn.SUCCESS  
										  # TransitionCallbackReturn.FAILURE  
										  # TransitionCallbackReturn.ERROR  
	def on_activate(self, state: LifecycleState) -> TransitionCallbackReturn:  
		"""Called as response to the 'activate()' transition.  
		The node evolves from 'inactive' to 'active'."""  
		return super().on_activate(state)  
	def on_deactivate(self, state: LifecycleState) -> TransitionCallbackReturn:  
		"""Called as response to the 'deactivate()' transition.  
		The node evolves from 'active' to 'inactive'."""  
		return super().on_deactivate(state)  
	def on_cleanup(self, state: LifecycleState) -> TransitionCallbackReturn:  
		"""Called as response to the 'cleanup()' transition.  
		The node evolves from 'inactive' to 'unconfigured'."""  
		return super().on_cleanup(state)  
	def on_shutdown(self, state: LifecycleState) -> TransitionCallbackReturn:  
		"""Called as response to the 'shutdown()' transition. The node evolves  
		from 'unconfigured', 'inactive', or 'active' to 'finalized'."""  
		return super().on_shutdown(state)  
	def on_error(self, state: LifecycleState) -> TransitionCallbackReturn:  
		"""Called as a response to an error raised in any state or transition.  
		The node evolves to 'unconfigured' if the error is fixed or to  
		'finalized' on failure."""  
		return super().on_error(state)  
		
def main(args=None):  
	rclpy.init(args=args)  
	minimal_lifecycle_node = MinimalLifecycleNode()  
	rclpy.spin(minimal_lifecycle_node)  
	minimal_lifecycle_node.destroy_node() # Optional  
	rclpy.shutdown() # Or rclpy.try_shutdown()  
	
if __name__ == "__main__":  
main()
```
#### 12. Archivos de Lanzamiento
> Un robot suele estar compuesto por muchos nodos, y abrir un terminal por cada uno es tedioso y propenso a errores. Un archivo de lanzamiento (_launch file_) permite definir **qué nodos** se van a ejecutar, con **qué argumentos** y **qué parámetros**, para arrancarlo todo con **un único comando**. Se ejecuta con `ros2 launch <paquete> <archivo.launch.py> <parámetros>` (los parámetros son opcionales). Normalmente, los parámetros que recibe cada nodo se declaran y se leen en `__init__()` o (si es un _lifecycle node_) en `on_configure()`.
> Para lanzar varios nodos en un solo comando se usa: 
> 	`ros2 launch <nombre_del_paquete> <nombre_del_archivo> <parámetros>` 
> como por ejemplo `ros2 launch amr_bringup wall_follower_sim.launch.py`
```python
# Ejemplo de Launch File (Python)
from launch import LaunchDescription
from launch_ros.actions import Node
import math

def generate_launch_description():  # Este Nombre Es Obligatorio
    # Parámetros
    start = (2.0, -3.0, 1.5 * math.pi)

    wall_follower_node = Node(
        package="amr_control",
        executable="wall_follower",
        arguments=["--ros-args", "--log-level", "WARN"],
    )

    coppeliasim_node = Node(
        package="amr_simulation",
        executable="coppeliasim",
        arguments=["--ros-args", "--log-level", "WARN"],
        parameters=[{"start": start}],
    )

    return LaunchDescription([
        wall_follower_node,
        coppeliasim_node,
    ])

# Leer un Parámetro Dentro del Nodo (en __init__ o en on_configure)
self.declare_parameter("start", (0.0, 0.0, 0.0))
start = tuple(
	self.get_parameter("start")
    .get_parameter_value()
    .double_array_value.tolist()
)
```
#### 13. Ejemplo 4 - Launcher File & Node Managing
###### 13.1. Launcher File
> En este _launch file_ se lanzan **dos nodos con ciclo de vida** (`LifecycleNode`), `wall_follower` y `coppeliasim`, y además un nodo normal (`Node`) que actúa como **gestor del ciclo de vida** (`lifecycle_manager`). La idea es que el _launch_ no solo arranque los procesos, sino que también deje preparado el **orden de arranque** mediante el parámetro `node_startup_order`, indicando qué nodos hay que configurar y activar primero. En este caso, `coppeliasim` se fuerza a ir el último para que el resto del sistema esté listo antes de iniciar la simulación.
```python
from launch import LaunchDescription  
from launch_ros.actions import LifecycleNode, Node  
import math  

def generate_launch_description(): # This name is mandatory  
	# Parameters  
	start = (2.0, -3.0, 1.5 * math.pi)  
	wall_follower_node = LifecycleNode(  
		package="amr_control",  
		executable="wall_follower",  
		name="wall_follower",  
		namespace="",  
		output="screen",  
		arguments=["--ros-args", "--log-level", "WARN"],  
	)  
	coppeliasim_node = LifecycleNode(  
		package="amr_simulation",  
		executable="coppeliasim",  
		name="coppeliasim",  
		namespace="",  
		output="screen",  
		arguments=["--ros-args", "--log-level", "WARN"],  
		parameters=[{"start": start}],  
	)
	lifecycle_manager_node = Node(  
		package="amr_bringup",  
		executable="lifecycle_manager",  
		output="screen",  
		arguments=["--ros-args", "--log-level", "WARN"],  
		parameters=[  
			{  
				"node_startup_order": (  
					"wall_follower",  
					"coppeliasim", # Must be started last  
				)  
			}  
		],  
	)  
	return LaunchDescription(  
		[  
			wall_follower_node,  
			coppeliasim_node,  
			lifecycle_manager_node, # Must be launched last  
		]  
	)
```
###### 13.2. Node Managing
> Este nodo (`LifecycleManagerNode`) lee el parámetro `node_startup_order` y, con esa lista de nombres, crea un **cliente de servicio** `ChangeState` para cada _lifecycle node_ (el servicio típico es `/<nombre>/change_state`). Primero espera a que todos esos servicios estén disponibles y después lanza las transiciones **en orden**: (1) `configure` para pasar de _unconfigured_ a _inactive_, y (2) `activate` para pasar de _inactive_ a _active_. La función `_change_state()` construye la petición con el `transition_id`, hace la llamada asíncrona y bloquea hasta recibir respuesta con `spin_until_future_complete`, asegurando que cada transición se completa antes de pasar a la siguiente.
```python
import rclpy  
from rclpy.client import Client  
from rclpy.node import Node  
from lifecycle_msgs.srv import ChangeState  
from lifecycle_msgs.msg import Transition  

class LifecycleManagerNode(Node):  
	def __init__(self):  
		"""Lifecycle manager initializer."""  
		super().__init__("lifecycle_manager")  
		# Parameters  
		self.declare_parameter("node_startup_order", [""])  
		lifecycle_names = (  
			self.get_parameter("node_startup_order")  
			.get_parameter_value()  
			.string_array_value  
		)  
		# Create clients to change the states of lifecycle nodes  
		self._clients = [  
			self.create_client(ChangeState, f"/{name}/change_state")  
			for name in lifecycle_names  
		]  
		# Wait for the services to be available  
		for client in self._clients:  
			client.wait_for_service()
		# Transition nodes to the 'inactive' state in order  
		for client in self._clients:  
			self._change_state(client, Transition.TRANSITION_CONFIGURE)  
		# Transition nodes to the 'active' state in order  
		for client in self._clients:  
		self._change_state(client, Transition.TRANSITION_ACTIVATE)  
	def _change_state(self, client: Client, transition_id: int) -> None:  
		request = ChangeState.Request()  
		request.transition.id = transition_id  
		future = client.call_async(request)  
		rclpy.spin_until_future_complete(self, future)  
		
def main(args=None):  
	rclpy.init(args=args)  
	lifecycle_manager_node = LifecycleManagerNode()  
	try:  
		rclpy.spin(lifecycle_manager_node)  
	except KeyboardInterrupt:  
		pass  
	lifecycle_manager_node.destroy_node()  
	rclpy.try_shutdown()  
	
if __name__ == "__main__":  
main()
```
#### 14. Calidad de Servicio `QoS`
> En ROS 2, gracias a que se apoya en DDS (Data Distribution Service), la **calidad de servicio (QoS)** permite ajustar _cómo_ se comunican los nodos (no solo “qué” se comunican). Esto va desde comunicaciones muy fiables (tipo TCP) hasta entregas de _mejor esfuerzo_ (best-effort, más parecido a UDP). En la práctica, un **perfil de QoS** se construye combinando varias **políticas** (history, reliability, durability, etc.), y ROS 2 incluso ofrece **perfiles predefinidos** (`QoSPresetProfiles`) para usos típicos como datos de sensores.
> 
> Los QoS se pueden fijar en **publicadores, suscriptores, servicios y clientes**, y cada instancia puede tener un perfil distinto. La idea clave es que la comunicación funciona como un “acuerdo”: el **emisor anuncia la calidad máxima** que puede ofrecer y el **receptor indica la calidad mínima** que está dispuesto a aceptar. Si hay alguna **política incompatible**, directamente **no se entregan mensajes** (parece que “no funciona”, pero en realidad es un _mismatch_ de QoS). Elegir requisitos de QoS depende sobre todo de las **necesidades de tiempo real** y de los **recursos computacionales disponibles**.
> 
> Un sistema en **tiempo real** no es “más rápido”, sino aquel donde la corrección depende también del **instante** en el que llega el resultado:
> 	- **tiempo real fuerte (hard):** llegar tarde es un fallo crítico (ej.: un sensor llega tarde y el vehículo colisiona).
>     - **tiempo real firme (firm):** se toleran retrasos esporádicos, pero si llega tarde el resultado ya no sirve (ej.: una pieza no se coloca a tiempo en una línea).
>     - **tiempo real blando (soft):** el resultado pierde utilidad si se retrasa, pero no es catastrófico (ej.: perder fotogramas en streaming).  
> Por eso, el QoS se ajusta para equilibrar **fiabilidad, latencia, carga** y **robustez** según el caso.
>    
> **Políticas principales de QoS:**
> - **history (historia):** define cuántas muestras se guardan.
>     - `KEEP_LAST`: guarda solo las últimas **N** muestras (se configura con `depth`).
>     - `KEEP_ALL`: guarda **todas** las muestras (el límite real lo impone el middleware por recursos).
> - **reliability (fiabilidad):** define si “se garantiza entrega” o no.
>     - `BEST_EFFORT`: no asegura que lleguen todas las muestras (típico en redes inestables o sensores con alta frecuencia donde prima latencia).
>     - `RELIABLE`: intenta garantizar entrega (puede reintentar varias veces).
>     - Compatibilidad típica (según la tabla): un **suscriptor best-effort** suele aceptar tanto emisores best-effort como reliable, pero un **suscriptor reliable** necesita que el emisor sea reliable (si el emisor es best-effort, no hay comunicación).
> - **durability (durabilidad):** si el sistema “recuerda” mensajes para suscriptores que llegan tarde
>     - `VOLATILE`: no persiste muestras; solo se entregan mensajes nuevos.
>     - `TRANSIENT_LOCAL`: mientras el publicador exista, conserva muestras para suscriptores que se conecten después (efecto tipo “latched”).
>     - Compatibilidad típica: si el receptor exige `TRANSIENT_LOCAL` pero el emisor es `VOLATILE`, no hay comunicación; si el emisor es `TRANSIENT_LOCAL` y el receptor `VOLATILE`, se entregan solo los mensajes nuevos; si ambos son `TRANSIENT_LOCAL`, se entregan nuevos y antiguos.    
> - **deadline (fecha límite):** tiempo máximo permitido entre mensajes consecutivos publicados en un mismo tema. Si se excede, se considera que se incumple el requisito temporal. Para que el “acuerdo” sea válido, o se usa la política por defecto del receptor, o se fijan explícitamente ambos tiempos, y típicamente el del receptor debe ser **mayor o igual** que el del emisor.
> - **lifespan (esperanza de vida):** tiempo máximo desde el envío hasta la recepción antes de considerar el mensaje **obsoleto**. Los mensajes caducados se eliminan silenciosamente.
> - **liveliness (vivacidad):** cómo se detecta que un publicador “sigue vivo”.
>     - `AUTOMATIC`: el sistema asume que el publicador está operativo y renueva el “lease” automáticamente al comunicar (con un `liveliness_lease_duration`).
>     - `MANUAL_BY_TOPIC`: cada publicador debe “hacer señales” explícitas (llamada a la API) para renovar su concesión.
>     - Compatibilidad típica: un receptor `AUTOMATIC` suele aceptar ambos, pero un receptor `MANUAL_BY_TOPIC` requiere emisores `MANUAL_BY_TOPIC`.
#### 15. Ejemplo 5 - QoS
> En el primer bloque se ve cómo asignar QoS de manera directa al crear la suscripción. Si se pasa un entero en `qos_profile=10`, se está usando el perfil por defecto con **historia `KEEP_LAST`** y **profundidad (depth) 10**, es decir, el suscriptor solo mantiene en memoria las últimas 10 muestras recibidas. Alternativamente, se puede usar un perfil predefinido de ROS 2 con `QoSPresetProfiles.SENSOR_DATA`, pensado para datos de sensores, para no tener que configurar a mano todas las políticas; es útil cuando queremos un comportamiento típico ya probado y consistente en el sistema.
```python
from rclpy.qos import QoSPresetProfiles  
# Subscriber with the default QoS profile: Keep last 10 messages  
self._subscriber = self.create_subscription(  
	msg_type=String,  
	topic="hello",  
	callback=self._listener_callback,  
	qos_profile=10, # depth  
)  
# Subscriber with a preset QoS profile  
self._subscriber = self.create_subscription(  
	msg_type=String,  
	topic="hello",  
	callback=self._listener_callback,  
	qos_profile=QoSPresetProfiles.SENSOR_DATA,  
)
```
> En el segundo bloque se construye un perfil de QoS **personalizado** con `QoSProfile`, seleccionando explícitamente varias políticas: `history=KEEP_LAST` y `depth=10` controlan cuántas muestras se almacenan; `reliability=BEST_EFFORT` prioriza la fluidez/latencia aceptando posibles pérdidas (típico en streams de sensores o redes inestables); y `durability=VOLATILE` indica que no se guardan mensajes para suscriptores que se conecten tarde (solo llegan los nuevos). Una vez definido, ese `qos_profile` se pasa a `create_subscription` para que el suscriptor imponga exactamente esas condiciones de comunicación.
```python
from rclpy.qos import (  
QoSDurabilityPolicy,  
QoSHistoryPolicy,  
QoSProfile,  
QoSReliabilityPolicy,  
)  

qos_profile = QoSProfile(  
	history=QoSHistoryPolicy.KEEP_LAST,  
	depth=10,  
	reliability=QoSReliabilityPolicy.BEST_EFFORT,  
	durability=QoSDurabilityPolicy.VOLATILE,  
)  
# Subscriber with a custom QoS profile  
self._subscriber = self.create_subscription(  
	msg_type=String,  
	topic="hello",  
	callback=self._listener_callback,  
	qos_profile=qos_profile,  
)
```