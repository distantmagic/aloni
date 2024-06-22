# Aloni

Aloni is a Python framework designed to increase productivity when developing applications. Simplicity, productivity, and great developer experience are our primary goals.

It is based on an innovative Role-Based Services approach. (more info below).

It is async and thus performs well with IO-bound services (for example, anything that makes a lot of long-running HTTP calls to large language models or uses a lot of microservices and third-party services)—but not just those.

## Try it out

Aloni will take only a few minutes to set up, and it might amaze you and change how you develop apps. :)

## Key Features

- **Effortlessly split your project into multiple files**: Aloni automatically combines your project files based on the roles you assign them, making it easy to manage large projects.
- **Dependency Injection**: Manage your application's dependencies effortlessly with a container that holds one instance of each service, ensuring efficient resource management.
- **Async-First**: Aloni is optimized for asynchronous programming, making it perfect for IO-bound tasks.
- **Minial boilerplate**: Aloni adds no redundant boilerplate code. Keep your project as simple as possible.

## Getting Started

### Installation

#### Requirements

Linux or MacOS (should work on all Unix systems). It does not work on Windows because Aloni requires the `fork` multiprocessing method (which Windows does not have).

That might change in the future (see also: https://github.com/emmett-framework/granian/issues/330).

#### Steps

Aloni works best with [Poetry](https://python-poetry.org/). Install [Poetry](https://python-poetry.org/) first and follow the steps:

1. Create a new Poetry project, then install Aloni:  
    ```shell
    poetry add aloni
    ```
2. Create your application's module:  
    ```shell
    mkdir my_app
    ```
    ```shell
    touch my_app/__init__.py
    ```
3. Create the `app.py` (primary application file). That is the entire boilerplate code that Aloni needs to work:  
    ```py
    import my_app
    import aloni

    aloni.start(my_app).exit_after_finishing()
    ```

Invoking `poetry run python ./app.py` should display something like:

```shell
usage: app.py [-h] {hello,serve} ...

Aloni CLI

positional arguments:
  {serve}
    serve        Start the app in HTTP server mode

options:
  -h, --help     show this help message and exit
```

Congratulations! You have installed the Aloni project. You can continue with the next steps.

### Usage

Check the [demo project](/examples/demo-app) for basic usage.

Aloni will scan your module (in this case, `my_app`) for services with a role decorator and start your CLI application. That's it!

Add a new CLI command if you want to start developing something new. Use `responds_to_cli` role. Add a new file in `my_app/hello_command.py` (file name can be anything; it's just an example - file names and directory structure do not matter for Aloni):

```py
from aloni.cli_foundation import Command
from aloni.role import responds_to_cli


@responds_to_cli(
    name="hello",
    description="Say hello!",
)
class Hello(Command):
    async def respond(self) -> int:
        print("Hello, World!")

        return 0
```

You can then run it with:

```shell
python ./app.py hello
```

You should see:

```
Hello, World!
```

## Quick Tutorials

### Responding to HTTP Requests

Create a responder in your application's module. Filename and location do not matter:

```py
from aloni.http import Responder, TextResponse
from aloni.role import responds_to_http


@responds_to_http(path='/ping')
class Ping(Responder):
    async def respond(self) -> TextResponse:
        return TextResponse("pong")
```

### Responding with Jinja2 Templates

Place a template inside your application's `templates` directory. Name it `hello.j2`:

```html
<p>Hello, world!</p>
```

```py
from aloni.http import Responder, JinjaResponse
from aloni.role import responds_to_http


@responds_to_http(path='/hello')
class Hello(Responder):
    async def respond(self) -> JinjaResponse:
        return JinjaResponse('hello.j2')
```

### Injecting Services

Create a service in your application's module. Filename and location do not matter:

```py
from aloni.role import service


@service
class MyService:
    pass
```

Use it in your other services:

```py
from aloni.role import service

from .my_service import MyService


@service
class OtherService:
    def __init__(self, my_service: MyService) -> None:
        self.my_service = my_service
```

### Creating Service Providers

Create a base service class in your application's module. Do not add `@service` role to that class:

```py
class MyService:
    def __init__(self, foo: str) -> None:
        self.foo = foo
```

Create service provider (again, location and filename do not matter as long as it's in your application's module):

```py
from aloni.application_state import ApplicationState
from aloni.role import service_provider
from aloni.service_provider import ServiceProvider

from .my_service import MyService


@service_provider(provides=MyService)
class MyServiceProvider(ServiceProvider[MyService]):
    def provide(self) -> MyService:
        return MyService(foo="bar")
```

Use it in your other services:

```py
from aloni.role import service

from .my_service import MyService


@service
class OtherService:
    def __init__(self, my_service: MyService) -> None:
        self.my_service = my_service
```

### Registering Jinja Functions

Custom Jinja functions have their constructor (`__init__`) arguments injected by the dependency injection container.

Arguments passed to the `__call__` method are passed from a template.

```py
from aloni.jinja_function import JinjaFunction
from aloni.role.jinja_function import jinja_function


@jinja_function(name="say_hello")
class UrlFor(JinjaFunction):
    def __call__(self) -> str:
        return "Hello, world!"
```

Then use it in a template:

```j2
{{ say_hello() }}
```

## API Reference

### HTTP Responses

All the available roles are accessible from `aloni.http` module. 

For example:

```py
from aloni.http import AssetResponse
```

| Response | Description |
| ------------- | ------------- |
| [AssetResponse](aloni/http/asset_response.py) | Returns an asset file if it is present inside your application's `assets` directory |
| [JinjaResponse](aloni/http/jinja_response.py) | Returns a parsed Jinja2 template if it is present inside your application's `templates` directory |
| [TextResponse](aloni/http/text_response.py) | Returns a plain text response |

### Available Roles

All the available roles are accessible from `aloni.role` module. 

For example:

```py
from aloni.role import responds_to_http
```

| Role | Description |
| ------------- | ------------- |
| [intercepts_http_response](aloni/role/intercepts_http_response.py) | Allows to intercept any response returned by your http responder and convert it into a renderable response. It acts kind of like inversed middleware - instead of intercepting a request, it intercepts and modifies a response. |
| [responds_to_cli](aloni/role/responds_to_cli.py) | Responds to CLI command |
| [responds_to_http](aloni/role/responds_to_http.py) | Responds to HTTP request |
| [service](aloni/role/service.py) | Marks the current class as a service. Its constructor arguments will be injected from the dependency injection container |
| [service_provider](aloni/role/service_provider.py) | Registers a service provider for dependency injection. Use it to create a class that provides an instance of a different class to the dependency injection container. |

## Special Thanks

- [Granian](https://github.com/emmett-framework/granian) for creating an awesome HTTP Python runner with excellent performance

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
