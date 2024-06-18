from ..http_foundation import Request
from .not_found_responder import NotFoundResponder
from .route import Route
from .route_match import RouteMatch
from .route_node import RouteNode


class Router:
    def __init__(
        self,
        not_found_responder: NotFoundResponder,
    ):
        self.not_found_responder = not_found_responder
        self.root = RouteNode(route=None)

    def match(self, request: Request) -> RouteMatch:
        node = self.root
        parts = request.path.strip("/").split("/")
        path_variables = {}

        for part in parts:
            if part in node.children:
                node = node.children[part]
            elif "*" in node.children:
                node = node.children["*"]
                var_name = node.declared_path_variables.get("*", "*")
                if var_name != "*":
                    path_variables[var_name] = part
            else:
                return self.not_found(request)

        if node.route is not None:
            return RouteMatch(
                path_variables=path_variables,
                route=node.route,
            )
        else:
            return self.not_found(request)

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
        node = self.root
        parts = route.pattern.strip("/").split("/")

        for part in parts:
            if part.startswith("{") and part.endswith("}"):
                key = "*"
                var_name = part[1:-1]
            elif part == "*":
                key = "*"
                var_name = "*"
            else:
                key = part
                var_name = None

            if key not in node.children:
                node.children[key] = RouteNode(route=None)

            node = node.children[key]

            if var_name:
                node.declared_path_variables[key] = var_name

        node.route = route
