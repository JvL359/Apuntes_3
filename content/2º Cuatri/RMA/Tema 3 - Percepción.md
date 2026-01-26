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
> El material advierte un caso práctico: **a bajas velocidades** la medida puede salir **nula**, y se propone **aumentar N** o el **periodo de muestreo Δt.
> Si el motor está acoplado a una rueda de radio R, se pasa a magnitudes lineales con:
> $\Delta s=\Delta\theta\cdot R, \qquad v=\omega\cdot R$

