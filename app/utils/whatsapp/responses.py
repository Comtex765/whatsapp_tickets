def mensaje_texto(numero: str, body: str, url: bool = False) -> dict:
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": numero,
        "type": "text",
        "text": {"preview_url": url, "body": body},
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


def mensaje_lista_inicio(numero: str) -> dict:
    from utils.constantes import id_interactivos
    from utils.constantes import mensajes as msg

    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": numero,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {"type": "text", "text": "🎉 Bienvenido a RIOSOFT369"},
            "body": {"text": "Selecciona una opción del menú para continuar"},
            "footer": {"text": "Tu experiencia comienza aquí 🚀"},
            "action": {
                "button": "Ver opciones",
                "sections": [
                    {
                        "title": "📋 Opciones disponibles",
                        "rows": [
                            {
                                "id": id_interactivos.ID_LISTA_REGISTRO,
                                "title": msg.OPCION_PRINCIPAL_REGISTRO["title"],
                                "description": msg.OPCION_PRINCIPAL_REGISTRO[
                                    "description"
                                ],
                            },
                            {
                                "id": id_interactivos.ID_LISTA_COMPRA_TICKETS,
                                "title": msg.OPCION_PRINCIPAL_COMPRA["title"],
                                "description": msg.OPCION_PRINCIPAL_REGISTRO[
                                    "description"
                                ],
                            },
                        ],
                    }
                ],
            },
        },
    }
