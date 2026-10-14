---
estado: pendiente de revisión
---

### I. Negocio y desconexión entre equipos

#### 1. Objetivos y desafíos del negocio

> La actividad de TI forma parte del funcionamiento del negocio: una aplicación aporta valor cuando puede entregarse, utilizarse y mantenerse de manera fiable. En una empresa con fines de lucro, ese valor debe contribuir a su objetivo económico.
>
> Los desafíos combinan exigencias que deben satisfacerse conjuntamente:

| Desafío | Consecuencia para la entrega de software |
| --- | --- |
| **Competitividad** | Responder a las necesidades del mercado y del cliente. |
| **Time-to-market** | Reducir el tiempo entre una idea y su disponibilidad para los usuarios. |
| **Calidad desde la entrega** | Evitar que la rapidez se traduzca en fallos que comprometan el servicio. |
| **Reducción de costes** | Disminuir esfuerzo repetido, correcciones e intervenciones manuales. |
| **Minimización de riesgos** | Controlar las consecuencias de cambios, incidencias y dependencias. |

> Una entrega rápida pierde parte de su valor si genera errores, interrupciones o costes de mantenimiento elevados. Por ello, el proceso completo debe considerar tanto las nuevas funcionalidades como la operación del servicio.
>
> La **disponibilidad**, expresada como porcentaje de *uptime* —por ejemplo, 99,9 %—, ilustra una dimensión operativa que debe observarse junto con los resultados del negocio.

#### 2. Problemas del modelo tradicional

> Cuando cada equipo trabaja con sus propios objetivos e información, los problemas se trasladan de una etapa a otra. El resultado es una cadena de entregas parciales en la que nadie dispone de una visión suficiente del conjunto.

##### 2.1. Desarrollo

> El desarrollador puede recibir **especificaciones poco definidas**, plazos cortos y presión para entregar. Si el código contiene defectos y pasa a producción, esos defectos también llegan al servicio.
>
> La falta de tiempo para pruebas y documentación, el desconocimiento de las incidencias reales y la ausencia de un entorno de pruebas representativo de producción aumentan la distancia entre lo que se desarrolla y lo que finalmente se opera.
>
> El problema organizativo aparece cuando entregar código se considera el final de la responsabilidad de desarrollo, aunque el comportamiento del sistema todavía no se haya comprobado en condiciones relevantes.

##### 2.2. Operaciones

> **Operaciones** mantiene vivo el entorno de producción: administra y protege sus recursos, investiga problemas y procura mantener el servicio disponible. Debe responder a incidencias internas y externas que no siempre estaban previstas.
>
> Su trabajo incluye determinar causas, comunicar lo ocurrido y resolverlo cuando sea posible. Si predominan las urgencias, el equipo queda en una dinámica de **trabajo reactivo**, dedicando gran parte de su capacidad a restablecer el funcionamiento.
>
> El trabajo no planificado reduce el tiempo disponible para las mejoras previstas. Una incidencia recurrente afecta, por tanto, al servicio actual y al avance de cambios futuros.

##### 2.3. Quality Assurance

> **QA (Quality Assurance)** necesita criterios claros para comprobar la calidad del código producido por otros. La verificación se dificulta cuando faltan especificaciones funcionales o pruebas de aceptación, cuando el código llega demasiado tarde o cuando no existe un criterio compartido para clasificar un error como crítico.
>
> Si las decisiones de negocio no tienen en cuenta a QA, se exige calidad sin reservar la información y el tiempo necesarios para evaluarla. La comprobación queda relegada al final, cuando corregir puede implicar retrasar toda la entrega.

##### 2.4. Seguridad y redes

> Los equipos de **Seguridad y Redes** permiten que los datos circulen a través de la infraestructura y protegen el entorno de producción. Sus necesidades afectan a puertos, tráfico, cifrado, controles de acceso, protección de datos y auditorías.
>
> Si no participan durante el desarrollo, esas condiciones pueden descubrirse cuando la aplicación ya está construida. Involucrarlos desde el principio permite incorporar los requisitos operativos y de seguridad a las decisiones de diseño y entrega.

