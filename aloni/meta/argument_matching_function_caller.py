from typing import Any, Awaitable, Callable, List, Mapping, TypeVar

from .function_parameter_store import FunctionParameterStore

TReturn = TypeVar("TReturn")


class ArgumentMatchingFunctionCaller:
    def __init__(
        self,
        function_parameter_store: FunctionParameterStore,
        args: Mapping[str, Any],
    ) -> None:
        self.args = args
        self.cached_param_names: dict[
            Callable[..., Any],
            List[str],
        ] = {}
        self.function_parameter_store = function_parameter_store

    async def call_async_function(
        self, func: Callable[..., Awaitable[TReturn]]
    ) -> TReturn:
        return await func(**self.prepare_arguments(func))

    def call_function(self, func: Callable[..., TReturn]) -> TReturn:
        return func(**self.prepare_arguments(func))

    def prepare_arguments(self, func: Callable[..., Any]) -> dict[str, Any]:
        func_args: dict[str, Any] = {}
        params = self.function_parameter_store.cached_get_params(func)

        if isinstance(self.args, dict):
            for param in params:
                if param.name in self.args:
                    func_args[param.name] = self.args[param.name]
        else:
            for param in params:
                if hasattr(self.args, param.name):
                    func_args[param.name] = getattr(self.args, param.name)

        return func_args
