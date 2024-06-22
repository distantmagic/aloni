from typing import Optional
from ..http_foundation import Request
from .not_found_responder import NotFoundResponder
from .route import Route
from .route_dynamic_matcher import RouteDynamicMatcher
from .route_dynamic_node_match import RouteDynamicNodeMatch
from .route_match import RouteMatch
from .route_pattern import RoutePattern


class Router:
    def __init__(
        self,
        not_found_responder: NotFoundResponder,
        route_dynamic_matcher: RouteDynamicMatcher,
    ):
        self.not_found_responder = not_found_responder
        self.route_dynamic_matcher = route_dynamic_matcher
        self.static_routes: dict[str, Route] = {}

    def match(self, request: Request) -> RouteMatch:
        if request.path in self.static_routes:
            return RouteMatch(
                path_variables={},
                route=self.static_routes[request.path],
            )

        matched = self.route_dynamic_matcher.find_potential_dynamic_matches(
            current_depth=1,
            parent_match=None,
            parts=request.path.split("/"),
        )

        potential_matches: list[RouteDynamicNodeMatch] = list(matched)

        if len(potential_matches) > 1:
            raise Exception("multiple route matches found")

        if len(potential_matches) < 1:
            return self.not_found(request)

        final_match: Optional[RouteDynamicNodeMatch] = potential_matches[0]

        if not final_match or not final_match.route_node.route:
            return self.not_found(request)

        return RouteMatch(
            path_variables=final_match.get_path_variables(),
            route=final_match.route_node.route,
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

        self.route_dynamic_matcher.register_dynamic_route(
            route=route,
            parts=route.pattern.parts,
        )
