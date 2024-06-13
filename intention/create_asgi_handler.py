from asgiref.typing import (
    ASGIReceiveCallable,
    ASGISendCallable,
    Scope,
)

from .asgi import (
    HTTPResponderAggregate,
    LifespanResponderAggregate,
    WebSocketResponderAggregate,
)
from .dependency_injection_container import DependencyInjectionContainer
from .import_all_from import import_all_from
from .role.role_regsitry_global import role_registry_global
from .service_provider import *  # noqa: F403


def create_asgi_handler(module):
    import_all_from(module)

    di = DependencyInjectionContainer(role_registry=role_registry_global)
    di.prepare()

    http_responder_aggregate = di.make(HTTPResponderAggregate)
    lifespan_responder_aggregate = di.make(LifespanResponderAggregate)
    websocket_responder_aggregate = di.make(WebSocketResponderAggregate)

    async def asgi_handler(
        scope: Scope,
        receive: ASGIReceiveCallable,
        send: ASGISendCallable,
    ):
        match scope["type"]:
            case "http":
                await http_responder_aggregate.respond_to_http(
                    scope,
                    receive,
                    send,
                )
            case "lifespan":
                await lifespan_responder_aggregate.respond_to_lifespan(
                    scope,
                    receive,
                    send,
                )
            case "websocket":
                await websocket_responder_aggregate.respond_to_websocket(
                    scope,
                    receive,
                    send,
                )

    return asgi_handler
