from typing import Any, List, Optional

from ..cli_foundation.command_option import CommandOption
from .service import service


class responds_to_cli(service):
    name: str
    options: List[CommandOption[Any]] = []
    description: Optional[str] = None
