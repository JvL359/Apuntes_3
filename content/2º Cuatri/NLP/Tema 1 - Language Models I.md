### I. 
#### 1.
> rellenar hasta la diapo 19

#### n. Generación AutoRegresiva
> Con la entrada de un prompt a rellenar/continuar, a partir de unas predicciones con sus probabilidades asociadas, elige la palabra más probable a continuación, y así sucesivamente. Se detendrá cuando llegue al máximo de tokens, o al devolver un End Of Sequence `EoS` token (se calla xq ya ha terminado y no se va a enrollar más). 
#### m. Definiciones
> - *`Vocabulario:`* set fijo y finito de símbolos (palabras o tokens).
> - *`Secuencia de Palabras:`* secuencia finita de palabras del vocabulario.
> - *`Frases/Oraciones:`* Son secuencias de palabras con un token `BoS` al inicio y otro `EoS` al final.
#### Probabilidad de una Oración
> Como los generadores predicen palabra a palabra, las probabilidades se asignan a cada palabra, y de ahí se calcula la probabilidad total de la frase. Estas probabilidades se calculan con la regla de la cadena (foto diapo 39).

![[Pasted image 20260121163000.png]]
### II. Estimadores de Probabilidades
#### 1. N-Gram Model
> Se predice en base a frecuencias relativas: cuántas veces aparece la palabra `R` después del contexto (secuencia de palabras) `S` y se calcula la probabilidad como $P(R \mid S) = \frac{P(R \cap S)}{P(S)}$
##### 1.1. Estimar `P(next word)` basado en conteo
> diapo 64
> Ejemplo: 
![[Pasted image 20260121164646.png]]
##### 1.2. Problema del Modelo
> Si se introduce un prompt que no está contenido en el contexto del modelo, hay una probabilidad 0 de ocurrencia.
##### 1.3. Solución al Zero-Count
> Descartar las primeras `m` palabras del prompt hasta que haya una coincidencia. Esto se llama `Supuesto Markoviano` que se queda con las `n-1` últimas palabras para predecir con un `N-grama`. 
> Por ejemplo en un `Tri-grama` si se quiere predecir `P(dream | a kid who had a)` se toma la aproximación `P(dream | had a)` haciendo `Count(had a dream) / Count (had a __)`.

rellenar 89-
##### 1.5. Limitaciones del Modelo
> - Zero-Count: reducir el input (`Backoff`), o suavizarlo (`Smoothing`) añadiendo 1 al count.
> - Dependencias a largo plazo: El modelo va perdiendo 'memoria' y  cambia totalmente de tema.
> - Generalización limitada: Sus conocimientos son independientes, dando problemas con sinónimos o palabras pertenecientes a la misma familia de palabras pero que no aparecen.

