from typing import Type, Union

from .role import Role


class responds_to_http_wrapped(Role):
    def __init__(
        self,
        classname: Type,
        pattern: str,
        method: str = "get",
        description: Union[None, str] = None,
        name: Union[None, str] = None,
    ):
        Role.__init__(self, classname)

        self.description = description
        self.method = method
        self.name = name
        self.pattern = pattern
