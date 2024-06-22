class RoutePattern:
    def __init__(
        self,
        pattern: str,
    ) -> None:
        stripped_pattern = pattern.strip("/")
        stripped_pattern_parts = stripped_pattern.split("/")

        total_dynamic_parts = 0

        for part in stripped_pattern_parts:
            if "{" in part and "}" in part:
                total_dynamic_parts += 1

        self.is_static = total_dynamic_parts < 1
        self.parts = stripped_pattern_parts
        self.pattern = stripped_pattern
        self.total_dynamic_parts = total_dynamic_parts
