from aloni.role import responds_to_http
from aloni.http import Responder, JinjaResponse


@responds_to_http(pattern="/")
class Homepage(Responder):
    async def respond(self) -> JinjaResponse:
        return JinjaResponse("homepage.j2")
