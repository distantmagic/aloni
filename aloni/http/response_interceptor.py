from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Union

from ..http_foundation.response import Response
from .responder import Responder

TResponse = TypeVar("TResponse", bound=Response)


class ResponseInterceptor(ABC, Generic[TResponse]):
    @abstractmethod
    async def intercept(self, response: TResponse) -> Union[Responder, Response]:
        pass
