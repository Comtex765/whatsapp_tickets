from fastapi import FastAPI, Request, HTTPException
import uvicorn
from os import getenv
from services.whatsapp_service import enviar_mensajes_whatsapp

app = FastAPI()

META_HUB_TOKEN = getenv("META_HUB_TOKEN")
PORT = int(getenv("PORT", 8000))


@app.get("/webhook")
async def verificar_token(request: Request):
    params = request.query_params
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if challenge and token == META_HUB_TOKEN:
        return int(challenge)  # challenge debe ser int o str.

    raise HTTPException(status_code=401, detail="Token Inválido")


@app.post("/webhook")
async def recibir_mensajes(request: Request):

    print("\n\nMensaje recibido en el webhook\n\n")

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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
