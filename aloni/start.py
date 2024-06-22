import argparse
import asyncio
from types import ModuleType
from typing import Iterable, Tuple, Type
from natsort import natsorted

from .application_mode import ApplicationMode
from .application_run_result import ApplicationRunResult
from .application_state import ApplicationState
from .cli import *  # noqa: F403
from .cli_foundation.command import Command
from .cli_foundation.command_option import CommandOption
from .dependency_injection_container import DependencyInjectionContainer
from .import_all_from import import_all_from
from .jinja_function import *  # noqa: F403
from .meta.argument_matching_function_caller import ArgumentMatchingFunctionCaller
from .meta.function_parameter_store import FunctionParameterStore
from .meta.is_responder import is_responder
from .role.responds_to_cli import responds_to_cli
from .role.role import Role
from .role.role_registry import RoleRegistry
from .role.role_regsitry_global import role_registry_global
from .service_provider import *  # noqa: F403


def get_sorted_roles(
    role_registry: RoleRegistry[Role],
) -> Iterable[Tuple[responds_to_cli, Type[Command]]]:
    return natsorted(
        role_registry_global.filter_by_role_class(responds_to_cli),
        key=lambda x: x[0].name,
    )


async def start_async(
    module: ModuleType,
    role_registry: RoleRegistry[Role] = role_registry_global,
) -> ApplicationRunResult:
    import_all_from(module)

    di = DependencyInjectionContainer(role_registry=role_registry)

    await di.prepare()

    di.register_instance(
        ApplicationState,
        ApplicationState(
            mode=ApplicationMode.CLI,
            root_module=module,
        ),
    )

    parser = argparse.ArgumentParser(description="Aloni CLI")
    subparsers = parser.add_subparsers(dest="command")

    available_commands: dict[str, Type[Command]] = {}

    for role, wrapped_class in get_sorted_roles(role_registry):
        available_commands[role.name] = wrapped_class
        subparser = subparsers.add_parser(role.name, help=role.description)

        for option in role.options:
            if not isinstance(option, CommandOption):
                raise ValueError(f"Expected {CommandOption}, got {type(option)}")

            subparser.add_argument(
                option.name,
                type=option.type,
                help=option.help,
                default=option.default,
                required=option.required,
            )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()

        return ApplicationRunResult(exit_code=0)

    if args.command not in available_commands:
        raise ValueError(f"Command {args.command} not found")

    command = await di.make(available_commands[args.command])

    if not is_responder(command):
        raise NotImplementedError(
            f"command {args.command} must have a 'respond' method that returns an int"
        )

    args_dict = vars(args)
    exit_code = await ArgumentMatchingFunctionCaller(
        args=args_dict,
        function_parameter_store=await di.make(FunctionParameterStore),
    ).call_async_function(command.respond)

    if not isinstance(exit_code, int):
        raise ValueError(f"expected int as exit code, got {type(exit_code)}")

    return ApplicationRunResult(exit_code=exit_code)


def start(
    module: ModuleType,
    role_registry: RoleRegistry[Role] = role_registry_global,
) -> ApplicationRunResult:
    loop = asyncio.get_event_loop()

    return loop.run_until_complete(start_async(module, role_registry))
