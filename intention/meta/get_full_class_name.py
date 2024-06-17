import inspect
from typing import Any


def get_full_class_name(obj: Any) -> str:
    if inspect.isclass(obj):
        return obj.__module__ + "." + obj.__qualname__

    return get_full_class_name(type(obj))
