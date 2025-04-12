from os import getenv

import utils.constantes.estados as est
import uvicorn
from colorama import Fore, init
from database import guardar_comprobante
from factory.handler_factory import HandlerFactory
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from models import TransferenciaSch
from utils.session import sesiones_usuarios

init(autoreset=True)  # Esto hace que después de cada print, se reinicie el color
ENV = getenv("ENV")

IS_PROD = ENV == "production"


META_HUB_TOKEN = getenv("META_HUB_TOKEN")

API_TITLE = "Webhook WhatsApp"
API_VERSION = "1.0.0"

PORT = int(getenv("PORT"))


# URLs de documentación
DOCS_URL = None if IS_PROD else "/docs"
REDOC_URL = None if IS_PROD else "/redoc"
OPENAPI_URL = None if IS_PROD else "/openapi.json"


app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    docs_url=DOCS_URL,
    redoc_url=REDOC_URL,
    openapi_url=OPENAPI_URL,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite cualquier método (GET, POST, etc.)
    allow_headers=["*"],  # Permite cualquier encabezado
)


@app.post("/transferencia")
async def registrar_transferencia(transferencia: TransferenciaSch):
    # Llamar a la función para guardar el Transferencia en la base de datos
    try:
        guardar_comprobante(
            transferencia.model_dump()
        )  # Pasar los datos como diccionario
        return {"message": "Transferencia guardado exitosamente"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al guardar el Transferencia: {e}"
        )


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

            print(f"\n\nEl mensaje recibido es {mensaje_recibido}\n\n")

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
                elif tipo == "image":
                    media_id = mensaje_recibido["image"]["id"]
                    texto_mensaje = media_id

                elif tipo == "text":
                    texto_mensaje = mensaje_recibido["text"]["body"]

            # Si no existe una sesión activa para el número, se crea
            if numero_telefono not in sesiones_usuarios:
                # Guardamos la sesión del usuario
                sesiones_usuarios[numero_telefono] = {
                    "fase": est.FASE_INICIO_MSG,
                    "estado": est.INICIO_PRINCIPAL,
                    "datos": {},
                }

            print(Fore.BLUE + "\nMENSAJE RECIBIDO")
            print(Fore.GREEN + "📱 Número  :\t" + Fore.WHITE + f"+{numero_telefono}")
            print(Fore.GREEN + "💬 Mensaje :\t" + Fore.WHITE + f"{texto_mensaje}\n")

            # Extraemos la fase y usuario desde la sesión
            fase_actual = sesiones_usuarios[numero_telefono]["fase"]

            try:
                handler = HandlerFactory.get_handler(fase_actual)
                handler.handle(texto_mensaje, numero_telefono, sesiones_usuarios)
            except ValueError as e:
                print(Fore.RED + f"\nERROR FACTORY:\t " + Fore.WHITE + f"{e}\n")

        return {"message": "EVENT_RECEIVED"}
    except Exception:
        return {"message": "EVENT_RECEIVED"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
