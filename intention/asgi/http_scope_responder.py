# mypy: ignore-errors

from asgiref.typing import ASGIReceiveCallable, ASGISendCallable, HTTPScope

from ..http.recursive_response_producer import RecursiveResponseProducer
from ..httpfoundation import Request
from ..role.service import service


@service
class HTTPScopeResponder:
    def __init__(
        self,
        recursive_response_producer: RecursiveResponseProducer,
    ):
        self.recursive_response_producer = recursive_response_producer

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
                    response = await self.recursive_response_producer.produce_response(
                        request
                    )

                    await send(
                        {
                            "type": "http.response.start",
                            "status": response.get_status(),
                            "headers": [
                                [
                                    b"content-type",
                                    bytes(response.get_content_type(), "utf-8"),
                                ],
                            ],
                        }
                    )
                    await send(
                        {
                            "type": "http.response.body",
                            "body": bytes(response.get_content(), "utf-8"),
                        }
                    )

                case "http.disconnect":
                    break