##### 2.5. Responsables de producto y proyecto

> Los responsables de producto o proyecto definen la **hoja de ruta** y gestionan retrasos, recortes, ampliaciones de alcance y otras restricciones que afectan al producto.
>
> Deben atender demandas y quejas de distintos niveles de la organización, coordinar personas y procesos y procurar superar las restricciones del negocio. Esa presión requiere una visión compartida de prioridades, dependencias y capacidad real de los equipos.

#### 3. Impacto conjunto de los silos

> Los **silos** favorecen los prejuicios entre funciones: cada grupo puede percibirse como imprescindible y atribuir las dificultades a los demás. La relación entre negocio y TI se vuelve conflictiva si se discuten responsabilidades sin atender al resultado común.
>
> Un problema en TI puede convertirse en un problema de todo el negocio. Por ejemplo, una funcionalidad terminada pero imposible de desplegar todavía no está disponible para el cliente. La productividad de un equipo aislado no basta para valorar la entrega completa.

### II. Cultura DevOps

#### 4. Colaboración y responsabilidad compartida

> **DevOps** responde a la desconexión tradicional entre desarrollo y operaciones. Es una cultura y una forma de trabajo que enfatiza la **colaboración y comunicación** entre profesionales de TI, junto con la automatización de la entrega de software y los cambios de infraestructura.
>
> Su objetivo es crear un entorno en el que construir, probar y liberar software sea más **rápido, frecuente y fiable**. Aunque su nombre destaca *Development* y *Operations*, incluye QA, seguridad, redes, gestión y negocio.
>
> La colaboración necesita continuidad: formar un grupo inicia la relación, mantenerlo permite avanzar y trabajar conjuntamente permite alcanzar resultados. En la práctica supone compartir información, objetivos y responsabilidad sobre el servicio, desde la idea hasta su operación.
>
> La comunicación debe atravesar las barreras entre equipos. Una incidencia de producción aporta información a desarrollo; un cambio previsto debe ser conocido por quienes lo probarán, asegurarán y operarán. Así, las decisiones se toman con una comprensión más completa de sus consecuencias.

#### 5. Agile en desarrollo y operaciones

> **Agile** aporta una orientación al cambio mediante trabajo iterativo y retroalimentación. Aplicarla al desarrollo y a las operaciones facilita ajustar las entregas a necesidades reales y preparar el entorno en el que se ejecutarán.
>
> La relación conceptual es **Agile Development + Agile Operations → Continuous Delivery**: para entregar con continuidad, el desarrollo ágil debe acompañarse de una operación capaz de absorber y verificar los cambios.
>
> **Continuous Delivery**, o entrega continua, busca mantener el software en condiciones de ser liberado de manera fiable. La decisión de liberar y la automatización completa del despliegue son aspectos que se definen dentro del proceso; preparar una entrega y desplegarla son actividades relacionadas, pero diferentes.
>
> El ciclo general conecta **idea → planificación → entrega → implementación → monitorización**. Dentro de él se repiten actividades de construcción, despliegue, pruebas, promoción a otros entornos y nuevas comprobaciones. Los resultados de operación alimentan las decisiones posteriores.
>
> Ese ciclo se apoya en **cultura y procesos**, **tecnología y herramientas** y **técnicas DevOps**. A su vez, debe integrar financiación, gobierno de procesos, cumplimiento, políticas de liberación y estándares operativos. La entrega continua es una capacidad del conjunto de la organización.

#### 6. Cultura del cambio: personas, procesos y herramientas

##### 6.1. Infraestructura y monitorización

