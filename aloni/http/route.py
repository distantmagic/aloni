from typing import Optional

from .responder import Responder
from .route_pattern import RoutePattern


class Route:
    def __init__(
        self,
        name: Optional[str],
        pattern: RoutePattern,
        responder: Responder,
    ) -> None:
        self.name = name
        self.pattern = pattern
        self.responder = responder
