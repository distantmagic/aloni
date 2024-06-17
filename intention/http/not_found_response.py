from http import HTTPStatus

from ..http_foundation import Response


class NotFoundResponse(Response):
    def get_status(self) -> HTTPStatus:
        return HTTPStatus.NOT_FOUND
