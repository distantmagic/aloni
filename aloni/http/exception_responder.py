from ..role.service import service
from .exception_response import ExceptionResponse
from .responder import Responder


@service
class ExceptionResponder(Responder):
    async def respond(self, exception: Exception) -> ExceptionResponse:
        return ExceptionResponse(exception)
