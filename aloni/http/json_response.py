from http import HTTPStatus
from typing import Any
from ..http_foundation import Response


class JsonResponse(Response):
    def __init__(
        self,
        data: dict[str, Any],
        status: HTTPStatus = HTTPStatus.OK,
    ):
        Response.__init__(self)

        self.data = data
        self.status = status

    def get_status(self) -> HTTPStatus:
        return self.status
