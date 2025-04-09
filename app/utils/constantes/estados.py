# -------------------------
# Estados del flujo de registro
# -------------------------

FASE_REGISTRO = "registro"
INICIO_REGISTRO = "inicio_registro"
# Estado inicial del usuario asumido


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

FASE_RESERVA = "reserva"
INICIO_RESERVA = "inicio_reserva"

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

FASE_PAGO = "pago"
INICIO_PAGO = "inicio_pago"

ESPERANDO_PAGO = "esperando_pago"
# Esperando que el usuario realice el pago correspondiente
