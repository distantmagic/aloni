from typing import Optional

from .responder import Responder


class Route:
    def __init__(
        self,
        name: Optional[str],
        pattern: str,
        responder: Responder,
    ) -> None:
        self.name = name
        self.pattern = pattern
        self.responder = responder
