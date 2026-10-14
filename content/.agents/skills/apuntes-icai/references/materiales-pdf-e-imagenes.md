# Materiales PDF e imágenes

## Lectura multimodal

No confíes únicamente en el texto extraído de un PDF. Ejecuta primero `prepare_pdf.py prepare`, siguiendo [herramientas.md](herramientas.md), y combina:

1. Extracción del texto y metadatos de paginación.
2. Renderizado visual de las páginas relevantes.
3. OCR cuando una página sea escaneada, el texto esté trazado como imagen o la extracción resulte incompleta.
4. Inspección visual de fórmulas, gráficas, tablas, diagramas y relaciones espaciales.

Procesa las fuentes en el orden indicado por el usuario. Completa el mapa `coverage.json` en la carpeta temporal con los conceptos, fórmulas, figuras, posibles errores y secciones de destino. No añadas ese mapa al repositorio.

Revisa las miniaturas de todas las páginas. Las señales de poco texto, contenido raster no repetido, caracteres ilegibles o muchos trazos vectoriales priorizan la inspección, pero no prueban que las demás páginas estén completas. Una página con mucho texto puede ocultar una fórmula o un algoritmo en una imagen. El script descuenta imágenes repetidas al priorizar; esas imágenes también pueden ser relevantes y siguen visibles en las miniaturas.

Usa `prepare_pdf.py render` para abrir en bloque las páginas seleccionadas a resolución legible. El OCR es opcional, conserva su resultado separado del texto original y requiere Tesseract y los idiomas instalados; si falla, continúa con la inspección visual. No transcribas matemáticas desde OCR sin contrastarlas con el renderizado.

Si el OCR y la inspección visual producen lecturas incompatibles que afectan al contenido, no adivines: deja un `TODO` o consulta al usuario si existe una contradicción sustantiva.

## Selección de imágenes

Incluye una imagen solo cuando aporte comprensión que se perdería o degradaría al expresarla únicamente con texto. Son candidatas habituales:

- Arquitecturas grandes o con muchas conexiones.
- Diagramas de flujo o bloques.
- Gráficas cuya forma sea parte de la explicación.
- Esquemas espaciales.
- Comparaciones visuales relevantes.

No incluyas fotografías decorativas, logos, portadas, iconos, fondos, ecuaciones que puedan transcribirse limpiamente a LaTeX ni capturas cuyo contenido principal ya esté redactado.

## Recorte y almacenamiento

Cuando una diapositiva combine texto e imagen:

1. Renderiza la página con resolución suficiente para que etiquetas y ejes sean legibles.
2. Recorta únicamente el diagrama, gráfica, arquitectura o región informativa.
3. Evita márgenes amplios y texto circundante que ya se haya incorporado a la nota.
4. Guarda el recorte como PNG en `<Asignatura>/imgs/`; crea esa carpeta si no existe.
5. Conserva los nombres de imágenes existentes. Para un recorte nuevo, acepta el nombre generado por la herramienta o usa un nombre `Pasted image <timestamp>.png` libre de colisiones; no lo renombres solo para hacerlo descriptivo.
6. Incrusta la imagen con la sintaxis de Obsidian utilizada en el vault, por ejemplo `![[Pasted image 20260325174402.png]]`.

Usa `crop_figures.py` para generar y revisar conjuntamente los recortes antes de publicarlos. Sus nombres estables dependen de la fuente, página, región y resolución, de modo que repetir un recorte lo reutiliza. Si un nombre existente tiene contenido diferente, el script rechaza la colisión.

No sustituyas una imagen ilegible por un redibujado y no añadas advertencias sobre su calidad. Selecciona la mejor extracción fiel disponible.

## Integración en la explicación

- Sitúa la imagen inmediatamente después o antes del párrafo que explica qué representa y cómo debe interpretarse.
- No dejes imágenes aisladas sin explicación.
- No uses la imagen como sustituto de definiciones, conclusiones o relaciones que deban quedar escritas.
- Si contiene notación, respétala también en la explicación.

## Límite de densidad

El objetivo es la mínima cantidad de imágenes que conserve la comprensión.

- El máximo habitual es una imagen por subsección.
- Añade una segunda solo si representa una idea distinta y ambas son claramente útiles.
- Usa los resúmenes de DpL como referencia de carga visual máxima. No añadas saltos de línea para satisfacer un contador ni descartes una figura esencial por una proporción mecánica.
- La auditoría informa de imágenes por cantidad de texto; una relación alta produce un aviso para inspección editorial, no un error automático ni una cuota.
- Si el límite obligara a elegir, prioriza arquitecturas, diagramas y gráficas que no puedan reconstruirse mentalmente a partir del texto.

## Idempotencia de imágenes

Antes de generar un recorte, revisa los embeds y archivos existentes para comprobar que la misma figura no esté ya incluida. En una actualización, reutiliza la imagen anterior si su contenido no ha cambiado. Una segunda ejecución con los mismos materiales no debe crear otro PNG ni modificar el embed.
