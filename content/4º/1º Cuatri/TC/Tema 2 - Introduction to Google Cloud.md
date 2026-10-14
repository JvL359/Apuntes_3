---
estado: pendiente de revisión
---

### I. Google Cloud Infrastructure

#### 1. Regions, Zones and Global Connectivity

> **Google Cloud** ofrece servicios de computación, red y almacenamiento sobre una infraestructura distribuida. Una **region** agrupa infraestructura en una ubicación geográfica; dentro de ella existen varias **zones**, que permiten distribuir los recursos entre dominios de fallo distintos. Elegir región y zona determina dónde se ejecuta una carga y condiciona su proximidad a los usuarios, la latencia y las opciones de disponibilidad.
>
> Las regiones se conectan mediante el **Google backbone**, una red de enlaces terrestres y submarinos. Los **Points of Presence (PoPs)** permiten conectar esa red con operadores, clientes y otras redes. En el borde aparecen servicios de peering, CDN y nodos de caché, que acercan el contenido a los usuarios y reducen recorridos hasta los centros de datos.
>
> Hay que distinguir la ubicación de los recursos de los puntos de entrada a la red: un usuario puede entrar por un PoP cercano y acceder a una aplicación desplegada en otra región. Una empresa también puede conectar su centro de datos con Google mediante **Dedicated Interconnect** o **Partner Interconnect**, en lugar de transportar todo el tráfico por Internet.

### II. Resources and Identity and Access Management

#### 2. Resource Hierarchy

> La jerarquía organiza los recursos y proporciona ámbitos donde aplicar políticas. Sus niveles principales son **Organization → Folders → Projects → Resources**:
>
> - **Organization**: representa a la organización y constituye la raíz de su estructura.
> - **Folders**: agrupan departamentos, equipos o áreas. Pueden contener otras carpetas y proyectos.
> - **Projects**: agrupan los recursos de una aplicación o entorno y permiten separar su administración.
> - **Resources**: elementos concretos, como máquinas virtuales, discos o subredes.
>
> La figura muestra carpetas departamentales y de equipos, con proyectos distintos para producción y desarrollo. Esta separación permite administrar conjuntamente recursos relacionados sin mezclar ámbitos de confianza.

![[apuntes-b0148c0c11a8-p0007-2d50049d9752.png]]

> En las políticas de concesión de acceso, los permisos otorgados en un nivel superior se heredan hacia sus descendientes. Por ello, conceder un rol en una carpeta afecta a los proyectos que cuelgan de ella, mientras que concederlo en un proyecto limita ese alcance. La ubicación de una concesión importa tanto como el rol elegido.

#### 3. Principals, Permissions, Roles and Policies

##### 3.1. Principals and Permissions

> **Identity and Access Management (IAM)** responde a tres preguntas: **quién** puede realizar **qué acciones** sobre **qué recurso**. El quién es el **principal**, que puede corresponder a una cuenta de usuario de Google, un Google Group, una service account o un dominio de Google Workspace/Cloud Identity.
>
> Un **permission** representa una operación concreta, como consultar o detener una instancia. Los permisos se agrupan en **roles**; un rol se concede a uno o varios principals sobre un ámbito determinado. No basta con que una persona esté autenticada: debe disponer de los permisos necesarios sobre el recurso de la operación.
>
> La referencia de permisos relaciona cada operación con los roles que la incluyen. Por ejemplo, `accessapproval.requests.approve` permite aprobar una solicitud de Access Approval, mientras que `accessapproval.requests.get` permite consultarla. Un rol de lectura puede incluir la segunda operación sin permitir la primera.

##### 3.2. Role Types

| Tipo | Característica | Ejemplo |
| --- | --- | --- |
| **Basic roles** | Conjuntos amplios de permisos que abarcan muchos servicios. | Los roles clásicos Viewer, Editor y Owner. |
| **Predefined roles** | Google define conjuntos orientados a tareas de un servicio. | Un rol de administración de instancias de Compute Engine. |
| **Custom roles** | La organización selecciona los permisos que necesita una tarea específica. | Un operador que consulta, inicia y detiene instancias. |

> **Viewer** permite consultar recursos; **Editor** añade operaciones de modificación; **Owner** añade capacidades administrativas, como gestionar el acceso al proyecto. Su amplitud explica por qué conviene buscar un rol más limitado cuando la tarea está bien delimitada.
>
> En el ejemplo de un **Instance Admin**, aparecen permisos como `compute.instances.delete`, `compute.instances.get`, `compute.instances.list`, `compute.instances.setMachineType`, `compute.instances.start` y `compute.instances.stop`. Un **Instance Operator** personalizado puede limitarse a `get`, `list`, `start` y `stop`: puede operar la instancia, pero no eliminarla ni cambiar su tipo de máquina.
>
> Los custom roles se **crean a nivel de proyecto u organización**, no como definiciones pertenecientes a una carpeta. Hay que separar el lugar donde se define el rol del ámbito donde se concede acceso.

