from typing import Awaitable, Callable, Union
from granian.constants import Interfaces
from granian.rsgi import HTTPProtocol, Scope, WebsocketProtocol  # type: ignore
from granian.server import Granian
import sys

from ..application_mode import ApplicationMode
from ..application_state import ApplicationState
from ..role.responds_to_cli import responds_to_cli
from ..rsgi.http_scope_responder import HTTPScopeResponder
from ..rsgi.websocket_scope_responder import WebSocketScopeResponder
from .command import Command
from .command_option import CommandOption


@responds_to_cli(
    name="serve",
    description="Start the app in HTTP server mode",
    options=[
        CommandOption(
            name="--host",
            type=str,
            help="The host to bind the app to",
            default="127.0.0.1",
        ),
        CommandOption(
            name="--port",
            type=int,
            help="The port to bind the app to",
            default=8000,
        ),
        CommandOption(
            name="--reload",
            type=bool,
            help="Enable auto reload on application's files changes (requires granian[reload] extra)",
            default=False,
        ),
        CommandOption(
            name="--ssl-certificate",
            type=str,
            help="SSL certificate",
            default=None,
        ),
        CommandOption(
            name="--ssl-keyfile",
            type=str,
            help="SSL key file",
            default=None,
        ),
        CommandOption(
            name="--url-path-prefix",
            type=str,
            help="URL path prefix the app is mounted on",
            default=None,
        ),
    ],
)
class Serve(Command):
    def __init__(
        self,
        application_state: ApplicationState,
        http_scope_responder: HTTPScopeResponder,
        websocket_scope_responder: WebSocketScopeResponder,
    ):
        Command.__init__(self)

        self.application_state = application_state
        self.http_scope_responder = http_scope_responder
        self.websocket_scope_responder = websocket_scope_responder

    def respond(self) -> int:
        server = Granian(
            self.application_state.root_module.__name__,
            interface=Interfaces.RSGI,
            websockets=False,
            workers=2,
        )

        server.serve(target_loader=self.load_target)

        return 0

    def load_target(
        self, target: str
    ) -> Callable[
        [
            Scope,
            Union[HTTPProtocol, WebsocketProtocol],
        ],
        Awaitable[None],
    ]:
        if target not in sys.modules:
            raise ImportError(f"module {target} is not loaded")

        self.application_state.mode = ApplicationMode.HTTP_SERVER

        async def rsgi_handler(
            scope: Scope,
            proto: Union[HTTPProtocol, WebsocketProtocol],
        ) -> None:
            match scope.proto:
                case "http":
                    await self.http_scope_responder.respond_to_http(
                        scope,
                        proto,  # type: ignore
                    )
                case "ws":
                    await self.websocket_scope_responder.respond_to_websocket(
                        scope,
                        proto,  # type: ignore
                    )

        return rsgi_handler
