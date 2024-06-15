from abc import ABC, abstractmethod
from typing import Any, Type

from ..role.role import Role


class ServiceCollectionFilter(ABC):
    @abstractmethod
    def should_include(self, role: Role[Any], provided_class: Type[Any]) -> bool:
        pass
