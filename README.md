# Pipeline de datos del clima en AWS
Este proyecto es un pipeline de datos 100% automatizado que se ejecuta en la nube de AWS.

## Objetivo del proyecto
El objetivo es construir un sistema que, sin necesidad de mi intervención, capture el estado del clima de Guadalajara todos los días. Estos datos se guardan de forma ordenada para poder usarlos en el futuro para análisis de tendencias, series de tiempo o proyectos de Machine Learning.

## ¿Cómo funciona? (Arquitectura)
Este proyecto es serverless, lo que significa que no usa un servidor tradicional. Se basa en tres servicios principales de AWS que trabajan juntos:

### 1. Amazon EventBridge ⏰

- Un trigger programado se activa automáticamente una vez al día (usando una regla cron).

### 2. AWS Lambda 🧠

- Cuando EventBridge se activa, llama a una función de Lambda.

- Esta función contiene un script de Python que se conecta a la API de OpenWeatherMap para pedir el clima actual.

### 3. AWS S3🗄️

- Una vez que Lambda tiene los datos del clima, los procesa y los guarda como un nuevo archivo JSON en un bucket de S3.

- Los archivos se organizan automáticamente en carpetas por año/mes/día para que sean fáciles de encontrar y consultar después.

## Características principales
- Totalmente automatizado: Se ejecuta solo, todos los días, sin necesidad de tocar nada.

- 100% Sin servidor: Costo-eficiente. Solo se paga por los segundos que la función Lambda se ejecuta (que con la capa gratuita de AWS, es prácticamente gratis).

- Manejo seguro de claves (API Keys): La API Key de OpenWeatherMap se guarda de forma segura usando las Variables de Entorno de AWS Lambda. Esto evita que la llave sea robada si el código se hace público.

- Escalable: El sistema puede guardar datos por años sin problemas.

## Tecnologías utilizadas
- Python: Para el script de extracción de datos.

- AWS Lambda: Para ejecutar el código en la nube.

- AWS S3: Para el almacenamiento de los archivos JSON.

- Amazon EventBridge: Para la automatización y programación de la tarea.

- OpenWeatherMap API: Como fuente de datos del clima.

- Git / GitHub: Para el control de versiones y la documentación.

