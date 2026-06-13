### I. Introduction
#### 1. Idea y Contexto
> Las **CNNs** surgen porque las redes **fully connected** no son la mejor opción para trabajar con imágenes. En una imagen, los patrones visuales suelen ser **locales** y pueden aparecer en distintas posiciones, mientras que un MLP trata todas las entradas como independientes y no aprovecha esa estructura espacial. Por eso, las fully connected no son naturalmente **invariantes o equivariantes** a cambios de posición, y además requieren muchos parámetros.
> 
> La idea central es que en imágenes no hace falta aprender un detector distinto para cada posición: el **mismo patrón** puede reaparecer en muchos lugares, así que conviene **compartir parámetros** y buscar patrones locales con un número mucho menor de pesos. Esto permite detectar características pequeñas (bordes, texturas o partes de objetos) y reutilizarlas en toda la imagen.
> 
> A partir de ahí, las CNNs construyen una representación **de local a global**: las primeras capas detectan patrones simples en regiones pequeñas, y las capas más profundas combinan esas características para formar patrones cada vez más abstractos hasta llegar a objetos completos. Esta organización explota dos principios clave: **localidad** en las capas iniciales y **agregación jerárquica** en las capas profundas.
> 
> En este sentido, para datos tabulares una MLP puede ser adecuada, pero para imágenes una arquitectura mejor debe responder de forma similar ante parches similares, centrarse primero en regiones locales y después combinar esa información. Esa necesidad es lo que lleva al diseño de las **Convolutional Neural Networks**. Además, su importancia práctica queda reflejada en la evolución de la visión por computador moderna y en el papel de **ImageNet** como benchmark clave en el desarrollo de estos modelos.

