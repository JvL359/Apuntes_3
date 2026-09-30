---
estado: pendiente de revisión
---

### I. Introduction

#### 1. Detection and Bounding Boxes

##### 1.1. The Detection Problem

> En **image classification** se asigna una categoría a la imagen completa. En **object detection** hay que identificar cada objeto de interés y localizarlo, incluso cuando aparecen varios en una escena. Cada detección combina una clase, una **bounding box** y una puntuación de confianza. Esta información permite, por ejemplo, situar peatones y vehículos en una secuencia captada por un coche o localizar objetos durante la navegación de un robot.

##### 1.2. Bounding Box Representations

> Una caja rectangular puede representarse por sus esquinas superior izquierda e inferior derecha, $(x_1,y_1,x_2,y_2)$, o por su centro, anchura y altura, $(x,y,w,h)$. Con el origen de coordenadas en la esquina superior izquierda de la imagen:

$$
x=\frac{x_1+x_2}{2},\qquad y=\frac{y_1+y_2}{2},\qquad
w=x_2-x_1,\qquad h=y_2-y_1.
$$

> Por ejemplo, $(x_1,y_1,x_2,y_2)=(10,5,85,100)$ corresponde exactamente a $(x,y,w,h)=(47.5,52.5,75,95)$. La elección de representación no cambia la región descrita, pero sí la forma en que se predicen y comparan sus coordenadas.

#### 2. Detecting a Single Object

##### 2.1. Model and Loss

> Para localizar como máximo un objeto, una CNN puede extraer rasgos de toda la imagen y alimentar dos cabezas: una **MLP** predice la clase y otra las cuatro coordenadas de la caja. La clasificación debe incluir la clase **background** o «no object». Si esta es la clase verdadera, las coordenadas predichas no tienen significado y se excluyen de la pérdida.

> Sean $y=(y_1,\ldots,y_n)^T$ la etiqueta *one-hot*, $\hat y=(\hat y_1,\ldots,\hat y_n)^T$ los *logits*, $(x_1,y_1,x_2,y_2)$ la caja real y $(\hat x_1,\hat y_1,\hat x_2,\hat y_2)$ la estimada. La pérdida combina clasificación y regresión:

$$
\mathcal L=\mathcal L_{\mathrm{CE}}+\lambda\,\mathbf 1_{\mathrm{no\ bg}}\,\mathcal L_{L2},
\qquad \lambda>0,
$$

$$
\mathcal L_{\mathrm{CE}}
=-\sum_{i=1}^{n}y_i\log\left(\frac{\exp(\hat y_i)}
{\sum_{j=1}^{n}\exp(\hat y_j)}\right),
$$

$$
\mathcal L_{L2}
=\frac14\left[(x_1-\hat x_1)^2+(y_1-\hat y_1)^2
+(x_2-\hat x_2)^2+(y_2-\hat y_2)^2\right].
$$

> El indicador $\mathbf 1_{\mathrm{no\ bg}}$ vale $1$ si hay un objeto real y $0$ si la etiqueta es *background*. La constante $\lambda$ equilibra los dos objetivos. Si solo existe una clase de objeto, la cabeza de presencia puede usar **binary cross-entropy**. Si se sabe que ese mismo objeto aparece en todas las imágenes, basta con la cabeza de coordenadas y el problema pasa a ser de regresión; localizar el balón a lo largo de un partido es un ejemplo.

##### 2.2. Naive Multi-Object Extension

> Para detectar varios objetos podríamos recortar muchas regiones de la imagen y aplicar a cada una el detector anterior. El número de posibles recortes vuelve inviable esta búsqueda exhaustiva. En una imagen de altura $H$ y anchura $W$, hay $H(H+1)/2$ intervalos de filas y $W(W+1)/2$ intervalos de columnas, por lo que el número total de cajas es

$$
N_{\mathrm{boxes}}
=\frac{H(H+1)}{2}\,\frac{W(W+1)}{2}
\in\mathcal O(H^2W^2).
$$

> Incluso una imagen $3\times3$ admite $36$ cajas. Muestrear aproximadamente $c$ cajas por píxel reduce el recuento a alrededor de $cHW$, pero puede omitir la caja correcta y sigue exigiendo muchas evaluaciones. Los detectores posteriores necesitan seleccionar o aprender propuestas más informativas.

