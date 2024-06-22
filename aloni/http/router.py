from typing import Generator, Optional
from ..http_foundation import Request
from .not_found_responder import NotFoundResponder
from .route import Route
from .route_node_match import RouteNodeMatch
from .route_match import RouteMatch
from .route_node import RouteNode
from .route_pattern import RoutePattern


class Router:
    def __init__(
        self,
        not_found_responder: NotFoundResponder,
    ):
        self.not_found_responder = not_found_responder
        self.root_node = RouteNode(wildcard=True)
        self.static_routes: dict[str, Route] = {}

    def find_potential_matches(
        self,
        current_depth: int,
        parent_match: Optional[RouteNodeMatch],
        parts: list[str],
        route_node: RouteNode,
    ) -> Generator[RouteNodeMatch, None, None]:
        if not parts:
            return

        part = parts[0]

        for child_node in route_node.child_nodes:
            if child_node.is_part_matching(part):
                route_node_match = RouteNodeMatch(
                    parent_match=parent_match,
                    route_node=child_node,
                    var_name=child_node.var_name,
                    var_value="/".join(parts) if child_node.greedy else part,
                )

                if child_node.is_final:
                    if child_node.greedy or child_node.depth == current_depth:
                        yield route_node_match

                    return

                yield from self.find_potential_matches(
                    current_depth + 1,
                    route_node_match,
                    parts[1:],
                    child_node,
                )

    def match(self, request: Request) -> RouteMatch:
        if request.path in self.static_routes:
            return RouteMatch(
                path_variables={},
                route=self.static_routes[request.path],
            )

        parts = request.path.split("/")

        matched = self.find_potential_matches(
            current_depth=1,
            parent_match=None,
            parts=parts,
            route_node=self.root_node,
        )

        final_matches: list[RouteNodeMatch] = list(matched)

        if len(final_matches) > 1:
            raise Exception("multiple route matches found")

        if len(final_matches) < 1:
            return self.not_found(request)

        final_match: Optional[RouteNodeMatch] = final_matches[0]

        if not final_match or not final_match.route_node.route:
            return self.not_found(request)

        final_match_route = final_match.route_node.route

        path_variables = {}

        while final_match:
            if final_match.var_name and final_match.var_value is not None:
                path_variables[final_match.var_name] = final_match.var_value

            final_match = final_match.parent_match

        return RouteMatch(
            path_variables=path_variables,
            route=final_match_route,
        )

    def not_found(self, request: Request) -> RouteMatch:
        return RouteMatch(
            path_variables={},
            route=Route(
                name=None,
                pattern=RoutePattern(request.path),
                responder=self.not_found_responder,
            ),
        )

    def register_route(
        self,
        route: Route,
    ) -> None:
        if route.pattern.is_static:
            self.static_routes[route.pattern.pattern] = route

            return

        self.register_dynamic_route(
            route=route,
            route_node=self.root_node,
            parts=route.pattern.parts,
        )

    def register_dynamic_route(
        self,
        route: Route,
        route_node: RouteNode,
        parts: list[str],
    ) -> None:
        if len(parts) < 1:
            return

        part = parts[0]

        child_node = RouteNode(
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
