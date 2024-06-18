from http import HTTPStatus

from ..http_foundation import RenderableResponse


class NotFoundResponse(RenderableResponse):
    def get_content(self) -> str:
        return "not found"

    def get_content_type(self) -> str:
        return "text/plain"

    def get_status(self) -> HTTPStatus:
        return HTTPStatus.NOT_FOUND
