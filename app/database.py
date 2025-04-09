import config
from models.user import Usuario
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

        return usuario is not None
    finally:
        if owns_session:
            session.close()
