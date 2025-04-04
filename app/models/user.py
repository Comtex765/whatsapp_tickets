from pydantic import BaseModel, Field
from datetime import datetime
import pytz


# Obtener la hora actual en UTC-5
def obtener_hora_registro():
    return datetime.now(pytz.timezone("America/Guayaquil"))


class UsuarioRegistro(BaseModel):
    cedula: str
    nombre: str
    apellido: str
    fecha_nacimiento: str
    direccion: str
    hora_registro: datetime = Field(default_factory=obtener_hora_registro)

    class Config:
        # Asegura que las fechas se serialicen correctamente en formato ISO
        json_encoders = {datetime: lambda v: v.isoformat()}
