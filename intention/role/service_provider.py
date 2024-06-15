from typing import Any, Generic, Type, TypeVar

from .role_builder import RoleBuilder
from .service_provider_wrapped import service_provider_wrapped

TProvides = TypeVar("TProvides", bound=object)


class service_provider(
    Generic[TProvides],
    RoleBuilder[service_provider_wrapped[TProvides]],
):
    def __init__(
        self,
        provides: Type[TProvides],
    ) -> None:
        RoleBuilder.__init__(self)

        self.provides = provides

    def wrap_with_role(self, cls: Type[Any]) -> service_provider_wrapped[TProvides]:
        return service_provider_wrapped(
            classname=cls,
            provides=self.provides,
        )
