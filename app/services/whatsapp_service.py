import json
import http.client
from os import getenv

WHATSAPP_CLOUD_TOKEN = getenv("WHATSAPP_CLOUD_TOKEN")
NUMBER_ID = getenv("NUMBER_ID")


def enviar_mensajes_whatsapp(texto, number):
    texto = texto.lower()

    mensajes = {
        "hola": "👋 ¡Hola, bienvenido a RIOSOFT369! 🎟️\nPara comenzar con tu compra de boletos, digita tu número de cédula:",
        "1": "Mand uno",
        "2": {
            "latitude": "45.2014",
            "longitude": "9.1499",
            "name": "Moza Racing",
            "address": "Viale Brambilla, 98, Italia",
        },
        "3": {
            "link": "https://www.turnerlibros.com/ejemplo.pdf",
            "caption": "Temario del Curso #001",
        },
        "4": {"link": "https://filesamples.com/samples/audio/mp3/sample1.mp3"},
        "5": "Introducción al curso! https://youtu.be/6ULOE2tGlBM",
    }

    response_data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": mensajes.get(texto, "Gracias, has ingresado tu número de cédula"),
        },
    }

    data = json.dumps(response_data)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {WHATSAPP_CLOUD_TOKEN}",
    }

    conn = http.client.HTTPSConnection("graph.facebook.com")
    conn.request("POST", f"/v22.0/{NUMBER_ID}/messages", body=data, headers=headers)
    response = conn.getresponse()
    return response.read().decode()
