import inspect
from abc import ABC, abstractmethod
from typing import Any, Generic, Type, TypeVar, Union

from .get_root_class import get_root_class
from .role import Role

TRole = TypeVar("TRole", bound=Role[Any])


class RoleBuilder(ABC, Generic[TRole]):
    @abstractmethod
    def wrap_with_role(self, cls: Type[Any]) -> TRole:
        pass

    # decorator can wrap either a class or an object wrapped by a different
    # decorator
    def __call__(self, wrapped: Union[object, Type[Any]]) -> TRole:
        if inspect.isclass(wrapped):
            return self.wrap_with_role(wrapped)
        elif isinstance(wrapped, Role):
            return self.wrap_with_role(get_root_class(wrapped))
        else:
            raise Exception("Roles can only wrap classes or other roles.")
