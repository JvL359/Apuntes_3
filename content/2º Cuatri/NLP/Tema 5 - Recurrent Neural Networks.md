### I. Motivación y Transición desde Ventana Fija
#### 1. Recordatorio del LM de Ventana Fija
> El material parte del “fixed-window LM” y recuerda su estructura general: embeddings de varias palabras concatenados $\Rightarrow$ capa oculta $\Rightarrow$ $\mathrm{softmax}$ para producir una distribución sobre el vocabulario.  
> También resume pros y contras:
> - Mejoras frente a $n$-gram: no hace falta almacenar todos los $n$-gram observados y generaliza mejor.
> - Problemas que quedan: la ventana fija es demasiado pequeña; aumentar la ventana aumenta los parámetros $W$ y $b$; y la ventana “nunca puede ser lo bastante grande”.  
>     Conclusión motivacional: hace falta una arquitectura que procese inputs de longitud arbitraria.
#### 2. Dejando Markov Atrás
> El material recalca que las redes feed-forward solo manejan entradas de longitud fija, y que en modelado de lenguaje eso fuerza una asunción tipo Markov como:  $$p(w_n\mid w_1,\dots,w_{n-1})=p(w_n\mid w_{n-3},w_{n-2},w_{n-1})$$Interpretación: el modelo tiene memoria limitada y no sabe lo que ocurrió mucho antes.  
> Se ilustra que dependencias de largo alcance pueden ser cruciales para predecir correctamente una palabra siguiente (ejemplo donde falta contexto para predecir “French”).

### II. RNN: Idea y Procesamiento Secuencial
#### 1. Consumo Secuencial de Tokens y Estado Oculto
> En un RNN-LM, el modelo “consume” tokens uno a uno:
> i) Para el primer token, se calcula su embedding $x^{(1)}=e(w^{(1)})$ y se inicializa el estado oculto $h^{(0)}$
> ii) En cada paso, se combina el embedding actual con el estado previo para obtener un nuevo estado:  $$h^{(t)}=\phi_h\left(W_x x^{(t)}+W_h h^{(t-1)}+b_h\right)$$iii) Tras consumir varios tokens, $h^{(t)}$ actúa como un “resumen en marcha” de la secuencia $(w_1,\dots,w_t)$.
#### 2. Distribución de Salida y Generación Autoregresiva
> Una vez se aplica la capa de salida, se obtiene una distribución sobre la siguiente palabra: $$y^{(t)}=\mathrm{softmax}\left(h^{(t)}W_{\text{out}}+b_{\text{out}}\right)$$El material describe el bucle de generación:
> - seleccionar el siguiente token desde $y^{(t)}$
> - realimentar ese token como siguiente entrada y continuar de forma autoregresiva.
#### 3. Visualización y “Unrolling” en el Tiempo
> El material muestra el “unrolling”: una misma celda RNN repetida a lo largo del tiempo, recibiendo $x^{(1)},x^{(2)},\dots$ y produciendo estados $h^{(1)},h^{(2)},\dots$ (y opcionalmente salidas $y^{(t)}$).  
> Idea clave: el estado en el paso $t$ depende de $h^{(t-1)}$ y de $x^{(t)}$.

### III. Definición Formal de RNN
#### 1. Definición de RNN
> Definición: un RNN procesa una secuencia de entradas $x^{(1)},\dots,x^{(T)}$ manteniendo un estado oculto $h^{(t)}\in\mathbb{R}^{d_h}$ que se actualiza secuencialmente: $$h^{(t)}=\phi_h\left(x^{(t)}W_x+h^{(t-1)}W_h+b_h\right)$$Opcionalmente, en cada paso $t$ produce una salida:  $$y^{(t)}=\phi_y\left(W_y h^{(t)}+b_y\right)$$Punto crucial del material: los mismos parámetros $W_x,W_h,W_y$ se comparten en todos los time-steps, lo que permite inputs de longitud arbitraria.

### IV. Modelos de Lenguaje Basados en RNN
#### 1. Definición de RNN-LM (Según el Material)
> Un RNN-LM es un RNN cuya capa de salida es un $\mathrm{softmax}$ sobre el vocabulario.  
> Sea el vocabulario $\mathcal{V}$ y una matriz de embeddings $E\in\mathbb{R}^{|\mathcal{V}|\times d_{\text{emb}}}$. Dado $w_t\in\mathcal{V}$, su embedding es $e(w_t)\in\mathbb{R}^{d_{\text{emb}}}.$  
> En cada paso $t:$  $$h^{(t)}=\phi_h\left(e(w_t)W_x+h^{(t-1)}W_h+b_h\right)$$$$P(\cdot\mid w_1,\dots,w_t)=\mathrm{softmax}\left(h^{(t)}W_y+b_y\right)\in\mathbb{R}^{|\mathcal{V}|}$$
#### 2. Pros y Contras del RNN-LM
> Ventajas listadas:
> - puede procesar inputs de cualquier longitud
> - el cómputo en el paso $t$ puede (en teoría) usar información de muchos pasos atrás
> - el tamaño del modelo no crece al aumentar el contexto de entrada
> - se aplican los mismos pesos en cada time-step (simetría en el procesamiento).  
> 
> Desventajas listadas:
> - el cómputo recurrente es lento
> - en la práctica es difícil acceder a información de muchos pasos atrás.

