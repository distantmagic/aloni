from intention.role import responds_to_http
from intention.http import Responder, TextResponse


@responds_to_http(pattern="/ping")
class Ping(Responder):
    async def respond(self) -> TextResponse:
        return TextResponse("pong")
