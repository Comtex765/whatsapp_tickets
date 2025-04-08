# -------------------------
# Mensajes de bienvenida e inicio
# -------------------------

BIENVENIDA = (
    "👋 ¡Hola, bienvenido a RIOSOFT369! 🎟️\n"
    "Para comenzar con tu compra de boletos, por favor digita tu número de cédula:"
)
# Mensaje de bienvenida inicial al usuario

# -------------------------
# Mensajes del flujo de registro
# -------------------------

# Cédula
CEDULA_OK = "✅ Cédula recibida. \nAhora, ingresa tu *Nombre* y *Apellido* (Ejemplo: Juan Pérez):"
# Confirmación de cédula válida

CEDULA_ERROR = "❌ Cédula *no válida*. Asegúrate de ingresar 10 dígitos numéricos."
# Mensaje de error cuando la cédula no cumple con el formato esperado

CEDULA_NO_VALIDA = "❌ Cédula *no válida*. Revisa tu número de cédula"
# Mensaje genérico de error de cédula

# Nombre y apellido
NOMBRE_APELLIDO_ERROR = (
    "❌ Por favor, ingresa tu Nombre y Apellido juntos (Ejemplo: Juan Pérez)."
)
# Mensaje de error si el usuario no proporciona correctamente nombre y apellido

# Fecha de nacimiento
FECHA_NACIMIENTO_SOLICITUD = "📅 Por favor, ingresa tu *fecha de nacimiento* en formato *DD/MM/AAAA* (Ejemplo: 15/07/1995)."
# Solicitud de fecha de nacimiento al usuario

FECHA_NACIMIENTO_ERROR = (
    "❌ Fecha no válida. Asegúrate de usar el formato *DD/MM/AAAA*."
)
# Mensaje de error por formato de fecha incorrecto

# Correo electrónico
CORREO_SOLICITUD = "📧 Por favor, ingresa tu correo electrónico."
# Solicitud de correo electrónico

CORREO_ERROR = "❌ El correo ingresado no es válido. Intenta nuevamente."
# Mensaje de error si el formato del correo no es válido

# Dirección
DIRECCION_SOLICITUD = (
    "🏠 Ahora, ingresa tu *dirección* (Ejemplo: Guayaquil y Pichincha, Riobamba)."
)
# Solicitud de dirección domiciliaria

# -------------------------
# Mensajes del flujo de reserva
# -------------------------

TICKETS_SOLICITUD = (
    "🎟️ ¿Cuántos *tickets* te gustaría comprar?\n"
    "Cada ticket cuesta *$2*.\n"
    "Por favor, ingresa el número de tickets que deseas adquirir."
)
# Solicitud de cantidad de tickets al usuario

TICKETS_CANTIDAD_ERROR = "❌ Por favor, ingresa un número válido de tickets (mínimo 1)."
# Mensaje de error si el número de tickets es inválido

OPCION_NO_VALIDA = "Por favor selecciona una opción válida"


SELECCION_METODO_PAGO = "Ahora seleccionar tu método de pago."


def mensaje_confirmacion_tickets(cantidad: int, total: float):
    """
    Genera un mensaje para confirmar la cantidad de tickets seleccionados y el total a pagar.

    Args:
        cantidad (int): Número de tickets seleccionados.
        total (float): Monto total a pagar.

    Returns:
        str: Mensaje formateado.
    """
    return (
        f"✅ Has seleccionado {cantidad} ticket(s).\n"
        f"💵 Total a pagar: ${total}\n"
        f"¿Continuar al pago?"
    )


# -------------------------
# Mensajes finales y confirmaciones
# -------------------------


def mensaje_registro_completado(user):
    """
    Genera un mensaje de confirmación cuando el registro se completa con éxito.

    Args:
        user (dict): Diccionario con las claves 'nombre' y 'apellido'.

    Returns:
        str: Mensaje de registro completado.
    """
    return (
        f"🎉 ¡Registro completado, {user['nombre']} {user['apellido']}! 🎟️\n"
        f"Ahora comencemos con tu compra. 🚀"
    )


def edicion_datos_registro(datos):
    """
    Genera un mensaje para confirmar todos los datos ingresados durante el registro.

    Args:
        datos (dict): Diccionario con claves: nombre, apellido, cedula,
                      fecha_nacimiento, correo, direccion.

    Returns:
        str: Mensaje de confirmación de datos.
    """
    return (
        f"📝 *Por favor confirma tus datos:*\n\n"
        f"👤 *\tNombre:* {datos.get('nombre')} {datos.get('apellido')}\n"
        f"🪪 *\tCédula:* {datos.get('cedula')}\n"
        f"📅 *\tFecha de nacimiento:* {datos.get('fecha_nacimiento')}\n"
        f"📧 *\tCorreo:* {datos.get('correo')}\n"
        f"🏠 *\tDirección:* {datos.get('direccion')}\n\n"
        f"¿Están correctos estos datos?"
    )


# -------------------------
# Mensajes generales
# -------------------------

ERROR_GENERICO = "⚠️ Ocurrió un error. Por favor, intenta nuevamente."
# Mensaje de error genérico para cualquier fallo inesperado
