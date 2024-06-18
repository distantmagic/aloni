from typing import Any

from ..http_foundation.request import Request
from ..meta.argument_matching_function_caller import ArgumentMatchingFunctionCaller
from ..meta.async_responder_protocol import AsyncResponderProtocol
from ..meta.function_parameter_store import FunctionParameterStore
from ..meta.is_responder import is_responder
from ..role.service import service
from .responder import Responder


@service
class ResponderCaller:
    def __init__(
        self,
        function_parameter_store: FunctionParameterStore,
    ) -> None:
        self.function_parameter_store = function_parameter_store
        self.prepared_responders: dict[
            Responder,
            AsyncResponderProtocol[Any],
        ] = {}
        self.responder_callers: dict[
            Request,
            ArgumentMatchingFunctionCaller,
        ] = {}

    async def call_responder(
        self,
        request: Request,
        responder: Responder,
    ) -> Any:
        if responder not in self.prepared_responders:
            raise Exception(f"not prepared to handle {responder}")

        if request not in self.responder_callers:
            self.responder_callers[request] = ArgumentMatchingFunctionCaller(
                function_parameter_store=self.function_parameter_store,
                args={
                    "request": request,
                },
            )

        return await self.responder_callers[request].call_async_function(
            self.prepared_responders[responder].respond
        )

    # this method is called by the HttpRouterServiceProvider
    # it gives the opportunity for ResponderCaller to precache responder
    # parameters and to make the response times consistent later
    def prepare_for(self, responder: Responder) -> None:
        orig_responder = responder

        if not is_responder(responder):
            raise Exception(
                f"expected {responder} to implement async 'response' method"
            )

        self.prepared_responders[orig_responder] = responder
        self.function_parameter_store.cached_get_param_names(responder.respond)

    def request_done(self, request: Request) -> None:
        if request in self.responder_callers:
            del self.responder_callers[request]
