from typing import Any, Generator, Set, Tuple, Type, TypeVar

from .role import Role

TRole = TypeVar("TRole")


class RoleRegistry:
    def __init__(self) -> None:
        self.registry: Set[Tuple[Role[Any], Type[Any]]] = set()

    def filter_by_role_class(
        self,
        role_class: Type[TRole],
    ) -> Generator[
        Tuple[TRole, Type[Any]],
        None,
        None,
    ]:
        for role, wrapped_class in self.registry:
            if isinstance(role, role_class):
                yield (role, wrapped_class)

    def register(self, role: Role[Any], wrapped_class: Type[Any]) -> None:
        self.registry.add((role, wrapped_class))
