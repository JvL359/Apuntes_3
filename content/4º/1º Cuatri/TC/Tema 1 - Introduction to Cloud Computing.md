---
estado: pendiente de revisión
---

### I. Cloud Computing Fundamentals

#### 1. Definition and Main Characteristics

> **Cloud computing** es un modelo que permite acceder por red, de forma ubicua, cómoda y bajo demanda, a un **pool compartido de recursos informáticos configurables**. Esos recursos pueden incluir redes, servidores, almacenamiento, aplicaciones y servicios. Se pueden aprovisionar y liberar rápidamente, con un esfuerzo de gestión reducido y poca interacción manual con el proveedor.

> La idea central es que el usuario solicita capacidades a través de una red y la plataforma las obtiene de un conjunto de recursos compartidos. La infraestructura física continúa existiendo, pero se presenta mediante servicios que permiten crear, configurar y utilizar recursos sin gestionar directamente cada equipo físico.

| Characteristic | Meaning |
| --- | --- |
| **Ubiquitous network access** | Los recursos son accesibles a través de la red desde los dispositivos y ubicaciones admitidos |
| **On-demand access** | Se solicita capacidad cuando hace falta |
| **Self-service** | El cliente puede aprovisionar recursos sin que el proveedor tenga que atender manualmente cada solicitud |
| **Resource pooling** | La plataforma comparte un conjunto de recursos y los asigna a distintos consumidores |
| **Rapid elasticity** | La capacidad puede aumentar y reducirse rápidamente para ajustarse a la demanda |
| **Measured service** | Se mide el uso de los recursos para supervisarlo, controlarlo y contabilizarlo |

> **Escalabilidad** y **elasticidad** están relacionadas. La escalabilidad es la capacidad de soportar una carga mayor aumentando recursos; la elasticidad adapta la capacidad a las variaciones de la demanda, incluyendo liberarla cuando deja de ser necesaria. Por ejemplo, un servicio puede añadir recursos durante un pico y retirarlos después.

#### 2. Historical Development

> La evolución del cloud une la idea de consumir computación como un servicio con avances que permiten compartir infraestructura, acceder a ella por red y gestionarla mediante software.

| Period | Milestone |
| --- | --- |
| Década de 1960 | John McCarthy plantea la computación como un servicio comparable a una utilidad |
| 1999 | Salesforce representa el desarrollo de aplicaciones empresariales entregadas como servicio |
| 2006 | AWS lanza S3 y EC2, ofreciendo almacenamiento y capacidad de cómputo a través de Internet |
| 2008 | Google presenta la preview de App Engine para ejecutar aplicaciones web en su infraestructura |
| 2010 | Windows Azure alcanza disponibilidad general |

