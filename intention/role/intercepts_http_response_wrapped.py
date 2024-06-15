from typing import Any, Type

from ..httpfoundation.response import Response
from .service import service


class intercepts_http_response_wrapped(service):
    def __init__(
        self,
        classname: Type[Any],
        response_cls: Type[Response],
    ) -> None:
        service.__init__(self, classname)

        self.response_cls = response_cls
