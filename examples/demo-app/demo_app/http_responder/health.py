from http import HTTPMethod
from intention.role import responds_to_http
from intention.http import Responder, TextResponse


@responds_to_http(
    description="Health check endpoint",
    method=HTTPMethod.GET,
    name="health",
    pattern="/health",
)
class Health(Responder):
    async def respond(self) -> TextResponse:
        return TextResponse("OK")
