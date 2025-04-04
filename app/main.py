from os import getenv

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from services.registro import gestion_registro
from services.reserva import gestion_reserva
from utils.session import sesiones_usuarios

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
        body = await request.json()
        messages = body["entry"][0]["changes"][0]["value"].get("messages", [])

        if messages:
            mensaje = messages[0]
            numero = mensaje["from"]
            text = mensaje.get("text", {}).get("body", "")
            print(f"\n\nMensaje de {numero}: {text}\n\n")

            # Verificar si el usuario ya tiene una sesión
            if numero not in sesiones_usuarios:
                sesiones_usuarios[numero] = {
                    "fase": "registro",  # Sino se empieza por el registro
                    "estado": "inicio",
                    "datos": {},
                }

            fase_actual = sesiones_usuarios[numero]["fase"]

            # Lógica por fase
            if fase_actual == "registro":
                gestion_registro(text, numero, sesiones_usuarios)
            elif fase_actual == "reserva":
                gestion_reserva(text, numero, sesiones_usuarios)
            elif fase_actual == "pago":
                # gestion_pago(text, numero)
                pass

        return {"message": "EVENT_RECEIVED"}
    except Exception:
        return {"message": "EVENT_RECEIVED"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
