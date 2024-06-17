from ..role.service import service
from ..role.service_override_behavior import ServiceOverrideBehavior
from .not_found_response import NotFoundResponse
from .responder import Responder


@service(override_behavior=ServiceOverrideBehavior.ALLOW)
class NotFoundResponder(Responder):
    async def respond(self) -> NotFoundResponse:
        return NotFoundResponse()
