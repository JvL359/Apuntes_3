---
estado: pendiente de revisión
---

### I. Git: modelo y operaciones básicas

#### 1. Repositorios distribuidos y snapshots

> **Git** es un sistema distribuido de control de versiones. Cada desarrollador dispone de un repositorio local y puede realizar la mayoría de las operaciones —crear commits, consultar el historial o trabajar con ramas— sin comunicarse con un servidor.
>
> Un **commit** registra una instantánea, o *snapshot*, de los archivos versionados, junto con metadatos y referencias a sus padres. El historial conecta esas instantáneas. Los identificadores basados en **checksums** permiten referirse a los objetos y comprobar su integridad.
>
> El modelo distribuido permite que distintas copias del repositorio compartan historia y evolucionen de forma independiente. La colaboración se realiza intercambiando commits con otros repositorios.

> [!warning] Corrección
> En el material aparece que cada snapshot es un repositorio completo, pero un snapshot representa el estado de los archivos versionados en un momento. El repositorio contiene los objetos, referencias y metadatos que permiten conservar y recorrer el historial.
> Fuente de comprobación: [Git: snapshots y estructura del repositorio](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)

#### 2. Estados y áreas de trabajo

> Git distingue tres áreas y tres estados principales de los archivos. El **working directory** contiene los archivos con los que se trabaja; la **staging area**, también llamada *index*, prepara el contenido del próximo commit; el **Git directory**, normalmente `.git/`, conserva objetos y metadatos.

| Estado | Significado |
| --- | --- |
| **Modified** | Hay cambios en el archivo que todavía no se han confirmado. |
| **Staged** | Una versión concreta del archivo está preparada para el próximo commit. |
| **Committed** | El contenido está registrado en un commit del repositorio. |

![[apuntes-2c7d295840d1-p0003-ab6eaa9384e3.png]]

> El flujo normal es **modificar → preparar con `git add` → confirmar con `git commit`**. Recuperar una versión del proyecto permite reconstruir sus archivos en el directorio de trabajo.
>
> `git add` prepara el contenido existente en ese momento. Si se modifica otra vez el archivo, hay que volver a añadirlo para incluir la nueva versión. Por ello, un mismo archivo puede tener cambios preparados y otros cambios posteriores todavía sin preparar.

#### 3. Crear, clonar y configurar

| Comando | Función |
| --- | --- |
| `git init` | Crear un repositorio y sus metadatos. |
| `git clone <URL>` | Obtener una copia local de un repositorio existente y configurar habitualmente el remoto `origin`. |
| `git config` | Configurar opciones del repositorio o del usuario. |

> La configuración local afecta al repositorio actual; `--global` permite aplicar opciones al usuario. La identidad que se escribe en los commits se define mediante `user.name` y `user.email`.
>
> Para iniciar un repositorio local y asociarlo a otro remoto:

```bash
git init
git config user.name "nombreUsuario"
git config user.email "emailUsuario"
git remote add origin "http://..."
```

> El nombre, correo y URL son marcadores que deben sustituirse. **Crear el repositorio local y añadir un remoto son operaciones distintas**: `remote add` registra una conexión, pero no publica los archivos.
>
> Otra posibilidad consiste en crear primero el repositorio en GitHub: seleccionar **New**, elegir su nombre y pulsar **Create repository**. Con la URL que proporciona la plataforma se obtiene la copia local:

```bash
git clone linkDelRepo
```

> `linkDelRepo` representa esa URL. En una clonación ordinaria se obtiene el historial disponible y una copia de trabajo; los cambios locales no modifican el remoto hasta que se publican.

#### 4. Guardar y consultar cambios

> `git commit` registra el contenido del index. `git commit --amend` sustituye el último commit por otro que puede incorporar contenido preparado y modificar su mensaje; cambia su identificador.
>
> El procedimiento básico de publicación es:

```bash
git add .
git commit -m "mensaje"
git push origin master
git status
```

> `git add .` prepara los cambios bajo el directorio actual que Git puede incluir; `commit` crea la instantánea local y `push` la envía al remoto. `master` es el nombre de rama utilizado en este ejemplo: si el proyecto utiliza `main`, debe emplearse ese nombre.
>
> Para inspeccionar el trabajo y el historial:

```bash
git status
git log
git log --oneline --graph --all
```

> **`git status`** describe la relación entre los archivos de trabajo, el index y el commit actual; ayuda a identificar qué entrará en el siguiente commit. **`git log`** consulta la historia confirmada y permite filtrarla. Las opciones `--oneline --graph --all` muestran un resumen del grafo y las referencias relevantes, útil para estudiar ramas.
>
> Antes de confirmar debe comprobarse qué está preparado. Un commit local no implica que ese contenido ya esté disponible en el repositorio remoto.

#### 5. Guardar trabajo temporal con stash

> **Stash** permite apartar cambios que todavía no se quieren confirmar y recuperar una copia de trabajo basada en `HEAD`. En su uso habitual guarda modificaciones de archivos seguidos por Git y del index; incluir archivos no seguidos requiere `-u`.
>
> El flujo conserva una descripción para identificar el trabajo:

```bash
git stash save "nombre"
git stash list
git stash apply 'stash@{0}'
```

> `save` es la forma heredada; su alternativa actual es `git stash push -m "nombre"`. El mensaje facilita reconocer la entrada, mientras `stash@{0}` identifica la más reciente.
>
> `apply` reaplica los cambios y conserva la entrada. `git stash pop` intenta reaplicarla y retirarla de la lista; si se producen conflictos, la entrada se conserva hasta resolverlos.

