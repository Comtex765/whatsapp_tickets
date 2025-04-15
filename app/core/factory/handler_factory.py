import utils.constantes.estados as est
from core.handlers.inicio_handler import InicioHandler
from core.handlers.pago_handler import PagoHandler
from core.handlers.registro_handler import RegistroHandler
from core.handlers.reserva_handler import ReservaHandler


class HandlerFactory:
    handlers = {
        est.FASE_INICIO_MSG: InicioHandler,
        est.FASE_REGISTRO: RegistroHandler,
        est.FASE_RESERVA: ReservaHandler,
        est.FASE_PAGO: PagoHandler,
    }

    @staticmethod
    def get_handler(fase):
        handler_class = HandlerFactory.handlers.get(fase)

        if not handler_class:
            raise ValueError(f"Fase no soportada: {fase}")
        return handler_class()
