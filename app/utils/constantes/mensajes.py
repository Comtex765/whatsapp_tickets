BIENVENIDA = (
    "👋 ¡Hola! 🎟️\n"
    "Para comenzar por favor digita tu número de cédula\n"
    "\n📌 *Tip:* El número de cédula no debe contener espacios ni caracteres que no sean números -> Ej: 1234567890"
)

CEDULA_OK = "✅ Cédula recibida\n"

USUARIO_NO_EXISTE = (
    "⚠️ *Aún no te encuentras registrado para poder continuar con tu compra.*\n\n"
    "📝 Comencemos con tu registro"
)

NOMBRE_APELLIDO_SOLICITUD = "👤 Ingresa tu *Nombre* y *Apellido* (Ejemplo: Juan Pérez):"


CEDULA_ERROR = "❌ Cédula *no válida*\nAsegúrate de ingresar 10 dígitos numéricos"


CEDULA_NO_VALIDA = "❌ Cédula *no válida*\nRevisa tu número de cédula"


NOMBRE_APELLIDO_ERROR = (
    "❌ Por favor, ingresa tu Nombre y Apellido juntos (Ejemplo: Juan Pérez)"
)

FECHA_NACIMIENTO_SOLICITUD = "📅 Por favor, ingresa tu *fecha de nacimiento* en formato *DD/MM/AAAA* (Ejemplo: 15/07/1995)"

FECHA_NACIMIENTO_ERROR = "❌ Fecha no válida\nAsegúrate de usar el formato *DD/MM/AAAA*"

CORREO_SOLICITUD = "📧 Por favor, ingresa tu correo electrónico"

CORREO_ERROR = "❌ El correo ingresado no es válido\nIntenta nuevamente"

DIRECCION_SOLICITUD = (
    "🏠 Ahora, ingresa tu *dirección* (Ejemplo: Guayaquil y Pichincha, Riobamba)"
)

TICKETS_CANTIDAD_ERROR = "❌ Por favor, ingresa un número válido de tickets (mínimo 1)"


OPCION_NO_VALIDA = (
    "❌ *Opción no válida.* Por favor selecciona una opción válida del menú"
)

SELECCION_METODO_PAGO = "💳 *Selecciona tu método de pago* para continuar"


def mensaje_tickets_solicitud(nombre: str):
    return (
        f"🎟️ ¿Cuántos *tickets* te gustaría comprar {nombre}?\n"
        "Cada ticket cuesta *$2*\n"
        "\nPor favor, ingresa el número de tickets que deseas adquirir"
    )


def mensaje_confirmacion_tickets(cantidad: int, total: float):
    """
    Genera un mensaje para confirmar la cantidad de tickets seleccionados y el total a pagar

    Args:
        cantidad (int): Número de tickets seleccionados
        total (float): Monto total a pagar

    Returns:
        str: Mensaje formateado
    """
    return (
        f"✅ Has seleccionado {cantidad} ticket(s)\n"
        f"💵 Total a pagar: ${total}\n"
        f"\n¿Continuar al pago?"
    )


def mensaje_registro_completado(user):
    """
    Genera un mensaje de confirmación cuando el registro se completa con éxito

    Args:
        user (dict): Diccionario con las claves 'nombre' y 'apellido'

    Returns:
        str: Mensaje de registro completado
    """
    return (
        f"🎉 ¡Registro completado, {user['nombre']} {user['apellido']}! 🎟️\n"
        f"Ahora comencemos con tu compra 🚀"
    )


def edicion_datos_registro(datos: dict):
    """
    Genera un mensaje para confirmar todos los datos ingresados durante el registro

    Args:
        datos (dict): Diccionario con claves: nombre, apellido, cedula,
                      fecha_nacimiento, correo, direccion

    Returns:
        str: Mensaje de confirmación de datos
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


def usuario_existe(nombre: str):
    return f"🙌 {nombre}, ya te encuentras registrado. ¡Comencemos con tu proceso de compra! 🎟️"


ERROR_GENERICO = "⚠️ Ocurrió un error Por favor, intenta nuevamente"

INFORMACION_BANCARIA_PICHINCHA = (
    "🏦 *Información para el pago:*\n\n"
    "🏛️ Banco: *Banco Pichincha*\n"
    "💳 Cuenta de ahorros: *# 3339836104*\n"
    "👤 Nombre: *Coba Toledo Daniel Jovany*\n"
    "📧 Correo asociado a la cuenta: *ferchon123443@gmail.com*\n\n"
    "🔔 Por favor, al registrar el contacto de la cuenta bancaria, incluye también este correo.\n"
    "Luego de realizar el depósito, envíanos una foto del comprobante en este chat para confirmar tu compra. 📸✅"
)


INFORMACION_LINK_PAGO = (
    "💳 *Pago con Tarjeta (Link de Pago):*\n\n"
    "Haz clic en el siguiente enlace para realizar tu pago de forma rápida y segura con tarjeta:\n"
    "🔗 [Pagar ahora](https://www.youtube.com/watch?v=GStPXGB1kdY&list=RDMM&index=30)\n\n"
    "Una vez realizado el pago, por favor envíanos una foto del comprobante para confirmar tu compra. 📸✅"
)
