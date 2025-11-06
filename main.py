import requests
import json
from datetime import datetime
import os

# API URL
API_URL = "https://datos.cdmx.gob.mx/api/3/action/datastore_search?resource_id=cce544e1-dc6b-42b4-bc27-0d8e6eb3ed72&limit=1000"

# Crear carpeta para guardar los datos
OUTPUT_DIR = "datos_locales"

def fetch_and_save_metro_data():
    """
    Extrae datos de la API de afluencia del Metro CDMX y los guarda 
    en un archivo JSON dentro de la carpeta 'datos_locales'.
    """
    print("Iniciando extracción de datos...")

    try:
        response = requests.get(API_URL)
        # Asegurarnos que la peticion fue exitosa (codigo 200)
        response.raise_for_status() 
        
        print("Conexión con la API exitosa.")
        data = response.json()
        
        # Validamos que la respuesta es la que esperamos
        if not data.get('success'):
            print("Error: La API no reportó éxito en la respuesta.")
            return None, None
            
        records = data['result']['records']
        
        # Crear la carpeta de salida si no existe
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        
        # Generar un nombre de archivo único con la fecha de hoy
        today_str = datetime.now().strftime("%Y-%m-%d")
        file_name = f"afluencia_metro_{today_str}.json"
        file_path = os.path.join(OUTPUT_DIR, file_name)
        
        # Guardar los datos en el archivo localmente para probar
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=4)
        
        print(f"Datos guardados exitosamente en {file_path}")
        return file_path, records

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return None, None
    except KeyError:
        print("Error: La estructura del JSON de la API no es la esperada.")
        return None, None
    except Exception as e:
        print(f"Un error inesperado ocurrió: {e}")
        return None, None

# Esto es para que podamos probarlo directamente desde la terminal
if __name__ == "__main__":
    fetch_and_save_metro_data()