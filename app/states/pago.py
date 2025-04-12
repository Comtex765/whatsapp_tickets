from utils.constantes import estados as est
from utils.constantes import id_interactivos
from utils.constantes import mensajes as msg
from utils.whatsapp import responses as wpp_resp
from utils.whatsapp.sender import enviar_mensaje_whatsapp


class InicioPago:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        # Enviar mensaje de inicio de pago
        mensaje = msg.SELECCION_METODO_PAGO
        response_data = wpp_resp.mensaje_botones_interactivos(
            numero_telefono,
            mensaje,
            id_opc_1=id_interactivos.ID_PAGO_TRANSFERENCIA,
            id_opc_2=id_interactivos.ID_PAGO_TARJETA,
            titulo_1="Transferencia",
            titulo_2="Tarjeta",
        )
        enviar_mensaje_whatsapp(response_data)
        sesiones_usuarios[numero_telefono]["estado"] = est.ESPERANDO_METODO_PAGO


class EsperandoMetodoPago:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        if id_interactivos.ID_PAGO_TRANSFERENCIA in texto:
            sesiones_usuarios[numero_telefono][
                "estado"
            ] = est.ESPERANDO_PAGO_TRANSFERENCIA
            mensaje = msg.INFORMACION_BANCARIA_PICHINCHA
        elif id_interactivos.ID_PAGO_TARJETA in texto:
            sesiones_usuarios[numero_telefono]["estado"] = est.ESPERANDO_PAGO_TARJETA
            mensaje = msg.INFORMACION_LINK_PAGO
            response_data = wpp_resp.mensaje_texto(numero_telefono, mensaje, True)
            enviar_mensaje_whatsapp(response_data)
            return

        response_data = wpp_resp.mensaje_texto(numero_telefono, mensaje)
        enviar_mensaje_whatsapp(response_data)


class EsperandoPagoTransferencia:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        # Obtener los datos de la imagen (comprobante)
        from os import getenv

        # Verificar si la transferencia con ese comprobante existe
        from database import existe_transferencia_por_comprobante
        from utils.requests import obtener_data_img

        WHATSAPP_CLOUD_TOKEN = getenv("WHATSAPP_CLOUD_TOKEN")

        datos_img = obtener_data_img(texto, WHATSAPP_CLOUD_TOKEN, numero_telefono)
        comprobante = datos_img["comprobante"]

        print(f"\n\nDatos de imagen son {datos_img}\n\n")

        if existe_transferencia_por_comprobante(comprobante):
            mensaje = msg.PAGO_REALIZADO
        else:
            mensaje = msg.NO_EXISTE_COMPROBANTE
            response_data = wpp_resp.mensaje_texto(numero_telefono, mensaje)

            mensaje = msg.INFORMACION_BANCARIA_PICHINCHA

        response_data = wpp_resp.mensaje_texto(numero_telefono, mensaje)
        enviar_mensaje_whatsapp(response_data)
        sesiones_usuarios[numero_telefono]["estado"] = est


class EsperandoPagoTarjeta:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        # Se asume que el mensaje con el link de pago se ha enviado antes
        # Ahora esperar la confirmación de pago, si es necesario
        mensaje = msg.PAGO_REALIZADO
        response_data = wpp_resp.mensaje_texto(numero_telefono, mensaje)
        enviar_mensaje_whatsapp(response_data)
        sesiones_usuarios[numero_telefono]["estado"] = est
