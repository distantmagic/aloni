from abc import abstractmethod
from .response import Response


class RenderableResponse(Response):
    @abstractmethod
    def get_content(self) -> str:
        pass

    def get_content_type(self) -> str:
        return "text/plain"
