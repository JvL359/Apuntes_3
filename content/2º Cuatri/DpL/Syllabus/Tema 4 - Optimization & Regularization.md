## D2DpL 5.5-5.6 Generalization y Dropout

### I. Alcance del Fragmento

#### 1. Qué Incluye y Qué Se Omite

> Este apunte cubre **solo** las secciones **5.5 Generalization in Deep Learning** y **5.6 Dropout** del capítulo 5.  
> Se **omite** cualquier contenido **anterior** al título _5.5_ (final de _5.4_) y se **omite** el **inicio de 5.7 Predicting House Prices on Kaggle**.

---

### II. Generalización en Deep Learning

#### 1. Motivación y Panorama del Problema

> El material recuerda la idea central: **ajustar el entrenamiento** es solo un objetivo intermedio; el objetivo real es **generalizar** y predecir bien en ejemplos nuevos de la misma población.  
> También insiste en que, aunque usamos algoritmos de optimización (y a veces los desarrollamos), la **optimización es un medio**, mientras que el deep learning es, en el fondo, una disciplina **estadística** orientada a generalización.
> 
> Situación actual según el texto:
> 
> - En la práctica, redes profundas entrenadas con **SGD** suelen **generalizar sorprendentemente bien** en muchos dominios (visión, NLP, series temporales, recomendación, salud, plegamiento de proteínas, juegos, etc.).
>     
> - En teoría, entender **por qué se optimizan** tan bien y **por qué generalizan** sigue siendo difícil: el campo se describe como “wild west” en ambos frentes, con teoría y práctica evolucionando rápido.
>     

#### 2. Sobreajuste, Sesgos Inductivos y Brecha de Generalización

> Según el material, por el “**no free lunch**” (Wolpert y Macready, 1995), cualquier algoritmo generaliza mejor para unas distribuciones y peor para otras: con un conjunto finito, el modelo depende de **supuestos** (sesgos inductivos).  
> Ejemplo que da el texto: un MLP profundo tiene sesgo inductivo hacia construir funciones complejas como **composición de funciones más simples**.
> 
> El entrenamiento se describe en dos fases:
> 
> - (i) **Ajustar** el entrenamiento.
>     
> - (ii) **Estimar el error de generalización** evaluando en datos _holdout_.
>     
> 
> Definiciones operativas del fragmento:
> 
> - **Brecha de generalización (generalization gap)**: diferencia entre rendimiento en entrenamiento y en test/holdout.
>     
> - **Overfitting**: cuando esa brecha es grande (caso extremo: error de entrenamiento ≈ 0 pero error de test significativo).
>     
> 
> Giro “contraintuitivo” en deep learning:
> 
> - En clasificación, modelos suelen ser lo bastante expresivos para **ajustar perfectamente** el entrenamiento incluso con datasets muy grandes.
>     
> - Aun así, a veces **aumentar expresividad** (más capas/nodos o más épocas) puede **reducir el error de generalización**.
>     
> - La relación complejidad–brecha puede ser **no monótona** con patrón de **double descent** (Nakkiran et al., 2021).
>     
> 
> Además, el material afirma que las cotas clásicas basadas en complejidad (p. ej., **VC dimension** o **Rademacher complexity**) **no explican** la generalización de redes profundas, porque estas pueden ajustar etiquetas arbitrarias incluso con regularización familiar como ℓ2.

#### 3. Inspiración Desde Modelos No Paramétricos

