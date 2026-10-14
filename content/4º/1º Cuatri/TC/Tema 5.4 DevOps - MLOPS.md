---
estado: pendiente de revisión
---

### I. From DevOps to MLOps

#### 1. Operationalizing machine learning

> **Machine Learning Operations (MLOps)** reúne prácticas que coordinan el desarrollo de modelos de machine learning y la operación de los sistemas que los utilizan. Abarca desarrollar, desplegar, monitorizar y mantener modelos de forma eficiente y fiable.
>
> MLOps toma principios de **DevOps**, pero incorpora las necesidades del ciclo de vida de los datos y los modelos. DevOps favorece la colaboración entre desarrollo e infraestructura y la estabilidad de producción; MLOps añade la experimentación, el entrenamiento, la validación y el seguimiento del comportamiento predictivo.
>
> **Operationalize AI** significa integrar capacidades de inteligencia artificial en las operaciones cotidianas de una organización. El objetivo es llevar los modelos desde la experimentación hasta aplicaciones que contribuyan a las metas del negocio.
>
> Un modelo entrenado es una parte de ese sistema. Para utilizarlo de forma estable hacen falta datos adecuados, software que lo integre, infraestructura, despliegue y monitorización. Por ello, los equipos DevOps mantienen un papel esencial dentro de MLOps.

#### 2. Lifecycle and conceptual architecture

> El ciclo general comienza con la definición de objetivos, continúa con la recogida y preparación de datos, el desarrollo o ajuste del modelo y su integración en una aplicación, y termina con su monitorización y gestión.
>
> La monitorización proporciona información para revisar los objetivos y mejorar el modelo. El recorrido es iterativo: las condiciones de producción pueden cambiar y exigir nuevas decisiones sobre datos, entrenamiento o integración.

![[imgs/apuntes-5779b8d8cb73-p0006-71dcf465c89d.png]]

> La arquitectura conceptual distingue cuatro áreas funcionales sobre una plataforma e infraestructura comunes:
>
> - **Gather and prepare data:** almacenamiento, data lakes, exploración, preparación y procesamiento de flujos de datos.
> - **Develop model:** notebooks y librerías de ML para experimentar y construir modelos.
> - **Deploy models in an application:** gestión del ciclo de vida y procesos CI/CD para incorporar los modelos a aplicaciones.
> - **Model monitoring and management:** monitorización, alertas, visualización y seguimiento del drift.
>
> La plataforma puede ofrecer capacidades de **autoservicio** en entornos híbridos o multicloud, permitiendo que los equipos soliciten las herramientas y recursos que necesitan. La aceleración de cómputo sostiene las cargas que requieren más capacidad.
>
> La infraestructura subyacente puede ser física, virtual, cloud privada, cloud pública o **edge**. La separación por capas ayuda a distinguir el trabajo sobre datos y modelos de los servicios de plataforma que lo hacen posible.

#### 3. DevOps, GitOps and organizational change

> MLOps incorpora **DevOps y GitOps** para mejorar la gestión del ciclo de vida de la aplicación de ML. En un ciclo de entrega se entrena y valida el modelo, se desarrolla el código de aplicación, se construye y prueba el sistema y se ofrece el modelo para inferencia.
>
> Después del serving, la monitorización y la detección de drift o valores atípicos pueden motivar cambios en el código de ML y un nuevo entrenamiento. La entrega y el aprendizaje sobre producción forman un circuito continuo.

| Principio | Aplicación a MLOps |
| --- | --- |
| **Cross-functional collaboration** | Coordinar perfiles que trabajan sobre negocio, datos, modelos, aplicaciones e infraestructura |
| **Git as Single Source of Truth** | Mantener una referencia compartida y versionada del código y de las definiciones declarativas |
| **Repeatability** | Poder repetir los procesos con sus entradas y configuración identificadas |
| **Automation** | Automatizar pasos del entrenamiento, validación, construcción y entrega |
| **Security** | Incorporar controles sobre software, accesos y despliegues |
| **Observability** | Obtener información que permita interpretar el comportamiento en producción |

> Utilizar Git como referencia no exige guardar dentro del repositorio todos los datasets o artefactos de los modelos. El código y las configuraciones pueden referenciar versiones de datos y modelos almacenadas en los sistemas apropiados.
>
> Adoptar MLOps requiere cambios organizativos:
>
> - **Equipos multidisciplinares:** formar a sus integrantes en los fundamentos de las áreas con las que colaboran.
> - **Automatización:** automatizar las tareas que puedan realizarse de forma sistemática.
> - **Paciencia:** avanzar gradualmente; una plataforma y una forma de trabajo compartida necesitan tiempo.
> - **Métricas y transparencia:** combinar la medición y el seguimiento con la visibilidad de los resultados.
>
> La repetibilidad depende del código, los datos, el entorno y la configuración utilizados. Automatizar el proceso ayuda a controlarlos, aunque no convierte cualquier entrenamiento en un cálculo estrictamente determinista.

