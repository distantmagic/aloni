from typing import Annotated

from ..http.responder import Responder
from ..http.response_interceptor import ResponseInterceptor
from ..http.response_interceptor_aggregate import ResponseInterceptorAggregate
from ..role.intercepts_http_response_wrapped import intercepts_http_response_wrapped
from ..role.service_provider import service_provider
from ..service_collection import ServiceColletion
from ..service_collection_filter.has_role import HasRole
from .service_provider import ServiceProvider


@service_provider(provides=ResponseInterceptorAggregate)
class HttpResponseInterceptorAggregateProvider(
    ServiceProvider[ResponseInterceptorAggregate]
):
    def __init__(
        self,
        service_collection: Annotated[
            ServiceColletion,
            HasRole(intercepts_http_response_wrapped),
        ],
    ):
        ServiceProvider.__init__(self)

        self.service_collection = service_collection

    def provide(self) -> ResponseInterceptorAggregate:
        response_interceptor_aggregate = ResponseInterceptorAggregate()

        for role, response_interceptor in self.service_collection:
            if not isinstance(role, intercepts_http_response_wrapped):
                raise Exception(
                    f"expected {intercepts_http_response_wrapped} got {role}"
                )

            if not isinstance(response_interceptor, ResponseInterceptor):
                raise Exception(f"expected {Responder} got {response_interceptor}")

            if role.response_cls in response_interceptor_aggregate.interceptors:
                raise Exception(
                    f"response interceptor for {role.response_cls} already registered"
                )

            response_interceptor_aggregate.interceptors[role.response_cls] = (
                response_interceptor
            )

        return response_interceptor_aggregate
