def mensaje_texto(numero: str, body: str) -> dict:
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": numero,
        "type": "text",
        "text": {"body": body},
    }


def mensaje_botones_interactivos(
    numero: str,
    body: str,
    id_opc_1: str = "confirmar_si",
    id_opc_2: str = "confirmar_no",
    titulo_1: str = "Sí, continuar",
    titulo_2: str = "No, corregir",
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
                            "id": id_opc_1,
                            "title": titulo_1,
                        },
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": id_opc_2,
                            "title": titulo_2,
                        },
                    },
                ]
            },
        },
    }
