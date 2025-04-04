import utils.whatsapp.responses as wpp_resp
from utils import mensajes
from utils.whatsapp.sender import enviar_mensaje_whatsapp


def gestion_reserva(texto, numero, sesiones_usuarios):
    # Normalizar texto recibido: eliminar espacios y a minúsculas
    texto = texto.strip().lower()

    # Se obtiene el estado actual del usuario en el flujo de registro
    estado_actual = sesiones_usuarios[numero]["estado"]

    try:
        if estado_actual == "esperando_num_tickets":
            if texto.isdigit() and int(texto) > 0:
                cantidad = int(texto)
                total = cantidad * 2  # cada ticket cuesta $2

                # Guardar en sesión
                sesiones_usuarios[numero]["datos"]["num_tickets"] = cantidad
                sesiones_usuarios[numero]["datos"]["total_pago"] = total

                # Actualizar estado para confirmar pago
                sesiones_usuarios[numero]["estado"] = "confirmar_pago"

                mensaje = mensajes.mensaje_confirmacion_tickets(cantidad, total)
                response_data = wpp_resp.mensaje_botones_confirmar_num_tickets(
                    numero, mensaje
                )

                enviar_mensaje_whatsapp(response_data)
                return

            else:
                mensaje = mensajes.TICKETS_CANTIDAD_ERROR
                response_data = wpp_resp.mensaje_texto(numero, mensaje)

        elif estado_actual == "confirmar_pago":
            if texto in ["sí", "si"]:
                sesiones_usuarios[numero]["fase"] = "pago"
                sesiones_usuarios[numero]["estado"] = "esperando_pago"
                response_data["text"] = {
                    "body": "💳 Perfecto. A continuación te enviaremos las opciones de pago."
                }
            elif texto == "no":
                response_data["text"] = {
                    "body": "❌ Has cancelado la compra. Si deseas empezar de nuevo, escribe *Hola*."
                }
                sesiones_usuarios.pop(numero, None)
            else:
                response_data["text"] = {
                    "body": "❓ Por favor responde *Sí* para continuar con el pago o *No* para cancelar."
                }

    except Exception as e:
        print(f"Error en gestion_registro: {e}")
        # Si ocurre algún error inesperado, se envía un mensaje genérico
        mensaje = mensajes.ERROR_GENERICO

    # Enviar mensaje a través de la API de WhatsApp
    response_data = wpp_resp.mensaje_texto(numero, mensaje)
    enviar_mensaje_whatsapp(response_data)
