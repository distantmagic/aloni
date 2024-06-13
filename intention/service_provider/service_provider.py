from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from ..role.role_registry import RoleRegistry

TProvidedService = TypeVar("TProvidedService")


class ServiceProvider(ABC, Generic[TProvidedService]):
    @abstractmethod
    def provide(self, role_registry: RoleRegistry) -> TProvidedService:
        pass
