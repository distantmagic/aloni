import inspect
from typing import Any, Type


def get_root_class(role: Any) -> Type[Any]:
    if inspect.isclass(role):
        return role

    if hasattr(role, "classname") and inspect.isclass(role.classname):
        return get_root_class(role.classname)

    raise ValueError(f"unable to get a root class: {role}")
