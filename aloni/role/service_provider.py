from typing import Any, Type

from .service import service


class service_provider(service):
    provides: Type[Any]
