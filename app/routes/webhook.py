from os import getenv

import utils.constantes.estados as est
from colorama import Fore, init
from core.factory.handler_factory import HandlerFactory
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import PlainTextResponse
from utils.session import sesiones_usuarios

# Obtén el token desde las variables de entorno
META_HUB_TOKEN = getenv("META_HUB_TOKEN")

router = APIRouter()


@router.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    # Verificar si el modo es "subscribe" y el token es correcto
    if mode == "subscribe" and token == META_HUB_TOKEN and challenge:
        return PlainTextResponse(content=challenge)

    # Si alguno de los parámetros no es válido, retornar un error
    if not token or token != META_HUB_TOKEN:
        raise HTTPException(status_code=401, detail="Token Inválido")

    if not challenge:
        raise HTTPException(status_code=400, detail="Falta el parámetro challenge")

    # Si el token y el challenge son incorrectos
    return PlainTextResponse(content="Token o challenge inválido", status_code=401)


# Función principal para manejar el webhook
@router.post("/webhook")
async def recibir_mensajes(request: Request):
    try:
        req = await request.json()
        objeto_mensaje = req["entry"][0]["changes"][0]["value"]["messages"]

        mensaje_recibido = objeto_mensaje[0]
        numero_telefono = mensaje_recibido["from"]

        

        # Procesar el mensaje recibido
        try:
            texto_mensaje = procesar_mensaje(mensaje_recibido)

            print(Fore.BLUE + "\nMENSAJE RECIBIDO")
            print(Fore.GREEN + "📱 Número  :\t" + Fore.WHITE + f"+{numero_telefono}")
            print(Fore.GREEN + "💬 Mensaje :\t" + Fore.WHITE + f"{texto_mensaje}\n")


        except ValueError as e:
            print(Fore.RED + f"ERROR al procesar el mensaje: {e}")
            return {"message": "ERROR en el mensaje", "status": 400}

        # Crear o actualizar la sesión del usuario
        crear_o_actualizar_sesion(numero_telefono)

        # Extraemos la fase actual del usuario
        fase_actual = sesiones_usuarios[numero_telefono]["fase"]

        # Procesar el mensaje dependiendo de la fase
        try:
            handler = HandlerFactory.get_handler(fase_actual)
            handler.handle(texto_mensaje, numero_telefono, sesiones_usuarios)
        except Exception as e:
            print(
                Fore.RED + f"\nERROR en el handler de fase:\t" + Fore.WHITE + f"{e}\n"
            )
            return {"message": "ERROR en el manejo del mensaje", "status": 500}

        return {"message": "EVENT_RECEIVED"}
    except Exception:
        return {"message": "EVENT_RECEIVED"}


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


# Función para manejar la sesión del usuario
def crear_o_actualizar_sesion(numero_telefono):
    if numero_telefono not in sesiones_usuarios:
        sesiones_usuarios[numero_telefono] = {
            "fase": est.FASE_INICIO_MSG,
            "estado": est.INICIO_PRINCIPAL,
            "datos": {},
        }
