import core.states.inicio as estate
from colorama import Fore, Style
from utils.constantes import estados as est


class InicioHandler:
    estrategias = {
        est.INICIO_PRINCIPAL: estate.InicioPrincipal,
        est.ESPERANDO_CEDULA: estate.EsperandoCedula,
        est.ESPERANDO_OPCION_PRINCIPAL: estate.EsperandoOpcionPrincipal,
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
                        + "\nERROR ESTRATEGIA InicioHandler:\t"
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
                        + "\nERROR WHATSAPP FALLBACK EN InicioHandler:\t"
                        + Fore.WHITE
                        + f"{e}\n"
                        + Style.RESET_ALL
                    )

        except Exception as e:
            print(
                Fore.RED
                + "\nERROR GENERAL EN InicioHandler:\t"
                + Fore.WHITE
                + f"{e}\n"
                + Style.RESET_ALL
            )
