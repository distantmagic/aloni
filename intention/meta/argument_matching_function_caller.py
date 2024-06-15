import inspect
from typing import Any, Callable, TypeVar

TReturn = TypeVar("TReturn")


class ArgumentMatchingFunctionCaller:
    def __init__(self, args: Any) -> None:
        self.args = args

    def call_function(self, func: Callable[..., TReturn]) -> TReturn:
        sig = inspect.signature(func)
        params = sig.parameters

        if isinstance(self.args, dict):
            func_args = {name: self.args[name] for name in params if name in self.args}
        else:
            func_args = {
                name: getattr(self.args, name)
                for name in params
                if hasattr(self.args, name)
            }

        return func(**func_args)
