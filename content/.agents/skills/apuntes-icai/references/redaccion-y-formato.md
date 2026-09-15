# Redacción y formato

## Objetivo editorial

Cubre todo el contenido relevante con explicación suficiente para comprenderlo y estudiarlo. Sintetiza repeticiones entre fuentes, pero no suprimas matices, condiciones, excepciones, demostraciones, procedimientos ni interpretaciones útiles.

No impongas una longitud proporcional al número de diapositivas. Deja que la dificultad y densidad del tema determinen la extensión.

Ante una fórmula o concepto abstracto, combina hasta cuatro capas cuando aporten comprensión:

1. Presentación fiel del concepto o fórmula.
2. Explicación intuitiva y significado de sus elementos.
3. Desarrollo completo de los pasos intermedios relevantes.
4. Ejemplo breve y original para afianzar la idea.

El ejemplo del punto 4 no puede resolver un ejercicio evaluable ni sustituir una solución ausente en los materiales.

## Perfil del tema

Elige el perfil internamente; no lo declares en la nota.

### Teórico

Prioriza definiciones precisas, intuición, hipótesis, propiedades, fórmulas, derivaciones, relaciones entre conceptos y consecuencias. Menciona prerrequisitos solo de forma breve cuando sean necesarios para seguir la explicación.

### Práctico

Organiza el contenido como un procedimiento comprensible: propósito, preparación, pasos, código o método e interpretación. Explica por qué se ejecuta cada bloque y qué debe observarse en el resultado.

### Mixto

Integra la teoría inmediatamente antes de la aplicación que la necesita. No separes artificialmente el tema en una mitad teórica y otra práctica si intercalarlas mejora la comprensión.

## Idioma y terminología

- Redacta siempre las explicaciones en español.
- Conserva en inglés los nombres técnicos empleados por la asignatura y explícalos en español.
- Si los materiales están en inglés, escribe en inglés el nombre del archivo y los títulos de bloques, secciones y subsecciones.
- Si los materiales están en español, escribe esos títulos en español.
- En materiales mixtos, respeta el idioma establecido por el nombre del archivo de destino; si no basta, usa el idioma dominante en los materiales.
- Conserva siglas, capitalización y terminología técnica de forma consistente.

## Tono

Escribe de manera directa, práctica y académicamente clara.

- Puedes usar con naturalidad la primera persona del plural: «vemos», «usamos», «comprobamos».
- Puedes usar marcadores pedagógicos como «idea clave», «en la práctica», «lo importante» o «en resumen» cuando orienten realmente al lector.
- Usa con moderación advertencias breves y metáforas intuitivas como «ojo», «borra la tendencia» o «mirar al futuro»; acompáñalas de una explicación precisa cuando puedan inducir una interpretación literal incorrecta.
- Usa la segunda persona solo de forma excepcional.
- No uses humor, incorrecciones deliberadas ni expresiones como «menos mejor y más peor».
- Evita relleno, reiteraciones, frases sobre el proceso de redacción y comentarios dirigidos al profesor o al autor del material.

## Estructura

No añadas un título H1 dentro de la nota. Comienza el contenido tras el frontmatter con esta jerarquía:

```markdown
### I. Block
#### 1. Section
##### 1.1. Subsection
###### 1.1.1. Additional Level
```

- Numera los bloques con romanos y las divisiones internas con arábigos.
- Mantén la numeración continua y coherente.
- Usa el sexto nivel solo cuando evite mezclar contenidos distintos dentro de una subsección.
- No crees secciones vacías ni subdivisiones con un único fragmento trivial.
- Reorganiza el orden de las diapositivas cuando una estructura conceptual o procedimental distinta facilite el estudio, sin alterar las dependencias lógicas.

La última sección es siempre `Resumen Final` si los títulos están en español o `Final Summary` si están en inglés. Resume relaciones, decisiones y resultados esenciales; no copies párrafos anteriores ni introduzcas contenido nuevo.

## Convenciones Markdown de Obsidian

