from typing import Type

from .service import service


class service_provider_wrapped(service):
    def __init__(
        self,
        classname: Type,
        provides: Type,
    ):
        service.__init__(self, classname)

        self.provides = provides
