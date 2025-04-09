import database as db
import utils.whatsapp.responses as wpp_resp
from colorama import Fore, init
from services.reserva import gestion_reserva
from utils import validaciones as check
from utils.constantes import estados as est
from utils.constantes import mensajes as msg
from utils.whatsapp.sender import enviar_mensaje_whatsapp

init(autoreset=True)  # Esto hace que después de cada print, se reinicie el color


def gestion_registro(texto, numero_telefono, sesiones_usuarios):
    # Normalizar texto recibido: eliminar espacios y a minúsculas
    texto = texto.strip().lower()

    # Se obtiene el estado actual del usuario en el flujo de registro
    estado_actual = sesiones_usuarios[numero_telefono]["estado"]

    try:
        # Estado inicial del flujo
        if estado_actual == est.INICIO_REGISTRO:
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
                    ] = est.ESPERANDO_NOMBRE_APELLIDO

                    mensaje = msg.CEDULA_OK
                else:
                    mensaje = msg.CEDULA_NO_VALIDA
            else:
                mensaje = msg.CEDULA_ERROR

        # Estado donde se espera el nombre y apellido
        elif estado_actual == est.ESPERANDO_NOMBRE_APELLIDO:
            nombres_apellidos = texto.split(" ", 1)

            if len(nombres_apellidos) < 2:
                mensaje = msg.NOMBRE_APELLIDO_ERROR
            else:
                nombre = nombres_apellidos[0].strip().title()
                apellido = nombres_apellidos[1].strip().title()

                # Verificar si nombre y apellido contienen solo letras
                if (
                    not nombre.replace(" ", "").isalpha()
                    or not apellido.replace(" ", "").isalpha()
                ):
                    mensaje = msg.NOMBRE_APELLIDO_ERROR
                else:
                    sesiones_usuarios[numero_telefono]["datos"]["nombre"] = nombre
                    sesiones_usuarios[numero_telefono]["datos"]["apellido"] = apellido
                    sesiones_usuarios[numero_telefono][
                        "estado"
                    ] = est.ESPERANDO_FECHA_NACIMIENTO

                    mensaje = msg.FECHA_NACIMIENTO_SOLICITUD

        # Estado donde se espera la fecha de nacimiento
        elif estado_actual == est.ESPERANDO_FECHA_NACIMIENTO:
            if check.validar_fecha_nacimiento(texto):
                sesiones_usuarios[numero_telefono]["datos"]["fecha_nacimiento"] = texto
                sesiones_usuarios[numero_telefono]["estado"] = est.ESPERANDO_CORREO

                mensaje = msg.CORREO_SOLICITUD
            else:
                mensaje = msg.FECHA_NACIMIENTO_ERROR

        # Estado donde se espera el correo electrónico
        elif estado_actual == est.ESPERANDO_CORREO:
            if check.validar_correo(texto):
                sesiones_usuarios[numero_telefono]["datos"]["correo"] = texto
                sesiones_usuarios[numero_telefono]["estado"] = est.ESPERANDO_DIRECCION

                mensaje = msg.DIRECCION_SOLICITUD
            else:
                mensaje = msg.CORREO_ERROR

        # Estado donde se solicita la dirección
        elif estado_actual == est.ESPERANDO_DIRECCION:
            sesiones_usuarios[numero_telefono]["datos"]["direccion"] = texto

            # Confirmación y cambio de fase
            sesiones_usuarios[numero_telefono]["fase"] = est.FASE_RESERVA
            sesiones_usuarios[numero_telefono]["estado"] = est.INICIO_RESERVA

            new_user = sesiones_usuarios[numero_telefono]["datos"]
            new_user["numero_telefono"] = numero_telefono

            db.crear_usuario(new_user)
            print(
                Fore.YELLOW
                + "INFO:\t"
                + Fore.WHITE
                + f"El user creado es \n{new_user}\n"
            )

            # Enviar mensaje de confirmación
            mensaje = msg.mensaje_registro_completado(
                sesiones_usuarios[numero_telefono]["datos"]
            )

            response_data = wpp_resp.mensaje_texto(numero_telefono, mensaje)
            enviar_mensaje_whatsapp(response_data)

            gestion_reserva("", numero_telefono, sesiones_usuarios)

            return

    except Exception as e:
        print(Fore.RED + "ERROR GESTION REGISTRO:\t" + Fore.WHITE + f"{e}")
        # Si ocurre algún error inesperado, se envía un mensaje genérico
        mensaje = msg.ERROR_GENERICO

    # Enviar mensaje a través de la API de WhatsApp
    response_data = wpp_resp.mensaje_texto(numero_telefono, mensaje)
    enviar_mensaje_whatsapp(response_data)