> La infraestructura evoluciona desde centros de datos gestionados de manera tradicional hacia una **infraestructura definida por software**. Cloud computing, contenedores y OpenTofu permiten expresar y automatizar cambios de recursos.
>
> También se amplía el enfoque de la **monitorización de sistemas** a la **monitorización del negocio**. Conocer el estado de hosts y servicios ayuda a detectar fallos técnicos; relacionarlo con indicadores como visitas, adquisición de usuarios o resultados de campañas permite comprender sus efectos sobre la actividad.
>
> Las métricas técnicas y de negocio aportan información complementaria. Un sistema disponible debe seguir evaluándose por el servicio que presta y el resultado que obtiene el usuario.

##### 6.2. Prioridad de las personas

> La prioridad cultural se expresa como **People over processes over tools**: las personas y su colaboración orientan los procesos, y estos dan sentido a las herramientas.
>
> Las prácticas y herramientas deben apoyar una forma de trabajo compartida:

| Dimensión | Elementos |
| --- | --- |
| **Personas** | Comunicación, objetivos comunes, responsabilidad compartida, innovación, habilidades cruzadas, cultura sin culpas y colaboración negocio–TI. |
| **Procesos** | Automatización, integración continua, entrega continua, monitorización continua, infraestructura como código y gestión de configuración. |
| **Herramientas** | Kubernetes, Git, ArgoCD, Jenkins, Sonar, Nexus, JUnit, OpenTofu, CDK, Ansible, Splunk, Grafana y Prometheus. |

> Las **habilidades cruzadas** ayudan a comprender el trabajo de otras funciones y sus restricciones. La **cultura sin culpas** favorece examinar causas y mejorar el sistema tras un fallo, manteniendo la responsabilidad compartida por la mejora.
>
> El proceso organiza cómo se trabaja y la herramienta permite ejecutarlo con mayor consistencia. Por ejemplo, automatizar una comprobación resulta útil cuando existe un criterio claro de aceptación y alguien puede interpretar y atender su resultado.

### III. Los Tres Caminos

> Los **Tres Caminos (The Three Ways)** organizan los principios de DevOps alrededor del flujo de valor, la retroalimentación y el aprendizaje. Permiten relacionar la cultura de trabajo con el rendimiento del negocio.

#### 7. Primer Camino: pensamiento sistémico

> El **Primer Camino**, *Systems Thinking*, enfatiza el rendimiento de **todo el sistema**. Las cadenas de valor del negocio están habilitadas por TI, por lo que el flujo debe comprenderse desde la necesidad inicial hasta el cliente.
>
> Su representación va de **Dev hacia Ops**, conectando el trabajo de desarrollo con la entrega y operación. Cada etapa debe contribuir al resultado global y evitar transferir errores al siguiente centro de trabajo.
>
> Los resultados buscados son:
>
> - **Calidad en cada etapa**: detectar y atender problemas antes de que se propaguen.
> - **Optimización global**: mejorar el rendimiento de la cadena completa y sus restricciones.
>
> Por ejemplo, incrementar la cantidad de código terminado no acelera necesariamente la entrega si QA no dispone de tiempo para probarlo o si existe una espera prolongada para desplegarlo. Identificar el **cuello de botella** permite actuar sobre la limitación que afecta al conjunto.

#### 8. Segundo Camino: ampliar los bucles de retroalimentación

> El **Segundo Camino**, *Amplify Feedback Loops*, refuerza la información que vuelve desde la operación y el uso real hacia quienes desarrollan y toman decisiones. El flujo de entrega se completa con un **bucle de retorno de Ops a Dev**.
>
> Los datos valiosos proceden del mundo real: errores, métricas y necesidades de los usuarios permiten evaluar si lo entregado se comporta como se esperaba. Cuanto más rápido llega esa información y se responde a ella, más rápido pueden corregirse los problemas.
>
> Sus resultados son:
>
> - Comprender y responder mejor a las **necesidades de los clientes**.
> - Ampliar el conocimiento compartido y el impacto de la información mediante **bucles de retroalimentación**.
>
> Por ejemplo, si una modificación empeora el rendimiento en producción, esa información debe llegar al equipo que puede investigarla y corregirla. Registrar una métrica sin incorporarla a las decisiones deja incompleto el ciclo.

