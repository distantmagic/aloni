from http import HTTPMethod
from typing import Any, Optional, Type

from .responds_to_http_wrapped import responds_to_http_wrapped
from .role_builder import RoleBuilder


class responds_to_http(RoleBuilder[responds_to_http_wrapped]):
    def __init__(
        self,
        pattern: str,
        method: HTTPMethod = HTTPMethod.GET,
        description: Optional[str] = None,
        name: Optional[str] = None,
    ) -> None:
        RoleBuilder.__init__(self)

        self.description = description
        self.method = method
        self.name = name
        self.pattern = pattern

    def wrap_with_role(self, cls: Type[Any]) -> responds_to_http_wrapped:
        return responds_to_http_wrapped(
            classname=cls,
            description=self.description,
            method=self.method,
            name=self.name,
            pattern=self.pattern,
        )