### II. Convolutional Layers
#### 1. De MLP a Convolución: Invariancia y Localidad
> Una capa convolucional puede entenderse como una versión **restringida** de una MLP aplicada a imágenes. Si la entrada es una imagen bidimensional $X$ y la representación oculta tiene la misma forma $H$, una unidad oculta en $(i,j)$ en una red totalmente conectada se escribiría como: $$H_{i,j}=U_{i,j}+\sum_k\sum_l W_{i,j,k,l} \cdot X_{k,l}$$o, reindexando por desplazamientos espaciales, $$H_{i,j}=U_{i,j}+\sum_a\sum_b V_{i,j,a,b} \cdot X_{i+a,j+b}$$Esta formulación muestra que cada posición tiene sus propios pesos, lo que hace que el número de parámetros crezca enormemente para imágenes grandes.
> 
> Para hacer el modelo adecuado a imágenes, se introduce primero el principio de **invariancia/equivariancia a traslaciones**, imponiendo que los pesos no dependan de la posición $(i,j)$. Así se comparten pesos entre posiciones: $$H_{i,j}=u+\sum_a\sum_b V_{a,b} \cdot X_{i+a,j+b}$$donde $u$ es un sesgo constante y $V_{a,b}$ representa un conjunto de pesos compartidos en toda la imagen.
> 
> Después se aplica el principio de **localidad**, restringiendo el cálculo de $H_{i,j}$ a una pequeña vecindad alrededor de $(i,j)$. En ese caso:  $$H_{i,j}=u+\sum_{a=-\Delta}^{\Delta}\sum_{b=-\Delta}^{\Delta}V_{a,b} \cdot X_{i+a,j+b}$$donde $\Delta$ fija el tamaño del vecindario local.
> 
> El tensor $V$ recibe el nombre de **kernel**, **filtro** o pesos de la capa convolucional. En conjunto, compartir pesos y limitar la interacción a regiones locales reduce drásticamente el número de parámetros y da lugar a la idea central de las **convolution layers**.
#### 2. Convolución: intuición, formulación y capa convolucional
> Una **convolución** aplica un conjunto de pesos locales sobre pequeñas regiones de la entrada para producir una nueva representación. Visualmente, cada unidad de salida solo “ve” una región pequeña de la entrada, llamada **receptive field**, y calcula una combinación lineal local más un sesgo: $$y = w * x + b$$Matemáticamente, la convolución entre dos funciones $f$ y $g$ se define como: $$(f*g)(x)=\int f(z)\,g(x-z)\,dz$$Para entradas discretas: $$(f*g)(i)=\sum_a f(a)\,g(i-a)$$y en dos dimensiones: $$(f*g)(i,j)=\sum_a\sum_b f(a,b)\,g(i-a,j-b)$$En CNNs, estrictamente la operación implementada es **cross-correlation** y no convolución pura, porque no se invierte el kernel. Aun así, por convención se sigue llamando **convolución**.
> ![[Pasted image 20260318112944.png]]
>
> Si no se usa _padding_, el tamaño espacial de la salida disminuye según: $$o_h \times o_w = (n_h-k_h+1)\times(n_w-k_w+1)$$donde $n_h\times n_w$​ es el tamaño de la entrada y $k_h\times k_w$ el tamaño del kernel.
> 
> Una **capa convolucional** realiza esta operación entre la entrada y el kernel y añade un **bias** escalar para generar la salida. Sus dos parámetros principales son:
> - el **kernel** o conjunto de pesos,
> - el **bias**.
> Normalmente, los kernels se inicializan de forma aleatoria.
#### 3. Canales, Feature Maps y Receptive Field
> En imágenes reales, la entrada no suele ser solo bidimensional, sino un **tensor** con dimensiones de **alto, ancho y canales**. Por ejemplo, en una imagen RGB cada píxel puede representarse como $X_{i,j,k}$donde $k$ indexa el canal.
> ![[Pasted image 20260318112754.png]]
> Para trabajar con esta estructura, la salida de una capa convolucional también se representa como un tensor de orden tres: $$H_{i,j,d}$$donde $d$ indexa los distintos **feature maps**. Cada **feature map** se especializa en detectar un tipo de patrón, como bordes, texturas o colores.
> 
> Al aplicar **múltiples kernels**, se obtienen **múltiples feature maps**, es decir, múltiples canales de salida. Por eso, tanto la entrada como la salida de una convolución deben entenderse como tensores apilados por canales.
> 
> El **receptive field** de una unidad es la región local de la entrada que influye en esa activación concreta. Así, una neurona de la salida no depende de toda la imagen, sino solo de una ventana local.
> 
> Para soportar múltiples canales en la entrada y en la salida, la formulación se amplía añadiendo más índices al kernel: $$H_{i,j,d}=u+\sum_{a=-\Delta}^{\Delta}\sum_{b=-\Delta}^{\Delta} V_{a,b,c,d}\,X_{i+a,j+b,c}$$donde:
> - $c$ recorre los **canales de entrada**,
> - $d$ identifica el **feature map de salida**,
> - $V$ contiene los pesos del kernel,
> - $U$ es el sesgo.
> 
> En resumen, una convolución en imágenes reales toma un tensor de entrada con varios canales, aplica kernels locales compartidos y produce un nuevo tensor de salida formado por **feature maps**, que servirán como entrada para la siguiente capa.
#### 4. Convolución como Multiplicación Matricial
> Aunque la convolución se suele entender como un **kernel que se desliza** sobre la entrada, también puede verse como una **multiplicación matricial estructurada**. La diferencia con la multiplicación matricial usual es que esta combina filas y columnas completas, mientras que la convolución trabaja sobre **ventanas locales** y realiza productos elemento a elemento dentro de cada región.
> 
> En una dimensión, la convolución puede escribirse como una multiplicación entre el vector de entrada y una **matriz de Toeplitz**, es decir, una matriz cuyas diagonales son constantes. Si $h$ es el kernel y $x$ la entrada, entonces:  $$y = h * x$$puede representarse matricialmente usando una matriz construida a partir de copias desplazadas del kernel. De forma equivalente, también puede escribirse como: $$y^{T} = [h_1\ h_2\ \cdots\ h_m] \begin{bmatrix} x_1 & x_2 & x_3 & \cdots & x_n & 0 & \cdots & 0 \\ 0 & x_1 & x_2 & \cdots & x_{n-1} & x_n & \cdots & 0 \\ \vdots & \ddots & \ddots & \ddots & \ddots & \ddots & \ddots & \vdots \\ 0 & \cdots & 0 & x_1 & x_2 & \cdots & x_{n-1} & x_n \end{bmatrix}$$lo que muestra que la convolución puede interpretarse como una operación lineal.
> 
> En dos dimensiones, la misma idea se mantiene. Si $A$ es la imagen de entrada y $K$ el kernel, la convolución $A*K$ puede representarse como:  $Mv^T = v'$ donde:
> - $v$ es la imagen $A$ vectorizada fila a fila
> - $M$ es una matriz por bloques construida a partir del kernel $K$
> - $v'$ es el resultado vectorizado de la convolución
> 
> Si la entrada es de tamaño $n\times n$ y el kernel de tamaño $k\times k$, entonces el tamaño espacial de la salida es:  $t = n-k+1$ y la matriz $M$ tiene tamaño $t^2 \times n^2$.
> 
> La construcción de $M$ se hace generando submatrices $K_i$ que representan el deslizamiento horizontal de cada fila del kernel, concatenándolas horizontalmente y después desplazándolas verticalmente mediante bloques nulos. Finalmente, tras multiplicar por el vector de entrada, el vector resultante $v'$ se reorganiza para recuperar la salida bidimensional.
> 
> En resumen, la convolución no deja de ser una **transformación lineal**, pero con una estructura muy particular: la matriz asociada es extremadamente estructurada y refleja el **deslizamiento local y compartido** del kernel sobre la entrada.

