class Request:
    def __init__(
        self,
        path: str,
    ):
        self.path = path.strip("/")
