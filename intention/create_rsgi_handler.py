from typing import Union
from granian.rsgi import HTTPProtocol, Scope, WebsocketProtocol

from .dependency_injection_container import DependencyInjectionContainer
from .import_all_from import import_all_from
from .role.role_regsitry_global import role_registry_global
from .rsgi import (
    HTTPResponderAggregate,
    WebSocketResponderAggregate,
)
from .service_provider import *  # noqa: F403


def create_rsgi_handler(module):
    import_all_from(module)

    di = DependencyInjectionContainer(role_registry=role_registry_global)
    di.prepare()

    http_responder_aggregate = di.make(HTTPResponderAggregate)
    websocket_responder_aggregate = di.make(WebSocketResponderAggregate)

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
