from typing import Optional, Self
from .route_node import RouteNode


class RouteNodeMatch:
    def __init__(
        self,
        parent_match: Optional[Self],
        route_node: RouteNode,
        var_name: Optional[str],
        var_value: Optional[str],
    ) -> None:
        self.parent_match = parent_match
        self.route_node = route_node
        self.var_name = var_name
        self.var_value = var_value
