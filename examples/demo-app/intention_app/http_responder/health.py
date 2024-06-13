from intention.role import responds_to_http
from intention.http import Responder, TextResponse
from intention.httpfoundation import Request


@responds_to_http(
    description="Health check endpoint",
    method="get",
    name="health",
    pattern="/health",
)
class Health(Responder):
    async def respond(self, request: Request):
        return TextResponse("HEALTH OK!")
