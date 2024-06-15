from intention.role import responds_to_http
from intention.http import Responder, TextResponse
from intention.httpfoundation import Request


@responds_to_http(pattern="/ping")
class Ping(Responder):
    async def respond(self, request: Request) -> TextResponse:
        return TextResponse("pong")