### II. People, Collaboration and Operational Responsibility

#### 4. Roles across the lifecycle

> Poner un modelo en producción requiere la colaboración de varios perfiles. Su participación se solapa porque desarrollar el modelo, integrarlo y operarlo implica decisiones compartidas.

| Perfil | Participación principal en el ciclo |
| --- | --- |
| **Business leadership** | Definir objetivos |
| **Data engineer** | Recoger y preparar datos |
| **Data scientist** | Desarrollar modelos y estudiar su comportamiento durante la monitorización |
| **ML engineer** | Participar desde el desarrollo del modelo hasta su integración, monitorización y gestión |
| **App developer** | Integrar el modelo en la aplicación y mantener esa integración |
| **IT operations** | Sostener la operación desde la preparación de datos hasta la gestión del sistema desplegado |

> Esta distribución indica focos de trabajo y no fronteras rígidas. Los modelos, la aplicación, los datos y la ingeniería de datos forman partes interdependientes del sistema.
>
> El **data engineer** se ocupa de extraer y entregar datos preparados para su procesamiento. El **app developer** integra las predicciones en la lógica de la aplicación. Ambos necesitan entender los requisitos de quienes producen y consumen esa información.

#### 5. Data scientists and model behavior

> Los **data scientists** experimentan con algoritmos y técnicas para crear modelos capaces de predecir, clasificar o extraer información de los datos. Su pregunta central es cómo utilizar los datos disponibles para entrenar un modelo que resuelva el problema planteado.
>
> MLOps les proporciona un entorno controlado y flexible para construir prototipos, probarlos e iterar. También facilita que el modelo pase a producción, escale y conserve un comportamiento predictivo adecuado.
>
> La información del mundo real permite estudiar los casos que el modelo encuentra después del despliegue. Entre ellos pueden aparecer **datos adversarios**, diseñados para confundirlo e inducir predicciones perjudiciales.
>
> Esos casos pueden utilizarse para evaluar su robustez y orientar un reentrenamiento. Para incorporarlos al entrenamiento es necesario controlar su calidad y disponer de la respuesta correcta: añadir entradas maliciosas indiscriminadamente no garantiza una mejora.

#### 6. Machine learning engineers and the wall of confusion

> Los **Machine Learning Engineers (MLEs)** conectan los prototipos de ciencia de datos con sistemas preparados para producción. Optimizan modelos, los incorporan a software mantenible y los integran con la infraestructura existente.
>
> El control de versiones, CI/CD y la monitorización les ayudan a conseguir modelos desplegables, escalables y mantenibles. Una cuestión esencial para este perfil es cómo utilizará la aplicación el modelo.

> La **wall of confusion** describe un traspaso entre equipos en el que el trabajo se entrega sin suficiente contexto o sin considerar las necesidades del receptor. En ML puede aparecer tanto entre ciencia de datos e ingeniería como entre ingeniería y Operaciones.
>
> Entregar un Jupyter notebook y pedir que se convierta en una aplicación de producción deja decisiones pendientes. Hay que resolver vulnerabilidades, fijar versiones de dependencias, definir la construcción del software y organizar su ejecución.
>
> Un notebook permite experimentar, pero no proporciona por sí solo todas las condiciones de un servicio de producción. Si no existe una forma común de compartir el trabajo, su traducción a software operativo puede reducir la estabilidad del modelo y retrasar el **time to market**.

#### 7. DevOps engineers and platform operations

> Los **DevOps engineers** aportan conocimientos de infraestructura, automatización y monitorización. Adaptan esas prácticas a los ciclos de vida de datos y modelos y automatizan pipelines de entrenamiento y despliegue.
>
> También suelen actuar como equipo de desarrollo y soporte de la plataforma. Las herramientas que sostienen el trabajo de ML siguen siendo aplicaciones: necesitan construcción, pruebas, actualizaciones, observabilidad y operación.
>
> El trabajo operativo repetitivo, o **toil**, continúa existiendo en los despliegues de ML. Gestionarlo permite que los modelos funcionen de manera fiable y a escala.
>
> Desde Operaciones se plantea cómo comprobar que el sistema y el modelo estén funcionando de acuerdo con los objetivos. Esta perspectiva conecta el estado técnico de la plataforma con las expectativas del producto.

