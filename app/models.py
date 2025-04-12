from pydantic import BaseModel
from sqlalchemy import Column, Date, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

# Declarar base
Base = declarative_base()


class Transferencia(Base):
    __tablename__ = "transferencia"

    comprobante = Column(String, primary_key=True, index=True)
    monto = Column(String)
    fecha = Column(String)


class TransferenciaSch(BaseModel):
    comprobante: str
    monto: str
    fecha: str


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cedula = Column(String(10))
    nombre = Column(String(50))
    apellido = Column(String(50))
    correo = Column(String(100), unique=True)
    numero_telefono = Column(String(15), unique=True)
    fecha_nacimiento = Column(Date)
    direccion = Column(Text)
