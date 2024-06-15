from http import HTTPMethod
from typing import Any, Optional, Type

from .service import service


class responds_to_http_wrapped(service):
    def __init__(
        self,
        classname: Type[Any],
        pattern: str,
        method: HTTPMethod,
        description: Optional[str],
        name: Optional[str],
    ) -> None:
        service.__init__(self, classname)

        self.description = description
        self.method = method
        self.name = name
        self.pattern = pattern
