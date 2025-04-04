import http.client
import json
from os import getenv

# Variables de entorno
WHATSAPP_CLOUD_TOKEN = getenv("WHATSAPP_CLOUD_TOKEN")
NUMBER_ID = getenv("NUMBER_ID")


def enviar_mensaje_whatsapp(response_data):
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
        print("Código de respuesta:", response.status)
        print("Respuesta:", response.read().decode())

    except Exception as e:
        # Se captura cualquier error en la conexión o solicitud
        print("Error >>", e)

    finally:
        # Se cierra la conexión para liberar recursos
        connection.close()
