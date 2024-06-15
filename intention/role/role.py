from abc import ABC
from typing import Any, Dict, Generic, Tuple, Type, TypeVar

from .role_regsitry_global import role_registry_global

TWrapped = TypeVar("TWrapped")


class Role(ABC, Generic[TWrapped]):
    def __init__(self, classname: Type[TWrapped]) -> None:
        role_registry_global.register(
            role=self,
            wrapped_class=classname,
        )

        self.classname = classname

    def __call__(
        self,
        *args: Tuple[Any, ...],
        **kwargs: Dict[str, Any],
    ) -> TWrapped:
        return self.classname(*args, **kwargs)
