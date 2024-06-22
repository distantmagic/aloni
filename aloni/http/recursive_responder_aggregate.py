from typing import Any, Mapping

from ..http_foundation.final_response import FinalResponse
from ..http_foundation.request import Request
from ..http_foundation.response import Response
from ..role.service import service
from .exception_response import ExceptionResponse
from .response_interceptor_aggregate import ResponseInterceptorAggregate
from .responder import Responder
from .responder_caller import ResponderCaller
from .router import Router


@service
class RecursiveResponderAggregate:
    def __init__(
        self,
        responder_caller: ResponderCaller,
        response_interceptor_aggregate: ResponseInterceptorAggregate,
        router: Router,
    ):
        self.responder_caller = responder_caller
        self.response_interceptor_aggregate = response_interceptor_aggregate
        self.router = router

    async def produce_response(self, request: Request) -> FinalResponse:
        try:
            router_match = self.router.match(request)
            responder_args = router_match.path_variables | {
                "request": request,
            }

            responder = router_match.route.responder
            response = await self.responder_caller.call_responder(
                request, responder, responder_args
            )

            return await self.process_response(request, response, responder_args)
        except Exception as err:
            return ExceptionResponse(err)

    async def process_interceptors(
        self,
        request: Request,
        response: Response,
        responder_args: Mapping[str, Any] = {},
    ) -> FinalResponse:
        if not self.response_interceptor_aggregate.can_intercept(response):
            if isinstance(response, FinalResponse):
                return response

            raise ValueError(f"unable to produce a renderable response from {response}")

        return await self.process_response(
            request=request,
            response=await self.response_interceptor_aggregate.intercept(response),
            responder_args=responder_args,
        )

    async def process_response(
        self,
        request: Request,
        response: Any,
        responder_args: Mapping[str, Any] = {},
    ) -> FinalResponse:
        if isinstance(response, FinalResponse):
            return await self.process_interceptors(request, response)
        elif isinstance(response, Responder):
            return await self.process_response(
                request=request,
                response=await self.responder_caller.call_responder(
                    request, response, responder_args
                ),
            )
        elif isinstance(response, Response):
            return await self.process_interceptors(request, response)
        else:
            raise ValueError("unable to produce any kind of response")
