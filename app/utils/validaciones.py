import re
from datetime import datetime

import database as db


def validar_pago(data_img: dict, fecha_esperada: bool = True) -> bool:
    monto_valido = data_img.get("monto") != "-1"

    if fecha_esperada:
        # Valida que la fecha coincida con la de hoy
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        fecha_valida = data_img.get("fecha") == fecha_actual
    else:
        # Solo verifica que haya una fecha válida
        fecha_valida = True

    return monto_valido and fecha_valida


def validar_cedula(cedula: str) -> bool:
    """Valida si una cédula ecuatoriana es correcta."""
    if not cedula.isdigit() or len(cedula) != 10:
        return False  # Debe tener solo números y ser de 10 dígitos

    provincia = int(cedula[:2])  # Los dos primeros dígitos
    tercer_digito = int(cedula[2])  # El tercer dígito

    if provincia < 1 or provincia > 24:  # Verificar si la provincia es válida
        return False

    if (
        tercer_digito < 0 or tercer_digito > 6
    ):  # Verificar que el tercer dígito esté en el rango correcto
        return False

    # Algoritmo de verificación (Módulo 10)
    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]  # Pesos usados en el cálculo
    suma = 0

    for i in range(9):
        valor = int(cedula[i]) * coeficientes[i]
        if valor >= 10:
            valor -= 9  # Restar 9 si el valor es mayor o igual a 10
        suma += valor

    digito_verificador = (10 - (suma % 10)) % 10  # Cálculo del dígito verificador

    return digito_verificador == int(cedula[9])  # Comparar con el último dígito


def validar_fecha_nacimiento(fecha: str) -> bool:
    """Valida que la fecha tenga formato DD/MM/AAAA y que la persona tenga al menos 15 años."""
    try:
        if not re.match(r"^\d{2}/\d{2}/\d{4}$", fecha):
            return False

        fecha_nac = datetime.strptime(fecha, "%d/%m/%Y")
        hoy = datetime.today()
        edad = (
            hoy.year
            - fecha_nac.year
            - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
        )

        return edad >= 15
    except ValueError:
        return False


def validar_correo(correo: str) -> bool:
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(patron, correo) is not None


def validar_usuario_existe(cedula: str):
    return db.obtener_usuario_por_cedula(cedula)
