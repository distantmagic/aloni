from http import HTTPMethod
from typing import Type, Union

from .service import service


class responds_to_http_wrapped(service):
    def __init__(
        self,
        classname: Type,
        pattern: str,
        method: HTTPMethod,
        description: Union[None, str],
        name: Union[None, str],
    ):
        service.__init__(self, classname)

        self.description = description
        self.method = method
        self.name = name
        self.pattern = pattern
