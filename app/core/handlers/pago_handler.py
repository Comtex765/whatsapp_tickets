import core.states.pago as estate
from colorama import Fore, Style
from utils.constantes import estados as est


class PagoHandler:
    estrategias = {
        est.INICIO_PAGO: estate.InicioPago,
        est.ESPERANDO_METODO_PAGO: estate.EsperandoMetodoPago,
        est.ESPERANDO_PAGO_TRANSFERENCIA: estate.EsperandoPagoTransferencia,
        est.ESPERANDO_PAGO_TARJETA: estate.EsperandoPagoTarjeta,
    }

    def handle(self, texto, numero_telefono, sesiones_usuarios):
        try:
            estado = sesiones_usuarios[numero_telefono]["estado"]
            estrategia_class = self.estrategias.get(estado)

            if estrategia_class:
                try:
                    estrategia_class().handle(numero_telefono, texto, sesiones_usuarios)
                except Exception as e:
                    print(
                        Fore.RED
                        + "\nERROR ESTRATEGIA PagoHandler:\t"
                        + Fore.WHITE
                        + f"{e}\n"
                        + Style.RESET_ALL
                    )
            else:
                try:
                    from utils.constantes.mensajes import ERROR_GENERICO
                    from utils.whatsapp import responses as wpp_resp
                    from utils.whatsapp.sender import enviar_mensaje_whatsapp

                    response = wpp_resp.mensaje_texto(numero_telefono, ERROR_GENERICO)
                    enviar_mensaje_whatsapp(response)
                except Exception as e:
                    print(
                        Fore.RED
                        + "\nERROR WHATSAPP FALLBACK EN PagoHandler:\t"
                        + Fore.WHITE
                        + f"{e}\n"
                        + Style.RESET_ALL
                    )

        except Exception as e:
            print(
                Fore.RED
                + "\nERROR GENERAL EN PagoHandler:\t"
                + Fore.WHITE
                + f"{e}\n"
                + Style.RESET_ALL
            )
