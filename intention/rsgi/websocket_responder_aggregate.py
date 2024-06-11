from granian.rsgi import WebsocketProtocol, Scope


class WebSocketResponderAggregate:
    async def respond_to_websocket(
        self,
        scope: Scope,
        proto: WebsocketProtocol,
    ):
        assert scope.proto == "ws"
