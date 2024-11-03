# 👗 Vestidos para Cuerpos Reales 

![Descripción de la imagen](imagenes/portada.png)

# 💡 Introducción al proyecto 

Hace unos meses comencé con muchisima ilusión la busqueda del vestido perfecto para mi graduación, sin embargo, tras ojear unas cuántas webs y visitar la mayoría de las tiendas de mi ciudad me di cuenta de algo, o los fabricantes se habían olvidado de mi talla o no encajaba en los patrones de la moda normativa. Me considero una mujer dentro de la media española, ni muy alta ni muy baja, ni muy delgada ni muy gorda, simplemnete en la media, o lo que yo pensaba que era la media. Por lo que investigué un poco qué estaba pasando con las tallas y descubrí que no estaba sola, que miles de mujeres se encontraban en la misma situación que yo. Me leí numerosos artículo hablando del tema, todos mencionaban una misma fuente, la Asecom (La Asociación de empresas de confección y moda de la comunidad de Madrid), la cual realizó un estudio en el que asegura que las tallas 42 y 44 son las que más se venden en España, pese a que los escaparates no muestran precisamente a maniquíes con dichas medidas.

Finalmente encontré mi vestido, pero me costó. Por lo que unos meses más tarde y ya con las herramientas y conocimientos necesarios planteo este proyecto abordando un problema real: **¿Son los vestidos de hoy para las mujeres del hoy?**

Se inicia este proyecto a pequeña escala, analizando nueve de las marcas que visité hace unos meses en busca de vestido las cuales son: Mango, Forever21, Ghospell, Jaded Rose, Love Triangle, NA-KD, Vero Moda, Natural by Lila y Ladypipa. Siendo estas tiendas muy diversas a pqueñas y gran escala tanto españolas como europeas o americanas.


# 🎯 Objetivo 

El objetivo fundamental entorno al cual se desarrolla este proyecto consiste en descubrir si las marcas objeto de nuestro estudio ofrecen diversidad de tallas y suficiente oferta de tallas L y XL, las cuales son las más consumidas en España. Para ello almacenaremos todos los datos recabados y observaremos y analizaremos las siguientes cuestiones:

- La ditribución de vestidos por marca.
- La distribución de prendas por talla para cada marca.
- El precio medio y mediano para los vestidos de cada marca.
- El precio medio y mediano por tallas.
- El porcentaje de prendas por tallas para distintos tipos de vestidos.
- La distribución de vestidos por tallas.

Además, de la marca Forever21 hemos conseguido obtener el stock para cada vestido y talla por lo que también serán analizados estos datos.

# 📁 Estructura

- El proyecto consiste en la implementación de una ETL y un posterioir análisis. Se ha estructurado en una primera fase de extracción de datos. Los datos se han obtenido mediante APIs y scraping de dos páginas web. Las APIs son: [Asos](https://rapidapi.com/DataCrawler/api/asos10) y [Forever21](https://rapidapi.com/apidojo/api/forever21) y las páginas web: [NaturalByLila](https://naturalbylila.com/) y [Ladypipa](https://ladypipa.com/). 

    - La obtención de información de las APIs se ha llevado a cabo en los notebooks 1 y 2 que se pueden encontrar en la carpeta `notebooks` apoyandose en el archivo de `funciones_api.py` de la carpeta `src`. Los datos extraidos han sido almacenados en la carpeta `datos` dentro de `api_asos` y `api_forever21`.

    - El scraping de las webs se puede encontrar en los notebooks `3-scraping_lila.ipynb` y `4-scraping_ladypipa.ipynb` y las funciones de apoyo en la carpeta `src` en el archivo `funciones_craping.py`. 

- Una vez etraidos todos los datos pasamos a la segunda fase de la ETL que es la transformación y limpieza, llevada a cabo en el notebook `5-limpieza.iynb`. En esta fase limpiamos las columnas de cada dataframe añadiendo nuevas columnas o quitando alguna existente y normalizando los datos para poder unificar todos los datos obtenidos en la primera fase.

- El último paso es la creación y carga de los datos en una base de datos SQL, este paso se ejecuta en el notebook `6-creacion_insercion_bbdd.ipynb` apoyandose en las funciones del archivo `funciones_bbdd.py` y `queries.py`. Se crea la base de datos, las tablas y se realizan las consultas necesarias para insertar todos los datos en nuestra base de datos. 

- Finamente, pasamos a la fase del análisis mediante consultas SQL. En esta fase extraeremos la información relevante para analizar las propuestas planteadas como objetivo y mostrar gráficas para observar de una forma más visual los resultados. Toda esta información se puede encontrar en el notebook `7-analisis.ipynb` apoyado en las funciones de `funciones_analisis.py`.

Por lo tanto, el contenido de las carpetas es el siguiente:

- **datos**: Contiene los datos obtenidos de las APIs y el scraping.
  - **api_asos**: Datos obtenidos de la API de ASOS.
  - **api_forever21**: Datos obtenidos de la API de Forever21.
  - **scraping**: Datos obtenidos mediante técnicas de scraping.
  - **dataframes**: Donde se almacenan los dataframes limpios de cada marca.

- **graficos**: Contiene las visualizaciones generadas a partir de los datos.

- **imagenes**: Imágenes utilizadas en el proyecto.

- **notebooks**: Jupyter notebooks con el código y análisis del proyecto.

- **src**: Scripts de Python con funciones de apoyo para los noteboks.