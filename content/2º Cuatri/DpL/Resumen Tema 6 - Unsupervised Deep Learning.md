### I. Introduction
#### 1. Autoencoders: idea general y objetivo
> Los **autoencoders** son una herramienta central del _unsupervised deep learning_. Su objetivo es aprender una **representación eficiente** de los datos de entrada sin usar etiquetas explícitas y a partir de ella **reconstruir** la entrada original.
> ![[Pasted image 20260325174402.png]]
> Un autoencoder se compone de tres partes:
> - **Encoder**: transforma la entrada $x$ en una representación latente $h$.
> - **Latent layer**: contiene una representación comprimida del dato, normalmente de menor dimensión que la entrada.
> - **Decoder**: reconstruye la entrada a partir de la representación latente.
> 
> De forma general:  $h = f(x), \qquad r = g(h), \qquad r \approx x$
> 
> La idea importante no es solo reconstruir bien la entrada, sino conseguir que la **representación latente** capture la información relevante en un espacio más útil. Esto es especialmente importante porque trabajar directamente en el espacio original puede ser problemático: las distancias entre muestras no siempre reflejan bien sus relaciones reales. Un buen autoencoder aprende un **espacio embebido** donde esas relaciones quedan mejor organizadas, lo que permite aplicar después técnicas como _clustering_.
> 
> Aplicaciones destacadas:
> - reducción de dimensionalidad
> - detección de anomalías
> - denoising
> - extracción de características
#### 2. Entrenamiento y visión probabilística
> El entrenamiento clásico de un autoencoder busca minimizar la diferencia entre la entrada original y su reconstrucción. La función de pérdida más habitual es el **Mean Squared Error (MSE)**:  $$\mathcal{L}_{\text{MSE}} = |x - \hat{x}|^2$$Aquí, el encoder aprende la proyección $x \to h$ y el decoder la proyección $h \to \hat{x}$, tratando de que la reconstrucción sea lo más parecida posible a la entrada original.
> Además de esta formulación determinista, las diapositivas introducen una **visión probabilística** en la que encoder y decoder se modelan como distribuciones:  $$p_{\text{encoder}}(h \mid x), \qquad p_{\text{decoder}}(x \mid h)$$En este caso, el modelo ya no produce una única representación o reconstrucción, sino una **distribución** sobre posibles valores. El objetivo pasa a expresarse como maximización de la probabilidad de reconstrucción:  $$\max_{\theta} \log p_{\text{decoder}}(x \mid h; \theta) \quad \Leftrightarrow \quad \min_{\theta} - \log p_{\text{decoder}}(x \mid h; \theta)$$Esta formulación estocástica permite:
> - aprender espacios latentes más flexibles,
> - introducir aleatoriedad beneficiosa durante entrenamiento o inferencia,
> - mejorar la robustez frente a pequeñas perturbaciones,
> - servir de base para modelos como los **Variational Autoencoders (VAEs)**.
> 
> Como aplicación práctica, los autoencoders también pueden usarse en **semi-supervised learning**: primero se entrenan con gran cantidad de datos no etiquetados para aprender una buena representación y, después, se reutiliza el encoder como capa de _embedding_ sobre la que se añade una cabeza de clasificación entrenada con los pocos datos etiquetados disponibles. En general, esta estrategia puede funcionar mejor que entrenar directamente un clasificador solo con los datos etiquetados.

### II. Auto-Encoders
#### 1. Sparse Autoencoders
> Los **sparse autoencoders** introducen una restricción de **esparsidad** sobre la representación oculta. La motivación es que un autoencoder estándar, si no está suficientemente restringido, puede aprender representaciones triviales o demasiado distribuidas. Para evitarlo, se fuerza a que, para una entrada dada, **muchas neuronas de la capa oculta permanezcan inactivas** o con activación cercana a cero. 
> ![[Pasted image 20260325174519.png]]
> 
> La idea es que la red aprenda **características más selectivas y localizadas**, lo que suele mejorar la extracción de _features_, la interpretabilidad y reducir el _overfitting_. En este caso, la capa latente suele ser **más grande que la entrada**, de modo que la separación de características no depende de comprimir dimensionalmente, sino de imponer activaciones escasas.
> 
> Para imponer esta esparsidad, se añade un término de regularización a la función de pérdida:  $$L(x, g(f(x))) + \Omega(h)$$Dos formas de imponerla que aparecen en las diapositivas son:
> - **Regularización L1**: se añade una penalización del tipo  $$\lambda \sum |w|  
    \quad \text{o} \quad  
    \lambda \sum |h|$$para favorecer que los pesos o las activaciones sean pequeños, y así reducir el tamaño del espacio latente, tendiendo a poner muchos ceros para reducir esta métrica.
