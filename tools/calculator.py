from enum import IntEnum
from typing import Optional
from tooling import agent_tool


class Operation(IntEnum):
    ADD = 1
    SUBTRACT = 2
    MULTIPLY = 3
    DIVIDE = 4


@agent_tool
def calculator(a: int, b: int, op: Operation) -> Optional[int]:
    """
    Calculate simple arithmetic expressions involving two operands and an operator.
    The operator is specified by a number:
    - Add: 1
    - Subtract: 2
    - Multiply: 3
    - Divide: 4
    """
    if op == Operation.ADD:
        return a + b
    elif op == Operation.SUBTRACT:
        return a - b
    elif op == Operation.MULTIPLY:
        return a * b
    elif op == Operation.DIVIDE:
        return a // b if b != 0 else None
    return None
