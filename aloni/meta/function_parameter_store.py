import inspect
from typing import Any, Callable, List
from ..role.service import service


# using inspect cases a lot of unpleasant performance issues, it also disturbs
# the JIT if you are using a version of python that supports it
# this parameter used to eliminate the need to use inspect during the
# application runtime
@service
class FunctionParameterStore:
    def __init__(
        self,
    ) -> None:
        self.cached_param_names: dict[
            Callable[..., Any],
            List[str],
        ] = {}

    def cached_get_param_names(
        self,
        func: Callable[..., Any],
    ) -> List[str]:
        if func in self.cached_param_names:
            return self.cached_param_names[func]

        sig = inspect.signature(func)

        params = sig.parameters
        param_names = []

        for param in params.values():
            if param.name == "self":
                continue

            param_names.append(param.name)

        self.cached_param_names[func] = param_names

        return param_names
