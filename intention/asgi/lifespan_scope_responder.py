# mypy: ignore-errors

from asgiref.typing import ASGIReceiveCallable, ASGISendCallable, LifespanScope
import pprint

from ..role.service import service


@service
class LifespanScopeResponder:
    async def respond_to_lifespan(
        self,
        scope: LifespanScope,
        receive: ASGIReceiveCallable,
        send: ASGISendCallable,
    ):
        assert scope["type"] == "lifespan"

        while True:
            message = await receive()

            match message["type"]:
                case "lifespan.shutdown":
                    await send(
                        {
                            "type": "lifespan.shutdown.complete",
                        }
                    )
                case "lifespan.startup":
                    try:
                        await send(
                            {
                                "type": "lifespan.startup.complete",
                            }
                        )
                    except Exception as e:
                        pprint.pp(e)

                        await send(
                            {
                                "type": "lifespan.startup.failed",
                            }
                        )
