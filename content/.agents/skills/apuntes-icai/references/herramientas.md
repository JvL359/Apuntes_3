# Herramientas de preparación, recorte y auditoría

## Entorno

Los tres scripts están en `../scripts/`. Requieren Python 3.10 o posterior y los paquetes de `scripts/requirements.txt`. Usa el Python del entorno que ya tenga esas dependencias. Si faltan, instala únicamente esos paquetes en un entorno virtual temporal; no cambies la configuración global ni los materiales.

En Windows, `uv python find` permite localizar Python aunque no esté en `PATH`. Si la caché habitual de `uv` no es escribible, selecciona una caché dentro de `$env:TEMP`:

```powershell
$taskCache = Join-Path $env:TEMP 'apuntes-icai-uv-cache'
uv --cache-dir $taskCache python find
# Selecciona la ruta devuelta y úsala al crear el entorno temporal.
$taskVenv = Join-Path $env:TEMP 'apuntes-icai-tools-venv'
uv --cache-dir $taskCache venv --python '<ruta-python>' $taskVenv
$taskPython = Join-Path $taskVenv 'Scripts\python.exe'
uv --cache-dir $taskCache pip install --python $taskPython -r '<skill>/scripts/requirements.txt'
```

Resuelve `<skill>` a la ubicación real de la skill. Conserva esa ruta y el ejecutable durante toda la ejecución. Los ejemplos siguientes usan `python` por brevedad; sustitúyelo por ese ejecutable.

Todos los mapas, previews, extracciones, snapshots y reports deben quedar dentro de una carpeta temporal del sistema. No los añadas al repositorio ni a la nota. Los scripts eligen una carpeta nueva automáticamente si no se proporciona `--output`.

## 1. Preparar PDF

```text
python <skill>/scripts/prepare_pdf.py prepare --pdfs "primero.pdf" "segundo.pdf" --output "<temporal>/tema/preparacion"
```

La carpeta debe estar vacía. Si ya contiene una preparación completa con idénticas fuentes, hashes y opciones, se reutiliza sin extraer de nuevo. Si las fuentes cambian o faltan assets, usa una carpeta temporal nueva.

Produce:

- `manifest.json`: fuentes en el orden indicado, hashes, tamaño y rotación de páginas, rutas, señales de revisión y tiempo de preparación.
- Un archivo de texto y una miniatura por página.
- Hojas de miniaturas numeradas de todas las páginas, en lotes de 12.
- `coverage.json`: una fila por página, inicialmente pendiente.

La señal `little_extracted_text` usa menos de 25 palabras por defecto. Las señales raster y vectoriales detectan riesgos adicionales. Imágenes repetidas en al menos el 60% de un PDF no activan por sí solas la prioridad raster, pero deben inspeccionarse en el overview. Ninguna señal sustituye revisar todas las miniaturas.

Abrir páginas a resolución legible:

```text
python <skill>/scripts/prepare_pdf.py render --manifest "<preparacion>/manifest.json" --source 2 --pages "3,6-9" --dpi 160
```

`source` y los números de página son siempre de base 1. La salida devuelve las rutas de los renders y sus dimensiones en puntos. Reutiliza esos renders para lectura y selección de coordenadas.

OCR opcional: añade `--ocr flagged` o `--ocr all` al preparar y, si procede, `--ocr-language eng+spa`. Requiere Tesseract con esos idiomas disponibles. Los textos OCR quedan separados; una falta de OCR se registra y permite seguir con los renders.

## 2. Completar el mapa de cobertura

Edita `coverage.json` solo en la carpeta temporal, conforme avanzas, sin una fila por cada frase. Una página puede quedar así:

```json
{
  "source": 1,
  "page": 8,
  "status": "covered",
  "items": [
    {"kind": "formula", "concept": "Bellman update", "destination": "III / 4"},
    {"kind": "algorithm", "concept": "Policy improvement", "destination": "III / 5"}
  ],
  "destination_sections": ["III / 4", "III / 5"],
  "visual_reviewed": true,
  "review_reasons": ["little_extracted_text"]
}
```

Estados finales: `covered`, `duplicate`, `irrelevant` o `todo`. Para `duplicate` indica `reason` y la página o concepto equivalente; para `irrelevant`, el motivo; para `todo`, qué falta y dónde se ha marcado en la nota. Puedes anotar `possible_error`, su clasificación y su resolución en los items. No marques la página como cubierta antes de inspeccionar las partes no extraíbles.