#### 8. Business, product and shared objectives

> Los **business stakeholders** y **product managers** definen los objetivos y requisitos del proyecto. Evalúan cómo puede resolver problemas del negocio, mejorar el producto y aportar valor.
>
> MLOps les permite seguir el desarrollo, entender las capacidades y limitaciones de los modelos desplegados y tomar decisiones basadas en datos. Deben conocer tanto la inversión necesaria como los resultados obtenidos para valorar la rentabilidad del proyecto.
>
> El stakeholder pregunta **qué valor aporta el modelo**. El product manager necesita determinar **qué recursos hacen falta para sostenerlo**. El **data science manager** debe comunicar a los interesados el impacto del trabajo y las necesidades del equipo.
>
> La perspectiva del **end user** completa la evaluación: cómo le ayuda la aplicación de ML. Una mejora técnica debe poder relacionarse con la utilidad del producto.

> La colaboración se sostiene con workflows automatizados, herramientas estandarizadas y prácticas compartidas:
>
> - **Collaborative development:** ciencia de datos, ingeniería de ML e ingeniería de datos construyen y refinan los modelos conjuntamente.
> - **Continuous integration and deployment:** se automatizan pruebas, despliegues y actualizaciones.
> - **Monitoring and maintenance:** se estudia el rendimiento para detectar cambios en los datos o deterioro del modelo.
> - **Governance and compliance:** se incorporan los requisitos regulatorios y las pautas éticas aplicables al sistema.
>
> Alinear objetivos y formas de trabajo ayuda a entregar modelos con mayor rapidez, eficiencia y fiabilidad, manteniendo la relación con el valor de negocio.

#### 9. Who holds the pager?

> Cuando falla un modelo, la causa puede estar en datos de baja calidad, respuestas demasiado lentas u otros componentes del sistema. Es necesario definir quién atiende la incidencia y cómo se escala a los perfiles que pueden investigarla.
>
> **Who holds the pager?** representa esa responsabilidad de respuesta. Los roles y caminos de escalado deben quedar claros para que el equipo pueda actuar coordinadamente.
>
> Ante un fallo de madrugada, contactar con el data scientist o retirar el modelo de producción son decisiones diferentes. Reentrenar y adaptar un modelo requiere tiempo: el proceso científico no suele ofrecer una solución inmediata.
>
> La respuesta inicial debe apoyarse en la automatización disponible y en decisiones que protejan al cliente y al negocio. El diagnóstico y la mejora del modelo pueden continuar después, con el tiempo y los datos que requieren.
>
> El **post-mortem** permite revisar lo ocurrido y mejorar la comprensión compartida y la coordinación. Una cultura de colaboración prepara al equipo para afrontar la siguiente incidencia.

### III. Workflow, Pipelines and Maturity

#### 10. The MLOps workflow

> El workflow transforma un problema de negocio en un modelo desplegado y monitorizado. Sus etapas separan tareas diferentes y permiten identificar qué debe revisarse cuando el resultado no es adecuado.

![[imgs/apuntes-5779b8d8cb73-p0009-a7285a5c6d27.png]]

> Las etapas son:
>
> 1. **Codifying problem and metrics:** formular el problema y definir las mediciones con las que se evaluará el resultado.
> 2. **Data collection and cleaning:** recoger datos y prepararlos para su utilización.
> 3. **Feature engineering:** construir las características de entrada que utilizará el modelo.
> 4. **Model development:** definir y experimentar con el modelo.
> 5. **Model training pipeline:** organizar y ejecutar el entrenamiento y sus ajustes.
> 6. **Model validation:** comprobar si el modelo cumple los criterios establecidos.
> 7. **Model serving pipeline:** preparar y desplegar el modelo para que una aplicación pueda consumirlo.
> 8. **Monitoring and validation:** observar y validar su comportamiento después del despliegue.

> Los retornos del diagrama muestran que las etapas no se completan una única vez. El desarrollo puede llevar a revisar la recogida de datos o las features, y la validación puede devolver el trabajo al desarrollo del modelo.
>
> La monitorización proporciona nuevos motivos para revisar datos, desarrollo o entrenamiento. Por ejemplo, un **outlier** es una observación atípica; el **drift** se refiere a cambios en el comportamiento o las distribuciones relevantes a lo largo del tiempo. Un caso aislado no demuestra por sí solo un cambio sostenido.
>
> La degradación del rendimiento predictivo, o **model decay**, exige investigar la causa y decidir qué parte del flujo se debe repetir. Volver a entrenar es una posibilidad dentro de ese proceso.

