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

