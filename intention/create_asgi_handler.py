from asgiref.typing import (
    ASGIReceiveCallable,
    ASGISendCallable,
    Scope,
)
from .application_module_provider import ApplicationModuleProvider
from .asgi import (
    HTTPScopeResponder,
    LifespanScopeResponder,
    WebSocketScopeResponder,
)
from .dependency_injection_container import DependencyInjectionContainer
from .import_all_from import import_all_from
from .role.role_regsitry_global import role_registry_global
from .service_provider import *  # noqa: F403


def create_asgi_handler(module):
    import_all_from(module)

    di = DependencyInjectionContainer(role_registry=role_registry_global)
    di.prepare()
    di.register_instance(ApplicationModuleProvider, ApplicationModuleProvider(module))

    http_scope_responder = di.make(HTTPScopeResponder)
    lifespan_scope_responder = di.make(LifespanScopeResponder)
    websocket_scope_responder = di.make(WebSocketScopeResponder)

    async def asgi_handler(
        scope: Scope,
        receive: ASGIReceiveCallable,
        send: ASGISendCallable,
    ):
        match scope["type"]:
            case "http":
                await http_scope_responder.respond_to_http(
                    scope,
                    receive,
                    send,
                )
            case "lifespan":
                await lifespan_scope_responder.respond_to_lifespan(
                    scope,
                    receive,
                    send,
                )
            case "websocket":
                await websocket_scope_responder.respond_to_websocket(
                    scope,
                    receive,
                    send,
                )

    return asgi_handler
