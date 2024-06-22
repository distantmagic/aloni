class RoutePattern:
    def __init__(
        self,
        pattern: str,
    ) -> None:
        stripped_pattern = pattern.strip("/")

        self.is_static = "{" not in stripped_pattern and "}" not in stripped_pattern
        self.parts = stripped_pattern.split("/")
        self.pattern = stripped_pattern
