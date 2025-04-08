import utils.whatsapp.responses as wpp_resp
from colorama import Fore, Style, init
from utils import estados as est
from utils import mensajes
from utils.whatsapp.sender import enviar_mensaje_whatsapp

init(autoreset=True)  # Esto hace que después de cada print, se reinicie el color


def gestion_reserva(texto, numero, sesiones_usuarios):
    # Normalizar texto recibido: eliminar espacios y a minúsculas
    texto = texto.strip().lower()

    # Se obtiene el estado actual del usuario en el flujo de registro
    estado_actual = sesiones_usuarios[numero]["estado"]

    try:
        if estado_actual == est.ESPERANDO_NUM_TICKETS:
            if texto.isdigit() and int(texto) > 0:
                cantidad = int(texto)
                total = cantidad * 2  # cada ticket cuesta $2

                # Guardar en sesión
                sesiones_usuarios[numero]["datos"]["num_tickets"] = cantidad
                sesiones_usuarios[numero]["datos"]["total_pago"] = total

                # Actualizar estado para confirmar el número correcto de tickets y el monto
                sesiones_usuarios[numero]["estado"] = est.CONFIRMAR_NUM_TICKETS

                mensaje = mensajes.mensaje_confirmacion_tickets(cantidad, total)
                response_data = wpp_resp.mensaje_botones_interactivos(
                    numero,
                    mensaje,
                    id_opc_1="num_tickets_si",
                    id_opc_2="num_tickets_no",
                )

                enviar_mensaje_whatsapp(response_data)
                return

            else:
                mensaje = mensajes.OPCION_NO_VALIDA

        elif estado_actual == est.CONFIRMAR_NUM_TICKETS:
            if "num_tickets_si" in texto:
                sesiones_usuarios[numero]["estado"] = est.ESPERANDO_METODO_PAGO
                mensaje = mensajes.SELECCION_METODO_PAGO

                response_data = wpp_resp.mensaje_botones_interactivos(
                    numero,
                    mensaje,
                    id_opc_1="pago_transferencia",
                    id_opc_2="pago_tarjeta",
                    titulo_1="Transferencia",
                    titulo_2="Tarjeta",
                )
                enviar_mensaje_whatsapp(response_data)
                return

        elif estado_actual == est.ESPERANDO_METODO_PAGO:
            if "pago_transferecia" in texto:
                print("pago con transferencia")
                mensaje = "Pago con transerencia en proceso"
            elif "pago_tarjeta" in texto:
                print("pago con tarjeta")
                mensaje = "Pago con tarjeta en proceso"

    except Exception as e:
        print(Fore.RED + "\nERROR GESTION RESERVA:" + Fore.WHITE + f"\t{e}\n")
        # Si ocurre algún error inesperado, se envía un mensaje genérico
        mensaje = mensajes.ERROR_GENERICO

    # Enviar mensaje a través de la API de WhatsApp
    response_data = wpp_resp.mensaje_texto(numero, mensaje)
    enviar_mensaje_whatsapp(response_data)
