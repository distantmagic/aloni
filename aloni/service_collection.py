from typing import Iterator, Tuple
from .role.role import Role


class ServiceColletion:
    def __init__(self, services: set[Tuple[Role, object]]):
        self.services = services

    def __iter__(self) -> Iterator[Tuple[Role, object]]:
        return iter(self.services)
