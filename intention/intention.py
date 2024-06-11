from .http.router import Router
from .role.responds_to_http_wrapped import responds_to_http_wrapped
from .role.role_registry import RoleRegistry


class Intention:
    def __init__(
        self,
        role_registry: RoleRegistry,
        router: Router,
    ):
        self.role_registry = role_registry
        self.router = router

    async def startup(self):
        for role_wrapped_class_tuple in self.role_registry.registry:
            if isinstance(role_wrapped_class_tuple[0], responds_to_http_wrapped):
                self.router.register_route(
                    pattern=role_wrapped_class_tuple[0].pattern,
                    responder=role_wrapped_class_tuple[1](),
                )
