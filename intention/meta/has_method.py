import inspect
from typing import Any, Type, TypeGuard, TypeVar

from ..cli.command_protocol import CommandProtocol

TReturn = TypeVar("TReturn")


def has_method(
    cls: Any, name: str, return_type: Type[TReturn]
) -> TypeGuard[CommandProtocol[TReturn]]:
    method = getattr(cls, name, None)

    if not method or not callable(method):
        return False

    sig = inspect.signature(method)

    if sig.return_annotation is not return_type:
        return False

    return True
