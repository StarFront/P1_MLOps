
Proyecto de Análisis de Datos de Juegos y Usuarios en Steam

Este proyecto se enfoca en analizar la dinámica entre usuarios y juegos en la plataforma Steam. Está compuesto por dos directorios principales y cinco archivos en Python, cada uno desempeñando un rol esencial en el procesamiento y análisis de datos. 

Organización de Carpetas 

dataset: Contiene datos que han pasado por procesos de limpieza y preparación para su análisis. Los archivos CSV resultantes son cruciales para diversas tareas de análisis. 

datasetAPI: Alberga datos específicos utilizados por la API para responder a las solicitudes de los usuarios. Estos datos son fundamentales para el funcionamiento de la API. 

Scripts en Python 

API's_csv: Desglosa el paso a paso del proceso para crear archivos CSV que alimentan la API. Detalla la limpieza, transformación y estructuración de datos para su posterior utilización. 

dummies_csv: Expone la metodología para generar un DataFrame con información sobre usuarios y sus preferencias de género en formato dummy. Este proceso es vital para el análisis de preferencias y recomendaciones. 

matriz_recomendacion: Describe la creación de una matriz de recomendación mediante la técnica de Descomposición de Valor Singular (SVD). Esta matriz es esencial para generar recomendaciones personalizadas. 

EDA: Documenta el proceso de Análisis Exploratorio de Datos, explorando datos, creando visualizaciones y extrayendo información para comprender mejor el conjunto de datos. 

ETL: Detalla el proceso de Extracción, Transformación y Carga de datos (ETL). Explica cómo se obtienen los datos originales, se aplican transformaciones y se preparan para su uso en análisis subsiguientes. 

Main.py - API de Datos

El archivo main.py incluye el código de la API web desarrollada con FastAPI. Esta API proporciona endpoints para consultar y analizar datos relacionados con juegos y usuarios. También incorpora un modelo de recomendación basado en SVD para ofrecer sugerencias personalizadas a los usuarios. 

Este proyecto fusiona la ciencia de datos con la creación de una API interactiva, permitiendo a los usuarios explorar y obtener información valiosa sobre los datos de Steam. La estructura organizativa y los scripts en Python detallan cada fase del proceso de análisis de datos, desde la obtención de datos crudos hasta la generación de recomendaciones.
