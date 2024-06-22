import types
from typing import Any, Mapping, Optional, Self, Type
from .responder_caller import ResponderCaller
from ..http_foundation.request import Request


class RequestContext:
    def __init__(
        self,
        request: Request,
        responder_caller: ResponderCaller,
        responder_args: Mapping[str, Any],
    ) -> None:
        self.request = request
        self.responder_args = responder_args
        self.responder_caller = responder_caller

    async def __aenter__(self) -> Self:
        await self.responder_caller.prepare_for_request(
            request=self.request,
            responder_args=self.responder_args,
        )

        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[types.TracebackType],
    ) -> bool:
        await self.responder_caller.request_done(self.request)

        return False
