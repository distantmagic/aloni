from granian.rsgi import HTTPProtocol, Scope

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
        scope: Scope,
        proto: HTTPProtocol,
    ):
        assert scope.proto == "http"

        request = Request(path=scope.path)
        response = await self.recursive_response_producer.produce_response(request)

        proto.response_str(
            status=response.get_status(),
            headers=[("content-type", response.get_content_type())],
            body=response.get_content(),
        )
