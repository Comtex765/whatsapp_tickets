import utils.whatsapp.responses as wpp_resp
from colorama import Fore, init
from utils.constantes import estados as est
from utils.constantes import id_interactivos, mensajes
from utils.whatsapp.sender import enviar_mensaje_whatsapp

init(autoreset=True)  # Esto hace que después de cada print, se reinicie el color


def gestion_pago(texto, numero_telefono, sesiones_usuarios):
    # Normalizar texto recibido: eliminar espacios y a minúsculas
    texto = texto.strip().lower()

    # Se obtiene el estado actual del usuario en el flujo de registro
    estado_actual = sesiones_usuarios[numero_telefono]["estado"]

    try:
        if estado_actual == est.INICIO_PAGO:
            sesiones_usuarios[numero_telefono]["estado"] = est.ESPERANDO_METODO_PAGO
            mensaje = mensajes.SELECCION_METODO_PAGO

            response_data = wpp_resp.mensaje_botones_interactivos(
                numero_telefono,
                mensaje,
                id_opc_1=id_interactivos.ID_PAGO_TRANSFERENCIA,
                id_opc_2=id_interactivos.ID_PAGO_TARJETA,
                titulo_1="Transferencia",
                titulo_2="Tarjeta",
            )
            enviar_mensaje_whatsapp(response_data)

            return

        elif estado_actual == est.ESPERANDO_METODO_PAGO:
            if id_interactivos.ID_PAGO_TRANSFERENCIA in texto:
                print("pago con transferencia")
                mensaje = "Pago con transerencia en proceso"
            elif id_interactivos.ID_PAGO_TARJETA in texto:
                print("pago con tarjeta")
                mensaje = "Pago con tarjeta en proceso"

    except Exception as e:
        print(Fore.RED + "\nERROR GESTION RESERVA:" + Fore.WHITE + f"\t{e}\n")
        # Si ocurre algún error inesperado, se envía un mensaje genérico
        mensaje = mensajes.ERROR_GENERICO

    # Enviar mensaje a través de la API de WhatsApp
    response_data = wpp_resp.mensaje_texto(numero_telefono, mensaje)
    enviar_mensaje_whatsapp(response_data)
