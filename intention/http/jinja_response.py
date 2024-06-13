from http import HTTPStatus
from ..httpfoundation import Response


class JinjaResponse(Response):
    def __init__(
        self,
        template_filename: str,
        data: dict = {},
        status: HTTPStatus = HTTPStatus.OK,
    ):
        Response.__init__(self)

        self.data = data
        self.template_filename = template_filename
        self.status = status

    def get_status(self) -> HTTPStatus:
        return self.status
