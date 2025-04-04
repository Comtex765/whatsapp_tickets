from os import getenv

import uvicorn
from fastapi import FastAPI, Request
from services.whatsapp_service import gestion_estado_usuario

app = FastAPI()


META_HUB_TOKEN = getenv("META_HUB_TOKEN")
PORT = int(getenv("PORT"))


@app.get("/webhook")
def verify(request: Request):
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if challenge and token == META_HUB_TOKEN:
        return challenge
    else:
        return {"error": "Token Inválido"}, 401


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

            gestion_estado_usuario(text, numero)

        return {"message": "EVENT_RECEIVED"}
    except Exception:
        return {"message": "EVENT_RECEIVED"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
