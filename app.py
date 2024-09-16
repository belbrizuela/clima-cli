import requests

def buscador_meteorologico(ciudad, pais, api_key):
    api = f'https://api.openweathermap.org/data/2.5/weather?q={ciudad},{pais}&appid={api_key}&units=metric'  # Devuelve la temperatura en grados Celsius.
    try:
        resultado = requests.get(api)  # Solicita datos del servidor específico.
        resultado.raise_for_status()  # Verifica el estado de la respuesta. Si hay un error HTTP, se lanza una excepción.
        return resultado.json()  # Convierte la respuesta JSON en un diccionario de Python.

    except requests.exceptions.HTTPError as errorhttp:
        print(f'Error HTTP: {errorhttp}')  # Imprime un mensaje de error específico para errores HTTP.

    except Exception as error:
        print(f'Ocurrió un error: {error}')  # Imprime un mensaje de error genérico para cualquier otro tipo de error.
    
    return None  # Retorna None si no se pudieron obtener los datos meteorológicos.


