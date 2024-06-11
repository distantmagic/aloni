import asyncio
from typing import Union
from granian.rsgi import HTTPProtocol, Scope, WebsocketProtocol

from .intention import Intention
from .http.router import Router
from .role.role_regsitry_global import role_registry_global
from .rsgi import (
    HTTPResponderAggregate,
    WebSocketResponderAggregate,
)


def create_rsgi_handler():
    intention = Intention(
        role_registry=role_registry_global,
        router=Router(),
    )

    http_responder_aggregate = HTTPResponderAggregate(
        router=intention.router,
    )
    websocket_responder_aggregate = WebSocketResponderAggregate()

    asyncio.run(intention.startup())

    async def rsgi_handler(
        scope: Scope,
        proto: Union[HTTPProtocol, WebsocketProtocol],
    ):
        match scope.proto:
            case "http":
                await http_responder_aggregate.respond_to_http(
                    scope,
                    proto,
                )
            case "ws":
                await websocket_responder_aggregate.respond_to_websocket(
                    scope,
                    proto,
                )

    return rsgi_handler