#### 11. Data science pipelines

> Un **pipeline** encadena tareas de ciencia de datos con un orden y unas dependencias explícitas. Permite orquestar procesos como preparar datos, construir modelos y servirlos, además de programar, seguir y gestionar sus ejecuciones.
>
> Una interfaz gráfica puede facilitar la construcción y la inspección del flujo. La automatización permite entregar y probar modelos de forma continua.

> Un pipeline ilustrativo sigue este recorrido:
>
> 1. Recoger los datos.
> 2. Procesarlos.
> 3. Entrenar un modelo nuevo.
> 4. Descargar el modelo existente para disponer de la referencia de comparación.
> 5. Comparar el modelo nuevo con el existente.
> 6. Publicar el nuevo modelo **si es mejor** bajo el criterio de evaluación establecido.
>
> La descarga del modelo existente y el entrenamiento del candidato son ramas independientes que convergen en la comparación. Esta depende de disponer de ambos modelos. Entrenar un candidato y desplegarlo son decisiones distintas; el paso de comparación condiciona la publicación.
>
> Definir el criterio de mejora permite relacionar la promoción del modelo con las métricas del problema. Automatizar ese criterio hace que la decisión sea repetible dentro del pipeline.

#### 12. MLOps maturity levels

> La madurez puede describirse mediante el alcance de la automatización. La siguiente clasificación utiliza cinco niveles, desde un proceso manual hasta la integración del ciclo completo.

| Nivel | Nombre | Idea principal |
| --- | --- | --- |
| **0** | **Manual Process** | Los pasos y sus traspasos se realizan principalmente de forma manual |
| **1** | **Continuous Integration** | Se automatiza la integración y comprobación de cambios |
| **2** | **Continuous Delivery** | Se organiza la entrega sistemática de cambios validados |
| **3** | **Continuous Training** | Se automatiza la repetición del entrenamiento dentro del workflow |
| **4** | **Full MLOps** | Se integra la gestión y automatización del ciclo de vida completo |

> La progresión amplía qué partes del trabajo se controlan mediante procesos compartidos. El **continuous training** incorpora la actualización de modelos al circuito operativo, además de la entrega del software.
>
> Un entrenamiento automatizado no implica publicar todos sus resultados. La validación y los criterios de promoción siguen siendo necesarios para decidir qué candidato se despliega.


### IV. Machine Learning Toolkits

#### 13. A common platform for different personas

> Un **Machine Learning Toolkit (MLT)** proporciona un conjunto compartido de herramientas y librerías para automatizar partes del workflow de ML. Ofrece una base común a perfiles que tienen necesidades distintas.
>
> Para data scientists y MLEs facilita el desarrollo y la evaluación de modelos. Para ingeniería de datos y DevOps simplifica el despliegue, la gestión y la monitorización. Negocio puede seguir la alineación con sus objetivos y el valor obtenido.
>
> Un toolkit como **Kubeflow** ayuda a integrar esas tareas en un proceso operativo. La productividad individual mejora cuando el resultado de cada etapa puede utilizarse en la siguiente con menos traspasos manuales.

#### 14. Open source across the workflow

> El ecosistema open source permite combinar herramientas especializadas a lo largo del ciclo. Los siguientes ejemplos se asocian con las áreas del workflow en las que contribuyen.

| Área | Ejemplos de herramientas |
| --- | --- |
| Recogida, almacenamiento, acceso y preparación de datos | **Pachyderm**, **Trino**, **Ceph** |
| Feature engineering y desarrollo interactivo | **Jupyter**, **Elyra**, **Visual Studio Code**, **RStudio** |
| Pipelines de entrenamiento y validación | **Ray**, **Kubeflow**, **CodeFlare**, **Tekton** |
| Serving y entrega de modelos | **KServe**, **Argo** |
| Monitorización y visualización | **Grafana**, **Prometheus** |

> Cada grupo reúne capacidades complementarias. El almacenamiento, la consulta y la preparación contribuyen al trabajo con datos; los entornos interactivos apoyan la experimentación; los componentes de orquestación coordinan tareas.
>
> La entrega y la ejecución de inferencias son funciones distintas dentro del pipeline de serving. La combinación de herramientas debe cubrir ambas y devolver información desde producción hacia las etapas que necesitan cambios.

#### 15. Cloud integration, portability and lock-in

> La integración con servicios cloud y **Kubernetes** facilita desplegar workflows, utilizar recursos y escalar. Existen distintos grados de integración con un proveedor.

