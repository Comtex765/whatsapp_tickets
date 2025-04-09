import utils.whatsapp.responses as wpp_resp
from colorama import Fore, init
from utils.constantes import estados as est
from utils.constantes import id_interactivos
from utils.constantes import mensajes as msg
from utils.whatsapp.sender import enviar_mensaje_whatsapp
from services.pago import gestion_pago

init(autoreset=True)  # Esto hace que después de cada print, se reinicie el color


def gestion_reserva(texto, numero_telefono, sesiones_usuarios):
    # Normalizar texto recibido: eliminar espacios y a minúsculas
    texto = texto.strip().lower()

    # Se obtiene el estado actual del usuario en el flujo de registro
    estado_actual = sesiones_usuarios[numero_telefono]["estado"]

    try:
        if estado_actual == est.INICIO_RESERVA:
            sesiones_usuarios[numero_telefono]["estado"] = est.ESPERANDO_NUM_TICKETS
            mensaje = msg.mensaje_tickets_solicitud(
                sesiones_usuarios[numero_telefono]["datos"]["nombre"]
            )

        elif estado_actual == est.ESPERANDO_NUM_TICKETS:
            if texto.isdigit() and int(texto) > 0:
                cantidad = int(texto)
                total = cantidad * 2  # cada ticket cuesta $2

                # Guardar en sesión
                sesiones_usuarios[numero_telefono]["datos"]["num_tickets"] = cantidad
                sesiones_usuarios[numero_telefono]["datos"]["total_pago"] = total

                # Actualizar estado para confirmar el número correcto de tickets y el monto
                sesiones_usuarios[numero_telefono]["estado"] = est.CONFIRMAR_NUM_TICKETS

                mensaje = msg.mensaje_confirmacion_tickets(cantidad, total)
                response_data = wpp_resp.mensaje_botones_interactivos(
                    numero_telefono,
                    mensaje,
                    id_opc_1=id_interactivos.ID_NUM_TICKETS_SI,
                    id_opc_2=id_interactivos.ID_NUM_TICKETS_NO,
                )

                enviar_mensaje_whatsapp(response_data)
                return

            else:
                mensaje = msg.OPCION_NO_VALIDA
                response_data = wpp_resp.mensaje_texto(numero_telefono, mensaje)

                enviar_mensaje_whatsapp(response_data)
                mensaje = msg.mensaje_tickets_solicitud(
                    sesiones_usuarios[numero_telefono]["datos"]["nombre"]
                )

        elif estado_actual == est.CONFIRMAR_NUM_TICKETS:
            if id_interactivos.ID_NUM_TICKETS_SI in texto:
                # Confirmación y cambio de fase
                sesiones_usuarios[numero_telefono]["fase"] = est.FASE_PAGO
                sesiones_usuarios[numero_telefono]["estado"] = est.INICIO_PAGO

                gestion_pago("", numero_telefono, sesiones_usuarios)
                return
            if id_interactivos.ID_NUM_TICKETS_NO in texto:
                sesiones_usuarios[numero_telefono]["estado"] = est.ESPERANDO_NUM_TICKETS
                mensaje = msg.mensaje_tickets_solicitud(
                    sesiones_usuarios[numero_telefono]["datos"]["nombre"]
                )

    except Exception as e:
        print(Fore.RED + "\nERROR GESTION RESERVA:" + Fore.WHITE + f"\t{e}\n")
        # Si ocurre algún error inesperado, se envía un mensaje genérico
        mensaje = msg.ERROR_GENERICO

    # Enviar mensaje a través de la API de WhatsApp
    response_data = wpp_resp.mensaje_texto(numero_telefono, mensaje)
    enviar_mensaje_whatsapp(response_data)