> [!warning] Corrección
> En el material aparece que stash es internamente una rama y que `git stash apply name` recupera la entrada por el mensaje usado al guardarla. Stash conserva commits mediante `refs/stash` y su reflog; para recuperarlos se utiliza una referencia como `stash@{0}`, no el mensaje descriptivo.
> Fuente de comprobación: [Git: funcionamiento y referencias de stash](https://git-scm.com/docs/git-stash)

#### 6. Repositorios remotos y sincronización

| Comando | Efecto |
| --- | --- |
| `git remote -v` | Mostrar las conexiones remotas. |
| `git remote add origin <URL>` | Añadir una conexión llamada `origin`. |
| `git remote remove <nombre>` | Eliminar la conexión local con ese nombre. |
| `git fetch` | Obtener objetos y actualizar las referencias de seguimiento remoto. |
| `git pull` | Obtener cambios e integrarlos en la rama actual. |
| `git push` | Publicar commits y actualizar referencias remotas autorizadas. |

> Eliminar una conexión remota no borra el repositorio alojado en el servidor. **Fetch** permite conocer cambios sin integrarlos en los archivos de trabajo. **Pull** añade una etapa de integración: en el flujo basado en merge equivale a fetch seguido de merge; otras configuraciones pueden utilizar rebase.
>
> En una rama con seguimiento remoto configurado se puede sincronizar con:

```bash
git status
git pull
```

> [!warning] Corrección
> En el material aparece que `git fetch` no realiza cambios en el repositorio local, pero descarga objetos y actualiza referencias locales de seguimiento remoto. Lo que no hace en su uso normal es integrar esos cambios en la rama actual ni modificar sus archivos de trabajo.
> Fuente de comprobación: [Git: fetch](https://git-scm.com/docs/git-fetch)

> Una actualización que reescribe historia puede requerir un push forzado. `git push --force` omite la protección habitual frente a actualizaciones que no son fast-forward. `git push --force-with-lease` exige que la referencia remota coincida con el valor esperado, normalmente el conocido por la referencia de seguimiento local.
>
> Esa condición se refiere a las referencias que se van a actualizar. Coordinar la reescritura sigue siendo necesario cuando otros desarrolladores han utilizado los commits publicados.

### II. Ramas, integración y recuperación

#### 7. Ramas y pull requests

> Una **rama** permite desarrollar una línea de trabajo. `git branch` crea, lista o elimina ramas; `git switch` cambia de rama; `git merge` integra otra línea de desarrollo en la rama actual.

| Operación | Comando específico | Forma con checkout |
| --- | --- | --- |
| Cambiar de rama | `git switch <rama>` | `git checkout <rama>` |
| Crear rama y cambiar a ella | `git switch -c <rama>` | `git checkout -b <rama>` |
| Restaurar un archivo desde el index | `git restore <archivo>` | `git checkout -- <archivo>` |

> [!warning] Corrección
> En el material aparece `git checkout` como deprecado, pero sigue siendo un comando válido. `switch` y `restore` separan sus funciones de cambio de rama y restauración de archivos.
> Fuente de comprobación: [Git: checkout](https://git-scm.com/docs/git-checkout)

> Una **pull request (PR)** pertenece a la plataforma de colaboración, como GitHub, y permite proponer una integración. Abre un canal para informar de que un desarrollo está listo, revisar el código, discutir la implementación y posponer la fusión hasta cumplir sus condiciones.
>
> La PR organiza la decisión del equipo; el merge es la operación que incorpora la historia o cambios según la estrategia elegida.

#### 8. Modelos de colaboración

| Workflow | Organización |
| --- | --- |
| **Centralized Workflow** | Existe un repositorio central y cada desarrollador mantiene su copia local. La colaboración sigue una estructura centralizada semejante a SVN. |
| **Feature Branch Workflow** | Añade ramas para cada desarrollo nuevo, que se revisan e integran en la línea compartida. |
| **Gitflow Workflow** | Asigna funciones estrictas a ramas de desarrollo, funcionalidades, releases y hotfixes. |
| **Forking Workflow** | Equipos o colaboradores mantienen repositorios propios en el servidor; un responsable integra los cambios en el repositorio central. |

> En **Forking Workflow**, controlar quién integra en el repositorio principal permite separar contribución y autorización de escritura. En **Feature Branch Workflow**, los cambios de cada funcionalidad pueden evolucionar antes de incorporarse al desarrollo común.
>
> **Gitflow** distingue:
>
> - **`main` / `master`**: versiones liberadas.
> - **`develop`**: integración del desarrollo.
> - **Feature branches**: funcionalidades que parten del desarrollo y vuelven a él.
> - **Release branches**: preparación de una versión.
> - **Hotfix branches**: correcciones rápidas de una versión liberada, que también deben incorporarse al desarrollo.

![[apuntes-2c7d295840d1-p0018-1538bbb90b91.png]]

> La figura muestra una funcionalidad que vuelve a `develop`, una release que llega a la rama principal y un hotfix que se incorpora a ambas líneas. Mantener la rama principal alineada con producción exige seguir una política de liberación y despliegue; el nombre de la rama por sí solo no impone qué versión está operando.

#### 9. Merge frente a rebase

> **Merge** integra historias conservando sus commits. Si las ramas divergen, una fusión ordinaria registra un commit con los padres de las dos líneas. Si una línea ya es antecesora de la otra, puede realizarse un **fast-forward**, que avanza la referencia sin crear un commit de fusión.
>
> **Rebase** reaplica commits sobre una base diferente y crea nuevos identificadores. Permite una línea más secuencial; los conflictos pueden tener que resolverse en cada commit reaplicado.

| Aspecto | Merge | Rebase |
| --- | --- | --- |
| Historia | Conserva los commits de las líneas integradas. | Reescribe los commits que reaplica. |
| Resultado con ramas divergentes | Commit de fusión que conecta las historias. | Secuencia de commits sobre una nueva base. |
| Conflictos | Se resuelven al combinar las líneas. | Pueden aparecer en cada paso de reaplicación. |
| Uso docente | Preservar la historia y facilitar la colaboración en ramas compartidas. | Preparar una rama feature con historia lineal antes de integrarla. |

> Para una feature con commits `D` y `E` que parte de `B`, mientras `main` avanza a `C`, una fusión se representa así:

```text
A---B---C---M  (main)
     \     /
      D---E    (feature)
```

> `M` conecta `C` y `E`. Un rebase de la feature sobre `C` produciría la secuencia conceptual `A → B → C → D' → E'`, mientras `main` seguiría en `C` hasta integrarla.

> [!warning] Corrección
> En el material aparece un esquema de merge en el que `M` solo está conectado con la feature, pero una fusión de esas dos ramas divergentes debe conectar `M` con ambos padres, `C` y `E`.
> Fuente de comprobación: [Git: representación y funcionamiento de merge](https://git-scm.com/docs/git-merge)

#### 10. Práctica comparativa de merge y rebase

##### 10.1. Crear la bifurcación

> La práctica utiliza un repositorio nuevo, con Git instalado e identidad configurada. `git switch -c main` presupone que la rama inicial todavía no se llama `main`; si ya tiene ese nombre, ese paso se omite.
>
> Primero se crea el commit base `C1`:

```bash
mkdir practica-git && cd practica-git
git init
git config user.name "nombreUsuario"
git config user.email "emailUsuario"
git switch -c main

echo "Base" > base.txt
git add . && git commit -m "C1: Base"
```

> Se crea `feature` y se confirma `C2`:

```bash
git switch -c feature
echo "Feature" > feature.txt
git add . && git commit -m "C2: Cambio en Feature"
```

> Después se vuelve a `main` y se confirma `C3`:

```bash
git switch main
echo "Main" > main.txt
git add . && git commit -m "C3: Cambio en Main"
```

> Las dos ramas han avanzado desde `C1`: `feature` contiene `C2` y `main` contiene `C3`. Los rótulos `C1`, `C2` y `C3` son nombres explicativos de los commits, no referencias creadas automáticamente por Git.

##### 10.2. Integrar con merge

```bash
git merge feature -m "C4: Merge Commit"
git log --oneline --graph --all
```

> La fusión registra `C4` con `C3` y `C2` como padres. El grafo debe mostrar las dos líneas conectadas; los identificadores concretos dependen de los commits creados.

##### 10.3. Comparar con rebase

> Para volver a la bifurcación del ejemplo se mueve `main` a `C3`. En el comando, `C3` debe sustituirse por su **hash real**. Este paso descarta las modificaciones no confirmadas que afecta `--hard` y se plantea dentro del repositorio de práctica.

```bash
git reset --hard C3

git switch feature
git rebase main

git switch main
git merge feature

git log --oneline --graph --all
```

> `rebase` reaplica el cambio de `C2` después de `C3`. Al integrar después `feature`, `main` puede avanzar mediante fast-forward: la historia queda `C1 → C3 → C2'`, sin un nuevo commit de fusión.
>
> El cambio de identificador de `C2` a `C2'` es la consecuencia de reaplicar su contenido sobre otro padre. La práctica compara estructuras de historia, aunque ambas integraciones incorporen los archivos de las dos líneas.

#### 11. Revert, reset, restore y clean

> **`git revert <commit>`** crea otro commit que invierte los cambios de uno anterior. Mantiene la historia publicada y permite compartir esa inversión como una modificación nueva.
>
> **`git reset <commit>`**, aplicado a la rama, mueve su referencia al commit indicado. El modo controla qué ocurre con el index y los archivos:

| Modo | Referencia de rama | Index | Working directory |
| --- | --- | --- | --- |
| `--soft` | Pasa al commit objetivo. | Se conserva. | Se conserva. |
| `--mixed`, predeterminado | Pasa al commit objetivo. | Se ajusta al objetivo. | Se conserva. |
| `--hard` | Pasa al commit objetivo. | Se ajusta al objetivo. | Se ajusta al objetivo, descartando cambios afectados. |

> Reset cambia qué commits se alcanzan desde esa rama; otros nombres o el reflog pueden seguir haciendo referencia a objetos anteriores. El modo hard puede perder trabajo que no se había guardado.
>
> **Restore** actúa sobre archivos. `git restore <archivo>` recupera normalmente la versión del index para el archivo de trabajo; `git checkout -- <archivo>` conserva esa forma de restauración.
>
> **Clean** elimina archivos no seguidos por Git. No debe confundirse con restaurar el contenido de un archivo versionado ni con invertir un commit. El alcance depende de sus opciones.

#### 12. Práctica de revert y reset

> En otro repositorio nuevo se crea `file.txt` y se confirman tres versiones. Se añade la preparación necesaria antes de los comandos del ejemplo:

```bash
mkdir practica-revert && cd practica-revert
git init
git config user.name "nombreUsuario"
git config user.email "emailUsuario"

echo "Línea 1" > file.txt
git add file.txt
git commit -m "Commit 1: Línea 1"

echo "Línea 2" >> file.txt
git commit -am "Commit 2: Línea 2"

echo "Línea 3" >> file.txt
git commit -am "Commit 3: Línea 3"
```

> `-a` prepara modificaciones de archivos ya seguidos; `file.txt` entró en seguimiento con el primer `add`. Para invertir el último commit:

```bash
git revert HEAD
```

> Se añade un commit de inversión y se conserva la historia de los tres commits originales. El archivo recupera el contenido previo a la adición de la tercera línea.
>
> Para reproducir el retorno al **Commit 2** mostrado en el ejemplo, se utiliza su identificador, aquí representado como `HASH_COMMIT_2`:

```bash
git reset --hard HASH_COMMIT_2
git log --oneline --graph --all
```

> [!warning] Corrección
> En el material aparece que reset elimina snapshots del repositorio y se muestra `git reset --hard` sin objetivo para volver al Commit 2. Reset mueve referencias y ajusta index/archivos según su modo; sin objetivo utiliza `HEAD` y no retrocede a otro commit. Para ese resultado debe indicarse el hash del Commit 2, como sí hace la captura de terminal.
> Fuente de comprobación: [Git: reset y sus modos](https://git-scm.com/docs/git-reset)

> **Revert** conserva la inversión dentro de la historia; **reset** cambia el extremo de la rama y, con hard, sus archivos. La comparación debe observar tanto el historial como el contenido del directorio de trabajo.

#### 13. Git hooks y automatización local

> Un **hook** es un script que Git ejecuta antes o después de determinados eventos. En la disposición habitual se guarda en `.git/hooks/` y debe ser ejecutable.
>
> `pre-commit` permite validar antes de confirmar; `pre-push` puede ejecutar pruebas antes de publicar; `post-merge` puede realizar tareas posteriores a la integración, como instalar dependencias. Los hooks personalizan el trabajo local y complementan CI/CD.

##### 13.1. Crear un pre-commit

> El ejemplo bloquea un commit si encuentra `FIXME` en los archivos examinados:

```bash
mkdir -p .git/hooks
echo '#!/bin/bash' > .git/hooks/pre-commit
echo 'if grep -q "FIXME" *; then echo "Error: No puedes hacer commit con FIXME en el código"; exit 1; fi' >> .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

> La primera redirección crea el archivo; la segunda añade la condición. `grep -q` busca el texto y `exit 1` indica fallo, interrumpiendo la confirmación cuando existe una coincidencia.
>
> El patrón `*` examina entradas del directorio de trabajo, no exclusivamente el contenido preparado. Este ejemplo es una comprobación local sencilla: no recorre por sí solo todos los subdirectorios ni representa una validación completa del snapshot.

##### 13.2. Comprobar el bloqueo

```bash
echo "Este es un problema pendiente FIXME" > test.txt
git add test.txt
git commit -m "Añadiendo archivo con FIXME"
```

> La coincidencia en `test.txt` provoca el bloqueo previsto por el hook. Para confirmar con esa regla debe desaparecer la coincidencia; si cambia el archivo, hay que volver a preparar su nueva versión.
>
> Los hooks locales y las comprobaciones del servidor son mecanismos distintos. Compartir commits no instala automáticamente todos los hooks de cada desarrollador.

#### 14. Seleccionar un cambio con cherry-pick

> **`git cherry-pick`** aplica el cambio de un commit concreto sobre la rama actual. Permite trasladar una corrección, realizar un backport o incorporar un hotfix sin fusionar todos los cambios de la rama de origen.
>
> Por ejemplo, si `develop` contiene un commit `F` con una corrección necesaria en `main`, puede seleccionarse ese commit en lugar de integrar también el resto de funcionalidades.
>
> Primero se identifica el commit en el historial y se cambia a la rama de destino:

```bash
git log --oneline --graph --all
git switch main
git cherry-pick a1b2c3d
```

> `a1b2c3d` es el identificador ilustrativo de la corrección y debe sustituirse por el real. Si hay conflictos, se resuelven los archivos, se preparan y se continúa:

```bash
git add .
git cherry-pick --continue
```

> La operación incorpora el cambio como un commit en la línea de destino, normalmente con otro identificador. No incorpora automáticamente todos sus antecesores de la rama de origen.
>
> Seleccionar cambios reduce integraciones innecesarias, pero puede causar conflictos o inconsistencias si el cambio depende de otros que no se trasladan. La coordinación cobra importancia cuando varias personas mantienen distintas ramas.

### III. Plataformas de colaboración y CI/CD

#### 15. Integración y entrega continuas

> **Continuous Integration (CI)** automatiza la integración y comprobación de los cambios. **Continuous Delivery (CD)** amplía el proceso para preparar y entregar software de forma repetible y fiable.
>
> El flujo conecta **Build → Test → Security Checks → Release → Deploy Stage → Deploy Prod**: construcción, pruebas, comprobaciones de seguridad, preparación de una versión y despliegues en staging y producción.
>
> La delimitación de las etapas depende del pipeline. La entrega continua mantiene la capacidad de liberar; la aprobación del paso a producción puede formar parte de la política de entrega. Un despliegue completamente automático añade esa decisión al flujo automatizado.
>
> Código, configuración y definición del pipeline pueden versionarse juntos para relacionar una ejecución con los cambios que la originaron.

#### 16. GitLab: plataforma y arquitectura

> **GitLab** aloja repositorios Git e integra herramientas para el ciclo de desarrollo: CI/CD, issues, tableros Kanban, planificación ágil, escaneo de código, control de acceso y auditoría. **Auto DevOps** proporciona automatización mediante configuraciones predefinidas.
>
> **GitLab.com** es una modalidad administrada por el proveedor. **GitLab Self-Managed** permite gestionar la instalación y su infraestructura, por ejemplo en un entorno on-premises.
>
> Entre sus componentes, **Gitaly** gestiona las operaciones sobre repositorios y **Puma** sirve la aplicación web de GitLab.

> [!warning] Corrección
> En el material aparece que GitLab se basa en microservicios, pero su aplicación principal es un monolito Rails acompañado de servicios. La evolución hacia módulos no convierte toda su arquitectura en un conjunto de microservicios independientes.
> Fuente de comprobación: [GitLab: descomposición del monolito Rails](https://handbook.gitlab.com/handbook/engineering/architecture/design-documents/modular_monolith/)

#### 17. Pipeline de GitLab

> Los pipelines personalizados se definen en **`.gitlab-ci.yml`**. Los **jobs** contienen comandos y los **stages** los agrupan. Los runners y sus ejecutores aportan el entorno donde se ejecutan.
>
> Este ejemplo define las etapas build, test y deploy:

```yaml
stages:
  - build
  - test
  - deploy

build:
  stage: build
  script:
    - echo "Building the project"

test:
  stage: test
  script:
    - echo "Running tests"

deploy:
  stage: deploy
  script:
    - echo "Deploying application"
```

> Los jobs pertenecen a etapas sucesivas. En el flujo básico, una etapa posterior comienza tras superar la anterior; los jobs de una misma etapa pueden ejecutarse en paralelo.
>
> Los comandos `echo` ilustran la estructura, pero no compilan, prueban ni despliegan una aplicación real. Para hacerlo deben sustituirse por las operaciones del proyecto y disponer de runners con sus herramientas y permisos.

#### 18. Auto DevOps

> **Auto DevOps** detecta el lenguaje y framework y utiliza un pipeline predefinido, sin exigir un `.gitlab-ci.yml` personalizado. Puede integrar construcción, pruebas, calidad, seguridad y rendimiento.
>
> En el modelo con contenedores, empaqueta la aplicación y utiliza **Helm** para desplegarla en Kubernetes. El flujo es **push → pipeline automático → despliegue, si está preparado → observación y análisis de seguridad**.
>
> La automatización presupone un proyecto compatible, runners y los recursos de despliegue configurados. Detectar y construir la aplicación no prepara automáticamente cualquier clúster o credencial.
>
> La monitorización aporta métricas para evaluar el funcionamiento y puede complementarse con la consulta de logs del entorno.

> [!warning] Corrección
> En el material aparece que Prometheus permite visualizar métricas y logs, pero Prometheus recoge y almacena métricas como series temporales. Los logs requieren mecanismos de registro y consulta distintos.
> Fuente de comprobación: [Prometheus: modelo y funciones de monitorización](https://prometheus.io/docs/introduction/overview/)

#### 19. GitHub y gestión del código

> **GitHub**, propiedad de Microsoft, es una plataforma basada en Git para colaborar en proyectos públicos y privados. Incorpora **GitHub Actions** para automatización, **Issues y Projects** para planificación, **Dependabot** y escaneo de código para seguridad, y **Copilot** como asistente de programación basado en IA.
>
> La gestión del código puede imponer **protección de ramas**, revisiones obligatorias de PRs y comprobaciones antes de fusionar. El escaneo de código, incluido el asociado a GitHub Advanced Security, permite detectar problemas durante el desarrollo.
>
> Las **firmas GPG** permiten verificar criptográficamente una firma asociada al commit y su clave. Su utilidad requiere relacionar esa clave con la identidad correspondiente; el nombre de autor escrito en el commit no constituye por sí solo esa verificación.

#### 20. Comparación de plataformas

| Característica | GitLab | GitHub | Bitbucket |
| --- | --- | --- | --- |
| CI/CD | GitLab CI/CD. | GitHub Actions. | Bitbucket Pipelines. |
| Hosting en nube | Disponible. | Disponible. | Disponible. |
| Repositorios privados y modalidades gratuitas | Disponible, con límites de la modalidad. | Disponible, con límites de la modalidad. | Disponible, con límites de la modalidad. |
| Issues y planificación | Issues y tableros. | Issues y Projects. | Herramientas de seguimiento y planificación del ecosistema Atlassian. |
| SSO / SAML | Opciones según modalidad y plan. | Opciones según modalidad y plan. | Opciones según modalidad y plan. |

> La comparación de capacidades no implica que todos los planes incluyan las mismas funciones, cuotas o permisos. GitHub Actions forma parte de GitHub; utilizar ese componente es el mecanismo de CI/CD de la plataforma.
>
> Entre GitLab y GitHub destacan **Auto DevOps**, como función específica de GitLab, y distintas formas de integrar seguridad, Kubernetes y proveedores cloud. GitHub puede participar en GitOps mediante sus workflows y herramientas externas; GitLab incorpora capacidades de integración y despliegue para Kubernetes.
>
> Ambas plataformas pueden integrarse con Azure, aunque el mecanismo y la configuración sean diferentes.

> [!warning] Corrección
> En el material aparece que GitLab no tiene integración con Azure, pero GitLab documenta cómo integrar sus jobs de CI/CD con Azure mediante autenticación federada.
> Fuente de comprobación: [GitLab: integración de CI/CD con Azure](https://docs.gitlab.com/ci/cloud_services/azure/)

### IV. GitOps y entrega declarativa

#### 21. Estado deseado, estado actual y reconciliación

> **GitOps** aplica un enfoque declarativo a la entrega de aplicaciones y la operación de infraestructura, utilizando un flujo de trabajo familiar para los desarrolladores.
>
> Sus principios son **tratar las definiciones como código**, conservar en **Git la fuente de verdad del estado deseado** y automatizar su **reconciliación** con el estado actual. El repositorio describe qué debe existir; el clúster refleja lo que existe realmente.
>
> Un controlador observa ambos estados y actúa según su política de sincronización. Una diferencia entre ellos es **drift**, o deriva de configuración. Por ejemplo, cambiar manualmente un recurso del clúster puede producir una diferencia respecto a lo versionado.
>
> El ciclo es **monitorizar → detectar drift → tomar una acción → sincronizar/desplegar → monitorizar**. Versionar una configuración permite revisarla, pero mantenerla reconciliada exige un mecanismo que vuelva a comparar y aplicar el estado.

#### 22. Modelo de entrega de aplicaciones

> El modelo separa un **repositorio de código fuente**, un **repositorio de configuración** y un **registro de imágenes**:

![[apuntes-b84216d1df23-p0008-4a52595c4260.png]]

> El recorrido es:
>
> 1. Un cambio del código dispara **CI**, que construye y verifica la aplicación.
> 2. La imagen construida se publica en el **Image Registry**.
> 3. Una PR propone actualizar la configuración que identifica la imagen o la versión deseada.
> 4. **CD** utiliza la configuración aprobada para sincronizar los recursos de Kubernetes.
> 5. El clúster obtiene las imágenes del registro y se sigue observando su estado.
>
> Código fuente, imagen y manifiestos representan objetos distintos. Aprobar un cambio en el código no actualiza necesariamente el manifiesto que selecciona qué imagen se despliega.
>
> Las etiquetas **push/pull** describen dónde se inicia la sincronización: un componente central puede aplicar cambios a un clúster remoto; un controlador situado en el clúster puede recuperar las definiciones que debe gestionar. Obtener una imagen desde el registro es otra transferencia distinta.
>
> Los beneficios de GitOps son:
>
> - **Workflow estándar**: reutilizar Git y la revisión de cambios.
> - **Seguridad**: revisar antes de aplicar y detectar cambios fuera de la configuración declarada.
> - **Visibilidad y auditoría**: relacionar los cambios con el historial.
> - **Consistencia multiclúster**: gestionar configuraciones y despliegues de distintos entornos de manera coherente.
>
> Esos beneficios dependen de versionar los cambios relevantes y de configurar la reconciliación. El historial de Git describe lo declarado; la observación del clúster permite comprobar lo que está aplicado.

#### 23. Argo CD

> **Argo CD** utiliza configuraciones de aplicaciones y clústeres versionadas en Git para gestionar su entrega en Kubernetes. Compara el estado declarado con el real y permite sincronizarlo, visualizar diferencias y consultar el estado e historial.
>
> Sus capacidades incluyen:
>
> - **Sincronización automática**, cuando se habilita la política correspondiente.
> - **Detección y corrección de drift**, según las opciones de reconciliación.
> - **Control del orden de sincronización** para despliegues con dependencias.
> - **Rollback y rollforward** hacia revisiones de configuración.
> - **Plantillas de manifiestos**, con herramientas como Helm y Kustomize.
> - **Visibilidad del estado de sincronización** y su historia.
>
> La monitorización no implica que todo cambio manual se corrija automáticamente: la política determina cuándo se sincroniza y si se habilita autorreparación. Asimismo, una revisión de Git solo describe los recursos y artefactos que su configuración referencia.
>
> En un flujo con sincronización automática, mantener una vuelta a una versión anterior requiere que el estado deseado en Git refleje esa decisión. Un rollback operativo y la actualización de la configuración versionada deben coordinarse.

#### 24. Estrategias de despliegue

> Argo CD puede organizarse con distintos ámbitos de gestión:

![[apuntes-b84216d1df23-p0012-dee715d3b440.png]]

| Estrategia | Ubicación y alcance |
| --- | --- |
| **Central Hub (Push)** | Una instancia central obtiene la configuración Git y aplica cambios a clústeres remotos. |
| **Cluster Scoped (Pull)** | Una instancia dentro del clúster recupera las configuraciones de sus servicios. |
| **Application Scoped (Pull)** | El ámbito se limita a aplicaciones y sus namespaces. |

> En el ámbito de clúster se pueden gestionar autenticación, registro, networking, almacenamiento, instalación de operadores y namespaces. En el ámbito de aplicación se gestionan los despliegues y configuraciones de aplicaciones como **App A** y **App B** en sus espacios.
>
> La diferencia combina **dónde se ejecuta el controlador** y **qué administra**. Una configuración central puede abarcar varios clústeres; una configuración por aplicación delimita sus recursos y responsabilidades.

#### 25. Arquitectura ampliada y bootstrap

##### 25.1. CI, CD, seguridad y gestión multiclúster

> La arquitectura ampliada asigna funciones diferentes a **Tekton**, **Argo CD**, el registro de imágenes y los servicios de gestión y seguridad de clústeres:

![[apuntes-b84216d1df23-p0010-05d8887db290.png]]

> Un **Git Event** del repositorio de aplicación dispara CI. Se recuperan los pipelines y tareas Tekton, se construye la aplicación y se publica su imagen.
>
> El repositorio de configuración alimenta CD mediante Argo CD, que sincroniza los entornos **Dev, Stage y Prod**. Los entornos recuperan sus imágenes del registro. **Advanced Cluster Security** integra comprobaciones de seguridad y cumplimiento; **Advanced Cluster Management** gestiona el ciclo de vida de los clústeres a escala.
>
> Las tres capas —**CI, CD y Scale**— separan construcción, entrega y gestión del conjunto de entornos. La integración de controles de seguridad en ese recorrido corresponde al enfoque **DevSecOps**.

##### 25.2. Capacidades de la solución GitOps

> La solución combina gestión declarativa de configuraciones **multiclúster**, instalación y actualización automatizadas de Argo CD mediante un operador disponible en **OperatorHub**, y visibilidad de despliegues e historia desde la consola de Kubernetes y herramientas de observabilidad.
>
> **GitOps Application Manager CLI**, o **KAM**, facilita el *bootstrapping* de un flujo con una organización predefinida. El comando presentado es:

```bash
kam bootstrap
```

> Su uso presupone la CLI y los accesos preparados. El esquema conecta un **push de código** con un webhook que activa Tekton; Tekton publica imágenes. Los cambios de manifiestos pasan por PRs; Argo CD recupera la configuración y sincroniza desarrollo, staging y producción.
>
> Bootstrap prepara la organización y componentes del flujo. Las entregas posteriores siguen necesitando commits, imágenes, configuraciones y credenciales adecuados para los entornos correspondientes.

### V. Pipelines como código y GitHub Actions

#### 26. CI/CD cloud-native

> **Cloud-native CI/CD** se diseña para aplicaciones en contenedores y ejecución sobre Kubernetes. El modelo combina contenedores, una experiencia de ejecución bajo demanda o *serverless* para el usuario, y soporte para microservicios y equipos distribuidos.
>
> En la comparación se contrasta un motor de CI tradicional administrado por el equipo con una plataforma de pipelines que gestiona más aspectos de ejecución:

| Aspecto | Modelo tradicional | Modelo cloud-native presentado |
| --- | --- | --- |
| Entorno previsto | Máquinas virtuales y motor de CI. | Contenedores y Kubernetes. |
| Operación del motor | IT Ops mantiene el motor. | La plataforma proporciona la ejecución como servicio. |
| Dependencias compartidas | Plugins del motor compartidos. | Entornos de ejecución aislados para pipelines. |
| Ciclo de actualización | Dependencias de plugins con ciclos propios. | Herramientas y tareas distribuidas como imágenes. |
| Relación con Kubernetes | Integración externa o adicional. | Recursos nativos de Kubernetes. |
| Persistencia | Administración específica del motor. | Gestión a través de la plataforma. |
| Configuración | Integrada en el entorno del motor. | Configuración declarativa, por ejemplo con ConfigMaps. |

> La reducción de trabajo operativo se refiere a la experiencia de quien consume el servicio. La plataforma y su Kubernetes siguen necesitando operación por parte de quien los administra.
>
> Utilizar imágenes y recursos declarativos permite gestionar las herramientas del pipeline junto con su configuración. El aislamiento y la persistencia dependen de cómo se configure la plataforma.

#### 27. Pipeline as Code

> **Pipeline as Code** conserva la definición del pipeline en Git. La definición se recupera para ejecutarse y sus cambios pueden pasar por el mismo proceso de revisión que el código.
>
> El modelo presentado vincula la ejecución a eventos **push** y **pull request**, publica el estado junto al commit o PR e integra resultados con **GitHub Checks**. La implementación ilustrada con **OpenShift Pipelines / Pipelines as Code** permite también solicitar reinicios mediante comentarios de PR.
>
> Esas integraciones conectan tres elementos: **definición versionada**, **evento que inicia la ejecución** y **resultado asociado al cambio**. Un archivo YAML describe el proceso; runners o recursos de la plataforma realizan las tareas.

#### 28. Elementos de GitHub Actions

> **GitHub Actions** es una plataforma de automatización CI/CD integrada en GitHub. Los workflows YAML responden a eventos del repositorio y pueden compilar, probar o desplegar, ejecutar scripts, utilizar contenedores y reutilizar acciones.

| Elemento | Función |
| --- | --- |
| **Workflow** | Proceso de automatización definido en un archivo YAML dentro de `.github/workflows/`. |
| **Job** | Conjunto de pasos asignado a un runner. |
| **Step** | Paso de un job que ejecuta una acción o un comando. |
| **Runner** | Entorno o máquina que ejecuta el job. |
| **Action** | Componente reutilizable que realiza una tarea. |

> Un workflow puede tener varios jobs, incluso paralelos; dentro de un job los pasos se ordenan. **`uses`** selecciona una acción y **`run`** ejecuta comandos.
>
> La automatización se integra con repositorios, issues y releases. La personalización permite reutilizar acciones entre proyectos y organizar distintos trabajos según las necesidades de construcción, prueba y entrega.

#### 29. Ejemplos de integración continua

##### 29.1. Instalar dependencias y probar

> El primer workflow se guarda, por ejemplo, como `.github/workflows/ci.yml`. Requiere un proyecto con `package.json`, un script de prueba accesible con `npm test` y Node.js/npm disponibles en el runner con una versión adecuada al proyecto.
>
> El workflow utiliza `actions/checkout@v2`, instala dependencias y ejecuta las pruebas:

```yaml
name: CI Pipeline
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: npm install
      - name: Run tests
        run: npm test
```

> **`on`** declara los eventos; **`jobs.build`** identifica el trabajo; **`runs-on`** selecciona el runner. Checkout obtiene los archivos del repositorio para que los comandos posteriores puedan utilizarlos.
>
> El job se llama `build`, pero sus comandos realizan instalación y pruebas. El nombre no añade una compilación ni un despliegue que no estén definidos.

##### 29.2. Variante con pasos nombrados

> La segunda variante utiliza `actions/checkout@v3` y nombra el paso de checkout. Se añade la instalación de dependencias necesaria antes de las pruebas; conserva los mismos eventos y el mismo runner:

```yaml
name: CI Pipeline
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      - name: Install dependencies
        run: npm install
      - name: Run tests
        run: npm test
```

> Estas definiciones son **alternativas** para el workflow básico. Utilizar ambas en archivos diferentes generaría dos workflows que responden a los mismos eventos.
>
> El resultado se inspecciona en los jobs y logs de la ejecución. Un fallo en las pruebas indica que el cambio no ha superado esa comprobación; completar el workflow únicamente demuestra lo que verifican sus pasos.

#### 30. Workflow de despliegue en Kubernetes

> GitHub Actions puede validar cambios, construir imágenes y actualizar las configuraciones utilizadas por **Argo CD** o **Flux**. También puede ejecutar un despliegue directo.
>
> En el esquema de integración, un commit activa la construcción —ilustrada con **Google Cloud Build**—, se actualiza la configuración en Git y Argo CD recupera ese cambio para sincronizar Kubernetes. GitHub Actions puede desempeñar las tareas de automatización del mismo recorrido.
>
> El siguiente ejemplo responde a un **push en `main`** y aplica los manifiestos de `k8s/`. Necesita `kubectl` disponible, manifiestos válidos y un kubeconfig con acceso al clúster. Se incorpora la preparación del archivo de credenciales usando `KUBE_CONFIG`.
>
> Para este bloque se supone que **`secrets.KUBE_CONFIG` contiene el texto completo de un kubeconfig**, no una ruta ni su representación en base64. Debe crearse previamente el secreto con ese formato.

```yaml
name: Deploy to Kubernetes
on:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      KUBE_CONFIG: ${{ secrets.KUBE_CONFIG }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      - name: Configure cluster access
        run: |
          printf '%s' "$KUBE_CONFIG" > "$RUNNER_TEMP/kubeconfig"
          echo "KUBECONFIG=$RUNNER_TEMP/kubeconfig" >> "$GITHUB_ENV"
      - name: Apply Kubernetes Manifests
        run: kubectl apply -f k8s/
```

> El paso de preparación escribe el archivo y comunica su ruta mediante **`KUBECONFIG`** a los pasos posteriores. `KUBE_CONFIG` es el nombre de una variable propia; asignarle un secreto no configura por sí solo la autenticación de `kubectl`.
>
> `kubectl apply -f k8s/` aplica las definiciones del directorio al clúster del contexto seleccionado. Es un **despliegue iniciado desde CI**. Para disponer además de detección de drift y reconciliación persistente debe existir el controlador GitOps y su configuración; ejecutar apply una vez no incorpora automáticamente ese ciclo.
>
> Tras la ejecución se inspeccionan los recursos, el entorno de destino y el estado del despliegue. Aplicar los objetos no garantiza por sí solo que la aplicación haya alcanzado un estado saludable.

#### 31. Secretos, permisos y revisiones

> Los secretos se referencian mediante el contexto **`secrets`**, evitando escribir valores reales en la definición del workflow. **`secrets.GITHUB_TOKEN`** proporciona el token de GitHub generado para la ejecución; un secreto como **`secrets.KUBE_CONFIG`** contiene las credenciales específicas que se hayan preparado para otro servicio.
>
> Los **permisos read/write** se limitan a las operaciones necesarias. En el ejemplo anterior, `contents: read` permite obtener el código, pero no concede permisos en Kubernetes: estos dependen de las credenciales y autorización del clúster.
>
> La revisión de **pull requests** permite controlar qué configuración se incorpora a la rama. Para exigirla se configuran reglas de protección o revisión de la rama.
>
> Los **required reviewers** de un environment añaden otra aprobación: autorizan el job de despliegue que referencia ese entorno. Esa aprobación y la revisión del código de una PR se sitúan en etapas diferentes.
>
> GitHub Actions favorece automatización, trazabilidad y auditoría cuando la configuración relevante queda versionada. Puede integrarse con AWS, Azure y Google Cloud, usando los mecanismos de acceso adecuados. La revisión de PRs y las comprobaciones previas apoyan el control sobre los cambios que se entregan.

#### 32. Integración con herramientas GitOps

| Herramienta | Función en el entorno |
| --- | --- |
| **Argo CD** | Sincronización de aplicaciones y configuraciones declarativas en Kubernetes. |
| **FluxCD** | Controladores para gestionar entrega declarativa mediante GitOps. |
| **Terraform** | Aprovisionamiento de infraestructura como código, que puede automatizarse dentro del proceso. |

> Las herramientas tienen responsabilidades diferentes. Un pipeline puede construir y validar; Terraform puede gestionar infraestructura; Argo CD o Flux pueden reconciliar las aplicaciones. Integrarlas requiere definir qué componente administra cada recurso.
>
> Para solicitar una sincronización de una aplicación existente en Argo CD, el paso presentado es:

```yaml
- name: Trigger ArgoCD Sync
  run: argocd app sync my-app
```

> Es un **fragmento de steps**, que se incorpora a un job; no constituye un workflow completo. Requiere la CLI `argocd`, acceso autenticado al servidor, permisos de sincronización y una aplicación llamada `my-app` ya configurada.
>
> El comando pide sincronizar la aplicación con su estado objetivo. No crea por sí solo el registro de la aplicación ni construye una nueva imagen. La configuración Git determina qué recursos y versión deben aplicarse.

### VI. Resumen Final

> **Git** conserva historia distribuida mediante commits, ramas y referencias. Working directory, index y repositorio permiten distinguir modificación, preparación y confirmación. Stash aparta trabajo temporal y los remotos permiten intercambiar commits.
>
> **Merge** conserva e integra historias; **rebase** reaplica commits sobre otra base; **cherry-pick** selecciona un cambio concreto. **Revert** registra una inversión, **reset** cambia referencias y ajusta archivos según su modo, **restore** recupera archivos y **clean** elimina contenido no seguido.
>
> **GitLab y GitHub** conectan colaboración, revisión y automatización. Pipelines YAML y runners ejecutan los pasos definidos; Auto DevOps aporta un flujo preconfigurado que requiere un entorno preparado.
>
> **GitOps** utiliza una configuración declarativa versionada y un ciclo de reconciliación. Código fuente, configuración e imágenes tienen funciones distintas; Argo CD o Flux mantienen la entrega coordinada con el estado deseado.
>
> **CI/CD cloud-native y Pipeline as Code** integran tareas versionadas, eventos y resultados observables. **GitHub Actions** organiza workflows en jobs y steps para validar, construir y desplegar.
>
> La entrega requiere herramientas disponibles, dependencias, autenticación, permisos y revisiones adecuados. Un comando de despliegue y una reconciliación continua ofrecen capacidades diferentes que deben comprobarse en el entorno.


