---
estado: pendiente de revisión
---

### I. Numerabilidad de Conjuntos

#### 1. Definiciones básicas

> Sea $X$ un conjunto. Diremos que es **finito** si $X=\varnothing$ o existe una biyección entre $X$ y $\mathbb{Z}_{n_0}=\{1,2,\ldots,n_0\}$ para algún $n_0\in\mathbb{N}$. Es **infinito numerable** si existe una biyección entre $X$ y $\mathbb{N}$; en ese caso puede escribirse como $X=\{x_1,x_2,\ldots\}$.

> Un conjunto es **numerable** si es finito o infinito numerable. La numerabilidad se preserva por biyección: si $X$ es numerable y existe una biyección entre $X$ e $Y$, entonces $Y$ también es numerable.

#### 2. Racionales, reales e irracionales

> El conjunto $\mathbb{Q}$ de los racionales es numerable. Se descompone como

$$
\mathbb{Q}=\mathbb{Q}^+\cup\mathbb{Q}^-\cup\{0\},
$$

> donde las fracciones positivas y negativas se consideran en forma irreducible. Para enumerar $\mathbb{Q}^+$ se ordenan por suma creciente $p+q$ y, dentro de cada suma, por $p$ creciente. El mismo argumento sirve para $\mathbb{Q}^-$; después se intercala todo el conjunto con los enteros mediante una biyección con $\mathbb{Z}$.

> En cambio, $\mathbb{R}$ no es numerable. Basta probarlo para $[0,1]$: si pudiéramos listar $[0,1]=\{a_1,a_2,\ldots\}$, construiríamos un número $\widetilde{x}=0.\widetilde d_1\widetilde d_2\ldots$ cuyo dígito $\widetilde d_j$ sea $1$ si el $j$-ésimo dígito de $a_j$ no es $1$, y $2$ en caso contrario. Entonces $\widetilde{x}\ne a_j$ para todo $j$, contradiciendo que la lista fuese completa.

> Como $\mathbb{R}=\mathbb{Q}\cup I$, donde $I$ es el conjunto de los irracionales, $I$ tampoco puede ser numerable. Por tanto, en la recta real hay más irracionales que racionales en el sentido de cardinalidad.

#### 3. Operaciones con conjuntos numerables

> Usaremos repetidamente las siguientes propiedades:

- Una unión finita o infinito numerable de conjuntos numerables es numerable:

$$
X=\bigcup_{i=1}^{\infty}X_i.
$$

- El producto cartesiano de un número finito de conjuntos numerables es numerable.
- Si $S$ es numerable y $T\subset S$, entonces $T$ es numerable.
- Si $S$ no es numerable y $S\subset T$, entonces $T$ no es numerable.

> Estas propiedades permiten tratar, por ejemplo, sucesiones racionales con soporte finito, polinomios con coeficientes racionales y familias de matrices mediante uniones o productos de conjuntos conocidos.

### II. Desigualdades Fundamentales

#### 1. Exponentes conjugados y desigualdad de Young

> Los números $p,q>1$ son **exponentes conjugados** si

$$
\frac{1}{p}+\frac{1}{q}=1.
$$

> La desigualdad de **Young** establece que, para $\alpha,\beta\ge0$,

$$
\alpha\beta\le\frac{\alpha^p}{p}+\frac{\beta^q}{q}.
$$

> Es una consecuencia de la convexidad. Si $f$ es convexa y $\alpha,\beta\ge0$ con $\alpha+\beta=1$, entonces

$$
f(\alpha x+\beta y)\le\alpha f(x)+\beta f(y).
$$

> Aplicando esta relación a $f(x)=e^x$, con pesos $1/p$ y $1/q$, se obtiene Young. Para $p=q=2$ queda $\alpha\beta\le(\alpha^2+\beta^2)/2$. Una forma con parámetro útil es, para $\varepsilon>0$,

$$
\alpha\beta\le\frac{\alpha^p\varepsilon^p}{p}+\frac{\beta^q}{q\varepsilon^q}.
$$

