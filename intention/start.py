import argparse
from types import ModuleType
from typing import Any, Iterable, Tuple, Type
from natsort import natsorted

from .application_mode import ApplicationMode
from .application_state import ApplicationState
from .cli.command import Command
from .cli.command_option import CommandOption
from .dependency_injection_container import DependencyInjectionContainer
from .import_all_from import import_all_from
from .meta.argument_matching_function_caller import ArgumentMatchingFunctionCaller
from .meta.has_method import has_method
from .role.responds_to_cli_wrapped import responds_to_cli_wrapped
from .role.role import Role
from .role.role_registry import RoleRegistry
from .role.role_regsitry_global import role_registry_global
from .service_provider import *  # noqa: F403


def get_sorted_roles(
    role_registry: RoleRegistry[Role[Any]],
) -> Iterable[Tuple[responds_to_cli_wrapped, Type[Command]]]:
    return natsorted(
        role_registry_global.filter_by_role_class(responds_to_cli_wrapped),
        key=lambda x: x[0].name,
    )


def start(
    module: ModuleType,
    role_registry: RoleRegistry[Role[Any]] = role_registry_global,
) -> int:
    import_all_from(module)

    di = DependencyInjectionContainer(role_registry=role_registry)
    di.prepare()
    di.register_instance(
        ApplicationState,
        ApplicationState(
            mode=ApplicationMode.CLI,
            root_module=module,
        ),
    )

    parser = argparse.ArgumentParser(description="Intention CLI")
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

        return 0

    if args.command not in available_commands:
        raise Exception(f"Command {args.command} not found")

    command = di.make(available_commands[args.command])

    if not has_method(command, name="respond", return_type=int):
        raise NotImplementedError(
            "command must have a 'respond' method that returns an int"
        )

    return ArgumentMatchingFunctionCaller(args).call_function(command.respond)
