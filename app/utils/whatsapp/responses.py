def mensaje_texto(numero: str, body: str) -> dict:
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": numero,
        "type": "text",
        "text": {"body": body},
    }


def mensaje_botones_confirmacion(
    numero: str,
    body: str,
    id_si: str = "confirmar_si",
    id_no: str = "confirmar_no",
    titulo_si: str = "Sí, continuar",
    titulo_no: str = "No, corregir",
) -> dict:
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": numero,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": body},
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": id_si,
                            "title": titulo_si,
                        },
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": id_no,
                            "title": titulo_no,
                        },
                    },
                ]
            },
        },
    }
