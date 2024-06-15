from typing import Any, Generic, Type, TypeVar

from .service import service

TProvides = TypeVar("TProvides", bound=object)


class service_provider_wrapped(
    service,
    Generic[TProvides],
):
    def __init__(
        self,
        classname: Type[Any],
        provides: Type[TProvides],
    ) -> None:
        service.__init__(self, classname)

        self.provides = provides
