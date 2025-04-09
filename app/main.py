from os import getenv

import utils.constantes.estados as est
import uvicorn
from colorama import Fore, init
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from services.registro import gestion_registro
from services.reserva import gestion_reserva
from services.pago import gestion_pago
from utils.session import sesiones_usuarios
from utils.validaciones import validar_usuario_existe

init(autoreset=True)  # Esto hace que después de cada print, se reinicie el color

app = FastAPI()


META_HUB_TOKEN = getenv("META_HUB_TOKEN")
PORT = int(getenv("PORT"))


@app.get("/webhook")
async def verify_webhook(request: Request):
    # Obtener parámetros de la query
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    # Verificar suscripción
    if mode == "subscribe" and token == META_HUB_TOKEN and challenge:
        return PlainTextResponse(content=challenge)

    # Respuesta en caso de fallo
    return PlainTextResponse(content="Token Inválido", status_code=401)


@app.post("/webhook")
async def recibir_mensajes(request: Request):
    try:
        req = await request.json()
        objeto_mensaje = req["entry"][0]["changes"][0]["value"]["messages"]

        if objeto_mensaje:
            mensaje_recibido = objeto_mensaje[0]
            numero_telefono = mensaje_recibido["from"]

            if "type" in mensaje_recibido:
                tipo = mensaje_recibido["type"]

                if tipo == "interactive":
                    tipo_interactivo = mensaje_recibido["interactive"]["type"]
                    if tipo_interactivo == "button_reply":
                        texto_mensaje = mensaje_recibido["interactive"]["button_reply"][
                            "id"
                        ]

                    elif tipo_interactivo == "list_reply":
                        texto_mensaje = mensaje_recibido["interactive"]["list_reply"][
                            "id"
                        ]

                if "text" in mensaje_recibido:
                    texto_mensaje = mensaje_recibido["text"]["body"]

            print(Fore.BLUE + "\nMENSAJE RECIBIDO")
            print(Fore.GREEN + "📱 Número  :\t" + Fore.WHITE + f"+{numero_telefono}")
            print(Fore.GREEN + "💬 Mensaje :\t" + Fore.WHITE + f"{texto_mensaje}\n")

            # Si no existe una sesión activa para el número, se crea
            if numero_telefono not in sesiones_usuarios:
                # Consultamos si el usuario ya existe en la BD
                user_db = validar_usuario_existe(numero_telefono)

                # Si existe en la BD, saltamos a la fase de reserva
                fase_inicial = est.FASE_RESERVA if user_db else est.FASE_REGISTRO
                estado_inicial = est.INICIO_RESERVA if user_db else est.INICIO_REGISTRO

                # Guardamos la sesión del usuario
                sesiones_usuarios[numero_telefono] = {
                    "existe": user_db,
                    "fase": fase_inicial,
                    "estado": estado_inicial,
                    "datos": {},
                }

            # Extraemos la fase y usuario desde la sesión
            fase_actual = sesiones_usuarios[numero_telefono]["fase"]
            user_db = sesiones_usuarios[numero_telefono]["existe"]

            # Procesamos según la fase
            if fase_actual == est.FASE_REGISTRO:
                gestion_registro(texto_mensaje, numero_telefono, sesiones_usuarios)
            elif fase_actual == est.FASE_RESERVA:
                gestion_reserva(texto_mensaje, numero_telefono, sesiones_usuarios)
            elif fase_actual == est.FASE_PAGO:
                gestion_pago(texto_mensaje, numero_telefono, sesiones_usuarios)
                pass

        return {"message": "EVENT_RECEIVED"}
    except Exception:
        return {"message": "EVENT_RECEIVED"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
