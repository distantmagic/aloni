# Intention (work in progress)

Intention is a Python framework designed to simplify the development of IO-bound applications with an innovative Role-Based Services approach. 

Whether you're building web applications or other async services, Intention streamlines your development process with ease.

## Key Features

- **Role-Based Services**: Organize your services with unique roles using simple decorators like @responds_to_http. Each service in the dependency injection container plays a specific role, making your code more modular and maintainable.
- **Dependency Injection**: Manage your application's dependencies effortlessly with a container that holds one instance of each service, ensuring efficient resource management.
- **Async-First**: Built with ASGI and RSGI support, Intention is optimized for asynchronous programming, making it perfect for IO-bound tasks.
- **Developer-Friendly**: Designed to be accessible for junior developers while providing powerful features for experienced programmers.

## Suitable for Bigger Projects

Intention allows you to split your HTTP responders and other modules among multiple files, facilitating easy maintenance and scalability.

You do not have to manually combine the project files. Intention treats `role.*` decorators as metadata and puts them together for you.

```py
from intention.role import responds_to_http
from intention.http import Responder, JinjaResponse
from intention.httpfoundation import Request


@responds_to_http(pattern="/")
class Homepage(Responder):
    async def respond(self, request: Request):
        return JinjaResponse("homepage.j2")
```

## Dependency Injections

Intention allows you to inject services into your responders and other modules.

It is possible to create service providers for more advanced use cases.

```py
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
```

## Why Intention?

Intention's unique Role-Based Services approach allows for clear and organized code, facilitating collaboration and maintenance. Its async-first design ensures your applications are performant and scalable, catering to a wide range of applications beyond just web development.
