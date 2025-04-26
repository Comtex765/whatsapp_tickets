import database as db
import utils.whatsapp.responses as wpp_resp
from colorama import Fore, Style
from utils import validaciones as check
from utils.constantes import estados as est
from utils.constantes import mensajes as msg
from utils.whatsapp.sender import enviar_mensaje_whatsapp


class InicioRegistro:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        try:
            # Estado de inicio de registro, esperando nombre y apellido
            cedula = sesiones_usuarios[numero_telefono]["datos"]["cedula"]
            user_db = check.validar_usuario_existe(cedula)

            if user_db:
                # Usuario ya existe, lo redirigimos a la fase de reserva
                sesiones_usuarios[numero_telefono]["fase"] = est.FASE_RESERVA
                sesiones_usuarios[numero_telefono]["estado"] = est.INICIO_RESERVA

                mensaje = msg.usuario_existe(user_db["nombre"])
                sesiones_usuarios[numero_telefono]["datos"] = user_db

                response = wpp_resp.mensaje_texto(numero_telefono, mensaje)
                enviar_mensaje_whatsapp(response)

                # Llamar al handler de la fase de reserva
                try:
                    from core.factory.handler_factory import HandlerFactory

                    handler = HandlerFactory.get_handler(est.FASE_RESERVA)
                    handler.handle("", numero_telefono, sesiones_usuarios)
                except ValueError as e:
                    print(Fore.RED + f"\nERROR FACTORY:\t " + Fore.WHITE + f"{e}\n")

            else:
                # Usuario no encontrado, solicitar nombre y apellido
                mensaje = msg.NOMBRE_APELLIDO_SOLICITUD
                sesiones_usuarios[numero_telefono][
                    "estado"
                ] = est.ESPERANDO_NOMBRE_APELLIDO
                response = wpp_resp.mensaje_texto(numero_telefono, mensaje)
                enviar_mensaje_whatsapp(response)

        except Exception as e:
            print(
                Fore.RED + f"\n[ERROR InicioRegistro.handle] → {e}\n" + Style.RESET_ALL
            )
            mensaje_error = "Ocurrió un error al procesar la solicitud. Por favor, intente nuevamente."
            response_error = wpp_resp.mensaje_texto(numero_telefono, mensaje_error)
            enviar_mensaje_whatsapp(response_error)
            
            sesiones_usuarios[numero_telefono]["estado"] = est.ERROR_REGISTRO


class EsperandoNombreApellido:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        # Separar el texto en nombre y apellido
        nombres_apellidos = texto.split(" ", 1)

        if len(nombres_apellidos) < 2:
            # Si no se proporciona tanto nombre como apellido
            mensaje = msg.NOMBRE_APELLIDO_ERROR
        else:
            nombre = nombres_apellidos[0].strip().title()  # Formatear el nombre
            apellido = nombres_apellidos[1].strip().title()  # Formatear el apellido

            # Validar que solo contenga letras
            if (
                not nombre.replace(
                    " ", ""
                ).isalpha()  # Verifica solo letras en el nombre
                or not apellido.replace(
                    " ", ""
                ).isalpha()  # Verifica solo letras en el apellido
            ):
                mensaje = (
                    msg.NOMBRE_APELLIDO_ERROR
                )  # Error si hay caracteres no alfabéticos
            else:
                # Si todo está bien, almacenar los datos y actualizar el estado
                sesiones_usuarios[numero_telefono]["datos"]["nombre"] = nombre
                sesiones_usuarios[numero_telefono]["datos"]["apellido"] = apellido
                sesiones_usuarios[numero_telefono][
                    "estado"
                ] = est.ESPERANDO_FECHA_NACIMIENTO

                mensaje = (
                    msg.FECHA_NACIMIENTO_SOLICITUD
                )  # Solicitar la fecha de nacimiento

        # Enviar la respuesta correspondiente
        response = wpp_resp.mensaje_texto(numero_telefono, mensaje)
        enviar_mensaje_whatsapp(response)


class EsperandoFechaNacimiento:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        texto = texto.strip()

        if check.validar_fecha_nacimiento(texto):
            # Si la fecha es válida, almacenar y avanzar
            sesiones_usuarios[numero_telefono]["datos"]["fecha_nacimiento"] = texto
            sesiones_usuarios[numero_telefono]["estado"] = est.ESPERANDO_CORREO
            mensaje = msg.CORREO_SOLICITUD
        else:
            # Mensaje de error si la fecha es incorrecta
            mensaje = msg.FECHA_NACIMIENTO_ERROR

        response = wpp_resp.mensaje_texto(numero_telefono, mensaje)
        enviar_mensaje_whatsapp(response)


class EsperandoCorreo:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        texto = texto.strip()

        if check.validar_correo(texto):
            # Almacenar el correo y avanzar al siguiente paso
            sesiones_usuarios[numero_telefono]["datos"]["correo"] = texto
            sesiones_usuarios[numero_telefono]["estado"] = est.ESPERANDO_DIRECCION
            mensaje = msg.DIRECCION_SOLICITUD
        else:
            # Mensaje de error si el correo no es válido
            mensaje = "El correo electrónico ingresado no es válido. Por favor, ingresa un correo en formato correcto."

        response = wpp_resp.mensaje_texto(numero_telefono, mensaje)
        enviar_mensaje_whatsapp(response)


class EsperandoDireccion:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        texto = texto.strip()

        if texto:  # Verificar que no esté vacío
            sesiones_usuarios[numero_telefono]["datos"]["direccion"] = texto
            sesiones_usuarios[numero_telefono]["estado"] = est.FIN_REGISTRO
        else:
            mensaje = "Por favor, ingresa una dirección válida."

            # Enviar mensaje de respuesta
            response = wpp_resp.mensaje_texto(numero_telefono, mensaje)
            enviar_mensaje_whatsapp(response)


class FinRegistro:
    def handle(self, numero_telefono, sesiones_usuarios):
        # Actualizar fase y estado del usuario
        sesiones_usuarios[numero_telefono]["fase"] = est.FASE_RESERVA
        sesiones_usuarios[numero_telefono]["estado"] = est.INICIO_RESERVA

        new_user = sesiones_usuarios[numero_telefono]["datos"]
        new_user["numero_telefono"] = numero_telefono

        try:
            # Intentar crear el usuario en la base de datos
            db.crear_usuario(new_user)

            # Enviar mensaje de confirmación de registro
            mensaje = msg.mensaje_registro_completado(
                sesiones_usuarios[numero_telefono]["datos"]
            )
            response = wpp_resp.mensaje_texto(numero_telefono, mensaje)
            enviar_mensaje_whatsapp(response)

            # Proseguir con la fase de reserva
            from core.factory.handler_factory import HandlerFactory

            handler = HandlerFactory.get_handler(est.FASE_RESERVA)
            handler.handle("", numero_telefono, sesiones_usuarios)

        except ValueError as e:
            print(Fore.RED + f"\nERROR FACTORY:\t " + Fore.WHITE + f"{e}\n")
        except Exception as e:
            print(Fore.RED + f"\nERROR DB:\t " + Fore.WHITE + f"{e}\n")
            mensaje = msg.ERROR_GENERICO
            response = wpp_resp.mensaje_texto(numero_telefono, mensaje)
            enviar_mensaje_whatsapp(response)
