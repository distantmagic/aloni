import inspect
from typing import Any, Callable, List

from .function_parameter import FunctionParameter
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
        self.cached_params: dict[
            Callable[..., Any],
            List[FunctionParameter],
        ] = {}

    def cached_get_params(
        self,
        func: Callable[..., Any],
    ) -> List[FunctionParameter]:
        if func in self.cached_params:
            return self.cached_params[func]

        sig = inspect.signature(func)

        params = sig.parameters
        param_names: list[FunctionParameter] = []

        for param in params.values():
            if param.name == "self":
                continue

            param_names.append(
                FunctionParameter(
                    annotation=param.annotation,
                    name=param.name,
                )
            )

        self.cached_params[func] = param_names

        return param_names
