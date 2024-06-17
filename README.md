# Intention

Intention is a Python framework designed to increase productivity when developing applications. Simplicity, productivity, and great developer experience are our primary goals.

It is based on an innovative Role-Based Services approach. You can del (more info below).

It is async and thus performs well with IO-bound services (for example, anything that makes a lot of long-running HTTP calls to large language models or uses a lot of microservices and third-party services)—but not just those.

## Try it out

Intention will take only a few minutes to set up, and it might amaze you and change how you develop apps. :)

## Key Features

- **Effortlessly split your project into multiple files**: Intention automatically combines your project files based on the roles you assign them, making it easy to manage large projects.
- **Dependency Injection**: Manage your application's dependencies effortlessly with a container that holds one instance of each service, ensuring efficient resource management.
- **Async-First**: Intention is optimized for asynchronous programming, making it perfect for IO-bound tasks.
- **Minial boilerplate**: Intention adds no redundant boilerplate code. Keep your project as simple as possible.

## Installation

### Requirements

Linux or MacOS (should work on all Unix systems). It currently doesn't work on Windows because it requires `fork` multiprocessing method (which Windows does not have).

Windows support might be added in the future.

### Steps

Intention works best with [Poetry](https://python-poetry.org/). Install [Poetry](https://python-poetry.org/) first and follow the steps:

1. Create a new project. Invoke the command and fill in the project creation form:  
    ```shell
    poetry init my_app
    ```
2. In the project's directory (the one with the newly created `pyproject.toml`) open:  
    ```shell
    poetry shell
    ```
3. Install Intention locally in the project:  
    ```shell
    poetry add intention
    ```
4. Create your application's module:  
    ```shell
    mkdir my_app
    ```
    ```shell
    touch my_app/__init__.py
    ```
5. Create the `app.py` (primary application file). That is the entire boilerplate code that Intention needs to work:  
    ```py
    import my_app
    import intention

    intention.start(my_app).exit_after_finishing()
    ```

Invoking `python ./app.py` should display something like:

```shell
usage: app.py [-h] {hello,serve} ...

Intention CLI

positional arguments:
  {serve}
    serve        Start the app in HTTP server mode

options:
  -h, --help     show this help message and exit
```

Congratulations! You have installed the Intention project. You can continue with the next steps.

## Usage

Check the [demo project](/examples/demo-app) for basic usage.

Intention will scan your module (in this case, `my_app`) for services with a role decorator and start your CLI application. That's it!

If you want to start developing something new, add a new CLI command. Use `responds_to_cli` role. Add a new file in `my_app/hello_command.py` (file name can be anything; it's just an example - file names and directory structure do not matter for Intention):

```py
from intention.cli_foundation import Command
from intention.role import responds_to_cli


@responds_to_cli(
    name="hello",
    description="Say hello!",
)
class Hello(Command):
    def respond(self) -> int:
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

## Why Intention?

Intention's unique Role-Based Services approach allows for clear and organized code. It scans your project for services decorated as `roles` and automatically combines them. It takes care of all the tedious work and allows you to focus on the application architecture.

### Suitable for Bigger Projects

Intention allows you to split your HTTP responders and other modules among multiple files.

You do not have to manually combine the project files. Intention treats `role.*` decorators as metadata and puts them together for you.

```py
from intention.role import responds_to_http
from intention.http import Responder, JinjaResponse
from intention.http_foundation import Request


@responds_to_http(pattern="/")
class Homepage(Responder):
    async def respond(self, request: Request):
        return JinjaResponse("homepage.j2")
```

### Dependency Injection

Intention allows you to inject services into your responders and other modules.

It is possible to create service providers for more advanced use cases.

```py
from intention.role import service_provider
from intention.service_provider.service_provider import ServiceProvider
from jinja2 import Environment, PackageLoader, select_autoescape


@service_provider(provides=Environment)
class JinjaEnvironmentServiceProvider(ServiceProvider[Environment]):
    def provide(self) -> Environment:
        return Environment(
            auto_reload=False,
            enable_async=True,
            loader=PackageLoader('mymodule'),
            autoescape=select_autoescape(),
        )
```

Then, you can inject the service into your responders and other modules. 

No further configuration is needed (just the type hint).

```py
from intention.role import service
from jinja2 import Environment


@service
class MyService:
    def __init__(self, env: Environment):
        self.env = env

    async def render_something(self):
        return self.env.get_template('foo.j2').render()
```

## Available Roles

All the available roles are accessible from `intention.role` module. 

For example:

```py
from intention.role import responds_to_http
```

| Role | Description |
| ------------- | ------------- |
| [intercepts_http_response](intention/role/intercepts_http_response.py) | Allows to intercept any response returned by your http responder and convert it into a renderable response. It acts kind of like inversed middleware - instead of intercepting a request, it intercepts and modifies a response. |
| [responds_to_cli](intention/role/responds_to_cli.py) | Responds to CLI command |
| [responds_to_http](intention/role/responds_to_http.py) | Responds to HTTP request |
| [service](intention/role/service.py) | Marks the current class as a service. Its constructor arguments will be injected from the dependency injection container |
| [service_provider](intention/role/service_provider.py) | Registers a service provider for dependency injection. Use it if you want to create a class that provides an instance of a different class to the dependency injection container. |

## Special Thanks

- [Granian](https://github.com/emmett-framework/granian) for creating an awesome HTTP Python runner with excellent performance

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
