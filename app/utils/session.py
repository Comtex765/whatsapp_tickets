from colorama import Fore
from datetime import datetime, timedelta
import utils.constantes.estados as est

TIEMPO_INACTIVIDAD_MINUTOS = 1

# Este diccionario almacena la sesión activa de cada usuario usando su número de WhatsApp como clave.
# La estructura esperada para cada usuario es:

"""
sesiones_usuarios = {
    "593xxxxxxxx": {
        "existe": bool,                 # Para saber si el usuario ya existe o no en la base de datos y saltarse el registro por defecto
        "fase": "registro",             # Fase actual del usuario: puede ser "registro", "reserva", o "pago"
        "estado": "esperando_cedula",   # Subestado dentro de la fase, usado para guiar el flujo de conversación
        "datos": {},                    # Diccionario donde se almacenan los datos ingresados por el usuario
        "ultimo_mensaje": datetime,     # Marca de tiempo del último mensaje recibido del usuario
    }
}
"""

sesiones_usuarios = {}


def verificar_inactividad(numero_telefono: str):
    ahora = datetime.now()

    # Si el usuario no tiene registro de tiempo, asumimos que está activo
    if "ultimo_mensaje" not in sesiones_usuarios[numero_telefono]:
        sesiones_usuarios[numero_telefono]["ultimo_mensaje"] = ahora
        return

    ultima_fecha = sesiones_usuarios[numero_telefono]["ultimo_mensaje"]
    inactivo = ahora - ultima_fecha > timedelta(minutes=TIEMPO_INACTIVIDAD_MINUTOS)

    if inactivo:
        print(
            Fore.YELLOW
            + f"\n⏱️ Usuario {numero_telefono} inactivo. Reiniciando conversación.\n"
        )

        sesiones_usuarios[numero_telefono] = {
            "existe": False,
            "fase": "registro",
            "estado": "esperando_cedula",
            "datos": {},
            "ultimo_mensaje": ahora,
        }

        from utils.whatsapp.sender import enviar_mensaje_whatsapp
        from utils.whatsapp.responses import mensaje_texto
        from utils.constantes import mensajes as msg

        mensaje = msg.INACTIVIDAD_USUARIO

        response = mensaje_texto(numero_telefono, mensaje)

        enviar_mensaje_whatsapp(response)


def crear_o_actualizar_sesion(numero_telefono):
    ahora = datetime.now()

    try:
        if numero_telefono not in sesiones_usuarios:
            sesiones_usuarios[numero_telefono] = {
                "existe": False,
                "fase": est.FASE_INICIO_MSG,
                "estado": est.INICIO_PRINCIPAL,
                "datos": {},
                "ultimo_mensaje": ahora,
            }
        else:
            sesiones_usuarios[numero_telefono]["ultimo_mensaje"] = ahora
    except Exception as e:
        print(f"---> {e}")
