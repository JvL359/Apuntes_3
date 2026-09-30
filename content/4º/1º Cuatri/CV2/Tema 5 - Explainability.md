---
estado: pendiente de revisión
---

### I. Introduction

#### 1. Why Explainability Matters

> Los modelos de visión pueden acertar una predicción y, aun así, basarse en una pista espuria del fondo, fallar al cambiar el entorno o reproducir sesgos de los datos. Una **explicación** ayuda a inspeccionar qué información influyó en una salida concreta, detectar errores y comunicar las limitaciones del sistema. Esto resulta especialmente relevante cuando una decisión afecta a personas o a la seguridad, como en diagnóstico médico, conducción autónoma o justicia.

> Una visualización convincente **no demuestra por sí sola** que el modelo haya utilizado causalmente las zonas resaltadas. Conviene separar la pregunta «¿qué muestra este método?» de «¿es fiel al comportamiento del modelo?», que se estudiará mediante perturbaciones, reentrenamiento y pruebas de aleatorización.

#### 2. Interpretability and Explainability

> Un modelo **interpretable** permite seguir directamente su mecanismo de decisión: los coeficientes de una regresión lineal o las reglas de un árbol de decisión pequeño son ejemplos de *white box*. La **explainability** construye una explicación *post hoc* para un modelo cuyo funcionamiento no se puede leer de ese modo, como una CNN o un ensemble complejo (*black box*). La distinción describe el acceso humano al razonamiento del modelo; las técnicas de explicación también pueden aplicarse a modelos interpretables.

> Distinguiremos explicaciones **locales**, que justifican una predicción de clase $c$ para una imagen $x$, de análisis de **representaciones internas**, que muestran qué patrones activan capas o canales. En las fórmulas, $f_c(x)$ será una salida escalar de la clase de interés, normalmente un *logit* o una probabilidad. La elección debe mantenerse fija al comparar imágenes alteradas.

### II. Visualization of Internal Features

#### 3. Maximally Activating Patches

> Para averiguar qué patrones reales detecta una CNN, se introducen imágenes en la red, se registra la activación de una **capa y canal elegidos** y se localizan las posiciones de mayor respuesta. La activación de un canal es un mapa espacial; para resumir toda una capa puede agregarse la dimensión de canales mediante media o máximo. Se escala el mapa a la resolución de la imagen y se examinan los parches de entrada correspondientes a sus máximos.

> Así se pueden comparar detectores de rasgos locales con otros más abstractos y descubrir si responden a partes del objeto o a detalles irrelevantes. La región dibujada es una **correspondencia espacial aproximada**: cada posición del mapa depende de su campo receptivo, por lo que el parche de entrada relevante puede ser mayor que una simple celda reescalada. El procedimiento muestra estímulos existentes en los datos; no caracteriza todas las situaciones en las que el canal puede activarse.

#### 4. Gradient Ascent

> **Gradient ascent** busca un estímulo sintético que maximice la salida de una clase, neurona, canal o capa. Se parte de ruido o de una imagen inicial y se modifican los **píxeles**, manteniendo fijos los pesos de la red. Si $f(x)$ es la activación escogida y `agg` reduce sus dimensiones a un escalar, puede utilizarse una penalización para evitar valores extremos:

$$
F(x)=\operatorname{agg}(f(x))-\lambda\|x\|_2,
\qquad
x^\star=\arg\max_x F(x),
\qquad
x_{t+1}=x_t+\alpha\nabla_xF(x_t).
$$

> Aquí $\lambda$ controla la regularización y $\alpha$ es el tamaño del paso. Para una clase final, $f(x)$ ya es escalar; para un canal se puede tomar la media, el máximo o una norma espacial, y para una capa se agregan también los canales. En algunos análisis interesa agregar el valor absoluto de las respuestas para no descartar activaciones negativas de gran magnitud. La imagen resultante enseña qué aumenta la activación elegida, aunque su aspecto artificial puede dificultar interpretarla; regularización y recorte de valores estabilizan la optimización.

#### 5. Feature Inversion

> **Feature inversion** pregunta qué información conserva una representación interna. Primero se calcula $f(x_0)$ para la imagen original $x_0$; después se busca otra imagen $x$ cuyas activaciones en la capa o canal elegido se parezcan a las originales. Una formulación es

$$
x^\star=\arg\min_x F(x),
\qquad
F(x)=\|f(x)-f(x_0)\|_2^2+\lambda\|x\|_2.
$$

