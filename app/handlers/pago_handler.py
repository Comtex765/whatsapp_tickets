import states.pago as estate
from utils.constantes import estados as est


class PagoHandler:
    def handle(self, texto, numero_telefono, sesiones_usuarios):
        estado = sesiones_usuarios[numero_telefono]["estado"]

        try:
            if estado == est.INICIO_PAGO:
                estate.InicioPago().handle(numero_telefono, texto, sesiones_usuarios)

            elif estado == est.ESPERANDO_METODO_PAGO:
                estate.EsperandoMetodoPago().handle(
                    numero_telefono, texto, sesiones_usuarios
                )

            elif estado == est.ESPERANDO_PAGO_TRANSFERENCIA:
                estate.EsperandoPagoTransferencia().handle(
                    numero_telefono, texto, sesiones_usuarios
                )

            elif estado == est.ESPERANDO_PAGO_TARJETA:
                estate.EsperandoPagoTarjeta().handle(
                    numero_telefono, texto, sesiones_usuarios
                )

            elif estado == est.FIN_PAGO:
                estate.FinalizadoPago().handle(
                    numero_telefono, texto, sesiones_usuarios
                )

            else:
                # Estado inesperado
                from utils.constantes.mensajes import ERROR_GENERICO
                from utils.whatsapp import responses as wpp_resp
                from utils.whatsapp.sender import enviar_mensaje_whatsapp

                response = wpp_resp.mensaje_texto(numero_telefono, ERROR_GENERICO)
                enviar_mensaje_whatsapp(response)

        except Exception as e:
            print(f"\nERROR GESTION PAGO: {e}")
            from utils.constantes.mensajes import ERROR_GENERICO
            from utils.whatsapp import responses as wpp_resp
            from utils.whatsapp.sender import enviar_mensaje_whatsapp

            response = wpp_resp.mensaje_texto(numero_telefono, ERROR_GENERICO)
            enviar_mensaje_whatsapp(response)
