from ..application_state import ApplicationState
from ..role.service_provider import service_provider
from .service_provider import ServiceProvider
from jinja2 import Environment, PackageLoader, select_autoescape


@service_provider(provides=Environment)
class JinjaEnvironmentServiceProvider(ServiceProvider[Environment]):
    def __init__(
        self,
        application_state: ApplicationState,
    ):
        ServiceProvider.__init__(self)

        self.application_state = application_state

    def provide(self) -> Environment:
        return Environment(
            auto_reload=False,
            enable_async=True,
            loader=PackageLoader(
                self.application_state.root_module.__name__,
            ),
            autoescape=select_autoescape(),
        )
