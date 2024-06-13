from typing import Union

from ..httpfoundation.renderable_response import RenderableResponse
from ..httpfoundation.request import Request
from ..httpfoundation.response import Response
from ..role.service import service
from .exception_response import ExceptionResponse
from .response_interceptor_aggregate import ResponseInterceptorAggregate
from .responder import Responder
from .router import Router


@service
class RecursiveResponseProducer:
    def __init__(
        self,
        response_interceptor_aggregate: ResponseInterceptorAggregate,
        router: Router,
    ):
        self.response_interceptor_aggregate = response_interceptor_aggregate
        self.router = router

    async def produce_response(self, request: Request) -> RenderableResponse:
        try:
            responder = self.router.match_responder(request)
            response = await responder.respond(request)

            return await self.process_response(request, response)
        except Exception as err:
            return ExceptionResponse(err)

    async def process_interceptors(
        self,
        request: Request,
        response: Response,
    ) -> RenderableResponse:
        if not self.response_interceptor_aggregate.can_intercept(response):
            if isinstance(response, RenderableResponse):
                return response

            raise ValueError(f"unable to produce a renderable response from {response}")

        return await self.process_response(
            request=request,
            response=await self.response_interceptor_aggregate.intercept(response),
        )

    async def process_response(
        self,
        request: Request,
        response: Union[Response, Responder],
    ) -> RenderableResponse:
        if isinstance(response, RenderableResponse):
            return await self.process_interceptors(request, response)
        elif isinstance(response, Responder):
            return await self.process_response(request, await response.respond(request))
        elif isinstance(response, Response):
            return await self.process_interceptors(request, response)
        else:
            raise ValueError("unable to produce any kind of response")
