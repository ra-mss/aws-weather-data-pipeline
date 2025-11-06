import requests
import json
from datetime import datetime
import os

#CONFIGURACIÓN

API_KEY = "5b3e673a3462a698120c6a621b8df17d" 

# Coordenadas de Guadalajara (puedes cambiarlas por cualquier ciudad)
# Para obtenerlas: https://www.latlong.net/
LAT = "20.6736" 
LON = "-103.344"

API_URL = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"

# Carpeta para guardar los datos
OUTPUT_DIR = "datos_locales"

def fetch_and_save_weather_data():
    """
    Extrae datos del clima actual de OWM y los guarda en un archivo JSON
    dentro de la carpeta 'datos_locales'.
    """
    print("Iniciando extracción de datos del clima...")

    try:
        response = requests.get(API_URL)
        # Asegurarnos que la peticion fue exitosa (codigo 200)
        response.raise_for_status() 
        
        print("Conexión con la API exitosa.")
        data = response.json()
        
        # Añadir una marca de tiempo de cuándo lo consultamos
        data['extraction_timestamp_utc'] = datetime.utcnow().isoformat()
        
        # Crear la carpeta de salida si no existe
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        
        # Generar un nombre de archivo único con la fecha y hora
        now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"clima_gdl_{now_str}.json"
        file_path = os.path.join(OUTPUT_DIR, file_name)
        
        # Guardar los datos en el archivo localmente para probar
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Datos guardados exitosamente en {file_path}")
        return file_path, data

    except requests.exceptions.HTTPError as e:
        # Errores específicos de la API (ej. API key incorrecta, 401)
        print(f"Error HTTP: {e}")
        print(f"Respuesta de la API: {e.response.text}")
        return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return None, None
    except Exception as e:
        print(f"Un error inesperado ocurrió: {e}")
        return None, None

# Esto es para que podamos probarlo directamente desde la terminal
if __name__ == "__main__":
    fetch_and_save_weather_data()