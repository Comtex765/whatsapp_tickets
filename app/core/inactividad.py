from datetime import datetime, timedelta
from utils.whatsapp.sender import enviar_mensaje_whatsapp
import utils.constantes.estados as est
import asyncio
from utils.session import sesiones_usuarios

TIEMPO_INACTIVIDAD_MINUTOS = 10


async def verificar_sesiones_inactivas():
    # Revisa periódicamente las sesiones de usuarios y reinicia las inactivas.
    while True:
        try:
            ahora = datetime.now()
            inactivos = []

            for numero, sesion in list(sesiones_usuarios.items()):
                ultima_fecha = sesion.get("ultimo_mensaje", ahora)
                if ahora - ultima_fecha > timedelta(minutes=TIEMPO_INACTIVIDAD_MINUTOS):
                    inactivos.append(numero)

            for numero in inactivos:
                print(f"⏱️ Reiniciando sesión por inactividad: {numero}")
                del sesiones_usuarios[numero]

                await enviar_mensaje_whatsapp(
                    {
                        "messaging_product": "whatsapp",
                        "to": numero,
                        "type": "text",
                        "text": {
                            "body": "Tu sesión ha expirado por inactividad. Empezaremos de nuevo 🕒"
                        },
                    }
                )

            await asyncio.sleep(60)  # Espera 60 segundos antes de volver a verificar
        except Exception as e:
            print(f"eerrorrr --> {e}")
