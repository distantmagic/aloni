from typing import Annotated

from ..http.exception_responder import ExceptionResponder
from ..http.not_found_responder import NotFoundResponder
from ..http.responder import Responder
from ..http.responder_caller import ResponderCaller
from ..http.route import Route
from ..http.router import Router
from ..role.responds_to_http import responds_to_http
from ..role.service_provider import service_provider
from ..service_collection import ServiceColletion
from ..service_collection_filter.has_role import HasRole
from .service_provider import ServiceProvider


@service_provider(provides=Router)
class HttpRouterServiceProvider(ServiceProvider[Router]):
    def __init__(
        self,
        exception_responder: ExceptionResponder,
        not_found_responder: NotFoundResponder,
        responder_caller: ResponderCaller,
        service_collection: Annotated[
            ServiceColletion,
            HasRole(responds_to_http),
        ],
    ):
        ServiceProvider.__init__(self)

        self.exception_responder = exception_responder
        self.not_found_responder = not_found_responder
        self.responder_caller = responder_caller
        self.service_collection = service_collection

    def provide(self) -> Router:
        router = Router(
            not_found_responder=self.not_found_responder,
        )

        for role, responder in self.service_collection:
            if not isinstance(role, responds_to_http):
                raise Exception(f"expected {responds_to_http} got {role}")

            if not isinstance(responder, Responder):
                raise Exception(f"expected {Responder} got {responder}")

            self.responder_caller.prepare_for(responder)

            router.register_route(
                Route(
                    name=role.name,
                    pattern=role.pattern,
                    responder=responder,
                )
            )

        # manually add responders registered as global services
        self.responder_caller.prepare_for(self.exception_responder)
        self.responder_caller.prepare_for(self.not_found_responder)

        return router
