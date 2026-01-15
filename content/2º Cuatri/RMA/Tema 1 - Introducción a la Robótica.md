### I. Historia de la Robótica
#### 1. Siglos XII y XIII
> En esta etapa aparecen **autómatas** como precursores de los robots: mecanismos capaces de ejecutar acciones “por sí solos”.
> - **Al-Jazari** desarrolla dispositivos como:
>     - Un **escanciador de vino automático**.
>     - Un **mecanismo dispensador** de jabón y toallas.
>     - Una **orquesta-autómata** que funcionaba con la **fuerza del agua**.  
>         **Conexión:** marca el paso de “máquinas curiosas” a **sistemas mecánicos diseñados para automatizar tareas**.
#### 2. Siglo XVIII
> Se consolidan autómatas muy sofisticados, diseñados para **imitar comportamientos animales**.
> - **1739: “El Pato Digestor” (Le canard digérateur)** de **Jacques de Vaucanson**:
>     - Tamaño real, en **cobre recubierto de oro**.
>     - Más de **400 piezas móviles**.
>     - Considerado una primera “**mascota**” robótica.
>     - Simulaba un **sistema digestivo artificial**: ingería granos, “digería” y excretaba.
>     - También podía **graznar, caminar, mover la cabeza y batir las alas**.  
>         **Conexión:** refuerza la idea de robot como **imitación mecánica de seres vivos**.
#### 3. Siglo XX
> En el siglo XX se fija el **imaginario cultural** (literatura) y despega la **robótica industrial**.
> - **1920–1921:** **Karel Čapek** acuña el término **“robot”** en la obra **R.U.R**.
> - **1942:** **Isaac Asimov** formula las **Tres Leyes de la Robótica** (y en **1985** añade la **Ley Cero**).
> - **1954:** **George C. Devol** registra la patente de lo que se considerará el **primer robot**.
> - **1956:** Devol y **Joseph Engelberger** fundan **Unimation** (primera empresa de robótica); **1961** se instala el **primer brazo robótico**.
> - Evolución por décadas:
> 	- **1960:** brazos para **fabricación de precisión** y **manejo de material radiactivo**.
> 	- **1970:** se generaliza en **industria manufacturera** y aparecen usos fuera de fábricas (rescate, espacio, medicina…).
> 	- **1980:** se estudia la conexión “**percepción–actuación**” inteligente.
> 	- **1990:** robots en entornos **no estructurados** → aumenta la **autonomía** (robots de campo, servicio, exoesqueletos).  
#### 4. Siglo XXI
> Desde el año 2000 la robótica se orienta más al **ser humano** y a la convivencia segura robot-persona.
> - **Robótica centrada en el ser humano**: robots que pueden **compartir el espacio físico** con personas de forma segura.
> - Mejora del **control y la destreza** apoyándose en técnicas de **inteligencia artificial** (p. ej., **DRL**).

### II. Tipos de Robots
#### 1. Manipuladores
> Robots (típicamente industriales) diseñados para **manipular piezas/herramientas** con un **brazo mecánico** en tareas repetitivas y precisas.
#### 2. Colaborativos (Cobots)
> Robots pensados para **trabajar junto a personas** en una **zona definida**, priorizando la **seguridad**.
> - Término acuñado en **2003** (RIA).
> - Suelen ser **ligeros/portables**, con **sensores** para detectar personas/entorno.
> - **Fáciles de programar** (guiado a mano o interfaz gráfica) y adaptables a nuevas tareas.
###### 2.1. Modelos de Operación Colaborativa
> - **Parada de Seguridad Monitorizada:** el robot se **para** si entra una persona; luego **reanuda** al salir (motores alimentados; suelen seguir vallas).
> - **Guiado a Mano:** el robot se **detiene** y el operario lo **reposiciona/controla** manualmente (útil en lotes pequeños).
> - **Velocidad y Separación Monitorizadas:** robot y persona se mueven a la vez manteniendo **distancia segura**; el robot **reduce velocidad** y puede pararse.
> - **Limitación de Potencia y Fuerza:** se permite **contacto**; el robot **limita fuerza/par** (para tareas lentas y cargas moderadas).
#### 3. Con Ruedas
> Robots móviles cuya **locomoción principal** se basa en **ruedas**, típicos en entornos relativamente planos y estructurados por su **simplicidad y eficiencia**.
#### 4. Con Patas
> Robots que se desplazan con **extremidades articuladas**, pensados para **terrenos irregulares** donde las ruedas tienen dificultades (más complejos, pero más versátiles en obstáculos).
#### 5. Voladores
> Robots aéreos (drones/UAV) que se mueven en **3D**, útiles cuando interesa **acceso desde el aire** o cubrir grandes áreas sin depender del terreno.
#### 6. Miscelánea
> Categoría “cajón de sastre” para robots que no encajan en las anteriores: **formas híbridas**, locomociones menos comunes o robots con **propósitos/entornos muy específicos**.

### III. Ciclo Ver-Pensar-Actuar
#### 1. Preguntas Clave
> Un robot móvil debe ser capaz de **navegar por el entorno** para realizar sus tareas.  
> Para ello debe responder a tres preguntas:
> - **¿Dónde estoy?** (Where am I?)
> - **¿A dónde voy?** (Where am I going?)
> - **¿Cómo llego allí?** (How do I get there?)
> 
> Para conseguirlo, necesita:
> - Un **modelo del entorno** → un **mapa**.
> - **Percibir** y entender lo que le rodea.
> - Determinar su **pose** (posición y orientación) respecto al mapa.
> - **Planificar un camino (path)** al objetivo y generar los **comandos** para seguirlo.
#### 2. AGV vs AMR
> **AGV (Automated Guided Vehicles):**
> - Siguen una **ruta fija** guiándose por hilos conductores, bandas magnéticas, códigos QR o haces láser (**LGV**).
> - Requieren **adaptaciones sustanciales del entorno**.
> 
> **AMR (Autonomous Mobile Robots):**
> - **Crean un mapa** de las instalaciones con sensores avanzados.
> - Pueden **replanificar dinámicamente** para esquivar obstáculos.
#### 3. Aplicación del Ciclo
> El ciclo **Ver–Pensar–Actuar (see-think-act)** se puede entender así:
> - **Ver (Percepción):** _Sensing_ (captura de datos) → _Information Extraction_ (extraer información útil) → construir un **modelo/mapa local**.
> - **Pensar (Cognición):** _Localization / Map Building_ produce la **posición en el mapa global** → _Path Planning_ genera un **path** a partir de esa posición y de las **mission commands**.
> - **Actuar (Control de Movimiento):** _Path Execution_ traduce el path a **comandos de actuador** → _Acting_ ejecuta el movimiento en el **mundo real**, cerrando el bucle con nueva percepción.

![[Pasted image 20260115172007.png]]