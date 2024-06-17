from abc import ABC
from typeguard import check_type
from typing import Any, Dict, Optional, Self, Type, Union
import inspect

from ..meta.get_class_properties import get_class_properties
from ..meta.get_root_class import get_root_class
from .role_regsitry_global import role_registry_global


class Role(ABC):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.classname: Optional[Type[Any]] = None

        if not kwargs and len(args) == 1:
            cls = args[0]

            if inspect.isclass(cls):
                self.set_wrapped_classname(cls)
            if isinstance(cls, Role):
                self.set_wrapped_classname(get_root_class(cls))
            else:
                self.init_class_properties(kwargs)
        elif len(args) > 0:
            raise Exception(
                "role decorator can only be called with keyword arguments in {self}"
            )
        else:
            self.init_class_properties(kwargs)

    def __call__(self, *args: Any, **kwargs: Any) -> Union[object, Self]:
        if self.classname is not None:
            ret = self.classname(*args, **kwargs)

            if not isinstance(ret, object):
                raise Exception("return type is not an object")

            return ret

        if len(args) != 1:
            raise Exception(
                "decorator must be called with an exactly one argument: a class"
            )

        wrapped = args[0]

        if inspect.isclass(wrapped):
            self.set_wrapped_classname(wrapped)

            return self
        elif isinstance(wrapped, Role):
            self.set_wrapped_classname(get_root_class(wrapped))

            return self
        else:
            raise Exception("roles can only wrap classes or other roles")

    def init_class_properties(self, kwargs: Dict[str, Any]) -> None:
        expected_class_properties = get_class_properties(type(self))

        for name in kwargs:
            if name not in expected_class_properties:
                raise Exception(f"unexpected property {name} in {self}")

            if not check_type(kwargs[name], expected_class_properties[name].type):
                raise Exception(
                    f"property {name} must be of type {expected_class_properties[name].type}  in {self}"
                )

            setattr(self, name, kwargs[name])

        for name in expected_class_properties:
            if not hasattr(self, name):
                if expected_class_properties[name].is_default_provided:
                    setattr(self, name, expected_class_properties[name].default_value)
                else:
                    raise Exception(f"property {name} must be provided in {self}")

    def set_wrapped_classname(self, cls: Type[Any]) -> None:
        self.classname = cls
        role_registry_global.register(self, cls)