##### 15.1. Toolkits integrated with a particular cloud

> Plataformas como **Amazon SageMaker** o **Vertex AI** integran gran parte del trabajo con los servicios de su cloud. Buscan simplificar la infraestructura y ofrecer un entorno coherente para el desarrollo y la operación de modelos.
>
> La integración estrecha puede reducir el número de componentes que el equipo debe gestionar y favorecer un comportamiento más predecible y estable de la plataforma. A la vez, relaciona el workflow con las interfaces y servicios del proveedor.

##### 15.2. Loosely coupled toolkits

> Herramientas como **Flyte** y **Kubeflow** buscan mantener una relación menos estrecha con un cloud concreto para reducir el **vendor lock-in**. Sus componentes pueden desplegarse localmente o conectarse a endpoints de servicios cloud.
>
> El almacenamiento de objetos ilustra esta elección: se pueden utilizar **Amazon S3**, **Google Cloud Storage** o un almacén como **MinIO**, según la integración y la distribución empleadas.
>
> La flexibilidad permite adaptar la solución a los conocimientos internos y a las necesidades de personalización. Consumir servicios cloud también puede mejorar la fiabilidad mediante capacidad de escalado y mecanismos de tolerancia a fallos, como la replicación entre regiones cuando se configura para ello.
>
> La portabilidad exige considerar dependencias, accesos, formatos y configuración. Utilizar componentes desacoplados facilita la migración, pero no elimina esas condiciones.

#### 16. Model versioning, tracking and customization

> El **versionado de modelos** y el **experiment tracking** conservan información sobre la evolución del trabajo: modificaciones del modelo, variaciones de los experimentos y resultados obtenidos.
>
> Este historial permite identificar qué se probó, qué cambió y qué resultado corresponde a cada versión. Mejora la reproducibilidad al relacionar los resultados con las condiciones del experimento.
>
> Los toolkits también ofrecen **extensibilidad**. Se pueden integrar herramientas externas, operadores personalizados y plugins para cubrir requisitos específicos.
>
> Versionado y extensibilidad cumplen funciones complementarias: el primero permite seguir la evolución; la segunda permite adaptar la plataforma al proceso de la organización.

### V. Kubeflow

#### 17. Portability, composability and scalability

> La misión de **Kubeflow** lleva al machine learning los principios de **portabilidad, composabilidad y escalabilidad**. Su enfoque amplía la utilización de recursos cloud hacia una plataforma capaz de coordinar aplicaciones intensivas en datos.
>
> DevOps proporciona prácticas para desplegar aplicaciones con rapidez. Trabajar con modelos añade necesidades sobre datos, entrenamiento y evaluación, lo que requiere capacidades específicas de MLOps.

##### 17.1. Portability

> La **portabilidad** permite migrar y ejecutar workflows entre los entornos de una organización. Un equipo puede desarrollar el modelo en su entorno preferido y desplegarlo donde resulte más adecuado.
>
> Kubernetes proporciona una base común sobre la que ejecutar los componentes. Las integraciones de almacenamiento, recursos y servicios deben estar disponibles en el entorno de destino para conservar el funcionamiento del workflow.

##### 17.2. Composability

> La **composabilidad** permite ensamblar y sustituir componentes del workflow. Los equipos seleccionan, integran y gestionan las herramientas que mejor responden a cada fase del desarrollo.
>
> El resultado puede adaptarse a los requisitos del proyecto y evolucionar conforme cambian sus necesidades. La selección de componentes reduce la dependencia de un conjunto único y rígido de herramientas.

##### 17.3. Scalability

> La **escalabilidad** permite procesar el trabajo actual y asignar recursos adicionales para nuevas tareas. En ML puede significar entrenar modelos más complejos, utilizar datasets mayores o distribuir el entrenamiento.
>
> **Scale up** aumenta la capacidad de los recursos utilizados. **Scale out** amplía el conjunto de recursos o trabajadores para repartir el trabajo, como en el entrenamiento distribuido.
>
> La arquitectura de Kubeflow permite gestionar la asignación y liberación de recursos de acuerdo con las cargas del workflow. La automatización depende de los componentes y políticas configurados, de las cuotas y de la capacidad disponible en el clúster.

#### 18. Component map

> Los componentes organizan distintas funciones del ciclo de ML. La separación ayuda a distinguir la experimentación, la orquestación, el entrenamiento y la inferencia.

![[imgs/apuntes-5779b8d8cb73-p0032-dcfa8405ba01.png]]

