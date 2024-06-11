from typing import Type, Union

from .responds_to_http_wrapped import responds_to_http_wrapped
from .role_builder import RoleBuilder


class responds_to_http(RoleBuilder):
    def __init__(
        self,
        pattern: str,
        method: str = "get",
        description: Union[None, str] = None,
        name: Union[None, str] = None,
    ):
        RoleBuilder.__init__(self)

        self.description = description
        self.method = method
        self.name = name
        self.pattern = pattern

    def wrap_with_role(self, cls: Type):
        return responds_to_http_wrapped(
            classname=cls,
            description=self.description,
            method=self.method,
            name=self.name,
            pattern=self.pattern,
        )
