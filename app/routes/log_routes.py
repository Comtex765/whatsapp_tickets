from flask import Blueprint, render_template
from models import Log
from services.log_service import agregar_mensajes_log

log_bp = Blueprint("logs", __name__)


@log_bp.route("/")
def index():
    registros = Log.query.order_by(Log.fecha_y_hora.desc()).all()
    return render_template("index.html", registros=registros)
