from typing import Any, Generic, Iterator, Tuple, TypeVar
from .role.role import Role

TRole = TypeVar("TRole", bound=Role[Any])


class ServiceColletion(Generic[TRole]):
    def __init__(self, services: set[Tuple[TRole, object]]):
        self.services = services

    def __iter__(self) -> Iterator[Tuple[TRole, object]]:
        return iter(self.services)