- Usa `>` para los párrafos explicativos, siguiendo el patrón de los apuntes de referencia. Mantén código, tablas y encabezados fuera del bloque de cita.
- Reserva la **negrita** para conceptos, nombres de métodos, propiedades decisivas y contrastes importantes. No pongas frases o párrafos completos en negrita.
- Usa *cursiva* solo para énfasis breve o extranjerismos cuando resulte natural. No combines negrita y cursiva sin una razón semántica.
- Usa código inline para `funciones()`, `clases`, variables, argumentos, comandos, librerías, rutas, extensiones y valores literales propios del código.
- Usa listas para enumeraciones paralelas, condiciones, pasos o comparaciones. Evita listas de un solo elemento y anidamientos innecesarios.
- Usa tablas únicamente cuando hagan más clara una comparación repetida, una correspondencia exacta o una matriz de decisión. No las uses para maquetar prosa.
- Conserva los wikilinks de Obsidian cuando sean útiles y apunta siempre a archivos existentes.

## Callouts

Emplea callouts de forma excepcional, no como formato general de cada definición.

- Las etiquetas sobre contenido examinable, complementario o práctico solo pueden aparecer si los materiales las indican expresamente.
- Puede haber como máximo dos callouts de esas categorías por tema.
- Los callouts de corrección no cuentan para ese límite.
- Los callouts de nota, ejemplo o advertencia solo se justifican si separan información especialmente útil que se perdería dentro del flujo normal.

## Matemáticas

- Reproduce estrictamente la notación de los materiales. No cambies símbolos, índices, orientación de vectores, nombres de variables ni convenciones por preferencia propia.
- Usa `$...$` para variables y expresiones breves integradas en una frase.
- Usa `$$...$$` para fórmulas largas, sistemas, derivaciones y desarrollos de varias líneas.
- Transcribe a LaTeX las fórmulas que aparezcan como imágenes; no las sustituyas por una captura salvo que el componente visual completo aporte información adicional.
- Define símbolos y condiciones cuando la fuente lo permita y no estén claros por el contexto.
- Completa pasos intermedios relevantes sin cambiar el método empleado por el profesor.
- Verifica signos, índices, dimensiones, dominios, hipótesis y consistencia de símbolos.
- No presentes como segura una reconstrucción dudosa: deja un `TODO` breve.

## Código

El código debe ser pedagógico, pero no simplificado.

- Conserva el lenguaje, algoritmo, librerías, estructuras y funcionalidad enseñados.
- No suprimas partes funcionales para acortar el ejemplo.
- Separa un bloque largo en unidades lógicas con una explicación previa para cada una.
- Añade imports, preparación y configuración claramente necesarios cuando el material los omita.
- Añade comentarios que expliquen decisiones o pasos relevantes; evita comentar cada línea obvia.
- Después del bloque, interpreta el resultado esperado o explica qué debe inspeccionarse si esa información aparece o se deduce con seguridad.
- Corrige errores manifiestos de sintaxis o lógica bajo la regla general de correcciones. No rediseñes la solución ni cambies de biblioteca por preferencia.
- No ejecutes el código salvo petición expresa. No inventes outputs, métricas ni resultados de ejecución.
- Usa fences con el identificador correcto, por ejemplo `python`, `r`, `matlab`, `sql` o `bash`.

Al procesar notebooks, respeta el orden lógico de las celdas y combina el Markdown, el código y los outputs que aporten al tema. Omite estados de ejecución, widgets y salidas accidentales. Al procesar scripts, reconstruye el propósito y las dependencias necesarias sin cambiar el lenguaje ni ejecutar el archivo.

## Ejercicios

- Puedes reproducir enunciados y soluciones presentes en las fuentes, reorganizándolos para hacerlos legibles.
- No completes una solución parcial si eso equivale a resolver el ejercicio por cuenta propia.
- Un ejemplo ilustrativo creado para explicar teoría debe ser mínimo, inequívocamente pedagógico y distinto de los ejercicios evaluables del material.
