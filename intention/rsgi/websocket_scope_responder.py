from granian.rsgi import WebsocketProtocol, Scope  # type: ignore

from ..role.service import service


@service
class WebSocketScopeResponder:
    async def respond_to_websocket(
        self,
        scope: Scope,
        proto: WebsocketProtocol,
    ) -> None:
        assert scope.proto == "ws"
