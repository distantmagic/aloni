from typing import Type

from .role_builder import RoleBuilder
from .service_provider_wrapped import service_provider_wrapped


class service_provider(RoleBuilder):
    def __init__(
        self,
        provides: Type,
    ):
        RoleBuilder.__init__(self)

        self.provides = provides

    def wrap_with_role(self, cls: Type):
        return service_provider_wrapped(
            classname=cls,
            provides=self.provides,
        )
