from typing import Any, Dict, Generic, Protocol, Tuple, TypeVar

TReturn = TypeVar("TReturn", covariant=True)


class CommandProtocol(Generic[TReturn], Protocol):
    def respond(
        self,
        *args: Tuple[Any, ...],
        **kwargs: Dict[str, Any],
    ) -> TReturn: ...