| Componente | Función |
| --- | --- |
| **Central Dashboard** | Acceso web a las herramientas de la plataforma |
| **Kubeflow Notebooks** | Entornos de desarrollo interactivo |
| **Kubeflow Pipelines** | Orquestación de workflows y programación de ejecuciones |
| **Katib** | Ajuste del modelo, especialmente búsqueda de hiperparámetros |
| **Training Operator** | Gestión de trabajos de entrenamiento en Kubernetes, incluido entrenamiento distribuido |
| **KServe** | Serving de modelos para inferencia |

> La base de Kubernetes permite desplegar estos componentes en entornos locales, autogestionados o cloud. El esquema también sitúa encima herramientas y frameworks como PyTorch, TensorFlow, Hugging Face, Jupyter, scikit-learn, Horovod y XGBoost.
>
> **Katib** organiza pruebas de configuraciones para evaluar su efecto sobre una métrica objetivo. El **Training Operator** coordina la ejecución de trabajos de entrenamiento. **Pipelines** organiza las dependencias entre tareas y puede incorporar esos trabajos dentro de un flujo más amplio.
>
> La denominación **Training Operator** corresponde a la familia de componentes v1; su evolución se denomina **Kubeflow Trainer v2**. La función de entrenamiento y su relación con el resto del workflow se mantienen como referencia conceptual.

#### 19. Kubernetes and managed cloud services

> Kubeflow utiliza Kubernetes como base para desplegar sus servicios. También puede consumir servicios externos como endpoints especializados, aprovechando las capacidades del cloud sin ejecutar dentro del clúster cada dependencia.
>
> En almacenamiento, los componentes pueden conectarse a un servicio de objetos apropiado. La interfaz elegida y la configuración de cada distribución determinan cómo se accede al backend.

> MinIO puede proporcionar una interfaz de objetos y combinar su almacenamiento con niveles remotos mediante **tiering**. Con esta modalidad, configurada mediante reglas, los datos de determinados objetos se trasladan a un nivel externo, como S3 o Google Cloud Storage, mientras sus metadatos permanecen en el almacenamiento principal. La integración concreta depende de la modalidad y versión utilizadas.

> Un ejemplo de integración específico de una distribución en **Google Cloud Platform** es utilizar una base de datos **Cloud SQL**, con un proxy de conexión, para apoyar Kubeflow Pipelines en lugar de administrar un MySQL dentro de Kubernetes.
>
> El proveedor gestiona la base de datos y el equipo configura cómo se conecta la plataforma. Esto reduce la carga de administrar ese servicio dentro del clúster.
>
> El patrón general consiste en combinar componentes ejecutados en Kubernetes con servicios gestionados cuando aportan fiabilidad o capacidad de escalado.

#### 20. Central Dashboard and access control

> El **Kubeflow Central Dashboard** proporciona una interfaz común para interactuar con los servicios de ML. Desde el navegador se puede acceder a notebooks, experimentos, endpoints de modelos y otras herramientas integradas.
>
> La plataforma también dispone de API para orquestar sus servicios, pero el dashboard suele ser el primer punto de contacto de los usuarios. Puede exponerse fuera del clúster y personalizarse para añadir opciones de aplicaciones.
>
> Los **namespaces** organizan los recursos y la visibilidad de los equipos. La interfaz debe mostrar a cada usuario los recursos que le permiten las políticas de la plataforma.
>
> **Kubernetes RBAC** controla las acciones autorizadas sobre recursos de Kubernetes. Las políticas de autorización de **Istio** pueden controlar la comunicación entre servicios. Estos mecanismos permiten separar lógicamente equipos y controlar accesos dentro de la plataforma.

#### 21. Kubeflow Notebooks

> **Kubeflow Notebooks** proporciona entornos de desarrollo integrados para trabajar con datos y modelos. Entre las opciones de servidor aparecen **Jupyter**, **RStudio** y **Visual Studio Code**.
>
> Las imágenes de los servidores pueden personalizarse para incluir las librerías y condiciones exigidas por la organización. La interfaz permite solicitar imágenes y recursos adecuados a la tarea.
>
> La configuración del entorno incluye:
>
> - **CPU y RAM:** capacidad de cómputo y memoria solicitada.
> - **GPU:** aceleradores y opciones relacionadas cuando estén disponibles.
> - **Workspace volume:** volumen de trabajo del entorno.
> - **Data volumes:** volúmenes adicionales para acceder a datos.
>
> Estos parámetros relacionan la experiencia interactiva con los recursos del clúster. Elegir una imagen de entorno y los volúmenes necesarios prepara el espacio donde se realizará la experimentación.
>
> Una configuración ilustrativa solicita `0.5` CPU y `1` Gi de memoria, con un volumen de trabajo de `5` Gi. Son valores del ejemplo de creación del entorno; las necesidades de cada tarea determinan los recursos que se deben solicitar.

