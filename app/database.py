import config
from models.user import Usuario
from sqlalchemy import create_engine
from colorama import Fore
from sqlalchemy.orm import sessionmaker

DATABASE_URL = config.SQLALCHEMY_DATABASE_URI

# Crear motor y sesión
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Crear usuario
def crear_usuario(data: dict):
    session = SessionLocal()
    try:
        if existe_usuario_por_numero_telefono(data["numero_telefono"], session):
            print("⚠️ Ya existe un usuario con ese número de teléfono.")
            return None

        session.add(Usuario(**data))
        session.commit()

        print("✅ Usuario creado")
    except Exception as e:
        session.rollback()
        print("❌ Error al crear usuario:", e)
    finally:
        session.close()


# Buscar usuario por número de teléfono
def existe_usuario_por_numero_telefono(numero_telefono: str, session=None):
    owns_session = False
    if session is None:
        session = SessionLocal()
        owns_session = True

    try:
        usuario = (
            session.query(Usuario).filter_by(numero_telefono=numero_telefono).first()
        )

        print(f"el usuario es {usuario}")

        return usuario is not None
    finally:
        if owns_session:
            session.close()


def obtener_usuario_por_numero_telefono(numero_telefono: str, session=None):
    owns_session = False
    if session is None:
        session = SessionLocal()
        owns_session = True

    try:
        usuario = (
            session.query(Usuario).filter_by(numero_telefono=numero_telefono).first()
        )
        if usuario:
            return {
                "id_usuario": usuario.id_usuario,
                "cedula": usuario.cedula,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "correo": usuario.correo,
                "numero_telefono": usuario.numero_telefono,
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
        if owns_session:
            session.close()
