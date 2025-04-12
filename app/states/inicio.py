from colorama import Fore
from utils import validaciones as check
from utils.constantes import estados as est
from utils.constantes import id_interactivos
from utils.constantes import mensajes as msg
from utils.whatsapp import responses as wpp_resp
from utils.whatsapp.sender import enviar_mensaje_whatsapp


class InicioPrincipal:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        mensaje = msg.BIENVENIDA
        sesiones_usuarios[numero_telefono]["estado"] = est.ESPERANDO_CEDULA

        response = wpp_resp.mensaje_texto(numero_telefono, mensaje)
        enviar_mensaje_whatsapp(response)


class EsperandoCedula:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
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


class EsperandoOpcionPrincipal:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        from factory.handler_factory import HandlerFactory

        texto = texto.strip().lower()

        if id_interactivos.ID_LISTA_REGISTRO in texto:
            sesiones_usuarios[numero_telefono]["fase"] = est.FASE_REGISTRO
            sesiones_usuarios[numero_telefono]["estado"] = est.INICIO_REGISTRO

            try:
                handler = HandlerFactory.get_handler(est.FASE_REGISTRO)
                handler.handle("", numero_telefono, sesiones_usuarios)
            except ValueError as e:
                print(Fore.RED + f"\nERROR FACTORY:\t " + Fore.WHITE + f"{e}\n")

        elif id_interactivos.ID_LISTA_COMPRA_TICKETS in texto:
            sesiones_usuarios[numero_telefono]["fase"] = est.FASE_RESERVA
            sesiones_usuarios[numero_telefono]["estado"] = est.INICIO_RESERVA

            try:
                handler = HandlerFactory.get_handler(est.FASE_RESERVA)
                handler.handle("", numero_telefono, sesiones_usuarios)
            except ValueError as e:
                print(Fore.RED + f"\nERROR FACTORY:\t " + Fore.WHITE + f"{e}\n")

        else:
            mensaje = msg.OPCION_NO_VALIDA

            response1 = wpp_resp.mensaje_texto(numero_telefono, mensaje)
            enviar_mensaje_whatsapp(response1)

            response2 = wpp_resp.mensaje_lista_inicio(numero_telefono)
            enviar_mensaje_whatsapp(response2)
