from abc import ABC, abstractmethod

from ..role.role import Role


class ServiceCollectionFilter(ABC):
    @abstractmethod
    def should_include(self, role: Role, provided_class) -> bool:
        pass
