from typing import Optional, Self

from .route import Route


class RouteNode:
    def __init__(
        self,
        depth: int = 0,
        greedy: bool = False,
        is_final: bool = False,
        pattern: Optional[str] = None,
        route: Optional[Route] = None,
        var_name: Optional[str] = None,
        wildcard: bool = False,
    ) -> None:
        self.child_nodes: list[Self] = []
        self.depth = depth
        self.greedy = greedy
        self.is_final = is_final
        self.pattern = pattern
        self.route = route
        self.var_name = var_name
        self.wildcard = wildcard

    def add_child(self, child_node: Self) -> None:
        self.child_nodes.append(child_node)

    def is_part_matching(self, part: str) -> bool:
        if self.wildcard:
            return True

        if self.pattern is not None:
            return self.pattern == part

        return False
