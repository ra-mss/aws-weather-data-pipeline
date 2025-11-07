import json
import requests
from datetime import datetime
import boto3
import os # Importamos 'os' para leer las variables de entorno


API_KEY = os.environ.get('API_KEY') 

BUCKET_NAME = 'aws-weather-data-pipeline-gdl' 

# Coordenadas de Guadalajara
LAT = "20.6736" 
LON = "-103.344"

# Inicializamos el cliente de S3
s3 = boto3.client('s3')

def lambda_handler(event, context):
    """
    Función principal de Lambda:
    1. Llama a la API de OWM.
    2. Añade una marca de tiempo.
    3. Guarda el resultado en S3.
    """
    print("Iniciando extracción de datos del clima...")

    if not API_KEY:
        print("Error: La variable de entorno API_KEY no está configurada en Lambda.")
        return {'statusCode': 500, 'body': 'API_KEY no configurada.'}

    # Construimos la URL de la API
    api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(api_url)
        response.raise_for_status() # Lanza un error si la respuesta no es 200

        print("Conexión con la API exitosa.")
        data = response.json()

        # Añadir una marca de tiempo de cuándo lo consultamos
        extraction_timestamp = datetime.utcnow().isoformat()
        data['extraction_timestamp_utc'] = extraction_timestamp

        # Organizamos los datos por fecha para que sea fácil consultarlos
        now = datetime.utcnow()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        file_name = f"clima_gdl_{now.strftime('%Y-%m-%d_%H-%M-%S')}.json"

        # Path completo en S3 (ej: year=2025/month=11/day=06/clima_gdl_...)
        file_key = f"year={year}/month={month}/day={day}/{file_name}"

        # Guardar el objeto en S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_key,
            Body=json.dumps(data, ensure_ascii=False, indent=4)
        )

        print(f"Datos guardados exitosamente en s3://{BUCKET_NAME}/{file_key}")

        return {
            'statusCode': 200,
            'body': json.dumps(f'Archivo {file_key} guardado en S3!')
        }

    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP: {e}")
        return {'statusCode': e.response.status_code, 'body': e.response.text}
    except Exception as e:
        print(f"Un error inesperado ocurrió: {e}")
        raise e