### II. Previous Concepts

#### 3. Intersection over Union (IoU)

> **Intersection over Union (IoU)** mide el solapamiento entre una caja predicha $A$ y una caja real $B$. Es el índice de Jaccard aplicado a sus áreas:

$$
\operatorname{IoU}(A,B)
=\frac{|A\cap B|}{|A\cup B|}
=\frac{|A\cap B|}{|A|+|B|-|A\cap B|}.
$$

> Toma valores entre $0$ y $1$: $0$ indica que no hay intersección y $1$ que las cajas coinciden. Permite medir la calidad de la localización, decidir si una detección alcanza un umbral de acierto y comparar cajas durante **NMS**.

#### 4. Non-Maximum Suppression (NMS)

> Un detector suele proponer varias cajas para el mismo objeto. **Non-Maximum Suppression (NMS)** conserva la de mayor confianza y elimina las que se solapan demasiado con ella. El esquema muestra cómo una lista de predicciones se reduce progresivamente hasta una caja por objeto visible.

![[Pasted image 20260930112900.png]]

1. Descartar *background* y, si se desea, las cajas cuya confianza esté por debajo de un umbral.
2. Ordenar las cajas restantes por puntuación descendente.
3. Conservar la primera caja y suprimir las otras de la misma clase cuya IoU con ella supere $\varepsilon$.
4. Repetir con la caja no suprimida de mayor puntuación hasta agotar la lista.

> Aplicar la supresión por clase evita que una caja de «persona» elimine una de «perro» por el mero hecho de solaparse. El umbral $\varepsilon$ regula cuán parecidas deben ser dos cajas para considerarlas duplicadas.

#### 5. Average Precision and mAP

> La **precision** mide qué parte de las detecciones positivas es correcta y el **recall** qué parte de los objetos reales se ha encontrado:

$$
\mathrm{precision}=\frac{TP}{TP+FP},
\qquad
\mathrm{recall}=\frac{TP}{TP+FN}.
$$

> Para una clase y un umbral de IoU fijo $\tau$, se reúnen sus predicciones de todo el conjunto de evaluación y se ordenan por confianza. Cada predicción se empareja, dentro de su imagen y clase, con la caja real aún no asignada de mayor IoU. Es **true positive (TP)** si alcanza $\tau$; de lo contrario es **false positive (FP)**. Una segunda detección del mismo objeto cuenta como FP. Los TP y FP acumulados proporcionan un punto de la curva precision–recall después de cada predicción.

> La **Average Precision (AP)** resume el área bajo esa curva para una clase, aplicando la regla de interpolación o integración del protocolo. La **mean Average Precision (mAP)** promedia las AP de las clases; si el protocolo usa varios umbrales de IoU, también promedia sobre ellos:

$$
\mathrm{mAP}=\frac1N\sum_{c=1}^{N}\mathrm{AP}_c.
$$

> La gráfica muestra que cada clase puede tener una curva y una AP distintas; una curva que mantiene mayor precisión conforme crece el recall encierra más área.

![[Pasted image 20260930112901.png]]

> Es necesario nombrar el protocolo al informar mAP. **VOC 2007** empleó AP interpolada en 11 puntos; evaluaciones VOC posteriores integraron los cambios de recall. **COCO** interpola en 101 niveles de recall y promedia umbrales de IoU de $0.50$ a $0.95$ con paso $0.05$, además de otras condiciones del benchmark.

#### 6. Selective Search

> **Selective Search** sustituye recortes arbitrarios por un conjunto menor de **region proposals** con contenido visual coherente. Primero divide la imagen en regiones pequeñas mediante segmentación basada en grafos; después combina repetidamente las regiones más similares para formar otras mayores. Las cajas que envuelven esas regiones se utilizan como localizaciones candidatas.

> La figura permite seguir la segmentación inicial, las fusiones sucesivas y las propuestas finales. Se generan regiones a distintas escalas sin evaluar todas las cajas geométricamente posibles.

![[Pasted image 20260930112902.png]]

#### 7. Anchor Boxes

