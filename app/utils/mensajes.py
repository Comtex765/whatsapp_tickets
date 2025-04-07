BIENVENIDA = "👋 ¡Hola, bienvenido a RIOSOFT369! 🎟️\nPara comenzar con tu compra de boletos, por favor digita tu número de cédula:"

CEDULA_OK = "✅ Cédula recibida. \nAhora, ingresa tu *Nombre* y *Apellido* (Ejemplo: Juan Pérez):"
CEDULA_ERROR = "❌ Cédula *no válida*. Asegúrate de ingresar 10 dígitos numéricos."
CEDULA_NO_VALIDA = "❌ Cédula *no válida*. Revisa tu número de cédula"

NOMBRE_APELLIDO_ERROR = (
    "❌ Por favor, ingresa tu Nombre y Apellido juntos (Ejemplo: Juan Pérez)."
)

ERROR_GENERICO = "⚠️ Ocurrió un error. Por favor, intenta nuevamente."

FECHA_NACIMIENTO_SOLICITUD = "📅 Por favor, ingresa tu *fecha de nacimiento* en formato *DD/MM/AAAA* (Ejemplo: 15/07/1995)."
FECHA_NACIMIENTO_ERROR = (
    "❌ Fecha no válida. Asegúrate de usar el formato *DD/MM/AAAA*."
)
CORREO_SOLICITUD = "📧 Por favor, ingresa tu correo electrónico."
CORREO_ERROR = "❌ El correo ingresado no es válido. Intenta nuevamente."


DIRECCION_SOLICITUD = (
    "🏠 Ahora, ingresa tu *dirección* (Ejemplo: Guayaquil y Pichincha, Riobamba)."
)

TICKETS_SOLICITUD = (
    "🎟️ ¿Cuántos *tickets* te gustaría comprar?\nCada ticket cuesta *$2*.\n"
    "Por favor, ingresa el número de tickets que deseas adquirir."
)

TICKETS_CANTIDAD_ERROR = "❌ Por favor, ingresa un número válido de tickets (mínimo 1)."


def mensaje_confirmacion_tickets(cantidad: int, total: float):
    return f"✅ Has seleccionado {cantidad} ticket(s).\n 💵 Total a pagar: ${total}\n\nEs correcto?"


def mensaje_registro_completado(user):
    return f"🎉 ¡Registro completado, {user["nombre"]} {user["apellido"]}! 🎟️\nAhora comencemos con tu compra. 🚀"


def edicion_datos_registro(datos):
    return (
        f"📝 *Por favor confirma tus datos:*\n\n"
        f"👤 *\tNombre:* {datos.get('nombre')} {datos.get('apellido')}\n"
        f"🪪 *\tCédula:* {datos.get('cedula')}\n"
        f"📅 *\tFecha de nacimiento:* {datos.get('fecha_nacimiento')}\n"
        f"📧 *\tCorreo:* {datos.get('correo')}\n"
        f"🏠 *\tDirección:* {datos.get('direccion')}\n\n"
        f"¿Están correctos estos datos?"
    )
