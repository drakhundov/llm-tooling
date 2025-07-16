import inspect
from typing import Callable, List, get_type_hints


class Tool:
    """
    A class representing a reusable piece of code (Tool).

    Attributes:
        name (str): Name of the tool.
        description (str): A textual description of what the tool does.
        func (callable): The function this tool wraps.
        arguments (list): A list of arguments.
        outputs (str or list): The return type(s) of the wrapped function.
    """

    def __init__(
        self, name: str, description: str, func: Callable, arguments: List, outputs: str
    ):
        self.name = name
        self.description = description
        self.func = func
        self.arguments = arguments
        self.outputs = outputs

    def to_string(self) -> str:
        """
        Return a string representation of the tool,
        including its name, description, arguments, and outputs.
        """
        args_str = ", ".join(
            [f"{arg_name}: {arg_type}" for arg_name, arg_type in self.arguments]
        )

        return (
            f"Tool Name: {self.name},"
            f" Description: {self.description},"
            f" Arguments: {args_str},"
            f" Outputs: {self.outputs}"
        )

    def __call__(self, *args, **kwargs):
        """
        Invoke the underlying function (callable) with provided arguments.
        """
        return self.func(*args, **kwargs)


def __convert_type(_type):
    """Convert a type (like int, str) into a string,"""
    return _type.__name__ if hasattr(_type, '__name__') else str(_type)


def __parse_args(func):
    """
    Takes a function and returns:
    - a tuple with function parameters metadata (name, type)
    - function output type.
    """
    signature = inspect.signature(func)
    parameters = get_type_hints(func)
    args = []
    for name, param in signature.parameters.items():
        param_type = parameters.get(name, "Any")
        args.append((name, __convert_type(param_type)))
    return args, __convert_type(signature.return_annotation)


def agent_tool(func):
    """
    A decorator used to convert a regular function into a Tool class.
    It is required so that the agent could be informed about the tools it could use.
    """
    args, output_type = __parse_args(func)
    return Tool(
        func.__name__,         # name
        func.__doc__,          # description
        func,                  # function to call
        args,                  # inputs (names and types)
        output_type,           # output
    )
