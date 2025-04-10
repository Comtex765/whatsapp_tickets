import utils.whatsapp.responses as wpp_resp
from colorama import Fore, init
from services.registro import gestion_registro
from services.reserva import gestion_reserva
from utils import validaciones as check
from utils.constantes import estados as est
from utils.constantes import id_interactivos
from utils.constantes import mensajes as msg
from utils.whatsapp.sender import enviar_mensaje_whatsapp

init(autoreset=True)  # Esto hace que después de cada print, se reinicie el color


def gestion_inicio_conversacion(texto, numero_telefono, sesiones_usuarios):
    # Normalizar texto recibido: eliminar espacios y a minúsculas
    texto = texto.strip().lower()

    # Se obtiene el estado actual del usuario en el flujo de registro
    estado_actual = sesiones_usuarios[numero_telefono]["estado"]

    try:
        # Estado inicial del flujo
        if estado_actual == est.INICIO_PRINCIPAL:
            mensaje = msg.BIENVENIDA
            sesiones_usuarios[numero_telefono]["estado"] = est.ESPERANDO_CEDULA

        # Estado donde se espera que el usuario envíe su cédula
        elif estado_actual == est.ESPERANDO_CEDULA:
            if texto.isdigit() and len(texto) == 10:
                if check.validar_cedula(
                    texto
                ):  # Validación formal de cédula ecuatoriana
                    sesiones_usuarios[numero_telefono]["datos"]["cedula"] = texto
                    sesiones_usuarios[numero_telefono][
                        "estado"
                    ] = est.ESPERANDO_OPCION_PRINCIPAL

                    mensaje = msg.CEDULA_OK
                    response_data = wpp_resp.mensaje_texto(numero_telefono, mensaje)
                    enviar_mensaje_whatsapp(response_data)

                    response_data = wpp_resp.mensaje_lista_inicio(numero_telefono)
                    enviar_mensaje_whatsapp(response_data)

                    return

                else:
                    mensaje = msg.CEDULA_NO_VALIDA
            else:
                mensaje = msg.CEDULA_ERROR

        elif estado_actual == est.ESPERANDO_OPCION_PRINCIPAL:
            if id_interactivos.ID_LISTA_REGISTRO in texto:
                # Confirmación y cambio de fase
                sesiones_usuarios[numero_telefono]["fase"] = est.FASE_REGISTRO
                sesiones_usuarios[numero_telefono]["estado"] = est.INICIO_REGISTRO

                gestion_registro("", numero_telefono, sesiones_usuarios)
                return
            elif id_interactivos.ID_LISTA_COMPRA_TICKETS in texto:
                # Confirmación y cambio de fase
                sesiones_usuarios[numero_telefono]["fase"] = est.FASE_RESERVA
                sesiones_usuarios[numero_telefono]["estado"] = est.INICIO_RESERVA

                gestion_reserva("", numero_telefono, sesiones_usuarios)
                return

    except Exception as e:
        print(Fore.RED + "\nERROR GESTION RESERVA:" + Fore.WHITE + f"\t{e}\n")
        # Si ocurre algún error inesperado, se envía un mensaje genérico
        mensaje = msg.ERROR_GENERICO

    # Enviar mensaje a través de la API de WhatsApp
    response_data = wpp_resp.mensaje_texto(numero_telefono, mensaje)
    enviar_mensaje_whatsapp(response_data)
