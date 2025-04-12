from abc import ABC, abstractmethod


class FaseHandler(ABC):
    @abstractmethod
    def handle(self, texto: str, numero: str, sesiones: dict) -> None:
        pass