#### 9. Tercer Camino: experimentación y aprendizaje continuos

> El **Tercer Camino**, *Culture of Continual Experimentation and Learning*, promueve aprender y experimentar de manera continua. La repetición y la práctica permiten dominar tanto la entrega como la respuesta a problemas.
>
> Busca pasar de una fase de **supervivencia**, dominada por urgencias, a una fase de **aprendizaje y autoorganización**. Las experiencias y resultados se utilizan para modificar cómo trabaja el equipo y reforzar la **resiliencia del producto**.
>
> Experimentar implica comprobar una hipótesis y aprender del resultado. Practicar repetidamente una actividad, como el despliegue o la recuperación ante fallos, permite encontrar dificultades y mejorar la capacidad para ejecutarla.

#### 10. Relación entre los Tres Caminos

> Los tres principios se refuerzan: el flujo lleva valor al usuario, la retroalimentación informa sobre el resultado y el aprendizaje mejora el sistema para las siguientes entregas. La figura reúne el flujo directo, el retorno de información y las iteraciones de experimentación.

![[apuntes-c6d5a3f633df-p0024-fe6b9154c1d7.png]]

> La flecha inferior representa el avance de Dev a Ops; la flecha exterior devuelve información; los bucles pequeños representan la experimentación repetida. Las iteraciones permiten mejorar el flujo completo a partir de la experiencia.

| Camino | Pregunta que orienta la mejora | Resultado buscado |
| --- | --- | --- |
| **Primero: sistema completo** | ¿Cómo avanza el valor hasta el cliente y dónde se limita? | Rendimiento global y reducción de errores transferidos. |
| **Segundo: retroalimentación** | ¿Qué ocurre realmente y con qué rapidez llega esa información? | Mejor respuesta al cliente y correcciones más rápidas. |
| **Tercero: aprendizaje** | ¿Qué podemos experimentar y practicar para mejorar? | Autoorganización y mayor resiliencia. |

### IV. Shift-Left y Shift-Right

#### 11. Validaciones a lo largo del ciclo

> **Shift-Left** y **Shift-Right** sitúan las validaciones en diferentes momentos del ciclo de desarrollo y operación. Ambos persiguen mejorar **calidad, seguridad y rendimiento**, favoreciendo la entrega continua y la resiliencia.
>
> Si se representa el ciclo de izquierda a derecha, se evalúan requisitos, código nuevo, cada *build*, cada despliegue y el comportamiento en producción. Shift-Left adelanta comprobaciones hacia las fases iniciales; Shift-Right utiliza pruebas y observación sobre el servicio desplegado.

#### 12. Shift-Left: prevención temprana

##### 12.1. Objetivo y beneficios

> **Shift-Left** mueve las validaciones hacia fases iniciales del desarrollo. Se aplica a pruebas, seguridad y calidad del código para encontrar problemas cuando todavía pueden corregirse antes de propagarse.
>
> Un ejemplo es **ejecutar pruebas unitarias en cada commit**. Cada cambio recibe información temprana sobre si conserva el comportamiento esperado.
>
> Los beneficios son la detección temprana de errores y vulnerabilidades, un menor coste de fallos en producción y un feedback más rápido a los desarrolladores. La integración con CI/CD y la automatización hacen que esas comprobaciones sean repetibles.
>
> En la figura, la flecha señala el desplazamiento hacia las actividades de desarrollo. El ciclo mantiene las pruebas a lo largo de sus etapas, mientras refuerza su realización temprana.

![[apuntes-c6d5a3f633df-p0026-b6b512103550.png]]

##### 12.2. Técnicas de implementación

