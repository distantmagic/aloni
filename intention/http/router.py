from ..httpfoundation import Request
from .responder import Responder


class Router:
    def __init__(self):
        self.routes = {}

    def match_responder(self, request: Request):
        for pattern in self.routes:
            if pattern == request.path:
                return self.routes[pattern]

        return None

    def register_route(
        self,
        pattern: str,
        responder: Responder,
    ):
        self.routes[pattern] = responder
