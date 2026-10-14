---
estado: pendiente de revisión
---

### I. Realimentación y telemetría en DevOps

#### 1. El retorno de información desde producción

> Un sistema desplegado necesita **monitorización** para conocer cómo se comporta realmente. La idea «si no está monitorizado, no está en producción» expresa que operar un servicio exige observarlo: saber si está disponible, si responde con el rendimiento esperado y si cumple su propósito de negocio.
>
> Este retorno de información materializa los **feedback loops** de DevOps. Desarrollo incorpora lógica de negocio, Operaciones observa su funcionamiento y los datos obtenidos vuelven a quienes pueden mejorar el producto. La realimentación permite relacionar las decisiones de desarrollo con sus efectos en producción.
>
> La información debe llegar con rapidez a cada fase del trabajo. Así se pueden evaluar los efectos de una acción mientras todavía resulta fácil interpretarlos, corregir problemas y orientar el siguiente cambio. Esto mejora la productividad, ayuda a mantener el foco en los objetivos y promueve una cultura de mejora continua.

#### 2. Qué recoge la telemetría y quién la necesita

> La **telemetría** es la recogida de información sobre el funcionamiento del sistema. Incluye aspectos no funcionales, como la velocidad de respuesta y el uso de memoria, que deben revisarse junto con el comportamiento funcional de la aplicación.
>
> El equipo de desarrollo necesita esos datos para comprobar sus decisiones técnicas. También se elaboran **KPI** y se sigue el progreso de los **OKR**, de modo que la información relevante pueda compartirse con los responsables del producto y el negocio.
>
> Negocio debe participar en la elección de los requisitos no funcionales que se observan y en la forma de informar sobre ellos. Una cifra técnica adquiere utilidad cuando se entiende su relación con el servicio ofrecido: por ejemplo, el tiempo de respuesta influye en la experiencia de uso.

#### 3. Medir para contrastar hipótesis

> El **Hypothesis Driven Development** plantea los cambios como hipótesis sobre lo que ocurrirá: «si modificamos este comportamiento, ¿qué efecto esperamos?». La telemetría permite comparar esa expectativa con lo observado y decidir si continuar, corregir o reconsiderar el cambio.
>
> La realimentación sirve para comprobar hipótesis, aprender y mantener a los equipos centrados en metas compartidas. Hacer visibles los resultados también aumenta la conciencia sobre el estado del producto y la motivación para mejorarlo.
>
> La cadena de trabajo es: **acción → observación de sus efectos → interpretación → siguiente decisión**. Recoger datos sin revisarlos ni relacionarlos con una decisión deja incompleto el circuito de realimentación.

### II. Monitorización y gestión de alertas

#### 4. Disponibilidad, recursos y tendencias

> La monitorización tradicional de Operaciones comprueba que los servicios estén disponibles y que la infraestructura funcione. Se observan el estado de los procesos, la CPU, la memoria, el disco y el ancho de banda.
>
> Una comprobación de estado responde si un componente funciona en ese momento. Las **series temporales** permiten estudiar cómo evoluciona: comparar periodos, reconocer patrones de carga, estimar la capacidad disponible y anticipar problemas.
>
> Por ejemplo, saber cuánto espacio libre queda en un disco aporta una fotografía del estado. Observar cómo disminuye ese espacio permite interpretar la velocidad de crecimiento y actuar antes de que se agote.

![[imgs/apuntes-72c6f8347543-p0006-9276717d76ae.png]]

> La figura compara el uso de CPU en ventanas diaria y semanal, desglosado por categorías. La vista diaria muestra variaciones concretas y la semanal ayuda a reconocer patrones recurrentes. Cambiar la ventana temporal proporciona contexto para distinguir una oscilación habitual de un comportamiento excepcional.

#### 5. Alertas y responsabilidad compartida

> El **alerting** avisa de una incidencia para que intervenga el equipo responsable. En el enfoque tradicional, la alerta suele dirigirse a Operaciones, pero este equipo puede necesitar la participación de otras áreas para diagnosticarla y resolverla.
>
> En una organización ágil, Negocio, Desarrollo, QA, Operaciones y Soporte participan según el problema. Un fallo de infraestructura, un defecto del código y una consecuencia inesperada de una regla de negocio requieren conocimientos diferentes.
>
> La alerta debe conducir a una respuesta. Si se emiten demasiados avisos sin una acción clara, la atención se degrada y los fallos relevantes pueden pasar inadvertidos.

#### 6. Limitaciones del enfoque tradicional

> Las dificultades de la monitorización clásica se hacen especialmente visibles al trasladar una configuración centralizada y manual a una infraestructura dinámica. Las críticas siguientes describen ese enfoque; su gravedad depende de la arquitectura y de las capacidades concretas de la herramienta.

