from typing import Any, List, Optional, Type

from ..cli.command_option import CommandOption
from .responds_to_cli_wrapped import responds_to_cli_wrapped
from .role_builder import RoleBuilder


class responds_to_cli(RoleBuilder[responds_to_cli_wrapped]):
    def __init__(
        self,
        name: str,
        options: List[CommandOption[Any]] = [],
        description: Optional[str] = None,
    ) -> None:
        RoleBuilder.__init__(self)

        self.description = description
        self.name = name
        self.options = options

    def wrap_with_role(self, cls: Type[Any]) -> responds_to_cli_wrapped:
        return responds_to_cli_wrapped(
            classname=cls,
            description=self.description,
            name=self.name,
            options=self.options,
        )
