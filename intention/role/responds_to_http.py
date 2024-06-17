from http import HTTPMethod
from typing import Optional

from .service import service


class responds_to_http(service):
    pattern: str
    method: HTTPMethod = HTTPMethod.GET
    description: Optional[str] = None
    name: Optional[str] = None