### III. Padding, Striding, Dilatation, Groups, & Pooling
#### 1. Padding, Striding & Dilatation
> En una convolución, cada vez que aplicamos un kernel se pierde información en el borde de la imagen, por lo que el tamaño espacial de la salida se reduce si no hacemos nada para evitarlo.
> 
> - **Sin padding ni stride**, para una entrada de tamaño $n_h \times n_w$ y un kernel de tamaño $k_h \times k_w$, la salida tiene tamaño: $$o_h \times o_w = (n_h-k_h+1)\times(n_w-k_w+1)$$Para controlar mejor ese tamaño aparecen tres ideas clave: **padding**, **stride** y **dilation**.
> 
> - **Padding** consiste en añadir filas y columnas al tensor de entrada, normalmente con ceros, para compensar la pérdida de píxeles en los bordes. Si añadimos $p_h$ filas y $p_w$ columnas, el tamaño de salida pasa a ser:  $$o_h \times o_w = (n_h-k_h+p_h+1)\times(n_w-k_w+p_w+1)$$Un caso importante es usar padding para mantener la forma espacial de la entrada. Para ello: $$p_h = k_h-1,\quad p_w = k_w-1$$Si $k_h$ o $k_w$ son pares, el padding necesario es asimétrico; por eso es habitual usar kernels impares.
> 
> - **Striding** indica cuánto se desplaza la ventana de convolución en cada paso. Por defecto, el stride es 1 en ambas dimensiones, lo que significa avanzar píxel a píxel. Si aumentamos el stride, reducimos el coste computacional y hacemos una especie de _downsampling_, ya que se omiten posiciones intermedias. Con stride vertical $s_h$ y horizontal $s_w$, el tamaño de salida es:  $$o_h \times o_w = \left[\frac{n_h-k_h+p_h+s_h}{s_h}\right] \times \left[\frac{n_w-k_w+p_w+s_w}{s_w}\right]$$![[Pasted image 20260318113056.png]]
> 
> - **Dilation** (o _atrous convolution_) separa los elementos del kernel, aumentando su campo receptivo sin incrementar el número de parámetros. Su objetivo es capturar contexto más amplio, aunque puede perder detalle local fino. Para un factor de dilatación $d$, la convolución se escribe como: $$H_{i,j}=\sum_{a=-\Delta}^{\Delta}\sum_{b=-\Delta}^{\Delta}V_{a,b},X_{i+da,;j+db}$$Aquí, $d$ separa las posiciones del kernel y hace que este “vea” una región mayor de la entrada.
> 
> En la fórmula general, combinando **padding**, **stride** y **dilation**, el tamaño de salida queda: $$o_h=\left[ \frac{n_h+2p_h-d(k_h-1)-1}{s_h}\right]+1, \quad o_w=\left[ \frac{n_w+2p_w-d(k_w-1)-1}{s_w}\right]+1$$![[Pasted image 20260318113229.png]]
> 
> En resumen:
> - **Padding** controla la pérdida de borde y puede mantener el tamaño espacial.
> - **Stride** controla cuánto avanza el kernel y reduce resolución/coste.
> - **Dilation** amplía el campo receptivo sin añadir parámetros.
> Los tres son hiperparámetros fundamentales de una capa convolucional porque determinan cuánto contexto observa la red y cuál será el tamaño de las representaciones intermedias.
#### 2. Múltiples Canales
> Cuando la entrada tiene varios canales $(c_i>1)$, el **kernel** debe tener también ese mismo número de canales. Si la ventana espacial del kernel es $k_h\times k_w$, entonces su forma pasa a ser: $$c_i \times k_h \times k_w$$La convolución se realiza **canal a canal** sobre tensores bidimensionales, y después se **suman** los resultados de todos los canales de entrada para obtener una única salida bidimensional.
> 
> Si además queremos varios **canales de salida**, no basta con un solo kernel, sino con un conjunto de kernels. Si $n_c$ es el número de canales de entrada y $o_c$ el número de canales de salida, entonces el tensor de pesos tiene forma:  $$o_c \times n_c \times k_h \times k_w$$Cada canal de salida se obtiene aplicando su kernel correspondiente sobre **todos** los canales de entrada. El resultado final es un tensor de forma:  $$o_c \times o_h \times o_w$$Es decir, cada filtro produce un **feature map**, y varios filtros producen varios mapas de características. ![[Pasted image 20260318113428.png]]
> 
> Un caso particular importante es la **convolución (1×1)**, donde: $k_h = k_w = 1$ 
> En este caso no se mezclan vecinos espaciales, sino solo la información en la **dimensión de los canales**. Puede verse como una capa totalmente conectada aplicada **independientemente en cada posición espacial**. Su función principal es transformar $n_c$ canales de entrada en $o_c$ canales de salida, pudiendo **reducir o aumentar** la profundidad del tensor sin alterar la estructura espacial.
> ![[Pasted image 20260318113459.png]]
#### 3. Groups
> En una **convolución estándar**, cada canal de entrada está conectado con **todos** los canales de salida. Esto da máxima flexibilidad, pero también implica un coste computacional alto y un gran número de parámetros.
> 
> Las **grouped convolutions** dividen los canales de entrada en $G$ grupos, conectando cada grupo de entrada solo con un grupo correspondiente de canales de salida. Así, la convolución deja de ser totalmente densa en la dimensión de canales y pasa a estar parcialmente separada.
> 
> Si una convolución estándar tiene:  $$C_{out}\times C_{in}\times k_h\times k_w$$parámetros, entonces una convolución con grupos tiene: $$G\left(\frac{C_{out}}{G}\times \frac{C_{in}}{G}\times k_h\times k_w\right)$$lo que reduce de forma importante el número de parámetros cuando $G>1$.
> 
> La principal ventaja de esta idea es que disminuye el coste computacional y la memoria aproximadamente en un factor $G$, haciendo el modelo más eficiente, especialmente en arquitecturas diseñadas para dispositivos con recursos limitados.
> 
> Por ejemplo, si la entrada es un tensor (imagen) $X$ de tamaño:  $8\times 32\times 32$  y usamos un kernel de tamaño:  $8\times 8\times 3\times 3$ (8 output channels, 8 input channels, y 3×3 kernel) con:  $G=4$, entonces los 8 canales de entrada se dividen en 4 grupos de 2 canales cada uno. Cada grupo utiliza sus propios filtros y opera solo sobre sus canales correspondientes. Finalmente, las salidas de todos los grupos se concatenan para formar el tensor final:  $8\times 30\times 30$  
> 
> En resumen, las **grouped convolutions** sacrifican parte de la conectividad total entre canales a cambio de una arquitectura mucho más eficiente en parámetros y computación.![[Pasted image 20260318113912.png]]
#### 4. Pipeline Completo de la CNN
> El pipeline típico de una **CNN** comienza con una **imagen de entrada**, sobre la que se aplican sucesivamente varias capas de **convolución + activación** (normalmente ReLU). Estas capas se encargan de extraer características locales de la imagen, como bordes, texturas y patrones cada vez más complejos.
> 
> Entre bloques convolucionales se suelen introducir capas de **pooling**, que reducen la dimensión espacial de los feature maps. Esto permite disminuir el coste computacional, conservar la información más relevante y hacer que la representación sea más compacta.
> 
> Tras varios bloques de **convolución + activación + pooling**, la red obtiene una representación de alto nivel de la imagen. Esa representación se transforma en un vector mediante la operación de **flatten**, que prepara la salida convolucional para las capas finales de clasificación.
> 
> Finalmente, el vector resultante pasa por una o varias capas **fully connected**, que combinan las características extraídas para producir una salida final. En problemas de clasificación, la última capa suele terminar en una **softmax**, que convierte las salidas en puntuaciones interpretables como probabilidades de clase.
> 
> En resumen, una CNN sigue este flujo: $$\text{Input} \rightarrow (\text{Conv}+\text{ReLU}\rightarrow \text{Pooling})^n \rightarrow \text{Flatten} \rightarrow \text{Fully Connected} \rightarrow \text{Softmax}$$donde la primera parte realiza el **feature learning** y la última lleva a cabo la **clasificación**.![[Pasted image 20260318114036.png]]

