from typing import Optional
import unittest
from types import SimpleNamespace

from .argument_matching_function_caller import ArgumentMatchingFunctionCaller
from .function_parameter_store import FunctionParameterStore

function_parameter_store = FunctionParameterStore()


def handle_command1(arg1: str, arg2: Optional[str] = None) -> str:
    return f"handle_command1 called with arg1={arg1} and arg2={arg2}"


def handle_command2(arg1: str, arg2: str, arg3: Optional[str] = None) -> str:
    return f"handle_command2 called with arg1={arg1}, arg2={arg2}, and arg3={arg3}"


class TestArgumentMatchingFunctionCaller(unittest.TestCase):
    def test_call_function_with_dict_args(self) -> None:
        args_dict = {"arg1": "value1", "arg2": "value2"}
        caller = ArgumentMatchingFunctionCaller(
            args=args_dict,
            function_parameter_store=function_parameter_store,
        )

        result1 = caller.call_function(handle_command1)
        self.assertEqual(
            result1, "handle_command1 called with arg1=value1 and arg2=value2"
        )

        result2 = caller.call_function(handle_command2)
        self.assertEqual(
            result2,
            "handle_command2 called with arg1=value1, arg2=value2, and arg3=None",
        )

    def test_call_function_with_object_args(self) -> None:
        args_obj = SimpleNamespace(arg1="value1", arg2="value2")
        caller = ArgumentMatchingFunctionCaller(
            args=vars(args_obj),
            function_parameter_store=function_parameter_store,
        )

        result1 = caller.call_function(handle_command1)
        self.assertEqual(
            result1, "handle_command1 called with arg1=value1 and arg2=value2"
        )

        result2 = caller.call_function(handle_command2)
        self.assertEqual(
            result2,
            "handle_command2 called with arg1=value1, arg2=value2, and arg3=None",
        )

    def test_call_function_with_partial_args(self) -> None:
        args_dict = {"arg1": "value1"}
        caller = ArgumentMatchingFunctionCaller(
            args=args_dict,
            function_parameter_store=function_parameter_store,
        )

        result1 = caller.call_function(handle_command1)
        self.assertEqual(
            result1, "handle_command1 called with arg1=value1 and arg2=None"
        )

    def test_call_function_with_extra_args(self) -> None:
        args_dict = {"arg1": "value1", "arg2": "value2", "arg4": "extra_value"}
        caller = ArgumentMatchingFunctionCaller(
            args=args_dict,
            function_parameter_store=function_parameter_store,
        )

        result1 = caller.call_function(handle_command1)
        self.assertEqual(
            result1, "handle_command1 called with arg1=value1 and arg2=value2"
        )

        result2 = caller.call_function(handle_command2)
        self.assertEqual(
            result2,
            "handle_command2 called with arg1=value1, arg2=value2, and arg3=None",
        )


if __name__ == "__main__":
    unittest.main()
