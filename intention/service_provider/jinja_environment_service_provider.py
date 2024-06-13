from ..application_module_provider import ApplicationModuleProvider
from ..role.service_provider import service_provider
from .service_provider import ServiceProvider
from jinja2 import Environment, PackageLoader, select_autoescape


@service_provider(provides=Environment)
class JinjaEnvironmentServiceProvider(ServiceProvider[Environment]):
    def __init__(
        self,
        application_module_provider: ApplicationModuleProvider,
    ):
        self.application_module_provider = application_module_provider

    def provide(self) -> Environment:
        return Environment(
            auto_reload=False,
            enable_async=True,
            loader=PackageLoader(
                self.application_module_provider.get_module().__name__,
            ),
            autoescape=select_autoescape(),
        )
