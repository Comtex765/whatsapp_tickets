import http.client
import json
from os import getenv
from utils import validaciones as check
from utils import mensajes

# Variables de entorno
WHATSAPP_CLOUD_TOKEN = getenv("WHATSAPP_CLOUD_TOKEN")
NUMBER_ID = getenv("NUMBER_ID")

# Diccionario para manejar sesiones en memoria
sesiones_usuarios = {}


def gestion_estado_usuario(texto, number):
    texto = texto.strip().lower()

    if number not in sesiones_usuarios:
        sesiones_usuarios[number] = {"estado": "inicio", "datos": {}}

    estado_actual = sesiones_usuarios[number]["estado"]

    response_data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "text",
    }

    try:
        if estado_actual == "inicio":
            response_data["text"] = {"preview_url": False, "body": mensajes.BIENVENIDA}
            sesiones_usuarios[number]["estado"] = "esperando_cedula"

        elif estado_actual == "esperando_cedula":
            if texto.isdigit() and len(texto) == 10:
                if check.validar_cedula(texto):
                    sesiones_usuarios[number]["datos"]["cedula"] = texto
                    response_data["text"] = {"body": mensajes.CEDULA_OK}
                    sesiones_usuarios[number]["estado"] = "esperando_nombre_apellido"
                else:
                    response_data["text"] = {"body": mensajes.CEDULA_NO_VALIDA}
            else:
                response_data["text"] = {"body": mensajes.CEDULA_ERROR}

        elif estado_actual == "esperando_nombre_apellido":
            nombres_apellidos = texto.split(" ", 1)

            if len(nombres_apellidos) < 2:
                response_data["text"] = {"body": mensajes.NOMBRE_APELLIDO_ERROR}
            else:
                nombre = nombres_apellidos[0].strip().title()
                apellido = nombres_apellidos[1].strip().title()

                # Verificar si nombre y apellido contienen solo letras
                if (
                    not nombre.replace(" ", "").isalpha()
                    or not apellido.replace(" ", "").isalpha()
                ):
                    response_data["text"] = {"body": mensajes.NOMBRE_APELLIDO_ERROR}
                else:
                    sesiones_usuarios[number]["datos"]["nombre"] = nombre
                    sesiones_usuarios[number]["datos"]["apellido"] = apellido

                    response_data["text"] = {
                        "body": mensajes.FECHA_NACIMIENTO_SOLICITUD
                    }
                    sesiones_usuarios[number]["estado"] = "esperando_fecha_nacimiento"

        elif estado_actual == "esperando_fecha_nacimiento":
            if check.validar_fecha_nacimiento(texto):
                sesiones_usuarios[number]["datos"]["fecha_nacimiento"] = texto
                response_data["text"] = {"body": mensajes.DIRECCION_SOLICITUD}
                sesiones_usuarios[number]["estado"] = "esperando_direccion"
            else:
                response_data["text"] = {"body": mensajes.FECHA_NACIMIENTO_ERROR}

        elif estado_actual == "esperando_direccion":
            sesiones_usuarios[number]["datos"]["direccion"] = texto

            print(f" el user es \n{sesiones_usuarios[number]["datos"]}\n")
            response_data["text"] = {
                "body": mensajes.mensaje_registro_completado(
                    sesiones_usuarios[number]["datos"]
                )
            }
            del sesiones_usuarios[number]  # Eliminar sesión tras completar registro

    except Exception:
        response_data["text"] = {"body": mensajes.ERROR_GENERICO}

    enviar_mensaje_whatsapp(response_data)


def enviar_mensaje_whatsapp(response_data):
    """Función para enviar el mensaje a la API de WhatsApp."""
    data = json.dumps(response_data)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {WHATSAPP_CLOUD_TOKEN}",
    }

    connection = http.client.HTTPSConnection("graph.facebook.com")

    try:
        connection.request("POST", f"/v19.0/{NUMBER_ID}/messages", data, headers)
        response = connection.getresponse()
    except Exception as e:
        print("Error >>", e)
    finally:
        connection.close()
