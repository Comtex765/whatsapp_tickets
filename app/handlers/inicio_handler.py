import states.inicio as estate
from utils.constantes import estados as est


class InicioHandler:
    def handle(self, texto, numero_telefono, sesiones_usuarios):
        estado = sesiones_usuarios[numero_telefono]["estado"]

        if estado == est.INICIO_PRINCIPAL:
            estate.InicioPrincipal().handle(numero_telefono, texto, sesiones_usuarios)

        elif estado == est.ESPERANDO_CEDULA:
            estate.EsperandoCedula().handle(numero_telefono, texto, sesiones_usuarios)

        elif estado == est.ESPERANDO_OPCION_PRINCIPAL:
            estate.EsperandoOpcionPrincipal().handle(
                numero_telefono, texto, sesiones_usuarios
            )

        else:
            # Estado inesperado
            from utils.constantes.mensajes import ERROR_GENERICO
            from utils.whatsapp import responses as wpp_resp
            from utils.whatsapp.sender import enviar_mensaje_whatsapp

            response = wpp_resp.mensaje_texto(numero_telefono, ERROR_GENERICO)
            enviar_mensaje_whatsapp(response)
