from abc import ABC, abstractmethod


class EstadoBase(ABC):
    @abstractmethod
    def next(self, mensaje: str, numero: str, sesion: dict):
        pass
