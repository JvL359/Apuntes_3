# Algoritmos y verificación de posibles errores

## Explicar un algoritmo

Usa esta secuencia como guía de cobertura, no como seis encabezados obligatorios. Puede convertirse en párrafos, una lista de pasos y fórmulas, según la dificultad:

1. **Objetivo:** qué se estima, optimiza o construye; distingue evaluación de un objeto fijo y actualización del propio objeto.
2. **Entradas e hipótesis:** datos, modelo o muestras disponibles, parámetros y condiciones necesarias.
3. **Inicialización:** variables, estructuras y valores especiales utilizados.
4. **Actualización:** ecuación exacta y significado de cada término; orden de operaciones, índices y estados previos o nuevos.
5. **Parada y casos límite:** criterio de terminación, bordes, empates y datos ausentes cuando proceda. En métodos episódicos, tratamiento del terminal y actualizaciones que quedan por completar al finalizar.
6. **Resultado e interpretación:** qué devuelve y bajo qué condiciones puede afirmarse convergencia, exactitud u optimalidad.

Transcribe todo el contenido informativo del pseudocódigo a pasos o código legibles, incluso si está incrustado como imagen. No es necesario incrustar también una captura de ese mismo pseudocódigo. Conserva la notación original y no inventes condiciones de convergencia. Si distintas variantes del algoritmo aparecen en el tema, explica la diferencia de actualización, hipótesis o resultado sin repetir todo el desarrollo.

## Clasificar un posible error

Antes de investigar, contrasta la afirmación con sus símbolos, hipótesis y contexto, incluidos los apartados anteriores y posteriores. Registra el caso en el mapa temporal:

- **Errata manifiesta:** signo, índice, dirección de desigualdad o variable contradice la ecuación o definición inmediata. Confirma el significado antes de corregir.
- **Hipótesis omitida o simplificación:** la frase es correcta en un contexto restringido. Explicita brevemente ese alcance cuando pueda establecerse con confianza; no la presentes automáticamente como error del profesor.
- **Convención distinta:** notación, parametrización, índices, normalización o terminología varían entre fuentes. Conserva la convención docente; no sustituyas la definición porque otra referencia utilice otra.
- **Contradicción sustantiva sin resolución evidente:** se mantienen dos afirmaciones incompatibles después de comprobar contexto y convenciones. Consulta al usuario.

Busca una fuente oficial o académica solo para los casos concretos que requieran comprobación, en vez de verificar externamente cada afirmación del tema. Puedes contrastar varios casos con una misma fuente fiable, pero lee el pasaje que sustenta cada decisión.

Un matiz ausente no es suficiente para declarar una corrección manifiesta. Por ejemplo, una afirmación de optimalidad puede depender de la clase de políticas o de hipótesis de exploración; primero identifica esa clase y las condiciones. Un cambio de sentido en un teorema que contradiga su propia desigualdad sí puede ser una errata manifiesta.

Para una corrección manifiesta confirmada, usa el callout y enlace establecidos en `SKILL.md`. Para una ambigüedad que no pueda resolverse, deja un `TODO` breve y sigue con el resto; si hay contradicción entre materiales, consulta antes de elegir. No introduzcas una explicación larga sobre tu investigación en los apuntes.
