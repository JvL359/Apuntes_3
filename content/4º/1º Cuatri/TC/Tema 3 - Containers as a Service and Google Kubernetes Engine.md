---
estado: pendiente de revisión
---

### I. Microservices

#### 1. Definition and Characteristics

> La arquitectura de **microservices** estructura una aplicación como un conjunto de servicios pequeños, autónomos y desplegables de forma independiente, que se comunican a través de la red. La descomposición se realiza por **funcionalidad**: cada servicio implementa una responsabilidad concreta.
>
> Sus características principales son componentes de grano fino, autonomía y comunicación entre procesos. Los servicios pueden desarrollarse, desplegarse, actualizarse y escalarse por separado. Esto permite adaptar la capacidad de una parte de la aplicación sin replicar necesariamente toda la aplicación.
>
> La independencia de despliegue no elimina las dependencias funcionales: un servicio puede necesitar que otro esté disponible para completar una petición. La comunicación distribuida introduce problemas de latencia, descubrimiento de servicios y gestión de fallos.

#### 2. Scalability and Benefits

> El modelo de escalabilidad distingue tres dimensiones:
>
> - **X-axis: horizontal duplication**. Se crean copias de la aplicación para repartir la carga.
> - **Y-axis: functional decomposition**. Se separan funciones en servicios y se escala cada una según su demanda.
> - **Z-axis: data partitioning**. Se divide el trabajo o los datos entre particiones que realizan una misma clase de tarea.
>
> La figura compara X e Y. Arriba, cada copia contiene las mismas funciones; abajo, la cantidad de instancias de cada función puede ser diferente.

![[apuntes-752457319883-p0006-3893c9d1acc3.png]]

> Los beneficios son **scalability**, flexibilidad tecnológica, facilidad de construcción y mantenimiento, desarrollo y despliegue más rápidos, **fault isolation** y **resiliency**. El aislamiento facilita contener un fallo en un componente, siempre que las dependencias también se diseñen para tolerarlo.
>
> La flexibilidad reduce la dependencia de una única pila tecnológica y puede ayudar a evitar vendor lock-in; no garantiza por sí sola independencia de cualquier proveedor o API.

### II. Containers

#### 3. Container, Image and Runtime

> Un **container** es una instancia aislada de ejecución de una aplicación, definida por su sistema de archivos, configuración y metadatos. Una **container image** es el paquete que proporciona el código, runtime, herramientas, bibliotecas y configuración necesarios. **La imagen se convierte en un contenedor al ejecutarse**.
>
> Los contenedores utilizan virtualización a nivel del sistema operativo. No incorporan hardware virtual ni un kernel invitado completo: comparten el kernel del host, con mecanismos de aislamiento. Por eso suelen ser más ligeros que las VMs.
>
> El **container runtime** obtiene imágenes de un registry, crea y ejecuta los contenedores y administra su ciclo de vida. En este ecosistema aparecen Docker, Podman, CRI-O y containerd, con funciones y capas de integración diferentes.
>
> El empaquetado reduce las diferencias entre el entorno de desarrollo y el de operación. La portabilidad sigue dependiendo de la compatibilidad del sistema y la arquitectura de ejecución.

#### 4. VMs and Containers

> Una **VM** incluye aplicaciones, bibliotecas y un sistema operativo invitado sobre un hypervisor. Un **container** incluye la aplicación y sus dependencias sobre el runtime y el sistema operativo del host. La figura muestra dónde se sitúa el aislamiento en cada caso.

![[apuntes-752457319883-p0010-e2749a403d45.png]]

| Aspecto | VM | Container |
| --- | --- | --- |
| Entorno propio | Sistema operativo invitado, además de la aplicación. | Procesos y dependencias, compartiendo el kernel del host. |
| Capa de ejecución | Hypervisor. | Container runtime. |
| Sobrecarga | Mayor por mantener un entorno de máquina y un SO invitado. | Menor al evitar un kernel invitado por contenedor. |
| Uso conjunto | Puede alojar varios contenedores. | Puede ejecutarse dentro de una VM. |

> Ambos mecanismos pueden combinarse: los nodos de un clúster cloud suelen ser VMs que ejecutan contenedores.

#### 5. Build, Ship and Run

> El flujo de Docker separa tres operaciones:
>
> 1. **Build**: un Dockerfile describe cómo construir la imagen.
> 2. **Ship**: la imagen se publica mediante push en un registry, como Docker Hub; otro entorno la obtiene mediante pull.
> 3. **Run**: el runtime crea un contenedor a partir de la imagen.
>
> El **Dockerfile** utiliza instrucciones como `FROM` para seleccionar una imagen base, `COPY` para incorporar archivos, `RUN` para ejecutar operaciones durante la construcción y `CMD` para indicar el comando por defecto al iniciar el contenedor.
>
> El esquema usa `ubuntu:18.04` como base, copia la aplicación bajo `/app`, incluye un paso de construcción con `make` y un comando Python. Las funciones de esas instrucciones se conservan en este fragmento; la aplicación, su fichero de construcción y las herramientas deben existir para completarlo.

```dockerfile
FROM ubuntu:18.04
COPY . /app
RUN make /app
CMD python /app/app.y
```

> `RUN` se ejecuta al construir la imagen; `CMD` al iniciar el contenedor. La ruta `/app` de `make` es un argumento del esquema: su significado depende del fichero de construcción. El nombre `app.y` es la ruta del programa representado, no una extensión obligatoria de Python. Este esquema necesita que `make` y `python` estén instalados y que el proyecto proporcione esos archivos; no define una aplicación completa.

