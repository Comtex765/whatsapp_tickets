import utils.whatsapp.responses as wpp_resp
from utils import mensajes
from utils import validaciones as check
from utils.whatsapp.sender import enviar_mensaje_whatsapp


def gestion_registro(texto, numero, sesiones_usuarios):
    # Normalizar texto recibido: eliminar espacios y a minúsculas
    texto = texto.strip().lower()

    # Se obtiene el estado actual del usuario en el flujo de registro
    estado_actual = sesiones_usuarios[numero]["estado"]

    try:
        # Estado inicial del flujo
        if estado_actual == "inicio":
            mensaje = mensajes.BIENVENIDA

            sesiones_usuarios[numero]["estado"] = "esperando_cedula"

        # Estado donde se espera que el usuario envíe su cédula
        elif estado_actual == "esperando_cedula":
            if texto.isdigit() and len(texto) == 10:
                if check.validar_cedula(
                    texto
                ):  # Validación formal de cédula ecuatoriana
                    sesiones_usuarios[numero]["datos"]["cedula"] = texto
                    sesiones_usuarios[numero]["estado"] = "esperando_nombre_apellido"

                    mensaje = mensajes.CEDULA_OK
                else:
                    mensaje = mensajes.CEDULA_NO_VALIDA
            else:
                mensaje = mensajes.CEDULA_ERROR

        # Estado donde se espera el nombre y apellido
        elif estado_actual == "esperando_nombre_apellido":
            nombres_apellidos = texto.split(" ", 1)

            if len(nombres_apellidos) < 2:
                mensaje = mensajes.NOMBRE_APELLIDO_ERROR
            else:
                nombre = nombres_apellidos[0].strip().title()
                apellido = nombres_apellidos[1].strip().title()

                # Verificar si nombre y apellido contienen solo letras
                if (
                    not nombre.replace(" ", "").isalpha()
                    or not apellido.replace(" ", "").isalpha()
                ):
                    mensaje = mensajes.NOMBRE_APELLIDO_ERROR
                else:
                    sesiones_usuarios[numero]["datos"]["nombre"] = nombre
                    sesiones_usuarios[numero]["datos"]["apellido"] = apellido
                    sesiones_usuarios[numero]["estado"] = "esperando_fecha_nacimiento"

                    mensaje = mensajes.FECHA_NACIMIENTO_SOLICITUD

        # Estado donde se espera la fecha de nacimiento
        elif estado_actual == "esperando_fecha_nacimiento":
            if check.validar_fecha_nacimiento(texto):
                sesiones_usuarios[numero]["datos"]["fecha_nacimiento"] = texto
                sesiones_usuarios[numero]["estado"] = "esperando_direccion"

                mensaje = mensajes.DIRECCION_SOLICITUD
            else:
                mensaje = mensajes.FECHA_NACIMIENTO_ERROR

        # Estado donde se solicita la dirección
        elif estado_actual == "esperando_direccion":
            sesiones_usuarios[numero]["datos"]["direccion"] = texto

            # Cambiar la fase a 'reserva' y el estado a 'esperando_num_tickets'
            sesiones_usuarios[numero]["fase"] = "reserva"
            sesiones_usuarios[numero]["estado"] = "esperando_num_tickets"

            # Imprimir los datos recopilados para revisión
            print(f"El user creado es \n{sesiones_usuarios[numero]}\n")

            # Mensaje de confirmación del registro
            mensaje = mensajes.mensaje_registro_completado(
                sesiones_usuarios[numero]["datos"]
            )
            response_data = wpp_resp.mensaje_texto(numero, mensaje)

            # Envío del mensaje de confirmación
            enviar_mensaje_whatsapp(response_data)

            # Mensaje para la compra de bolotes
            mensaje = mensajes.TICKETS_SOLICITUD
            response_data["text"] = {"body": mensajes.TICKETS_SOLICITUD}

    except Exception as e:
        print(f"Error en gestion_registro: {e}")
        # Si ocurre algún error inesperado, se envía un mensaje genérico
        mensaje = mensajes.ERROR_GENERICO

    # Enviar mensaje a través de la API de WhatsApp
    response_data = wpp_resp.mensaje_texto(numero, mensaje)
    enviar_mensaje_whatsapp(response_data)
