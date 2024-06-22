from typing import Any, Type


class FunctionParameter:
    def __init__(
        self,
        name: str,
        annotation: Type[Any],
    ) -> None:
        self.annotation = annotation
        self.name = name
