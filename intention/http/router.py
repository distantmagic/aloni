from ..httpfoundation import Request
from .not_found_responder import NotFoundResponder
from .responder import Responder


class Router:
    def __init__(
        self,
        not_found_responder: NotFoundResponder,
    ):
        self.not_found_responder = not_found_responder
        self.routes: dict[str, Responder] = {}

    def match_responder(self, request: Request) -> Responder:
        for pattern in self.routes:
            if pattern == request.path:
                return self.routes[pattern]

        return self.not_found_responder

    def register_route(
        self,
        pattern: str,
        responder: Responder,
    ) -> None:
        self.routes[pattern] = responder
