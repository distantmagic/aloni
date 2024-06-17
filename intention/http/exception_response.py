from http import HTTPStatus

from ..http_foundation.renderable_response import RenderableResponse


class ExceptionResponse(RenderableResponse):
    def __init__(self, exception: Exception):
        self.exception = exception

    def get_content(self) -> str:
        return str(self.exception)

    def get_status(self) -> HTTPStatus:
        return HTTPStatus.INTERNAL_SERVER_ERROR