> [!warning] Corrección
> En el material aparece 2009 como fecha conjunta de Google Cloud y Microsoft Azure, pero los hitos correctos deben distinguirse: la **preview de Google App Engine se lanzó el 7 de abril de 2008** y la **disponibilidad general de Windows Azure comenzó el 1 de febrero de 2010**.
> Fuente de comprobación: [Anuncio oficial de Google App Engine](https://developers.googleblog.com/en/google-app-engine-at-campfire-one/) y [Anuncio oficial de Windows Azure](https://blogs.microsoft.com/blog/2010/02/01/windows-azure-general-availability/)

> El desarrollo de AWS ilustra cómo una necesidad interna puede convertirse en una plataforma. Alrededor de 2000, el crecimiento del comercio electrónico de Amazon planteaba problemas de escalabilidad y la empresa también quería facilitar que terceros utilizaran su plataforma. Gestionar ese crecimiento exigió construir una infraestructura eficiente y exponer capacidades mediante **APIs**, convirtiéndolas en componentes reutilizables.

> Hacia 2003, la experiencia en operar data centers fiables, escalables y eficientes llevó a considerar que otros clientes podían aprovechar esas capacidades. S3 y EC2 materializaron esa idea en 2006: Internet se convirtió en el medio para consumir funciones de almacenamiento y cómputo que antes se asociaban a infraestructura propia.

> El crecimiento posterior se refleja en catálogos de cientos de servicios, presencia en numerosas regiones e ingresos elevados. El número de servicios, las regiones y las cifras comerciales cambian con el tiempo; sirven para ilustrar la escala de un proveedor, pero no definen qué es cloud computing.

### II. Service and Deployment Models

#### 3. Main Cloud Service Models

> Un **modelo de servicio** determina qué parte de la pila tecnológica entrega y gestiona el proveedor y qué parte conserva el cliente. Al pasar de IaaS a PaaS y SaaS, el proveedor asume progresivamente más componentes de esa pila.

##### 3.1. Infrastructure as a Service —IaaS—

> En **IaaS**, el proveedor entrega recursos de infraestructura: cómputo —por ejemplo, máquinas virtuales—, almacenamiento y red. Mantiene el hardware y las instalaciones del data center.

> El cliente configura y mantiene los sistemas operativos, el software de plataforma que utilice y sus aplicaciones. Por ejemplo, disponer de una VM evita comprar y mantener el servidor físico, pero sigue requiriendo administrar el sistema operativo instalado en ella.

##### 3.2. Platform as a Service —PaaS—

> En **PaaS**, el proveedor entrega y mantiene tanto la infraestructura como el entorno necesario para desarrollar y desplegar aplicaciones. El cliente puede desarrollar, ejecutar y gestionar su aplicación sin construir esa plataforma por su cuenta.

> El cliente escribe el código y administra sus aplicaciones y datos. El proveedor mantiene el sistema operativo y los componentes de plataforma, como el entorno de ejecución o el servidor de aplicaciones. Se reduce así la carga operativa de preparar y mantener el entorno.

##### 3.3. Software as a Service —SaaS—

> En **SaaS**, el proveedor entrega una aplicación completa y mantiene toda su pila: infraestructura, plataforma y software de aplicación. También realiza las actualizaciones, las correcciones y el mantenimiento del producto.

> El cliente utiliza la aplicación y configura aspectos como sus usuarios y permisos. Muchas aplicaciones SaaS se acceden directamente mediante un navegador, aunque el acceso por navegador no es por sí solo la definición del modelo.

##### 3.4. Division of Responsibilities

| Responsibility | IaaS | PaaS | SaaS |
| --- | --- | --- | --- |
| Instalaciones, energía, refrigeración y protección física | Proveedor | Proveedor | Proveedor |
| Hardware: servidores, discos, routers y cableado | Proveedor | Proveedor | Proveedor |
| Despliegue, actualización y parcheado del sistema operativo | Cliente | Proveedor | Proveedor |
| Servidor de aplicaciones y entorno de plataforma | Cliente | Proveedor | Proveedor |
| Despliegue, actualización y parcheado de la aplicación | Cliente | Cliente | Proveedor |
| Gestión de cuentas de usuario y permisos del cliente | Cliente | Cliente | Cliente |

> Delegar más capas al proveedor reduce tareas técnicas, pero el cliente sigue tomando decisiones sobre cómo utiliza el servicio y quién accede a él. La gestión de usuarios y permisos permanece como responsabilidad del cliente en los tres modelos.

> La analogía de la pizza ayuda a recordar ese reparto. Prepararla en casa equivale a gestionar todos los componentes; comprarla preparada para hornearla delega una parte; recibirla cocinada delega también la preparación; comer en un restaurante delega además el entorno de consumo.

| Model | Pizza analogy | What the customer still provides |
| --- | --- | --- |
| On-premises | Preparar la pizza en casa | Ingredientes, horno, energía, mesa y bebida |
| IaaS | Comprar una pizza preparada y hornearla | Horno, energía, mesa y bebida |
| PaaS | Recibir la pizza cocinada | Mesa y bebida |
| SaaS | Comer en un restaurante | Utilizar el servicio ofrecido |

#### 4. Additional Service Models

##### 4.1. Containers as a Service —CaaS—

> En **CaaS**, el proveedor ofrece y gestiona los recursos de hardware y software necesarios para desarrollar, desplegar y operar aplicaciones mediante contenedores. El cliente puede ejecutar y gestionar sus aplicaciones sin construir y mantener desde cero la infraestructura o plataforma de contenedores.

> El cliente conserva la responsabilidad sobre el código, los datos y las aplicaciones. El contenedor es la unidad de empaquetado y ejecución; más adelante se distingue de una máquina virtual.

##### 4.2. Function as a Service —FaaS—

> En **FaaS**, el proveedor entrega una plataforma para ejecutar aplicaciones como **funciones activadas por eventos**. El desarrollador define la función y el evento que provoca su ejecución, mientras la plataforma administra la infraestructura y su escalado.

> Este planteamiento se asocia a **serverless**: el cliente no tiene que gestionar servidores para ejecutar cada función. Los servidores siguen existiendo dentro de la infraestructura del proveedor. FaaS es una forma de ofrecer ejecución serverless.

#### 5. Cloud Deployment Models

> Un **modelo de despliegue** describe quién utiliza la infraestructura y cómo se organiza o combina. Es una dimensión distinta del modelo de servicio: IaaS, PaaS y SaaS indican qué se entrega; public, private o hybrid indican el contexto de despliegue.

![[apuntes-266e735681cb-p0017-0926c7cda41f.png]]

| Deployment model | Organization of resources |
| --- | --- |
| **Public cloud** | Un proveedor ofrece servicios a varios clientes sobre infraestructura compartida, manteniendo el aislamiento entre ellos |
| **Semi-private cloud** | El proveedor atiende a varios clientes, pero reserva recursos separados para cada uno, como representa el esquema |
| **Private cloud** | La infraestructura se dedica a una organización; en el esquema, esa organización actúa también como su proveedor |
| **Hybrid cloud** | Se combinan una nube privada y una pública, conectando ambos entornos |
| **Community cloud** | Varias organizaciones comparten una infraestructura destinada a su comunidad |
| **Multi-cloud** | Una organización utiliza servicios de más de un proveedor cloud |

> La diferencia visual entre public y semi-private está en compartir un recurso frente a disponer de recursos separados por cliente dentro del proveedor. La denominación semi-private se utiliza aquí para esa configuración; el grado concreto de dedicación y aislamiento depende de la solución.

> **Private cloud** describe el uso dedicado a una organización, no obliga a que la infraestructura esté siempre ubicada en sus instalaciones. El esquema representa el caso en que la propia organización proporciona esa nube.

> **Hybrid** y **multi-cloud** describen combinaciones diferentes. Hybrid conecta entornos privados y públicos; multi-cloud implica utilizar varios proveedores. Una arquitectura puede reunir ambas características.

### III. Benefits and Challenges

#### 6. Why Cloud Computing?

##### 6.1. Main Benefits

> La **agilidad** consiste en poder disponer de recursos con rapidez, reduciendo el tiempo necesario para preparar infraestructura. La **elasticidad** facilita ajustar esa capacidad al uso y la **escalabilidad** permite soportar el crecimiento.

> El cloud también puede aumentar la **fiabilidad** mediante infraestructura y mecanismos de operación especializados, reducir las necesidades de mantener infraestructura IT interna y facilitar el acceso a múltiples servicios. Estos beneficios requieren una arquitectura y una operación adecuadas: contratar un servicio cloud no convierte automáticamente una aplicación en tolerante a fallos.

##### 6.2. Cost and Performance as Trade-Offs

> **Coste** y **rendimiento** pueden ser tanto beneficios como desafíos. Su resultado depende del uso y del diseño de la solución.

> El **CAPEX** es inversión en activos, como comprar servidores e instalaciones. El **OPEX** es gasto operativo recurrente, como pagar por servicios consumidos. Utilizar servicios cloud puede reducir la inversión inicial propia y trasladar parte del gasto hacia la operación. A cambio, es necesario medir y controlar el consumo para evitar recursos sobredimensionados o innecesarios.

> El rendimiento puede mejorar al disponer de recursos adecuados y capacidad de escalado, pero también depende de la conectividad, la latencia y la configuración de los servicios. Por ello, coste y rendimiento se deben evaluar conjuntamente para la carga concreta.

##### 6.3. Other Challenges

| Challenge | Main concern |
| --- | --- |
| **Security** | Proteger accesos, configuración, comunicaciones y recursos compartidos |
| **Privacy** | Controlar el acceso y tratamiento de datos |
| **Regulatory** | Considerar las obligaciones aplicables al uso y la ubicación de los datos |
| **Interoperability** | Integrar aplicaciones y servicios entre plataformas y entornos |
| **Organizational** | Adaptar funciones, conocimientos y procesos de trabajo |

> Estos desafíos influyen en la elección del proveedor, del modelo de servicio y del modelo de despliegue. La adopción del cloud afecta a la tecnología y también a cómo la organización desarrolla, administra y supervisa sus sistemas.

### IV. Technology Enablers

#### 7. Data Centers and High-Speed Networking

> Tres habilitadores fundamentales son los **data centers**, las **redes de alta velocidad** y la **virtualización**. Los primeros alojan la infraestructura; las redes permiten acceder a ella y conectar sus componentes; la virtualización permite ofrecer vistas lógicas y asignar recursos con flexibilidad.

##### 7.1. What Is a Data Center?

> Un **data center** es una instalación física que aloja sistemas informáticos y sus componentes asociados para almacenar, procesar, gestionar y distribuir datos. Incluye cuatro elementos: **ubicación física, hardware, infraestructura de soporte y personal**.

> La infraestructura de soporte es necesaria para que el hardware pueda funcionar de forma continua y segura. El personal mantiene y opera el conjunto; un data center comprende mucho más que una sala con servidores.

##### 7.2. Data Center Types

| Type | Purpose |
| --- | --- |
| **Enterprise data center** | Alojar infraestructura de una organización |
| **Colocation data center** | Ofrecer instalaciones y servicios de soporte donde los clientes alojan sus equipos |
| **Managed data center** | Incorporar gestión de infraestructura por un operador especializado |
| **Cloud data center** | Alojar la infraestructura con la que se entregan servicios cloud |
| **Edge data center** | Situar recursos próximos a usuarios o fuentes de datos |

> Estas categorías destacan aspectos diferentes —propiedad, alojamiento, operación o proximidad—, por lo que pueden existir soluciones que compartan características de varias.

##### 7.3. Physical Requirements

> Los aspectos que hay que cubrir incluyen:
>
> - **Seguridad física:** proteger instalaciones y acceso a los equipos.
> - **Energía:** suministrar alimentación adecuada.
> - **Control climático:** mantener condiciones apropiadas de temperatura y refrigeración.
> - **Conexión de red:** conectar sistemas, usuarios y otros emplazamientos.
> - **Extinción de incendios:** proteger personas e infraestructura.
> - **Organización de servidores:** distribuir los equipos y sus conexiones de forma operable.

#### 8. Server Virtualization

##### 8.1. Virtual Resources and Benefits

> **Virtualización** es la creación de una versión virtual de un recurso tecnológico, como un servidor, un dispositivo de almacenamiento o un recurso de red. Se separa la vista que utiliza el consumidor de los recursos físicos que la implementan.

> En servidores, un equipo físico puede proporcionar varias **virtual machines —VMs—**. Esto permite aprovechar mejor el hardware y crear recursos de manera ágil y dinámica. También facilita administrar cambios de hardware, incidencias y traslado de VMs, y simplifica y homogeneiza la infraestructura del data center.

##### 8.2. Hypervisor, Host and Guests

> El **hypervisor** es el software que crea y ejecuta las VMs. Trata CPU, memoria y almacenamiento como un pool y asigna a cada VM los recursos configurados. También planifica cómo las demandas de los recursos virtuales se ejecutan sobre los físicos.

> El equipo físico es el **host** y los sistemas operativos de las VMs son **guest operating systems**. Cada guest ejecuta sus aplicaciones bajo el control del hipervisor.

> Cuando el guest realiza determinadas operaciones privilegiadas sobre recursos compartidos, el hipervisor puede interceptarlas y realizarlas en su nombre. La aplicación y el sistema operativo invitado trabajan con la vista virtual sin tener que conocer cada decisión de gestión del hardware.

> Este mecanismo proporciona **aislamiento** entre VMs y **encapsulación** de sus entornos. El aislamiento permite mantener separados sistemas que comparten un mismo equipo físico, aunque su eficacia también depende de la implementación y la configuración.

##### 8.3. Hypervisor Types

| Aspect | Type 1 | Type 2 |
| --- | --- | --- |
| Position | Directamente sobre el hardware | Sobre un sistema operativo anfitrión existente |
| Stack | Hardware → hypervisor → VMs y guest OS | Hardware → host OS → hypervisor → VMs y guest OS |
| Hardware access | Control directo | Acceso mediado por el sistema operativo anfitrión |
| General implications | Puede alcanzar mayores niveles de disponibilidad, seguridad y rendimiento | La capa adicional suele introducir más sobrecarga |

> La distinción describe la posición del hipervisor en la arquitectura. Las comparaciones de rendimiento y seguridad son tendencias generales; el resultado concreto también depende de la implementación y del entorno.

> [!warning] Corrección
> En el material aparece «guest OS» bajo el hipervisor de tipo 2, pero la etiqueta correcta es **«host OS»**: el hipervisor se instala sobre el sistema operativo anfitrión, mientras los sistemas operativos invitados pertenecen a las VMs que ejecuta.
> Fuente de comprobación: [Tipos de hipervisor en AWS](https://aws.amazon.com/what-is/hypervisor/)

#### 9. Network Virtualization and SDN

##### 9.1. Forms of Network Virtualization

> La **virtualización de red** presenta recursos y funciones de red mediante abstracciones lógicas. Puede tomar varias formas:

| Form | Example |
| --- | --- |
| Dividir una red física en varias redes lógicas independientes | Separar redes de distintos clientes sobre la misma infraestructura |
| Proporcionar funciones de red a una partición del sistema operativo | Dar conectividad virtual a las VMs de un host |
| Implementar en software funciones tradicionalmente asociadas a dispositivos | Routers, firewalls y balanceadores virtuales |
| Combinar varias redes físicas en una única red lógica | Crear una red privada que conecte recursos distribuidos de un cliente |

> Las dos direcciones de abstracción —dividir y combinar— son útiles: una infraestructura compartida puede proporcionar entornos separados, y varios emplazamientos físicos pueden presentarse como una red coherente.

##### 9.2. Networking Functions and Benefits

> Para conectar VMs se proporcionan **vNICs** —interfaces de red virtuales—, **vSwitches** —switches virtuales—, overlays, routing, aislamiento y movilidad. Los **overlays** permiten construir una topología lógica sobre la red física subyacente.

> En un entorno **multi-tenant**, cada cliente o tenant obtiene una red virtual aislada. **NFV —Network Functions Virtualization—** lleva funciones como firewalls, load balancers, VPNs y routers a implementaciones software.

> Las redes virtuales se pueden aprovisionar rápidamente y automatizar. Su gestión facilita escalar a grandes cantidades de redes lógicas sobre una infraestructura física común y aplicar **microsegmentación**, firewalls por VM y políticas consistentes. Un control lógicamente centralizado simplifica la operación del conjunto.

##### 9.3. Software-Defined Networking

> **SDN —Software-Defined Networking—** separa el **control plane** del **data plane**. El plano de control decide cómo debe tratarse y dirigirse el tráfico; el plano de datos aplica esas decisiones y reenvía los paquetes.

![[apuntes-266e735681cb-p0031-5b59c41108af.png]]

> El esquema sitúa el control en la parte superior y los dispositivos de reenvío en la inferior. Las conexiones entre ambos planos permiten programar el comportamiento de la red. El control puede ser lógicamente centralizado sin requerir un único equipo físico.

> [!warning] Corrección
> En el material aparece «decoupling the data plane and the data plane», pero la expresión correcta es **separar el control plane del data plane**, es decir, las funciones de control de las funciones de reenvío.
> Fuente de comprobación: [Definición de SDN de Open Networking Foundation](https://opennetworking.org/sdn-definition/)

> La combinación de SDN y virtualización de red permite automatizar y orquestar redes en arquitecturas cloud. Virtualizar proporciona las abstracciones; disponer de control programable permite configurarlas y modificarlas mediante software.

#### 10. Storage Virtualization

> La **virtualización de almacenamiento** presenta una vista lógica de recursos físicos de almacenamiento. Puede agrupar medios y dispositivos en un pool, evitando que cada sistema consumidor tenga que gestionar directamente cada soporte físico.

> Una implementación de red puede utilizar **SAN —Storage Area Network—**, con protocolos como Fibre Channel o iSCSI, para ofrecer acceso basado en bloques. **NAS —Network Attached Storage—** ofrece acceso basado en archivos.

| Storage paradigm | Unit exposed | How it is used |
| --- | --- | --- |
| **Block-based** | Bloques de almacenamiento | Se presenta capacidad similar a un disco; el consumidor organiza su contenido |
| **File-based** | Archivos y directorios | Se accede a una estructura de archivos compartida |
| **Object-based** | Objetos identificables, con datos y metadatos | Se almacenan y recuperan objetos mediante sus identificadores |

> Estos tres paradigmas son habituales en soluciones cloud. La virtualización de almacenamiento agrupa y abstrae recursos; el paradigma describe cómo se presentan y acceden los datos.

> **Software-Defined Storage —SDS—** es un concepto relacionado: separa el software que realiza las operaciones de almacenamiento del hardware físico. Puede utilizar servidores x86 y agregar sus recursos para construir almacenamiento escalable mediante un cluster, facilitando aprovechar hardware de coste contenido y añadir nodos al sistema.

### V. Containers and Container Orchestration

#### 11. Container Fundamentals

##### 11.1. Image, Container and Runtime

> Un **contenedor** es una instancia de ejecución aislada de una aplicación, definida por su sistema de archivos, configuración y metadatos. Una **container image** es el paquete inmutable a partir del que se crea esa instancia.

> La imagen incluye código, runtime de la aplicación, herramientas, bibliotecas y configuración necesarios para ejecutarla. Al ejecutar una imagen se crea un contenedor. La imagen es el artefacto empaquetado y el contenedor es su instancia en ejecución.

> Los contenedores son una forma de **virtualización a nivel de sistema operativo**. Comparten el kernel del host y necesitan un **container runtime** para operar en él. El runtime obtiene imágenes del **container registry**, ejecuta los contenedores y administra su ciclo de vida. Entre las herramientas y runtimes del ecosistema están Docker, Podman, CRI-O y containerd.

> Empaquetar la aplicación junto con sus dependencias facilita reproducir su entorno y evita tener que preparar manualmente cada dependencia en cada destino. Esa encapsulación requiere que el sistema anfitrión proporcione un entorno compatible.

##### 11.2. VMs versus Containers

![[apuntes-266e735681cb-p0034-41979e1c8608.png]]

> A la izquierda, cada VM contiene una aplicación, sus binarios y bibliotecas y un **guest OS**. A la derecha, cada contenedor empaqueta la aplicación y sus dependencias, mientras comparte el sistema operativo anfitrión. La arquitectura de VMs dibujada incorpora un host OS bajo el hipervisor, por lo que representa la disposición de tipo 2.

| Aspect | Virtual machine | Container |
| --- | --- | --- |
| Virtualization level | Recursos de hardware virtuales | Sistema operativo |
| Operating system | Cada VM tiene un sistema operativo invitado | Los contenedores comparten el kernel del host |
| Application package | Aplicación y dependencias dentro del entorno de la VM | Aplicación, dependencias y configuración en una imagen |
| Execution component | Hypervisor | Container runtime o engine |
| Relative weight | Incluye el entorno del guest OS | Suele ser más ligero al no incorporar un kernel propio ni hardware virtual |

> Ambos mecanismos ofrecen aislamiento y encapsulación mediante arquitecturas diferentes. Un contenedor puede ejecutarse dentro de una VM: las dos tecnologías se pueden combinar.

#### 12. Build, Ship and Run with Docker

> El flujo separa construir el artefacto, distribuirlo y ejecutarlo:

![[apuntes-266e735681cb-p0035-c97f1c0515c6.png]]

> 1. **Build:** un `Dockerfile` describe cómo construir la imagen. La construcción produce el paquete de la aplicación.
> 2. **Push:** se publica la imagen en un registry, como Docker Hub.
> 3. **Pull:** el sistema de destino descarga la imagen del registry.
> 4. **Run:** el runtime utiliza la imagen para crear y ejecutar un contenedor.

> El elemento que se distribuye es la **imagen**. Ejecutarla crea una instancia; varias instancias pueden partir del mismo artefacto. Esto permite trasladar una aplicación empaquetada desde su construcción hasta su despliegue.

#### 13. Container Orchestration

> Una plataforma de **orquestación de contenedores** administra su ciclo de vida, especialmente en entornos grandes y dinámicos. Ejecutar un contenedor es solo una parte del problema: también hay que mantener réplicas, conectarlas, comprobar su salud, asignar recursos y realizar cambios.

> **Kubernetes** es una plataforma de orquestación open source diseñada para entornos de producción. Permite controlar y automatizar las siguientes funciones:

| Function | Purpose |
| --- | --- |
| Deployment | Desplegar contenedores |
| Scaling out/in | Añadir y retirar instancias para ajustar capacidad |
| Communication | Conectar contenedores entre sí y con el exterior |
| Load balancing and service discovery | Distribuir tráfico y localizar los servicios |
| Health monitoring | Supervisar el estado de los componentes |
| Upgrades | Facilitar actualizaciones y mantener la continuidad cuando la configuración lo permite |
| Resource allocation | Asignar recursos a los contenedores |
| Storage management | Gestionar sus necesidades de almacenamiento |

> Las actualizaciones sin downtime requieren que la aplicación y la configuración soporten esa forma de actualización. La plataforma proporciona mecanismos para realizarlas, pero la continuidad no es una propiedad automática de cualquier despliegue.

> Sin una plataforma de orquestación, gestionar grandes arquitecturas de **microservicios** sería muy difícil: el número de instancias y sus relaciones cambia continuamente. La orquestación coordina esa evolución.

### VI. Platforms, Automation and Security

#### 14. Cloud Platforms

> Entre las plataformas de nube pública están **Amazon Web Services, Google Cloud, Microsoft Azure y Alibaba Cloud**. Para construir entornos privados se utilizan soluciones como **VMware, OpenStack** —open source— y **OpenShift Virtualization**.

> Comparar plataformas requiere estudiar las capacidades que ofrecen y cómo encajan con la aplicación:

| Feature | What to compare |
| --- | --- |
| **APIs** | Cómo crear, configurar y administrar recursos mediante software |
| **IAM —Identity and Access Management—** | Cómo gestionar identidades, roles y permisos |
| **Availability zones** | Cómo organizar recursos en zonas de disponibilidad para diseñar resiliencia |
| **Fault tolerance and failover** | Cómo mantener o recuperar el servicio ante fallos |
| **Elasticity** | Cómo ajustar capacidad a la carga |
| **Migration** | Cómo trasladar aplicaciones y datos |
| **Monitoring, logging and tracing** | Cómo observar estado, eventos y recorrido de operaciones |
| **Services provided** | Qué servicios necesita la solución y cuáles ofrece la plataforma |

> **Monitoring** permite seguir métricas y estados; **logging** registra eventos; **tracing** ayuda a seguir una operación a través de sus componentes. Las tres capacidades aportan información complementaria para operar sistemas distribuidos.

#### 15. Automation and Orchestration

##### 15.1. Scope and Purpose

> La escala, complejidad, heterogeneidad y cambio constante del cloud hacen imprescindible automatizar tanto en el **proveedor** como en el **cliente**. Las operaciones manuales repetidas dificultan mantener sistemas coherentes y reaccionar con rapidez.

> La automatización cubre creación y despliegue de recursos, supervisión de cargas, contabilización del uso, gestión del ciclo de vida, escalado y **self-healing** —acciones automáticas para recuperar componentes o corregir incidencias detectadas—.

> **Automatización** ejecuta tareas sin intervención manual en cada paso. **Orquestación** coordina los subsistemas y tareas necesarios para desplegar, actualizar, escalar y operar un servicio completo. Por ejemplo, un servicio puede necesitar cómputo, red y almacenamiento configurados de forma compatible.

##### 15.2. Declarative Approaches and Infrastructure as Code

> Un enfoque **declarativo**, basado en intención, describe el estado que se quiere alcanzar. El sistema de automatización decide qué acciones debe realizar para aproximar el estado real al deseado. Esto facilita gestionar entornos que cambian constantemente.

> **Infrastructure as Code —IaC—** trata la infraestructura virtualizada como el software de una aplicación: su configuración se expresa mediante código o definiciones que pueden gestionarse en un sistema de control de versiones.

> IaC facilita preparar y clonar entornos con agilidad, mantener configuraciones consistentes y reducir el esfuerzo de administración. Versionar las definiciones permite conservar y revisar los cambios de configuración.

##### 15.3. DevOps

> **DevOps** integra el desarrollo y la operación de aplicaciones para mejorar agilidad, eficiencia y calidad. Requiere automatizar el flujo de trabajo completo: **desarrollo, pruebas, despliegue y operación**.

> IaC contribuye a reproducir los entornos y la orquestación coordina su operación. DevOps integra estas capacidades dentro del proceso de entrega y mantenimiento de la aplicación.

#### 16. Cloud Security

##### 16.1. Cloud-Specific Risks

> Cloud computing introduce o aumenta ciertos riesgos. Una arquitectura y unos sistemas de gestión más complejos amplían la **superficie de ataque**, también en aplicaciones cloud native. Esa complejidad aumenta las oportunidades de errores de configuración explotables.

> La infraestructura puede compartirse entre varios tenants. El aislamiento puede fallar debido a bugs de hardware o software o a configuraciones incorrectas. Además, las interfaces de administración accesibles por Internet requieren proteger especialmente el acceso de gestión.

> También deben considerarse aspectos legales y de privacidad relacionados con datos y servicios. El reparto de responsabilidades depende del modelo de servicio, por lo que la seguridad debe contemplar las capas que administra cada parte.

##### 16.2. Security Practices

> Las buenas prácticas generales de seguridad IT siguen siendo necesarias. A ellas se añaden decisiones sobre el despliegue y la administración cloud:

| Practice | Purpose |
| --- | --- |
| Elegir modelos de servicio y despliegue apropiados | Ajustar control y responsabilidades a las necesidades |
| Utilizar **MFA —Multi-Factor Authentication—** | Reforzar la autenticación combinando factores |
| Aplicar **least privilege** | Conceder solo los permisos necesarios |
| Mantener **separation of duties** | Repartir funciones para limitar la concentración de capacidades sensibles |
| Asignar roles a grupos | Gestionar permisos de forma consistente sin asignarlos individualmente a cada usuario |
| Cifrar datos en tránsito y en reposo | Proteger información durante la comunicación y el almacenamiento |
| Proteger comunicaciones con HTTPS o IPsec | Cifrar comunicaciones de red |
| Aislar redes y utilizar **IDS/IPS** | Limitar exposición y detectar o prevenir intrusiones |
| Adoptar **Zero Trust** | Verificar accesos sin asumir confianza por la ubicación en una red |
| Mantener logging y monitoring adecuados | Detectar incidentes y disponer de información para investigarlos |

> Las medidas se complementan: autenticación robusta identifica al usuario; los permisos limitan lo que puede hacer; el aislamiento y cifrado protegen recursos y comunicaciones; la observación permite detectar comportamientos anómalos.

### VII. Final Summary

> **Cloud computing combina acceso por red, aprovisionamiento bajo demanda, recursos compartidos, elasticidad y medición del uso.** Su funcionamiento se apoya en data centers, conectividad y virtualización.

| Decision or technology | Main question |
| --- | --- |
| **Service model** | ¿Qué parte de la pila gestiona el proveedor y qué parte el cliente? |
| **Deployment model** | ¿Quién utiliza la infraestructura y cómo se combinan los entornos? |
| **Virtualization** | ¿Cómo se abstraen y asignan recursos físicos? |
| **Containers** | ¿Cómo se empaqueta y ejecuta una aplicación con sus dependencias? |
| **Orchestration** | ¿Cómo se coordinan los componentes y su ciclo de vida? |
| **IaC** | ¿Cómo se define y mantiene la infraestructura mediante código? |
| **DevOps** | ¿Cómo se integra desarrollo, pruebas, despliegue y operación? |
| **Security** | ¿Cómo se protegen identidades, datos, configuración y recursos compartidos? |

> **IaaS** entrega infraestructura, **PaaS** añade una plataforma gestionada y **SaaS** entrega la aplicación completa. **CaaS** facilita ejecutar aplicaciones en contenedores y **FaaS** permite ejecutar funciones activadas por eventos.

> Las VMs tienen sistemas operativos invitados y se ejecutan mediante un hipervisor. Los contenedores comparten el kernel del host y se crean a partir de imágenes. La orquestación permite gestionar sus despliegues, conexiones, escalado y salud.

> La virtualización de red crea redes y funciones lógicas; **SDN separa control y reenvío** para hacer la red programable. El almacenamiento se puede ofrecer mediante bloques, archivos u objetos.

> La adopción del cloud aporta agilidad y capacidad de crecimiento, pero exige evaluar coste y rendimiento, administrar las responsabilidades que conserva el cliente y atender seguridad, privacidad, interoperabilidad y cambios organizativos.
