from asgiref.typing import ASGIReceiveCallable, ASGISendCallable, HTTPScope

from ..http.router import Router
from ..httpfoundation import Request


class HTTPResponderAggregate:
    def __init__(
        self,
        router: Router,
    ):
        self.router = router

    async def respond_to_http(
        self,
        scope: HTTPScope,
        receive: ASGIReceiveCallable,
        send: ASGISendCallable,
    ):
        assert scope["type"] == "http"

        request = Request(path=scope["path"])

        while True:
            message = await receive()

            match message["type"]:
                case "http.request":
                    responder = self.router.match_responder(request)

                    if responder is None:
                        await send(
                            {
                                "type": "http.response.start",
                                "status": 404,
                                "headers": [
                                    [b"content-type", b"text/plain"],
                                ],
                            }
                        )
                        await send(
                            {
                                "type": "http.response.body",
                                "body": b"Not found",
                            }
                        )
                    else:
                        response = await responder.respond(request)

                        await send(
                            {
                                "type": "http.response.start",
                                "status": 200,
                                "headers": [
                                    [b"content-type", b"text/plain"],
                                ],
                            }
                        )
                        await send(
                            {
                                "type": "http.response.body",
                                "body": bytes(response.contents, "utf-8"),
                            }
                        )

                case "http.disconnect":
                    break
