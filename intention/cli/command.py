from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def respond(self) -> int:
        pass