> Se optimizan los píxeles de $x$ mediante descenso por gradiente, con los parámetros de la CNN fijos. En capas poco profundas suelen recuperarse bordes, texturas y una imagen parecida a $x_0$; en capas profundas, la reconstrucción puede ser más difusa y conservar sobre todo estructura semántica. La reconstrucción no prueba que el modelo haya «olvidado» por completo un detalle: también depende de la capa escogida, la regularización y el procedimiento de optimización.

![[Pasted image 20260930150100.png]]

> En las tres parejas, la imagen original aparece a la izquierda y su reconstrucción a la derecha. La comparación permite observar qué detalles se conservan en la representación utilizada.

#### 6. DeepDream

> **DeepDream** también modifica los píxeles para aumentar activaciones, pero empieza con una **imagen real** y potencia los patrones que la red ya detecta en ella. Se selecciona una capa o conjunto de canales, se define una agregación de sus activaciones y se repite el paso de ascenso de gradiente. El resultado amplifica rasgos presentes o sugeridos por la entrada, sin constituir una explicación cuantitativa de una clase.

![[Pasted image 20260930150101.png]]

> En la comparación, optimizar capas tempranas acentúa texturas y detalles locales (izquierda); optimizar capas profundas hace aparecer patrones de objetos más complejos (derecha). Es una forma visual de explorar la jerarquía de representaciones de la CNN.

### III. Perturbation-Based Methods

#### 7. Masking as an Experiment

> Los métodos de **perturbación** alteran regiones de la entrada y observan cómo cambia $f_c(x)$. Son *model agnostic*: requieren evaluar el modelo, pero no acceder a sus gradientes ni a su arquitectura. La máscara sustituye los píxeles ocultos por un **baseline** escogido, como cero, una media o una versión desenfocada. Por tanto, el resultado mide la importancia **respecto a ese modo concreto de ocultar**, no una propiedad independiente del baseline.

> Un parche grande requiere menos evaluaciones y produce una localización gruesa; uno pequeño mejora la resolución espacial, pero aumenta el coste y puede perder contexto. Además, una imagen con parches artificiales puede quedar fuera de la distribución de entrenamiento y alterar la predicción por el propio artefacto. Esta limitación debe tenerse presente tanto al explicar como al evaluar.

#### 8. SHAP

##### 8.1. Shapley Values

> **SHAP** atribuye a cada región de una imagen una contribución a la salida de una clase. Se divide la imagen en $M$ regiones, normalmente *superpixels* o parches, y se consideran coaliciones $S$ de regiones visibles. Si $N=\{1,\ldots,M\}$ y $f(S)$ es la predicción de la imagen donde solo se conservan las regiones de $S$, la contribución de la región $i$ se calcula promediando sus cambios marginales sobre todas las coaliciones que no la contienen:

$$
\phi_i=
\sum_{S\subseteq N\setminus\{i\}}
\frac{|S|!\,(M-|S|-1)!}{M!}
\bigl[f(S\cup\{i\})-f(S)\bigr].
$$

> El coeficiente asigna el mismo peso a cada orden posible de incorporación de regiones. La **diferencia conserva el signo**: $\phi_i>0$ indica apoyo a la clase respecto al baseline elegido; $\phi_i<0$, oposición. Por eso un mapa SHAP puede mostrar regiones positivas y negativas. La definición de $f(S)$ depende de cómo se representan las regiones ausentes; en imágenes suele usarse una máscara o una sustitución aproximada.

> Para $N=\{A,B,C\}$, las coaliciones previas a $A$ son $\varnothing$, $\{B\}$, $\{C\}$ y $\{B,C\}$. Sus pesos respectivos son $1/3$, $1/6$, $1/6$ y $1/3$. Por ejemplo, $A$ aparece primero en dos de las seis permutaciones y después de ambas regiones en otras dos; así se interpreta el peso $1/3$ de los extremos.

