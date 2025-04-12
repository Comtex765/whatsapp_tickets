import states.registro as estate
from utils.constantes import estados as est


class RegistroHandler:
    def handle(self, texto, numero_telefono, sesiones_usuarios):
        estado = sesiones_usuarios[numero_telefono]["estado"]

        if estado == est.INICIO_REGISTRO:
            estate.InicioRegistro().handle(numero_telefono, texto, sesiones_usuarios)

        elif estado == est.ESPERANDO_NOMBRE_APELLIDO:
            estate.EsperandoNombreApellido().handle(
                numero_telefono, texto, sesiones_usuarios
            )

        elif estado == est.ESPERANDO_FECHA_NACIMIENTO:
            estate.EsperandoFechaNacimiento().handle(
                numero_telefono, texto, sesiones_usuarios
            )

        elif estado == est.ESPERANDO_CORREO:
            estate.EsperandoCorreo().handle(numero_telefono, texto, sesiones_usuarios)

        elif estado == est.ESPERANDO_DIRECCION:
            estate.EsperandoDireccion().handle(
                numero_telefono, texto, sesiones_usuarios
            )

            estado = sesiones_usuarios[numero_telefono]["estado"]

            if estado == est.FIN_REGISTRO:
                estate.FinRegistro().handle(numero_telefono, sesiones_usuarios)

        else:
            # Estado inesperado
            from utils.constantes.mensajes import ERROR_GENERICO
            from utils.whatsapp import responses as wpp_resp
            from utils.whatsapp.sender import enviar_mensaje_whatsapp

            response = wpp_resp.mensaje_texto(numero_telefono, ERROR_GENERICO)
            enviar_mensaje_whatsapp(response)
