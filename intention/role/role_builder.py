import inspect
from abc import ABC, abstractmethod
from typing import Type

from .get_root_class import get_root_class
from .role import Role


class RoleBuilder(ABC):
    @abstractmethod
    def wrap_with_role(self, cls: Type) -> Role:
        pass

    # decorator can wrap either a class or an object wrapped by a different
    # decorator
    def __call__(self, wrapped):
        if inspect.isclass(wrapped):
            return self.wrap_with_role(wrapped)
        elif isinstance(wrapped, Role):
            return self.wrap_with_role(get_root_class(wrapped))
        else:
            raise Exception("Roles can only wrap classes or other roles.")
