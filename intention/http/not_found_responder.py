from ..httpfoundation.request import Request
from ..role.service import service
from .not_found_response import NotFoundResponse
from .responder import Responder


@service
class NotFoundResponder(Responder):
    async def respond(self, request: Request) -> NotFoundResponse:
        return NotFoundResponse()
