from typing import Optional, Self
from .route_dynamic_node import RouteDynamicNode


class RouteDynamicNodeMatch:
    def __init__(
        self,
        parent_match: Optional[Self],
        route_node: RouteDynamicNode,
        var_name: Optional[str],
        var_value: Optional[str],
    ) -> None:
        self.parent_match = parent_match
        self.route_node = route_node
        self.var_name = var_name
        self.var_value = var_value

    def get_path_variables(self) -> dict[str, str]:
        path_variables = {}
        match: Optional[RouteDynamicNodeMatch] = self

        while match:
            if match.var_name and match.var_value is not None:
                path_variables[match.var_name] = match.var_value

            match = match.parent_match

        return path_variables

    def get_dynamic_difference(self, other: Self) -> int:
        if self.route_node.route is None:
            raise Exception("route node has no route assigned")

        if other.route_node.route is None:
            raise Exception("other route node has no route assigned")

        return (
            self.route_node.route.pattern.total_dynamic_parts
            - other.route_node.route.pattern.total_dynamic_parts
        )
