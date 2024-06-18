from typing import Type

from ..http_foundation import Response
from .service import service


class intercepts_http_response(service):
    response_class: Type[Response]
