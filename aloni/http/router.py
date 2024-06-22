from typing import Optional
from ..http_foundation import Request
from .not_found_responder import NotFoundResponder
from .route import Route
from .route_node_match import RouteNodeMatch
from .route_match import RouteMatch
from .route_node import RouteNode


class Router:
    def __init__(
        self,
        not_found_responder: NotFoundResponder,
    ):
        self.not_found_responder = not_found_responder
        self.root_node = RouteNode(wildcard=True)

    def match(self, request: Request) -> RouteMatch:
        parts = request.path.strip("/").split("/")

        matched = self.match_recursive(
            current_depth=1,
            parent_match=None,
            parts=parts,
            route_node=self.root_node,
        )

        final_matches: list[RouteNodeMatch] = []

        for match in matched:
            if match.route_node.is_final:
                final_matches.append(match)

        if len(final_matches) < 1:
            return self.not_found(request)

        if len(final_matches) > 1:
            raise Exception("multiple route matches found")

        final_match: Optional[RouteNodeMatch] = final_matches[0]

        if not final_match:
            raise Exception("route not found")

        final_match_route = final_match.route_node.route

        if not final_match_route:
            raise Exception("route not found")

        path_variables = {}

        while final_match:
            if final_match.var_name and final_match.var_value is not None:
                path_variables[final_match.var_name] = final_match.var_value

            final_match = final_match.parent_match

        return RouteMatch(
            path_variables=path_variables,
            route=final_match_route,
        )

    def match_recursive(
        self,
        current_depth: int,
        parent_match: Optional[RouteNodeMatch],
        parts: list[str],
        route_node: RouteNode,
    ) -> list[RouteNodeMatch]:
        if not parts:
            return []

        part = parts[0]
        matches = []

        for child_node in route_node.child_nodes:
            if child_node.is_part_matching(part):
                route_node_match = RouteNodeMatch(
                    parent_match=parent_match,
                    route_node=child_node,
                    var_name=child_node.var_name,
                    var_value="/".join(parts) if child_node.greedy else part,
                )

                matches.append(route_node_match)

                if child_node.is_final:
                    return matches

                matches.extend(
                    self.match_recursive(
                        current_depth + 1,
                        route_node_match,
                        parts[1:],
                        child_node,
                    )
                )

        return matches

    def not_found(self, request: Request) -> RouteMatch:
        return RouteMatch(
            path_variables={},
            route=Route(
                name=None,
                pattern=request.path,
                responder=self.not_found_responder,
            ),
        )

    def register_route(
        self,
        route: Route,
    ) -> None:
        parts = route.pattern.strip("/").split("/")

        self.register_route_recursive(
            route,
            self.root_node,
            parts,
        )

    def register_route_recursive(
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

        return self.register_route_recursive(
            route=route,
            route_node=child_node,
            parts=parts[1:],
        )
