from aloni.role import responds_to_http
from aloni.http import Responder, TextResponse
from http import HTTPMethod


@responds_to_http(
    description="Health check endpoint",
    method=HTTPMethod.GET,
    name="health",
    pattern="/health",
)
class Health(Responder):
    async def respond(self) -> TextResponse:
        return TextResponse("OK")
