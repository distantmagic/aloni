from abc import ABC
from typing import Type

from .role_regsitry_global import role_registry_global


class Role(ABC):
    def __init__(self, classname: Type):
        role_registry_global.register(
            role=self,
            wrapped_class=classname,
        )

        self.classname = classname

    def __call__(self, *args, **kwargs):
        return self.classname(*args, **kwargs)
