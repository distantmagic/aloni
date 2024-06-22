from typing import Annotated
from jinja2 import Environment, PackageLoader, StrictUndefined, select_autoescape

from ..application_state import ApplicationState
from ..jinja_function.jinja_function import JinjaFunction
from ..role.service_provider import service_provider
from ..role.jinja_function import jinja_function
from ..service_collection import ServiceColletion
from ..service_collection_filter.has_role import HasRole
from .service_provider import ServiceProvider


@service_provider(provides=Environment)
class JinjaEnvironmentServiceProvider(ServiceProvider[Environment]):
    def __init__(
        self,
        application_state: ApplicationState,
        jinja_function_collection: Annotated[
            ServiceColletion,
            HasRole(jinja_function),
        ],
    ):
        ServiceProvider.__init__(self)

        self.application_state = application_state
        self.jinja_function_collection = jinja_function_collection

    async def provide(self) -> Environment:
        environment = Environment(
            autoescape=select_autoescape(),
            auto_reload=False,
            enable_async=True,
            loader=PackageLoader(
                self.application_state.root_module.__name__,
            ),
            undefined=StrictUndefined,
        )

        for role, func in self.jinja_function_collection:
            if not isinstance(role, jinja_function):
                raise Exception(f"expected {jinja_function} got {role}")

            if not isinstance(func, JinjaFunction):
                raise Exception(f"expected {JinjaFunction} got {func}")

            if role.name in environment.globals:
                raise Exception(f"jinja global '{role.name}' already exists")

            environment.globals[role.name] = func

        return environment
