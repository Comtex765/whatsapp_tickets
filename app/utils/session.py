# Este diccionario almacena la sesión activa de cada usuario usando su número de WhatsApp como clave.
# La estructura esperada para cada usuario es:

"""
    sesiones_usuarios = {
        "593xxxxxxxx": {
            "existe": bool                  # Para saber si el usuario ya existe o no en la base de datos y saltarse el registro por defecto
            "fase": "registro",             # Fase actual del usuario: puede ser "registro", "reserva", o "pago"
            "estado": "esperando_cedula",   # Subestado dentro de la fase, usado para guiar el flujo de conversación
            "datos": {}                     # Diccionario donde se almacenan los datos ingresados por el usuario
    }
}"""

sesiones_usuarios = {}
