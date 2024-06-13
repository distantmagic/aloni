from typing import Tuple
from .role.role import Role


class ServiceColletion:
    def __init__(self, services: set[Tuple[Role, object]]):
        self.services = services

    def __iter__(self):
        return iter(self.services)
