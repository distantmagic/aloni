from typing import Any, List, Optional, Type

from ..cli.command_option import CommandOption
from .service import service


class responds_to_cli_wrapped(service):
    def __init__(
        self,
        classname: Type[Any],
        name: str,
        description: Optional[str],
        options: List[CommandOption[Any]],
    ) -> None:
        service.__init__(self, classname)

        self.options = options
        self.description = description
        self.name = name
