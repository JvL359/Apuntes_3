---
name: apuntes-icai
description: Crea, actualiza o revisa, tema a tema, apuntes de Obsidian para asignaturas de ICAI a partir de los materiales docentes indicados por el usuario. Úsala solo cuando el usuario invoque explícitamente $apuntes-icai y proporcione la asignatura, los materiales ordenados y la nota de destino.
metadata:
  short-description: Apuntes de ICAI desde materiales docentes
---

# Apuntes ICAI

Transforma materiales docentes en una única nota de estudio completa por tema. Adapta el desarrollo a asignaturas teóricas, prácticas o mixtas sin perder contenido relevante ni convertir las diapositivas en una transcripción literal.

## Entrada obligatoria

Antes de trabajar, identifica:

- El modo: `crear`, `actualizar` o `revisar`. Infiérelo solo si la petición no deja dudas.
- La carpeta de la asignatura, que debe contener `_materiales/`.
- La subcarpeta del tema dentro de `_materiales/`.
- La lista de materiales que deben usarse y su orden de prioridad.
- El archivo Markdown de destino, situado en la raíz de la asignatura y correspondiente a un solo tema. Conserva siempre la ruta indicada por el usuario. Si te ha encargado elegir el nombre, usa `Tema X - Título.md`, tomando el título de las diapositivas o el tema común de sus partes, y crea el archivo si la petición lo autoriza.

Comprueba que las rutas y archivos existen. No proceses otros materiales por iniciativa propia. Si falta un dato obligatorio o el orden de las fuentes es ambiguo, pide únicamente la información imprescindible antes de escribir.

## Referencias de trabajo

- Lee [redaccion-y-formato.md](references/redaccion-y-formato.md) en toda ejecución.
- Si hay PDF, diapositivas escaneadas o imágenes, lee [materiales-pdf-e-imagenes.md](references/materiales-pdf-e-imagenes.md).
- Para ejecutar preparación, recortes o comprobaciones mecánicas, lee [herramientas.md](references/herramientas.md). Reutiliza los scripts incluidos en vez de reescribir su lógica en cada tema.
- Si hay algoritmos o posibles errores docentes, lee [algoritmos-y-errores.md](references/algoritmos-y-errores.md).
- En los modos `actualizar` y `revisar`, lee [actualizacion-y-revision.md](references/actualizacion-y-revision.md).
- Antes de terminar cualquier modo, lee y aplica [auditoria.md](references/auditoria.md).

Las reglas anteriores sintetizan el estilo de los apuntes de FC y de los archivos `Resumen Tema *.md` de DpL. Consulta esos apuntes originales solo como último recurso cuando las referencias de esta skill no resuelvan una decisión de presentación. No copies peculiaridades accidentales, errores ni convenciones propias de una sola asignatura.

## Flujo

1. Inspecciona el destino y los materiales en el orden indicado. Crea un snapshot temporal de la asignatura antes de editar con `audit_notes.py snapshot`.
2. Para PDF, ejecuta `prepare_pdf.py prepare` una vez por lista ordenada de fuentes. Revisa todas las hojas de miniaturas y abre a tamaño legible las páginas que lo requieran. Completa el mapa temporal `coverage.json` para evitar relecturas; no lo guardes en el repositorio.
3. Determina si el tema es predominantemente teórico, práctico o mixto.
4. Diseña una estructura lógica que cubra los materiales sin seguir necesariamente una división diapositiva por diapositiva.
5. Crea o integra el contenido según el modo. Para imágenes seleccionadas, usa `crop_figures.py`, inspecciona la vista previa y publica solo recortes revisados.
6. Ejecuta `audit_notes.py check` y realiza la segunda pasada conceptual comparando el resultado con las fuentes y el mapa. Los avisos automáticos necesitan juicio, no correcciones ciegas.
7. Informa del resultado de forma breve en el chat; no generes un archivo de informe.

