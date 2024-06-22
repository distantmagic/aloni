from typing import Generator, Optional

from ..role.service import service
from .route import Route
from .route_dynamic_node import RouteDynamicNode
from .route_dynamic_node_match import RouteDynamicNodeMatch


@service
class RouteDynamicMatcher:
    def __init__(self) -> None:
        self.root_node = RouteDynamicNode(wildcard=True)

    def find_potential_dynamic_matches(
        self,
        current_depth: int,
        parent_match: Optional[RouteDynamicNodeMatch],
        parts: list[str],
        route_node: Optional[RouteDynamicNode] = None,
    ) -> Generator[RouteDynamicNodeMatch, None, None]:
        if not parts:
            return

        if route_node is None:
            route_node = self.root_node

        part = parts[0]

        for child_node in route_node.child_nodes:
            if child_node.is_part_matching(part):
                route_node_match = RouteDynamicNodeMatch(
                    parent_match=parent_match,
                    route_node=child_node,
                    var_name=child_node.var_name,
                    var_value="/".join(parts) if child_node.greedy else part,
                )

                if child_node.is_final:
                    if child_node.greedy or child_node.depth == current_depth:
                        yield route_node_match

                    return

                yield from self.find_potential_dynamic_matches(
                    current_depth + 1,
                    route_node_match,
                    parts[1:],
                    child_node,
                )

    def register_dynamic_route(
        self,
        route: Route,
        parts: list[str],
        route_node: Optional[RouteDynamicNode] = None,
    ) -> None:
        if len(parts) < 1:
            return

        if route_node is None:
            route_node = self.root_node

        part = parts[0]

        child_node = RouteDynamicNode(
            depth=route_node.depth + 1,
            is_final=len(parts) == 1,
            route=route,
        )

        if part.startswith("{") and part.endswith("}"):
            var_name = part[1:-1]

            if ":" in var_name:
                var_name_parts = var_name.split(":")

                child_node.greedy = "**" == var_name_parts[1]
                child_node.var_name = var_name_parts[0]
                child_node.wildcard = True
            else:
                child_node.var_name = var_name
                child_node.wildcard = True
        else:
            child_node.pattern = part

        route_node.add_child(child_node=child_node)

        return self.register_dynamic_route(
            route=route,
            route_node=child_node,
            parts=parts[1:],
        )
