import inspect
from typing import Any, Type

from .role import Role


def get_root_class(role: Any) -> Type[Any]:
    if isinstance(role, Role):
        return get_root_class(role.classname)

    if inspect.isclass(role):
        return role

    raise ValueError(f"unable to get a root class: {role}")