> Las **anchor boxes** son cajas predefinidas de varias escalas y formas centradas en posiciones de la imagen o del mapa de rasgos. Para una imagen de anchura $w$ y altura $h$, una escala $s\in(0,1]$ y un parámetro de forma $r>0$, las dimensiones usadas son

$$
a_w=ws\sqrt r,\qquad a_h=\frac{hs}{\sqrt r}.
$$

> Así, la relación efectiva anchura/altura es $a_w/a_h=(w/h)r$; si la imagen es cuadrada, coincide con $r$. La figura muestra cómo variar $s$ y $r$ produce cajas centradas en un mismo punto que cubren objetos de tamaños y proporciones diferentes.

![[Pasted image 20260930112903.png]]

> Con $n$ escalas $s_1,\ldots,s_n$ y $m$ razones $r_1,\ldots,r_m$, usar todas las parejas en los $wh$ centros produce $whnm$ anchors. Para reducirlas, se toman solo las combinaciones que contienen la escala de referencia $s_1$ o la razón de referencia $r_1$:

$$
(s_1,r_1),\ldots,(s_1,r_m),(s_2,r_1),\ldots,(s_n,r_1).
$$

> Hay $n+m-1$ formas distintas por centro y $wh(n+m-1)$ anchors en total. Se suele escoger $s_1$ como escala intermedia y $r_1$ como razón neutra. Los anchors sirven como puntos de partida para predecir cajas ajustadas a los objetos.

### III. The R-CNN Family

#### 8. R-CNN

> **R-CNN (Region-based Convolutional Neural Network)** realiza detección a partir de regiones candidatas. Su proceso original separa la propuesta de cajas, la extracción de rasgos y la decisión final. El diagrama deja ver que cada propuesta pasa de forma independiente por la CNN.

![[Pasted image 20260930112904.png]]

1. **Selective Search** propone unas $2000$ regiones por imagen.
2. Cada región se redimensiona al tamaño exigido por una CNN preentrenada, truncada antes de su salida. La CNN extrae sus rasgos y puede ajustarse para las clases objetivo y *background*.
3. Un conjunto de **SVM**, una por clase, clasifica los rasgos de cada región.
4. Una regresión lineal corrige las coordenadas de la propuesta hacia la caja real.
5. Se trasladan las coordenadas a la imagen original y se aplican un umbral de confianza y NMS.

> La extracción repetida de rasgos domina el coste: con $n$ regiones y lotes de tamaño $b$ se requieren aproximadamente $\lceil n/b\rceil$ pasadas de la CNN. Las SVM y la regresión lineal describen el enfoque original; otras cabezas podrían cumplir esas funciones, pero no eliminan por sí solas el trabajo redundante sobre regiones solapadas.

#### 9. Fast R-CNN

##### 9.1. Shared Feature Extraction

> **Fast R-CNN** calcula una sola vez el mapa de rasgos de la imagen completa. Selective Search aún genera propuestas, pero cada una se proyecta sobre ese mapa compartido. Tras **RoI pooling**, una cabeza FC predice su clase y la corrección de su caja; finalmente se recuperan coordenadas de la imagen y se filtran las detecciones con umbral y NMS.

> El esquema muestra el cambio decisivo: la CNN recibe la imagen una vez y sus rasgos alimentan todas las propuestas, en vez de procesar cada recorte por separado.

![[Pasted image 20260930112905.png]]

> Si la salida de la CNN tiene forma $1\times c\times h_1\times w_1$ y hay $n$ propuestas, RoI pooling produce un tensor $n\times c\times h_2\times w_2$. Al aplanarlo se obtiene $n\times d$, con $d=c\,h_2w_2$, que sirve de entrada a las capas FC de clasificación y regresión. El extractor convolucional es entrenable.

##### 9.2. Region of Interest (RoI) Pooling

> **RoI pooling** convierte regiones de tamaños distintos en matrices de tamaño fijo. Una región de $H\times W$ se reparte en una cuadrícula objetivo de $h\times w$ celdas, con tamaños aproximados $\lceil H/h\rceil\times\lceil W/w\rceil$ y posibles celdas menores en los bordes. En cada celda y canal se aplica una agregación, habitualmente el máximo.