> 
> - **Penalización mediante divergencia KL**: se fija un nivel de activación media deseado $\rho$ para las neuronas ocultas, normalmente pequeño, y se compara con la activación media real $\hat{\rho}_j$ de cada neurona $j$. La penalización total es: $$\Omega = \sum_{j=1}^{H} \mathrm{KL}(\rho || \hat{\rho}_j)$$Aquí, $\rho$ es la activación media objetivo y $\hat{\rho}_j$ la activación media real de la neurona oculta $j$. Cuanto menor sea $\rho$, mayor es la esparsidad buscada.
> 
> La divergencia KL se interpreta tratando las activaciones medias como variables de Bernoulli: $\rho$ define la probabilidad objetivo de que una neurona esté activa y $\hat{\rho}_j$ la probabilidad observada. La discrepancia entre ambas se mide con:  $$\mathrm{KL}(\rho || \hat{\rho}_j) = \rho \log \frac{\rho}{\hat{\rho}_j} + (1-\rho)\log \frac{1-\rho}{1-\hat{\rho}_j}$$Al minimizar esta penalización dentro de la pérdida total, cada neurona es empujada a que su activación media se aproxime a $\rho$. Como consecuencia, para cada entrada solo unas pocas neuronas tienden a activarse, produciendo una **representación dispersa**. Esto favorece la **selectividad de características**, mejora la **interpretabilidad** y ayuda a **reducir activaciones redundantes**.
#### 2. Denoising Auto-Encoders
> Un **Denoising Autoencoder (DAE)** se entrena para **eliminar ruido de una entrada corrupta** y reconstruir su versión limpia. La idea clave es que, al obligar al modelo a recuperar la señal original a partir de una versión degradada, aprende representaciones **más robustas** y captura mejor la estructura esencial de los datos.
> 
> La motivación es que los datos reales suelen contener ruido. En lugar de aprender simplemente a copiar la entrada, el DAE aprende a reconstruir la **entrada limpia** a partir de una versión alterada. Entre los tipos de corrupción mencionados en las diapositivas están el **ruido gaussiano**, el **masking noise** y **dropout**.
> 
> La estructura básica es la siguiente:
> - Se parte de una entrada limpia $x$.
> - Se genera una versión corrupta $\tilde{x}$ mediante un proceso de corrupción $C(\tilde{x}\mid x)$.
> - El **encoder** recibe $\tilde{x}$ y produce una representación latente $h$.
> - El **decoder** reconstruye una salida $\hat{x}$ a partir de $h$, intentando aproximar la entrada limpia original $x$.
> 
> La pérdida se define comparando la reconstrucción con la entrada limpia, no con la entrada corrupta. En las diapositivas aparece, por ejemplo: $$\mathcal{L} = |x-\hat{x}|^2$$o una pérdida de **cross-entropy**, según el tipo de dato. En la formulación probabilística, el entrenamiento puede escribirse como la minimización de:  $$\large-\mathbb{E}_{x\sim \hat{p}_{\text{data}}(x)} \mathbb{E}_{\tilde{x}\sim C(\tilde{x}\mid x)} \log p_{\text{decoder}}(x \mid h=f(\tilde{x}))$$![[Pasted image 20260325174703.png]]
> 
> El procedimiento de entrenamiento sigue esta secuencia:
> _1._ Se toma una muestra limpia $x$ del conjunto de entrenamiento.
> _2._ Se genera una versión corrupta $\tilde{x}$.
> _3._ Se codifica $\tilde{x}$ para obtener la representación latente $h$.
> _4._ Se decodifica $h$ para producir la reconstrucción $\hat{x}$.
> _5._ Se compara $\hat{x}$ con la entrada limpia $x$.
> _6._ Se retropropaga el error de reconstrucción para actualizar encoder y decoder.
> 
> El ruido actúa además como una forma de **regularización**, ya que fuerza al modelo a aprender características **estables** e **invariantes frente a pequeñas perturbaciones**. Por eso, los DAE no solo sirven para limpiar datos corruptos, sino también para aprender representaciones más útiles que las de un autoencoder entrenado únicamente a copiar la entrada.
#### 3. Contractive Auto-Encoders
> Los **Contractive Autoencoders (CAE)** buscan aprender representaciones **robustas frente a pequeñas perturbaciones** en la entrada. La idea central es imponer que el encoder $f(x)$ sea **contractivo** en el entorno de los datos de entrenamiento, es decir, que pequeños cambios en la entrada produzcan cambios pequeños en la representación oculta.
> 
> Esta propiedad introduce una **invarianza local**: se preservan las variaciones esenciales de los datos, mientras que se suprimen las variaciones irrelevantes. Como resultado, las características aprendidas son menos sensibles al ruido y reflejan mejor la estructura intrínseca de los datos. A diferencia de los _denoising autoencoders_, que fuerzan robustez a través de la reconstrucción de entradas corruptas, los CAE **penalizan directamente la sensibilidad de la representación oculta** ante cambios en la entrada.
> 
> El entrenamiento minimiza una función objetivo regularizada compuesta por el error de reconstrucción más un término de contracción:  $$\mathcal{L} \sum_{x \in D_n} \left (L(x, \ g(f(x))) + \lambda ||J_f(x)||_F^2 \right)$$Aquí, $J_f(x)$ es el **Jacobiano** del encoder $f(x)$ respecto a la entrada $x$, y su norma de Frobenius mide cuánto cambia cada unidad oculta cuando cambian las dimensiones de entrada:  $$||J_f(x)||_F^2 = \sum_{i=1}^{d_h}\sum_{j=1}^{d_x} \left(\frac{\partial h_i}{\partial x_j}\right)^2$$Minimizar este término hace que la representación latente sea menos sensible a perturbaciones pequeñas. En activaciones no lineales, como la sigmoide, esta robustez no solo se consigue con pesos pequeños, sino también empujando las unidades hacia regiones de **saturación**, donde la derivada es cercana a cero. En el caso lineal, esta penalización del Jacobiano se reduce a una forma de regularización **L2** sobre los pesos.
> 
> En consecuencia, el encoder aprende un mapeo **localmente invariante** alrededor de los ejemplos de entrenamiento, capturando la estructura esencial del _manifold_ de datos y contrayendo las variaciones no relevantes.
#### 4. Variational Auto-Encoders
> Los **Variational Autoencoders (VAE)** son autoencoders con una formulación **probabilística y generativa**. En lugar de aprender una única representación latente determinista, aprenden una **distribución latente** a partir de la cual se pueden generar nuevas muestras de datos. ![[Pasted image 20260325174946.png]]
> 
> El **encoder probabilístico** transforma la entrada $x$ en una distribución aproximada sobre la variable latente $z: q_\phi(z\mid x)$. Normalmente, esta distribución se modela como una gaussiana cuyos parámetros son calculados por la red: $$q_\phi(z\mid x)=\mathcal{N}(z;\mu(x),\sigma^2(x))$$Es decir, no devuelve directamente un código latente, sino su **media** $\mu(x)$ y su **varianza** $\sigma^2(x)$.
> 
> A partir de esa distribución, se obtiene una muestra latente $z$. Para permitir el entrenamiento mediante backpropagation, se usa el **reparameterization trick**:  $$z=\mu(x)+\sigma(x)\odot \epsilon, \qquad \epsilon\sim\mathcal{N}(0,I)$$De este modo, la parte aleatoria queda separada en $\epsilon$, mientras que $\mu(x)$ y $\sigma(x)$ siguen siendo diferenciables respecto a los parámetros del modelo.
> 
> El **decoder probabilístico** recibe la variable latente $z$ y define una distribución de reconstrucción:  $$p_\theta(x\mid z)$$a partir de la cual se reconstruye la entrada. Por tanto, el flujo general del modelo es: $$x \rightarrow q_\phi(z\mid x) \rightarrow z \rightarrow p_\theta(x\mid z) \rightarrow x'$$con el objetivo de que la reconstrucción sea lo más parecida posible a la entrada original.
> 
> El entrenamiento de un VAE no minimiza solo un error de reconstrucción, sino que maximiza la **Evidence Lower Bound (ELBO)**: $$\mathcal{L}(\theta,\phi;x) = \mathbb{E}_{q_\phi(z\mid x)}[\log p_\theta(x\mid z)] - \mathrm{KL}\big(q_\phi(z\mid x)||p(z)\big)$$Esta función objetivo equilibra dos términos:
> - **Calidad de reconstrucción**: el término  $\mathbb{E}_{q_\phi(z\mid x)}[\log p_\theta(x\mid z)]$  favorece que el decoder reconstruya bien la entrada.
> - **Regularización del espacio latente**: el término  $\mathrm{KL}\big(q_\phi(z\mid x)||p(z)\big)$ fuerza a que la distribución latente aprendida sea cercana a un _prior_ $p(z)$, normalmente una gaussiana estándar.
> 
> En conjunto, maximizar la ELBO permite obtener reconstrucciones precisas y, al mismo tiempo, un **espacio latente bien regularizado**, continuo y adecuado para generación de nuevas muestras.
