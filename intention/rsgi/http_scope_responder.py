from granian.rsgi import HTTPProtocol, Scope  # type: ignore

from ..http.recursive_responder_aggregate import RecursiveResponderAggregate
from ..http.responder_caller import ResponderCaller
from ..http_foundation import Request
from ..role.service import service


@service
class HTTPScopeResponder:
    def __init__(
        self,
        recursive_responder_aggregate: RecursiveResponderAggregate,
        responder_caller: ResponderCaller,
    ):
        self.recursive_responder_aggregate = recursive_responder_aggregate
        self.responder_caller = responder_caller

    async def respond_to_http(
        self,
        scope: Scope,
        proto: HTTPProtocol,
    ) -> None:
        assert scope.proto == "http"

        request = Request(path=scope.path)

        try:
            response = await self.recursive_responder_aggregate.produce_response(
                request,
            )

            proto.response_str(
                status=response.get_status(),
                headers=[("content-type", response.get_content_type())],
                body=response.get_content(),
            )
        finally:
            self.responder_caller.request_done(request)
