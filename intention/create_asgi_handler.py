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
from .intention import Intention
from .role.role_regsitry_global import role_registry_global
from .http.router import Router


def create_asgi_handler():
    intention = Intention(
        role_registry=role_registry_global,
        router=Router(),
    )

    http_responder_aggregate = HTTPResponderAggregate(
        router=intention.router,
    )
    lifespan_responder_aggregate = LifespanResponderAggregate(intention)
    websocket_responder_aggregate = WebSocketResponderAggregate()

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
