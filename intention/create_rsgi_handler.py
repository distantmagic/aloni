from typing import Union
from granian.rsgi import HTTPProtocol, Scope, WebsocketProtocol

from .application_module_provider import ApplicationModuleProvider
from .dependency_injection_container import DependencyInjectionContainer
from .import_all_from import import_all_from
from .role.role_regsitry_global import role_registry_global
from .rsgi import (
    HTTPScopeResponder,
    WebSocketScopeResponder,
)
from .service_provider import *  # noqa: F403


def create_rsgi_handler(module):
    import_all_from(module)

    di = DependencyInjectionContainer(role_registry=role_registry_global)
    di.prepare()
    di.register_instance(ApplicationModuleProvider, ApplicationModuleProvider(module))

    http_scope_responder = di.make(HTTPScopeResponder)
    websocket_scope_responder = di.make(WebSocketScopeResponder)

    async def rsgi_handler(
        scope: Scope,
        proto: Union[HTTPProtocol, WebsocketProtocol],
    ):
        match scope.proto:
            case "http":
                await http_scope_responder.respond_to_http(
                    scope,
                    proto,
                )
            case "ws":
                await websocket_scope_responder.respond_to_websocket(
                    scope,
                    proto,
                )

    return rsgi_handler
