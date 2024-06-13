from granian.rsgi import HTTPProtocol, Scope

from ..http.router import Router
from ..httpfoundation import Request
from ..role.service import service


@service
class HTTPResponderAggregate:
    def __init__(
        self,
        router: Router,
    ):
        self.router = router

    async def respond_to_http(
        self,
        scope: Scope,
        proto: HTTPProtocol,
    ):
        assert scope.proto == "http"

        request = Request(path=scope.path)
        responder = self.router.match_responder(request)

        if responder is None:
            proto.response_str(
                status=404,
                headers=[("content-type", "text/plain")],
                body="Not found",
            )
        else:
            response = await responder.respond(request)

            proto.response_str(
                status=200,
                headers=[("content-type", "text/plain")],
                body=response.contents,
            )
