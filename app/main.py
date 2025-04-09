from os import getenv

import config
import utils.constantes.estados as est
import uvicorn
from colorama import Fore, init
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from services.registro import gestion_registro
from services.reserva import gestion_reserva
from services.pago import gestion_pago
from services.inicio_conversacion import gestion_inicio_conversacion
from utils.session import sesiones_usuarios
from utils.validaciones import validar_usuario_existe


init(autoreset=True)  # Esto hace que después de cada print, se reinicie el color

app = FastAPI(
    title=config.API_TITLE,
    version=config.API_VERSION,
    docs_url=config.DOCS_URL,
    redoc_url=config.REDOC_URL,
    openapi_url=config.OPENAPI_URL,
)

# Mapeo de fases a funciones
FASE_HANDLER = {
    est.FASE_INICIO_MSG: gestion_inicio_conversacion,
    est.FASE_REGISTRO: gestion_registro,
    est.FASE_RESERVA: gestion_reserva,
    est.FASE_PAGO: gestion_pago,
}


@app.get("/webhook")
async def verify_webhook(request: Request):
    # Obtener parámetros de la query
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    # Verificar suscripción
    if mode == "subscribe" and token == config.META_HUB_TOKEN and challenge:
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
                # Guardamos la sesión del usuario
                sesiones_usuarios[numero_telefono] = {
                    "fase": est.FASE_INICIO_MSG,
                    "estado": est.INICIO_PRINCIPAL,
                    "datos": {},
                }

            # Extraemos la fase y usuario desde la sesión
            fase_actual = sesiones_usuarios[numero_telefono]["fase"]

            # Ejecutar función correspondiente a la fase
            handler = FASE_HANDLER.get(fase_actual)

            if handler:
                handler(texto_mensaje, numero_telefono, sesiones_usuarios)

        return {"message": "EVENT_RECEIVED"}
    except Exception:
        return {"message": "EVENT_RECEIVED"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=config.PORT, reload=True)
