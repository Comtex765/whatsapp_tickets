from colorama import Fore, Style
from utils.constantes import estados as est
from utils.constantes import id_interactivos
from utils.constantes import mensajes as msg
from utils.whatsapp import responses as wpp_resp
from utils.whatsapp.sender import enviar_mensaje_whatsapp


class InicioPago:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        try:
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

            print(
                Fore.CYAN
                + f"[INFO] Estado actualizado a ESPERANDO_METODO_PAGO para {numero_telefono}"
                + Style.RESET_ALL
            )

        except Exception as e:
            print(Fore.RED + f"\n[ERROR InicioPago.handle] → {e}\n" + Style.RESET_ALL)


class EsperandoMetodoPago:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        try:
            texto = texto.strip().lower()

            if id_interactivos.ID_PAGO_TRANSFERENCIA in texto:
                sesiones_usuarios[numero_telefono][
                    "estado"
                ] = est.ESPERANDO_PAGO_TRANSFERENCIA
                mensaje = msg.INFORMACION_BANCARIA_PICHINCHA
                print(
                    Fore.CYAN
                    + f"[INFO] Estado actualizado a ESPERANDO_PAGO_TRANSFERENCIA para {numero_telefono}"
                    + Style.RESET_ALL
                )

            elif id_interactivos.ID_PAGO_TARJETA in texto:
                sesiones_usuarios[numero_telefono][
                    "estado"
                ] = est.ESPERANDO_PAGO_TARJETA
                mensaje = msg.INFORMACION_LINK_PAGO
                print(
                    Fore.CYAN
                    + f"[INFO] Estado actualizado a ESPERANDO_PAGO_TARJETA para {numero_telefono}"
                    + Style.RESET_ALL
                )

                response_data = wpp_resp.mensaje_texto(numero_telefono, mensaje, True)
                enviar_mensaje_whatsapp(response_data)
                return

            else:
                mensaje = msg.OPCION_NO_VALIDA
                print(
                    Fore.YELLOW
                    + f"[WARN] Opción de pago no válida recibida: {texto}"
                    + Style.RESET_ALL
                )

            response_data = wpp_resp.mensaje_texto(numero_telefono, mensaje)
            enviar_mensaje_whatsapp(response_data)

        except Exception as e:
            print(
                Fore.RED
                + f"\n[ERROR EsperandoMetodoPago.handle] → {e}\n"
                + Style.RESET_ALL
            )


class EsperandoPagoTransferencia:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        try:
            # Obtener los datos de la imagen (comprobante)
            from os import getenv

            # Verificar si la transferencia con ese comprobante existe
            from database import existe_transferencia_por_comprobante
            from utils.requests import obtener_data_img
            from utils.validaciones import validar_pago

            # Obtener el token de WhatsApp Cloud
            WHATSAPP_CLOUD_TOKEN = getenv("WHATSAPP_CLOUD_TOKEN")

            # Obtener los datos de la imagen (comprobante de transferencia)
            monto = sesiones_usuarios[numero_telefono]["datos"]["total_pago"]
            datos_img = obtener_data_img(
                texto, WHATSAPP_CLOUD_TOKEN, numero_telefono, monto
            )

            comprobante = datos_img.get("comprobante", None)

            if comprobante:
                print(
                    Fore.CYAN
                    + f"[INFO] Comprobante recibido para {numero_telefono}: {comprobante}"
                    + Style.RESET_ALL
                )
            else:
                print(
                    Fore.YELLOW
                    + f"[WARN] No se encontró un comprobante en los datos de la imagen para {numero_telefono}"
                    + Style.RESET_ALL
                )

            # Verificar si la transferencia con ese comprobante existe
            if validar_pago(data_img=datos_img, fecha_esperada=False):
                mensaje = msg.PAGO_REALIZADO
                print(
                    Fore.GREEN
                    + f"[INFO] Transferencia validada con éxito para {numero_telefono}"
                    + Style.RESET_ALL
                )
            else:
                mensaje = msg.NO_EXISTE_COMPROBANTE
                print(
                    Fore.RED
                    + f"[ERROR] Comprobante no encontrado en la base de datos para {numero_telefono}"
                    + Style.RESET_ALL
                )

                # Si no existe el comprobante, se pide nuevamente la información bancaria
                response_data = wpp_resp.mensaje_texto(numero_telefono, mensaje)
                enviar_mensaje_whatsapp(response_data)

                mensaje = msg.INFORMACION_BANCARIA_PICHINCHA

            # Enviar respuesta final
            response_data = wpp_resp.mensaje_texto(numero_telefono, mensaje)
            enviar_mensaje_whatsapp(response_data)

            # Actualizar estado del usuario
            sesiones_usuarios[numero_telefono]["estado"] = est.ESPERANDO_PAGO_TARJETA

        except Exception as e:
            print(
                Fore.RED
                + f"\n[ERROR EsperandoPagoTransferencia.handle] → {e}\n"
                + Style.RESET_ALL
            )


class EsperandoPagoTarjeta:
    def handle(self, numero_telefono, texto, sesiones_usuarios):
        try:
            # Enviar mensaje confirmando que el pago fue recibido correctamente
            mensaje = msg.PAGO_REALIZADO
            response_data = wpp_resp.mensaje_texto(numero_telefono, mensaje)
            enviar_mensaje_whatsapp(response_data)

            # Agregar la lógica para validar la confirmación del pago como revisar el estado de una transacción

            print(
                Fore.GREEN
                + f"[INFO] Pago de tarjeta confirmado para {numero_telefono}"
                + Style.RESET_ALL
            )

            # Actualizar estado del usuario
            sesiones_usuarios[numero_telefono]["estado"] = est.FIN_PAGO

            # Enviar mensaje final de éxito o próximos pasos si es necesario
            mensaje_final = msg.PAGO_EXITOSO
            response_data_final = wpp_resp.mensaje_texto(numero_telefono, mensaje_final)
            enviar_mensaje_whatsapp(response_data_final)

        except Exception as e:
            print(
                Fore.RED
                + f"\n[ERROR EsperandoPagoTarjeta.handle] → {e}\n"
                + Style.RESET_ALL
            )
            # Respuesta en caso de error
            mensaje_error = msg.ERROR_PAGO
            response_data_error = wpp_resp.mensaje_texto(numero_telefono, mensaje_error)
            enviar_mensaje_whatsapp(response_data_error)

            # Actualizar estado para manejar el error de manera adecuada
            sesiones_usuarios[numero_telefono]["estado"] = est.ERROR_PAGO