| Técnica | Aplicación |
| --- | --- |
| **Pruebas tempranas** | Pruebas unitarias y de integración, junto con análisis estático. |
| **Security as Code** | Análisis de dependencias y escaneo del código integrados en el proceso. |
| **Infraestructura como código** | Validaciones automáticas de las configuraciones de infraestructura. |
| **Pipelines CI/CD** | Comprobación continua de cambios con herramientas como GitHub Actions, Jenkins o GitLab CI. |

> Las pruebas unitarias comprueban unidades de comportamiento; las de integración examinan su interacción; el análisis estático revisa el código sin ejecutar la aplicación. Estas comprobaciones aportan información distinta y pueden combinarse en el pipeline.
>
> La infraestructura y las dependencias también forman parte del entorno que se entregará. Incluirlas en las validaciones tempranas amplía la prevención más allá del código de la aplicación.

#### 13. Shift-Right: validación en producción

##### 13.1. Objetivo y beneficios

> **Shift-Right** se centra en la validación y la **observabilidad en producción**. Utiliza información del entorno real, pruebas en vivo y simulación de fallos para evaluar el servicio que recibe el usuario y mejorar su resiliencia.
>
> Un ejemplo son las **pruebas A/B** en un servicio desplegado: distintas variantes se comparan mediante resultados observados en usuarios. Ese conocimiento procede del uso real.
>
> Los beneficios incluyen detectar problemas propios del entorno de producción, identificar degradaciones de rendimiento y obtener feedback real de usuarios y métricas clave. Este enfoque también es aplicable en **SRE (Site Reliability Engineering)**, orientado a la fiabilidad de los servicios.
>
> La figura desplaza la atención hacia las actividades de operación y su efecto sobre el usuario. La información recogida debe volver al proceso de mejora.

![[apuntes-c6d5a3f633df-p0029-6989734a3d3b.png]]

##### 13.2. Técnicas de implementación

| Técnica | Propósito |
| --- | --- |
| **Canary Releases** | Desplegar un cambio a un subconjunto de usuarios y observar su comportamiento. |
| **Feature Flags** | Activar o desactivar funcionalidades dinámicamente para controlar su disponibilidad. |
| **Chaos Engineering** | Simular fallos para evaluar la respuesta del sistema, con herramientas como Gremlin. |
| **Observabilidad** | Recoger y analizar logs, métricas y tracing para comprender el servicio. |

> **Canary Releases** controla el alcance inicial de una entrega; las **Feature Flags** controlan la activación de funcionalidades. Son mecanismos que pueden complementarse, pero actúan sobre aspectos distintos.
>
> Los **logs** registran eventos, las **métricas** describen magnitudes observables y el **tracing** permite seguir una petición a través de componentes. Prometheus y OpenTelemetry forman parte de las herramientas utilizadas para instrumentar y observar el entorno.
>
> La simulación de fallos aporta información sobre cómo responde el servicio. El objetivo de observar y experimentar es detectar y mitigar problemas y mejorar la experiencia de usuario mediante lo aprendido.

#### 14. Complementariedad e integración con CI/CD

| Característica | Shift-Left | Shift-Right |
| --- | --- | --- |
| **Enfoque** | Desarrollo. | Producción. |
| **Objetivo** | Prevenir fallos y detectarlos temprano. | Detectar y mitigar problemas en el entorno real. |
| **Prácticas representativas** | Pruebas unitarias y análisis estático. | Monitorización y Chaos Engineering. |
| **Impacto en DevOps** | Agilidad y calidad. | Resiliencia y experiencia de usuario. |

> **Shift-Left** mejora la calidad desde el inicio y **Shift-Right** mejora la estabilidad y resiliencia durante la operación. Su combinación permite comprobar cambios antes de entregarlos y aprender de su comportamiento real.
>
> La **automatización** y la integración con **CI/CD** conectan esas comprobaciones con el flujo de trabajo. El feedback temprano ayuda a corregir el cambio; el feedback de producción orienta nuevas correcciones y mejoras. Así, ambos enfoques refuerzan los Tres Caminos.

