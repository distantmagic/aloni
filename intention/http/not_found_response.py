from http import HTTPStatus

from ..httpfoundation import Response


class NotFoundResponse(Response):
    def get_status(self) -> HTTPStatus:
        return HTTPStatus.NOT_FOUND
