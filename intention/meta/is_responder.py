import inspect
from typing import Any, Type, TypeGuard, TypeVar

from .responder_protocol import ResponderProtocol

TReturn = TypeVar("TReturn")


def is_responder(
    cls: Any, return_type: Type[TReturn]
) -> TypeGuard[ResponderProtocol[TReturn]]:
    method = getattr(cls, "respond", None)

    if not method or not callable(method):
        return False

    sig = inspect.signature(method)

    if sig.return_annotation is not return_type:
        return False

    return True