### IV. Pooling
#### 1. Idea
> El **pooling** es una operación de **submuestreo** que reduce el tamaño espacial de los **feature maps** sin cambiar la naturaleza del objeto representado. La idea es que una imagen o un patrón relevante puede seguir reconociéndose aunque se represente con menos resolución.
> 
> Sus dos funciones principales son:
> - **Reducir el tamaño** de los feature maps, disminuyendo el coste computacional.
> - **Agregar información local**, ayudando a construir características más globales.
> 
> Un operador de pooling consiste en una **ventana de tamaño fijo** que recorre el mapa de entrada y produce un único valor por cada región visitada. A diferencia de una convolución, **no tiene parámetros aprendibles**: no hay kernel ni pesos que entrenar. Es una operación determinista que aplica una regla simple sobre cada ventana.
> 
> Los casos más habituales son:
> - **Max pooling**: toma el valor máximo de la ventana.
> - **Average pooling**: toma la media de los valores de la ventana.
> 
> En resumen, el pooling sirve para hacer la representación más compacta y para resumir la información local más importante antes de pasar a capas posteriores.
#### 2. Max Pooling & Avg Pooling
> Los dos tipos de pooling más habituales son **max pooling** y **average pooling**. Ambos aplican una ventana local sobre el mapa de características y devuelven un único valor por región, pero lo hacen con criterios distintos.
> 
> **Max pooling** devuelve el **valor máximo** dentro de la ventana de pooling. Por tanto, se centra en la característica más fuerte o más prominente de esa región. Esto lo hace especialmente útil cuando queremos conservar respuestas intensas, como bordes o activaciones muy marcadas.
> 
> Sus principales ventajas son:
> - conserva características destacadas,
> - reduce el efecto de valores pequeños o ruido débil,
> - es robusto ante pequeños desplazamientos o distorsiones,
> - resulta útil para detectar patrones nítidos.
> 
> Sus desventajas son:
> - puede descartar otra información potencialmente útil,
> - es sensible a picos de ruido altos si estos dominan la ventana.
> 
> **Average pooling** devuelve la **media** de todos los valores de la ventana. En vez de quedarse con la activación más fuerte, genera una versión más suavizada del mapa de características.
> 
> Sus ventajas son:
> - suaviza los feature maps y conserva el patrón general,
> - es menos sensible a picos aislados de ruido,
> - captura mejor el contexto global de la región.
> 
> Sus desventajas son:
> - diluye las características más prominentes,
> - difumina bordes o transiciones bruscas,
> - suele ser menos eficaz para detección precisa de rasgos.
> 
> En resumen:
> - **Max pooling** prioriza las activaciones más importantes.
> - **Average pooling** prioriza un resumen más suave y global.
> ![[Pasted image 20260318115654.png]]
> La elección entre ambos depende del objetivo: si interesa resaltar rasgos fuertes, suele preferirse **max pooling**; si interesa una agregación más estable y suavizada, puede usarse **average pooling**.
#### 3. Output Shape, Global Average Pooling y Papel del Pooling
> Las capas de pooling también admiten **padding** y **stride** para controlar el tamaño de la salida. Además, como el pooling agrega información dentro de una ventana, en muchos frameworks el **stride por defecto coincide con el tamaño de la ventana**. Por ejemplo, una ventana $3\times3$ suele usar stride $3\times3$.
> 
> Cuando la entrada tiene varios canales, el pooling se aplica **por separado en cada canal**; no mezcla ni suma canales como sí hace una convolución. Por eso, en pooling normalmente se cumple: $n_c=o_c$  
> 
> En general, para una entrada de tamaño $n_h\times n_w$, padding $p_h,p_w$, ventana $k_h\times k_w$ y stride $s_h,s_w$, el tamaño de salida es: $$o_h=\left[ \frac{n_h+2p_h-k_h}{s_h}\right] +1, \quad o_w=\left[ \frac{n_w+2p_w-k_w}{s_w}\right] +1$$
> Un caso especial importante es el **Global Average Pooling (GAP)**, que puede verse como una versión extrema del average pooling. En lugar de promediar pequeñas ventanas, promedia **todo el feature map** de cada canal y lo reduce a un único valor. Así, cada mapa espacial pasa de tamaño $H'\times W'$ a un solo escalar, quedando únicamente la dimensión de canales.
> Esto reduce fuertemente la dimensión espacial y deja una representación compacta, útil justo antes de una capa lineal o de clasificación.
> ![[Pasted image 20260318120049.png]]
> 
> También, el **max pooling** puede interpretarse como una pequeña fuente de **no linealidad**, porque selecciona la activación más fuerte de cada región en lugar de hacer una combinación lineal. Así complementa a las capas convolucionales: reduce dimensión espacial y conserva las respuestas más relevantes.
>  ![[Pasted image 20260318120055.png]]
> 
> En resumen:
> - el pooling controla también el tamaño de salida mediante ventana, stride y padding
> - se aplica canal a canal
> - el **GAP** reduce cada canal a un único valor
> - el **max pooling** no solo resume información, sino que también introduce un efecto no lineal

