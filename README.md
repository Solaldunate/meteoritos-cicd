# Meteoritos · CI/CD

Informe web generado a partir de [Meteorite Landings](https://data.nasa.gov/dataset/meteorite-landings), datos de The Meteoritical Society publicados por la NASA. Las filas con el prefijo SIMULACIÓN son ficticias.

## Inicio rápido

1. Copia el contenido del ZIP a la raíz del repositorio existente, junto a su carpeta .git. Conserva esa carpeta y confirma que .github/workflows/meteoritos.yml quedó en la raíz del repositorio.
2. Escribe tu nombre completo en estudiante.txt.
3. Abre una terminal en esa carpeta con Python 3.12 o posterior. Ejecuta estos comandos.

```powershell
python -m unittest discover -v
python validar.py
python generar.py
```

Abre public/index.html para revisar el informe local. El proyecto usa la biblioteca estándar de Python y funciona sin instalar paquetes adicionales.

## Datos y archivos

La descarga original tiene 45.716 registros. preparar_datos.py extrae los primeros 20.000 en el mismo orden y conserva id, name, recclass, mass (g), fall, year, reclat y reclong. Omite nametype y GeoLocation. El CSV incluido ya está preparado. Para reproducir la preparación desde la descarga original, ejecuta python preparar_datos.py seguido de la ruta del archivo original en una copia sin datos/meteoritos.csv.

Los campos vacíos o con solo espacios se interpretan como faltantes en masa, año y coordenadas. El cero conserva su valor. El año admite enteros, fechas ISO, fecha y hora ISO sin zona y el formato estadounidense con AM/PM. Los años presentes en la muestra original son enteros de cuatro cifras. La revisión inicial encontró 70 masas, 134 años y 2.429 pares de coordenadas faltantes. Las 20.000 filas pasaron la validación.

- validar.py lee el CSV completo y reporta fila, campo y motivo de cada error.
- analizar.py calcula indicadores, clasificaciones y tablas.
- generar.py crea public/index.html a partir de los datos validados.
- test_meteoritos.py ejecuta diez pruebas independientes del CSV principal.
- .github/workflows/meteoritos.yml ejecuta CI y CD.
- .gitignore excluye archivos temporales y el HTML generado. Git conserva el CSV.

## Publicar en GitHub

En el repositorio web, abre Settings → Pages → Build and deployment y selecciona GitHub Actions en Source. En GitHub Desktop crea un commit en main con el mensaje Primera publicación y pulsa Push origin. En Actions abre esa ejecución y espera que CI y CD terminen. Abre el enlace de despliegue y verifica en una ventana privada que el sitio muestre 20.000 registros. Guarda la captura de Actions y de la página inicial.

El workflow se dispara con cada push a main y permite ejecución manual. CI ejecuta las pruebas, valida el CSV del commit y genera el artefacto del sitio. CD depende de CI mediante needs y publica el artefacto en Pages. Si la validación sale con código 1, CD queda omitido y la página sigue sirviendo el último commit desplegado.

## Secuencia de demostración

Agrega una línea al final del CSV por caso y guarda. Haz un commit y push por cada fila o corrección. Espera el resultado y captura la evidencia de cada ejecución antes del siguiente push. Los ejemplos parten de la muestra inicial de 20.000 filas. Agrega cada fila de datos sin copiar la cabecera.

| Commit | Agrega esta fila o corrige el campo indicado | Resultado esperado en Pages |
| --- | --- | --- |
| Agregar registro válido | 900001,SIMULACIÓN Válida,H5,120,Found,2026,-17.4,-66.2 | 20.001 registros y nueva fila visible |
| Probar masa negativa | 900002,SIMULACIÓN Masa,H5,-20,Found,2026,-17.4,-66.2 | CI falla en mass (g). CD omitido. Sigue en 20.001 |
| Corregir masa | Cambia -20 a 20 en la fila 900002 | 20.002 registros |
| Probar latitud inválida | 900003,SIMULACIÓN Coordenada,H5,50,Fell,2026,95,-66.2 | CI falla en reclat. CD omitido. Sigue en 20.002 |
| Corregir latitud | Cambia 95 a -17.4 en la fila 900003 | 20.003 registros |
| Probar ID duplicado | 1,SIMULACIÓN ID,H5,60,Found,2026,-17.4,-66.2 | CI falla en id. CD omitido. Sigue en 20.003 |
| Corregir ID | Cambia el 1 inicial de la última fila a 900004 | 20.004 registros |

Ejecuta python validar.py antes de cada push. En los casos inválidos el error es intencional. Haz el push de demostración, captura el error de CI, el estado omitido de CD y el commit que sigue visible en Pages. En cada corrección vuelve a comprobar que ambos trabajos estén en verde y que aparezca el nuevo commit.

La primera simulación válida aumenta Found de 18.893 a 18.894 y la frecuencia de H5 en uno. Fell y el conteo de masas faltantes conservan sus valores. Como 120 g está por debajo de la media inicial, la media disminuye.

Para la clase, puedes añadir una nueva simulación con ID 900005 y masa -10, hacer push, mostrar el bloqueo y cambiar la masa a 10 en otro commit. Al corregirla, muestra la nueva fila y el SHA publicado.
