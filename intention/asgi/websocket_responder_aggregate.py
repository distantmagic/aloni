from asgiref.typing import ASGIReceiveCallable, ASGISendCallable, WebSocketScope
import pprint


class WebSocketResponderAggregate:
    async def respond_to_websocket(
        self,
        scope: WebSocketScope,
        receive: ASGIReceiveCallable,
        send: ASGISendCallable,
    ):
        pprint.pp(scope)

        while True:
            message = await receive()
            pprint.pp(message)

            match message["type"]:
                case "websocket.connect":
                    await send(
                        {
                            "type": "websocket.accept",
                        }
                    )
                case "websocket.disconnect":
                    break
                case "websocket.receive":
                    await send(
                        {
                            "type": "websocket.send",
                            "text": message["text"],
                        }
                    )