### V. Generación de Texto con un RNN-LM
#### 1. Procedimiento de Generación (Según el Material)
> Dada una secuencia de entrada $w_1,\dots,w_n$, el material describe:
> i) procesar toda la secuencia sin generar outputs: calcular $h^{(1)},h^{(2)},\dots,h^{(n)}$
> ii) generar la primera palabra tras consumir la entrada completa:  $$P(w_{n+1}\mid w_1,\dots,w_n)=\mathrm{softmax}\left(W_y h^{(n)}+b_y\right)$$iii) escoger $w_{n+1}$ muestreando desde esa distribución
> iv) seguir de forma autoregresiva: usar $w_{n+1}$ como input en el paso $n+1$, computar $h^{(n+1)}$ y generar $w_{n+2}$, etc.
#### 2. Resumen Intermedio del Material
> El material resume:
> - limitación de feed-forward: inputs de longitud fija y dificultad para dependencias largas
> - ventaja de RNN: secuencias de longitud variable procesadas incrementalmente
> - conexión recurrente: $h^{(t)}$ depende de $h^{(t-1)}$, lo que implementa “memoria”
> - el número de parámetros es constante respecto a la longitud de la secuencia.

### VI. Variantes: LSTM
#### 1. Motivación para LSTM
> El material explica que en un RNN básico el estado oculto tiene tamaño fijo $h^{(t)}\in\mathbb{R}^{d_h}$, independientemente de cuántos tokens se hayan procesado.  
> A medida que $t$ crece, $h^{(t)}$ debe “comprimir” más información en el mismo espacio, y el contexto pasado se comprime cada vez más.  
> Aunque los RNNs pueden (en teoría) capturar dependencias largas, son difíciles de entrenar para ello; por eso se introducen unidades más complejas.  
> Idea central: los LSTMs controlan explícitamente el flujo de información (qué se recuerda y qué se olvida) para capturar mejor dependencias de largo alcance.
#### 2. Estados en LSTM: Celda y Estado Oculto
> En un LSTM, en el time-step $t$ hay:
> - un estado oculto $h^{(t)}$
> - una celda de memoria $c^{(t)}$  
>     Ambos son vectores de la misma longitud $n$.  
>     Interpretación del material:
> - $c^{(t)}$: memoria de largo plazo (“lo que el modelo recuerda”)
> - $h^{(t)}$: “vista filtrada” de $c^{(t)}$ (“lo que el modelo usa ahora” y el vector que se usa para predecir la siguiente palabra).
#### 3. Operaciones Conceptuales: Borrar, Escribir y Leer
> El material presenta la celda LSTM como un “blackboard” y dice que el LSTM puede:
> - borrar información de $c^{(t)}$ (olvidar)
> - escribir nueva información relevante en $c^{(t)}$
> - leer la parte relevante (a través de $h^{(t)}$).

### VII. LSTM: Forget Gate
#### 1. Mecanismo y Actualización Parcial
> El forget gate controla qué información en la celda $c^{(t)}$ se conserva o se descarta, de forma elemento a elemento.  
> En cada paso produce un vector $f^{(t)}\in[0,1]^n$ con la misma dimensionalidad que $c^{(t)}$.  
> La actualización parcial descrita es:  $$c^{(t)}=f^{(t)}\odot c^{(t-1)}$$Interpretación por coordenada: $f^{(t)}_i\approx 1$ conserva, $f^{(t)}_i\approx 0$ borra, valores intermedios conservan parcialmente.
#### 2. Ecuación del Forget Gate
> El material da la ecuación con una capa sigmoide y parámetros propios:  $$f^{(t)}=\sigma\left(x^{(t)}W_f+h^{(t-1)}U_f+b_f\right)\in[0,1]^n$$(En otras diapositivas, el material reescribe estas ecuaciones usando $h^{(t-1)}W_f+x^{(t)}U_f$, manteniendo la idea: un término para el input y otro para el estado previo, con parámetros propios).

### VIII. LSTM: Input Gate y Escritura en Memoria
#### 1. Mecanismo: Candidato y Puerta de Entrada
> El material define primero un contenido candidato $\tilde{c}^{(t)}\in[-1,1]^n$ que representa nueva información que podría escribirse.  
> Luego la input gate produce $i^{(t)}\in[0,1]^n$ que controla cuánto se escribe, elemento a elemento.  
> La escritura se expresa como $i^{(t)}\odot \tilde{c}^{(t)}$.
#### 2. Ecuaciones del Candidato y del Input Gate
> El candidato se calcula con $\tanh$ y parámetros propios:  $$\tilde{c}^{(t)}=\tanh\left(x^{(t)}W_c+h^{(t-1)}U_c+b_c\right)$$La puerta de entrada:  $$i^{(t)}=\sigma\left(x^{(t)}W_i+h^{(t-1)}U_i+b_i\right)\in[0,1]^n$$
#### 3. Actualización Completa de la Celda
> El material combina olvido y escritura en:  $$c^{(t)}=f^{(t)}\odot c^{(t-1)}+i^{(t)}\odot \tilde{c}^{(t)}$$

