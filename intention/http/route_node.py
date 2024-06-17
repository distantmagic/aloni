from typing import Optional, Self

from .route import Route


class RouteNode:
    def __init__(
        self,
        route: Optional[Route],
    ) -> None:
        self.children: dict[str, Self] = {}
        self.declared_path_variables: dict[str, str] = {}
        self.route: Optional[Route] = route
