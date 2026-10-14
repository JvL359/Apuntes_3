---
estado: pendiente de revisión
---

### I. Infraestructura como código

#### 1. Relación entre IaaS e IaC

> **Infrastructure as a Service (IaaS)** proporciona recursos de infraestructura, como máquinas virtuales, discos y redes. **Infrastructure as Code (IaC)** describe y administra esos recursos mediante archivos de configuración y automatización. IaaS es un modelo de servicio; IaC es una forma de gestionar infraestructura.
>
> La automatización también puede utilizarse sobre **PaaS**, donde se administran servicios gestionados y plataformas de ejecución. Por tanto, IaC no está limitada a crear VMs: puede describir bases de datos, almacenamiento, redes o recursos de Kubernetes.
>
> En lugar de configurar cada entorno manualmente, se conserva una definición que permite revisar, reproducir y modificar su configuración. El estado deseado expresa qué debe existir; la herramienta calcula o ejecuta las acciones necesarias para aproximarse a él.

#### 2. Beneficios, herramientas y contenedores

> Los beneficios principales son:
>
> - **Consistencia**: entornos reproducibles a partir de una configuración conocida.
> - **Escalabilidad**: provisión y adaptación de recursos bajo demanda.
> - **Eficiencia**: automatización que reduce trabajo repetitivo y errores manuales.
> - **Versionado**: historial de cambios mediante sistemas como Git.
>
> Consistencia no exige que desarrollo y producción tengan idéntico tamaño. Una configuración puede compartir estructura y variar sus parámetros para cada entorno.

| Herramienta | Enfoque |
| --- | --- |
| **Terraform / OpenTofu** | Aprovisionamiento declarativo mediante providers, con soporte para distintos clouds. |
| **Ansible** | Configuración, automatización y orquestación mediante tareas. |
| **AWS CDK** | Definición de infraestructura de AWS mediante código. |
| **Pulumi** | Infraestructura utilizando lenguajes de programación. |
| **Crossplane** | Gestión declarativa de infraestructura a través de la interfaz de Kubernetes. |

> **Docker** empaqueta aplicaciones en contenedores portables; **Kubernetes** administra sus despliegues, escalado, recuperación y balanceo. IaC permite preparar la infraestructura sobre la que se ejecuta ese sistema.
>
> Un ejemplo combina Terraform/OpenTofu para configurar el clúster, manifiestos YAML para Pods y Services y un mecanismo de escalado basado en CPU. **Crear el clúster, desplegar cargas y configurar su escalado son decisiones diferentes**, aunque se integren en un mismo proceso.

#### 3. Ciclo de vida y buenas prácticas

> El ciclo de vida incluye **diseño → código → despliegue y verificación → actualizaciones → mantenimiento y monitorización**. En cada cambio se vuelve a describir la configuración, evaluar su efecto y comprobar el resultado.
>
> El código de infraestructura también puede seguir un proceso de control de versiones, revisión, validación e integración antes de desplegar. La figura sitúa esas actividades entre la escritura y la ejecución sobre un proveedor.

![[apuntes-4d98735752f7-p0007-68852c3d29e9.png]]

> Las buenas prácticas son mantener el código en control de versiones, probar en entornos previos a producción, automatizar pruebas y despliegues mediante **CI/CD**, y documentar scripts y configuraciones. Tener código versionado facilita la auditoría, pero no sustituye revisar los cambios que realmente se aplicarán.

### II. Terraform y OpenTofu

#### 4. Estado deseado, planificación y licencias

> **Terraform** permite construir, modificar y versionar infraestructura. Genera un **plan de ejecución** que anticipa las acciones necesarias para alcanzar el estado deseado. Si cambia la configuración, calcula cambios incrementales: no necesita recrear necesariamente todo el entorno.
>
> Terraform apareció en **2014** como proyecto open source. El cambio posterior de licencia de HashiCorp de **MPL a BSL** motivó la creación de **OpenTofu**, un fork orientado a mantener una alternativa open source con gobernanza bajo la Linux Foundation.
>
> OpenTofu conserva una experiencia basada en **HCL**, providers y comandos como `init`, `plan` y `apply`. Su evolución es independiente, con enfoque comunitario y roadmap abierto. La compatibilidad facilita la continuidad de configuraciones y proveedores, pero una migración debe revisar versiones, funcionalidades y estado: no implica intercambiabilidad automática de cualquier versión futura.
>
> Para las organizaciones, mantener una alternativa open source reduce la dependencia de futuros cambios de licencia y ofrece continuidad para entornos empresariales. La compatibilidad del enfoque facilita la migración desde Terraform, con las comprobaciones de versiones y estado correspondientes.
>
> Las características comunes incluyen soporte para varios clouds, **idempotencia**, archivos de estado y módulos reutilizables. En un enfoque declarativo se describe qué recursos se necesitan; la herramienta determina las operaciones de provisión.
>
> **Idempotencia** significa que repetir la aplicación de una misma configuración sobre un entorno ya reconciliado no debería generar cambios adicionales. No significa que cualquier script externo ejecutado durante el proceso sea también idempotente.

