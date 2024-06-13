from abc import ABC, abstractmethod
from http import HTTPStatus


class Response(ABC):
    @abstractmethod
    def get_status(self) -> HTTPStatus:
        pass
