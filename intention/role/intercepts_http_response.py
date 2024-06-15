from typing import Any, Type

from ..httpfoundation import Response
from .intercepts_http_response_wrapped import intercepts_http_response_wrapped
from .role_builder import RoleBuilder


class intercepts_http_response(RoleBuilder[intercepts_http_response_wrapped]):
    def __init__(
        self,
        response_cls: Type[Response],
    ) -> None:
        RoleBuilder.__init__(self)

        self.response_cls = response_cls

    def wrap_with_role(self, cls: Type[Any]) -> intercepts_http_response_wrapped:
        return intercepts_http_response_wrapped(
            classname=cls,
            response_cls=self.response_cls,
        )
