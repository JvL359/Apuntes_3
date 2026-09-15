# Auditoría final

Realiza esta segunda pasada después de redactar y antes de comunicar la finalización. Corrige directamente los fallos seguros que encuentres y vuelve a comprobar las partes afectadas.

## 1. Cobertura y fidelidad

- Contrasta el mapa de cobertura con todos los materiales y páginas indicados.
- Comprueba que ningún apartado relevante, condición, excepción, demostración, procedimiento o interpretación haya quedado fuera.
- Confirma que las repeticiones entre fuentes se hayan fusionado sin perder matices.
- Busca afirmaciones, ejemplos, resultados o conclusiones no respaldados por los materiales o por una aclaración externa de alta confianza.
- Confirma que no aparezcan citas ni referencias visibles, salvo en callouts de corrección manifiesta.
- Verifica que una contradicción no resuelta haya provocado una consulta al usuario y no una elección silenciosa.

## 2. Comprensión

- Comprueba que las ideas abstractas tengan la combinación necesaria de formulación, intuición, desarrollo y ejemplo.
- Verifica que los prerrequisitos solo se mencionen cuando ayuden.
- Elimina relleno y repeticiones sin reducir la cobertura.
- Confirma que el resumen final sintetice y no introduzca información nueva.

## 3. Matemáticas y código

- Compara la notación con la fuente: símbolos, índices, signos, dimensiones e hipótesis deben coincidir.
- Comprueba delimitadores `$...$` y `$$...$$`, comandos LaTeX y desarrollos intermedios.
- Revisa que el código conserve lenguaje, algoritmo y funcionalidad, esté dividido de forma pedagógica y tenga fences correctos.
- No afirmes que el código funciona o fue probado si no se ejecutó.
- Comprueba que no se haya inventado una solución de ejercicio ni un output.

## 4. Markdown y estilo

- Verifica el frontmatter y el valor de `estado` correspondiente al modo.
- Comprueba la jerarquía `###` → `####` → `#####` → `######` y toda la numeración.
- Revisa negrita, cursiva, código inline, listas, tablas, callouts y blockquotes según la guía.
- Confirma que los títulos estén en el idioma de los materiales y las explicaciones en español.
- Uniforma términos técnicos y siglas.
- Corrige ortografía, concordancia y puntuación.
- Verifica que no haya bloques de código, tablas, embeds o fórmulas sin cerrar.

## 5. Imágenes y enlaces

- Abre o comprueba cada imagen nueva y confirma que el recorte sea legible, fiel y relevante.
- Confirma que cada imagen esté dentro de `<Asignatura>/imgs/`, tenga un embed válido y una explicación próxima.
- Comprueba que no haya figuras duplicadas ni se exceda el límite de densidad.
- Verifica que todos los wikilinks y rutas incorporados existan.

## 6. Alcance e idempotencia

- Inspecciona el diff final cuando esté disponible.
- Confirma que solo hayan cambiado la nota solicitada, las imágenes estrictamente necesarias y, si faltaba, la carpeta `imgs/`.
- Confirma que `_materiales/`, el índice y otros temas sigan intactos.
- En modo `actualizar`, si no había novedades, el diff debe estar vacío.
- Evalúa una repetición inmediata con las mismas entradas: no debería añadir, reordenar ni reformular nada.
- No prepares commits ni alteres el área de staging.

## 7. Informe en el chat

Incluye solo:

- Modo ejecutado y nota afectada.
- Cantidad de materiales y páginas procesadas.
- Imágenes añadidas o reutilizadas.
- Correcciones manifiestas y `TODO` pendientes.
- Confirmación breve de la auditoría.

No guardes el informe. Su máximo es `300 × ceil(páginas / 50)` palabras, con un primer tramo de hasta 50 páginas. Si solo existen fuentes no paginadas, el máximo es 300 palabras. Intenta quedar muy por debajo del máximo.