### V. Principios para una cultura DevOps

#### 15. Trabajo, personas y mejora continua

##### 15.1. Producción y flujo de trabajo

> **Monitorización desde producción**: operar un servicio exige conocer su comportamiento. La monitorización forma parte de su puesta en producción.
>
> **Control del trabajo no planificado**: las urgencias consumen capacidad destinada a tareas previstas. Conviene identificar qué problemas interrumpen el flujo y qué restricciones actúan como cuellos de botella.
>
> **Requisitos operativos y funcionales**: ambos tienen importancia para el producto. El comportamiento solicitado debe acompañarse de condiciones que permitan desplegar, mantener y observar el servicio.
>
> **Entrega efectiva**: el trabajo debe llegar a quienes lo utilizarán. Entregar, integrar y practicar los despliegues permite mejorar una actividad esencial del proceso.

##### 15.2. Personas, procesos y aprendizaje compartido

> **Responsabilidad conjunta**: negocio, desarrollo, operaciones y las demás funciones participan en un mismo resultado. Esa participación se extiende a gestión, administración, ventas, diseño y otros trabajos que sostienen la organización.
>
> **Atención a las incidencias**: la responsabilidad por el servicio se comparte, incluida la coordinación ante avisos y guardias —*pager duty*—. La colaboración requiere conocer los problemas que afectan a otros equipos.
>
> **Personas y utilidad para el negocio**: denominaciones como DevOps, NoOps o Devs & Ops no sustituyen una colaboración efectiva. La filosofía o marco elegido debe permitir trabajar mejor y hacer más eficiente al negocio.
>
> **Procesos útiles y comunicación continua**: los procesos organizan el trabajo; la comunicación mantiene a las personas conectadas con las necesidades y consecuencias de sus acciones.
>
> **Aprendizaje también en la dirección**: compartir marcos de comprensión facilita que equipos y responsables apoyen la misma mejora. Lecturas como *The Phoenix Project*, *The Goal*, *Critical Chain* y *The DevOps Handbook* sirven como referencias de aprendizaje; involucrar a la dirección en ese aprendizaje favorece una visión común.

##### 15.3. Práctica y automatización

> **Integración continua**: comprobar con frecuencia cómo encajan los cambios ayuda a descubrir lo que puede romperse al combinarlos.
>
> **Práctica frecuente del despliegue**: desplegar es un proceso clave que mejora con la repetición. La práctica permite detectar dificultades y hacer la entrega más fiable.
>
> **Automatización sistemática**: automatizar las actividades repetibles reduce trabajo manual y favorece consistencia. Su valor aumenta cuando se aplica a procesos comprendidos, con resultados que se pueden verificar.
>
> Estas prácticas deben acompañarse de comunicación continua, identificación de cuellos de botella y aprendizaje sobre lo que ocurre realmente en el servicio.

### VI. Resumen Final

> **DevOps** conecta la entrega de software con el funcionamiento del negocio mediante colaboración, comunicación, responsabilidad compartida y automatización. El alcance incluye desarrollo, operaciones, QA, seguridad, redes, gestión y negocio.
>
> La prioridad **personas → procesos → herramientas** orienta el cambio cultural. La infraestructura definida por software y la monitorización técnica y de negocio apoyan una entrega más frecuente y fiable.
>
> Los **Tres Caminos** relacionan rendimiento global, retroalimentación rápida y experimentación continua. Mejorar el flujo, conocer sus resultados y aprender de ellos permite avanzar desde el trabajo reactivo hacia una mayor autoorganización y resiliencia.
>
> **Shift-Left** adelanta pruebas y validaciones para prevenir problemas; **Shift-Right** observa y evalúa el servicio en producción. Ambos enfoques se complementan mediante automatización, CI/CD y retorno de información.
>
> La mejora exige atender los requisitos operativos, limitar el impacto del trabajo no planificado, identificar cuellos de botella y practicar integración, despliegue y comunicación de manera continua.