> [!warning] Corrección
> En el material aparecen `COPY ./app`, `RUN make/app` y `CMD python/app/app.y`, pero la sintaxis requiere separar origen y destino en `COPY . /app` y separar el ejecutable de sus argumentos en `RUN make /app` y `CMD python /app/app.y`.
> Fuente de comprobación: [Docker: referencia de Dockerfile](https://docs.docker.com/reference/dockerfile/)

> La imagen está formada por **capas de solo lectura**. Al crear un contenedor se añade una capa **read/write** propia. Los cambios de esa capa no modifican la imagen base; para conservar datos más allá de la vida del contenedor hacen falta mecanismos de almacenamiento adecuados.
>
> Los beneficios de los contenedores son consistencia, predictibilidad, estabilidad, agilidad, eficiencia de recursos, portabilidad y facilidad de gestión. Contribuyen tanto al desarrollo ágil como a la eficiencia operativa.

### III. Container Orchestration and Kubernetes Architecture

#### 6. Why Orchestration Is Needed

> Microservicios y contenedores facilitan construir y empaquetar aplicaciones, pero operar muchos componentes mantiene varios desafíos: despliegues complejos y propensos a errores, dependencia de infraestructura, actualizaciones, recuperación ante fallos, service discovery, escalado automático, configuración y secretos, balanceo de tráfico, administración centralizada y almacenamiento.
>
> **DevOps** aporta prácticas de automatización y colaboración orientadas a agilidad, predictibilidad y fiabilidad. La **container orchestration** proporciona mecanismos para gestionar el ciclo de vida de los contenedores en entornos grandes y dinámicos.
>
> **Kubernetes (K8s)** es una plataforma open source de orquestación que automatiza despliegue, escalado horizontal, comunicación interna y externa, balanceo, descubrimiento, monitorización de salud, actualizaciones, asignación de recursos y gestión de almacenamiento. Las actualizaciones sin interrupción requieren réplicas, capacidad y comprobaciones de disponibilidad apropiadas; no son una consecuencia automática de usar Kubernetes.

#### 7. Control Plane and Worker Nodes

> El clúster distingue **control plane**, que administra el sistema y responde a eventos, y **worker nodes**, que ejecutan las cargas de usuario. El nodo de control de la figura representa los componentes de gestión; una instalación con alta disponibilidad puede distribuirlos entre varias máquinas.

![[apuntes-752457319883-p0018-20f5a1b90373.png]]

| Componente | Responsabilidad |
| --- | --- |
| **API server**, representado como API GW | Punto de acceso para consultar y modificar recursos del clúster. |
| **etcd** | Almacén del estado y configuración del clúster. |
| **Controller manager** | Ejecuta controladores que reconcilian el estado observado con el deseado. |
| **Scheduler** | Decide en qué nodo se asigna un Pod pendiente, considerando recursos y restricciones. |
| **Cloud controller manager** | Integración opcional con APIs y recursos del proveedor cloud. |
| **kubelet** | Agente de cada nodo que coordina la ejecución de los Pods asignados. |
| **Container runtime / engine** | Ejecuta los contenedores del nodo. |
| **kube-proxy** | Implementa funciones de red de Services en la arquitectura representada. |

> Un **controller** actúa para acercar el sistema al estado declarado. Si se solicitan tres réplicas y falta una, el controlador promueve su creación. El scheduler elige el nodo y el kubelet coordina la ejecución allí. Declarar el estado deseado permite que el sistema reaccione sin que el usuario gestione manualmente cada contenedor.

#### 8. APIs, Interfaces and Resource Manifests

> Las APIs permiten actuar sobre **resources**. Los desarrolladores describen cargas; los administradores gestionan el clúster y su integración con infraestructura. Tres interfaces separan Kubernetes de implementaciones concretas:

| Interfaz | Función |
| --- | --- |
| **CRI — Container Runtime Interface** | Integración con la ejecución de contenedores. |
| **CNI — Container Network Interface** | Integración con plugins de red. |
| **CSI — Container Storage Interface** | Integración con drivers de almacenamiento. |

> Se puede interactuar mediante `kubectl`, una interfaz gráfica o un cliente REST: las peticiones llegan al API server. Un manifiesto YAML describe la versión de la API, el tipo de recurso, sus metadatos y su especificación. Por ejemplo, el archivo `pod.yaml` puede contener:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
    - name: nginx
      image: nginx
```

> `apiVersion` selecciona el esquema; `kind` identifica el recurso; `metadata.name` su nombre; `spec` declara el estado deseado. Para aplicar el manifiesto necesitamos `kubectl` instalado, acceso al clúster configurado mediante kubeconfig y permisos para esa operación.

```bash
kubectl apply -f pod.yaml
```

> `apply` crea o actualiza el recurso declarado; no significa que la aplicación ya haya quedado lista para atender peticiones. Primero deben completarse la planificación, descarga y ejecución.

#### 9. Kubectl Syntax and Operations

> La estructura general es `kubectl [command] [TYPE] [NAME] [flags]`: operación, tipo, nombre y opciones. Un ejemplo de consulta con salida ampliada es:

```bash
kubectl get pods my-pod -o wide
```

> [!warning] Corrección
> En el material aparece `--o=wide` y hay guiones tipográficos en algunas opciones, pero la sintaxis correcta de salida es `-o wide` o `--output=wide`; las opciones de archivo y selector utilizan `-f` y `-l` con guiones ASCII.
> Fuente de comprobación: [Kubernetes: referencia de kubectl](https://kubernetes.io/docs/reference/kubectl/)

> Los comandos de inspección permiten ver recursos, detalles, manifiestos y logs. Los nombres entre `< >` son marcadores y deben sustituirse.

```bash
kubectl get pods
kubectl describe pod <pod-name>
kubectl get pod <pod-name> -o yaml
kubectl logs <pod-name>
kubectl port-forward <pod-name> <local-port>:<cont-port>
```

> `describe` muestra detalles y eventos; `-o yaml` representa el recurso; `logs` consulta los logs de un contenedor. `port-forward` abre un acceso desde un puerto local hacia el puerto indicado del Pod. En un Pod con varios contenedores puede ser necesario seleccionar uno para consultar sus logs.
>
> Las operaciones de eliminación y edición tienen efectos diferentes:

```bash
kubectl delete pod <pod-name>
kubectl delete pods -l key=value
kubectl delete pods --all
kubectl apply -f <manifest-file>
kubectl replace -f <manifest-file>
kubectl edit <type> <name>
```

> `delete` elimina los recursos seleccionados del namespace utilizado; `--all` selecciona todos los Pods de ese ámbito. `replace` sustituye la representación de un recurso existente, mientras que `edit` permite modificarlo interactivamente. Si un controlador mantiene réplicas, eliminar uno de sus Pods puede provocar la creación de un reemplazo.

### IV. Pods and Resource Organization

#### 10. Kubernetes Namespaces

> Un **Namespace** organiza recursos y proporciona un ámbito para sus nombres. Permite separar tenants, entornos como dev/test/prod o conjuntos de servicios. En ese ámbito se pueden aplicar RBAC, cuotas y reglas de red, con los mecanismos correspondientes.
>
> Crear un Namespace no impone automáticamente aislamiento de red ni seguridad completa entre tenants. El aislamiento efectivo depende de las políticas y de su implementación.

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: my-ns
---
apiVersion: v1
kind: Pod
metadata:
  name: web-fe
  namespace: my-ns
spec:
  containers:
    - image: nginx:alpine
      name: web-server
```

> Primero debe existir `my-ns`. `metadata.namespace` sitúa el Pod en ese ámbito; si se omite, se utiliza el namespace de la petición, normalmente el del contexto de `kubectl`.

#### 11. Pods and Shared Linux Namespaces

> Un **Pod** es la unidad mínima desplegable de Kubernetes. Agrupa uno o varios contenedores colocados en el mismo nodo y que comparten parte de su contexto de ejecución.
>
> Si dos procesos P1 y P2 están estrechamente acoplados —necesitan proximidad, comunicación frecuente y el mismo escalado—, pueden ejecutarse en contenedores separados **dentro de un mismo Pod**. Así se mantiene la separación entre aplicaciones sin tratarlas como unidades de planificación independientes.
>
> Los **Linux namespaces** son mecanismos de aislamiento del sistema operativo y no deben confundirse con el recurso **Namespace de Kubernetes**. La figura muestra que, en la configuración representada, los contenedores de un Pod comparten hostname, IPC y red, mientras mantienen otros ámbitos separados.

![[apuntes-752457319883-p0025-d9715afdb70e.png]]

> Compartir red implica una misma IP y espacio de puertos; los contenedores pueden comunicarse mediante `localhost` y deben evitar conflictos de escucha. El aislamiento de procesos y otros namespaces depende de la configuración; no se debe inferir que todos los namespaces Linux se comparten siempre.

#### 12. Labels and Selectors

> Las **labels** son pares clave-valor asociados a recursos. Un recurso puede tener varias etiquetas con claves diferentes. Los **selectors** permiten identificar conjuntos de recursos por esas etiquetas, por ejemplo para Services y ReplicaSets o para restricciones de planificación.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-fe
  labels:
    app: my-app
    env: prod
spec:
  restartPolicy: Always
  containers:
    - image: nginx:alpine
      name: web-server
```

> El Pod combina las etiquetas de aplicación y entorno. Las consultas y eliminaciones pueden filtrarse por ellas:

```bash
kubectl get pods -l app=my-app
kubectl delete pods -l env=test
```

> El nombre individual identifica un objeto; una etiqueta permite relacionar varios objetos aunque sus nombres sean diferentes.

#### 13. Requests, Limits and Namespace Constraints

> **Requests** declara los recursos necesarios para planificar el contenedor; **limits** restringe su consumo. El scheduler considera los requests para decidir si el Pod cabe en un nodo. Tener capacidad libre observada no sustituye la comprobación de recursos solicitados.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-fe
spec:
  containers:
    - image: nginx:alpine
      name: web-server
      resources:
        requests:
          cpu: "500m"
          memory: "20Mi"
        limits:
          cpu: "1000m"
          memory: "40Mi"
```

> CPU se expresa en cores o millicores: `500m` equivale a medio core y `1000m` a uno. Memoria suele expresarse en mebibytes (`Mi`) o gibibytes (`Gi`). La configuración solicita medio core y 20 Mi de memoria, con límites de un core y 40 Mi.
>
> El límite de CPU puede provocar throttling; superar el de memoria puede provocar la terminación por falta de memoria. Estos valores ilustran la sintaxis, no el dimensionamiento recomendado de Nginx.
>
> **LimitRange** permite establecer valores predeterminados y restricciones por contenedor o Pod dentro de un namespace. **ResourceQuota** limita el total de recursos consumibles por ese namespace. Son restricciones de escala diferente.

#### 14. Restart Policy and Pod Lifecycle

| `restartPolicy` | Comportamiento |
| --- | --- |
| `Always` | Reinicia un contenedor que termina, tanto con éxito como con error. |
| `OnFailure` | Reinicia si termina con código distinto de cero. |
| `Never` | No reinicia el contenedor terminado. |

> La política se declara en `spec.restartPolicy` del Pod, como en el ejemplo anterior. Reiniciar un contenedor dentro de un Pod no equivale a crear un Pod nuevo en otro nodo.

| Fase | Interpretación |
| --- | --- |
| **Pending** | El clúster ha aceptado el Pod, pero faltan pasos como asignarlo a un nodo o descargar imágenes. |
| **Running** | Está asignado a un nodo, sus contenedores se han creado y al menos uno está ejecutándose, arrancando o reiniciándose. |
| **Succeeded** | Todos terminaron con éxito y no se reiniciarán. |
| **Failed** | Todos terminaron y al menos uno falló, sin estar previsto su reinicio automático. |
| **Unknown** | No se puede obtener su estado, normalmente por problemas de comunicación con el nodo. |

> **Running no significa Ready**. La fase describe el ciclo de vida; la disponibilidad para recibir tráfico depende de otras condiciones, entre ellas las readiness probes.

#### 15. Liveness and Readiness Probes

##### 15.1. Purpose and Parameters

> Una **liveness probe** comprueba si un contenedor sigue funcionando; un fallo persistente puede hacer que Kubernetes lo reinicie según su política. Una **readiness probe** comprueba si puede atender peticiones. Un fallo de readiness retira su disponibilidad como backend, pero no implica reiniciarlo.
>
> Los mecanismos desarrollados son **HTTP GET**, que espera una respuesta 2xx o 3xx; **TCP socket**, que comprueba la conexión; y **exec**, que ejecuta una comprobación dentro del contenedor. Las pruebas se definen a nivel de contenedor. Para que un Pod esté Ready, sus contenedores deben estar listos y deben cumplirse las demás condiciones de readiness aplicables.

| Parámetro | Función |
| --- | --- |
| `periodSeconds` | Intervalo entre comprobaciones. |
| `initialDelaySeconds` | Espera inicial antes de empezar las pruebas. |
| `timeoutSeconds` | Tiempo máximo para una comprobación. |
| `successThreshold` | Éxitos consecutivos necesarios tras un fallo; en liveness debe ser 1. |
| `failureThreshold` | Fallos consecutivos necesarios para considerar fallida la prueba. |

##### 15.2. Probe Manifests

> El ejemplo comprueba `/` por HTTP. Para usar literalmente el puerto **8080**, Nginx debe estar configurado para escuchar en él; la imagen estándar escucha habitualmente en 80. En un despliegue sin esa configuración deben ajustarse la prueba y el targetPort del Service al puerto real. Declarar un puerto en Kubernetes no reconfigura el servidor.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-fe
spec:
  containers:
    - image: nginx:alpine
      name: web-server
      livenessProbe:
        periodSeconds: 1
        initialDelaySeconds: 20
        timeoutSeconds: 1
        successThreshold: 1
        failureThreshold: 3
        httpGet:
          path: /
          port: 8080
```

> Tras una espera inicial de 20 segundos, se comprueba cada segundo, con timeout de un segundo y umbral de tres fallos consecutivos. La configuración de readiness utiliza los mismos parámetros, pero produce un efecto diferente:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-fe
  labels:
    type: web
spec:
  containers:
    - image: nginx:alpine
      name: web-server
      readinessProbe:
        periodSeconds: 1
        initialDelaySeconds: 20
        timeoutSeconds: 1
        successThreshold: 1
        failureThreshold: 3
        httpGet:
          path: /
          port: 8080
```

> [!warning] Corrección
> En el material aparecen `metadata.label` y, en el Deployment, `readynessProbe`, pero los campos correctos son `metadata.labels` y `readinessProbe`.
> Fuente de comprobación: [Kubernetes: configuración de probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) y [labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)

> Una prueba debe medir la condición que representa. Reiniciar un proceso por una dependencia temporalmente no disponible puede empeorar el fallo; una readiness probe puede retirar el tráfico mientras el proceso se recupera.


### V. Networking and Service Discovery

#### 16. Kubernetes Network Model

> Cada Pod obtiene una IP. El modelo establece comunicación entre Pods de distintos nodos sin NAT entre ellos, y comunicación de los agentes de un nodo con los Pods alojados allí, dentro de las restricciones de red aplicables.
>
> Los plugins **CNI** configuran la red, asignan direcciones y establecen rutas. En este ámbito aparecen soluciones como **Calico** y **Flannel**; **kubenet** representa un mecanismo básico de networking de Kubernetes. La funcionalidad concreta depende de la implementación.
>
> Tres problemas motivan los Services: **los Pods son efímeros**, los clientes necesitan descubrir el servicio y una misma función puede estar disponible en varios Pods. Conectarse a una IP de Pod concreta no proporciona por sí solo una dirección estable para la aplicación.

#### 17. Services

##### 17.1. ClusterIP

> **ClusterIP** es el tipo de Service predeterminado. Proporciona una IP y un puerto internos para acceder a un conjunto de Pods. No publica por sí mismo un endpoint hacia clientes externos.
>
> El selector relaciona el Service con los Pods. La representación **Endpoints** recoge sus direcciones y puertos; en implementaciones actuales también se utilizan **EndpointSlices**. La arquitectura de kube-proxy mantiene las reglas que dirigen el tráfico del Service a los backends.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: ClusterIP
  selector:
    app: my-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

> `port: 80` es el puerto del Service; `targetPort: 8080` es el del backend. Los Pods deben tener `app: my-app` y el servidor debe escuchar en 8080. Las labels del Pod de readiness con `type: web` no coinciden con este selector: son ejemplos distintos y hay que utilizar etiquetas coherentes si se combinan.
>
> En **iptables mode**, kube-proxy programa reglas iptables; en **IPVS mode**, utiliza el balanceo IPVS, con características diferentes de rendimiento y gestión. Son modalidades de la arquitectura desarrollada, no una lista exhaustiva de todas las implementaciones actuales.

##### 17.2. NodePort and LoadBalancer

> **NodePort** expone el Service mediante un puerto de los nodos. Un cliente utiliza una IP accesible del nodo y ese puerto, siempre que la conectividad y las reglas de red lo permitan.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mysvc
spec:
  type: NodePort
  ports:
    - port: 80
      targetPort: 8080
      nodePort: 30100
  selector:
    type: web
```

> Aquí el acceso usa `<node-ip>:30100`, el Service tiene puerto 80 y el backend recibe en 8080. **LoadBalancer** solicita una integración de balanceo externo al proveedor correspondiente:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mysvc
spec:
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: 8080
  selector:
    type: web
```

> Son alternativas para `mysvc`, no dos Services independientes con el mismo nombre. LoadBalancer requiere que el entorno disponga de una implementación que proporcione ese balanceador. En el diseño de la figura, el cliente pasa por un balanceador antes de llegar a los nodos.

![[apuntes-752457319883-p0037-7f291af94f1c.png]]

> El dibujo utiliza **31000** como puerto ilustrativo de nodo; el manifiesto NodePort utiliza **30100**. Ambos son valores posibles, pero para ese manifiesto el cliente debe utilizar 30100. En el ejemplo LoadBalancer no se fija explícitamente `nodePort`.

#### 18. Ingress

> **Ingress** representa reglas de entrada HTTP/HTTPS de nivel 7, por nombre de host y ruta, hacia Services. Permite centralizar la configuración, incluidos aspectos de TLS y virtual hosts. Necesita un **Ingress controller** que implemente las reglas.
>
> El ejemplo enruta `example.com/hello` a `mysvc1:80` y `example.com/video` a `mysvc2:80`. Los Services deben existir y el nombre debe resolver hacia el punto de entrada adecuado. La ruta `/blog` del dibujo ilustra otra posible ruta, pero no tiene una regla definida en este manifiesto.
>
> La forma heredada usa `extensions/v1beta1` con `serviceName` y `servicePort`. Esa API fue válida en versiones anteriores. La siguiente representación conserva las rutas y backends en **`networking.k8s.io/v1`**; `ImplementationSpecific` conserva la dependencia del comportamiento del controlador de la forma antigua.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: mying
spec:
  rules:
    - host: example.com
      http:
        paths:
          - path: /hello
            pathType: ImplementationSpecific
            backend:
              service:
                name: mysvc1
                port:
                  number: 80
          - path: /video
            pathType: ImplementationSpecific
            backend:
              service:
                name: mysvc2
                port:
                  number: 80
```

> Service estabiliza el acceso a Pods; Ingress organiza la entrada hacia Services. La gestión centralizada de TLS es una posibilidad de configuración, pero el manifiesto anterior no incluye certificados ni una sección `tls`.

### VI. Volumes and Persistent Storage

#### 19. Volume Lifecycle and Types

> Un **volume** proporciona almacenamiento que puede montarse en los contenedores de un Pod. `spec.volumes` define su origen y cada contenedor declara dónde lo utiliza mediante `volumeMounts`. Varios contenedores pueden montar un mismo volumen, incluso en rutas diferentes.
>
> La referencia del volumen dentro del Pod participa en su ciclo de vida, pero **la persistencia de los datos depende del tipo de volumen**. Un directorio efímero, una ruta del host y un disco persistente no desaparecen bajo las mismas condiciones.

| Tipo | Persistencia | Límite principal |
| --- | --- | --- |
| **emptyDir** | Sobrevive al reinicio de un contenedor dentro del Pod. | Se pierde cuando el Pod deja de existir en el nodo. |
| **hostPath** | Usa archivos o directorios del nodo, que pueden sobrevivir al Pod. | No transporta automáticamente esos datos a otro nodo. |
| **Almacenamiento externo o persistente** | Puede sobrevivir al reemplazo del Pod y montarse desde otro nodo compatible. | Depende del backend, topología y modo de acceso. |

> Ejemplos de almacenamiento externo son **NFS**, **Fibre Channel (`fc`)** e **iSCSI**. Los tipos históricos `gcePersistentDisk`, `azureDisk` y `awsElasticBlockStore` representan integración con discos cloud. Su compatibilidad está ligada a la versión y a los drivers disponibles.
>
> **emptyDir** se crea vacío y, por defecto, utiliza almacenamiento del nodo. Puede utilizar memoria mediante tmpfs. Es especialmente útil para compartir archivos entre contenedores del mismo Pod.

#### 20. Sharing Files with EmptyDir

> En este ejemplo, `log-creator` utiliza el volumen `content` en `/var/log` y Nginx lo monta como contenido web en `/usr/share/nginx/html`, en modo de solo lectura. El volumen es el mismo aunque cambie su ruta dentro de cada contenedor.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-log
spec:
  containers:
    - image: rmartin1/logdate
      name: log-creator
      volumeMounts:
        - name: content
          mountPath: /var/log
    - image: nginx:alpine
      name: web-server
      volumeMounts:
        - name: content
          mountPath: /usr/share/nginx/html
          readOnly: true
  volumes:
    - name: content
      emptyDir: {}
```

> El productor puede escribir y el servidor leer esos mismos archivos. Reiniciar un contenedor no elimina el volumen; eliminar el Pod sí elimina sus datos. La imagen `rmartin1/logdate` debe estar disponible en el registry y proporcionar la funcionalidad de escritura correspondiente.

#### 21. Direct Persistent Disk Mounting

> El enfoque **`gcePersistentDisk`** monta un Persistent Disk previamente creado. Al quitar el Pod, se desmonta el volumen y se conservan los datos del disco. Puede contener datos previamente cargados y utilizarse sucesivamente desde Pods compatibles.
>
> En el caso zonal representado, los nodos deben ser VMs de GCE del proyecto y zona adecuados. Antes de montar el disco se necesita acceso al proyecto, permisos para crearlo y utilizarlo, y un sistema de archivos compatible. Crear un disco vacío no equivale a haber cargado ya su contenido web.

```bash
gcloud compute disks create --size=10GB --zone=europe-west1-b my-disk
```

> [!warning] Corrección
> En el material aparece `--size=1GiB`, pero `gcloud compute disks create` documenta tamaños con unidades `GB` o `TB` y los Persistent Disks estándar tienen un mínimo de 10 GiB. Para este ejemplo se utiliza `--size=10GB`.
> Fuente de comprobación: [gcloud: creación de discos](https://docs.cloud.google.com/sdk/gcloud/reference/compute/disks/create) y [Compute Engine: límites de tamaño](https://docs.cloud.google.com/compute/docs/disks/add-persistent-disk)

> El siguiente manifiesto conserva el **modelo heredado de montaje directo**. El driver in-tree fue retirado; en clústeres actuales la integración se realiza mediante CSI o migración compatible hacia el driver de Persistent Disk. No debe suponerse que el fragmento sirve para cualquier versión sin esa integración.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-fe
spec:
  containers:
    - image: nginx:alpine
      name: web-server
      volumeMounts:
        - name: content
          mountPath: /usr/share/nginx/html
          readOnly: true
  volumes:
    - name: content
      gcePersistentDisk:
        pdName: my-disk
        fsType: ext4
        readOnly: true
```

> `pdName` identifica el disco y `fsType` su sistema de archivos. El montaje de solo lectura conserva la finalidad de servir datos sin modificarlos.

#### 22. PersistentVolumes and Claims

> Para ocultar los detalles del almacenamiento a la aplicación, Kubernetes separa la **oferta** de la **solicitud**:
>
> - Un **PersistentVolume (PV)** representa almacenamiento del clúster y captura su implementación. Su ciclo de vida es independiente de un Pod concreto.
> - Un **PersistentVolumeClaim (PVC)** solicita capacidad y modos de acceso. Pertenece a un namespace y la aplicación lo utiliza por su nombre.
> - Una **StorageClass (SC)** describe una clase de almacenamiento y su provisioner, necesaria para el aprovisionamiento dinámico basado en esa clase.
>
> **ReadWriteOnce (RWO)** permite escritura desde un nodo; **ReadOnlyMany (ROX)** permite lectura desde varios nodos. RWO no significa necesariamente un único Pod: varios Pods del mismo nodo pueden utilizar el volumen según las condiciones del backend.
>
> La separación permite que el Pod solicite almacenamiento sin conocer si está implementado con un disco de GCE u otra tecnología compatible.

#### 23. Manual Provisioning

##### 23.1. Provisioning and Binding Sequence

> En el aprovisionamiento manual:
>
> 1. El administrador crea el almacenamiento físico o cloud.
> 2. Crea un PV que lo representa.
> 3. El usuario publica un PVC con su solicitud.
> 4. Kubernetes vincula la solicitud con un PV compatible.
> 5. El Pod referencia ese PVC.

![[apuntes-752457319883-p0045-3763ca235f77.png]]

> La compatibilidad incluye capacidad, modos de acceso y clase. Un PVC puede quedar pendiente si no hay almacenamiento compatible. **Retain** conserva el almacenamiento para recuperación manual cuando se libera la reclamación; no significa que Kubernetes lo vuelva a ofrecer automáticamente con sus datos a cualquier usuario.

##### 23.2. Manual Provisioning Manifests

> Este ejemplo utiliza un disco en `europe-north1-a`. Es una alternativa al ejemplo de `europe-west1-b`: un disco zonal no se mueve de zona por reutilizar su nombre. La capacidad de creación se ajusta al mínimo válido, manteniendo una solicitud ilustrativa de 1 Gi.

```bash
gcloud compute disks create --size=10GB --zone=europe-north1-a my-disk
```

> Primero se describe el PV. Se mantiene la integración heredada `gcePersistentDisk`, con las condiciones de compatibilidad anteriores. `storageClassName: ""` deja explícito que no pertenece a una clase dinámica.

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: web-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
    - ReadOnlyMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: ""
  gcePersistentDisk:
    pdName: my-disk
    fsType: ext4
```

> El PVC pide 1 Gi y RWO; esa solicitud puede satisfacerse con un PV mayor.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: web-pvc
spec:
  resources:
    requests:
      storage: 1Gi
  accessModes:
    - ReadWriteOnce
  storageClassName: ""
```

> [!warning] Corrección
> En el material aparece `resources.request` en los PVC y un disco de 1 GiB, pero el campo correcto es `resources.requests`. La capacidad declarada del PV debe representar el disco disponible; por eso se declaran 10 Gi para el disco de este ejemplo, conservando la solicitud de 1 Gi del PVC.
> Fuente de comprobación: [Kubernetes: PersistentVolumes y solicitudes de almacenamiento](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)

> Finalmente el Pod referencia `web-pvc` del mismo namespace. No contiene el nombre del disco ni sus detalles de implementación.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-fe
spec:
  containers:
    - image: nginx:alpine
      name: web-server
      volumeMounts:
        - name: content
          mountPath: /usr/share/nginx/html
  volumes:
    - name: content
      persistentVolumeClaim:
        claimName: web-pvc
```

> Los manifiestos se aplican en orden: PV, PVC y Pod, después de preparar el disco. Si hay otros PV compatibles, el binding depende de la selección de Kubernetes; los nombres `web-pv` y `web-pvc` no obligan por sí solos a vincularlos.

#### 24. Automatic Provisioning

> En el **dynamic provisioning** no se crean previamente todos los PV. El administrador configura un provisioner y una o varias StorageClasses; el usuario solicita almacenamiento con un PVC que selecciona una clase. El provisioner crea el almacenamiento y su PV, que se vincula al PVC; el Pod lo consume.

![[apuntes-752457319883-p0047-419ad0e9fb69.png]]

> El ejemplo define `fast` para discos SSD en `europe-north1-a`. `kubernetes.io/gce-pd` es el provisioner histórico in-tree; un clúster con CSI utiliza la configuración compatible de su driver. Se conserva esta forma para comprender cómo la clase conecta la solicitud con la infraestructura.

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-ssd
  zone: europe-north1-a
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: web-pvc
spec:
  resources:
    requests:
      storage: 1Gi
  accessModes:
    - ReadWriteOnce
  storageClassName: fast
```

> La solicitud de 1 Gi no obliga a que el proveedor cree un disco de exactamente ese tamaño: el almacenamiento debe respetar sus mínimos. El Pod puede utilizar la misma referencia `claimName: web-pvc`. Este PVC es una alternativa al manual; ambos no se crean simultáneamente con el mismo nombre y namespace.
>
> La diferencia decisiva es **quién y cuándo crea el almacenamiento**. En el modelo manual existe antes del PVC; en el automático se crea a partir de la solicitud y de la clase. El binding y las restricciones de topología siguen siendo necesarios.


### VII. Workload Controllers

#### 25. ReplicaSets

> Un **ReplicaSet** mantiene el número deseado de réplicas de Pod mediante un selector y una **Pod template**. Si falta una réplica, el controlador crea otra a partir de la plantilla; si sobran, reduce el conjunto. Mantener el número deseado es una tarea de reconciliación, no una garantía de que todas estén disponibles en cualquier instante.

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: my-replicaset
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: nginx
          image: nginx:latest
          ports:
            - containerPort: 80
```

> `replicas: 3` declara la cantidad. El selector coincide con la etiqueta de la plantilla. `containerPort: 80` describe el puerto del contenedor y no crea un Service. El ReplicaSet mantiene réplicas; para gestionar actualizaciones declarativas se utiliza normalmente un Deployment.

#### 26. Deployments and Application Updates

> Un **Deployment** declara una aplicación y administra la actualización de sus ReplicaSets. Sus estrategias principales son:
>
> - **Recreate**: elimina las instancias antiguas antes de crear las nuevas.
> - **RollingUpdate**: sustituye gradualmente las réplicas.
>
> Un despliegue **blue-green** utiliza conjuntos separados para las versiones y un cambio de tráfico entre ellos; no es una tercera opción del campo `strategy.type` y necesita coordinación adicional.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-fe
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  minReadySeconds: 30
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      name: web
      labels:
        app: web
    spec:
      containers:
        - image: nginx:alpine
          name: web-server
          readinessProbe:
            periodSeconds: 1
            httpGet:
              path: /
              port: 8080
```

> Se mantiene la condición de que Nginx escuche en 8080. **maxSurge: 1** permite una réplica adicional durante la actualización; **maxUnavailable: 0** impide que la estrategia reduzca voluntariamente el número de réplicas disponibles por debajo del deseado. Para tres réplicas, puede haber hasta cuatro Pods durante el rollout.
>
> **minReadySeconds: 30** exige que un Pod permanezca Ready durante ese tiempo antes de considerarlo disponible. La readiness probe y ese intervalo pueden bloquear el avance de una versión defectuosa. Se necesita capacidad para las réplicas adicionales; estas opciones no evitan fallos independientes de los nodos o de la aplicación.

> [!warning] Corrección
> En el material aparece `apiVersion: app/v1beta1` para Deployment y StatefulSet, pero el grupo es `apps`; los ejemplos se expresan en la API estable `apps/v1`, que exige un selector explícito coherente con las labels de la plantilla. `apps/v1beta1` pertenecía a versiones antiguas.
> Fuente de comprobación: [Kubernetes: migración de APIs](https://kubernetes.io/docs/reference/using-api/deprecation-guide/)

#### 27. StatefulSets

> Un **StatefulSet** administra aplicaciones que necesitan **identidades estables y únicas**, almacenamiento persistente y creación o escalado ordenados. Las identidades permiten distinguir las réplicas, aunque sus Pods concretos sean reemplazados.
>
> Un **headless Service**, con `clusterIP: None`, proporciona descubrimiento de las identidades sin una IP virtual de balanceo convencional. `serviceName` vincula el StatefulSet con ese Service.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: hl-web
spec:
  clusterIP: None
  selector:
    app: web-db
  ports:
    - port: 3306
      name: mysql
```

> El ejemplo utiliza MySQL. Para inicializar la imagen se necesita configurar credenciales, y el directorio montado debe coincidir con el directorio de datos del servidor. La preparación siguiente añade una credencial ilustrativa mediante Secret; el argumento `--datadir=/var/data` conecta el montaje del ejemplo con los datos reales.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysql-initialization
type: Opaque
stringData:
  root-password: secretpassword
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: db
spec:
  serviceName: hl-web
  replicas: 3
  selector:
    matchLabels:
      app: web-db
  template:
    metadata:
      labels:
        app: web-db
    spec:
      containers:
        - image: mysql:8.0
          name: db
          args:
            - --datadir=/var/data
          env:
            - name: MYSQL_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: mysql-initialization
                  key: root-password
          volumeMounts:
            - name: data
              mountPath: /var/data
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        resources:
          requests:
            storage: 1Mi
        accessModes:
          - ReadWriteOnce
```

> `volumeClaimTemplates` genera una reclamación de almacenamiento propia para cada réplica. La solicitud **1 Mi** es una cantidad esquemática; no es un dimensionamiento suficiente por sí solo para una base MySQL. El almacenamiento real debe satisfacer las necesidades de inicialización y crecimiento y requiere una clase predeterminada o PV compatibles.
>
> Las identidades siguen un orden, como `db-0`, `db-1` y `db-2`. Reemplazar un Pod no exige tratarlo como una identidad completamente nueva. **Crear tres Pods MySQL no configura automáticamente replicación ni una base distribuida**: el StatefulSet aporta identidad y almacenamiento; la coordinación de la base pertenece a la aplicación.

#### 28. Other Workload and Extension Resources

| Recurso | Finalidad | Matiz |
| --- | --- | --- |
| **DaemonSet** | Ejecutar una instancia de Pod en cada nodo elegible. | Útil para agentes de red o recolectores de logs; depende de selectores y restricciones de nodos. |
| **Job** | Ejecutar una tarea hasta completarla. | Puede utilizar varios Pods secuenciales o paralelos. |
| **CronJob** | Crear Jobs con una programación temporal. | Ejecuta tareas periódicas según un schedule. |
| **CustomResourceDefinition (CRD)** | Introducir tipos de recursos propios. | Normalmente se acompaña de un controlador que implementa su comportamiento. |

> Un Job completado no se reinicia como un servicio permanente. Ante fallos pueden existir reintentos según su configuración; **activeDeadlineSeconds** limita el tiempo de ejecución del Job. CronJob organiza la creación programada de Jobs.
>
> Definir una CRD incorpora un tipo a la API, pero no implementa por sí solo las acciones necesarias para cumplir el estado deseado de ese recurso.

### VIII. Configuration and Secrets

#### 29. ConfigMaps

> Un **ConfigMap** almacena configuración no sensible como pares clave-valor. Un valor puede ser un literal o el contenido completo de un archivo. Los Pods pueden recibirlo mediante variables de entorno o un volumen.

##### 29.1. Environment Variables

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-config-map
data:
  DB_HOST: "mysql.example.com"
  DB_PORT: "3306"
  DB_USER: "root"
---
apiVersion: v1
kind: Pod
metadata:
  name: web-fe
spec:
  containers:
    - image: nginx:alpine
      name: web-server
      envFrom:
        - prefix: CONF_
          configMapRef:
            name: my-config-map
```

> `envFrom` importa las claves con el prefijo indicado: aparecen variables como `CONF_DB_HOST`, `CONF_DB_PORT` y `CONF_DB_USER`. Su existencia no significa que Nginx configure automáticamente una conexión a MySQL; la aplicación debe leerlas y utilizar su significado.

##### 29.2. Configuration Files

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-config-map
data:
  app-config.conf: |
    DB_HOST: "mysql.example.com"
    DB_PORT: "3306"
    DB_USER: "root"
---
apiVersion: v1
kind: Pod
metadata:
  name: web-fe
spec:
  containers:
    - image: nginx:alpine
      name: web-server
      volumeMounts:
        - name: config-volume
          mountPath: /etc/myapp
  volumes:
    - name: config-volume
      configMap:
        name: my-config-map
```

> El contenido de `app-config.conf` se presenta como archivo en `/etc/myapp/app-config.conf`. El símbolo `|` conserva un bloque de texto multilínea. Son dos variantes alternativas de los mismos nombres, no recursos adicionales que puedan coexistir con esos nombres en el mismo namespace.

> [!warning] Corrección
> En el material aparecen comillas tipográficas y el valor `DB_USER` sin cierre de comillas, pero los ejemplos deben expresar las cadenas con comillas válidas y cerradas, como `DB_USER: "root"`; el puerto del ConfigMap se almacena como cadena `"3306"`.
> Fuente de comprobación: [Kubernetes: ConfigMaps y valores de configuración](https://kubernetes.io/docs/concepts/configuration/configmap/)

#### 30. Secrets

> Un **Secret** guarda configuración sensible, como credenciales o claves. Puede inyectarse mediante variables de entorno o volúmenes. Separarlo de un ConfigMap permite aplicar controles de acceso específicos, pero su nombre no aporta por sí solo cifrado.
>
> El kubelet obtiene los Secrets que necesitan los Pods del nodo. En el montaje de Secrets sobre Linux se utiliza **tmpfs** para la copia del volumen. Esto debe distinguirse del almacenamiento del objeto en etcd y de cualquier copia que haga la aplicación.

> [!warning] Corrección
> En el material aparece que los Secrets se almacenan cifrados en etcd y que nunca se escriben en almacenamiento físico, pero Kubernetes no cifra por defecto sus valores en etcd: el cifrado en reposo requiere configuración. El uso de tmpfs corresponde a la copia montada por el kubelet y no garantiza que ningún componente pueda guardar otra copia.
> Fuente de comprobación: [Kubernetes: almacenamiento y seguridad de Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)

> El ejemplo conserva el archivo con contenido `db-password: secretpassword`. En `data` se representa mediante **base64**, que es codificación reversible, no cifrado.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
data:
  app-config.conf: ZGItcGFzc3dvcmQ6IHNlY3JldHBhc3N3b3JkCg==
---
apiVersion: v1
kind: Pod
metadata:
  name: web-fe
spec:
  containers:
    - image: nginx:alpine
      name: web-server
      volumeMounts:
        - name: config-volume
          mountPath: /etc/myapp/app-config.conf
          subPath: app-config.conf
  volumes:
    - name: config-volume
      secret:
        secretName: my-secret
        items:
          - key: app-config.conf
            path: app-config.conf
```

> `items` selecciona la clave y su ruta dentro del volumen. `subPath` monta ese archivo concreto. Como alternativa, **stringData** acepta el texto sin codificar y Kubernetes lo convierte a la representación de datos del Secret, como en la preparación de MySQL.
>
> Un archivo montado con `subPath` no recibe automáticamente las actualizaciones posteriores del Secret. El mecanismo de configuración y su actualización deben formar parte del diseño de la aplicación.

> [!warning] Corrección
> En el material aparece texto sin codificar dentro de `Secret.data`, `kind: pod` y el campo `ítems`, pero la representación correcta utiliza valores base64 en `data` —o texto en `stringData`—, `kind: Pod` y `items` sin tilde.
> Fuente de comprobación: [Kubernetes: definición de Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)

### IX. Autoscaling

#### 31. Horizontal Pod Autoscaling

> **HorizontalPodAutoscaler (HPA)** cambia el número de réplicas de una carga, como un Deployment, ReplicaSet o StatefulSet. Declara el recurso objetivo, los límites de réplicas y las métricas utilizadas.
>
> Para escalar por **utilización de CPU respecto al request**, deben existir requests de CPU y una API de métricas disponible. El request es la referencia de esa utilización, no el límite máximo ni la capacidad completa del nodo. La variante de Deployment utilizada para el ejemplo es:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-fe
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      name: web
      labels:
        app: web
    spec:
      containers:
        - image: nginx:alpine
          name: web-server
          resources:
            requests:
              cpu: "500m"
              memory: "20Mi"
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-fe
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50
```

> El objetivo es `web-fe`, con entre **2 y 10 réplicas** y una utilización media de CPU del **50 % del request**. Con un request de `500m`, ese objetivo corresponde a `250m` por Pod como referencia de uso medio. El controlador evalúa métricas periódicamente y ajusta las réplicas dentro de los límites.
>
> La condición de definir requests se aplica a esta métrica de utilización relativa; otras métricas de HPA pueden utilizar referencias diferentes.

> [!warning] Corrección
> En el material aparece `kind: HorizontalpodAutoscaler`, pero el nombre correcto del recurso es `HorizontalPodAutoscaler`, respetando las mayúsculas.
> Fuente de comprobación: [Kubernetes: API de HorizontalPodAutoscaler](https://kubernetes.io/docs/reference/kubernetes-api/autoscaling/horizontal-pod-autoscaler-v2/)

#### 32. Vertical Pod Autoscaling

> **VerticalPodAutoscaler (VPA)** ajusta los **resource requests** de los contenedores según su uso. HPA modifica cuántas réplicas hay; VPA modifica los recursos solicitados por cada una.
>
> En el enfoque de actualización por recreación, el cambio se aplica mediante sustitución de Pods, por lo que hay que prever esa interrupción. El requisito de reinicio depende del modo y del soporte de actualización de recursos; no es una propiedad universal de todas las implementaciones de VPA.
>
> El escalado de Pods tampoco equivale al de nodos. Puede haber más réplicas pendientes porque no exista capacidad suficiente; en ese caso la gestión de infraestructura debe aumentar los nodos cuando corresponda.


### X. Securing the Kubernetes Cluster

#### 33. Authentication and ServiceAccounts

> El acceso al API server separa **authentication** y **authorization**. La autenticación identifica al sujeto y sus grupos; la autorización decide si puede realizar la operación sobre el recurso solicitado.
>
> Los usuarios humanos suelen integrarse mediante sistemas externos, como SSO. Las aplicaciones que se ejecutan en Pods utilizan **ServiceAccounts de Kubernetes**. Una ServiceAccount de Kubernetes no es automáticamente la misma identidad que una service account de Google Cloud.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: example-service-account
  namespace: my-ns
---
apiVersion: v1
kind: Pod
metadata:
  name: web-pod
  namespace: my-ns
spec:
  serviceAccountName: example-service-account
  containers:
    - image: <custom-image>
      name: web-server
```

> `my-ns` debe existir y `<custom-image>` debe sustituirse por una imagen disponible. El Pod y la cuenta pertenecen al mismo namespace. Asociar una identidad al Pod no concede por sí solo todos los permisos de administración.

#### 34. Role-Based Access Control

##### 34.1. Roles and Bindings

> **RBAC** autoriza acciones mediante reglas sobre recursos. Un **Role** define permisos y un **RoleBinding** relaciona sujetos con el rol. **ClusterRole** permite definir permisos de ámbito de clúster o reutilizar un conjunto de reglas; el binding determina dónde se conceden.

| Relación | Alcance |
| --- | --- |
| **RoleBinding → Role** | Recursos del namespace donde se define el binding. |
| **ClusterRoleBinding → ClusterRole** | Permisos en el conjunto del clúster, incluidos recursos de namespaces cuando las reglas los cubren. |
| **RoleBinding → ClusterRole** | Concede las reglas aplicables a recursos del namespace del binding; no concede acceso global a recursos de clúster. |

> Un ClusterRole puede describir acceso a **Nodes**, **PersistentVolumes**, recursos con namespace o URLs que no representan recursos, como `/api` y `/healthz`. Referenciarlo desde un RoleBinding no amplía el binding fuera de su namespace.
>
> Entre los roles predefinidos aparecen **view**, **edit**, **admin** y **cluster-admin**, con capacidades diferentes. La elección del rol y el ámbito de la concesión deben responder a la operación necesaria.

##### 34.2. RBAC Example

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-viewer
  namespace: my-ns
rules:
  - apiGroups: [""]
    verbs: ["get", "list"]
    resources: ["services"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: example-role-binding
  namespace: my-ns
subjects:
  - kind: ServiceAccount
    name: example-service-account
    namespace: my-ns
roleRef:
  kind: Role
  name: pod-viewer
  apiGroup: rbac.authorization.k8s.io
```

> `apiGroups: [""]` identifica el grupo principal de la API. La cuenta obtiene `get` y `list` sobre **Services de my-ns**. Aunque el nombre sea `pod-viewer`, el recurso declarado es `services`: **el nombre del rol no determina sus permisos**. Este ejemplo no permite consultar Pods ni modificar Services.
>
> `subjects` identifica a quién se concede y `roleRef` qué reglas se conceden. El nombre y namespace de la cuenta deben coincidir con los del sujeto utilizado por la aplicación.

#### 35. Security Context and Admission Policies

> Algunas opciones reducen o amplían de forma importante el aislamiento:
>
> - **hostNetwork**, **hostPID** y **hostIPC** permiten utilizar los ámbitos del host correspondientes.
> - **securityContext** configura aspectos de ejecución del Pod o del contenedor; cada propiedad debe situarse en el nivel que admite.
> - **runAsUser: 102** selecciona el UID de ejecución.
> - **runAsNonRoot: true** exige que el proceso no se ejecute como root.
> - **privileged: true** habilita ejecución privilegiada.
> - **readOnlyRootFilesystem: true** impide escribir en el sistema de archivos raíz del contenedor.
>
> Las Linux **capabilities** permiten añadir o retirar privilegios concretos. El fragmento de contexto de seguridad de un contenedor es:

```yaml
capabilities:
  add: ["NET_ADMIN", "SYS_TIME"]
  drop: ["CHOWN", "DAC_OVERRIDE"]
```

> Añadir NET_ADMIN o SYS_TIME y eliminar CHOWN o DAC_OVERRIDE son operaciones con objetivos diferentes. No son una lista conjunta de recomendaciones para cualquier aplicación. Del mismo modo, `privileged: true` aumenta capacidades, mientras que ejecutar sin root o hacer el filesystem de solo lectura busca restringirlas.
>
> **Pod Security Admission** comprueba la configuración de los Pods antes de admitirlos y aplica restricciones de **Pod Security Standards** asociadas al namespace.

| Nivel | Restricción |
| --- | --- |
| **Privileged** | Sin las restricciones de los otros perfiles; para cargas con necesidades especiales. |
| **Baseline** | Evita formas habituales de escalada de privilegios, con restricciones moderadas. |
| **Restricted** | Exige prácticas más estrictas de aislamiento y privilegios. |

> [!warning] Corrección
> En el material aparece que estos niveles se definen en un recurso PodSecurity, pero Pod Security Admission se configura mediante labels del Namespace, como `pod-security.kubernetes.io/enforce: restricted`, y la configuración del admission controller; no mediante un objeto estándar de tipo `PodSecurity`.
> Fuente de comprobación: [Kubernetes: Pod Security Admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/)

> **ValidatingAdmissionPolicy** permite comprobaciones de admisión más específicas. RBAC controla si un sujeto puede solicitar una operación; las políticas de admisión comprueban además si la configuración solicitada es aceptable.

#### 36. NetworkPolicies

##### 36.1. Ingress and Egress Rules

> Una **NetworkPolicy** limita comunicaciones de Pods y requiere una implementación de red que soporte y aplique estas políticas. Crear el objeto no tiene efecto de aislamiento si el plugin no implementa esa funcionalidad.
>
> `podSelector` selecciona los Pods afectados en el namespace de la política. **Ingress** define entradas permitidas y **egress** salidas permitidas. Los peers pueden expresarse mediante `podSelector`, `namespaceSelector` o **ipBlock** con notación CIDR; también se pueden delimitar puertos y protocolos.
>
> Hay que distinguir el **Pod afectado** de los **orígenes o destinos permitidos**. Un selector de namespace compara las labels del Namespace, no las de sus Pods. Un podSelector usado como peer sin namespaceSelector se refiere al namespace de la política.
>
> Las políticas aplicables se combinan de forma aditiva. Si ambos extremos están aislados en la dirección relevante, la comunicación debe estar permitida por la salida del origen y la entrada del destino. Añadir una regla no anula permisos concedidos por otra política.

##### 36.2. Ingress from a Namespace

> La primera política permite acceso a Pods `app: web-db` desde namespaces con la label `ns: op1`, por TCP 3306.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: dbs-netpolicy
spec:
  podSelector:
    matchLabels:
      app: web-db
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              ns: op1
      ports:
        - protocol: TCP
          port: 3306
```

> La etiqueta `ns: op1` debe existir en los namespaces de origen. La regla no selecciona únicamente un Pod concreto de esos namespaces: admite los orígenes que cumplan la selección indicada.

##### 36.3. Ingress from an IP Block

> La segunda variante permite entrada desde `192.168.54.0/24`. Al no especificar puertos, no limita la regla a 3306. Usa el mismo nombre que la variante anterior, por lo que ambas son configuraciones alternativas del objeto.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: dbs-netpolicy
spec:
  podSelector:
    matchLabels:
      app: web-db
  policyTypes:
    - Ingress
  ingress:
    - from:
        - ipBlock:
            cidr: 192.168.54.0/24
```

##### 36.4. Egress towards Database Pods

> La tercera política limita la salida de Pods `app: web-server` hacia Pods `app: web-db` de su mismo namespace. Se explicita `policyTypes: [Egress]` para que la intención sea únicamente de salida.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-netpolicy
spec:
  podSelector:
    matchLabels:
      app: web-server
  policyTypes:
    - Egress
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: web-db
```

> Sin una lista de puertos, la regla permite los puertos aplicables hacia esos destinos. Una aplicación que también necesite comunicarse con DNS u otros servicios requerirá permisos de salida correspondientes; esa ampliación no está incluida en el ejemplo.

> [!warning] Corrección
> En el material aparecen `ports: 3306`, un CIDR terminado en dos puntos y una política de solo salida sin `policyTypes`, pero `ports` debe ser una lista de objetos, el CIDR es `192.168.54.0/24` y `policyTypes: [Egress]` evita que el default incluya también aislamiento de entrada.
> Fuente de comprobación: [Kubernetes: definición y comportamiento de NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/)

### XI. Google Kubernetes Engine

#### 37. Managed Kubernetes and Operational Features

> **Google Kubernetes Engine (GKE)** proporciona Kubernetes gestionado por Google. Conserva la separación entre control plane y worker nodes, pero distribuye las responsabilidades de operación según el modo elegido.
>
> Sus funciones incluyen:
>
> - Actualizaciones gestionadas con **release channels**, para organizar la incorporación de versiones.
> - Ventanas y exclusiones de mantenimiento.
> - Escalado de nodos para responder a las necesidades de capacidad de los Pods.
> - **Node auto-repair**.
> - Logging y monitoring integrados.
> - Opciones de alta disponibilidad del plano de control y de los nodos.
> - Sistemas operativos reforzados, como **Container-Optimized OS**, y controles de seguridad integrados.
>
> Un objetivo mensual de disponibilidad superior al **99 %** expresa un **SLO** del servicio bajo sus condiciones. No equivale a garantizar ese porcentaje para cualquier aplicación: también importan la configuración del clúster, la distribución de réplicas y las dependencias.
>
> El escalado de nodos responde a los recursos necesarios para alojar cargas, no exclusivamente al número bruto de Pods. Dos conjuntos con la misma cantidad de Pods pueden solicitar CPU y memoria muy diferentes.

#### 38. Standard and Autopilot

| Aspecto | **Standard** | **Autopilot** |
| --- | --- | --- |
| Plano de control | Google lo crea y mantiene. | Google lo crea y mantiene. |
| Infraestructura de nodos | El cliente configura y dimensiona, con herramientas gestionadas disponibles. | Google administra la infraestructura y su adaptación. |
| Configuración | Mayor control de tipos de máquina, discos, imagen y ajustes del SO. | Más restricciones y menor carga de administración. |
| Actualizaciones, disponibilidad y hardening | El cliente conserva decisiones y responsabilidades de configuración. | Google asume más tareas operativas y controles predeterminados. |
| Atención principal del cliente | Aplicación e infraestructura configurable. | Aplicación y sus recursos, permisos y políticas. |
| Referencia de facturación | Recursos de los nodos/VMs, además de otros conceptos del servicio. | Recursos solicitados por Pods de uso general; algunas cargas con hardware específico usan facturación por nodos. |

> **Standard** ofrece flexibilidad para necesidades específicas y exige más experiencia de administración y optimización. Que el cliente gestione decisiones sobre los nodos no significa que deba realizar manualmente cada actualización: puede utilizar funciones gestionadas.
>
> **Autopilot** reduce la necesidad de gestionar los nodos y permite concentrarse en la aplicación. El esquema **pay per pod** significa facturación basada en los recursos de Pods para las cargas generales, no una tarifa fija por cada Pod ni una regla universal para cualquier hardware.
>
> En ambos casos siguen siendo necesarias las decisiones de aplicación: manifests, imágenes, configuración, acceso, almacenamiento y tolerancia a fallos. Google no convierte automáticamente una aplicación con una sola réplica o datos efímeros en una aplicación resistente a pérdidas.

### XII. Cloud Native

#### 39. Definition and Key Principles

> **Cloud Native** describe el diseño de aplicaciones para aprovechar entornos dinámicos y distribuidos, en clouds públicas, privadas o híbridas. Incluye contenedores, microservicios, service meshes, infraestructura inmutable y APIs declarativas.
>
> El objetivo es construir sistemas de bajo acoplamiento, resilientes, gestionables y observables. La automatización permite introducir cambios frecuentes y predecibles con menos operación manual. La **Cloud Native Computing Foundation (CNCF)** impulsa un ecosistema de proyectos open source y tecnologías neutrales respecto al proveedor.
>
> Los principios principales son:
>
> 1. **Microservices architecture**: responsabilidades separadas y despliegue independiente.
> 2. **Containers**: empaquetado consistente de aplicaciones.
> 3. **Orchestration and automation**: gestión automática de ejecución y cambios.
> 4. **DevOps y CI/CD**: integración y despliegue mediante procesos repetibles.
> 5. **Infrastructure as Code**: infraestructura descrita mediante definiciones versionables.
> 6. **Immutable infrastructure**: sustituir instancias por versiones nuevas en lugar de depender de cambios manuales acumulados.
> 7. **Cloud-first design**: asumir desde el diseño las propiedades y restricciones del entorno.
>
> Migrar una aplicación a una VM cloud no implica por sí solo que su arquitectura sea Cloud Native. La diferencia está en cómo utiliza y tolera la dinámica del entorno.

#### 40. Designing for a Dynamic Environment

##### 40.1. Relocation, State and Observability

> Los Pods pueden ser reemplazados y sus direcciones cambiar. La aplicación debe utilizar mecanismos estables de descubrimiento y no depender de una IP de Pod permanente.
>
> Los datos que deban sobrevivir se guardan fuera de la capa escribible del contenedor: en **persistent volumes**, en otro componente con almacenamiento persistente o en servicios externos. Un reinicio del contenedor o el reemplazo del Pod puede perder sus archivos locales; la imagen base no incorpora esos cambios.
>
> Centralizar **logs y KPIs** facilita observar el conjunto aunque desaparezcan las instancias que los generaron. Guardar logs en un servicio como Cloud Storage es una posibilidad de almacenamiento externo.

##### 40.2. Dependencies, Startup and Shutdown

> No se puede asumir que todos los componentes estarán listos en un orden fijo. Una aplicación debe tolerar dependencias temporalmente no disponibles, incluidas las interrupciones durante su ciclo de vida.
>
> Las **readiness probes** deben impedir enviar clientes a una instancia que no puede atenderlos. Los **init containers** permiten comprobar o preparar condiciones antes de arrancar los contenedores de aplicación. Los lifecycle hooks, como **postStart** y **preStop**, permiten coordinar acciones en el arranque o la terminación.
>
> También hay que manejar el apagado para evitar cortar peticiones o conexiones en curso. Los hooks y las probes aportan mecanismos, pero la aplicación debe cooperar con ellos.
>
> Conviene hacer **stateless** tantos microservicios como sea razonable: así su reemplazo y escalado no dependen de datos que existan únicamente en una instancia. Las partes que requieren estado deben utilizar identidad y almacenamiento compatibles con esa necesidad.

### XIII. Final Summary

> La relación principal del tema es **microservices → containers → orchestration**: los servicios separan responsabilidades, las imágenes empaquetan la ejecución y Kubernetes administra el estado deseado.
>
> El **Pod** es la unidad de planificación y puede agrupar contenedores acoplados. Los namespaces organizan ámbitos, las labels relacionan recursos y los requests guían la asignación de capacidad. **Liveness** decide sobre la recuperación del proceso; **readiness** sobre su disponibilidad para recibir tráfico.
>
> **Services** proporcionan acceso estable a conjuntos de Pods e **Ingress** organiza la entrada HTTP/HTTPS. **Volumes, PV, PVC y StorageClass** separan montaje, almacenamiento disponible, solicitud y aprovisionamiento. Eliminar un Pod no tiene el mismo efecto sobre todos los tipos de almacenamiento.
>
> **ReplicaSet** mantiene réplicas; **Deployment** administra actualizaciones; **StatefulSet** aporta identidades y almacenamiento por réplica. ConfigMaps y Secrets separan configuración de las imágenes, mientras que HPA cambia el número de réplicas y VPA ajusta sus recursos.
>
> La seguridad combina **identidad, RBAC, contexto de ejecución, admisión y NetworkPolicy**. GKE gestiona parte de la infraestructura, con más control en Standard y más automatización en Autopilot. Una aplicación Cloud Native debe completar ese soporte mediante descubrimiento estable, persistencia externa, observabilidad y manejo de dependencias y apagado.




