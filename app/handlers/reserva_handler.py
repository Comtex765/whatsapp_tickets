import states.reserva as estate
from utils.constantes import estados as est


class ReservaHandler:
    def handle(self, texto, numero_telefono, sesiones_usuarios):
        estado = sesiones_usuarios[numero_telefono]["estado"]

        if estado == est.INICIO_RESERVA:
            estate.InicioReserva().handle(numero_telefono, texto, sesiones_usuarios)

        elif estado == est.ESPERANDO_NUM_TICKETS:
            estate.EsperandoNumTickets().handle(
                numero_telefono, texto, sesiones_usuarios
            )

        elif estado == est.CONFIRMAR_NUM_TICKETS:
            estate.ConfirmarNumTickets().handle(
                numero_telefono, texto, sesiones_usuarios
            )

        elif estado == est.ESPERANDO_PAGO:
            estate.EsperandoPago().handle(numero_telefono, texto, sesiones_usuarios)

        elif estado == est.FINALIZADO_RESERVA:
            estate.FinalizadoReserva().handle(numero_telefono, texto, sesiones_usuarios)

        else:
            # Estado inesperado
            from utils.constantes.mensajes import ERROR_GENERICO
            from utils.whatsapp import responses as wpp_resp
            from utils.whatsapp.sender import enviar_mensaje_whatsapp

            response = wpp_resp.mensaje_texto(numero_telefono, ERROR_GENERICO)
            enviar_mensaje_whatsapp(response)
