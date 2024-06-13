from granian.rsgi import WebsocketProtocol, Scope

from ..role.service import service


@service
class WebSocketResponderAggregate:
    async def respond_to_websocket(
        self,
        scope: Scope,
        proto: WebsocketProtocol,
    ):
        assert scope.proto == "ws"
