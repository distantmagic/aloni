from abc import ABC
from http import HTTPStatus


class Response(ABC):
    def get_content_type(self) -> str:
        return "text/plain"

    def get_status(self) -> HTTPStatus:
        return HTTPStatus.OK
