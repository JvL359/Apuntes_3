# Materiales PDF e imágenes

## Lectura multimodal

No confíes únicamente en el texto extraído de un PDF. Usa las herramientas o la skill de PDF disponibles para combinar:

1. Extracción del texto y metadatos de paginación.
2. Renderizado visual de las páginas relevantes.
3. OCR cuando una página sea escaneada, el texto esté trazado como imagen o la extracción resulte incompleta.
4. Inspección visual de fórmulas, gráficas, tablas, diagramas y relaciones espaciales.

Procesa las fuentes en el orden indicado por el usuario. Registra en memoria qué páginas y apartados quedan representados en la nota; no guardes ese registro.

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
- Como techo global, no superes aproximadamente 10 imágenes por cada 100 líneas no vacías de contenido Markdown, densidad máxima observada en los resúmenes de DpL usados como referencia.
- El techo no es una cuota: un tema que se entienda bien sin imágenes debe tener pocas o ninguna.
- Si el límite obligara a elegir, prioriza arquitecturas, diagramas y gráficas que no puedan reconstruirse mentalmente a partir del texto.

## Idempotencia de imágenes

Antes de generar un recorte, revisa los embeds y archivos existentes para comprobar que la misma figura no esté ya incluida. En una actualización, reutiliza la imagen anterior si su contenido no ha cambiado. Una segunda ejecución con los mismos materiales no debe crear otro PNG ni modificar el embed.