### VI. Model Serving and KServe

#### 22. Models as a service

> Un modelo forma parte de una aplicación, pero su función se centra en obtener predicciones a partir de datos. La aplicación interpreta esos resultados y decide qué acciones realizar, por ejemplo aplicando umbrales asociados a distintos resultados de negocio.
>
> El modelo puede integrarse de dos formas:
>
> - **Embedded:** se carga y utiliza dentro de la propia aplicación, en un diseño monolítico o integrado.
> - **Endpoint:** se ofrece como servicio separado; la aplicación envía datos en una petición y recibe predicciones en una respuesta.
>
> Desacoplarlo como microservicio permite gestionar su despliegue detrás de una interfaz. Los contenedores empaquetan el software de serving y Kubernetes puede organizar su ejecución.
>
> El modelo que hay detrás del endpoint puede actualizarse utilizando estrategias **A/B** o **canary**. En A/B se comparan alternativas asignando tráfico entre versiones; en canary se introduce progresivamente una versión nueva y se observa su comportamiento.
>
> Para aplicar estas estrategias, los equipos necesitan desplegar modelos de forma consistente y eficiente. Los frameworks especializados de serving proporcionan capacidades reutilizables para esa tarea.

#### 23. Building a serving layer with web frameworks

> Una solución a medida puede utilizar **Flask**, **Django** o **FastAPI** para ofrecer un modelo como servicio web. Esa flexibilidad exige implementar y mantener varias responsabilidades de la capa de serving.

| Responsabilidad | Trabajo necesario |
| --- | --- |
| **Model loading** | Cargar el modelo entrenado en memoria para realizar predicciones |
| **API endpoints** | Recibir datos, por ejemplo JSON, invocar el modelo y devolver respuestas HTTP |
| **Data preprocessing and validation** | Validar formato y estructura; aplicar transformaciones como normalización o cambio de forma |
| **Concurrency and scalability** | Atender varias peticiones simultáneas y organizar el escalado; considerar procesamiento asíncrono cuando corresponda |
| **Security** | Configurar autenticación, autorización y cifrado de las comunicaciones |
| **Error handling** | Gestionar entradas incorrectas, errores de carga del modelo y fallos del servidor |
| **Deployment** | Empaquetar la aplicación, por ejemplo con Docker, y desplegarla en servidores cloud o locales |
| **Monitoring and maintenance** | Configurar logs, monitorización y alertas; aplicar actualizaciones y correcciones |

> Mantener estas funciones para cada modelo aumenta el trabajo de ingeniería. Los frameworks de serving abstraen tareas comunes y proporcionan una forma más uniforme de desplegar.
>
> La aplicación sigue necesitando un contrato de entrada y salida y una configuración apropiada. La validación de los datos y el significado de las predicciones deben relacionarse con el modelo concreto.

#### 24. Serving tools and the InferenceService resource

> Entre las herramientas de serving se encuentran **NVIDIA Triton Inference Server**, **TensorFlow Serving**, **Seldon Core Serving** y **KServe**.
>
> **KServe** es una plataforma de inferencia sobre Kubernetes orientada a ofrecer modelos de forma escalable. Proporciona una abstracción de alto nivel para distintos frameworks y formatos, entre ellos TensorFlow, XGBoost, scikit-learn, PyTorch y ONNX.
>
> Su recurso **`InferenceService`** describe el servicio de inferencia que se quiere desplegar. Se incorpora a Kubernetes mediante una **Custom Resource Definition (CRD)**; los controladores de KServe interpretan esa descripción y gestionan los componentes necesarios.