> [!warning] Corrección
> En el material aparece Billing Admin dentro de los basic roles, pero la clasificación correcta de Billing Account Administrator (`roles/billing.admin`) es la de un rol predefinido de facturación.
> Fuente de comprobación: [Google Cloud IAM: roles y permisos de Cloud Billing](https://docs.cloud.google.com/iam/docs/roles-permissions/billing)

##### 3.3. Policy Bindings

> Un **binding** asocia un rol con sus miembros. Una **IAM policy** reúne bindings y se aplica a un recurso. En esta política, Alice y el grupo de desarrolladores reciben `roles/viewer`, mientras que la service account recibe `roles/storage.objectAdmin`.

```json
{
  "version": 3,
  "etag": "BwYJ8abc123=",
  "bindings": [
    {
      "role": "roles/viewer",
      "members": [
        "user:alice@example.com",
        "group:developers@example.com"
      ]
    },
    {
      "role": "roles/storage.objectAdmin",
      "members": [
        "serviceAccount:app@mypro.iam.gserviceaccount.com"
      ]
    }
  ]
}
```

> Los prefijos `user:`, `group:` y `serviceAccount:` identifican el tipo de principal. `bindings` contiene las concesiones y `role` nombra el conjunto de permisos. `version` y `etag` son metadatos de la política.
>
> El JSON no indica por sí solo dónde se aplica la política: su alcance lo determina **el recurso al que se adjunta**. Si se aplica a un proyecto, la concesión puede alcanzar recursos descendientes; si se aplica a un recurso concreto compatible con IAM, el alcance es más limitado. Además, Object Admin se refiere a operaciones sobre objetos de almacenamiento, no a administrar todos los servicios.

#### 4. Service Accounts and IAM Best Practices

> Una **service account** representa una aplicación o carga de trabajo, en lugar de una persona. Tiene una dirección de correo única y puede autenticarse para llamar a APIs con los permisos que se le hayan concedido. Las credenciales permiten demostrar esa identidad; esto no exige que toda aplicación descargue y gestione manualmente una clave, porque una carga puede utilizar la identidad asociada a su entorno.
>
> La service account desempeña dos papeles distintos: es un **principal** cuando accede a otros recursos y es un **resource** cuando se administra quién puede gestionarla o usar su identidad. Poder modificar una cuenta de servicio y poder ejecutar una carga con ella son capacidades diferentes.
>
> El rol **Service Account User** permite actuar como la cuenta de servicio en operaciones que requieren `actAs`, por ejemplo al asociarla a una carga. Debe concederse con cuidado: permitir configurar una carga que utiliza esa identidad puede dar acceso indirecto a sus permisos.
>
> Las prácticas básicas de IAM son:
>
> - Agrupar en un proyecto componentes que comparten el mismo **trust boundary**.
> - Aplicar **least privilege**: conceder solo los permisos necesarios.
> - Conceder roles a **grupos**, para gestionar sus miembros sin rehacer todas las políticas individuales.
> - Restringir los permisos para usar service accounts.
> - Dar nombres visibles claros a las cuentas de servicio, de modo que su finalidad sea reconocible.
>
> Estas decisiones se complementan: separar producción y pruebas en proyectos distintos ayuda poco si se concede un rol demasiado amplio sobre la carpeta que contiene ambos.

### III. Interacting with Google Cloud

#### 5. Management Interfaces

> Existen cuatro vías principales de interacción:
>
> - **Google Cloud Console**: interfaz web para configurar servicios y consultar recursos.
> - **Cloud SDK / Google Cloud CLI**: herramientas de línea de comandos, entre ellas `gcloud`.
> - **Cloud Shell**: entorno de shell accesible desde el navegador, con herramientas de Google Cloud disponibles.
> - **APIs y Google Cloud mobile app**: acceso programático y administración desde dispositivos móviles, respectivamente.
>
> Console y `gcloud` permiten operar sobre los mismos recursos mediante interfaces diferentes. La CLI facilita repetir operaciones y hacer explícitos sus parámetros; las APIs permiten integrarlas en aplicaciones.

#### 6. Gcloud Basics

##### 6.1. Authentication and Project Configuration

> Antes de operar, necesitamos acceso a una cuenta, un proyecto y los permisos apropiados. `PROJECT_ID` es un marcador que debe sustituirse por el identificador real del proyecto. Para crear VMs también deben estar habilitados el servicio correspondiente y la facturación cuando proceda.

```bash
gcloud --version
gcloud auth login
gcloud auth list
gcloud projects list
gcloud config set project PROJECT_ID
gcloud config list
```

> `--version` muestra la versión de las herramientas. `auth login` inicia la autenticación y `auth list` permite comprobar las cuentas disponibles y la activa. `projects list` muestra proyectos accesibles. `config set project` selecciona el proyecto predeterminado y `config list` permite revisar la configuración.
>
> **Seleccionar un proyecto no concede permisos sobre él**. Si una operación falla por autorización, cambiar su identificador no resuelve la ausencia del permiso.

##### 6.2. Instance Creation and SSH Access

> Los ejemplos utilizan `my-vm` y la zona `us-central1-a`. `VM_NAME` debe sustituirse por el nombre de una instancia existente; para conectarse a la recién creada, sería `my-vm`. La zona identifica dónde está la VM y debe coincidir con la del recurso.

```bash
gcloud compute instances list
gcloud compute instances create my-vm --zone=us-central1-a
gcloud compute ssh VM_NAME
gcloud compute ssh VM_NAME --tunnel-through-iap
```

> `instances list` permite inspeccionar las instancias; `instances create` crea la VM. `compute ssh` establece una conexión SSH. Si la zona no está configurada ni indicada, debe seleccionarse cuando la herramienta lo solicite.
>
> `--tunnel-through-iap` utiliza **Identity-Aware Proxy (IAP)** para transportar la conexión. La opción necesita los permisos y la configuración de red correspondientes; añadir el argumento no configura por sí solo IAP ni las reglas que permiten el acceso SSH.

##### 6.3. Stopping and Starting an Instance

```bash
gcloud compute instances stop my-vm --zone=us-central1-a
gcloud compute instances start my-vm --zone=us-central1-a
```

> `stop` detiene la ejecución y `start` vuelve a arrancar la instancia. **Detener y eliminar son operaciones distintas**: una VM detenida conserva su recurso y puede arrancarse de nuevo. Más adelante veremos la distinción entre detener, suspender y hacer reset.

##### 6.4. IAM Changes and Command Help

> El siguiente comando añade al proyecto `my-project` una concesión del rol Viewer para Alice. Es una modificación de su política IAM y requiere permisos para administrarla.

```bash
gcloud projects add-iam-policy-binding my-project --member="user:alice@example.com" --role="roles/viewer"
```

> La ayuda puede consultarse sobre toda la herramienta, sobre un grupo o sobre un comando concreto:

```bash
gcloud help
gcloud compute help
gcloud compute instances create --help
```

> [!warning] Corrección
> En el material aparecen guiones tipográficos en `–version` y `–help` y espacios dentro del valor de `--member`, pero la sintaxis correcta es `--version`, `--help` y `--member="user:alice@example.com"`, con dos guiones ASCII y sin esos espacios.
> Fuente de comprobación: [Referencia de gcloud](https://docs.cloud.google.com/sdk/gcloud/reference) y [add-iam-policy-binding](https://docs.cloud.google.com/sdk/gcloud/reference/projects/add-iam-policy-binding)

### IV. Networking

#### 7. Virtual Private Cloud

> Una **Virtual Private Cloud (VPC)** es una red privada virtual implementada en Google Cloud. Conecta recursos y proporciona funciones de **routing** y **firewall**. Las VPC están lógicamente aisladas entre sí; para comunicar redes o conectar servicios hay que establecer las conexiones y reglas adecuadas.
>
> La VPC es un recurso **global**, pero sus **subnets son regionales**. Una subred puede contener recursos situados en distintas zonas de su región. En el ejemplo, `vpc1` tiene una subred `10.0.0.0/24` en `asia-east1` y otra `10.0.1.0/24` en `us-east1`; cada una abarca varias zonas.

![[apuntes-b0148c0c11a8-p0018-456cf148e1ea.png]]

> Compartir subred no obliga a compartir zona. Esto permite distribuir instancias entre zonas conservando una misma organización de direcciones regional. La conectividad con Internet también depende de rutas, reglas y mecanismos de acceso: pertenecer a una VPC no implica que una VM privada quede expuesta públicamente.

#### 8. Premium and Standard Network Tiers

> **Premium Tier** transporta el tráfico durante gran parte del recorrido por la red de Google y lo entrega a redes externas cerca del destino. Este enfoque se denomina **cold potato routing**: Google conserva el tráfico más tiempo en su backbone.
>
> **Standard Tier** entrega el tráfico a Internet cerca de su origen y utiliza más recorrido sobre redes de terceros. Es **hot potato routing**, orientado a reducir el coste de transporte. La diferencia principal es quién controla la mayor parte del trayecto.

![[apuntes-b0148c0c11a8-p0019-c8ffa7b62a7c.png]]

> Premium prioriza la calidad y previsibilidad del transporte; Standard prioriza el coste. La figura representa tráfico desde una región hacia un usuario: arriba sale de Google cerca del usuario y abajo cerca de la región. Es una comparación de arquitectura, no una garantía de que cualquier petición tenga siempre una latencia determinada.

#### 9. Network Connectivity and Delivery Services

| Servicio | Función |
| --- | --- |
| **VPC Network Peering** | Conecta VPC para intercambiar tráfico privado. |
| **Shared VPC** | Permite que recursos de varios proyectos compartan una red VPC y sus subredes. |
| **Cloud Load Balancing** | Distribuye tráfico entre varios backends mediante balanceadores gestionados y distribuidos. |
| **Cloud DNS** | Proporciona resolución de nombres hacia direcciones y otros registros DNS. |
| **Cloud CDN** | Sirve contenido desde cachés de la red global próximas a los usuarios. |
| **Cloud NAT** | Permite conexiones salientes de recursos sin IP externa, con las respuestas asociadas. |

> **Peering** conecta redes distintas, mientras que **Shared VPC** permite utilizar una misma red desde proyectos diferentes. En este último caso, los recursos pueden comunicarse mediante direcciones internas dentro de la red compartida.
>
> DNS ayuda a localizar el servicio; el balanceador decide a qué backend enviar el tráfico; CDN evita llegar al origen cuando puede responder desde caché. **NAT** resuelve otra necesidad: una instancia privada puede iniciar conexiones hacia Internet sin aceptar por ello conexiones entrantes nuevas desde Internet.

#### 10. Hybrid Connectivity

> **Cloud VPN** extiende una red externa hacia Google mediante túneles **IPsec** sobre Internet. Es una opción de configuración relativamente rápida para establecer una conexión cifrada. La referencia de rendimiento de aproximadamente **1,5–3 Gbps por túnel** debe interpretarse como una magnitud orientativa: el caudal real depende, entre otros factores, del tamaño de los paquetes y del trayecto. Una arquitectura con varios túneles puede agregar capacidad y mejorar disponibilidad.
>
> **Cloud Interconnect** proporciona conectividad privada para grandes volúmenes de tráfico, con latencia y jitter más previsibles. **Dedicated Interconnect** utiliza circuitos dedicados hacia Google; **Partner Interconnect** utiliza un proveedor de servicios.

| Alternativa | Camino de conexión | Referencia de capacidad | Uso característico |
| --- | --- | --- | --- |
| Cloud VPN | Túnel IPsec sobre Internet. | Orden de unos Gbps por túnel. | Conexión segura y rápida de establecer. |
| Dedicated Interconnect | Circuitos dedicados. | Ejemplos de enlaces de 10 y 100 Gbps. | Tráfico privado de gran volumen. |
| Partner Interconnect | Conexión a través de un proveedor. | Capacidades ajustables desde 50 Mbps, según la oferta. | Conectividad privada con capacidad adaptada al cliente. |

> [!warning] Corrección
> En el material aparece un intervalo de 50 Mbps a 10 Gbps para Partner Interconnect, pero 10 Gbps no es su límite superior general: existen capacidades mayores y su disponibilidad depende del proveedor.
> Fuente de comprobación: [Google Cloud: elección del producto de conectividad](https://docs.cloud.google.com/network-connectivity/docs/how-to/choose-product)

#### 11. Load Balancer Types

> La selección empieza por el protocolo y el nivel de procesamiento. Un **Application Load Balancer** procesa tráfico **HTTP/HTTPS**. Un **Network Load Balancer** cubre necesidades de transporte y red; los protocolos concretos que admite dependen de su modalidad.
>
> También hay que elegir exposición **external** o **internal**, y alcance **regional**, **global** o **cross-region**. Un balanceador externo recibe tráfico desde fuera de la red privada; uno interno distribuye tráfico privado. Regional limita su alcance a una región, mientras que global o cross-region permite distribuir entre regiones según el producto.

| Familia | Modalidad | Exposición | Alcances de la clasificación |
| --- | --- | --- | --- |
| Application Load Balancer | HTTP/HTTPS | External | Global o regional. |
| Application Load Balancer | HTTP/HTTPS | Internal | Regional o cross-region. |
| Network Load Balancer | Proxy | External | Global o regional. |
| Network Load Balancer | Proxy | Internal | Regional o cross-region. |
| Network Load Balancer | Passthrough | External | Regional. |
| Network Load Balancer | Passthrough | Internal | Regional. |

> En un balanceador **proxy**, el balanceador termina la conexión del cliente y establece otra hacia el backend. En **passthrough**, reenvía los paquetes sin actuar como ese proxy de terminación. La clasificación general de Network Load Balancing incluye TCP, UDP y otros protocolos IP, pero no todas sus variantes soportan todos esos protocolos.


### V. Compute Engine

#### 12. Compute Products and Service Models

> Los productos de computación cubren distintos grados de gestión. Cuanto más gestionado es el servicio, más tareas de infraestructura asume el proveedor; la elección también determina qué configuración conserva el cliente.

| Modelo | Productos | Unidad principal |
| --- | --- | --- |
| **IaaS** | Bare Metal, Google Cloud VMware Engine (GCVE), Google Compute Engine (GCE). | Infraestructura física dedicada o máquinas virtuales. |
| **CaaS** | Google Kubernetes Engine (GKE). | Contenedores organizados en un clúster Kubernetes. |
| **PaaS** | App Engine, en sus entornos Standard y Flexible; Cloud Run. | Aplicaciones o contenedores sobre una plataforma gestionada. |
| **FaaS** | Cloud Functions / Cloud Run functions. | Funciones invocadas por peticiones o eventos. |

> **Compute Engine** permite crear VMs y elegir su configuración. **GKE** añade la gestión de Kubernetes; **Cloud Run** permite desplegar contenedores sin administrar el clúster; las funciones reducen la unidad de desarrollo a código con una finalidad específica.

#### 13. Machine Families and VM Configuration

##### 13.1. Machine Families

> Una **machine family** orienta la máquina hacia una clase de carga. El **machine type** concreta la configuración de vCPU y RAM. Elegir una familia adecuada exige identificar si el recurso dominante es CPU, memoria, almacenamiento o aceleración.

| Orientación | Series de referencia | Cargas características |
| --- | --- | --- |
| **Efficient** | E | Web y aplicaciones de poco tráfico, desarrollo, pruebas, microservicios y escritorios virtuales. |
| **Flexible** | N | Aplicaciones equilibradas, tráfico bajo o medio, microservicios, escritorios, CRM/BI, pipelines y bases de datos pequeñas o medianas. |
| **Performance** | C | Web de alto tráfico, publicidad, juegos, bases de datos, analítica, cachés, streaming, transcodificación e IA sobre CPU. |
| **Compute** | H | HPC, simulación, dinámica de fluidos, genómica, cálculo científico y modelado financiero. |
| **Memory** | M y X | Bases de datos y cachés grandes en memoria, diseño electrónico, modelado y simulación. |
| **Storage** | Z | Analítica y bases de datos con alto volumen de almacenamiento por núcleo, incluidas cargas distribuidas y optimizadas para flash. |
| **Inference and Visualization with GPUs** | G | Inferencia, entrenamiento compatible con CUDA, visualización y transcodificación de vídeo. |
| **Other GPU Tasks** | A | Cómputo masivamente paralelo, modelos de lenguaje y sistemas de recomendación con deep learning. |

> Las letras identifican series de referencia, no una configuración fija ni una única generación de hardware. La diferencia útil para estudiar es el **perfil de recursos**: las familias generales equilibran coste y rendimiento; las especializadas priorizan cómputo, memoria, almacenamiento o GPU.

##### 13.2. Configuration Choices

> Al crear una VM se seleccionan:
>
> - Región y **zona**.
> - Familia y tipo de máquina, con sus **vCPU y RAM**.
> - **Persistent boot disk**, con el sistema operativo, y su tipo de almacenamiento, por ejemplo HDD o SSD.
> - Discos persistentes adicionales, si la aplicación los necesita.
> - **Local SSD**, si se requiere almacenamiento local de baja latencia.
> - Sistema operativo e imagen de arranque.
> - Aceleradores apropiados para la carga, como GPU; las cargas con TPU utilizan los recursos de Cloud TPU correspondientes.
>
> El **boot disk** contiene el sistema que arranca la máquina; un disco adicional puede separar los datos de la aplicación. Un Persistent Disk y un Local SSD tienen propiedades distintas de persistencia, por lo que no deben elegirse solo por velocidad.
>
> **Cloud Marketplace** ofrece soluciones preconfiguradas de Google y de terceros. Facilita disponer de software ya instalado, aunque siguen siendo necesarias las decisiones de ubicación, permisos, recursos y operación.

#### 14. Maintenance and Availability Policies

> El host físico puede necesitar mantenimiento o sufrir un fallo. Las políticas de disponibilidad determinan cómo responde la VM:
>
> - **Maintenance event**: migración en vivo, cuando la configuración la admite, o detención de la instancia.
> - **Automatic restart**: decisión de reiniciar o dejar la instancia terminada cuando falla, sufre un error del host o deja de responder.
> - **Host error detection time**: tiempo máximo que Compute Engine espera para reiniciar o terminar una instancia después de detectar que no responde.
> - **Local SSD recovery timeout**: tiempo destinado a intentar recuperar datos de los SSD locales. Si no se recuperan, esos datos pueden perderse.
>
> **Live migration** traslada una VM a otro host dentro de la misma zona para realizar mantenimiento sin requerir un reinicio del sistema invitado. Su disponibilidad depende del tipo de instancia y de sus recursos. No equivale a mover la VM a otra región ni sustituye una estrategia de respaldo.

#### 15. Instance Groups and Autoscaling

> Un **instance group** permite administrar varias VMs como un conjunto. Hay dos tipos principales:
>
> - **Managed Instance Group (MIG)**: gestiona instancias con una configuración común y ofrece autoscaling, autohealing, actualizaciones automáticas y despliegue regional entre zonas.
> - **Unmanaged instance group**: agrupa instancias administradas individualmente. Puede utilizarse como conjunto de backends de un balanceador, pero no aporta la misma gestión automática.
>
> **Autoscaling** aumenta o reduce el número de VMs de un MIG según la carga. El balanceador reparte el tráfico entre ellas. **Autohealing** atiende otro problema: sustituir o recuperar instancias que no están sanas.
>
> Escalar y reparar no son lo mismo. Una aplicación puede tener todas sus instancias sanas y necesitar más capacidad; también puede tener carga baja y necesitar reemplazar una VM defectuosa. La distribución entre zonas reduce la dependencia de un único dominio de fallo.

#### 16. Images, Snapshots and Templates

##### 16.1. Disk Images

> Una **disk image** representa el contenido de un disco persistente: estructura del sistema de archivos, datos, software y personalizaciones. Si es una **boot disk image**, incluye además el bootloader y el sistema operativo, de modo que permite crear un disco de arranque nuevo.
>
> Las **public images** proceden de Google, terceros o la comunidad, por ejemplo distribuciones Linux y Windows. Las **custom images** contienen software y configuración preparados para una aplicación. Crear varias VMs desde una imagen común facilita repetir la instalación inicial.
>
> En virtualización existen formatos como `vmdk`, `vhdx`, `vpc`, `vdi` y `qcow2`. Son formatos de representación de discos; su existencia no significa que todos puedan utilizarse directamente como un recurso Image de Compute Engine sin un proceso de importación o conversión compatible.

##### 16.2. Disk Snapshots

> Un **snapshot** captura el contenido de un disco en un instante y permite realizar respaldos **incrementales**. Puede obtenerse tanto si el disco está asociado a una VM en ejecución como si no lo está. Su objeto de respaldo es el disco, por lo que un snapshot de un disco no representa toda la configuración de una VM con varios discos.
>
> Capturar un disco mientras una aplicación está ejecutándose no garantiza por sí solo que todos sus datos formen una copia coherente a nivel de aplicación: hay que distinguir capturar bloques de disco de coordinar una operación de respaldo de la aplicación.

| Tipo | Finalidad | Redundancia y alcance |
| --- | --- | --- |
| **Standard snapshot** | Respaldo para recuperación ante pérdidas y fallos de infraestructura. | Puede usar almacenamiento georredundante en varias regiones según su ubicación. |
| **Archive snapshot** | Retención durante meses o años con acceso poco frecuente; archivo, auditorías y cumplimiento. | Respaldo de menor coste de almacenamiento, con opciones georredundantes. |
| **Instant snapshot** | Restauración rápida tras errores del usuario o corrupción de la aplicación. | Copia local no georredundante, en la misma zona o región que el disco de origen. |

> Un instant snapshot facilita recuperar rápidamente, pero no ofrece la protección geográfica de una copia situada fuera del ámbito del disco. **Rapidez de restauración y protección frente a fallos regionales son criterios distintos**.

##### 16.3. Machine Images and Instance Templates

> Una **machine image** conserva la configuración, metadatos, permisos y datos de los discos persistentes de una VM. Es útil para respaldo, recuperación y clonación de una instancia con varios discos, porque captura más que el contenido de un único disco.
>
> Una **instance template** describe cómo crear instancias: tipo de máquina, imagen de arranque, etiquetas, startup scripts y otras propiedades. Se utiliza para crear VMs o MIGs con una configuración repetible. Es una **receta de creación**, no una copia de los datos actuales de una instancia en ejecución.

| Escenario | Machine image | Persistent disk snapshot | Custom image | Instance template |
| --- | --- | --- | --- | --- |
| Respaldo de un disco | Sí | Sí | Sí | No |
| Respaldo de varios discos de una VM como conjunto | Sí | No | No | No |
| Respaldo basado en diferencias | Sí | Sí | No | No |
| Creación de instancias equivalentes / clonación | Sí | No por sí solo | Sí, desde el disco base | Sí, desde la configuración |
| Replicación de una imagen base | No | No | Sí | No |

> La fila de clonación tiene alcances distintos: la machine image reproduce configuración y discos; una custom image proporciona el contenido base de un disco; una plantilla reproduce una configuración de creación. Una plantilla puede **referirse** a una imagen, pero no es ella misma una imagen ni una copia de seguridad.
>
> Asimismo, es posible hacer snapshots de varios discos por separado, pero eso no convierte cada snapshot en un respaldo completo de todos los discos de la VM. Para elegir, hay que preguntar **qué se desea conservar: un disco, el estado de varios discos con su configuración, o una receta para desplegar instancias nuevas**.

#### 17. VM Lifecycle

| Estado | Significado |
| --- | --- |
| **Provisioning** | Se reservan CPU, memoria y discos para la instancia. |
| **Staging** | Se prepara la ejecución, se asigna la dirección IP y se arranca el sistema. |
| **Running** | La instancia está en ejecución. |
| **Repairing** | Se atiende un error interno o la indisponibilidad del host, por ejemplo durante mantenimiento. |
| **Stopping** | La instancia se está deteniendo. |
| **Terminated** | La instancia está detenida. |
| **Suspending** | Se guarda en almacenamiento el estado necesario para suspenderla, incluido el contenido de memoria. |
| **Suspended** | La instancia permanece suspendida hasta reanudarse. |

> El diagrama distingue las operaciones de inicio, detención, suspensión, reanudación y eliminación. Tras `stop()`, la VM llega a **Terminated** y puede volver a iniciarse con `start()`. Tras `suspend()`, puede reanudarse con `resume()`. La eliminación lleva al final de la existencia del recurso.

![[apuntes-b0148c0c11a8-p0031-1ab2a467f850.png]]

> **Terminated significa detenida, no eliminada**. Suspender conserva el estado de ejecución necesario para continuar; detener supone arrancar otra vez el sistema al iniciar. El **reset** vacía la memoria y reinicia la máquina sin devolver los discos a una copia inicial. La instancia mantiene el estado administrativo Running durante el reset, aunque la aplicación se interrumpe.

#### 18. Compute Engine Billing

> Compute Engine utiliza facturación **por segundo con un mínimo de un minuto** para el cómputo. El modelo basado en recursos considera por separado las vCPU y la memoria, en lugar de entender la VM como un paquete indivisible. Otros recursos asociados, como discos y tráfico, tienen sus propios conceptos de facturación.
>
> Los mecanismos de reducción de coste responden a situaciones diferentes:
>
> - **Sustained-use discounts**: descuentos por uso sostenido de recursos elegibles.
> - **Committed-use discounts**: descuentos vinculados a un compromiso de uso.
> - **Preemptible y Spot VMs**: capacidad de menor coste que puede ser interrumpida por el proveedor.
>
> Los descuentos dependen de la elegibilidad del recurso. Una Spot VM requiere que la carga tolere interrupciones; no debe interpretarse como una instancia ordinaria con idéntica continuidad a menor precio.

### VI. Storage and Database Services

#### 19. Object, Block and File Storage

> La primera decisión de almacenamiento es **cómo necesita acceder la aplicación a los datos**: como objetos completos, como bloques de un disco o como archivos de un sistema compartido.

| Modelo | Producto | Acceso y propiedades | Usos |
| --- | --- | --- | --- |
| **Object storage** | Cloud Storage | Objetos identificados con datos, atributos y metadatos; acceso mediante APIs y URLs. | Imágenes, vídeo, documentos, sitios web, analítica, genómica, backups, archivos regulatorios y disaster recovery. |
| **Persistent block storage** | Persistent Disk | Discos para VMs y GKE, con opciones de latencia y rendimiento. | Discos de VMs, almacenamiento de bases de datos, datos de solo lectura compartidos y respaldos duraderos. |
| **Local block storage** | Local SSD | Almacenamiento local de muy baja latencia, con naturaleza efímera. | Cachés, scratch disks, bases de datos optimizadas para flash, analítica distribuida y renderizado. |
| **File storage** | Filestore | Network Attached Storage (NAS) gestionado para compartir archivos. | Procesamiento multimedia y genómico, diseño electrónico, migraciones, ML, analítica, contenido web y modelado financiero. |

> Un **objeto** se recupera mediante su identificador y no se comporta como un disco de arranque. El almacenamiento por **bloques** ofrece la base sobre la que el sistema puede utilizar un disco. **Filestore** proporciona archivos compartidos para cargas que requieren esa interfaz.
>
> Local SSD resulta útil para datos temporales o reproducibles y para acelerar una carga, pero necesita una estrategia distinta a la de Persistent Disk cuando los datos deben sobrevivir a la pérdida del almacenamiento local.

#### 20. Cloud Storage

##### 20.1. Buckets, Durability and Access

> **Cloud Storage** es almacenamiento de objetos a gran escala. Los objetos se organizan en **buckets** y pueden identificarse mediante URLs. La existencia de una URL no implica acceso público: la autorización sigue determinando quién puede leer o modificar el objeto.
>
> Está diseñado para escalar a volúmenes de exabytes y servir objetos con tiempos de respuesta bajos; un tiempo al primer byte del orden de milisegundos es una referencia de rendimiento, no una latencia fija para cualquier ubicación o petición.
>
> Su durabilidad de diseño de **once nueves, 99,999999999 %**, expresa la protección frente a pérdida de datos. **Durabilidad y disponibilidad no son lo mismo**: conservar el objeto y poder acceder a él en un instante determinado son propiedades distintas.
>
> Los buckets pueden usar ubicaciones **region**, **dual-region** o **multi-region**. Las clases de almacenamiento comparten una API, de modo que cambiar la clase no obliga a cambiar el modelo de acceso de la aplicación.

##### 20.2. Storage Classes and Autoclass

| Clase | Duración mínima de almacenamiento a efectos de cobro | Coste de recuperación | Perfil de uso |
| --- | --- | --- | --- |
| **Standard** | Sin mínimo. | Sin cargo de recuperación por clase. | Acceso frecuente; mayor coste de almacenamiento y disponibilidad más alta. |
| **Nearline** | 30 días. | Cargo por recuperación. | Acceso poco frecuente y almacenamiento de menor coste. |
| **Coldline** | 90 días. | Cargo de recuperación mayor. | Acceso más infrecuente y coste de almacenamiento muy bajo. |
| **Archive** | 365 días. | Cargo de recuperación más alto. | Archivo de largo plazo y menor coste de almacenamiento. |

> El intercambio es **coste de almacenamiento frente a coste de acceso y retención mínima facturable**. Standard puede ser más caro por conservar un GB, pero evita los cargos de recuperación propios de las clases frías. Una duración mínima no significa que sea técnicamente imposible eliminar un objeto antes: puede generar un cargo por eliminación anticipada.
>
> **Autoclass** transiciona automáticamente los objetos entre clases apropiadas según su patrón de acceso. Se utiliza cuando interesa adaptar la clase sin decidir manualmente el destino de cada objeto.
>
> El acceso puede controlarse mediante **IAM** y, cuando la configuración lo permite, **ACLs**. Con acceso uniforme a nivel de bucket se utiliza IAM y se deshabilitan las ACLs. Por tanto, ambos mecanismos no están disponibles simultáneamente en cualquier configuración.

#### 21. Managed Databases and Related Services

> El carácter **managed** significa que Google asume tareas de plataforma, como mantenimiento y parte de la gestión de disponibilidad. La aplicación sigue teniendo que elegir su modelo de datos, capacidad y configuración de acceso.

| Servicio | Modelo | Necesidad principal |
| --- | --- | --- |
| **Cloud SQL** | Relacional. | Aplicaciones web, CMS y comercio electrónico sobre motores conocidos. |
| **Spanner** | Relacional distribuido. | Escala horizontal, consistencia fuerte y alta disponibilidad. |
| **AlloyDB** | Relacional; procesamiento transaccional y analítico. | Cargas híbridas, incluidas necesidades de analítica e IA. |
| **Firestore** | NoSQL documental. | Aplicaciones móviles y web, perfiles y estado de juegos. |
| **Bigtable** | NoSQL de tablas amplias. | Gran volumen de lecturas y escrituras, eventos, IoT y datos financieros. |
| **BigQuery** | Data warehouse. | Analítica empresarial y dashboards. |
| **Memorystore** | Servicios en memoria, como Redis y Memcached. | Caché y automatización de tareas de disponibilidad, failover y mantenimiento. |

##### 21.1. Cloud SQL

> **Cloud SQL** ofrece MySQL, PostgreSQL y SQL Server como servicio. Google gestiona tareas de plataforma como parches, actualizaciones, backups y replicación, por lo que el cliente no necesita instalar ni mantener el software del motor.
>
> La capacidad se dimensiona mediante CPU, RAM y almacenamiento; una referencia de configuración de gran tamaño es **128 cores, 864 GB de RAM y 64 TB de almacenamiento**. Las capacidades admisibles dependen del motor, la edición y el tipo de máquina: estas cifras no definen una configuración universal para todas las instancias.
>
> Puede desplegarse en una zona o en varias zonas **dentro de la misma región**. Distribuirlo entre zonas aumenta la protección frente a un fallo zonal, pero no equivale a distribuir la base entre regiones.
>
> **Cloud SQL Studio** permite ejecutar consultas, crear vistas y modificar esquemas desde la consola.

##### 21.2. Spanner

> **Spanner** combina un modelo relacional y SQL con **escalabilidad horizontal** y **consistencia fuerte**. Gestiona replicación, sharding y procesamiento de transacciones en despliegues distribuidos, incluso entre regiones y continentes.
>
> Está orientado a cargas de decenas de miles de lecturas y escrituras por segundo o más, según el dimensionamiento. La diferencia frente a aumentar la capacidad de una sola instancia es distribuir la capacidad conservando las propiedades del servicio relacional.
>
> Admite configuraciones **regional**, **dual-region** y **multi-region**, y dialectos **GoogleSQL** y **PostgreSQL**. El objetivo de disponibilidad de **99,999 %** corresponde a configuraciones dual-region y multi-region; no debe extenderse automáticamente a una configuración regional.
>
> **Spanner Studio** permite consultar datos, crear vistas y modificar esquemas desde la consola.

##### 21.3. Firestore

> **Firestore** es una base NoSQL documental para aplicaciones móviles, web y de servidor. Ofrece escalabilidad horizontal, escalado automático, seguridad integrada y opciones de replicación multirregional; puede actuar como **Backend as a Service (BaaS)**.
>
> Los datos se organizan en **collections** que contienen **documents**. Cada documento contiene pares clave-valor, puede incluir objetos anidados y puede tener subcolecciones. Esto permite representar estructuras jerárquicas sin convertirlas en tablas relacionales.
>
> Por ejemplo, una colección de usuarios puede contener un documento por usuario y cada documento una subcolección relacionada. **Un campo con un objeto anidado y una subcolección no son la misma estructura**, aunque ambos permiten organizar información dependiente del documento.
>
> Existen **Native mode** y **Datastore mode**, que responden a modelos de uso y compatibilidad diferentes. El objetivo de disponibilidad de **99,999 %** se asocia a ubicaciones multirregionales, no a cualquier despliegue de Firestore.

##### 21.4. Bigtable

> **Bigtable** es una base NoSQL diseñada para cargas masivas con baja latencia y alto throughput, como IoT, analítica de usuarios y datos financieros. Es apropiada para grandes volúmenes de datos estructurados o semiestructurados —por ejemplo, más de 1 TB—, muchas operaciones, datos que cambian rápidamente y series temporales.
>
> Encaja cuando no se necesitan las relaciones y transacciones generales de una base relacional. Esto no significa que sus operaciones carezcan de toda garantía de consistencia; significa que su modelo y sus capacidades transaccionales no sustituyen las de una base relacional para cualquier aplicación.
>
> Se integra con **Hadoop**, **Cloud Dataflow** y **Cloud Dataproc**, y soporta la API de **HBase**. Puede aportar datos a procesos de big data y machine learning.
>
> Su estructura se basa en:
>
> - **Rows**, identificadas por una única **row key**.
> - **Column families**, que agrupan columnas relacionadas.
> - **Cells**, con distintas versiones identificadas mediante timestamps.
> - Tablas **sparse**: las posiciones vacías no ocupan espacio como valores almacenados.
>
> En la figura, la familia `follows` agrupa varias columnas y la row key identifica a cada persona. Algunas intersecciones contienen varias versiones; no se exige que todas las filas tengan valores para todas las columnas.

![[apuntes-b0148c0c11a8-p0040-c63764f648a7.png]]

### VII. Containers, Platforms and Functions

#### 22. Google Kubernetes Engine

> **Google Kubernetes Engine (GKE)** es Kubernetes gestionado por Google. Un **cluster** agrupa nodos, implementados como instancias de Compute Engine, sobre los que se ejecutan las cargas en contenedores.
>
> GKE ofrece dos modos de operación:
>
> - **Autopilot**: Google gestiona la infraestructura subyacente, incluida la configuración de nodos, su escalado, actualizaciones y configuraciones básicas de seguridad y red.
> - **Standard**: el cliente conserva más control sobre esa infraestructura, incluida la configuración de los nodos.
>
> Un **node pool** agrupa un subconjunto de nodos del clúster con características comunes. Permite combinar configuraciones adecuadas para cargas diferentes, en lugar de tratar todos los nodos como equivalentes.
>
> Las funciones de gestión incluyen balanceo de carga, escalado automático del número de nodos, actualizaciones del software, **node auto-repair** y logging y monitoring mediante **Google Cloud Observability**. El auto-repair persigue recuperar la salud del clúster; el autoscaling adapta su capacidad.

#### 23. Cloud Run

##### 23.1. Execution and Scaling

> **Cloud Run** es una plataforma gestionada para ejecutar contenedores sin administrar servidores o un clúster. Los servicios pueden responder a peticiones web y recibir eventos, por ejemplo procedentes de Pub/Sub. Entre sus cargas aparecen frontends, backends, jobs de procesamiento por lotes, LLMs y procesamiento de colas.
>
> Para los servicios, los contenedores deben diseñarse como **stateless**: el estado que deba persistir se mantiene en servicios de almacenamiento apropiados. Así, añadir o retirar instancias no hace depender la continuidad de datos guardados solo en una instancia.
>
> El servicio puede **escalar a cero** y volver a crear instancias cuando llegan peticiones. El arranque de una instancia nueva introduce un tiempo de inicialización, por lo que la rapidez del escalado no debe interpretarse como ausencia absoluta de cold starts. También puede configurarse acceso bajo demanda a **GPU NVIDIA L4** para cargas de inferencia.

##### 23.2. Developer Workflow

> El flujo de despliegue de un servicio tiene tres etapas:
>
> 1. **Escribir la aplicación**, que inicia un servidor capaz de escuchar peticiones web.
> 2. **Construir y empaquetar** la aplicación en una imagen de contenedor.
> 3. **Publicar la imagen en Artifact Registry y desplegarla en Cloud Run**.
>
> Tras el despliegue se obtiene una **URL HTTPS**. Cloud Run inicia contenedores para atender peticiones y ajusta su número según la demanda y la configuración. Artifact Registry almacena la imagen; publicar en el registro y desplegar el servicio son pasos relacionados, pero la publicación no despliega por sí sola la aplicación.

##### 23.3. Billing Conditions

> La facturación utiliza intervalos de **100 ms**, redondeados hacia arriba, pero el periodo facturable depende del modo configurado. La facturación basada en peticiones y la facturación basada en instancias tienen condiciones diferentes. Mantener instancias mínimas puede producir costes aun cuando no estén procesando peticiones.

> [!warning] Corrección
> En el material aparece que Cloud Run solo cobra recursos usados y que nunca se pagan recursos sobredimensionados, pero la afirmación correcta depende del modo de facturación: las instancias mínimas pueden generar costes en reposo y la facturación basada en instancias cobra su tiempo de vida, incluso sin peticiones.
> Fuente de comprobación: [Google Cloud Run: precios y condiciones de facturación](https://cloud.google.com/run/pricing)

#### 24. Cloud Run Functions

> **Cloud Run functions**, también denominado Cloud Functions, permite desarrollar funciones pequeñas de una finalidad concreta, activadas por eventos o peticiones, sin gestionar el servidor ni el entorno de ejecución subyacente.
>
> Soporta código en **Node.js, Python, Go, Java, .NET, Ruby y PHP**. Los eventos de **Cloud Storage** y **Pub/Sub** permiten invocaciones asíncronas; una invocación **HTTP** permite interacción síncrona.
>
> La facturación se expresa con granularidad de **100 ms** para el tiempo facturable de ejecución. La idea de pagar solo mientras se ejecuta código debe leerse con las condiciones de configuración del servicio: mantener instancias mínimas puede generar también cargos en reposo.
>
> La diferencia de unidad de desarrollo ayuda a elegir: en Cloud Run se despliega una aplicación empaquetada como contenedor; en functions se escribe una función para responder a una petición o evento. Ambas opciones reducen la administración de infraestructura, aunque la aplicación sigue siendo responsable de sus datos, permisos y lógica.

### VIII. Final Summary

> Para diseñar una aplicación en Google Cloud hay que coordinar cinco decisiones:
>
> - **Organización y acceso**: la jerarquía establece ámbitos; IAM une principals, roles y recursos. Los permisos mínimos y las service accounts adecuadas delimitan lo que puede hacer cada carga.
> - **Ubicación y red**: una VPC es global y sus subredes son regionales. Premium y Standard cambian el recorrido del tráfico; VPN e Interconnect conectan la red externa; DNS, balanceo, CDN y NAT resuelven funciones diferentes.
> - **Computación**: Compute Engine ofrece control de la VM; GKE gestiona Kubernetes; Cloud Run ejecuta contenedores y functions ejecuta funciones. La familia de máquina debe ajustarse al recurso dominante de la carga.
> - **Persistencia y recuperación**: Cloud Storage almacena objetos, Persistent Disk y Local SSD ofrecen bloques, y Filestore comparte archivos. Una imagen, un snapshot, una machine image y una plantilla conservan elementos distintos.
> - **Modelo de datos y operación**: Cloud SQL proporciona motores relacionales gestionados; Spanner distribuye un modelo relacional; Firestore organiza documentos y Bigtable atiende grandes volúmenes NoSQL. Capacidad, disponibilidad y facturación deben interpretarse con las condiciones del despliegue.
>
> El punto común es que **un servicio gestionado reduce tareas de plataforma, pero no decide por la aplicación sus permisos, estructura de datos, tolerancia a fallos ni dimensionamiento**.


