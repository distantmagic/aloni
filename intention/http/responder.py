from abc import ABC, abstractmethod
from typing import Self, Union

from ..httpfoundation import Request, Response


class Responder(ABC):
    @abstractmethod
    async def respond(self, request: Request) -> Union[Response, Self]:
        pass