### V. Design Principles of CNN Models
#### 1. Principios de Diseño
> En CNNs modernas, es habitual **reducir progresivamente la resolución espacial** de los feature maps mediante **striding** o **pooling**, mientras que **aumenta el número de canales**. La idea es intercambiar detalle espacial por representaciones más abstractas y ricas, manteniendo controlados el coste computacional y la memoria.
> 
> Otro principio importante es **usar kernels pequeños**, normalmente 3×3, en lugar de kernels grandes como 7×7. Varias convoluciones pequeñas apiladas suelen ser preferibles porque:
> - reducen el número de parámetros
> - introducen más no linealidades
> - en la práctica suelen rendir mejor que una sola convolución grande
> 
> También es común **repetir bloques de capas** con una estructura regular, por ejemplo combinaciones de:
> - **conv 1×1** para reducir o expandir canales (_bottleneck_),
> - **conv 3×3** para capturar patrones espaciales locales,
> - **ReLU** u otras no linealidades entre medias.
> 
> Estos patrones repetidos facilitan construir redes más profundas con un diseño más limpio, estable y fácil de ajustar.
> 
> Finalmente, muchas arquitecturas modernas tienden a ser **“all convolutional”**, evitando grandes bloques `Flatten + Linear`. En su lugar, suelen usar **global pooling** (por ejemplo, _global average pooling_) antes de la clasificación final. Esto aporta:
> - menos parámetros
> - mayor flexibilidad respecto al tamaño de entrada
> - una arquitectura más coherente al mantener el procesamiento convolucional hasta casi el final
> 
> En resumen, los principios de diseño más importantes son:
> - bajar resolución espacial de forma gradual
> - aumentar canales al profundizar
> - preferir kernels pequeños
> - reutilizar bloques simples y repetidos
> - reducir el uso de capas fully connected grandes al final
#### 2. Modelos
> **1. `LeNet-5`**  
> Es una de las primeras arquitecturas CNN clásicas. Sigue una estructura simple y muy representativa:  
> `Input → Convolution → Nonlinearity → Pooling → Convolution → Nonlinearity → Pooling → Fully Connected → Nonlinearity → Fully Connected → Nonlinearity`
> 
> Idea principal:
> - primeras capas convolucionales para extraer patrones locales
> - pooling para reducir resolución
> - capas fully connected al final para clasificar
> 
> Es un modelo relativamente pequeño y sirve muy bien para entender el pipeline básico de una CNN clásica. ![[Pasted image 20260318121350.png]]
> 
> **2. `AlexNet`**  
> Supone un salto importante respecto a LeNet-5: la red se hace bastante más profunda y ancha. Combina varias capas convolucionales con ReLU, pooling y varias capas fully connected finales, terminando en una salida `Softmax`.
> 
> Idea principal:
> - extraer características cada vez más complejas con varias convoluciones
> - reducir resolución de forma progresiva
> - usar una cabeza densa grande para clasificación
> 
> Rasgos que se aprecian en el esquema:
> - varias capas `Conv + ReLU`
> - pooling intermedio
> - capas fully connected grandes al final
> - salida final de clasificación
> 
> En comparación con LeNet-5, AlexNet es más profunda, usa más canales y tiene mucha mayor capacidad de representación. ![[Pasted image 20260318121418.png]]
> 
> **3. `VGGNet`**  
> VGG lleva la idea de profundidad todavía más lejos, pero con una filosofía muy regular: repetir muchas veces bloques simples, normalmente convoluciones pequeñas seguidas de no linealidades y reducciones progresivas de resolución.
> 
> Idea principal:
> - usar una arquitectura muy uniforme
> - apilar muchas convoluciones pequeñas
> - y construir profundidad a partir de bloques repetidos
> 
> Rasgos clave:
> - diseño muy regular y modular
> - gran profundidad
> - repetición de patrones simples
> - reducción progresiva de tamaño espacial
> 
> VGG es importante porque consolida varios principios de diseño de CNN modernas: preferir kernels pequeños, aumentar canales al profundizar, repetir bloques y separar claramente la parte de extracción de características de la parte final de clasificación. ![[Pasted image 20260318121603.png]]
> 
> **Resumen rápido**
> - **LeNet-5**: CNN clásica y simple; muy útil para entender la estructura base.
> - **AlexNet**: CNN más profunda y potente; marca un gran avance en visión por computador.
> - **VGGNet**: arquitectura muy profunda y regular, basada en bloques repetidos y convoluciones pequeñas.
> 
> En conjunto, estos modelos muestran la evolución típica de las CNN: más profundidad, más canales, bloques más estructurados y mejores representaciones jerárquicas.
#### 3. Profundidad
> Aumentar la profundidad de una CNN suele mejorar su capacidad de representación, porque permite construir características jerárquicas cada vez más abstractas. En general, más capas permiten pasar de patrones simples a estructuras más complejas.
> 
> Sin embargo, **más profundidad no garantiza automáticamente menor error**. A partir de cierto punto puede aparecer degradación del rendimiento: añadir capas deja de ayudar e incluso puede empeorar los resultados si la arquitectura o el entrenamiento no están bien diseñados.
> 
> Los principales problemas de redes profundas son:
> - **Vanishing / exploding gradients**: los gradientes pueden hacerse muy pequeños o muy grandes al propagarse por muchas capas.
> - **Overfitting**: al aumentar el número de parámetros, la red puede ajustarse demasiado a los datos de entrenamiento.
> - **Mayor coste computacional**: más capas implican más tiempo de entrenamiento y más memoria.
> - **Rendimientos decrecientes**: apilar capas sin más no siempre produce mejoras proporcionales.
> 
> Para mitigar estos problemas suelen emplearse:
> - **skip / residual connections**
> - **inicialización cuidadosa**
> - **Batch Normalization**
> - **regularización**
> - **data augmentation**
> 
> Además, una CNN es robusta por diseño sobre todo frente a **traslaciones**, pero no necesariamente frente a otras transformaciones como:
> - rotaciones,
> - cambios de escala,
> - deformaciones,
> - shearing o warping.
> 
> Por eso, para que una red profunda generalice mejor, es habitual usar **data augmentation**, generando versiones transformadas de las imágenes durante el entrenamiento. Así, la red aprende a ser más robusta frente a variaciones que no vienen incorporadas directamente en la convolución.
> 
> **Idea clave:**  
> La profundidad es útil y necesaria para aprender representaciones complejas, pero debe ir acompañada de buenas técnicas de entrenamiento y de estrategias que mejoren la robustez del modelo.

