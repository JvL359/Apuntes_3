### I. Sensores para Robótica
#### 1. Clasificación
> Se plantea con **dos preguntas**: **qué miden** y **cómo lo miden**.
> Por **qué miden**, se distinguen los **sensores propioceptivos (PC)**, que observan **variables internas del robot** (por ejemplo, velocidad de motores, ángulos articulares o tensión de batería), frente a los **sensores exteroceptivos (EC)**, que captan información del **entorno** (por ejemplo, distancias a objetos, intensidad de luz o apariencia visual).
> Por **cómo lo miden**, hay **sensores pasivos (P)**, que miden la energía ya presente en el ambiente, y **sensores activos (A)**, que **emiten energía** y analizan su efecto. En los activos se destaca que la interacción con el entorno es más controlada, pero también que la variable de interés puede verse afectada y que puede haber **interferencias entre sensores**.
> La tabla del tema concreta ejemplos típicos: **táctiles/proximidad**, **posición y velocidad angulares** (encoders, synchros, resolvers), **orientación e inerciales** (giroscopios, inclinómetros, IMU), **balizas/GNSS**, **velocidad (radar Doppler)**, **distancia** (ultrasonidos, IR, ToF, LiDAR, luz estructurada) y **visión** (cámaras CCD/CMOS), junto con su etiquetado **PC/EC** y **A/P** según el caso.
#### 2. Posición y Velocidad Angular
> En el tema, los **codificadores rotatorios (encoders)** se presentan como dispositivos electromecánicos que convierten la **posición del eje** de un motor en una señal **analógica o digital**, y se usan para hacer **odometría**.
> Se distinguen **encoders absolutos**, que **mantienen la posición** aunque se quite la alimentación, y **encoders incrementales**.
> Para un **encoder relativo** con **N ranuras** uniformemente distribuidas, el desplazamiento angular entre dos instantes se estima contando el incremento de ranuras y escalándolo por $\pi/N:$ 
> $\Delta\theta=\big(\text{ranuras\_totales}_t-\text{ranuras\_totales}_{t-\Delta t}\big)\cdot\frac{2\pi}{N}, \qquad \text{con } \text{ranuras\_totales}_{t=0}=0$ 
> A partir de ahí, la velocidad angular se obtiene por derivada discreta: $\omega=\frac{\Delta\theta}{\Delta t}$
> El material advierte un caso práctico: **a bajas velocidades** la medida puede salir **nula**, y se propone **aumentar N** o el **periodo de muestreo Δt**.
> Si el motor está acoplado a una rueda de radio R, se pasa a magnitudes lineales con:
> $\Delta s=\Delta\theta\cdot R, \qquad v=\omega\cdot R$
#### 3. Sensores de Velocidad (Doppler)
> Un **Radar Doppler** mide velocidad usando el **efecto Doppler**: detecta cambios de frecuencia en microondas (76–77 GHz) debidos al movimiento relativo entre el emisor y el objeto sobre el que rebota la señal.
> - **RADAR** es acrónimo de _RAdio Detection And Ranging_.
> - Ventajas: excelente detección a largas distancias (hasta ~250 m), buen funcionamiento con baja visibilidad y coste relativamente bajo.
> - Limitación clave: **baja resolución**.
#### 4. Sensores de Distancia
> Estos sensores estiman la distancia a obstáculos del entorno (típicamente **EC** y **A** en la tabla de clasificación).
> 1. **Ultrasonidos (ToF):** la distancia se estima a partir del **tiempo de vuelo** de la señal acústica (ejemplo mostrado a 40 kHz).
>     - $d=\dfrac{1}{2},c,t$ (ida y vuelta).
>     - Limitaciones principales: la velocidad del sonido es variable (temperatura, humedad, altitud), existe **zona muerta** para distancias cortas (< 2–3 cm), la señal se atenúa con la distancia y aparecen problemas por ángulo de medida, reflexiones y **crosstalk**.
>    
> 2. **Infrarrojos Reflexivos:** la distancia se estima en función del **ángulo de incidencia**; la luz del LED puede modularse para reducir la influencia de la luz ambiente; rango típico 4–150 cm.
>    
> 3. **Láser ToF:** mide el tiempo (ns) que tardan los fotones en alcanzar un obstáculo y volver (principio ToF).
>     - Láser de Clase 1 (según diapositiva): no causa daños a la vista humana; rango hasta 10 m; relativamente barato.
>     - Limitaciones: falla con fuentes de luz muy brillantes y presenta problemas de reflexión.
>
> 4. **LiDAR:** acrónimo de _Light Detection And Ranging_ (también aparece como _Light Imaging, Detection and Ranging_).
>     - Principio: ToF de haces láser (ns); rango hasta ~200 m con resolución de cm.
>     - **Scanning LiDAR (Electromecánico):** un haz (2D) o de 8 a 128 (3D) sobre husillo giratorio; hasta 360º de HFOV; caro y propenso a fallos mecánicos.
>     - **LiDAR de Estado Sólido:** sin partes móviles, más barato y fiable; hasta 270º de HFOV.
>    
> 5. **Escáneres de Luz Estructurada:** proyectan un patrón infrarrojo conocido (rejilla/rayas/puntos); el patrón se deforma al chocar con superficies; una cámara capta la luz modificada y calcula profundidad y superficie mediante geometría.
#### 5. Mensaje de un Sensor
> Este mensaje representa **una única medida de distancia** de un sensor de rango (típicamente **activo**), válida **sobre un arco** a la distancia medida. No está pensado para escáneres láser (para eso se usa el mensaje de _laser scan_). Incluye un `header` con el instante en que el sensor devuelve la lectura, el tipo de radiación mediante `radiation_type` (p. ej., `ULTRASOUND` o `INFRARED`), el `field_of_view` (apertura del arco en radianes) y los límites `min_range` / `max_range`. La medida principal es `range`, que debe descartarse si cae fuera de esos límites. Además, puede modelar sensores binarios de distancia fija imponiendo `min_range == max_range`, y en ese caso el mensaje puede codificar detección/no detección con `-Inf` y `+Inf` respectivamente (según REP 117).
```python
# Single range reading from an active ranger that emits energy and reports one range reading that is valid along an arc at the distance measured.  
# This message is not appropriate for laser scanners. See the LaserScan message if you are working with a laser scanner.  
# This message can also represent a fixed-distance (binary) ranger. This sensor will have min_range == max_range == distance of detection.  
# These sensors follow REP 117 and will output -Inf if the object is detected and +Inf if the object is outside of the detection range.  
Header header # Timestamp in the header is the time the ranger returned the distance reading  
# Radiation type enums  
# If you want a value added to this list, send an email to the ros-users list  
uint8 ULTRASOUND=0  
uint8 INFRARED=1  
uint8 radiation_type # The type of radiation used by the sensor (sound, IR, etc) [enum]  
float32 field_of_view # The size of the arc that the distance reading is valid for [rad]  
# The object causing the range reading may have been anywhere within -field_of_view/2 and field_of_view/2 at the measured range.  
# 0 angle corresponds to the x-axis of the sensor.  
float32 min_range # Minimum range value [m]  
float32 max_range # Maximum range value [m]  
# Fixed distance rangers require min_range == max_range  
float32 range # Range data [m] (Note: values < range_min or > range_max should be discarded)  
# Fixed distance rangers only output -Inf or +Inf.  
# -Inf represents a detection within fixed distance (detection too close to the sensor to quantify)  
	# +Inf represents no detection within the fixed distance (object out of range)
```
> Este mensaje representa **un barrido completo** de un telémetro láser planar: un conjunto de rayos que cubren un rango angular. El `header` marca el instante de adquisición del **primer rayo**. La geometría del barrido se define con `angle_min`, `angle_max` y `angle_increment`, donde los ángulos se miden alrededor del eje **Z positivo** (sentido antihorario si Z apunta hacia arriba) y el ángulo cero apunta hacia el eje **x** del sensor. La temporización se describe con `time_increment` (tiempo entre medidas, útil si el escáner se mueve) y `scan_time` (tiempo entre barridos). Las distancias van en `ranges` y deben descartarse si están fuera de `range_min`/`range_max`. Opcionalmente, `intensities` guarda la intensidad devuelta por el dispositivo; si no existe, se deja vacío.
```python
# Single scan from a planar laser rangefinder.  
# If you have another ranging device with different behavior (e.g. a sonar array), please find or create a different message, since applications  
# will make fairly laser-specific assumptions about this data.  
Header header # Timestamp in the header is the acquisition time of the first ray in the scan.  
# In frame frame_id, angles are measured around the positive Z axis (counterclockwise, if Z is up)  
# with zero angle being forward along the x axis  
float32 angle_min # Start angle of the scan [rad]  
float32 angle_max # End angle of the scan [rad]  
float32 angle_increment # Angular distance between measurements [rad]  
float32 time_increment # Time between measurements [seconds] - if your scanner is moving, this will be used in interpolating position of 3D points  
float32 scan_time # Time between scans [seconds]  
float32 range_min # Minimum range value [m]  
float32 range_max # Maximum range value [m]  
float32[] ranges # Range data [m] (Note: values < range_min or > range_max should be discarded)  
float32[] intensities # Intensity data [device-specific units]. If your device does not provide intensities, please leave the array empty.
```
![[Pasted image 20260127200500.png]]
#### 6. Sensores de Visión
> RELLENAR