#### 5. Providers, recursos y módulos

> Un **provider** integra la herramienta con una API y define los tipos de recursos administrables. Entre los entornos disponibles aparecen AWS, Azure, IBM Cloud, Google Cloud, DigitalOcean, Oracle Cloud Infrastructure, VMware vSphere, OpenStack y el ecosistema de OpenShift.
>
> Un **resource** describe un objeto básico. Un **module** agrupa recursos y sus relaciones para representar un sistema mayor y reutilizarlo. La dirección de un recurso combina su tipo y su nombre local; ese nombre local no tiene por qué ser el nombre del objeto en el proveedor.
>
> Por ejemplo, se puede declarar una floating IP de OpenStack en el pool `ext-net`:

```hcl
resource "openstack_networking_floatingip_v2" "tf_vm_ip" {
  pool = "ext-net"
}
```

> `openstack_networking_floatingip_v2` es el tipo que aporta el provider y `tf_vm_ip` identifica el recurso dentro de la configuración. El provider de OpenStack y el pool deben estar preparados para utilizarlo.
>
> En Google Cloud pueden gestionarse instancias, imágenes, redes, App Engine, Cloud SQL, recursos de analítica y datos como BigQuery/Firebase, Kubernetes y Cloud Storage, mediante los providers y recursos apropiados. **Multi-cloud no significa que todos los proveedores utilicen los mismos tipos de recurso**.

#### 6. Organización de archivos

> Los archivos de una configuración se separan por responsabilidad. No se ejecutan por el orden de sus nombres: los archivos `.tf` del directorio forman un módulo y las referencias entre recursos determinan dependencias.

```text
proyecto/
├── main.tf
├── plantilla.tpl
├── script.sh
├── providers.tf
├── variables.tf
├── terraform.tfvars
└── outputs.tf
```

| Archivo | Contenido |
| --- | --- |
| `main.tf` | Definiciones de recursos y sus relaciones. |
| `providers.tf` | Providers requeridos y configuración de acceso. |
| `variables.tf` | Declaraciones de variables de entrada. |
| `terraform.tfvars` | Valores concretos para variables declaradas. |
| `outputs.tf` | Salidas de la configuración. |
| `plantilla.tpl` | Plantilla con contenido parametrizable. |
| `script.sh` | Script de inicialización o configuración. |

> Si aumenta la complejidad, puede añadirse documentación y extraerse módulos:

```text
proyecto/
├── README.md
├── main.tf
├── providers.tf
├── variables.tf
├── outputs.tf
└── modules/
    ├── moduleA/
    │   ├── README.md
    │   ├── main.tf
    │   ├── providers.tf
    │   ├── variables.tf
    │   └── outputs.tf
    └── moduleB/
```

> La estructura organiza las definiciones, pero un módulo hijo no se utiliza por aparecer en una carpeta: debe ser invocado desde la configuración correspondiente.

#### 7. Variables de entrada y salida

##### 7.1. Declaración y uso

> Una **input variable** parametriza una configuración. Puede declarar tipo, descripción y valor predeterminado. Su valor se referencia mediante `var.nombre`.

```hcl
variable "openstack_user_name" {
  type        = string
  description = "The username for the Tenant."
  default     = "mtorres"
}

variable "security_groups" {
  type    = list(string)
  default = ["default"]
}
```

> `openstack_user_name` es una cadena y `security_groups` una lista de cadenas. El fragmento de configuración del provider que utiliza la primera variable es:

```hcl
provider "openstack" {
  user_name = var.openstack_user_name
}
```

> Es un fragmento de uso, no una configuración completa de autenticación de OpenStack: los demás parámetros dependen del entorno.

##### 7.2. Asignación en archivos y variables de entorno

> `terraform.tfvars` asigna valores a las variables previamente declaradas. No sustituye sus declaraciones ni elimina las restricciones de tipo.

```hcl
openstack_user_name = "johndoe"
security_groups     = ["default"]
```