#### 2. Desigualdad de Hölder

> Si $p,q>1$ son conjugados y las sucesiones $\{x_i\}$ e $\{y_i\}$ cumplen

$$
\sum_{i=1}^{\infty}|x_i|^p<\infty,
\qquad
\sum_{i=1}^{\infty}|y_i|^q<\infty,
$$

> entonces

$$
\sum_{i=1}^{\infty}|x_iy_i|
\le
\left(\sum_{i=1}^{\infty}|x_i|^p\right)^{1/p}
\left(\sum_{i=1}^{\infty}|y_i|^q\right)^{1/q}.
$$

> La demostración normaliza ambas sucesiones para que las sumas de potencias sean $1$, aplica Young término a término y desnormaliza al final. Para funciones $f,g:[a,b]\to\mathbb{R}$ con las potencias integrables correspondientes,

$$
\int_a^b|f(x)g(x)|\,dx
\le
\left(\int_a^b|f(x)|^p\,dx\right)^{1/p}
\left(\int_a^b|g(x)|^q\,dx\right)^{1/q}.
$$

#### 3. Cauchy-Schwarz y Minkowski

> **Cauchy-Schwarz** es el caso particular de Hölder con $p=q=2$:

$$
\sum_{i=1}^{\infty}|x_iy_i|
\le
\left(\sum_{i=1}^{\infty}|x_i|^2\right)^{1/2}
\left(\sum_{i=1}^{\infty}|y_i|^2\right)^{1/2}.
$$

> Su versión integral sustituye las sumas por integrales sobre $[a,b]$.

> La desigualdad de **Minkowski** es la desigualdad triangular para la norma $p$. Si $p\ge1$ y las sucesiones son $p$-sumables,

$$
\left(\sum_{i=1}^{\infty}|x_i+y_i|^p\right)^{1/p}
\le
\left(\sum_{i=1}^{\infty}|x_i|^p\right)^{1/p}
+
\left(\sum_{i=1}^{\infty}|y_i|^p\right)^{1/p}.
$$

> Para $p=1$ se reduce a $|x_i+y_i|\le|x_i|+|y_i|$. Para $p>1$, se acota $\sum|x_i+y_i|^p$ separando los términos con $|x_i|$ e $|y_i|$ y aplicando Hölder con el exponente conjugado de $p$. Para funciones se obtiene análogamente

$$
\left(\int_a^b|f(x)+g(x)|^p\,dx\right)^{1/p}
\le
\left(\int_a^b|f(x)|^p\,dx\right)^{1/p}
+
\left(\int_a^b|g(x)|^p\,dx\right)^{1/p}.
$$

#### 4. Desigualdad de Jensen

> Para $1\le p\le q<\infty$ y una sucesión con norma $p$ finita, se cumple la relación entre normas

$$
\left(\sum_{i=1}^{\infty}|x_i|^q\right)^{1/q}
\le
\left(\sum_{i=1}^{\infty}|x_i|^p\right)^{1/p}.
$$

### III. Espacios de Sucesiones y Funciones

#### 1. Espacios de sucesiones

> Para $1\le p<\infty$, el espacio $\ell^p$ de sucesiones $p$-sumables es

$$
\ell^p=\left\{x=\{x_i\}_{i=1}^{\infty}:\sum_{i=1}^{\infty}|x_i|^p<\infty\right\}.
$$

> El caso $p=2$ recibe el nombre de sucesiones de cuadrado sumable. Para $p=\infty$,

$$
\ell^\infty=\left\{x=\{x_i\}_{i=1}^{\infty}:\sup_i|x_i|<\infty\right\}.
$$

> Si $x\in\ell^p$ con $p>1$, entonces $x_i\to0$. Si $x\in\ell^\infty$, existe $K>0$ tal que $|x_i|\le K$ para todo $i$. Para $x=\{1/n^\alpha\}_{n=1}^{\infty}$, con $\alpha>0$, se tiene $x\in\ell^\infty$ y $x\in\ell^p$ si y solo si $\alpha>1/p$.

