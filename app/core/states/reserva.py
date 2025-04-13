import utils.whatsapp.responses as wpp_resp
from colorama import Fore, init
from utils.constantes import estados as est
from utils.constantes import id_interactivos
from utils.constantes import mensajes as msg
from utils.validaciones import validar_usuario_existe
from utils.whatsapp.sender import enviar_mensaje_whatsapp

init(autoreset=True)  # Esto hace que después de cada print, se reinicie el color


class InicioReserva:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        # Estado de inicio de reserva, esperando número de tickets
        cedula = sesiones_usuarios[numero_telefono]["datos"]["cedula"]
        user_db = validar_usuario_existe(cedula)

        if user_db:
            sesiones_usuarios[numero_telefono]["estado"] = est.ESPERANDO_NUM_TICKETS
            sesiones_usuarios[numero_telefono]["datos"] = user_db

            mensaje = msg.mensaje_tickets_solicitud(
                sesiones_usuarios[numero_telefono]["datos"]["nombre"]
            )
            response = wpp_resp.mensaje_texto(numero_telefono, mensaje)
            enviar_mensaje_whatsapp(response)
        else:
            # Confirmación y cambio de fase
            sesiones_usuarios[numero_telefono]["fase"] = est.FASE_REGISTRO
            sesiones_usuarios[numero_telefono]["estado"] = est.INICIO_REGISTRO

            mensaje = msg.USUARIO_NO_EXISTE
            response = wpp_resp.mensaje_texto(numero_telefono, mensaje)
            enviar_mensaje_whatsapp(response)
            try:
                from core.factory.handler_factory import HandlerFactory

                handler = HandlerFactory.get_handler(est.FASE_REGISTRO)
                handler.handle("", numero_telefono, sesiones_usuarios)
            except ValueError as e:
                print(Fore.RED + f"\nERROR FACTORY:\t " + Fore.WHITE + f"{e}\n")


class EsperandoNumTickets:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        # Esperando número de tickets
        if texto.isdigit() and int(texto) > 0:
            cantidad = int(texto)
            total = cantidad * 2  # cada ticket cuesta $2

            # Guardar en sesión
            sesiones_usuarios[numero_telefono]["datos"]["num_tickets"] = cantidad
            sesiones_usuarios[numero_telefono]["datos"]["total_pago"] = total

            # Actualizar estado para confirmar el número correcto de tickets y el monto
            sesiones_usuarios[numero_telefono]["estado"] = est.CONFIRMAR_NUM_TICKETS

            mensaje = msg.mensaje_confirmacion_tickets(cantidad, total)
            response = wpp_resp.mensaje_botones_interactivos(
                numero_telefono,
                mensaje,
                id_opc_1=id_interactivos.ID_NUM_TICKETS_SI,
                id_opc_2=id_interactivos.ID_NUM_TICKETS_NO,
            )

            enviar_mensaje_whatsapp(response)
        else:
            mensaje = msg.OPCION_NO_VALIDA
            response = wpp_resp.mensaje_texto(numero_telefono, mensaje)
            enviar_mensaje_whatsapp(response)

            mensaje = msg.mensaje_tickets_solicitud(
                sesiones_usuarios[numero_telefono]["datos"]["nombre"]
            )
            response = wpp_resp.mensaje_texto(numero_telefono, mensaje)
            enviar_mensaje_whatsapp(response)


class ConfirmarNumTickets:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        # Confirmando el número de tickets
        if id_interactivos.ID_NUM_TICKETS_SI in texto:
            # Confirmación y cambio de fase
            sesiones_usuarios[numero_telefono]["fase"] = est.FASE_PAGO
            sesiones_usuarios[numero_telefono]["estado"] = est.INICIO_PAGO

        elif id_interactivos.ID_NUM_TICKETS_NO in texto:
            sesiones_usuarios[numero_telefono]["estado"] = est.ESPERANDO_NUM_TICKETS
            mensaje = msg.mensaje_tickets_solicitud(
                sesiones_usuarios[numero_telefono]["datos"]["nombre"]
            )
            response = wpp_resp.mensaje_texto(numero_telefono, mensaje)
            enviar_mensaje_whatsapp(response)
