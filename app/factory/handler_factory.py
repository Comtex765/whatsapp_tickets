import utils.constantes.estados as est
from handlers.inicio_handler import InicioHandler
from handlers.pago_handler import PagoHandler
from handlers.registro_handler import RegistroHandler
from handlers.reserva_handler import ReservaHandler


class HandlerFactory:
    @staticmethod
    def get_handler(fase):
        if fase == est.FASE_INICIO_MSG:
            return InicioHandler()
        elif fase == est.FASE_REGISTRO:
            return RegistroHandler()
        elif fase == est.FASE_RESERVA:
            return ReservaHandler()
        elif fase == est.FASE_PAGO:
            return PagoHandler()
        else:
            raise ValueError(f"Fase no soportada: {fase}")