> [!warning] Corrección
> En el material aparece `security_groups = "default"`, pero la variable se ha declarado como `list(string)` y el valor correcto es `security_groups = ["default"]`.
> Fuente de comprobación: [OpenTofu: variables de entrada y restricciones de tipo](https://opentofu.org/docs/language/values/variables/)

> En la organización propuesta se excluye `terraform.tfvars` del control de versiones y se publica una plantilla **`terraform.tfvars.example`** sin credenciales reales. Los valores concretos se proporcionan en cada entorno.
>
> Una variable también puede recibirse desde el entorno mediante el prefijo **`TF_VAR_`**, después de declarar la variable de entrada correspondiente:

```hcl
variable "openstack_password" {
  type      = string
  sensitive = true
}
```

> La contraseña no tiene un valor predeterminado en el código. `sensitive` limita su presentación en salidas habituales, pero no impide que información sensible termine en el estado.

```bash
export TF_VAR_openstack_password=your-password
```

> `your-password` es un marcador. Este mecanismo evita escribir la contraseña en el código, pero no garantiza que ningún atributo derivado se guarde en el estado o aparezca en otros lugares. La gestión del estado y del acceso a las credenciales sigue siendo necesaria.

##### 7.3. Outputs y dependencias

> Un **output** expone un resultado del módulo, por ejemplo una dirección IP creada por un recurso. Se puede conservar en `outputs.tf`.

```hcl
output "tf_vm_Floating_IP" {
  value = openstack_networking_floatingip_v2.tf_vm_ip.address

  depends_on = [
    openstack_networking_floatingip_v2.tf_vm_ip
  ]
}
```

> `value` utiliza el atributo `address` de la floating IP. La referencia ya expresa una dependencia; `depends_on` la declara explícitamente. Un output devuelve información de los recursos, no crea otra IP.

#### 8. Instalación y operaciones básicas

> OpenTofu se distribuye como un binario. Para la instalación manual se obtiene la versión y arquitectura adecuadas, se descomprime y se sitúa `tofu` en un directorio accesible mediante **PATH**. Los comandos se ejecutan desde el directorio de la configuración.
>
> El flujo básico es:

```bash
tofu init
tofu plan
tofu apply
```

| Operación | Efecto |
| --- | --- |
| **`tofu init`** | Inicializa la configuración y obtiene providers y componentes necesarios. |
| **`tofu plan`** | Lee la configuración y presenta las operaciones previstas, sin aprovisionar ni modificar los recursos cloud. |
| **`tofu apply`** | Ejecuta cambios para alcanzar el estado deseado y actualiza el estado administrado. |
| **`tofu destroy`** | Elimina los recursos administrados según el plan de destrucción y actualiza sus registros en el estado. |

> El plan permite revisar creaciones, modificaciones y reemplazos antes de aplicar. `apply` puede generar su propio plan y solicitar confirmación; ver un plan anteriormente no garantiza que un `apply` posterior use exactamente aquella misma instantánea.
>
> Cuando se ha decidido eliminar el entorno, la operación correspondiente es:

```bash
tofu destroy
```

> La destrucción afecta a los recursos administrados por esa configuración; no significa borrar todos los recursos del proyecto cloud. Debe distinguirse terminar un ejemplo de borrar recursos utilizados por otras aplicaciones.

#### 9. Archivo de estado y colaboración

> **`terraform.tfstate`** relaciona las direcciones declaradas con los objetos reales y conserva información necesaria para gestionarlos. Permite seguir recursos, calcular cambios y eliminarlos cuando corresponda.
>
> Hay que distinguir **configuración**, **estado guardado** e **infraestructura real**. La configuración expresa lo deseado; el estado conserva lo que la herramienta conoce; los recursos remotos pueden haber cambiado después de la última operación.
>
> El estado puede contener información sensible y se excluye del control de versiones. En un entorno colaborativo se utiliza un **backend** con almacenamiento compartido y soporte de **locking** para impedir operaciones simultáneas incompatibles. El bloqueo del estado no sustituye la coordinación sobre cambios de código o de aplicaciones.

#### 10. Reemplazo de recursos y actualización del estado

> Un recurso puede estar degradado aunque su configuración declarada no haya cambiado. Forzar su reemplazo permite recrearlo sin cambiar artificialmente sus atributos:

```bash
tofu apply -replace="<recurso>.<instancia>"
```

> Los marcadores deben sustituirse por la dirección real, por ejemplo `google_compute_instance.tf-vm`. El plan indicará el reemplazo y sus consecuencias. La operación crea otro objeto: no repara necesariamente el contenido interno de la máquina existente.
>
> Para sincronizar el estado con atributos legibles de los objetos remotos aparece la operación:

```bash
tofu refresh
```

> **Refresh modifica el estado, no la configuración ni los objetos remotos**. El plan y la aplicación ya realizan normalmente lecturas de los recursos mediante el provider. Si un cambio externo es observable por esa API, puede detectarse; un fallo de la aplicación que no se refleja en esos atributos puede requerir una decisión de reemplazo.
>
> `tofu refresh` se conserva como comando heredado, pero está deprecado. La alternativa que permite revisar y confirmar los cambios de estado es:

```bash
tofu apply -refresh-only
```

> Sincronizar el estado no expresa si se quiere conservar un cambio externo o revertirlo: para eso hay que contrastarlo con la configuración deseada. Aceptar información remota en el estado no equivale a editar automáticamente los archivos HCL.


### III. Ejemplo de OpenTofu en Google Cloud

#### 11. Preparación del proyecto y autenticación

> El ejemplo requiere un proyecto de Google Cloud accesible, la API de Compute Engine habilitada, facturación y permisos adecuados para crear los recursos. Utiliza una **service account** con una clave JSON, una red `default` con su subred regional y una clave pública SSH local.
>
> La clave JSON se guarda como **`gcp-identity.json`** en el directorio padre de la configuración. La clave pública debe existir en **`~/.ssh/id_rsa.pub`** antes de evaluar `file()`. Se carga el contenido de la clave pública en los metadatos; la clave privada se conserva para autenticarse por SSH.
>
> Los archivos se organizan así para el ejemplo con inicialización:

```text
entorno/
├── gcp-identity.json
└── proyecto/
    ├── providers.tf
    ├── variables.tf
    ├── main.tf
    ├── outputs.tf
    ├── firewall.tf
    └── setup-docker.sh
```

> Los nombres de proyecto y usuario que aparecen en las variables son valores de ejemplo y deben adaptarse. La cuenta de servicio tiene que estar autorizada para las operaciones; disponer de su JSON no concede permisos que no tenga esa identidad.

##### 11.1. Provider

> **`providers.tf`** fija la versión del provider y configura autenticación, proyecto, región y zona predeterminadas. La restricción `6.5.0` conserva la versión de este ejemplo.

```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.5.0"
    }
  }
}

provider "google" {
  credentials = file("../gcp-identity.json")

  project = var.gcp-project
  region  = "us-central1"
  zone    = "us-central1-c"
}
```

> `source` identifica el provider; `version` limita qué versión se descarga. `credentials` lee el archivo local y las demás propiedades indican el ámbito predeterminado. Un recurso puede declarar una zona propia, que prevalece sobre ese valor por defecto.

##### 11.2. Variables

> **`variables.tf`** declara usuario y proyecto. Se añade la declaración de `gcp-network` necesaria para la variante con disco, que utiliza esa variable.

```hcl
variable "gcp-username" {
  description = "GCP user name"
  default     = "mtorres"
}

variable "gcp-project" {
  description = "GCP project"
  default     = "cc2025-mtorres"
}

variable "gcp-network" {
  type        = string
  description = "Red y subred del ejemplo"
  default     = "default"
}
```

> En esa variante se utiliza el mismo nombre para red y subred. Es una simplificación adecuada si existen esos recursos con ese nombre y en la región correspondiente; no significa que una VPC y sus subredes deban llamarse igual en cualquier diseño.

#### 12. Creación de la VM y salidas

> La primera versión de **`main.tf`** crea una instancia `tf-vm` de tipo `n1-standard-1` en `us-central1-a` con un disco de arranque basado en Debian 11. La zona está indicada explícitamente y no es la zona predeterminada del provider.

```hcl
resource "google_compute_instance" "tf-vm" {
  name         = "tf-vm"
  zone         = "us-central1-a"
  machine_type = "n1-standard-1"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  metadata = {
    ssh-keys = "${var.gcp-username}:${file("~/.ssh/id_rsa.pub")}"
  }

  # El startup script se activa en la variante con Docker.

  network_interface {
    network    = "default"
    subnetwork = "default"

    access_config {}
  }
}
```

> `boot_disk.initialize_params.image` selecciona la imagen de arranque. `metadata.ssh-keys` asocia el usuario con su clave pública. La interfaz utiliza la red y subred `default`; `access_config {}` solicita una configuración de acceso externo con IP efímera.
>
> Las salidas se separan en **`outputs.tf`**. Estas mismas definiciones sirven para las tres variantes porque todas conservan la dirección `google_compute_instance.tf-vm`.

```hcl
output "tf-vm-internal-ip" {
  value = google_compute_instance.tf-vm.network_interface.0.network_ip

  depends_on = [
    google_compute_instance.tf-vm
  ]
}

output "tf-vm-ephemeral-ip" {
  value = google_compute_instance.tf-vm.network_interface.0.access_config.0.nat_ip

  depends_on = [
    google_compute_instance.tf-vm
  ]
}
```

> La primera salida expone la IP interna de la primera interfaz; la segunda, la IP externa de su primera configuración de acceso. Se conservan las dependencias explícitas. Tener una IP externa no garantiza que HTTP o SSH sean accesibles: también importan las reglas de firewall y el servicio que escucha.
>
> Desde el directorio del proyecto, el flujo de evaluación y aplicación es:

```bash
tofu init
tofu plan
tofu apply
```

> Primero se prepara el provider; después se revisan las operaciones y se aplican. La verificación debe contrastar los recursos y las IPs obtenidas con el proyecto, zona y configuración previstos.

#### 13. Variante con disco adicional

> La siguiente configuración **sustituye** a la versión anterior de `main.tf`. Conserva la dirección lógica de la VM, pero cambia la zona a **`us-central1-c`**, el tipo a **`n1-standard-2`** y utiliza `var.gcp-network`. Añade un disco SSD y un recurso de conexión.

```hcl
resource "google_compute_instance" "tf-vm" {
  name         = "tf-vm"
  zone         = "us-central1-c"
  machine_type = "n1-standard-2"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  metadata = {
    ssh-keys = "${var.gcp-username}:${file("~/.ssh/id_rsa.pub")}"
  }

  network_interface {
    network    = var.gcp-network
    subnetwork = var.gcp-network

    access_config {}
  }

  lifecycle {
    ignore_changes = [attached_disk]
  }
}

resource "google_compute_disk" "tf-disk" {
  name = "tf-disk"
  type = "pd-ssd"
  size = 10
}

resource "google_compute_attached_disk" "attached-tf-disk" {
  disk     = google_compute_disk.tf-disk.id
  instance = google_compute_instance.tf-vm.id
}
```

> El disco utiliza la zona predeterminada del provider, `us-central1-c`, que coincide con la de esta VM. El recurso de conexión referencia los identificadores de disco e instancia; esas referencias expresan que ambos deben existir antes de conectarlos.
>
> **Crear, conectar y montar un disco son pasos distintos**. La conexión lo presenta a la VM, pero el ejemplo no incluye formato del sistema de archivos ni montaje dentro del sistema operativo. Tampoco hay un startup script activo en esta variante.

> [!warning] Corrección
> En el material aparece un disco `pd-ssd` con `size = 1`, pero el tamaño mínimo de un Persistent Disk SSD zonal es 10 GiB. La configuración correcta de este ejemplo utiliza `size = 10`.
> Fuente de comprobación: [Google Cloud: tamaños admitidos de Persistent Disk](https://docs.cloud.google.com/compute/docs/disks/add-persistent-disk)

> [!warning] Corrección
> En el material aparece `google_compute_attached_disk` sin excluir la gestión del bloque `attached_disk` en la instancia, pero el provider exige `lifecycle { ignore_changes = [attached_disk] }` para que los dos recursos no compitan por administrar la conexión.
> Fuente de comprobación: [Provider Google 6.5.0: compute_attached_disk](https://github.com/hashicorp/terraform-provider-google/blob/v6.5.0/website/docs/r/compute_attached_disk.html.markdown)

> El plan debe inspeccionarse de nuevo. **La variante no solo añade almacenamiento**: cambiar de zona implica reemplazar la instancia. Los cambios de tipo de máquina también tienen condiciones de operación. No se debe interpretar esta configuración como una ampliación transparente de la VM inicial.
>
> Si se adopta la variante siguiente sin el disco, hay que decidir qué recursos se conservan: eliminar sus declaraciones de la configuración puede producir un plan de destrucción del disco administrado. Las variantes son alternativas didácticas, no archivos que deban cargarse simultáneamente.

#### 14. Inicialización con Docker, Compose y aplicación

##### 14.1. Reglas de firewall

> El ejemplo completo usa Ubuntu 22.04 e instala Docker y su plugin Compose al arrancar. Antes de describir la VM se definen reglas de entrada para HTTP y SSH en **`firewall.tf`**.

```hcl
resource "google_compute_firewall" "allow-http" {
  name    = "tf-fw-allow-http"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["80"]
  }

  target_tags   = ["http"]
  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "allow-ssh" {
  name    = "tf-fw-allow-ssh"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  target_tags   = ["ssh"]
  source_ranges = ["0.0.0.0/0"]
}
```

> Las reglas se aplican a instancias con las tags `http` o `ssh`, respectivamente. `0.0.0.0/0` permite esos orígenes desde cualquier dirección IPv4; el ejemplo no restringe SSH a una red de administración.
>
> La apertura del firewall no instala un servidor ni publica un puerto del contenedor. Para atender HTTP debe existir una aplicación que escuche en el puerto permitido y una publicación de puertos adecuada en su configuración de Compose.

##### 14.2. Instancia con startup script

> Esta tercera variante de **`main.tf`** mantiene `tf-vm` en `us-central1-a` con tipo `n1-standard-1`, cambia la imagen a **Ubuntu 22.04 LTS**, añade las tags y carga el contenido de `setup-docker.sh`.

```hcl
resource "google_compute_instance" "tf-vm" {
  name         = "tf-vm"
  zone         = "us-central1-a"
  machine_type = "n1-standard-1"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
    }
  }

  metadata = {
    ssh-keys = "${var.gcp-username}:${file("~/.ssh/id_rsa.pub")}"
  }

  tags = ["ssh", "http"]

  metadata_startup_script = file("setup-docker.sh")

  network_interface {
    network    = "default"
    subnetwork = "default"

    access_config {}
  }
}
```

> **`metadata_startup_script` contiene el script**, no solo su ruta: `file()` lo lee antes de la operación de OpenTofu. Debe guardarse con el nombre `setup-docker.sh` en el directorio del proyecto, aunque se haya descargado con otro nombre.
>
> Se reutilizan provider, variables y outputs. No se mezclan varias declaraciones de `google_compute_instance.tf-vm` en el mismo módulo. La creación de la VM puede finalizar antes de que la aplicación haya completado su instalación, por lo que hay que verificar ambos resultados.

##### 14.3. Script de instalación: repositorio y dependencias

> El script se ejecuta como inicialización de una VM Ubuntu y necesita acceso a los repositorios de paquetes, Docker y GitHub. Se añade **Git** a la preparación porque se utiliza después para clonar la aplicación. Este primer bloque es el comienzo de `setup-docker.sh`:

```bash
#!/bin/bash

echo "Instalando Docker"

apt-get update
apt-get install -y ca-certificates curl git
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update
```

> Se actualiza el índice, se instalan herramientas y se prepara el keyring para comprobar la firma del repositorio. `dpkg --print-architecture` determina la arquitectura y `VERSION_CODENAME` la versión de Ubuntu. Después de añadir el repositorio se actualiza otra vez el índice para incorporar sus paquetes.
>
> La URL y el repositorio son los de **Ubuntu**: este script no debe trasladarse sin adaptación al ejemplo anterior con Debian.

##### 14.4. Docker, Compose y despliegue

> El siguiente bloque continúa el mismo script. Instala el motor, CLI, containerd y los plugins Buildx y Compose; habilita Docker y despliega la aplicación.

```bash
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
systemctl enable docker

git clone https://github.com/ualmtorres/docker_customer_catalog.git
cd docker_customer_catalog
docker compose up -d

exit 0
```

> `systemctl enable docker` habilita el arranque del servicio en futuros inicios. En una instalación habitual de Docker sobre Ubuntu, el paquete inicia el servicio; si no está activo, debe arrancarse antes de ejecutar Compose.
>
> `git clone` obtiene el proyecto y `docker compose up -d` utiliza su definición para crear e iniciar la aplicación en segundo plano. El ejemplo descarga ese proyecto para el despliegue, pero sus archivos internos y puertos deben verificarse en el propio entorno.
>
> El script no incluye un criterio de parada ante todos los fallos ni lógica para reutilizar un directorio ya clonado. **El éxito de OpenTofu o el `exit 0` final no demuestran por sí solos que la aplicación esté operativa**. Los logs de inicialización y el estado de los contenedores deben inspeccionarse; la idempotencia declarativa de OpenTofu no corrige automáticamente esas propiedades del script.

### IV. Ansible y gestión de configuraciones

#### 15. Arquitectura y ciclo de trabajo

> **Ansible** automatiza la gestión de configuraciones, la orquestación y el despliegue de aplicaciones. Expresa las tareas en archivos **YAML**, llamados *playbooks*, y dispone de módulos que implementan operaciones concretas.
>
> Su arquitectura es **sin agentes**: para administrar servidores Linux suele conectarse por SSH, sin instalar un servicio permanente de Ansible en cada nodo. Desde un nodo de control se pueden gestionar cientos de máquinas, tanto locales (*on-premises*) como en la nube. Los módulos permiten trabajar también con APIs de proveedores, como ocurre en el ejemplo de creación de una VM en GCP.
>
> El ciclo de trabajo consta de tres elementos:

| Elemento | Función |
| --- | --- |
| **Inventario** | Identificar los nodos y grupos sobre los que se actuará, junto con sus datos de conexión. |
| **Playbook** | Definir los grupos destinatarios y las tareas, los módulos y sus parámetros. |
| **Ejecución** | Aplicar la configuración o desplegar la aplicación y revisar el resultado de cada tarea. |

![[apuntes-4d98735752f7-p0033-63af89334c30.png]]

> Administradores, equipos de pruebas y responsables de entrega pueden utilizar el mismo mecanismo de automatización. Los playbooks coordinan módulos y plantillas para crear y aprovisionar recursos, distribuir configuraciones, aplicar ajustes de seguridad y desplegar aplicaciones sobre el conjunto de máquinas del inventario.
>
> Un **módulo** realiza una operación; una **plantilla** permite generar un archivo de configuración a partir de variables; el **playbook** organiza las tareas. La modularidad evita tener que escribir de nuevo toda la lógica de cada operación.

#### 16. Complementariedad con OpenTofu

> OpenTofu y Ansible cubren necesidades que pueden combinarse en un mismo entorno. La división habitual consiste en aprovisionar la infraestructura con OpenTofu y configurar su software con Ansible.

| Aspecto | OpenTofu | Ansible |
| --- | --- | --- |
| Enfoque principal | Infraestructura y su estado deseado. | Configuración, orquestación y despliegue de software. |
| Unidad de trabajo | Recursos y módulos declarados en HCL. | Tareas de módulos organizadas en playbooks YAML. |
| Ejemplo en GCP | Crear la VM, discos y reglas de firewall. | Instalar y configurar las aplicaciones dentro del servidor. |
| Mecanismo habitual | APIs del proveedor y archivo de estado. | Conexiones sin agentes, como SSH, o llamadas a APIs mediante módulos. |

> **Un flujo integrado** comienza con la creación de la VM por OpenTofu. Sus datos, como la dirección IP, permiten identificar el servidor que Ansible debe gestionar; después, el playbook configura las aplicaciones requeridas. La automatización conjunta cubre la infraestructura y el entorno de ejecución.
>
> Esta división describe el uso habitual, pero Ansible también dispone de módulos de aprovisionamiento. El ejemplo siguiente utiliza precisamente uno de ellos para crear una VM mediante la API de Compute Engine. En un entorno combinado conviene definir qué herramienta administra cada recurso, evitando que dos automatizaciones impongan configuraciones incompatibles sobre él.

#### 17. Ejemplo de creación de una VM en GCP con Ansible

##### 17.1. Preparación

> Se necesita una cuenta activa de Google Cloud, un proyecto con Compute Engine habilitado y una cuenta de servicio con permisos adecuados. Se prepara también el SDK de GCP para las operaciones del entorno y una **clave JSON** de la cuenta de servicio para la autenticación del playbook.
>
> En el equipo de control deben estar instalados Python, Ansible y la colección `google.cloud`. Las dependencias del entorno incluyen `google-auth` y `google-api-python-client`; el módulo empleado requiere además `requests`. Una preparación posible en un entorno virtual es:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install ansible google-auth google-api-python-client requests
ansible-galaxy collection install google.cloud
```

> Los paquetes se instalan en el intérprete que ejecutará el módulo. El siguiente inventario, guardado como `inventory.yml`, explicita que las tareas de este ejemplo se ejecutan **localmente en el nodo de control**:

```yaml
all:
  hosts:
    localhost:
      ansible_connection: local
      ansible_python_interpreter: "{{ ansible_playbook_python }}"
```

> Aquí `localhost` no representa la VM que se creará: representa el equipo desde el que se llama a la API de Google Cloud. Por ello, la creación de la instancia no necesita una conexión SSH previa a una máquina que todavía no existe. Un playbook posterior que configurase su sistema operativo sí necesitaría identificar y alcanzar esa VM.

##### 17.2. Playbook

> El archivo `playbook_gce.yml` declara una instancia llamada `mi-instancia`, de tipo `e2-micro`, en `us-central1-a`. El disco de arranque se inicializa desde una imagen de Debian; la interfaz utiliza la red `default` del proyecto y solicita una IP externa mediante NAT.
>
> `path/to/key.json` y `mi-proyecto` son valores de ejemplo que deben sustituirse. El identificador del proyecto aparece tanto en `project` como en la referencia a la red; ambos deben corresponder al mismo entorno. Se utiliza la ruta completa de la familia de imágenes `debian-11`.

```yaml
- name: Crear instancia en GCE
  hosts: localhost
  connection: local
  gather_facts: false

  tasks:
    - name: Crear VM en GCP
      google.cloud.gcp_compute_instance:
        auth_kind: serviceaccount
        service_account_file: "path/to/key.json"
        project: "mi-proyecto"
        zone: "us-central1-a"
        name: "mi-instancia"
        machine_type: "e2-micro"
        state: present

        disks:
          - auto_delete: true
            boot: true
            initialize_params:
              source_image: "projects/debian-cloud/global/images/family/debian-11"

        network_interfaces:
          - network:
              selfLink: "https://www.googleapis.com/compute/v1/projects/mi-proyecto/global/networks/default"
            access_configs:
              - name: "External NAT"
                type: "ONE_TO_ONE_NAT"
```

> [!warning] Corrección
> En el material aparece `google.cloud.gce_instance` y `network: "default"`, pero el módulo correcto es `google.cloud.gcp_compute_instance` y su parámetro `network` requiere un diccionario de referencia, como el que contiene `selfLink`.
> Fuente de comprobación: [Módulo gcp_compute_instance de Ansible](https://docs.ansible.com/projects/ansible/latest/collections/google/cloud/gcp_compute_instance_module.html)

> `auth_kind: serviceaccount` selecciona el tipo de autenticación y `service_account_file` indica la clave. `state: present` expresa que la instancia debe existir. En el disco, `boot: true` lo identifica como disco de arranque y `auto_delete: true` hace que se elimine cuando se borre la VM.
>
> `connection: local` fija la ejecución local y `gather_facts: false` evita recopilar información del sistema de control innecesaria para esta tarea. El playbook solicita la VM a GCP; no instala aplicaciones dentro de ella ni incorpora las reglas de firewall del ejemplo anterior.

##### 17.3. Ejecución y validación

> El comando básico para ejecutar el archivo es:

```bash
ansible-playbook playbook_gce.yml
```

> Para utilizar explícitamente el inventario preparado:

```bash
ansible-playbook -i inventory.yml playbook_gce.yml
```

> Tras la ejecución, se comprueba en la consola de Google Cloud que la instancia pertenece al proyecto y zona previstos, que utiliza el tipo de máquina y disco indicados y que dispone de la interfaz configurada. También se revisan los mensajes de Ansible y los logs para detectar errores de autenticación, permisos o creación.
>
> **La creación de la VM y la configuración de una aplicación son etapas diferentes**. Que la VM exista no demuestra que haya software desplegado ni que un servicio sea accesible: eso requiere las tareas de configuración y las comprobaciones correspondientes.

#### 18. Organización y buenas prácticas de Ansible

> Las **claves de servicio** deben mantenerse seguras y separadas de los archivos que se comparten. La automatización necesita acceso a las credenciales para autenticarse, pero el playbook puede conservar únicamente la referencia al archivo.
>
> Cuando aumenta la complejidad, los **roles** permiten agrupar tareas, variables y plantillas para reutilizar configuraciones. La documentación debe explicar el inventario, los parámetros y las configuraciones utilizadas, de forma que otro miembro del equipo pueda reproducir el procedimiento.
>
> La integración con **CI/CD** permite ejecutar la automatización de forma sistemática al introducir cambios. Junto con la revisión del código, la validación del resultado y una asignación clara de responsabilidades entre OpenTofu y Ansible, facilita mantener entornos coherentes.

### V. Resumen Final

> **IaaS** proporciona recursos de infraestructura; **IaC** expresa su creación y gestión mediante código. Versionar y revisar ese código aporta reproducibilidad, consistencia y trazabilidad, y facilita la automatización de entornos.
>
> **OpenTofu** utiliza providers, recursos, variables, outputs y módulos para describir el estado deseado. Su ciclo esencial es `init → plan → apply`; `destroy` elimina los recursos gestionados. El plan se interpreta antes de aplicar y el archivo de estado permite relacionar la configuración con los recursos existentes, por lo que debe protegerse y coordinarse en el trabajo en equipo.
>
> En **Google Cloud**, la autenticación de la cuenta de servicio permite gestionar VMs, discos y reglas de firewall. Las variantes desarrollan una VM básica, la conexión de un disco adicional y una VM Ubuntu inicializada con Docker y Compose. Aprovisionar, conectar un disco, inicializar el sistema y desplegar una aplicación son operaciones distintas y requieren comprobaciones específicas.
>
> **Ansible** organiza la automatización en inventarios y playbooks YAML, empleando módulos sin agentes permanentes en los nodos. Puede configurar software y también aprovisionar recursos a través de APIs, como la VM de Compute Engine del ejemplo.
>
> La combinación habitual consiste en **crear la infraestructura con OpenTofu y configurar las aplicaciones con Ansible**. Credenciales protegidas, código modular, documentación, revisión de cambios, integración con CI/CD y validación del resultado sostienen el mantenimiento de todo el entorno.



