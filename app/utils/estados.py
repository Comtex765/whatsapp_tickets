# -------------------------
# Estados del flujo de registro
# -------------------------

INICIO = "inicio"
# Estado inicial del usuario, antes de iniciar el proceso de registro

ESPERANDO_CEDULA = "esperando_cedula"
# Esperando que el usuario proporcione su número de cédula

ESPERANDO_NOMBRE_APELLIDO = "esperando_nombre_apellido"
# Esperando que el usuario proporcione su nombre y apellido

ESPERANDO_FECHA_NACIMIENTO = "esperando_fecha_nacimiento"
# Esperando que el usuario proporcione su fecha de nacimiento

ESPERANDO_CORREO = "esperando_correo"
# Esperando que el usuario proporcione su dirección de correo electrónico

ESPERANDO_DIRECCION = "esperando_direccion"
# Esperando que el usuario proporcione su dirección domiciliaria

FIN_REGISTRO = "fin_registro"
# Estado alcanzado una vez finalizado exitosamente el proceso de registro

# -------------------------
# Estados del flujo de reserva de tickets
# -------------------------

RESERVA = "reserva"
# Inicio del flujo de reserva de tickets

ESPERANDO_NUM_TICKETS = "esperando_num_tickets"
# Esperando que el usuario indique la cantidad de tickets que desea reservar

CONFIRMAR_NUM_TICKETS = "confirmar_num_tickets"
# Esperando confirmación del usuario sobre la cantidad de tickets a reservar

ESPERANDO_METODO_PAGO = "esperando_metodo_pago"

CONFIRMAR_PAGO = "confirmar_pago"
# Esperando confirmación del usuario para proceder con el pago

# -------------------------
# Estados del flujo de pago
# -------------------------

PAGO = "pago"
# Inicio del proceso de pago

ESPERANDO_PAGO = "esperando_pago"
# Esperando que el usuario realice el pago correspondiente