### VI. Other Types of Convolutions & Implementations
#### 1. Up-Convolution
> La **up-convolution** (también llamada **transposed convolution** o **deconvolution**) se utiliza para transformar un mapa de características pequeño en una salida de **mayor resolución espacial**.
> 
> A diferencia de la convolución estándar, que normalmente reduce o mantiene la resolución, la     up-convolution **aprende a hacer upsampling** preservando la estructura aprendida. Por eso aparece con frecuencia en la parte **decodificadora** de arquitecturas que necesitan reconstruir detalle espacial. ![[Pasted image 20260318123202.png]]
> 
> Sus usos más habituales son **autoencoders**, **generadores de imágenes** como GANs, y **redes de segmentación** como **U-Net**.
> 
> Una forma intuitiva de entenderla es la siguiente:
> Se parte de una entrada pequeña, en algunas implementaciones se **insertan ceros entre los elementos** de la entrada para “expandir” la rejilla, después se aplica un filtro aprendible, el filtro “rellena” las posiciones intermedias y produce una salida más grande. ![[Pasted image 20260318123243.png]]
> 
> En otras palabras, la up-convolution realiza un **upsampling aprendido**, no una simple interpolación fija.
> 
> **Idea clave:** mientras la convolución estándar extrae y comprime características, la up-convolution permite **reconstruir resolución espacial** a partir de representaciones compactas.
> 
> **Ejemplo importante: U-Net**
> - U-Net combina una rama de **contracción** (encoder) con una rama de **expansión** (decoder).
> - En la parte expansiva se usan **up-convolutions 2×2** para aumentar la resolución.
> - Después de cada subida de resolución, se combinan características de baja y alta resolución mediante conexiones laterales.
> - Finalmente, una convolución 1×1 produce el mapa de segmentación de salida.
> ![[Pasted image 20260318123346.png]]
> Esto hace que U-Net sea especialmente útil cuando no basta con clasificar una imagen completa, sino que hay que **predecir una etiqueta por píxel**.
#### 2. Temporal Convolutions
> Las **convoluciones temporales 1D** aplican filtros sobre secuencias ordenadas, como texto, audio o series temporales.
>
> En lugar de recorrer una imagen en dos dimensiones, el filtro se desplaza a lo largo del eje temporal y aprende patrones locales entre elementos consecutivos. Así, una convolución 1D puede capturar dependencias de corto alcance entre tokens, muestras de audio o pasos de tiempo.
> 
> Ideas clave:
> - El filtro “desliza” sobre la secuencia y detecta patrones locales.
> - Apilar varias capas aumenta el **contexto temporal efectivo**.
> - Puede usarse como alternativa a modelos recurrentes en algunos problemas secuenciales.
> - Una capa **lineal final** puede agregar las características aprendidas para producir una salida de clasificación o regresión.
> ![[Pasted image 20260318123549.png]]
> En resumen, las convoluciones temporales permiten modelar secuencias de forma eficiente, capturando estructura local y construyendo contexto más amplio al profundizar la red.
#### 3. Casual Convolutions
> **Convoluciones causales** son un tipo de convolución temporal diseñado para respetar el orden temporal de la secuencia.
> La idea es que la salida en una posición $t$ solo puede depender de la entrada actual, y las entradas pasadas, pero **no** de valores futuros.
> 
> Esto es especialmente importante en tareas autorregresivas, donde el modelo genera o predice el siguiente elemento de una secuencia sin “mirar al futuro”.
> 
> Su utilidad principal es:
> - mantener la coherencia temporal
> - evitar fuga de información futura
> - permitir predicción paso a paso en audio, texto o series temporales
> ![[Pasted image 20260318123720.png]]
> Por tanto, una convolución causal es una restricción sobre la convolución temporal para que el modelo use solo información disponible hasta el instante actual.
#### 4. Wave-Net
> **WaveNet** es un ejemplo de arquitectura basada en convoluciones 1D para modelar secuencias, especialmente audio.
> 
> Su idea principal es combinar **convoluciones causales**, para no usar información futura, y **dilatación** (creciente), para ampliar rápidamente el campo receptivo.
> Esto permite que la red capture dependencias a distintas escalas temporales sin necesidad de usar kernels enormes ni una profundidad descontrolada.
> 
> La ventaja clave de WaveNet es que modela contexto temporal largo, mantiene causalidad, y lo hace de manera eficiente gracias a las convoluciones dilatadas. ![[Pasted image 20260318123739.png]]
> En resumen, WaveNet muestra cómo combinar **convolución temporal + causalidad + dilatación** para construir modelos secuenciales potentes.
#### 5. 3D-Convolutions
> Las **convoluciones 3D** extienden las convoluciones 2D añadiendo una dimensión extra, normalmente el **tiempo** o la **profundidad volumétrica**.
> Son adecuadas para datos como vídeo, imágenes médicas 3D, y datos volumétricos.
> 
> En este caso, el filtro ya no cubre solo **alto × ancho**, sino también una tercera dimensión. Por ejemplo, un filtro **(3×3×3)** captura estructura espacial, y también contexto entre frames o cortes consecutivos.
> 
> Ideas clave:
> - Permiten aprender **características espaciotemporales**.
> - Son útiles cuando importa tanto la forma en cada imagen como su evolución temporal.
> - Al apilar varias capas, la red puede aprender patrones de movimiento o estructuras volumétricas cada vez más complejas.
> ![[Pasted image 20260318124111.png]]
> En resumen, las convoluciones 3D son la extensión natural de las CNN cuando los datos no son solo imágenes estáticas, sino secuencias o volúmenes.
#### 6. Implementation of CNNs
> En la implementación práctica de convoluciones en CNNs, una idea central es transformar la operación de convolución en una secuencia de pasos matriciales sobre bloques extraídos de la imagen. Para ello se usan las operaciones **unfold** y **fold**.
> 
> **Unfold** (también conocido como **im2col**) extrae bloques o parches solapados de una imagen o de un lote de imágenes.  
> Si la entrada tiene forma: $$b \times n_c \times n_h \times n_w$$entonces la salida de `unfold` tiene forma: $$b \times (n_c \cdot k_h \cdot k_w) \times (h' \cdot w')$$donde:
> - $k_h, \ k_w$ son el alto y ancho del kernel
> - $h', \ w'$ son el número de bloques extraídos en vertical y horizontal
> 
> El cálculo de $h'$ y $w'$ sigue exactamente la misma lógica que en una convolución: $$h' = \left[ \frac{n_h + 2p_h - d,(k_h-1) - 1}{s_h} \right] + 1, \quad w' = \left[ \frac{n_w + 2p_w - d,(k_w-1) - 1}{s_w} \right] + 1$$donde:
> - $n_h, \ n_w$ es el tamaño espacial de la entrada
> - $p_h, \ p_w$ es el padding
> - $s_h, \ s_w$ es el stride
> - $d$ es la dilatación
> 
> La operación inversa es **fold** (o **col2im**), que reconstruye una imagen a partir de los bloques extraídos.  
> Recibe una entrada de forma: $$b \times (n_c \cdot k_h \cdot k_w) \times (h' \cdot w')$$y devuelve una imagen reconstruida de forma: $$b \times n_c \times n_h \times n_w$$Durante esta reconstrucción, los bloques solapados se **suman** en las posiciones compartidas.
> 
> El flujo práctico es:
> 1. Aplicar `unfold` para extraer parches.
> 2. Operar sobre esos parches, por ejemplo con transformaciones lineales o implementaciones manuales de convolución.
> 3. Aplicar `fold` para reconstruir la salida espacial.
> 
> Esto permite entender la convolución como una operación matricial explícita, aunque tiene varios inconvenientes prácticos:
> - **Solapamiento de bloques**: algunos píxeles aparecen varias veces.
> - **Mayor uso de memoria**: extraer todos los bloques puede ser costoso.
> - **Consistencia de parámetros**: stride, padding y dilatación deben coincidir entre `unfold` y `fold`.
> 
> Los parámetros principales de **unfold** son:
> - `kernel_size`: tamaño de la ventana,
> - `dilation`: separación interna entre elementos del bloque,
> - `padding`: ceros añadidos al borde,
> - `stride`: desplazamiento entre bloques.
> 
> Los parámetros principales de **fold** son los mismos, añadiendo además:
> - `output_size`: tamaño espacial objetivo de la reconstrucción.
> 
> En resumen, `unfold` y `fold` son herramientas útiles para implementar convoluciones de forma explícita, manipular parches de imagen y entender cómo una CNN procesa localmente la información espacial.

La sección de resúmenes continúa en [[Resumen Tema 4 - Optimization & Regularization]]