> En el ejemplo, la región $3\times3$ se transforma en $2\times2$. Los máximos de las cuatro zonas son $6$, $4$, $3$ y $9$, respectivamente.

![[Pasted image 20260930112906.png]]

#### 10. Faster R-CNN

> **Faster R-CNN** conserva la extracción compartida y la segunda etapa de Fast R-CNN, pero aprende las propuestas mediante una **Region Proposal Network (RPN)** en lugar de usar Selective Search. La RPN trabaja sobre el mapa de rasgos de la CNN: una convolución produce características para anchors de varias escalas y razones, y dos salidas predicen **objectness** (objeto frente a fondo) y ajustes de caja.

> El diagrama distingue la RPN, a la derecha, de la cabeza de detección final, a la izquierda. Ambas reutilizan el mapa de rasgos.

![[Pasted image 20260930112907.png]]

1. La CNN calcula los rasgos de la imagen y la RPN evalúa anchors centrados en posiciones de ese mapa.
2. Se conservan las cajas con puntuación de objeto suficiente y NMS elimina propuestas duplicadas.
3. Las propuestas restantes pasan por RoI pooling y la cabeza final predice clases y cajas refinadas.
4. Se expresan las cajas en coordenadas de la imagen original y se aplican el umbral final y NMS.

> La RPN y el detector se entrenan conjuntamente: la función objetivo incluye clasificación y regresión tanto de anchors como de detecciones finales. Aprender propuestas adecuadas permite trabajar con menos regiones y evita el coste de Selective Search.

#### 11. Historical Comparison

> Esta comparación histórica de las variantes R-CNN en VOC 2007 muestra el cambio de escala en tiempo de inferencia. Las cifras dependen de la configuración experimental y no son tiempos universales de cada familia.

| Modelo | Tiempo por imagen | Aceleración | mAP (VOC 2007) |
|---|---:|---:|---:|
| R-CNN | 50 s | $1\times$ | 66.0 % |
| Fast R-CNN | 2 s | $25\times$ | 66.9 % |
| Faster R-CNN | 0.2 s | $250\times$ | 69.9 % |