> También usamos:

$$
\begin{aligned}
c&=\{x\in\ell^\infty:x\text{ es convergente}\},\\
c_0&=\{x\in c:x\text{ converge a }0\},\\
c_{00}&=\{x:\text{tiene un número finito de términos no nulos}\}.
\end{aligned}
$$

#### 2. Espacios funcionales

> Para un intervalo $I$,

$$
C(I)=\{f:I\to\mathbb{R}:f\text{ es continua en }I\},
$$

$$
C^k(I)=\{f:I\to\mathbb{R}:f,f',f'',\ldots,f^{(k)}\text{ son continuas en }I\}.
$$

> Los espacios $L^p(I)$, con $1\le p<\infty$, recogen las funciones $p$-integrables:

$$
L^p(I)=\left\{f:I\to\mathbb{R}:\int_I|f(x)|^p\,dx<\infty\right\}.
$$

> Para $p=\infty$ se consideran las funciones acotadas:

$$
L^\infty(I)=\left\{f:I\to\mathbb{R}:\sup_{x\in I}|f(x)|<\infty\right\}.
$$

### IV. Resultados a Recordar

#### 1. Cotas, supremo e ínfimo

> Sea $D\subset\mathbb{R}$ no vacío. Un número $M$ es una **cota superior** si $x\le M$ para todo $x\in D$; un número $m$ es una **cota inferior** si $x\ge m$ para todo $x\in D$. El conjunto es acotado si lo está superior e inferiormente.

> Si $D$ está acotado superiormente, $\sup(D)$ es la menor de sus cotas superiores; si además pertenece a $D$, se denomina $\max(D)$. Si $D$ está acotado inferiormente, $\inf(D)$ es la mayor de sus cotas inferiores; si pertenece a $D$, es $\min(D)$.

> El axioma del supremo e ínfimo garantiza su existencia para conjuntos no vacíos acotados en la dirección correspondiente. En particular, $\sup(D)\ge x$ para todo $x\in D$, y toda cota superior $M$ satisface $M\ge\sup(D)$; las afirmaciones duales valen para el ínfimo.

#### 2. Series numéricas

> Una condición necesaria para que $\sum_{n=1}^{\infty}a_n$ converja es

$$
\lim_{n\to\infty}a_n=0.
$$

> La serie geométrica cumple

$$
\sum_{n=k}^{\infty}q^n<\infty\iff|q|<1,
\qquad
\sum_{n=k}^{\infty}q^n=\frac{q^k}{1-q}.
$$

> La serie armónica generalizada satisface

$$
\sum_{n=1}^{\infty}\frac{1}{n^\alpha}<\infty\iff\alpha>1.
$$

#### 3. Integrales

> Sea $D\subset\mathbb{R}^N$, $\mu$ una medida y $f:D\to\mathbb{R}$ integrable. Se cumple

$$
\int_D1\,d\mu=\mu(D),
\qquad
\mu(D)=0\implies\int_Df\,d\mu=0.
$$

> Si $m\le f(x)\le M$ para todo $x\in D$, entonces

$$
m\mu(D)\le\int_Df\,d\mu\le M\mu(D).
$$

> Además, si $f$ es integrable, $|f|$ también lo es y

$$
\int_Df(x)\,d\mu\le\int_D|f(x)|\,d\mu.
$$

### V. Resumen Final

> Los conjuntos numerables se relacionan con $\mathbb{N}$ mediante biyecciones y son estables bajo uniones numerables, productos finitos y subconjuntos. Los racionales son numerables, pero los reales y los irracionales no lo son por el argumento diagonal.

> Young, Hölder, Cauchy-Schwarz y Minkowski proporcionan las cotas que estructuran las normas en $\ell^p$ y $L^p$. Estos espacios, junto con las nociones de supremo, series e integrales, forman el lenguaje básico para los resultados posteriores de la asignatura.