## 3. Recortar y publicar figuras

Crea una especificación JSON temporal que haga referencia al manifest:

```json
{
  "preparation": "<ruta absoluta a manifest.json>",
  "crops": [
    {"source": 1, "page": 8, "box": [0.12, 0.20, 0.92, 0.85], "units": "relative"}
  ]
}
```

Las coordenadas son `[izquierda, arriba, derecha, abajo]` sobre la página mostrada, incluyendo su rotación. Con `relative` van de 0 a 1; con `points` utilizan las dimensiones del render. En un render de W × H píxeles, divide x entre W e y entre H para obtener coordenadas relativas. Mantén ejes y etiquetas; excluye logos y texto redundante.

```text
python <skill>/scripts/crop_figures.py --spec "<temporal>/recortes.json" --output "<temporal>/previews" --dpi 220
```

Abre las hojas `crops-*.png` y los PNG individuales a tamaño legible. Ajusta la especificación y vuelve a ejecutar si hace falta. Una vez revisados:

```text
python <skill>/scripts/crop_figures.py --spec "<temporal>/recortes.json" --output "<temporal>/previews" --dpi 220 --publish "<asignatura>/imgs"
```

El script valida todos los recortes y colisiones antes de publicar. Rechaza rutas de publicación distintas de `imgs`, dentro de `_materiales` o de una asignatura distinta de la que contiene las fuentes preparadas. Los nombres generados son estables; si un PNG ya existe y tiene los mismos bytes, lo reutiliza sin modificarlo. Para preservar un nombre explícito, añade `filename`; una colisión con bytes diferentes exige elegir otro nombre, nunca sobrescribirlo. `crops.json` devuelve dimensiones, hashes y embeds listos para la nota.

## 4. Auditoría mecánica y alcance

Antes de editar:

```text
python <skill>/scripts/audit_notes.py snapshot --course "<asignatura>" --output "<temporal>/antes.json"
```

Después:

```text
python <skill>/scripts/audit_notes.py check --course "<asignatura>" --note "<asignatura>/Tema X - Nombre.md" --mode crear --baseline "<temporal>/antes.json" --coverage "<preparacion>/coverage.json" --report "<temporal>/auditoria.json"
```

- Añade `--vault "<content>"` para resolver enlaces fuera de la asignatura.
- Omite `--mode` cuando audites apuntes existentes sin cambiar su estado.
- Una actualización sin novedades usa `--expect-no-change --baseline ...` y omite `--mode`.
- Para sustituir explícitamente una imagen existente, pasa su ruta mediante `--allowed-images`; las imágenes nuevas dentro de `imgs` ya se permiten.
- Códigos de salida: `0` sin errores seguros (puede haber avisos), `1` con errores seguros y `2` para argumentos o entorno inválidos.

Errores seguros: YAML inválido, estado incorrecto, fence abierto, imagen inexistente o cambios fuera del tema. Avisos: numeración, delimitadores matemáticos sospechosos, resumen final, cobertura pendiente, enlace ambiguo, imágenes repetidas o carga visual alta. Revisa los avisos en contexto; no modifiques el texto solo para eliminar un aviso.

El auditor acepta numeración de secciones global o reiniciada por bloque. El aviso matemático ignora código, inline code y dólares escapados, pero no es un parser LaTeX. No comprueba demostraciones, fórmulas, pertinencia de las imágenes ni cobertura real; esas comprobaciones siguen en la segunda pasada conceptual.

## Medir mejoras

Los scripts devuelven su duración. Cuando el usuario pida evaluar rapidez, registra también lectura visual, redacción, auditoría y retoques. Compara el mismo conjunto de fuentes con las mismas reglas y herramientas. Las notas anteriores orientan la comparación, pero cada afirmación y fórmula se contrasta con las fuentes originales. No cambies de modelo ni ejecutes un benchmark con otras llamadas de modelo salvo petición del usuario.

Para verificar las herramientas después de modificarlas, ejecuta `python <skill>/tests/test_tools.py`. Añade `--pdf "<material existente.pdf>"` para probar también preparación, renders y recortes; las pruebas copian ese material a una asignatura temporal, sin editar el original ni los apuntes.
