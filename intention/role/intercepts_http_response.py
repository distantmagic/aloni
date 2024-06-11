from typing import Type
from ..httpfoundation import Response
from .role import Role


class intercepts_http_response(Role):
    def __init__(self, name: Type[Response]):
        pass

    def __call__(self, cls):
        return cls
