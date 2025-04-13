from colorama import Fore, Style
from utils import validaciones as check
from utils.constantes import estados as est
from utils.constantes import id_interactivos
from utils.constantes import mensajes as msg
from utils.whatsapp import responses as wpp_resp
from utils.whatsapp.sender import enviar_mensaje_whatsapp


class InicioPrincipal:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        try:
            mensaje = msg.BIENVENIDA
            sesiones_usuarios[numero_telefono]["estado"] = est.ESPERANDO_CEDULA

            response = wpp_resp.mensaje_texto(numero_telefono, mensaje)
            enviar_mensaje_whatsapp(response)

        except Exception as e:
            print(
                Fore.RED
                + "\n[ERROR InicioPrincipal.handle] → "
                + Fore.WHITE
                + f"{e}\n"
                + Style.RESET_ALL
            )


class EsperandoCedula:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        try:
            texto = texto.strip()

            if texto.isdigit() and len(texto) == 10:
                if check.validar_cedula(texto):
                    sesiones_usuarios[numero_telefono]["datos"]["cedula"] = texto
                    sesiones_usuarios[numero_telefono][
                        "estado"
                    ] = est.ESPERANDO_OPCION_PRINCIPAL

                    mensaje = msg.CEDULA_OK
                    response1 = wpp_resp.mensaje_texto(numero_telefono, mensaje)
                    enviar_mensaje_whatsapp(response1)

                    response2 = wpp_resp.mensaje_lista_inicio(numero_telefono)
                    enviar_mensaje_whatsapp(response2)
                    return
                else:
                    mensaje = msg.CEDULA_NO_VALIDA
            else:
                mensaje = msg.CEDULA_ERROR

            response = wpp_resp.mensaje_texto(numero_telefono, mensaje)
            enviar_mensaje_whatsapp(response)

        except Exception as e:
            print(
                Fore.RED
                + "\n[ERROR EsperandoCedula.handle] → "
                + Fore.WHITE
                + f"{e}\n"
                + Style.RESET_ALL
            )


class EsperandoOpcionPrincipal:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        try:
            from core.factory.handler_factory import HandlerFactory

            texto = texto.strip().lower()

            if id_interactivos.ID_LISTA_REGISTRO in texto:
                sesiones_usuarios[numero_telefono]["fase"] = est.FASE_REGISTRO
                sesiones_usuarios[numero_telefono]["estado"] = est.INICIO_REGISTRO

                print(Fore.CYAN + "[INFO] Fase de registro iniciada" + Style.RESET_ALL)

                try:
                    handler = HandlerFactory.get_handler(est.FASE_REGISTRO)
                    handler.handle("", numero_telefono, sesiones_usuarios)
                except Exception as e:
                    print(
                        Fore.RED
                        + "\n[ERROR FASE_REGISTRO - HandlerFactory] → "
                        + Fore.WHITE
                        + f"{e}\n"
                        + Style.RESET_ALL
                    )

            elif id_interactivos.ID_LISTA_COMPRA_TICKETS in texto:
                sesiones_usuarios[numero_telefono]["fase"] = est.FASE_RESERVA
                sesiones_usuarios[numero_telefono]["estado"] = est.INICIO_RESERVA

                print(Fore.CYAN + "[INFO] Fase de reserva iniciada" + Style.RESET_ALL)

                try:
                    handler = HandlerFactory.get_handler(est.FASE_RESERVA)
                    handler.handle("", numero_telefono, sesiones_usuarios)
                except Exception as e:
                    print(
                        Fore.RED
                        + "\n[ERROR FASE_RESERVA - HandlerFactory] → "
                        + Fore.WHITE
                        + f"{e}\n"
                        + Style.RESET_ALL
                    )

            else:
                mensaje = msg.OPCION_NO_VALIDA

                response1 = wpp_resp.mensaje_texto(numero_telefono, mensaje)
                enviar_mensaje_whatsapp(response1)

                response2 = wpp_resp.mensaje_lista_inicio(numero_telefono)
                enviar_mensaje_whatsapp(response2)

        except Exception as e:
            print(
                Fore.RED
                + "\n[ERROR EsperandoOpcionPrincipal.handle] → "
                + Fore.WHITE
                + f"{e}\n"
                + Style.RESET_ALL
            )
