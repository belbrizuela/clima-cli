import argparse  # Analiza los comandos que pone el usuario. Maneja los argumentos.
import requests  # Simplifica el envío de solicitudes HTTP. Es una herramienta para realizar llamadas a la API.
import json  # Proporciona funciones para analizar los archivos JSON y convertirlos en diccionarios y listas en Python.
import sys  # Proporciona funciones específicas como salir o entrar en un programa de Python.
from dotenv import load_dotenv
import os


# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Accede a la API key
api_key = os.getenv('API_KEY')


def analizar_argumento():
    analizador = argparse.ArgumentParser(description='Este programa analiza el clima de una Ciudad, País o ambos')  # Crea un objeto para analizar los argumentos de la línea de comandos.
    analizador.add_argument('ubicacion', help='Especificar el lugar como Ciudad-Pais (ejemplo: Asuncion-PY)')
    analizador.add_argument('--output', choices=['json', 'csv', 'plain'], default='plain', help='Elige el formato de salida')
    return analizador.parse_args()  # Analiza los comandos que ingresó el usuario y devuelve un objeto con los argumentos.

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

def mostrar_datos(clima, tipo_formato):
    if tipo_formato == 'json':
        temperatura = clima['main']['temp']
        descripcion = clima['weather'][0]['description']
        lista = []
        lista.append({"Temperatura" :temperatura})
        lista.append({"Descripcion" :descripcion})
        print(json.dumps(lista, indent=2))  # Muestra los datos en formato JSON con una sangría de 2 espacios.
    elif tipo_formato == 'csv':
        temperatura = clima['main']['temp']  # Obtiene la temperatura.
        descripcion = clima['weather'][0]['description']  # Obtiene la descripción del clima.
        print(f'temperatura,{temperatura}\ncondición,{descripcion}')  # Muestra los datos en formato CSV.
    else:
        temperatura = clima['main']['temp']
        descripcion = clima['weather'][0]['description']
        print(f'La temperatura actual es {temperatura} ºC con {descripcion}')  # Muestra los datos en formato de texto plano.

def main():
    argumentos = analizar_argumento()  # Almacena los datos ingresados por el usuario.
    try:
        ciudad, pais = argumentos.ubicacion.split('-')  # Separa ciudad y país a partir de la ubicación ingresada.
    except ValueError:
        print('Error: Asegúrate de que la ubicación esté marcada como ciudad-país (ejemplo: Asuncion-PY)')
        sys.exit(1)
    
    clima = buscador_meteorologico(ciudad, pais, api_key)  # Obtiene los datos meteorológicos.
    
    if clima: 
        mostrar_datos(clima, argumentos.output)  # Muestra los datos en el formato seleccionado.

if __name__ == '__main__':
    main()  # Ejecuta la función principal.