> [!warning] Corrección
> En el material aparece `InferencingService`, pero el nombre del recurso de KServe es `InferenceService`.
> Fuente de comprobación: [KServe: creación de un InferenceService](https://kserve.github.io/website/docs/getting-started/predictive-first-isvc)

> La analogía con un pod ayuda a entender la abstracción: un **pod** proporciona el contexto para ejecutar un contenedor; un **InferenceService** proporciona una descripción gestionada del servicio que ofrece el modelo.
>
> Si hacen falta nuevas réplicas, la plataforma puede preparar instancias equivalentes del serving. El recurso no contiene los pesos del modelo: referencia los artefactos y la configuración necesaria para cargarlos y servirlos.
>
> La abstracción permite reutilizar servidores y automatizar la gestión de recursos. El equipo de plataforma sigue siendo responsable de instalar y configurar KServe y de disponer de la infraestructura requerida.

#### 25. Deploying, scaling and exposing a model

> El recorrido de despliegue parte de un modelo entrenado y serializado, conservado como un artefacto accesible. Un registro de modelos permite identificar sus versiones y localizar los artefactos que se van a utilizar.
>
> A continuación se define o actualiza el manifiesto que describe el servicio. La plataforma prepara el servidor adecuado, obtiene el modelo y lo expone mediante un endpoint.

> La configuración debe resolver:
>
> 1. **Identificación del modelo:** proyecto, nombre y framework o formato que utilizará el servidor.
> 2. **Ubicación del artefacto:** conexión de almacenamiento y ruta del modelo.
> 3. **Recursos y escala:** número de réplicas y capacidad asignada a cada una.
> 4. **Exposición del endpoint:** ruta interna o externa y requisitos de acceso.
> 5. **Comprobación del despliegue:** estado del servicio y endpoint de inferencia.
>
> Exponer una ruta externa y exigir autenticación son decisiones configurables. Deben elegirse de acuerdo con quién vaya a consumir el servicio.
>
> El listado de modelos desplegados permite identificar los endpoints y su estado. Escalar el serving modifica la capacidad de atender inferencias; entrenar de nuevo modifica el modelo que se ofrece.

#### 26. KServe architecture and inference flow

> La arquitectura organiza la ejecución de inferencias sobre Kubernetes y sobre los recursos de cómputo disponibles.

![[imgs/apuntes-5779b8d8cb73-p0041-750d7eefe4d4.png]]

> Las capas son:
>
> - **Compute cluster:** CPU, GPU o TPU que ejecutan las cargas.
> - **Kubernetes:** organización de los recursos y de los componentes desplegados.
> - **Knative e Istio:** capa opcional asociada al modo serverless y a la comunicación del servicio.
> - **KServe:** gestión de la inferencia y de su integración con los artefactos del modelo.
>
> El carácter opcional de la capa serverless permite distinguirla de la base Kubernetes. KServe también puede desplegar servicios mediante recursos estándar de Kubernetes; las capacidades de escalado dependen del modo y de su configuración.

> El recorrido de inferencia puede incorporar:
>
> 1. **Pre-process:** preparar la entrada para el modelo.
> 2. **Predict:** ejecutar la inferencia.
> 3. **Post-process:** transformar la salida para que pueda utilizarse.
> 4. **Explain:** producir explicaciones cuando se haya configurado esa capacidad.
> 5. **Monitor:** recoger información sobre la ejecución y el comportamiento.
>
> Estas funciones se configuran según el caso; una predicción no incluye automáticamente todas ellas. Los **model assets** proporcionan los artefactos utilizados por el servicio.
>
> El esquema muestra tecnologías como TensorFlow, PyTorch, scikit-learn, XGBoost, ONNX y TensorRT. El runtime elegido debe ser compatible con el formato y los requisitos del modelo.
>
> El serving completa la conexión entre el modelo entrenado y la aplicación. La información obtenida al operarlo vuelve al workflow para orientar mantenimiento, validación y nuevos entrenamientos.

### VII. Final Summary

> MLOps lleva los modelos desde la experimentación hasta una operación que aporte valor. Extiende las prácticas de DevOps con la gestión de datos, entrenamiento, validación y seguimiento del comportamiento predictivo.
>
> La colaboración entre negocio, ingeniería de datos, ciencia de datos, MLEs, desarrollo de aplicaciones y Operaciones permite gestionar las dependencias del ciclo. Los traspasos de trabajo y las responsabilidades ante incidentes deben quedar definidos.
>
> El workflow combina etapas de desarrollo con retornos desde la validación y la monitorización. Los pipelines hacen explícitas sus dependencias y permiten automatizar el entrenamiento y la comparación antes de promover un modelo.
>
> Los toolkits ofrecen una base compartida. La integración estrecha con un cloud simplifica parte de la infraestructura; la composabilidad y la portabilidad permiten adaptar la solución a distintos entornos.
>
> Kubeflow organiza entornos interactivos, workflows, ajuste y entrenamiento sobre Kubernetes. KServe proporciona una abstracción para desplegar modelos como servicios de inferencia.
>
> La aplicación interpreta las predicciones, la plataforma sostiene el serving y la monitorización devuelve información para mejorar el sistema. La calidad operativa depende de coordinar esas funciones con los objetivos del producto.