### IX. LSTM: Output Gate y Lectura a Estado Oculto
#### 1. Mecanismo de Lectura
> Tras actualizar $c^{(t)}$, el LSTM produce el nuevo estado oculto $h^{(t)}$.  
> El material explica que $c^{(t)}$ puede contener más información de la necesaria “ahora”, y que la output gate selecciona una vista específica del time-step para predecir.
#### 2. Ecuación del Output Gate y del Estado Oculto
> La output gate:  $$o^{(t)}=\sigma\left(x^{(t)}W_o+h^{(t-1)}U_o+b_o\right)\in[0,1]^n$$El estado oculto se obtiene filtrando $\tanh(c^{(t)})$:  
> $$h^{(t)}=o^{(t)}\odot\tanh\left(c^{(t)}\right)$$Interpretación por coordenada: $o^{(t)}_i\approx 1$ expone, $o^{(t)}_i\approx 0$ oculta.

### X. Ecuaciones LSTM: Foto Completa y Notación Alternativa
#### 1. Foto Completa (Según el Material)
> El material resume el LSTM en el paso $t$ con:  $$f^{(t)}=\sigma\left(h^{(t-1)}W_f+x^{(t)}U_f+b_f\right),$$$$i^{(t)}=\sigma\left(h^{(t-1)}W_i+x^{(t)}U_i+b_i\right),$$$$o^{(t)}=\sigma\left(h^{(t-1)}W_o+x^{(t)}U_o+b_o\right),$$$$\tilde{c}^{(t)}=\tanh\left(h^{(t-1)}W_c+x^{(t)}U_c+b_c\right),$$$$c^{(t)}=f^{(t)}\odot c^{(t-1)}+i^{(t)}\odot\tilde{c}^{(t)},$$$$h^{(t)}=o^{(t)}\odot\tanh\left(c^{(t)}\right).$$
#### 2. Forma con Concatenación de Entradas
> El material indica que es común escribirlo con una sola matriz por puerta, concatenando $h^{(t-1)}$ y $x^{(t)}$:  $$\sigma\left(h^{(t-1)}W+x^{(t)}U+b\right)=\sigma!\left([h^{(t-1)},x^{(t)}],[W;U]+b\right)$$Usando $W$ para la matriz concatenada, las ecuaciones se reescriben como:  $$f^{(t)}=\sigma\left([h^{(t-1)},x^{(t)}]W_f+b_f\right),$$$$i^{(t)}=\sigma\left([h^{(t-1)},x^{(t)}]W_i+b_i\right),$$$$o^{(t)}=\sigma\left([h^{(t-1)},x^{(t)}]W_o+b_o\right),$$$$\tilde{c}^{(t)}=\tanh\left([h^{(t-1)},x^{(t)}]W_c+b_c\right),$$$$c^{(t)}=f^{(t)}\odot c^{(t-1)}+i^{(t)}\odot\tilde{c}^{(t)},$$$$h^{(t)}=o^{(t)}\odot\tanh\left(c^{(t)}\right).$$
#### 3. Nota de Convención (Filas vs Columnas)
> El material avisa que en el ejemplo paso a paso usa convención de vectores columna para $x^{(t)}$, $c^{(t)}$ y $h^{(t)}$, mientras que las ecuaciones del tema usan convención de fila.  
> Al leer el diagrama, aparece la equivalencia por transposición:  $$x^{(t)}W;\leftrightarrow;W^\top\left(x^{(t)}\right)^\top.$$

### XI. Resumen Final del Tema
#### 1. Ideas Clave
> - Un RNN procesa secuencias de longitud variable manteniendo un estado $h^{(t)}$ que se actualiza con $x^{(t)}$ y $h^{(t-1)}$, reutilizando los mismos parámetros en todos los time-steps.
> - Un RNN-LM produce $P(\cdot\mid w_1,\dots,w_t)$ con una salida $\mathrm{softmax}$ sobre el vocabulario.
> - Ventajas del RNN-LM: contexto de longitud arbitraria sin aumentar el número de parámetros con la longitud de la entrada; desventajas: cómputo recurrente lento y dificultad práctica para acceder a dependencias muy largas.
> - Un LSTM introduce memoria $c^{(t)}$ y puertas $f^{(t)}$, $i^{(t)}$, $o^{(t)}$ para controlar qué se olvida, qué se escribe y qué se lee, mejorando la capacidad de capturar dependencias de largo alcance.

Los apuntes continúan en [[Tema 6 - ]]