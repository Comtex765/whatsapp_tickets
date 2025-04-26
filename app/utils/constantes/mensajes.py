BIENVENIDA = "👋 ¡Hola! 🎟️\nPor favor, ingresa tu número de cédula (sin espacios ni caracteres). Ej: 1234567890"

CEDULA_OK = "✅ Cédula recibida\n"

OPCION_PRINCIPAL_REGISTRO = {
    "title": "Registrarme",
    "description": "Crea una cuenta y empieza a disfrutar de nuestros servicios",
}

OPCION_PRINCIPAL_COMPRA = {
    "title": "Comprar Tickets",
    "description": "Adquiere tickets para usar nuestros simuladores",
}

USUARIO_NO_EXISTE = "⚠️ *Aún no estás registrado.*\nVamos a comenzar tu registro."


NOMBRE_APELLIDO_SOLICITUD = "👤 Ingresa tu *Nombre* y *Apellido* (Ej: Juan Pérez):"

CEDULA_ERROR = "❌ Cédula *inválida*. Debe tener 10 dígitos numéricos."

CEDULA_NO_VALIDA = "❌ Cédula *no válida*. Revisa tu número de cédula."

NOMBRE_APELLIDO_ERROR = "❌ Ingresa tu Nombre y Apellido juntos (Ej: Juan Pérez)."

FECHA_NACIMIENTO_SOLICITUD = (
    "📅 Ingresa tu *fecha de nacimiento* (DD/MM/AAAA). Ej: 15/07/1995"
)

FECHA_NACIMIENTO_ERROR = "❌ Fecha no válida. Usa el formato *DD/MM/AAAA*."

CORREO_SOLICITUD = "📧 Ingresa tu correo electrónico."

CORREO_ERROR = "❌ Correo no válido. Intenta de nuevo."

DIRECCION_SOLICITUD = "🏠 Ingresa tu *dirección* (Ej: Guayaquil y Pichincha, Riobamba)."


TICKETS_CANTIDAD_ERROR = "❌ Ingresa un número válido de tickets (mínimo 1)."


OPCION_NO_VALIDA = "❌ Opción no válida. Selecciona una opción válida."


SELECCION_METODO_PAGO = "💳 Elige tu método de pago."

ERROR_GENERICO = "⚠️ Ocurrió un error. Intenta de nuevo."


PAGO_REALIZADO = "✅ Pago verificado con éxito."

PAGO_NO_COMPROBADO = "❌ No se pudo validar la información del pago. Intenta nuevamente o contacta con soporte"

INACTIVIDAD_USUARIO = "Tu sesión ha expirado por inactividad"

INFORMACION_BANCARIA_PICHINCHA = (
    "🏦 *Pago Banco Pichincha:*\n\n"
    "💳 Cuenta: *# 3339836104*\n"
    "👤 Nombre: *Daniel Jovany Coba Toledo*\n"
    "📧 Correo: *ferchon123443@gmail.com*\n\n"
    "🔔 Registra este correo al hacer el pago y envíanos el comprobante. 📸✅"
)


INFORMACION_LINK_PAGO = (
    "💳 *Pago con Tarjeta (Link de Pago):*\n\n"
    "Haz clic para pagar con tarjeta: 🔗 [Pagar ahora](https://www.youtube.com/watch?v=GStPXGB1kdY&list=RDMM&index=30)\n\n"
    "Después, envíanos el comprobante. 📸✅"
)


def mensaje_tickets_solicitud(nombre: str):
    return f"🎟️ ¿Cuántos *tickets* deseas comprar {nombre}? \nCada uno cuesta *$2*."


def mensaje_confirmacion_tickets(cantidad: int, total: float):
    return f"✅ Seleccionaste {cantidad} ticket(s). \nTotal: *${total}*.\n\n¿Continuar al pago?"


def mensaje_registro_completado(user):
    return f"🎉 ¡Registro completado, {user['nombre']} {user['apellido']}! 🎟️\nVamos a empezar con tu compra."


def edicion_datos_registro(datos: dict):
    return (
        f"📝 *Confirma tus datos:*\n\n"
        f"👤 *Nombre:* {datos.get('nombre')} {datos.get('apellido')}\n"
        f"🪪 *Cédula:* {datos.get('cedula')}\n"
        f"📅 *Fecha de nacimiento:* {datos.get('fecha_nacimiento')}\n"
        f"📧 *Correo:* {datos.get('correo')}\n"
        f"🏠 *Dirección:* {datos.get('direccion')}\n\n"
        "¿Están correctos?"
    )


def usuario_existe(nombre: str):
    return f"🙌 {nombre}, ya estás registrado. \n¡Vamos a comenzar con la compra!"
