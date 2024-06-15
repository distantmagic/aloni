from typing import Any, Dict, Generic, Protocol, Tuple, TypeVar

TReturn = TypeVar("TReturn", covariant=True)


class AsyncResponderProtocol(Generic[TReturn], Protocol):
    async def respond(
        self,
        *args: Tuple[Any, ...],
        **kwargs: Dict[str, Any],
    ) -> TReturn: ...
