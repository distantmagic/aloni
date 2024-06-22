from ..role.service import service
from ..role.service_override_behavior import ServiceOverrideBehavior
from .exception_response import ExceptionResponse
from .responder import Responder


@service(override_behavior=ServiceOverrideBehavior.ALLOW)
class ExceptionResponder(Responder):
    async def respond(
        self,
        exception: Exception,
        trace: str,
    ) -> ExceptionResponse:
        return ExceptionResponse(
            exception=exception,
            trace=trace,
        )
