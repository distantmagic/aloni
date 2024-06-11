from typing import Type

from .role import Role


def get_root_class(role) -> Type:
    if isinstance(role, Role):
        return get_root_class(role.classname)

    return role