> El texto propone un cambio de perspectiva: aunque las redes tienen millones de parámetros (se actualizan, se guardan a disco), puede ser útil pensar que **se comportan en parte como modelos no paramétricos**, cuya complejidad “crece” con los datos.
> 
> Ejemplo principal: **k-nearest neighbors (k-NN)**:
> 
> - En entrenamiento: “memoriza” el dataset.
>     
> - En predicción: ante un punto (x), busca los (k) vecinos más cercanos según una distancia (d(x, x'_i)).
>     
> - Para (k=1), el error de entrenamiento es **cero**, pero aun así puede **generalizar**; el texto menciona que bajo condiciones suaves, 1-NN es **consistente** (converge al predictor óptimo).
>     
> 
> Punto clave: elegir (d) (o una featurización (\phi(x))) fija **sesgos inductivos** distintos; con datos finitos, distintas distancias producen predictores distintos.
> 
> Conexión con redes grandes:
> 
> - Por estar **sobre-parametrizadas**, tienden a **interpolar** (ajustar perfecto) y por eso “se parecen” a no paramétricos en algunos aspectos.
>     
> - Se menciona conexión teórica con métodos kernel: en el límite de MLPs infinitamente anchos con pesos aleatorios, se obtiene equivalencia con un kernel específico llamado **neural tangent kernel** (Jacot et al., 2018).
>     

#### 4. Early Stopping

> El material describe hallazgos en presencia de **ruido en etiquetas**:
> 
> - Las redes tienden a ajustar primero datos con etiquetas “limpias” y después a interpolar los ejemplos mal etiquetados (Rolnick et al., 2017).
>     
> - Si el modelo ajusta los limpios pero no los aleatorios incluidos en el entrenamiento, entonces **ha generalizado** (Garg et al., 2021).
>     
> 
> **Early stopping** como regularización:
> 
> - En vez de restringir directamente pesos, restringe el **número de épocas**.
>     
> - Criterio típico: monitorizar el **error de validación** (a menudo 1 vez por época) y parar cuando no disminuye más de un umbral (\epsilon) durante cierto número de épocas (**patience criterion**).
>     
> 
> Beneficio adicional destacado: **ahorro de tiempo/coste** en entrenamientos grandes (menciona modelos que pueden requerir días y múltiples GPUs).
> 
> Matiz del texto:
> 
> - Sin ruido de etiquetas y con datasets “realizables” (clases separables), early stopping suele aportar **pocas mejoras**.
>     
> - Con ruido o variabilidad intrínseca del label (ej. mortalidad), early stopping es **crucial** y entrenar hasta interpolar el ruido suele ser mala idea.
>     

#### 5. Regularización Clásica en Redes Profundas

> Se recuerda **weight decay** (Sección 3.7) como añadir un término a la pérdida para penalizar pesos grandes:
> 
> - ℓ2 → ridge
>     
> - ℓ1 → lasso
>     
> 
> Observación del material en deep learning:
> 
> - Las fuerzas típicas de ℓ2 suelen ser **insuficientes** para impedir interpolación; sus beneficios “como regularización” pueden tener sentido especialmente junto con **early stopping**.
>     
> 
> Interpretación alternativa sugerida por el texto:
> 
> - Puede que funcionen no porque reduzcan de verdad la “potencia” del modelo, sino porque **inducen sesgos inductivos** más compatibles con los patrones del dataset (analogía: como la métrica en 1-NN o decisiones de arquitectura).
>     
> 
> Conexión con la siguiente sección:
> 
> - Se menciona que también se usan técnicas como **añadir ruido a entradas**, y se anuncia **dropout** como técnica famosa (Srivastava et al., 2014).
>     

#### 6. Resumen de la Sección

> Ideas de cierre del material:
> 
> - Redes profundas suelen estar **sobre-parametrizadas** y pueden **ajustar perfectamente** el entrenamiento (interpolación).
>     
> - Pensarlas como **paramétricas** es natural, pero a veces intuiciones más fiables vienen de verlas como **no paramétricas**.
>     
> - Como muchos modelos candidatos ya ajustan entrenamiento, casi toda mejora viene de **mitigar overfitting** (cerrar la brecha).
>     
> - Intervenciones que mejoran generalización a veces parecen **aumentar** y otras **disminuir** complejidad, y la teoría clásica no lo explica bien: sigue siendo una gran cuestión abierta.
>     

#### 7. Ejercicios del Material

> Preguntas propuestas (5.5.6):
> 
> - En qué sentido fallan medidas clásicas de complejidad para explicar generalización en deep nets.
>     
> - Por qué early stopping puede verse como regularización.
>     
> - Cómo se decide típicamente el criterio de parada.
>     
> - Qué factor diferencia los casos donde early stopping mejora mucho.
>     
> - Otro beneficio de early stopping más allá de generalizar.
>     

---

### III. Dropout

#### 1. Motivación: Simplicidad y Robustez

> El material parte de lo que esperamos de un buen modelo: rendir bien en **datos no vistos**.  
> Desde teoría clásica, para cerrar la brecha train–test buscamos **modelos simples**; el texto concreta varias nociones de “simplicidad”:
> 
> - Pocas **dimensiones** (menciona la discusión de bases monomiales en Sección 3.6).
>     
> - Tamaño (inverso de la norma) de los parámetros: conexión con **weight decay (ℓ2)** (Sección 3.7).
>     
> - **Suavidad (smoothness)**: no ser sensible a pequeños cambios en la entrada (ej.: ruido en píxeles debería afectar poco a una clasificación).
>     
> 
> Se cita a Bishop (1995): entrenar con **ruido en la entrada** es equivalente a **Tikhonov regularization**, conectando formalmente “suavidad” con “resistencia a perturbaciones”.
> 
> Dropout (Srivastava et al., 2014) se presenta como idea para llevar esa noción a **capas internas**:
> 
> - Inyectar ruido durante el **forward** en capas internas.
>     
> - En _standard dropout_, se “dropea” (pone a cero) una fracción de nodos en cada iteración.
>     

#### 2. Intuición: Co-Adaptation y Analogía

> El texto define el problema como **co-adaptation**: cada capa puede depender de patrones específicos de activación de la capa previa.  
> El paper original usa una analogía con **reproducción sexual** para “romper” co-adaptaciones (el material dice explícitamente que esta justificación es debatible), pero resalta que la técnica ha sido duradera y está implementada en librerías estándar.

#### 3. Inyección de Ruido Sin Sesgo y Ecuación de Dropout

> Desafío clave según el material: inyectar ruido de forma **unbiased**, de modo que el valor esperado de una capa (fijando las otras) coincida con el valor sin ruido.  
> Ejemplo previo (Bishop): añadir ruido gaussiano a la entrada de un modelo lineal: (\epsilon \sim \mathcal{N}(0,\sigma^2)), (x' = x + \epsilon), con (\mathbb{E}[x'] = x).
> 
> En dropout estándar:
> 
> - Con probabilidad (p) se pone a cero una activación intermedia (h).
>     
> - Se “des-sesga” reescalando por la fracción retenida ((1-p)).
>     
> 
> Definición que da el texto (Ecuación 5.6.1):  
> [  
> h' =  
> \begin{cases}  
> 0 & \text{con probabilidad } p \  
> \frac{h}{1-p} & \text{en otro caso}  
> \end{cases}  
> ]  
> y por diseño (\mathbb{E}[h'] = h).

#### 4. Dropout en Práctica y Efecto en Gradientes

> Aplicado a una capa oculta, dropout puede verse como seleccionar una **subred** en cada iteración.  
> La figura 5.6.1 ilustra un MLP donde, tras dropout, se eliminan ciertas unidades (el texto menciona (h_2) y (h_5)); entonces:
> 
> - la salida ya no depende de esas unidades
>     
> - y sus gradientes **se anulan** en backprop  
>     Con esto, la capa de salida no puede depender “demasiado” de un único elemento de (h_1,\dots,h_5).
>     

#### 5. Dropout en Test y Excepción de Incertidumbre

> Regla típica del material:
> 
> - En **test**, normalmente se **desactiva** dropout: no se dropea nada y no hace falta reescalar.
>     
> 
> Excepción mencionada:
> 
> - Algunos investigadores usan dropout en test como heurística para estimar **incertidumbre**: si muchas ejecuciones con dropout dan predicciones parecidas, se interpreta como mayor confianza.
>     

---

### IV. Implementación de Dropout en el Material

#### 1. Implementación Desde Cero: Máscara Bernoulli

> Para una capa, el material propone:
> 
> - Muestrear una variable Bernoulli por elemento (1 = keep con probabilidad (1-p), 0 = drop con probabilidad (p)).
>     
> - Implementarlo fácilmente muestreando primero (U[0,1]) y quedándose con los nodos cuyo valor sea mayor que (p).
>     
> 
> El texto implementa `dropout_layer(X, dropout)` que:
> 
> - dropea con probabilidad `dropout`
>     
> - reescala dividiendo por (1-\text{dropout})
>     
> - maneja casos extremos (`dropout==1` devuelve ceros).
>     

```python
def dropout_layer(X, dropout):
    assert 0 <= dropout <= 1
    if dropout == 1: return torch.zeros_like(X)
    mask = (torch.rand(X.shape) > dropout).float()
    return mask * X / (1.0 - dropout)
```

#### 2. Prueba Rápida de la Capa de Dropout

> El material prueba la función con probabilidades 0, 0.5 y 1 sobre un tensor (2\times 8), mostrando que:
> 
> - con (p=0) no cambia nada
>     
> - con (p=1) todo se hace cero
>     
> - con (p=0.5) se anulan aproximadamente la mitad de entradas y las restantes se reescalan.
>     

```python
X = torch.arange(16, dtype=torch.float32).reshape((2, 8))
print('dropout_p = 0:', dropout_layer(X, 0))
print('dropout_p = 0.5:', dropout_layer(X, 0.5))
print('dropout_p = 1:', dropout_layer(X, 1))
```

#### 3. Modelo “Scratch” con Dropout Solo en Entrenamiento

> El modelo del texto aplica dropout tras la activación en cada capa oculta, con probabilidades distintas por capa.  
> También menciona una heurística común: usar **menor dropout** cerca de la entrada.  
> Punto operativo importante: se asegura que dropout solo está activo cuando `self.training` es verdadero.

```python
class DropoutMLPScratch(d2l.Classifier):
    def __init__(self, num_outputs, num_hiddens_1, num_hiddens_2,
                 dropout_1, dropout_2, lr):
        super().__init__()
        self.save_hyperparameters()
        self.lin1 = nn.LazyLinear(num_hiddens_1)
        self.lin2 = nn.LazyLinear(num_hiddens_2)
        self.lin3 = nn.LazyLinear(num_outputs)
        self.relu = nn.ReLU()

    def forward(self, X):
        H1 = self.relu(self.lin1(X.reshape((X.shape[0], -1))))
        if self.training:
            H1 = dropout_layer(H1, self.dropout_1)
        H2 = self.relu(self.lin2(H1))
        if self.training:
            H2 = dropout_layer(H2, self.dropout_2)
        return self.lin3(H2)
```

#### 4. Entrenamiento del Ejemplo

> El material entrena en Fashion-MNIST con batch size 256 y `max_epochs=10`, de forma similar a los MLPs anteriores.

```python
hparams = {'num_outputs':10, 'num_hiddens_1':256, 'num_hiddens_2':256,
           'dropout_1':0.5, 'dropout_2':0.5, 'lr':0.1}
model = DropoutMLPScratch(**hparams)
data = d2l.FashionMNIST(batch_size=256)
trainer = d2l.Trainer(max_epochs=10)
trainer.fit(model, data)
```

#### 5. Implementación Concisa con APIs de Alto Nivel

> Con APIs de alto nivel, el texto dice que basta con insertar capas `nn.Dropout(p)` después de cada fully-connected (o equivalente), pasando (p) como único argumento.  
> Comportamiento según el material:
> 
> - En entrenamiento: `Dropout` elimina aleatoriamente salidas de la capa anterior.
>     
> - Fuera de modo entrenamiento: `Dropout` deja pasar los datos tal cual en test.
>     

```python
class DropoutMLP(d2l.Classifier):
    def __init__(self, num_outputs, num_hiddens_1, num_hiddens_2,
                 dropout_1, dropout_2, lr):
        super().__init__()
        self.save_hyperparameters()
        self.net = nn.Sequential(
            nn.Flatten(), nn.LazyLinear(num_hiddens_1), nn.ReLU(),
            nn.Dropout(dropout_1), nn.LazyLinear(num_hiddens_2), nn.ReLU(),
            nn.Dropout(dropout_2), nn.LazyLinear(num_outputs))
```

---

### V. Resumen y Checklist del Fragmento

#### 1. Resumen de Ideas Clave

> - Generalización en deep learning: se enfatiza que optimizar entrenamiento es medio; el reto grande es entender y mejorar **generalización**, con fenómenos como interpolación y **double descent** que complican el relato clásico.
>     
> - Regularización práctica: **early stopping** (patience sobre validación) y regularizadores clásicos (como weight decay) siguen usándose, aunque su explicación teórica en deep nets es menos clara.
>     
> - Dropout: técnica de regularización por **ruido interno**; dropea activaciones con probabilidad (p) y reescala por (1-p) para mantener (\mathbb{E}[h']=h); típicamente solo en entrenamiento.
>     

#### 2. Checklist de Verificación

> Antes de dar por dominadas estas secciones, deberías poder:
> 
> - Definir **brecha de generalización** y explicar por qué “ajustar train” no basta.
>     
> - Explicar por qué medidas clásicas de complejidad (VC/Rademacher) no bastan para redes profundas según el texto.
>     
> - Describir el **patience criterion** de early stopping (validación + umbral (\epsilon) + paciencia).
>     
> - Escribir y explicar la ecuación de dropout (5.6.1) y justificar (\mathbb{E}[h']=h).
>     
> - Justificar por qué dropout suele desactivarse en test y mencionar la excepción de incertidumbre que cita el material.
>     
> - Implementar el `dropout_layer` del fragmento y activar dropout solo cuando `self.training` sea verdadero.
>     

---

### VI. Ejercicios del Material

#### 1. Ejercicios de Generalización

> Ver lista 5.5.6 (incluye preguntas sobre fallos de medidas clásicas, early stopping y sus beneficios/condiciones).

#### 2. Ejercicios de Dropout

> Preguntas propuestas (5.6.5):
> 
> - Cambiar probabilidades de dropout por capa (incluido intercambiarlas) y diseñar experimento.
>     
> - Aumentar épocas y comparar con/sin dropout.
>     
> - Analizar varianza de activaciones con/sin dropout y trazar su evolución.
>     
> - Por qué no se usa típicamente en test.
>     
> - Comparar dropout vs weight decay y combinarlos: si efectos son aditivos, hay rendimientos decrecientes o se cancelan.
>     
> - Aplicar dropout a pesos en vez de activaciones.
>     
> - Inventar otra técnica de ruido por capa y evaluar si supera a dropout en Fashion-MNIST (arquitectura fija).

## D2DpL 12. Optimization Algorithms

### I. Optimización y Dificultades en Deep Learning

#### 1. Qué Se Optimiza y Qué Problemas Aparecen

> En deep learning, **minimizar el error de entrenamiento** no garantiza obtener el mejor conjunto de parámetros para **generalizar**. Además, la optimización puede ser difícil porque:
> 
> - puede haber **muchos mínimos locales**;
>     
> - suele haber aún más **puntos silla** (porque en alta dimensión es probable que el Hessiano tenga autovalores negativos y positivos);
>     
> - pueden aparecer **gradientes evanescentes**, p. ej. en (f(x)=\tanh(x)), donde (f'(x)=1-\tanh^2(x)) puede ser muy pequeño (ej. (f'(4)=0.0013)), haciendo que el aprendizaje se estanque.
>     
> 
> El material enfatiza que, en la práctica, **no siempre hace falta el “mejor” mínimo**: soluciones locales o aproximadas pueden ser útiles, pero necesitamos **algoritmos robustos** y **buenas decisiones** (p. ej. activaciones tipo ReLU frente a saturación).

#### 2. Criterio de Mínimo Local, Máximo Local y Punto Silla (Hessiano)

> En un punto con **gradiente cero**:
> 
> - si los autovalores del Hessiano son **todos positivos** → **mínimo local**;
>     
> - si son **todos negativos** → **máximo local**;
>     
> - si hay **positivos y negativos** → **punto silla**.
>     
> 
> El material subraya que, en alta dimensión, los **puntos silla** son especialmente probables.

---

### II. Convexidad Como Herramienta de Análisis

#### 1. Por Qué Convexidad Importa Aquí

> Aunque la mayoría de problemas reales en deep learning **no son convexos**, el material usa convexidad para **motivar** y **entender** algoritmos de optimización con más detalle (y para justificar resultados teóricos en escenarios controlados).

#### 2. Propiedades Clave y Consecuencias

> Resumen de hechos que usa el capítulo:
> 
> - **Intersección** de conjuntos convexos es convexa; **unión** en general no.
>     
> - **Jensen**: la **esperanza** de una función convexa es (\ge) que la función convexa de la esperanza.
>     
> - Si (f) es dos veces derivable: (f) es convexa **ssi** su **Hessiano** es **semidefinido positivo**.
>     
> - Restricciones convexas pueden incorporarse vía **Lagrangiano**; en la práctica, a menudo se añaden como **penalización** al objetivo.
>     
> - **Proyecciones**: llevan un punto al **más cercano** dentro de un conjunto convexo (útil, p. ej., para imponer esparsidad proyectando sobre una **bola (\ell_1)**).
>     

---

### III. Descenso por Gradiente

#### 1. Idea General y Limitación Práctica

> El capítulo sitúa el **descenso por gradiente** como el extremo “determinista”: calcular gradiente usando **todo el dataset** y actualizar parámetros en cada paso.
> 
> Limitación práctica destacada al compararlo con métodos estocásticos: cuando los datos son **redundantes o muy similares**, usar todo el conjunto puede ser **poco eficiente** (en coste por iteración).

---

### IV. Descenso por Gradiente Estocástico (SGD)

#### 1. Actualización Estocástica y Efecto del Ruido

> En SGD, el gradiente se calcula con **una observación** (o una muestra) por paso. En el ejemplo del capítulo, esto genera trayectorias **más ruidosas** que en descenso por gradiente (incluso cerca del mínimo), debido a la incertidumbre del gradiente instantáneo.
> 
> Consecuencia práctica que enfatiza el material: con **tasa de aprendizaje constante**, el ruido puede impedir “refinar” la solución; la alternativa es **ajustar (\eta)** durante el entrenamiento.

#### 2. Tasa de Aprendizaje Dinámica (Schedules) En SGD

> El capítulo introduce estrategias básicas para (\eta(t)):
> 
> - **por tramos (piecewise constant)**:  
>     [  
>     \eta(t)=\eta_i \quad \text{si } t_i \le t \le t_{i+1}  
>     ]
>     
> - **decaimiento exponencial**:  
>     [  
>     \eta(t)=\eta_0 e^{-\lambda t}  
>     ]
>     
> - **decaimiento polinómico**:  
>     [  
>     \eta(t)=\eta_0 (\beta t + 1)^{-\alpha}  
>     ]  
>     El material comenta que el exponencial puede **decaer demasiado rápido** (parando “prematuramente”), y destaca que el polinómico con (\alpha=0.5) es una elección popular en convexos por propiedades teóricas.
>     

#### 3. Muestreo con y sin Reemplazo (Eficiencia de Datos)

> Aunque en una formulación “ideal” se podría muestrear de una distribución discreta sobre el dataset, el material aclara que en la práctica suele iterarse **sin reemplazo** (una permutación por época).
> 
> Razón: muestrear **con reemplazo** reduce eficiencia de datos. El capítulo muestra que, si eliges (n) veces con reemplazo:
> 
> - probabilidad de seleccionar un ejemplo (i) **al menos una vez**:  
>     [  
>     P(\text{elegir } i)=1-(1-1/n)^n \approx 1-e^{-1}\approx 0.63  
>     ]
>     
> - probabilidad de seleccionar un ejemplo **exactamente una vez**:  
>     [  
>     \binom{n}{1}\frac{1}{n}\left(1-\frac{1}{n}\right)^{n-1} \approx e^{-1}\approx 0.37  
>     ]  
>     Conclusión del material: se prefiere **sin reemplazo** (y es el **default** del libro), recorriendo el dataset en orden aleatorio distinto en cada época.
>     

#### 4. Resumen de Resultados y Limitaciones Teóricas

> Resumen del capítulo para SGD:
> 
> - En **convexo**, con una familia amplia de tasas de aprendizaje, SGD **converge** al óptimo.
>     
> - En deep learning (no convexo), el análisis convexo sirve como **intuición**: hay que **reducir** (\eta) progresivamente, **pero no demasiado rápido**.
>     
> - Problemas típicos: (\eta) **muy pequeña** (progreso lento/subóptimo) o **muy grande** (divergencia); se suele encontrar una buena (\eta) tras **múltiples experimentos**.
>     
> - Con datasets grandes, cada iteración de gradiente completo es cara: se prefiere SGD.
>     
> - En no convexo no hay garantías generales (p. ej., número de mínimos locales podría crecer exponencialmente).
>     

---

### V. SGD con Minibatches

#### 1. Motivación: “Entre Dos Extremos”

> El material presenta minibatches como un punto intermedio:
> 
> - Gradiente completo: **computacionalmente caro** por paso.
>     
> - SGD puro: menos eficiente en hardware porque CPU/GPU no explotan bien **vectorización**.
>     
> 
> Minibatch SGD busca **eficiencia estadística** (ruido útil) y **eficiencia computacional** (vectorización).

#### 2. Vectorización, Cachés y Localidad

> La decisión de usar minibatches se justifica por eficiencia de cómputo, especialmente al paralelizar (múltiples GPUs/servidores). El resumen enfatiza:
> 
> - la **vectorización** reduce overhead del framework;
>     
> - mejora **localidad de memoria y cachés** (CPU/GPU).
>     

#### 3. Resumen Operativo de Minibatch SGD

> Resumen del capítulo:
> 
> - existe un trade-off entre **eficiencia estadística** (más estocástico) y **eficiencia computacional** (batches grandes).
>     
> - en minibatch SGD se procesan batches obtenidos por **permutación aleatoria** del training set: cada observación se procesa **una vez por época**, en orden aleatorio.
>     
> - es aconsejable **decaer** la tasa de aprendizaje durante entrenamiento.
>     
> - medido en **tiempo de reloj**, minibatch SGD puede ser más rápido que SGD puro y que gradiente completo para alcanzar riesgos pequeños.
>     

---

### VI. Momentum

#### 1. Intuición y Ecuaciones

> Momentum agrega un **promedio móvil exponencial (leaky average)** de gradientes para acelerar convergencia (especialmente en direcciones “consistentes”) y suavizar oscilaciones.
> 
> El material lo escribe como:  
> [  
> v_t \leftarrow \beta v_{t-1} + (1-\beta) g_t,\qquad  
> x_t \leftarrow x_{t-1} - \eta v_t  
> ]  
> donde (g_t) es el gradiente del paso y (\beta) controla cuánto “histórico” se acumula.

#### 2. Lectura Como Promedio Ponderado y “Memoria Efectiva”

> El capítulo interpreta el leaky average como pesos geométricos sobre el pasado; la “cantidad efectiva” de historial está relacionada con (\frac{1}{1-\beta}) (cuanto más cerca de 1, más memoria).

---

### VII. AdaGrad

#### 1. Idea Central: Escalado por Coordenada

> AdaGrad adapta la tasa de aprendizaje **por coordenada** acumulando el cuadrado del gradiente en un estado (s). En la implementación “from scratch” del capítulo:  
> [  
> s \leftarrow s + g^2,\qquad  
> x \leftarrow x - \eta \frac{g}{\sqrt{s+\varepsilon}}  
> ]  
> con (\varepsilon) pequeño (p. ej. (10^{-6})) por estabilidad numérica.

#### 2. Cuándo Ayuda y Cuándo Puede Fallar

> Resumen del material:
> 
> - reduce (\eta) de forma dinámica y **por coordenada**;
>     
> - compensa coordenadas con gradientes grandes mediante un escalado que reduce el paso;
>     
> - útil como proxy de precondicionamiento cuando el problema es “desigual” por coordenadas;
>     
> - especialmente efectivo en **features dispersas**, donde ciertas coordenadas aparecen raramente;
>     
> - en deep learning puede ser **demasiado agresivo** reduciendo (\eta) (se enlaza con mejoras posteriores).
>     

---

### VIII. RMSProp

#### 1. Motivación Frente a AdaGrad

> El problema clave que marca el capítulo: en AdaGrad, (s_t) crece sin cota al acumular (g_t^2), y la tasa efectiva decrece aproximadamente como (O(t^{-1/2})), apropiado en convexos pero a veces no ideal en no convexos.
> 
> RMSProp introduce un promedio móvil exponencial en (s_t) para “olvidar” pasado:  
> [  
> s_t \leftarrow \gamma s_{t-1} + (1-\gamma) g_t^2,\qquad  
> x_t \leftarrow x_{t-1} - \eta \frac{g_t}{\sqrt{s_t+\varepsilon}}  
> ]  
> con (\varepsilon) típico (10^{-6}).

#### 2. Resumen del Material

> RMSProp:
> 
> - es similar a AdaGrad (usa (g^2) para escalar coordenadas),
>     
> - comparte con momentum el **leaky averaging**, pero aplicado al **precondicionador**,
>     
> - requiere que el experimentador **programe** la tasa de aprendizaje,
>     
> - (\gamma) determina “cuánta historia” se conserva al ajustar la escala por coordenada.
>     

---

### IX. Adadelta

#### 1. Idea: Calibrar el Paso con el Historial de Cambios

> Adadelta se presenta como variante de AdaGrad que reduce cuán “agresiva” es la adaptatividad por coordenada y, “tradicionalmente”, se describe como no teniendo tasa de aprendizaje explícita.
> 
> El capítulo define dos estados:
> 
> - (s_t): leaky average del segundo momento del gradiente,
>     
> - (\Delta x_t): leaky average del segundo momento del **cambio** en parámetros.
>     
> 
> Ecuaciones:  
> [  
> s_t = \rho s_{t-1} + (1-\rho) g_t^2  
> ]  
> [  
> x_t = x_{t-1} - g'_t  
> ]  
> [  
> g'_t = \frac{\sqrt{\Delta x_{t-1}+\varepsilon}}{\sqrt{s_t+\varepsilon}}, g_t  
> ]  
> [  
> \Delta x_t = \rho \Delta x_{t-1} + (1-\rho) (g'_t)^2  
> ]  
> con (\varepsilon) (p. ej. (10^{-5})) para estabilidad.

#### 2. Resumen del Material

> - Adadelta “no tiene” (\eta) explícita: usa el propio **ritmo de cambio** como calibración.
>     
> - requiere **dos** variables de estado (segundos momentos del gradiente y del cambio).
>     
> - usa leaky averages para estimar estadísticas relevantes de forma continua.
>     

---

### X. Adam y Yogi

#### 1. Adam: Unificación de Ideas Previas

> El material lo presenta como combinación de:
> 
> - minibatches (eficiencia por vectorización),
>     
> - momentum (historial de gradientes),
>     
> - escalado por coordenada tipo AdaGrad,
>     
> - desacople entre escalado y (\eta) tipo RMSProp.
>     
> 
> Define estados (EWMA):  
> [  
> v_t \leftarrow \beta_1 v_{t-1} + (1-\beta_1) g_t,\qquad  
> s_t \leftarrow \beta_2 s_{t-1} + (1-\beta_2) g_t^2  
> ]  
> con valores típicos (\beta_1=0.9), (\beta_2=0.999).
> 
> Como (v_0=s_0=0) sesga al inicio, introduce **bias correction**:  
> [  
> \hat v_t=\frac{v_t}{1-\beta_1^t},\qquad \hat s_t=\frac{s_t}{1-\beta_2^t}  
> ]
> 
> Rescalado y update:  
> [  
> g'_t = \frac{\eta \hat v_t}{\sqrt{\hat s_t}+\varepsilon},\qquad  
> x_t \leftarrow x_{t-1} - g'_t  
> ]  
> (con (\varepsilon) típico (10^{-6})).

#### 2. Yogi: Ajuste del Segundo Momento Para Evitar Explosión

> El material indica que Adam puede fallar incluso en convexos si la estimación del segundo momento (s_t) “se dispara”. Propone Yogi reescribiendo la actualización de Adam:  
> [  
> s_t \leftarrow s_{t-1} + (1-\beta_2)\bigl(g_t^2 - s_{t-1}\bigr)  
> ]  
> y sustituyendo el término por uno con signo:  
> [  
> s_t \leftarrow s_{t-1} + (1-\beta_2), g_t^2 \odot \operatorname{sgn}(g_t^2 - s_{t-1})  
> ]  
> (según el material, esto evita que la magnitud del update dependa del tamaño de la desviación).

#### 3. Resumen del Material (Adam)

> - Adam es una regla de actualización “robusta” que combina varias ideas previas.
>     
> - usa EWMA para momentum y segundo momento; aplica **bias correction**.
>     
> - con gradientes de alta varianza puede haber problemas de convergencia; el material menciona mitigaciones como **minibatches más grandes** o usar alternativas como **Yogi** para (s_t).
>     

---

### XI. Programación de la Tasa de Aprendizaje

#### 1. Por Qué Es Tan Importante Como el Algoritmo

> El capítulo remarca que ajustar (\eta) puede ser tan importante como el optimizador:
> 
> - (\eta) grande → **divergencia**; (\eta) pequeña → entrenamiento lento o subóptimo.
>     
> - influye el **condition number** del problema (mencionado en relación con momentum).
>     
> - también importa la **tasa de decaimiento**: si (\eta) no baja, podemos “rebotar” cerca del mínimo.
>     
> - aparece la idea de **warmup**: no empezar con pasos grandes cuando los parámetros son aleatorios.
>     
> 
> El capítulo se centra en schedulers “manejables” y muestra cómo gestionarlos con herramientas del framework.

#### 2. Políticas Básicas: Por Tramos, Exponencial y Polinómica

> El material lista (entre otras) estas formas típicas:
> 
> - piecewise constant, exponencial y polinómica (ver fórmulas en la sección de SGD).
>     
> 
> Además comenta que hay muchas variantes (p. ej. alternar rates), pero el capítulo prioriza las que admiten análisis más claro (especialmente en convexos).

#### 3. Schedulers Concretos del Capítulo

> El capítulo introduce schedulers y da ejemplos con entrenamiento (p. ej. en Fashion-MNIST). Incluye:
> 
> - scheduler tipo (\eta = \eta_0 (t+1)^{-1/2}) (square-root decay) como ejemplo de scheduler “callable”.
>     
> - **Factor scheduler** (multiplicativo):  
>     [  
>     \eta_{t+1} \leftarrow \eta_t \cdot \alpha,\quad \alpha\in(0,1),\qquad  
>     \eta_{t+1}\leftarrow \max(\eta_{\min}, \eta_t \cdot \alpha)  
>     ]
>     
> - **Multi-step** (piecewise): reducir (\eta) en hitos (t\in s) con un factor (\alpha).
>     

#### 4. Cosine Scheduler y Warmup

> El capítulo presenta el **cosine schedule** (Loshchilov y Hutter, 2016) para (t\in[0,T]):  
> [  
> \eta_t = \eta_T + \frac{\eta_0-\eta_T}{2}\bigl(1+\cos(\pi t/T)\bigr)  
> ]  
> y para (t>T) fija (\eta_t=\eta_T).
> 
> También describe **warmup**: un periodo inicial donde la tasa **aumenta** (típicamente lineal) hasta un máximo antes de “enfriarse”, para evitar divergencia inicial en arquitecturas inestables. El material señala que warmup puede combinarse con cualquier scheduler (no solo coseno).

#### 5. Resumen del Material (Scheduling)

> - bajar (\eta) durante entrenamiento puede mejorar precisión y, “perplejamente”, reducir overfitting.
>     
> - bajar (\eta) por tramos cuando el progreso se estanca funciona bien: primero converges rápido, luego reduces varianza bajando (\eta).
>     
> - cosine es popular en visión (sin garantía universal).
>     
> - warmup ayuda a evitar divergencia.
>     
> - la optimización afecta no solo al error de entrenamiento sino también a generalización/overfitting para el mismo error de entrenamiento.
>     

---

### XII. Checklist de Repaso del Capítulo

#### 1. Dominio Mínimo Operativo

> Antes de dar por “controlado” el capítulo, deberías poder:
> 
> - Explicar por qué en deep learning aparecen **mínimos locales**, **puntos silla** y **gradientes evanescentes**, y por qué esto complica optimización.
>     
> - Relacionar convexidad con: Hessiano PSD, Jensen, Lagrangiano y proyecciones (y qué aporta al análisis).
>     
> - Distinguir **gradiente completo**, **SGD** y **minibatch SGD** (trade-off estadística vs cómputo; permutación sin reemplazo).
>     
> - Escribir (y justificar cuándo conviene) las reglas de actualización de:
>     
>     - Momentum, AdaGrad, RMSProp, Adadelta, Adam, y la modificación de Yogi para (s_t).
>         
> - Enumerar y comparar estrategias de **learning rate scheduling** (piecewise, exponencial, polinómico, coseno, warmup) y explicar el “por qué” práctico de bajar (\eta).
>     

#### 2. Siguiente Paso

> Si quieres, en el siguiente turno puedo:
> 
> - convertir este resumen en un “apunte de examen” (muy compacto, solo fórmulas + cuándo usar cada método), o
>     
> - preparar **preguntas tipo examen** basadas en los ejercicios y resúmenes del capítulo (sin salir del material).
>