> [!warning] Corrección
> En las diapositivas y los apuntes aparece un valor absoluto alrededor de $f(S\cup\{i\})-f(S)$. En el valor de Shapley la diferencia es **con signo**; tomar su valor absoluto impediría representar contribuciones negativas y rompería la descomposición aditiva de la predicción.
> Fuente de comprobación: [Lundberg y Lee, *A Unified Approach to Interpreting Model Predictions*](https://proceedings.neurips.cc/paper_files/paper/2017/file/8a20a8621978632d76c43dfd28b67767-Paper.pdf).

![[Pasted image 20260930150102.png]]

> El mapa muestra qué zonas apoyan (rojo) u oponen (azul) la salida de distintas clases. La misma imagen puede tener explicaciones diferentes para clases diferentes.

##### 8.2. KernelSHAP in Practice

> Evaluar las $2^M$ coaliciones es inviable para una imagen dividida en muchas regiones. **KernelSHAP** muestrea coaliciones y ajusta un modelo lineal local a las **predicciones del modelo original**, no a las etiquetas verdaderas. Para una coalición $S$, $x_S$ conserva sus regiones y sustituye el resto por el baseline; su valor es $v(S)=f_c(x_S)$. El vector $z\in\{0,1\}^M$ indica qué regiones se conservan, y el modelo auxiliar es

$$
g(z)=\phi_0+\sum_{i=1}^{M}\phi_i z_i,
\qquad
\pi(S)=\frac{M-1}{\binom{M}{|S|}\,|S|\,(M-|S|)}
\quad (0<|S|<M).
$$

> Cada muestra de regresión es el par $(z,v(S))$ y se pondera con el **Shapley kernel** $\pi(S)$. Las coaliciones vacía y completa tienen pesos singulares y se imponen como restricciones: $\phi_0=v(\varnothing)$ y $\sum_i\phi_i=v(N)-v(\varnothing)$, de modo que $f_c(x)=\phi_0+\sum_i\phi_i$. La aproximación depende del muestreo, el baseline y cualquier regularización o selección de regiones añadida. Con todas las coaliciones y el ajuste ponderado adecuado se recuperan los valores de Shapley; una regresión lineal arbitraria no tiene esa garantía.

> [!warning] Corrección
> Una diapositiva califica de «opcional» la ponderación con el Shapley kernel. En **KernelSHAP** esa ponderación es necesaria para recuperar los valores de Shapley mediante regresión lineal; omitirla define otro ajuste.
> Fuente de comprobación: [Lundberg y Lee, *A Unified Approach to Interpreting Model Predictions*](https://proceedings.neurips.cc/paper_files/paper/2017/file/8a20a8621978632d76c43dfd28b67767-Paper.pdf).

#### 9. Occlusion

> **Occlusion** recorre la imagen con una ventana enmascarada y mide el cambio de una salida escalar. Para una imagen alterada $x'$, se usa la diferencia **con signo**

$$
\Delta=f_c(x)-f_c(x').
$$

> Si $\Delta>0$, la región retirada apoyaba la clase; si $\Delta<0$, la presencia de la región se oponía a ella. Con una ventana $S\times S$ de paso uno, se inicializan un acumulador $A$ y un contador de cobertura $K$ de tamaño $H\times W$. En cada posición se suma $\Delta$ en la ventana correspondiente de $A$ y uno en la misma ventana de $K$. El mapa final es $A/K$ donde $K>0$: dividir por el número de oclusiones evita que los píxeles centrales tengan más peso solo por haber sido cubiertos más veces.

> Con ventanas válidas y paso uno, hacen falta $(H-S+1)(W-S+1)$ predicciones alteradas, además de calcular una vez $f_c(x)$. Al aumentar $S$ o el *stride* baja el coste, pero el mapa pierde detalle. Una oclusión que tape parte del objeto y del fondo atribuye el cambio al parche completo, por lo que la resolución no equivale automáticamente a precisión causal.

#### 10. RISE

> **RISE** (*Randomized Input Sampling for Explanation*) sustituye el barrido ordenado por $N$ máscaras aleatorias $M_n$. Calcula $f_c(x\odot M_n)$ para cada imagen enmascarada y suma las máscaras ponderadas por esa salida: las regiones conservadas en máscaras que mantienen alta la puntuación reciben mayor valor. Su estimador, cuando el valor esperado de cada posición de máscara es $p$, es

$$
S_c(x)=\frac{1}{Np}\sum_{n=1}^{N}f_c(x\odot M_n)\,M_n.
$$

> La multiplicación por $M_n$ es **elemento a elemento** y $f_c(x\odot M_n)$ es un escalar. En la construcción de máscaras, cada celda de una cuadrícula pequeña $s\times s$ se muestrea con una Bernoulli$(p)$. Con $c_H=\lceil H/s\rceil$ y $c_W=\lceil W/s\rceil$, la cuadrícula se interpola bilinealmente a $(s+1)c_H\times(s+1)c_W$ y se recorta a $H\times W$ con desplazamientos aleatorios de $0$ a $c_H-1$ y de $0$ a $c_W-1$. La interpolación produce valores continuos entre 0 y 1; el desplazamiento evita que todas las máscaras compartan los mismos límites de celda. Muestrear directamente una Bernoulli por píxel es más simple, pero suele dar mapas menos estables. $N=4000$, $s\in\{7,14\}$ y $p=0{,}5$ son configuraciones de ejemplo, no constantes del método.

> [!warning] Corrección
> En los apuntes se define $p$ como probabilidad de **enmascarar** el píxel, aunque la máscara multiplicativa vale $1$ cuando lo **conserva**. En la fórmula con divisor $Np$, $p=P(M_n(i,j)=1)$ es la probabilidad de conservarlo.
> Fuente de comprobación: [Petsiuk, Das y Saenko, *RISE: Randomized Input Sampling for Explanation of Black-box Models*](https://arxiv.org/html/1806.07421).

![[Pasted image 20260930150103.png]]

> El esquema enseña cómo cada máscara produce una imagen parcial y una puntuación, que después pondera esa máscara en el mapa final. RISE requiere muchas evaluaciones, pero solo acceso a entradas y salidas del modelo.

### IV. Gradient-Based Methods

#### 11. Local Sensitivity

> Los métodos basados en gradientes miden cómo cambia $f_c(x)$ ante una variación **infinitesimal** de los píxeles. Necesitan un modelo diferenciable y acceso a su retropropagación, pero normalmente obtienen una primera explicación con una pasada hacia delante y otra hacia atrás. Un gradiente grande indica sensibilidad local; no demuestra por sí solo cuánto cambiaría la predicción al eliminar de verdad una región amplia.

#### 12. Saliency Maps

> Un **saliency map** para una imagen RGB $x\in\mathbb R^{3\times H\times W}$ condensa el gradiente de la clase $c$ respecto a los tres canales en cada posición $(i,j)$:

$$
S_{i,j}(x)=\max_{k\in\{1,2,3\}}
\left|\frac{\partial f_c(x)}{\partial x_{k,i,j}}\right|,
\qquad S(x)\in\mathbb R^{H\times W}.
$$

> El máximo del valor absoluto detecta sensibilidad tanto positiva como negativa. Da un mapa rápido y fácil de superponer, pero puede ser ruidoso y **pierde el sentido del efecto**: una zona brillante no indica si aumentar su intensidad sube o baja la puntuación de la clase. Para conservar el signo habría que observar los gradientes por separado.

#### 13. Input × Gradient

> **Input × Gradient** pondera la sensibilidad por el valor presente en la entrada:

$$
S_{i,j}(x)=\max_{k\in\{1,2,3\}}
\left|x_{k,i,j}\frac{\partial f_c(x)}{\partial x_{k,i,j}}\right|.
$$

> Puede destacar píxeles cuyo valor y gradiente son simultáneamente grandes, pero atenúa los que tienen intensidad baja o cero aunque su gradiente sea importante. Comparte con el saliency map el ruido y la pérdida de signo tras tomar valores absolutos. El resultado depende de la representación y escala de los píxeles.

#### 14. Modified ReLU Backpropagation

##### 14.1. Guided Backpropagation

> En una ReLU estándar, la derivada deja pasar el gradiente entrante solo donde la activación previa fue positiva. **Guided Backpropagation** exige además que el gradiente entrante sea positivo: aplica la máscara de la pasada hacia delante y una segunda máscara al gradiente. Suele producir mapas más nítidos, pero modifica la derivada real del modelo y puede resaltar patrones visuales sin atribuir fielmente la predicción de la clase.

##### 14.2. DeconvNet

> **DeconvNet** deja pasar los gradientes entrantes positivos aunque la neurona correspondiente no se activase en la pasada hacia delante. Sirve para visualizar qué estímulos excitan una unidad interna, pero tampoco es la retropropagación matemática original de la red. No invierte literalmente una convolución: «deconvolution» forma parte del nombre histórico de la visualización.

![[Pasted image 20260930150104.png]]

> El esquema compara las cuatro reglas en una ReLU: pasada hacia delante, retropropagación estándar, DeconvNet y Guided Backpropagation. La diferencia decisiva es qué posiciones se anulan: por activación previa, por signo del gradiente entrante o por ambos.

#### 15. SmoothGrad

> **SmoothGrad** reduce la variabilidad visual de un mapa calculándolo sobre $N$ imágenes perturbadas con ruido gaussiano y promediando las explicaciones:

$$
x_i=x+\varepsilon_i,\quad
\varepsilon_i\sim\mathcal N(0,\sigma^2),
\qquad
\overline S(x)=\frac{1}{N}\sum_{i=1}^{N}S(x_i).
$$

> Se puede envolver con este promedio un método de atribución basado en gradientes. Si los mapas conservan el signo, los valores opuestos pueden cancelarse; conviene decidir si se promedian mapas firmados o magnitudes según lo que se quiera interpretar. Como ejemplos de configuración aparecen $N$ entre 10 y 100 y $\sigma$ entre el 10 % y el 20 % del rango de píxeles. Mejorar la estabilidad cuesta aproximadamente $N$ evaluaciones y retropropagaciones.

#### 16. Integrated Gradients

> **Integrated Gradients** (IG) compara la imagen $x$ con un **baseline** $x'$ e integra el gradiente de $f_c$ a lo largo del segmento $x'+\alpha(x-x')$. Para cada componente $q$ de la entrada,

$$
\operatorname{IG}_{q}(x)=
(x_q-x'_q)\int_0^1
\frac{\partial f_c\!\left(x'+\alpha(x-x')\right)}
{\partial x_q}\,d\alpha.
$$

> Se aproxima con $M$ puntos del recorrido, evitando calcular una integral analítica:

$$
\operatorname{IG}_{q}(x)\approx
(x_q-x'_q)\frac1M\sum_{k=1}^{M}
\left.
\frac{\partial f_c(u)}{\partial u_q}
\right|_{u=x'+\frac{k}{M}(x-x')}.
$$

> Integrar a lo largo del camino puede detectar contribuciones que el gradiente **en $x$** no muestra por saturación. Un baseline negro, una media o una imagen desenfocada son posibilidades, pero deben representar razonablemente «ausencia de señal» para la clase y se ha de comprobar qué salida producen. Más pasos aproximan mejor la integral a costa de más cálculo; una referencia distinta también puede cambiar la atribución.

> La propiedad de **completitud** establece, para la integral exacta y las condiciones habituales de diferenciabilidad,

$$
\sum_q\operatorname{IG}_{q}(x)=f_c(x)-f_c(x').
$$

> En la suma numérica la igualdad es aproximada; su discrepancia permite comprobar si hacen falta más pasos. Como referencia práctica, pueden utilizarse $M$ entre 50 y 300 pasos. La garantía corresponde a integrar el **gradiente real** de la salida, no a sustituirlo sin más por cualquier mapa de saliencia.

> [!warning] Corrección
> Los apuntes afirman que la suma de las atribuciones de IG es la diferencia entre la **imagen** y el baseline. La completitud relaciona las **salidas escalares** del modelo: $\sum_q\operatorname{IG}_{q}(x)=f_c(x)-f_c(x')$.
> Fuente de comprobación: [Sundararajan, Taly y Yan, *Axiomatic Attribution for Deep Networks*](https://proceedings.mlr.press/v70/sundararajan17a/sundararajan17a.pdf).

### V. Ad Hoc Methods

#### 17. Class Activation Mapping (CAM)

> **CAM** localiza las regiones que apoyan una clase en CNN cuya última capa convolucional va seguida de **Global Average Pooling** (GAP) y una capa clasificadora lineal. En esta derivación, $f_c$ es la puntuación lineal de clase **antes de softmax** (*logit*). Si $A_{i,j,k}(x)$ es el mapa del canal $k$ de tamaño $h\times w$, GAP calcula

$$
F_k(x)=\frac1{hw}\sum_{i=1}^{h}\sum_{j=1}^{w}A_{i,j,k}(x),
\qquad
f_c(x)=b_c+\sum_{k=1}^{n}w_k^cF_k(x).
$$

> Al sustituir $F_k$ y reagrupar las sumas,

$$
f_c(x)=b_c+\frac1{hw}\sum_{i=1}^{h}\sum_{j=1}^{w}
\underbrace{\sum_{k=1}^{n}w_k^cA_{i,j,k}(x)}_{M_c(i,j)},
\qquad
M_c(i,j)=\sum_{k=1}^{n}w_k^cA_{i,j,k}(x).
$$

> Los pesos $w_k^c$ conectan cada canal con la clase $c$; $b_c$ es el sesgo, que afecta a la puntuación pero no a la localización espacial. Se interpola $M_c$ a la resolución de la entrada para superponerlo. CAM es eficiente y fácilmente interpretable, aunque exige esa arquitectura GAP más clasificador lineal.

![[Pasted image 20260930150105.png]]

> En el diagrama, cada canal genera un mapa espacial; la suma ponderada por los pesos de la clase produce su mapa CAM.

#### 18. Grad-CAM

> **Grad-CAM** elimina el requisito de GAP y de una cabeza lineal. Se elige una capa convolucional, normalmente una profunda, y se calculan los gradientes de $f_c(x)$ respecto a sus $n$ mapas $A_k$ de tamaño $h\times w$. El peso de cada canal es la media espacial de esos gradientes:

$$
\alpha_k^c=\frac1{hw}\sum_{i=1}^{h}\sum_{j=1}^{w}
\frac{\partial f_c(x)}{\partial A_{i,j,k}(x)},
\qquad
M_c(i,j)=
\operatorname{ReLU}\!\left(\sum_{k=1}^{n}\alpha_k^c A_{i,j,k}(x)\right).
$$

> La ReLU del mapa combinado deja visibles las posiciones asociadas **positivamente** con la clase. Se reescala el resultado a $H\times W$ para visualizarlo sobre la imagen. Una capa profunda ofrece información más abstracta y contextual, pero suele tener menor resolución espacial; por ello Grad-CAM localiza **regiones** y no necesariamente píxeles precisos. Se aplica a CNN con capas convolucionales aunque no tengan la arquitectura concreta de CAM; no se extiende sin adaptación a una red sin dichos mapas.

#### 19. Guided Grad-CAM

> **Guided Grad-CAM** multiplica elemento a elemento el mapa Grad-CAM reescalado y el mapa de Guided Backpropagation. El primero selecciona las regiones relacionadas con la clase y el segundo aporta detalle de alta resolución. La combinación puede verse más precisa, pero hereda la limitación de Guided Backpropagation: el detalle visible no prueba una atribución causal fiel.

#### 20. Attention as Explainability

> Los pesos de **attention** de un ViT u otro modelo indican cómo se combinan representaciones en una capa y cabeza concreta. Una atención alta no implica necesariamente que esa región **cause** la predicción: intervienen otras cabezas, capas y transformaciones, y el mapa puede cambiar con el contexto. Puede aportar una pista exploratoria, pero exige validación adicional mediante sensibilidad, perturbaciones o intervenciones antes de tratarlo como explicación de la salida.

### VI. Evaluation

#### 21. Common Problems of Attribution Maps

> Un mapa debe juzgarse por su **fidelidad al modelo**, no por su atractivo visual. Entre los problemas recurrentes están:

- **Gradientes inestables o ruidosos:** pequeñas variaciones de entrada modifican mucho el mapa; SmoothGrad promedia varias perturbaciones.
- **Cambios rápidos de signo:** tomar valores absolutos muestra magnitud, pero elimina la dirección de la contribución.
- **Rasgos irrelevantes o poco específicos de clase:** Guided Backpropagation limpia el aspecto del mapa, mientras que Grad-CAM selecciona evidencia relacionada con $c$; Guided Grad-CAM combina localización y detalle sin garantizar fidelidad.
- **Saturación:** una derivada local casi nula puede ocultar una contribución; IG integra a lo largo de un recorrido.
- **Gradientes que se desvanecen:** retropropagar por muchas capas puede debilitar la señal; Grad-CAM analiza gradientes de una capa convolucional profunda.
- **Sensibilidad solo local:** un gradiente en $x$ no revela por sí mismo el efecto de suprimir una región; IG considera un recorrido, SmoothGrad una vecindad y Grad-CAM mapas con contexto espacial.

#### 22. Loyalty and Inverse Loyalty

> **Loyalty** comprueba si las regiones más importantes del mapa realmente sostienen la predicción. Se ordenan de mayor a menor importancia, se eliminan progresivamente y se mide la caída de la salida para $c$. **Inverse loyalty** elimina primero las regiones menos importantes: si el orden es bueno, la predicción cambia poco al principio y cae al retirar las importantes al final.

> Para una salida positiva $f_c(x)$, si $x_t$ es la imagen tras retirar una fracción $t$ de regiones, una curva de **caída relativa** coherente con las gráficas es

$$
D_c(t)=\frac{f_c(x)-f_c(x_t)}{f_c(x)}
=1-\frac{f_c(x_t)}{f_c(x)}.
$$

> Al usar esta ordenada, una explicación fiel produce una **AUC alta** en loyalty y **baja** en inverse loyalty. En cambio, si se representa la probabilidad residual $f_c(x_t)$, una buena curva de eliminación de regiones importantes tiene **AUC baja**. Hay que indicar qué magnitud aparece en el eje vertical antes de comparar números de AUC; cambiar el baseline o la granularidad del borrado cambia también el resultado.

> [!warning] Corrección
> Los apuntes imprimen $1-[f_c(x)-f_c(x_t)]/f_c(x)$ como «diferencia» de loyalty, pero esa expresión equivale a $f_c(x_t)/f_c(x)$ y **disminuye** al caer la predicción. Las gráficas crecientes de loyalty usan la caída relativa $[f_c(x)-f_c(x_t)]/f_c(x)$. Si se usase la probabilidad restante, la interpretación de la AUC se invertiría.
> Fuente de comprobación: [Petsiuk, Das y Saenko, *RISE: Randomized Input Sampling for Explanation of Black-box Models*](https://arxiv.org/html/1806.07421).

![[Pasted image 20260930150106.png]]

> La curva izquierda retira primero zonas relevantes y asciende rápido (loyalty, AUC 0,90); la derecha retira primero zonas irrelevantes y tarda en subir (inverse loyalty, AUC 0,31). Son ejemplos de la **caída relativa**. La eliminación puede generar imágenes fuera de distribución, como en Occlusion, por lo que una buena AUC no constituye una prueba definitiva de causalidad.

#### 23. Remove and Retrain (ROAR)

> **ROAR** (*RemOve And Retrain*) comprueba la utilidad de un orden de importancia dejando que el modelo se **reentrene** tras eliminar información. Se entrena un modelo original, se calculan mapas para las imágenes y se suprimen los píxeles más importantes en **entrenamiento y prueba**. Para cada proporción eliminada se entrena desde cero un modelo nuevo y se mide su rendimiento, comparándolo con un borrado aleatorio y, opcionalmente, con el orden inverso.

> Si el método identifica información realmente útil para aprender, suprimir primero sus píxeles debería empeorar el rendimiento del modelo reentrenado más que suprimir píxeles aleatorios. El coste es alto porque requiere múltiples entrenamientos. Además, el resultado depende de qué información queda disponible y de cómo se enmascara: una caída sin reentrenar puede exagerar la importancia de píxeles cuyo contenido aún puede recuperarse del resto de la imagen.

![[Pasted image 20260930150107.png]]

> Las curvas comparan precisión sin reentrenar (izquierda) y con ROAR (derecha). El orden que parece mejor por la fuerte caída inicial puede dejar, tras reentrenar, más información utilizable que una eliminación aleatoria; por eso ambas evaluaciones pueden llevar a conclusiones distintas.

#### 24. Sanity Checks

##### 24.1. Model Parameter Randomization Test

> Se compara la explicación de un modelo entrenado con la obtenida tras **reinicializar parámetros**. En la variante en cascada se aleatorizan capas progresivamente desde la salida hacia la entrada; en la variante independiente se modifica una sola capa y se conservan las demás. Un mapa casi idéntico pese al cambio de pesos no sirve para estudiar con fidelidad lo aprendido por esas capas, aunque aún pueda visualizar propiedades de la entrada.

![[Pasted image 20260930150108.png]]

> La figura compara métodos al reinicializar capas por separado. Hay que observar si los patrones cambian al alterar los parámetros de los que supuestamente depende la explicación.

##### 24.2. Data Randomization Test

> Se permutan las **etiquetas de entrenamiento** y se entrena otra red con la misma arquitectura hasta que ajuste esa relación aleatoria. Después se comparan sus mapas con los del modelo entrenado con etiquetas correctas. Una explicación sensible a lo aprendido debería cambiar; si el modelo aleatorizado no llega a ajustar las etiquetas, la comparación se parece más a contrastar un modelo entrenado con otro no entrenado.

![[Pasted image 20260930150109.png]]

> Los mapas y su correlación muestran la respuesta a etiquetas verdaderas y aleatorias. Conviene combinar inspección visual y una medida numérica (por ejemplo, correlación de rangos o SSIM), ya que una apariencia similar puede esconder diferencias de signo u orden. El resultado depende del modelo, datos y transformación visual, y no establece una clasificación universal de métodos.

### VII. Exercises

#### 25. Proposed Exercises

> Los ejercicios de implementación presuponen una CNN preentrenada, como ResNet50 en PyTorch, y un conjunto de imágenes de clases distintas. Los siguientes son **enunciados**; no se incluyen soluciones nuevas.

##### 25.1. Concepts and Derivations

- **Exercise 1 — Importance of Explainability.** Argumentar por qué son necesarias las explicaciones en contextos como sanidad, justicia penal o navegación autónoma.
- **Exercise 2 — Grad-CAM and CAM.** Partiendo de $F_k=\frac1Z\sum_{i,j}A_{i,j,k}$ y $f_c=b_c+\sum_k w_k^cF_k$, demostrar que, para la arquitectura de CAM, $\alpha_k^c=\frac1Z\sum_{i,j}\frac{\partial f_c}{\partial A_{i,j,k}}$ equivale a $w_k^c$ salvo un factor proporcional.
- **Exercise 3 — Computing Gradients.** Para $f(x)=\operatorname{ReLU}(x)-\operatorname{ReLU}(x-10)$ y $x=15$, calcular el gradiente ordinario, explicar su saturación y calcular Integrated Gradients con baseline $x'=0$.
- **Exercise 4 — Complexity of SHAP and Occlusion.** Derivar el coste asintótico del cálculo exacto de Shapley y de Occlusion para $N$ píxeles o regiones, y justificar el muestreo de Monte Carlo.

##### 25.2. Internal Features

- **Exercise 5 — CNN Feature Maps.** Extraer y representar activaciones de distintas capas; describir cómo evolucionan de capas tempranas a profundas.
- **Exercise 6 — Maximally Activating Patches.** Visualizar los parches de mayor activación en varias capas o, alternativamente, los correspondientes a los cinco filtros más activos de una capa profunda.
- **Exercise 7 — Gradient Ascent.** Sintetizar desde ruido una imagen que maximice la probabilidad predicha de una clase objetivo, como «dog», formulando la optimización.
- **Exercise 8 — Feature Inversion.** Reconstruir una imagen, por ejemplo de un gato, a partir de representaciones de una capa y comparar la calidad entre capas tempranas y profundas.
- **Exercise 9 — DeepDream.** Aplicar DeepDream maximizando activaciones medias y comparar los patrones obtenidos en capas tempranas y profundas.

##### 25.3. Perturbation Methods

- **Exercise 10 — Shapley Values.** Implementar una aproximación Monte Carlo y representar un mapa de importancia de los píxeles o regiones.
- **Exercise 11 — Occlusion.** Deslizar una máscara por la imagen, crear el mapa de saliencia y analizar cómo el tamaño del parche afecta a resolución y tiempo.
- **Exercise 12 — RISE.** Generar máscaras aleatorias, evaluar las imágenes parciales y ponderar cada máscara por la probabilidad de la clase para obtener el mapa.

##### 25.4. Gradient and CAM Methods

- **Exercise 13 — Saliency Map.** Calcular un mapa de sensibilidad de la salida mediante una pasada hacia atrás.
- **Exercise 14 — Input × Gradient.** Multiplicar los gradientes de la clase por la imagen original y visualizar la atribución.
- **Exercise 15 — Guided Backpropagation.** Modificar con *hooks* de PyTorch la retropropagación por ReLU y construir el mapa.
- **Exercise 16 — DeconvNet.** Usar *hooks* para reconstruir los estímulos asociados a una activación interna según la regla de DeconvNet.
- **Exercise 17 — SmoothGrad.** Aplicar el promedio sobre entradas ruidosas a un método base, como Saliency Maps, y comparar los mapas.
- **Exercise 18 — Integrated Gradients.** Sumar los gradientes a lo largo de la interpolación lineal desde un baseline, como una imagen negra, hasta la imagen objetivo.
- **Exercise 19 — CAM.** Extraer el mapa espacial de importancia de clase en una arquitectura adecuada para CAM.
- **Exercise 20 — Grad-CAM.** Capturar con *hooks* mapas y gradientes de la última capa convolucional y producir Grad-CAM sin exigir GAP.
- **Exercise 21 — Guided Grad-CAM.** Multiplicar elemento a elemento las visualizaciones de Guided Backpropagation y Grad-CAM.

##### 25.5. Evaluation

- **Exercise 22 — Loyalty and Inverse Loyalty.** Calcular y representar ambas curvas y sus AUC, visualizar el borrado progresivo y discutir el desplazamiento fuera de distribución.
- **Exercise 23 — ROAR.** En un conjunto ligero, como CIFAR-10 o MNIST, eliminar píxeles según los mapas, reentrenar y comparar la caída de precisión con un borrado aleatorio.
- **Exercise 24 — Sanity Checks.** Implementar las pruebas de aleatorización de parámetros y de etiquetas; comparar visualizaciones y cuantificar diferencias, por ejemplo con SSIM.

### VIII. Final Summary

> Para explorar **qué ha aprendido** una CNN, los parches de activación máxima usan imágenes reales; Gradient Ascent y DeepDream crean o intensifican estímulos; Feature Inversion comprueba qué información puede recuperarse de una representación. Ninguna de estas visualizaciones, por sí sola, demuestra qué causó una predicción concreta.

> Para explicar **una salida de clase**, SHAP, Occlusion y RISE preguntan al modelo por entradas enmascaradas y funcionan sin gradientes, a costa de muchas evaluaciones y de depender del baseline. Saliency Maps, Input × Gradient, SmoothGrad e Integrated Gradients utilizan sensibilidad diferenciable; IG agrega el recorrido desde una referencia y satisface completitud respecto al **cambio de salida**. CAM y Grad-CAM explotan mapas convolucionales; el primero exige GAP y clasificador lineal, mientras que el segundo usa gradientes de la clase para ponderar canales.

> La explicación debe contrastarse con el comportamiento real: loyalty e inverse loyalty comprueban el efecto de borrar regiones, ROAR incorpora reentrenamiento y los sanity checks prueban la dependencia de parámetros y etiquetas aprendidas. El criterio de AUC depende de si se representa **caída** o **probabilidad residual**, y las máscaras pueden crear imágenes fuera de distribución.
