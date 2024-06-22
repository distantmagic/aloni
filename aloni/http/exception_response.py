from http import HTTPStatus

from ..http_foundation.renderable_response import RenderableResponse


class ExceptionResponse(RenderableResponse):
    def __init__(
        self,
        exception: Exception,
        trace: str,
    ):
        self.exception = exception
        self.trace = trace

    def get_content(self) -> str:
        return self.trace

    def get_status(self) -> HTTPStatus:
        return HTTPStatus.INTERNAL_SERVER_ERROR
