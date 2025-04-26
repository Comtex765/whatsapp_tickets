import http.client
import json
from os import getenv

from colorama import Fore, Style, init

init(autoreset=True)  # Esto hace que después de cada print, se reinicie el color


# Variables de entorno
WHATSAPP_CLOUD_TOKEN = getenv("WHATSAPP_CLOUD_TOKEN")
NUMBER_ID = getenv("NUMBER_ID")


# Función para procesar los tipos de mensajes
def procesar_mensaje(mensaje_recibido):
    try:
        tipo = mensaje_recibido["type"]

        if tipo == "interactive":
            tipo_interactivo = mensaje_recibido["interactive"]["type"]

            if tipo_interactivo == "button_reply":
                return mensaje_recibido["interactive"]["button_reply"]["id"]

            elif tipo_interactivo == "list_reply":
                return mensaje_recibido["interactive"]["list_reply"]["id"]

        elif tipo == "image":
            return mensaje_recibido["image"]["id"]

        elif tipo == "text":
            return mensaje_recibido["text"]["body"]

        else:
            raise ValueError("Tipo de mensaje no reconocido")
    except KeyError as e:
        raise ValueError(f"Error de clave al procesar el mensaje: {e}")


def enviar_mensaje_whatsapp (response_data):
    """Función para enviar el mensaje a la API de WhatsApp."""

    # Se convierte el diccionario de datos a una cadena JSON para enviar al servidor
    data = json.dumps(response_data)

    # Se definen los encabezados necesarios para autenticación y tipo de contenido
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {WHATSAPP_CLOUD_TOKEN}",  # Token de acceso a la API
    }

    # Se crea una conexión HTTPS hacia la API de Meta (Facebook Graph API)
    connection = http.client.HTTPSConnection("graph.facebook.com")

    try:
        # Se hace la solicitud POST al endpoint correspondiente para enviar mensajes
        connection.request("POST", f"/v19.0/{NUMBER_ID}/messages", data, headers)

        # Se obtiene la respuesta del servidor
        response = connection.getresponse()
        print(
            Fore.GREEN + "\nCODIGO ENVIO MENSAJE:\t" + Fore.WHITE + f"{response.status}"
        )
        print(
            Fore.GREEN + "RESPUESTA:\t" + Fore.WHITE + response.read().decode(),
            "\n",
        )

    except Exception as e:
        # Se captura cualquier error en la conexión o solicitud
        print(Fore.RED + f"ERORR CONEXION ENVIO MENSAJE:\t" + Fore.WHITE + f"{e}\n")

    finally:
        # Se cierra la conexión para liberar recursos
        connection.close()
