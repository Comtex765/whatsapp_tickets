import json

from database import db
from models import Log


def agregar_mensajes_log(texto):
    texto_str = json.dumps(texto, ensure_ascii=False)
    nuevo_registro = Log(texto=texto_str)
    db.session.add(nuevo_registro)
    db.session.commit()