##### 6.1. De servidores estables a infraestructura efímera

> El modelo de servidores tratados como **pets** presupone máquinas duraderas que se registran y configuran individualmente. Un sistema central conserva la lista de servidores y las comprobaciones que debe ejecutar sobre sus servicios.
>
> En el modelo **cattle**, las instancias se crean y destruyen de forma habitual. Registrar cada una manualmente dificulta seguir el ritmo de un entorno cloud. La monitorización necesita adaptarse al ciclo de vida de los recursos y descubrir los componentes que existen en cada momento.

##### 6.2. Escalabilidad de las comprobaciones

> Si se ejecuta una comprobación por minuto para CPU, red, memoria, disco y servicio, cada nodo añade cinco comprobaciones por minuto. El trabajo crece con el número de nodos.
>
> Un monitor central que concentre toda esa carga puede convertirse en un cuello de botella. El problema se agrava cuando su diseño no permite repartir las comprobaciones entre componentes independientes.

##### 6.3. Configuración compleja y estados demasiado simples

> Algunas herramientas tradicionales requieren archivos de configuración extensos, cambios difíciles de automatizar y reinicios para aplicar modificaciones. Esto encarece mantener la monitorización actualizada en un sistema que cambia continuamente.
>
> Un resultado binario **UP/DOWN** tampoco explica toda la situación. Un servicio puede estar activo y responder lentamente; un disco puede seguir disponible y estar llenándose a una velocidad preocupante. La tendencia y el contexto complementan el estado instantáneo.

##### 6.4. Fatiga de alertas e informes poco accionables

> La **fatiga de alertas** aparece cuando el volumen de avisos supera la capacidad de atenderlos. Recibir cien correos diarios puede llevar a ignorar el canal completo, incluso cuando contiene una incidencia relevante.
>
> Los informes básicos de disponibilidad y **SLA** ayudan a evaluar el cumplimiento del servicio, pero deben complementarse con información que permita interpretar y mejorar la operación. La **Operational Intelligence** utiliza los datos para comprender qué ocurre y orientar acciones, además de resumir estados o porcentajes de disponibilidad.

#### 7. Evolución de las herramientas de monitorización

> La comunidad técnica ha impulsado esta evolución mediante foros, canales de conversación, repositorios, herramientas y publicaciones que comparten problemas y soluciones. Las necesidades de la infraestructura dinámica han favorecido sistemas más automatizables y escalables.

| Necesidad | Capacidad que la aborda |
| --- | --- |
| Aumento del número de recursos | Recogida escalable y distribuida |
| Aparición y desaparición de instancias | **Autodiscovery** de recursos y servicios |
| Cambios frecuentes | Configuración más sencilla y dinámica |
| Integración entre componentes | Interfaces de paso de mensajes y API |
| Interpretación de la información | Mejores informes y consultas sencillas |

> Se pueden gestionar herramientas dentro de la organización o consumirlas como servicio. Entre los ejemplos de soluciones gestionadas por el equipo aparecen **Zabbix**, **Nagios**, **ELK** y **Prometheus con Grafana**. Entre los ejemplos de servicios o plataformas comerciales figuran **Datadog**, **New Relic**, **Google Cloud Operations**, **AWS CloudWatch** y **Splunk**.
>
> Esta agrupación describe formas de uso: algunas plataformas admiten distintas modalidades de despliegue. La decisión depende de cómo se quiera gestionar la recogida, el almacenamiento, las consultas y la operación de la propia herramienta.

### III. Dashboards, APM y logs

#### 8. Comunicar el estado y visualizar la información

> Una **status page** comunica a los usuarios el estado de un servicio y sus incidencias. Puede presentar componentes o regiones por separado, como en una página de estado de DigitalOcean. Ofrece un canal de información sobre interrupciones que afecta a quienes utilizan el producto.
>
> Un **dashboard** reúne indicadores relevantes mediante gráficos y paneles. Funciona como un **information radiator**: hace visible información que el equipo necesita conocer sin exigir que cada persona la busque en sistemas separados.
>
> Los dashboards pueden actualizarse de forma continua o periódica e integrar varias fuentes. Herramientas como **Geckoboard** y **Grafana** permiten presentar esa información de forma comprensible para distintos destinatarios.

#### 9. Fuentes de datos y API de monitorización

> Los paneles necesitan obtener sus datos de alguna fuente. Pueden consumir información de servicios de terceros, como New Relic o Pingdom, o de una API de la propia aplicación.
>
> Una **monitoring API** expone datos relacionados con las métricas que se quieren observar. El siguiente endpoint representa una consulta de visitas de un CMS:

