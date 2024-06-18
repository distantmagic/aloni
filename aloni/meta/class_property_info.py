from typing import Any, Type


class ClassPropertyInfo:
    def __init__(
        self,
        default_value: Any,
        is_default_provided: bool,
        name: str,
        type: Type[Any],
    ) -> None:
        self.default_value = default_value
        self.is_default_provided = is_default_provided
        self.name = name
        self.type = type
