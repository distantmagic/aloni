from asgiref.typing import ASGIReceiveCallable, ASGISendCallable, LifespanScope
import pprint

from ..intention import Intention
from ..role import singleton


@singleton
class LifespanResponderAggregate:
    def __init__(self, intention: Intention) -> None:
        self.intention = intention

    async def respond_to_lifespan(
        self,
        scope: LifespanScope,
        receive: ASGIReceiveCallable,
        send: ASGISendCallable,
    ):
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
                        await self.intention.startup()
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
