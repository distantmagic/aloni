from http import HTTPStatus

from ..http_foundation.renderable_response import RenderableResponse


class TextResponse(RenderableResponse):
    def __init__(
        self,
        content: str,
        content_type: str = "text/plain",
        status: HTTPStatus = HTTPStatus.OK,
    ):
        RenderableResponse.__init__(self)

        self.content = content
        self.content_type = content_type
        self.status = status

    def get_content(self) -> str:
        return self.content

    def get_content_type(self) -> str:
        return self.content_type

    def get_status(self) -> HTTPStatus:
        return self.status
