from intention.role import responds_to_http
from intention.http import Responder, JinjaResponse
from intention.httpfoundation import Request


@responds_to_http(pattern="/")
class Homepage(Responder):
    async def respond(self, request: Request) -> JinjaResponse:
        return JinjaResponse("homepage.j2")
