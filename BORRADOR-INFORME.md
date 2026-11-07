# Informe de trabajo · Validación de meteoritos y CI/CD

Completa el nombre, enlaces, resultados remotos y capturas después de ejecutar la demostración. Exporta este documento completado a un único PDF.

**Estudiante** [nombre completo]  
**Repositorio público** [enlace]  
**GitHub Pages** [enlace verificado en ventana privada]

## Objetivo y preparación de los datos

El proyecto automatiza la validación de Meteorite Landings y la publicación de un informe web. La muestra conserva las primeras 20.000 filas de la descarga original de 45.716, en su orden original. Contiene id, name, recclass, mass (g), fall, year, reclat y reclong. Los campos vacíos se representan como datos faltantes y los ceros se incluyen en los cálculos que corresponden. El CSV de origen trae los años presentes como enteros de cuatro cifras. La muestra inicial incluye 70 masas, 134 años y 2.429 pares de coordenadas faltantes. La validación no encontró errores en esas filas. Fuente de los datos de The Meteoritical Society. [NASA Open Data](https://data.nasa.gov/dataset/meteorite-landings)

## Organización y CI/CD

El repositorio guarda datos/meteoritos.csv, preparar_datos.py, validar.py, analizar.py, generar.py, las pruebas unitarias y el workflow. Se usó Python con su biblioteca estándar. El CSV versionado es la entrada de cada ejecución. El HTML se escribe en public/index.html después de validar.

Cada push a main o ejecución manual inicia CI. CI ejecuta las pruebas unitarias, revisa el CSV completo y genera el sitio. CD requiere el éxito de CI y despliega el artefacto a GitHub Pages. El sitio muestra el identificador del commit desplegado, que se puede comparar con la ejecución de Actions.

## Resultados y evidencias

Localmente pasaron diez pruebas automatizadas. El CSV inicial contiene 1.107 caídas observadas, 18.893 hallazgos y 20.000 registros en total. Anota la masa media inicial y la de la primera actualización válida.

| Caso | Dato introducido | Resultado esperado | Resultado observado y enlace a Actions |
| --- | --- | --- | --- |
| Primera publicación | 20.000 registros de la muestra | CI y CD correctos | [Completar] |
| Registro válido | 900001, masa 120 g | 20.001 y fila visible | [Completar] |
| Masa negativa | 900002, masa -20 g | Error en mass (g), CD omitido | [Completar] |
| Corrección de masa | 900002, masa 20 g | 20.002 y despliegue | [Completar] |
| Latitud inválida | 900003, latitud 95 | Error en reclat, CD omitido | [Completar] |
| Corrección de latitud | 900003, latitud -17,4 | 20.003 y despliegue | [Completar] |
| ID duplicado | ID 1 | Error en id, CD omitido | [Completar] |
| Corrección de ID | ID 900004 | 20.004 y despliegue | [Completar] |

Inserta capturas legibles de la primera publicación, del registro válido en la tabla, de cada fallo y de cada corrección. En cada caso inválido registra el SHA que siguió visible en Pages. Bajo cada captura indica el caso, el SHA o la ejecución y lo que muestra.

## Conclusiones

[Explica con tus palabras qué diferencia hay entre las pruebas unitarias y la validación del CSV real. Describe una dificultad, cómo se resolvió y qué observaste al comparar el commit fallido con el que seguía publicado.]

Se utilizó Codex como apoyo para preparar los datos, redactar el código y verificar el funcionamiento local.
