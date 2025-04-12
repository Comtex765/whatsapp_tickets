import config
import models as mod
from colorama import Fore
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = config.SQLALCHEMY_DATABASE_URI

# Crear motor y sesión
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Crear usuario
def crear_usuario(data: dict):
    session = SessionLocal()
    try:
        if existe_usuario_por_cedula(data["cedula"], session):
            print("⚠️ Ya existe un usuario con ese número de teléfono.")
            return None

        session.add(mod.Usuario(**data))
        session.commit()

        print("✅ Usuario creado")
    except Exception as e:
        session.rollback()
        print("❌ Error al crear usuario:", e)
    finally:
        session.close()


# Función para guardar el registro en la base de datos
def guardar_comprobante(data: dict):
    # Crear una nueva sesión de base de datos
    session = SessionLocal()

    # Crear un nuevo objeto de RegistroDB
    nuevo_registro = mod.Transferencia(
        comprobante=data["comprobante"],
        monto=data["monto"],
        fecha=data["fecha"],
    )

    # Añadir el nuevo registro a la sesión
    session.add(nuevo_registro)

    # Confirmar la transacción
    session.commit()
    session.refresh(nuevo_registro)  # Obtener el objeto actualizado

    return nuevo_registro


# Buscar usuario por número de teléfono
def existe_usuario_por_cedula(cedula: str, session=None):
    session = SessionLocal()

    try:
        usuario = session.query(mod.Usuario).filter_by(cedula=cedula).first()

        print(f"el usuario es {usuario}")

        return usuario is not None
    finally:
        session.close()


def obtener_usuario_por_cedula(cedula: str, session=None):
    session = SessionLocal()

    try:
        usuario = session.query(mod.Usuario).filter_by(cedula=cedula).first()
        if usuario:
            return {
                "cedula": usuario.cedula,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "correo": usuario.correo,
                "fecha_nacimiento": (
                    usuario.fecha_nacimiento.isoformat()
                    if usuario.fecha_nacimiento
                    else None
                ),
                "direccion": usuario.direccion,
            }
        return None
    except Exception as e:
        print(
            Fore.RED
            + "\nERROR OBTENER USUARIO POR NUM TELEFONO:"
            + Fore.WHITE
            + f"\t{e}\n"
        )
    finally:
        session.close()


# Función para verificar si existe un registro de transferencia por el comprobante
def existe_transferencia_por_comprobante(comprobante: str):
    session = SessionLocal()

    try:
        # Consultar la base de datos buscando una transferencia con el comprobante dado
        transferencia = (
            session.query(mod.Transferencia).filter_by(comprobante=comprobante).first()
        )

        print(f"la transrferencia es {transferencia}")
        # Si se encuentra un registro, devuelve True (existe)
        return transferencia is not None
    except Exception as e:
        print(f"---> {e}")
    finally:
        session.close()
