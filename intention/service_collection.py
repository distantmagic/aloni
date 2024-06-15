from typing import Any, Iterator, Tuple
from .role.role import Role


class ServiceColletion:
    def __init__(self, services: set[Tuple[Role[Any], object]]):
        self.services = services

    def __iter__(self) -> Iterator[Tuple[Role[Any], object]]:
        return iter(self.services)
