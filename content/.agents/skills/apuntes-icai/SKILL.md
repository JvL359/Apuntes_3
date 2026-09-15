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
- El archivo Markdown de destino, situado en la raíz de la asignatura, correspondiente a un solo tema y nombrado `Tema X - Nombre.md`.

Comprueba que las rutas y archivos existen. No proceses otros materiales por iniciativa propia. Si falta un dato obligatorio o el orden de las fuentes es ambiguo, pide únicamente la información imprescindible antes de escribir.

## Referencias de trabajo

- Lee [redaccion-y-formato.md](references/redaccion-y-formato.md) en toda ejecución.
- Si hay PDF, diapositivas escaneadas o imágenes, lee [materiales-pdf-e-imagenes.md](references/materiales-pdf-e-imagenes.md).
- En los modos `actualizar` y `revisar`, lee [actualizacion-y-revision.md](references/actualizacion-y-revision.md).
- Antes de terminar cualquier modo, lee y aplica [auditoria.md](references/auditoria.md).

Las reglas anteriores sintetizan el estilo de los apuntes de FC y de los archivos `Resumen Tema *.md` de DpL. Consulta esos apuntes originales solo como último recurso cuando las referencias de esta skill no resuelvan una decisión de presentación. No copies peculiaridades accidentales, errores ni convenciones propias de una sola asignatura.

## Flujo

1. Inspecciona el destino y los materiales en el orden indicado.
2. Construye en memoria un mapa de cobertura por fuente y página o sección. No lo guardes en el repositorio.
3. Determina si el tema es predominantemente teórico, práctico o mixto.
4. Diseña una estructura lógica que cubra los materiales sin seguir necesariamente una división diapositiva por diapositiva.
5. Crea o integra el contenido según el modo, incluyendo solo las imágenes que superen los criterios de selección.
6. Realiza una segunda pasada de auditoría comparando el resultado con las fuentes.
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
- No elabores soluciones nuevas para ejercicios. Incluye soluciones solo si figuran en los materiales.
- Si aparece un examen o problema evaluable sin solución, pide permiso antes de resolverlo.

## Modos y estado

- `crear`: redacta sobre una nota existente y vacía y establece `estado: pendiente de revisión`. Si ya contiene apuntes, no la sobrescribas: pide cambiar a `actualizar` o `revisar`.
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
- No ejecutes `git add`, `git commit`, `git push` ni operaciones que alteren el historial. Puedes consultar el diff para auditar el alcance.
- La operación debe ser idempotente: repetirla sin materiales o instrucciones nuevas no debe cambiar archivos ni regenerar imágenes. Las excepciones son una revisión solicitada o la resolución de un `TODO`.

## Entrega

Resume en el chat: modo, nota afectada, materiales y páginas procesadas, imágenes añadidas, correcciones y `TODO`, y resultado de la auditoría. Para notebooks o código sin paginación, indica archivos o secciones procesados. Sé mucho más breve que el máximo permitido. El límite absoluto es `300 × ceil(páginas procesadas / 50)` palabras, considerando un primer tramo de hasta 50 páginas; si no hay fuentes paginadas, el máximo es 300 palabras.
