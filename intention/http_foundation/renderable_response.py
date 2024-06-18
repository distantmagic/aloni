from abc import abstractmethod
from .final_response import FinalResponse


class RenderableResponse(FinalResponse):
    @abstractmethod
    def get_content(self) -> str:
        pass
