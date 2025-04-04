def mensaje_texto(numero: str, body: str) -> dict:
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": numero,
        "type": "text",
        "text": {"body": body},
    }


def mensaje_botones_confirmar_num_tickets(numero: str, body: str) -> dict:
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
                            "id": "cantidad_tickets_si",
                            "title": "Sí, proceder al pago",
                        },
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "cantidad_tickets_no",
                            "title": "No, corregir tickets",
                        },
                    },
                ]
            },
        },
    }
