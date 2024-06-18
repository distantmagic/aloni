from .route import Route


class RouteMatch:
    def __init__(
        self,
        path_variables: dict[str, str],
        route: Route,
    ) -> None:
        self.path_variables = path_variables
        self.route = route
