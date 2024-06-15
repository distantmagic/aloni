from typing import Any, TypeGuard

from .responder_protocol import ResponderProtocol


def is_responder(cls: Any) -> TypeGuard[ResponderProtocol[Any]]:
    method = getattr(cls, "respond", None)

    if not method or not callable(method):
        return False

    return True
