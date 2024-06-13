from typing import Type

from ..httpfoundation.response import Response
from .service import service


class intercepts_http_response_wrapped(service):
    def __init__(
        self,
        classname: Type,
        response_cls: Type[Response],
    ):
        service.__init__(self, classname)

        self.response_cls = response_cls
