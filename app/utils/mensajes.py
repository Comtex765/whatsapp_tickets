# mensajes.py

BIENVENIDA = "👋 ¡Hola, bienvenido a RIOSOFT369! 🎟️\nPara comenzar con tu compra de boletos, por favor digita tu número de cédula:"

CEDULA_OK = (
    "✅ Cédula recibida. \nAhora, ingresa tu *Nombre* y *Apellido* (Ejemplo: Juan Pérez):"
)
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
DIRECCION_SOLICITUD = (
    "🏠 Ahora, ingresa tu *dirección* (Ejemplo: Guayaquil y Pichincha, Riobamba)."
)


def mensaje_registro_completado(user):
    return f"🎉 ¡Registro completado, {user["nombre"]} {user["apellido"]}! 🎟️\n\nTu compra está en proceso. 🚀"
