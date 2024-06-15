from typing import Generic, Optional, Type, TypeVar

TValueType = TypeVar("TValueType")


class CommandOption(Generic[TValueType]):
    def __init__(
        self,
        name: str,
        type: Type[TValueType],
        default: Optional[TValueType] = None,
        required: bool = False,
        help: Optional[str] = None,
    ) -> None:
        self.default = default
        self.help = help
        self.name = name
        self.required = required
        self.type = type
