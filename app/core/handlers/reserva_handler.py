import core.states.reserva as estate
from colorama import Fore, Style
from utils.constantes import estados as est


class ReservaHandler:
    estrategias = {
        est.INICIO_RESERVA: estate.InicioReserva,
        est.ESPERANDO_NUM_TICKETS: estate.EsperandoNumTickets,
        est.CONFIRMAR_NUM_TICKETS: estate.ConfirmarNumTickets,
    }

    def handle(self, texto, numero_telefono, sesiones_usuarios):
        try:
            estado = sesiones_usuarios[numero_telefono]["estado"]
            estrategia_class = self.estrategias.get(estado)

            if estrategia_class:
                try:
                    estrategia_class().handle(numero_telefono, texto, sesiones_usuarios)

                    # Releer el nuevo estado/fase tras ejecutar el handler
                    nueva_fase = sesiones_usuarios[numero_telefono]["fase"]
                    nuevo_estado = sesiones_usuarios[numero_telefono]["estado"]

                    if nueva_fase == est.FASE_PAGO and nuevo_estado == est.INICIO_PAGO:
                        try:
                            from core.handlers.pago_handler import PagoHandler

                            PagoHandler().handle("", numero_telefono, sesiones_usuarios)
                        except Exception as e:
                            print(
                                Fore.RED
                                + "\nERROR AL LLAMAR A PagoHandler DESDE ReservaHandler:\t"
                                + Fore.WHITE
                                + f"{e}\n"
                                + Style.RESET_ALL
                            )

                except Exception as e:
                    print(
                        Fore.RED
                        + "\nERROR EN ESTRATEGIA ReservaHandler:\t"
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
                        + "\nERROR EN WHATSAPP FALLBACK ReservaHandler:\t"
                        + Fore.WHITE
                        + f"{e}\n"
                        + Style.RESET_ALL
                    )

        except Exception as e:
            print(
                Fore.RED
                + "\nERROR GENERAL ReservaHandler:\t"
                + Fore.WHITE
                + f"{e}\n"
                + Style.RESET_ALL
            )
