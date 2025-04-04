from os import getenv

from fastapi import APIRouter, HTTPException, Request
from services.whatsapp_service import enviar_mensajes_whatsapp

META_HUB_TOKEN = getenv("META_HUB_TOKEN")

router = APIRouter()


@router.get("/webhook")
async def verificar_token(request: Request):
    params = request.query_params

    print(params)
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if challenge and token == META_HUB_TOKEN:
        return int(
            challenge
        )  # FastAPI devuelve respuestas JSON por defecto, challenge debe ser int o str.

    raise HTTPException(status_code=401, detail="Token Inválido")


@router.post("/webhook")
async def recibir_mensajes(request: Request):
    print("\n\nllegooo\n\n")

    try:
        body = await request.json()
        messages = body["entry"][0]["changes"][0]["value"].get("messages", [])

        if messages:
            mensaje = messages[0]
            numero = mensaje["from"]
            text = mensaje.get("text", {}).get("body", "")

            enviar_mensajes_whatsapp(text, numero)

        return {"message": "EVENT_RECEIVED"}
    except Exception:
        raise HTTPException(status_code=400, detail="ERROR")