```text
/api/monitoring/v1/visits?from=10
```

> El ejemplo asocia el nombre del indicador con su valor:

```json
{
  "key": "CMS Visitors NOW",
  "value": 44
}
```

> `key` identifica el indicador y `value` contiene el número mostrado. El valor `44` pertenece al ejemplo y coincide con el panel de visitantes actuales. La interpretación y la unidad del parámetro `from` dependen del contrato de esa API.

> [!warning] Corrección
> En el material aparece el objeto JSON con comillas tipográficas y una coma después del último miembro. JSON exige comillas dobles rectas y no admite esa coma final. El bloque anterior conserva los campos y valores con la sintaxis correcta.
> Fuente de comprobación: [RFC 8259: formato JSON](https://www.rfc-editor.org/rfc/rfc8259)

![[imgs/apuntes-72c6f8347543-p0021-75385aff5efa.png]]

> El dashboard combina una serie de visitas de la última semana con un indicador de visitantes actuales. La serie ayuda a interpretar la evolución, mientras que el segundo panel comunica el valor del momento. Ambos requieren una definición clara de la métrica y de su periodo de observación.

#### 10. Application Performance Management

> **Application Performance Management (APM)** permite detectar y diagnosticar problemas complejos de rendimiento para mantener el nivel de servicio esperado. Relaciona las mediciones técnicas con efectos que tienen sentido para el negocio.
>
> La instrumentación de aplicaciones y servidores recoge información sobre sus conexiones con sistemas backend, las transacciones, el código ejecutado y las dependencias de terceros. También puede facilitar el descubrimiento de la arquitectura y la elaboración de informes.
>
> Por ejemplo, un desglose del tiempo de respuesta por aplicación, base de datos y otros componentes ayuda a localizar dónde se consume el tiempo. El análisis de transacciones permite conectar el rendimiento global con operaciones concretas.

> Estas plataformas permiten consultar datos del sistema y de la aplicación, visualizarlos y extraer **insights**. Un panel puede relacionar el comportamiento técnico con actividad de usuarios, visitas o distribución geográfica, haciendo la información útil para diferentes áreas.
>
> El coste de una solución APM puede ser elevado y resultar una barrera para determinadas organizaciones. Debe valorarse junto con la utilidad de la instrumentación y del análisis que ofrece.

#### 11. Logs estructurados: las cinco preguntas

> Los **logs** registran eventos del sistema. En una aplicación distribuida pueden quedar repartidos entre servicios e instancias, lo que dificulta reconstruir una operación completa.
>
> Un registro útil responde a las cinco preguntas **what, who, when, where y why**: qué ocurrió, quién intervino, cuándo ocurrió, dónde sucedió y por qué. Los campos estructurados permiten buscar, filtrar y agrupar esa información con mayor facilidad que un mensaje aislado.
>
> El siguiente registro describe un fallo de pago en un microservicio desplegado en Kubernetes/OpenShift. Reúne información del evento, el usuario, la transacción, la petición HTTP, el entorno y una dependencia externa.

```json
{
  "timestamp": "2026-03-22T10:15:32.456Z",
  "level": "ERROR",
  "service": "payment-service",
  "version": "v1.4.2",
  "trace_id": "8f3c9a7b2d4e6f01",
  "span_id": "a1b2c3d4",
  "message": "Payment transaction failed due to insufficient funds",
  "event_type": "PAYMENT_FAILED",
  "user": {
    "user_id": "usr-98234",
    "role": "customer"
  },
  "transaction": {
    "transaction_id": "txn-56789",
    "amount": 120.50,
    "currency": "EUR"
  },
  "http": {
    "method": "POST",
    "endpoint": "/api/v1/payments",
    "status_code": 402,
    "client_ip": "192.168.10.45"
  },
  "kubernetes": {
    "namespace": "production",
    "pod_name": "payment-service-7f9c8d6f5b-xk2lm",
    "node": "worker-node-3",
    "cluster": "openshift-prod-eu-west"
  },
  "reason": "INSUFFICIENT_FUNDS",
  "external_dependency": {
    "service": "bank-api",
    "response_time_ms": 230,
    "status": "REJECTED"
  }
}
```

| Pregunta | Campos que ayudan a responderla | Interpretación del ejemplo |
| --- | --- | --- |
| **What: qué ocurrió** | `message`, `event_type`, `transaction`, `http` | Falló una operación de pago asociada a una transacción y una petición |
| **Who: quién intervino** | `user`, `service` | El usuario `usr-98234` actuó como cliente y `payment-service` procesó la operación |
| **When: cuándo ocurrió** | `timestamp` | El evento tiene una marca temporal precisa; `Z` indica UTC |
| **Where: dónde sucedió** | `kubernetes` | Identifica clúster, nodo, pod y namespace |
| **Why: por qué ocurrió** | `reason`, `message`, `external_dependency` | La causa registrada es insuficiencia de fondos y el servicio bancario rechazó la operación |

> El **what** describe el suceso y la operación que se intentaba realizar. El **who** incluye tanto al usuario como al servicio que ejecuta la acción. El identificador de transacción añade contexto para localizar el pago concreto.
>
> El **when** proporciona un instante comparable entre sistemas. Expresar la marca temporal en UTC evita interpretar cada registro con una hora local diferente al correlacionar eventos.
>
> El **where** sitúa el evento dentro del despliegue: el clúster contiene nodos; el pod se ejecuta en un nodo y pertenece al namespace indicado. Esto ayuda a localizar una instancia concreta aunque existan muchas réplicas.
>
> El **why** combina la causa registrada con la respuesta de la dependencia externa. En este ejemplo, un rechazo por insuficiencia de fondos explica el resultado de negocio; ese rechazo, por sí solo, no demuestra que la API bancaria esté caída. El código HTTP `402` forma parte del ejemplo de esta aplicación.
>
> `trace_id` y `span_id` son campos de correlación para relacionar el evento con una operación distribuida y una parte de su ejecución. El nivel `ERROR` y la versión del servicio aportan contexto adicional para la búsqueda y el diagnóstico.

#### 12. Agregar logs para obtener información

> La gestión de logs permite reunir registros distribuidos y consultarlos como un conjunto. Los eventos individuales pueden agruparse por campos y agregarse para obtener conteos o distribuciones.
>
> Por ejemplo, agrupar peticiones por centro de datos permite comparar dónde se concentra la actividad. Una vista temporal muestra cómo cambia el volumen de eventos, mientras que una tabla o un gráfico de barras resume la distribución entre grupos.
>
> La agregación convierte una colección de mensajes en información interpretable. Para que resulte útil, los registros deben conservar campos que permitan relacionar el evento con el servicio, el contexto y el instante en que ocurrió.

### IV. KPI, OKR y medición del progreso

#### 13. De las métricas a los indicadores de negocio

> Una **métrica** cuantifica un aspecto del sistema o de su actividad. Un **Key Performance Indicator (KPI)** es un indicador seleccionado porque ayuda a evaluar un aspecto clave del rendimiento o del negocio.
>
> Los KPI pueden ser cantidades, tiempos o ratios. Su utilidad reside en aportar una visión relevante para gestionar el producto: elegir qué medir orienta la atención hacia lo que se quiere mejorar.
>
> Cada aplicación o servicio debe disponer de un dashboard con los indicadores de negocio relevantes, accesible a las personas implicadas. La visibilidad facilita la transparencia y la conciencia compartida sobre la situación del producto.

#### 14. Qué problemas resuelve un dashboard de KPI

> La presentación de los indicadores debe facilitar su comprensión y conectarlos con los objetivos. Reunir información de distintas fuentes también reduce el trabajo manual de seguimiento.

| Problema | Respuesta del dashboard |
| --- | --- |
| Las métricas de negocio son abstractas o difíciles de comprender | Visualizaciones sencillas y estandarizadas |
| Las personas necesitan orientación | Comunicación de los objetivos y de su progreso |
| Informar sobre métricas consume mucho tiempo | Actualización automática cuando cambian los datos |
| Acceder a varias plataformas resulta incómodo y puede añadir riesgos de acceso | Concentración de la información útil de los distintos servicios |
| Es difícil detectar tendencias entre sistemas | Agregación de fuentes para aportar contexto común |

> Centralizar la visualización no sustituye la recogida de datos: sigue siendo necesario conectar las fuentes adecuadas. El resultado debe permitir interpretar la información sin depender de conocer cada plataforma de origen.

#### 15. Cuatro KPI de DevOps

> Los siguientes indicadores permiten observar la entrega de cambios y la recuperación del servicio. Deben interpretarse conjuntamente para relacionar la velocidad de entrega con la estabilidad de la operación.

| KPI | Qué mide | Ejemplos de valores |
| --- | --- | --- |
| **Deployment frequency** | Frecuencia con la que la organización despliega código | Varios despliegues al día; semanal; mensual |
| **Lead time for changes** | Tiempo que tarda un cambio, desde el commit, en llegar a producción | Menos de una hora; entre una semana y un mes; entre un mes y seis meses |
| **Mean time to recover** | Tiempo medio necesario para restaurar el servicio después de una incidencia | Menos de una hora; menos de un día; menos de una semana |
| **Change failure rate** | Porcentaje de cambios que degradan el servicio o requieren remediación, como un parche | `0–15 %`; `31–45 %`; `16–30 %` |

> Los valores de la tabla son ejemplos de niveles observables, no una partición exhaustiva de todos los resultados posibles.
>
> La **deployment frequency** describe cuántas entregas se realizan. El **lead time** describe cuánto espera un cambio para llegar a producción. Una frecuencia alta no permite deducir por sí sola el tiempo de entrega de cada cambio.
>
> El **mean time to recover** caracteriza la rapidez con que se restablece el servicio tras un incidente. El **change failure rate** caracteriza la proporción de cambios problemáticos. Medir ambos ayuda a distinguir la aparición de fallos de la capacidad de recuperarse.

#### 16. Objectives and Key Results

> Los **Objectives and Key Results (OKR)** son un método para definir objetivos y seguir los resultados que muestran su avance. Conectan las metas de la organización, los equipos y las personas mediante resultados medibles orientados en una dirección común.
>
> El **Objective** expresa lo que se quiere conseguir. Los **Key Results** concretan cómo se comprobará el logro. La distinción ayuda a convertir una intención general en resultados que se pueden observar.
>
> El método se desarrolló en Intel y fue popularizado por John Doerr, que lo presentó en Google en 1999.

##### 16.1. Ejemplo de objetivo y resultados clave

> Para un equipo de la NFL, el objetivo ilustrativo es **generar ingresos para los propietarios**. Se presenta como una aspiración ambiciosa vinculada al negocio.
>
> Los resultados clave del ejemplo son:
>
> - **Ganar la Super Bowl**: el cumplimiento puede comprobarse.
> - **Llenar las gradas al 88 %**: establece un nivel de ocupación medible.
>
> Los resultados clave permiten evaluar avances concretos asociados al objetivo. Uno tiene un resultado binario y el otro utiliza un porcentaje.

##### 16.2. Alineamiento, motivación y seguimiento

> Los OKR aclaran qué se espera de las personas y los equipos. Su finalidad en este enfoque es orientar y coordinar el trabajo; no utilizarlos como instrumento de evaluación del rendimiento individual.
>
> Conectan objetivos más abstractos de medio y largo plazo con resultados que pueden medirse mediante KPI. Esto ayuda a mantener el foco, implicar a los equipos y hacer visible cómo contribuye cada persona a las metas de la organización.
>
> Un dashboard de seguimiento muestra los objetivos, sus resultados clave, las mediciones relevantes y las responsabilidades. Permite informar, motivar y concentrar el esfuerzo en el progreso compartido.

| Elemento | Función |
| --- | --- |
| **Métrica** | Cuantificar una observación |
| **KPI** | Seleccionar una medición relevante para evaluar el desempeño |
| **Objective** | Expresar la meta que se pretende alcanzar |
| **Key Result** | Establecer un resultado verificable que permita seguir esa meta |
| **Dashboard** | Hacer visibles las mediciones y el progreso a las personas implicadas |

### V. Observabilidad con Prometheus y Grafana

#### 17. Observar un entorno Kubernetes

> La **observabilidad** permite comprender el estado interno de un sistema a partir de las señales que produce. En Kubernetes se utilizan métricas, logs y trazas para analizar el funcionamiento de aplicaciones y recursos.
>
> Las métricas permiten seguir valores como el consumo de CPU o memoria; los logs describen eventos; las trazas relacionan las partes de una operación distribuida y sus tiempos. Combinar estas señales facilita diagnosticar problemas y optimizar recursos.
>
> **Prometheus** y **Grafana** proporcionan una combinación habitual para recoger, almacenar, consultar y visualizar métricas en un entorno como GKE. Sus responsabilidades se complementan.

#### 18. Prometheus: recogida, almacenamiento y alertas

> **Prometheus** es una herramienta de código abierto de monitorización y alertas. Recoge métricas mediante un modelo **pull**: consulta periódicamente endpoints que las exponen. Esa recogida se denomina **scraping**.
>
> Almacena las mediciones como series temporales y permite consultarlas mediante **PromQL**. Los nombres de las métricas y sus etiquetas permiten seleccionar y agrupar la información.

> [!warning] Corrección
> En el material aparece que Prometheus fue diseñado para Kubernetes, pero se inició en SoundCloud en 2012. Es una herramienta de monitorización general que se integra con Kubernetes.
> Fuente de comprobación: [Prometheus: origen y funcionamiento](https://prometheus.io/docs/introduction/overview/)

| Componente | Responsabilidad |
| --- | --- |
| **Prometheus Server** | Consultar los endpoints, almacenar las series temporales y evaluar reglas |
| **Exporters** | Exponer métricas de sistemas o componentes que se quieren monitorizar |
| **Service Discovery** | Identificar los targets o endpoints que deben consultarse |
| **Alertmanager** | Gestionar las alertas recibidas y enviarlas a canales como Slack o PagerDuty |

> Un **exporter** hace accesible la información de un componente en un formato que Prometheus pueda recoger. El descubrimiento de servicios evita mantener a mano todos los destinos de recogida en una infraestructura dinámica.
>
> Las reglas de alerta se evalúan en Prometheus. **Alertmanager** se ocupa de gestionar las alertas y sus notificaciones. Por tanto, detectar que se cumple una condición y comunicarla son responsabilidades distintas dentro del flujo.

#### 19. Integración con GKE y ServiceMonitors

> Para desplegar esta solución en GKE se puede dedicar un namespace, por ejemplo `monitoring`, y utilizar **Helm** para gestionar la instalación de sus componentes.
>
> La configuración debe permitir descubrir las aplicaciones y los componentes de Kubernetes que se observarán, como nodos y controladores. La disponibilidad de una métrica concreta depende de que exista un endpoint o exporter que la exponga y de que Prometheus lo consulte.
>
> Los **ServiceMonitors** pertenecen al modelo de configuración de **Prometheus Operator**, por lo que requieren que el Operator y sus definiciones de recursos estén instalados. No son recursos nativos que aparezcan por desplegar únicamente Kubernetes.

> Un `ServiceMonitor` utiliza selectores para identificar **Services** y especifica cómo consultar sus endpoints de métricas. Esos Services permiten acceder a las aplicaciones que se ejecutan en los pods.
>
> El flujo de preparación y recogida es:
>
> 1. Instalar los componentes de monitorización y configurar su acceso a los recursos del clúster.
> 2. Exponer métricas en aplicaciones o exporters.
> 3. Configurar el descubrimiento de los endpoints, mediante ServiceMonitors cuando se utilice el Operator.
> 4. Dejar que Prometheus consulte esos endpoints y almacene las muestras.

#### 20. Grafana: consultas, paneles y fuentes de datos

> **Grafana** permite construir dashboards interactivos con gráficos y paneles. Se conecta a fuentes de datos y consulta la información necesaria para visualizarla.
>
> Entre sus fuentes aparecen **Prometheus**, **Loki** y **Elasticsearch**. Los plugins amplían sus posibilidades de integración, incluidas las relacionadas con Kubernetes.
>
> Grafana también permite configurar alertas y notificaciones visuales o enviadas a canales como correo electrónico o Slack. Estas capacidades conviven con las de la cadena de alertas de Prometheus; la configuración determina dónde se evalúa cada condición.
>
> En la integración básica, Prometheus recoge las métricas de Kubernetes y Grafana se conecta a él como **data source**. A partir de las consultas se construyen paneles de CPU y memoria por pod, latencia HTTP o errores de las aplicaciones.

#### 21. Interpretación de consultas PromQL

> Las consultas siguientes requieren que las métricas y etiquetas utilizadas estén disponibles en Prometheus. La consulta selecciona y transforma datos existentes; no incorpora por sí sola la instrumentación que los genera.

##### 21.1. Uso de CPU en modo usuario

> `node_cpu_seconds_total` es un contador del tiempo de CPU acumulado. La etiqueta `mode="user"` selecciona el tiempo dedicado al modo usuario y `[5m]` establece una ventana de cinco minutos.

```promql
rate(node_cpu_seconds_total{mode="user"}[5m])
```

> `rate()` calcula la tasa media de incremento por segundo dentro de esa ventana. El resultado se expresa en **segundos de CPU por segundo** para cada serie seleccionada, habitualmente identificada por nodo, CPU y modo.
>
> Esta consulta representa la utilización en modo usuario de cada serie. No calcula la carga media de procesos pendientes ni suma todos los modos de CPU. Tampoco agrega por nodo: mantiene las series de entrada y sus etiquetas.

##### 21.2. Memoria utilizada por pod

> `container_memory_usage_bytes` expresa el uso de memoria de los contenedores en bytes. Se suman las series conservando como criterio de agrupación la etiqueta `pod`.

```promql
sum(container_memory_usage_bytes) by (pod)
```

> El resultado es una suma de **bytes por valor de `pod`**. Es una cantidad de memoria, no una tasa temporal.
>
> Agrupar solo por `pod` combina las series que compartan ese valor. Si existen nombres de pod iguales en distintos namespaces o clústeres dentro de los datos consultados, la agrupación no conserva esas diferencias.

##### 21.3. Tasa de errores HTTP 5xx

> `http_requests_total` cuenta peticiones HTTP. El selector `status=~"5.."` utiliza una expresión regular para seleccionar valores de estado que empiezan por `5` y tienen dos caracteres más; con etiquetas de códigos HTTP, corresponde a la familia 5xx.

```promql
sum(rate(http_requests_total{status=~"5.."}[5m]))
```

> Primero se calcula la tasa de incremento de cada contador durante cinco minutos y después se suman los resultados. `rate()` tiene en cuenta los reinicios de los contadores, por lo que se aplica antes de la agregación.
>
> El resultado es una **tasa de peticiones con error 5xx por segundo**, agregada sobre todas las series seleccionadas. No es un porcentaje de errores, porque no se divide entre el total de peticiones. La suma sin agrupación elimina las diferencias entre las etiquetas de esas series.

#### 22. Crear un dashboard en Grafana

> Para visualizar estas métricas, Grafana necesita poder conectarse al servidor Prometheus y este debe contener las muestras correspondientes.
>
> El procedimiento es:
>
> 1. Configurar una **Data Source** de tipo Prometheus con la dirección del servidor accesible desde Grafana.
> 2. Crear un panel y seleccionar esa fuente.
> 3. Escribir la consulta PromQL que represente la información que se desea observar.
> 4. Ajustar el gráfico y sus unidades para que el resultado sea interpretable.
> 5. Configurar las alertas necesarias para avisar de las condiciones relevantes.
>
> La representación debe respetar lo que devuelve la consulta. Por ejemplo, una suma de memoria se muestra como cantidad de bytes y una tasa de errores como peticiones por segundo. La ventana de `rate()` y el periodo visible del dashboard son parámetros diferentes.

### VI. Herramientas de Google Cloud para evaluar la operación

#### 23. Google Cloud Operations Suite

> **Google Cloud Operations Suite**, anteriormente conocida como **Stackdriver**, reúne herramientas de métricas, logs y trazas para seguir la operación de sistemas y aplicaciones. Sus servicios permiten pasar de observar un síntoma a investigar dónde se produce y qué parte del código está implicada.

| Servicio | Información o tarea principal |
| --- | --- |
| **Cloud Monitoring** | Métricas, dashboards y alertas |
| **Cloud Logging** | Recogida, almacenamiento y análisis de logs |
| **Cloud Trace** | Trazas distribuidas y análisis de latencia |
| **Cloud Profiler** | Perfiles de consumo de recursos del código |
| **Cloud Debugger** | Inspección histórica del estado y las variables en producción; servicio retirado |

> Estas herramientas cubren niveles distintos del diagnóstico. Monitoring muestra la evolución del servicio, Logging proporciona eventos, Trace sigue operaciones entre componentes y Profiler ayuda a identificar funciones que consumen recursos.

#### 24. Cloud Monitoring y Cloud Logging

##### 24.1. Métricas y alertas con Cloud Monitoring

> **Cloud Monitoring** permite recoger métricas de servicios como **GKE**, **Compute Engine** y **Cloud Functions**, crear dashboards y configurar alertas.
>
> El seguimiento también puede incluir entornos híbridos o recursos alojados en AWS mediante la integración o instrumentación correspondiente. Los recursos deben enviar sus señales al sistema de monitorización; estar fuera de Google Cloud no significa que sus métricas se recojan automáticamente.
>
> Las vistas de rendimiento y consumo ayudan a detectar incidencias y a decidir cómo utilizar los recursos. Las alertas automatizan el aviso cuando se cumplen las condiciones configuradas.

##### 24.2. Eventos y búsqueda con Cloud Logging

> **Cloud Logging** permite recopilar, almacenar y analizar logs. Se pueden buscar eventos, filtrar por sus campos y configurar alertas basadas en ellos.
>
> También admite integraciones con herramientas **SIEM** para el análisis de información y eventos de seguridad. Los logs estructurados facilitan esas consultas porque conservan campos sobre la acción, el actor, el tiempo y el entorno.
>
> Monitoring y Logging aportan perspectivas complementarias: una métrica puede revelar que aumentan los errores y los registros permiten investigar qué operaciones están fallando.

#### 25. Cloud Trace y el recorrido de una petición

> **Cloud Trace** sigue operaciones distribuidas para identificar cuellos de botella y analizar la latencia. La visualización permite observar cómo se reparte el tiempo entre las partes de una petición, por ejemplo una operación HTTP que atraviesa varios servicios.
>
> Se integra con **OpenTelemetry** para instrumentar y recoger trazas. La correlación entre las partes de una operación permite investigar el recorrido completo, además de observar cada componente por separado.
>
> Trace resulta útil cuando el tiempo total de respuesta aumenta y es necesario localizar qué tramo contribuye al retraso.

#### 26. Cloud Profiler y el consumo dentro del código

> **Cloud Profiler** analiza el consumo de CPU y memoria de las aplicaciones en producción mediante perfiles. Ayuda a identificar funciones que afectan al rendimiento y a orientar la optimización del código.
>
> Su muestreo está diseñado para introducir una **sobrecarga reducida**, de modo que se pueda estudiar el comportamiento de la aplicación durante su funcionamiento habitual.

> [!warning] Corrección
> En el material aparece que Cloud Profiler funciona sin impacto en el rendimiento, pero la documentación describe una sobrecarga baja de recogida de perfiles, no un impacto estrictamente nulo.
> Fuente de comprobación: [Google Cloud: funcionamiento e impacto de Cloud Profiler](https://docs.cloud.google.com/profiler/docs/about-profiler)

![[imgs/apuntes-72c6f8347543-p0055-469da2a49f70.png]]

> El **flame graph** muestra una jerarquía de llamadas. Cada bloque representa una función y su anchura corresponde al consumo atribuido a esa función, incluidas sus llamadas descendientes, para la métrica seleccionada.
>
> En la figura se ha seleccionado **CPU time**. Las ramas anchas ayudan a localizar recorridos que concentran una parte relevante del tiempo de CPU. El eje horizontal distribuye ese consumo entre ramas; no representa una cronología de ejecución.
>
> Al comparar los perfiles se puede decidir qué funciones merece la pena investigar. Los colores distinguen grupos de funciones y no deben interpretarse por sí solos como una escala de gravedad.

#### 27. Cloud Debugger como herramienta histórica

> **Cloud Debugger** permitía inspeccionar el estado y las variables de aplicaciones en producción sin detener su ejecución. Utilizaba snapshots del estado para investigar problemas en entornos reales.
>
> Entre los lenguajes asociados a esta herramienta aparecen **Java**, **Python**, **Node.js** y **Go**. Su propósito era acercar el diagnóstico a la situación concreta que estaba experimentando una aplicación desplegada.

> [!warning] Corrección
> En el material aparece Cloud Debugger como servicio disponible, pero fue declarado obsoleto el 16 de mayo de 2022 y retirado el 31 de mayo de 2023. Sus capacidades se describen aquí como parte histórica de la suite.
> Fuente de comprobación: [Google Cloud: retirada de Cloud Debugger](https://docs.cloud.google.com/stackdriver/docs/deprecations/debugger-deprecation?hl=en)

#### 28. Beneficios de una plataforma integrada

> Una plataforma integrada centraliza la información procedente de varios entornos y facilita relacionar las señales durante la investigación de una incidencia.
>
> Entre los beneficios están:
>
> - **Visibilidad conjunta** de entornos cloud, híbridos y locales cuando se configuran las integraciones necesarias.
> - **Detección y aviso de incidentes** mediante alertas automatizadas.
> - **Escalabilidad de los servicios gestionados**, que evita desplegar y operar una infraestructura propia para esos servicios.
> - **Integración con otras herramientas**, como Prometheus, Grafana o Elastic Stack.
>
> La plataforma aporta el soporte de recogida y análisis, pero el equipo sigue teniendo que seleccionar las señales, configurar sus fuentes e interpretar los resultados. Esa interpretación completa el retorno de información hacia las decisiones de operación, desarrollo y negocio.

### VII. Resumen Final

> La evaluación en DevOps conecta lo que ocurre en producción con las decisiones sobre el producto. La telemetría alimenta un circuito de realimentación que permite contrastar hipótesis y mejorar el sistema.
>
> La monitorización combina disponibilidad, recursos y tendencias. En una infraestructura dinámica necesita descubrimiento automático, capacidad de escalar y alertas que conduzcan a una respuesta del equipo adecuado.
>
> Los dashboards hacen visibles los datos; el APM ayuda a investigar el rendimiento; los logs estructurados permiten reconstruir eventos mediante qué, quién, cuándo, dónde y por qué. Agregar registros aporta contexto sobre la actividad del conjunto.
>
> Los KPI seleccionan mediciones relevantes y los OKR vinculan objetivos con resultados verificables. Los indicadores de entrega y recuperación deben leerse conjuntamente para relacionar rapidez y estabilidad.
>
> Prometheus recoge y consulta métricas, Alertmanager gestiona sus notificaciones y Grafana construye visualizaciones. La interpretación de PromQL exige distinguir cantidades de memoria, tasas por segundo y porcentajes.
>
> Monitoring, Logging, Trace y Profiler aportan vistas complementarias de la operación en Google Cloud. Su información resulta útil cuando conduce a comprender el problema y orientar el siguiente cambio.
