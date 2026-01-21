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
