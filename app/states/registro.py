import database as db
import utils.whatsapp.responses as wpp_resp
from colorama import Fore
from utils import validaciones as check
from utils.constantes import estados as est
from utils.constantes import mensajes as msg
from utils.whatsapp.sender import enviar_mensaje_whatsapp


class InicioRegistro:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        # Estado de inicio de registro, esperando nombre y apellido
        cedula = sesiones_usuarios[numero_telefono]["datos"]["cedula"]
        user_db = check.validar_usuario_existe(cedula)

        if user_db:
            sesiones_usuarios[numero_telefono]["fase"] = est.FASE_RESERVA
            sesiones_usuarios[numero_telefono]["estado"] = est.INICIO_RESERVA

            mensaje = msg.usuario_existe(user_db["nombre"])
            sesiones_usuarios[numero_telefono]["datos"] = user_db

            response = wpp_resp.mensaje_texto(numero_telefono, mensaje)

            enviar_mensaje_whatsapp(response)

            try:
                from factory.handler_factory import HandlerFactory

                handler = HandlerFactory.get_handler(est.FASE_RESERVA)
                handler.handle("", numero_telefono, sesiones_usuarios)
            except ValueError as e:
                print(Fore.RED + f"\nERROR FACTORY:\t " + Fore.WHITE + f"{e}\n")
        else:
            mensaje = msg.NOMBRE_APELLIDO_SOLICITUD
            sesiones_usuarios[numero_telefono]["estado"] = est.ESPERANDO_NOMBRE_APELLIDO
            response = wpp_resp.mensaje_texto(numero_telefono, mensaje)
            enviar_mensaje_whatsapp(response)


class EsperandoNombreApellido:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        nombres_apellidos = texto.split(" ", 1)

        if len(nombres_apellidos) < 2:
            mensaje = msg.NOMBRE_APELLIDO_ERROR
        else:
            nombre = nombres_apellidos[0].strip().title()
            apellido = nombres_apellidos[1].strip().title()

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

        response = wpp_resp.mensaje_texto(numero_telefono, mensaje)
        enviar_mensaje_whatsapp(response)


class EsperandoFechaNacimiento:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        if check.validar_fecha_nacimiento(texto):
            sesiones_usuarios[numero_telefono]["datos"]["fecha_nacimiento"] = texto
            sesiones_usuarios[numero_telefono]["estado"] = est.ESPERANDO_CORREO
            mensaje = msg.CORREO_SOLICITUD
        else:
            mensaje = msg.FECHA_NACIMIENTO_ERROR

        response = wpp_resp.mensaje_texto(numero_telefono, mensaje)
        enviar_mensaje_whatsapp(response)


class EsperandoCorreo:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        if check.validar_correo(texto):
            sesiones_usuarios[numero_telefono]["datos"]["correo"] = texto
            sesiones_usuarios[numero_telefono]["estado"] = est.ESPERANDO_DIRECCION
            mensaje = msg.DIRECCION_SOLICITUD
        else:
            mensaje = msg.CORREO_ERROR

        response = wpp_resp.mensaje_texto(numero_telefono, mensaje)
        enviar_mensaje_whatsapp(response)


class EsperandoDireccion:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        sesiones_usuarios[numero_telefono]["datos"]["direccion"] = texto
        sesiones_usuarios[numero_telefono]["estado"] = est.FIN_REGISTRO


class FinRegistro:
    def handle(self, numero_telefono, sesiones_usuarios):
        sesiones_usuarios[numero_telefono]["fase"] = est.FASE_RESERVA
        sesiones_usuarios[numero_telefono]["estado"] = est.INICIO_RESERVA

        new_user = sesiones_usuarios[numero_telefono]["datos"]
        new_user["numero_telefono"] = numero_telefono

        db.crear_usuario(new_user)

        mensaje = msg.mensaje_registro_completado(
            sesiones_usuarios[numero_telefono]["datos"]
        )

        response = wpp_resp.mensaje_texto(numero_telefono, mensaje)
        enviar_mensaje_whatsapp(response)

        try:
            from factory.handler_factory import HandlerFactory

            handler = HandlerFactory.get_handler(est.FASE_RESERVA)
            handler.handle("", numero_telefono, sesiones_usuarios)
        except ValueError as e:
            print(Fore.RED + f"\nERROR FACTORY:\t " + Fore.WHITE + f"{e}\n")
