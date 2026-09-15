# Actualización y revisión

## Principio de preservación

Lee la nota completa antes de editarla. Conserva su información válida, estructura útil, enlaces e imágenes. Limita el cambio a lo pedido y a inconsistencias del mismo tema que sea necesario corregir para integrar el material.

No uses una actualización como oportunidad para reescribir toda la nota. No uses una revisión para imponer un estilo uniforme a costa de contenido correcto o matices útiles.

## Modo actualizar

1. Construye un esquema del contenido ya presente.
2. Compara semánticamente cada material nuevo o corregido con ese esquema.
3. Identifica adiciones, sustituciones y pequeñas correcciones; ignora cambios puramente visuales del PDF que no alteren el contenido.
4. Integra cada novedad en su lugar lógico. No vuelques todo al final de la nota.
5. Ajusta numeración y transiciones solo donde sea necesario.
6. Revisa si una imagen existente sigue siendo válida antes de sustituirla.
7. Si hubo al menos un cambio real, establece `estado: actualizado`.

Si no existe ninguna diferencia sustantiva, termina sin escribir el archivo, sin tocar el frontmatter y sin regenerar imágenes.

## Modo revisar

Aplica únicamente el alcance pedido por el usuario. Puede incluir:

- Completar cobertura frente a los materiales indicados.
- Resolver `TODO` cuando ya haya información fiable.
- Corregir errores de contenido, Markdown, LaTeX, código, numeración o enlaces.
- Reorganizar secciones para mejorar dependencias y continuidad.
- Reducir repeticiones sin perder información.
- Ajustar el equilibrio entre explicación, fórmulas, código e imágenes.

Tras la auditoría, establece `estado: completado`. Si queda algún `TODO` porque la información sigue siendo insuficiente, mantenlo y destácalo en el informe final.

## Frontmatter

Si la nota no tiene frontmatter, añádelo al comienzo. Si ya existe:

- Modifica únicamente la propiedad `estado`.
- Conserva el orden y valor de las demás propiedades.
- No dupliques delimitadores `---` ni la clave `estado`.

## Idempotencia

Antes de aplicar un cambio, comprueba que no esté ya representado con otras palabras. No dupliques definiciones, ejemplos, fórmulas, fragmentos de código ni conclusiones.

Al terminar una actualización, razona cómo se comportaría una segunda ejecución inmediata con las mismas entradas: debería detectar cobertura completa y producir cero cambios.