> [!warning] Corrección
> En la tabla de las diapositivas aparece 66.9 % de mAP para Faster R-CNN en VOC 2007, pero el resultado de la configuración comparada es 69.9 %.
> Fuente de comprobación: [Artículo original de Faster R-CNN](https://arxiv.org/pdf/1506.01497).

### IV. Single-Stage Object Detection

#### 12. YOLOv1

##### 12.1. Grid and Predictions

> Los detectores **two-stage** de la familia R-CNN generan propuestas y después las clasifican y refinan. Un detector **single-stage** como **YOLO (You Only Look Once)** usa rasgos de toda la imagen para predecir conjuntamente cajas y clases en una pasada, sin una fase explícita de propuestas. En su versión original se informó de 45 imágenes por segundo; la comparación de velocidad y precisión corresponde a aquellas versiones y condiciones.

> YOLOv1 divide la imagen en una cuadrícula $S\times S$. La celda que contiene el **centro** de un objeto es responsable de predecirlo. La figura usa $S=5$ y muestra cajas de jugador y balón: pueden abarcar zonas extensas aunque se asignen a celdas concretas.

![[Pasted image 20260930112908.png]]

> Cada celda predice $B$ cajas, cada una con centro $(x,y)$, dimensiones $(w,h)$ y confianza $\hat C_{ij}$ para la caja $j$ de la celda $i$. Además, predice una sola distribución sobre las $C$ clases. El tensor de salida tiene forma

$$
S\times S\times(5B+C).
$$

> En YOLOv1, $(x,y)$ se expresa respecto a los límites de la celda y $(w,h)$ respecto a la imagen completa. La confianza estima presencia de objeto y calidad de la caja, $\Pr(\mathrm{Object})\cdot\mathrm{IoU}$; en inferencia la IoU se predice, pues no se conoce la caja real. Cada clase tiene una probabilidad condicional por celda, $\Pr(\mathrm{Class}_c\mid\mathrm{Object})$; la puntuación de la caja $j$ para la clase $c$ es $\hat C_{ij}\hat p_i(c)$. Después se aplican un umbral de confianza y NMS.

> [!warning] Corrección
> En los apuntes se describe el centro $(x,y)$ como relativo a la propia caja y la quinta predicción se simplifica a $p(\mathrm{object})$. En YOLOv1 el centro es relativo a la celda y la quinta predicción es una confianza que combina presencia e IoU.
> Fuente de comprobación: [Artículo original de YOLOv1](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Redmon_You_Only_Look_CVPR_2016_paper.pdf).

##### 12.2. Architecture and Limitations

> La arquitectura original emplea 24 capas convolucionales y dos FC. Alterna reducciones $1\times1$ con convoluciones $3\times3$, usa **Leaky ReLU** salvo en la última capa lineal y reordena la salida FC como $S\times S\times(5B+C)$. Con $S=7$, $B=2$ y $C=20$, la salida es $7\times7\times30$. La arquitectura y estos hiperparámetros pueden modificarse.

> La predicción de clases se comparte entre las $B$ cajas de una celda. Por eso **YOLOv1 solo puede asignar una clase por celda** y producir como máximo $B$ cajas de esa misma clase. Puede fallar si los centros de objetos de clases distintas caen en la misma celda o si hay más de $B$ objetos que la celda deba representar.

#### 13. YOLOv1 Loss

##### 13.1. Assignment and Targets

> La imagen tiene $S^2$ celdas, cada una con $B$ predictores de caja y una distribución sobre $C$ clases. Usamos $i\in\{1,\ldots,S^2\}$ para la celda, $j\in\{1,\ldots,B\}$ para el predictor y $c\in\{1,\ldots,C\}$ para la clase. Una variable sin sombrero es el objetivo real y con sombrero es la salida del modelo.

> Si la celda $i$ contiene un objeto, su caja real es $B_i=(x_i,y_i,w_i,h_i)$ y la caja predicha por $j$ es $\hat B_{ij}=(\hat x_{ij},\hat y_{ij},\hat w_{ij},\hat h_{ij})$. El predictor con mayor IoU respecto a $B_i$ se hace **responsable** de ese objeto. Entonces $\mathbf1^{\mathrm{obj}}_{ij}=1$ para ese predictor; $\mathbf1^{\mathrm{obj}}_i=1$ indica que la celda contiene un objeto y $\mathbf1^{\mathrm{noobj}}_{ij}=1-\mathbf1^{\mathrm{obj}}_{ij}$ marca los predictores no responsables.

> La confianza predicha es $\hat C_{ij}$. Para el predictor responsable, el objetivo puede ser $C_{ij}=\operatorname{IoU}(\hat B_{ij},B_i)$; se puede usar $C_{ij}=1$ como simplificación. Para los predictores no responsables, el objetivo de confianza es $0$. La etiqueta $p_i(c)$ es *one-hot* en una celda con objeto y $\hat p_i(c)$ es la predicción de clase.

##### 13.2. Four Loss Terms

> YOLOv1 emplea una suma de errores cuadráticos para caja, confianza de la caja responsable, confianza de cajas no responsables y clasificación:

$$
\mathcal L=\mathcal L_{\mathrm{BB}}+\mathcal L_{\mathrm{O}}
+\mathcal L_{\mathrm{NO}}+\mathcal L_{\mathrm{C}}.
$$

$$
\begin{aligned}
\mathcal L_{\mathrm{BB}}
&=\lambda_{\mathrm{coord}}\sum_{i=1}^{S^2}\sum_{j=1}^{B}
\mathbf1^{\mathrm{obj}}_{ij}\Big[
(x_i-\hat x_{ij})^2+(y_i-\hat y_{ij})^2\\
&\hspace{5em}
+(\sqrt{w_i}-\sqrt{\hat w_{ij}})^2
+(\sqrt{h_i}-\sqrt{\hat h_{ij}})^2\Big],\\
\mathcal L_{\mathrm{O}}
&=\sum_{i=1}^{S^2}\sum_{j=1}^{B}
\mathbf1^{\mathrm{obj}}_{ij}(C_{ij}-\hat C_{ij})^2,\\
\mathcal L_{\mathrm{NO}}
&=\lambda_{\mathrm{noobj}}\sum_{i=1}^{S^2}\sum_{j=1}^{B}
\mathbf1^{\mathrm{noobj}}_{ij}\hat C_{ij}^{\,2},\\
\mathcal L_{\mathrm{C}}
&=\sum_{i=1}^{S^2}\mathbf1^{\mathrm{obj}}_i
\sum_{c=1}^{C}\big(p_i(c)-\hat p_i(c)\big)^2.
\end{aligned}
$$

> Solo la caja responsable recibe pérdida de coordenadas y de confianza positiva; todos los predictores no responsables aportan a $\mathcal L_{\mathrm{NO}}$, incluso si su celda contiene un objeto asignado a otra caja. La pérdida de clase se calcula una vez por celda con objeto. Esta asignación favorece que distintos predictores se especialicen en ciertas formas y tamaños.

> La abundancia de celdas sin objeto podría dominar el entrenamiento, por lo que se aumenta el peso de coordenadas y se reduce el de ausencia: en el modelo original $\lambda_{\mathrm{coord}}=5$ y $\lambda_{\mathrm{noobj}}=0.5$. Usar $\sqrt w$ y $\sqrt h$ evita penalizar de igual forma un mismo error absoluto en cajas grandes y pequeñas. La pérdida cuadrática es fácil de optimizar, aunque no coincide directamente con maximizar AP.

### V. Exercises

#### 14. Proposed Exercises

> Los ejercicios del tema se recogen como enunciados, sin soluciones añadidas.

1. **Single Object Detection:** entrenar un detector de un solo objeto con datos propios o descargados y equilibrar clasificación y regresión de caja.
2. **Naive Proposal Generation:** generar $c$ cajas aleatorias por píxel, visualizar una muestra y discutir su coste.
3. **Intersection over Union:** implementar IoU con un parámetro que permita elegir entre $(x_1,y_1,x_2,y_2)$ y $(x,y,w,h)$.
4. **Non-Maximum Suppression:** implementar NMS a partir de cajas, confianzas y umbral $\varepsilon$, y probarlo con cajas muy solapadas.
5. **Mean Average Precision:** calcular curvas precision–recall por clase y mAP a partir de predicciones, cajas reales y umbral IoU, usando, por ejemplo, la regla trapezoidal con NumPy.
6. **Anchor Box Generation:** generar anchors para una imagen $H\times W$ a partir de escalas y razones; hallar el número exacto si solo se usan combinaciones que contienen $s_1$ o $r_1$.
7. **Region of Interest Pooling:** transformar un mapa $C\times H\times W$ en $C\times h\times w$, tratando los tamaños de celda aproximados $\lceil H/h\rceil\times\lceil W/w\rceil$ y aplicando, por ejemplo, el máximo.
8. **Architectural Implementations:** escribir desde cero el pseudocódigo o código PyTorch de las pasadas *forward* de R-CNN y Fast R-CNN, destacando el número de extracciones convolucionales.
9. **Architectural Variations:** proponer clasificadores y regresores alternativos para la familia R-CNN, como Gradient Boosting Classifier o Random Forest Regressor, y discutir efectos sobre entrenamiento y retropropagación.
10. **YOLO Loss Function:** explicar matemáticamente cómo la raíz cuadrada de anchura y altura en $\mathcal L_{\mathrm{BB}}$ afecta de forma distinta a los errores de cajas pequeñas y grandes.
11. **Two-Stage vs. Single-Stage Detectors:** comparar ventajas, límites y situaciones reales en las que se elegiría YOLO o Faster R-CNN.

### VI. Final Summary

> Detectar objetos exige localizar y clasificar varias regiones. Las cajas describen su posición; **IoU** mide solapamiento, **NMS** elimina duplicados y **mAP** resume precisión y recall bajo un protocolo concreto. **Selective Search** y **anchor boxes** reducen la búsqueda de propuestas frente al barrido exhaustivo.

> R-CNN evalúa cada propuesta por separado; Fast R-CNN comparte una extracción de rasgos; Faster R-CNN aprende las propuestas con una RPN. **YOLOv1** predice cajas y clases directamente sobre una cuadrícula: gana rapidez al prescindir de propuestas explícitas, con límites cuando varios objetos compiten por una misma celda. Su pérdida distribuye el entrenamiento entre localización, confianza y clasificación según qué predictor es responsable de cada objeto.
