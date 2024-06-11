from ..httpfoundation import Request, Response


class TextResponse(Response):
    def __init__(
        self,
        request: Request,
        contents: str,
    ):
        Response.__init__(self)

        self.request = request
        self.contents = contents
