from typing import Type, Union

from ..http_foundation.response import Response
from .responder import Responder
from .response_interceptor import ResponseInterceptor


class ResponseInterceptorAggregate:
    def __init__(self) -> None:
        self.interceptors: dict[
            Type[Response],
            ResponseInterceptor[Response],
        ] = {}

    def can_intercept(self, response: Response) -> bool:
        return type(response) in self.interceptors

    async def intercept(self, response: Response) -> Union[Responder, Response]:
        interceptor = self.interceptors[type(response)]

        if interceptor is None:
            raise ValueError(f"unable to intercept {response}")

        return await interceptor.intercept(response)