## Tratamiento de las fuentes

Los materiales del profesor son la fuente principal. Pueden ser PDF, imágenes, notebooks o archivos de código en el lenguaje utilizado por la asignatura. Puedes usar conocimiento propio, bibliografía, documentación oficial o búsqueda web para aclarar una idea, completar un paso omitido o comprobar un dato, pero no para desplazar el enfoque docente ni añadir contenido tangencial.

- No incluyas citas, bibliografía, números de página ni expresiones como «según las diapositivas».
- Si dos materiales se contradicen y no existe una resolución evidente, detente y consulta al usuario antes de escribir la parte afectada.
- Corrige un error del material solo cuando sea manifiesto. En ese caso usa exactamente un callout de corrección con una fuente oficial o académica:

```markdown
> [!warning] Corrección
> En el material aparece [...], pero la expresión correcta es [...].
> Fuente de comprobación: [Fuente oficial o académica](URL)
```

- Para una laguna que no pueda resolverse con suficiente confianza, escribe un `TODO` breve que diga qué falta. Continúa con el resto del tema.
- Antes de corregir una afirmación, distingue un error de una hipótesis omitida, una simplificación o una convención distinta, siguiendo la referencia de algoritmos y errores.
- No elabores soluciones nuevas para ejercicios. Incluye soluciones solo si figuran en los materiales.
- Si aparece un examen o problema evaluable sin solución, pide permiso antes de resolverlo.

## Modos y estado

- `crear`: redacta sobre una nota vacía o crea el destino si el usuario lo ha autorizado; establece `estado: pendiente de revisión`. Si ya contiene los apuntes de los mismos materiales, termina sin cambios. Si la petición ya autoriza completar o revisar esa nota, usa el modo correspondiente; consulta solo cuando el alcance sea ambiguo.
- `actualizar`: integra únicamente información nueva o corregida; si hay cambios reales, establece `estado: actualizado`. Si no hay novedad, no modifiques nada.
- `revisar`: completa, corrige o reorganiza la nota según lo solicitado y, tras auditarla, establece `estado: completado`.

Usa este frontmatter al crear una nota:

```yaml
---
estado: pendiente de revisión
---
```

Al actualizar un frontmatter existente, conserva todas sus demás propiedades. En ningún modo añadas fechas, fuentes o propiedades no solicitadas.

## Límites de actuación

- No muevas, renombres, edites ni elimines nada dentro de `_materiales/`.
- No modifiques el índice de la asignatura, otros temas ni archivos no indicados.
- Puedes crear `imgs/` dentro de la asignatura y añadir allí exclusivamente los recortes necesarios para la nota.
- Puedes guardar extracciones, mapas de cobertura, snapshots, especificaciones de recortes y resultados de auditoría en un directorio temporal del sistema. Esos archivos son de trabajo y nunca se añaden a los apuntes ni al repositorio.
- No ejecutes `git add`, `git commit`, `git push` ni operaciones que alteren el historial. Puedes consultar el diff para auditar el alcance.
- La operación debe ser idempotente: repetirla sin materiales o instrucciones nuevas no debe cambiar archivos ni regenerar imágenes. Las excepciones son una revisión solicitada o la resolución de un `TODO`.

## Entrega

Resume en el chat: modo, nota afectada, materiales y páginas procesadas, imágenes añadidas, correcciones y `TODO`, y resultado de la auditoría. Para notebooks o código sin paginación, indica archivos o secciones procesados. Si se está evaluando el ahorro de tiempo, añade las duraciones observadas de preparación, lectura visual, redacción y auditoría; no atribuyas al razonamiento todo el tiempo transcurrido. Sé mucho más breve que el máximo permitido. El límite absoluto es `300 × ceil(páginas procesadas / 50)` palabras, considerando un primer tramo de hasta 50 páginas; si no hay fuentes paginadas, el máximo es 300 palabras.
