"""
Tool: calculator — safe arithmetic via AST, no eval().
"""

from __future__ import annotations

import ast
import operator
from typing import Any

from pydantic import BaseModel

from murphyx.tools.base import ToolResult, run_with_timeout

_OPS: dict[type, Any] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


class CalculatorInput(BaseModel):
    expression: str


class CalculatorOutput(BaseModel):
    result: float


def _safe_eval(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_safe_eval(node.operand))
    raise ValueError(f"unsupported expression node: {ast.dump(node)}")


async def _calc(inp: CalculatorInput) -> CalculatorOutput:
    tree = ast.parse(inp.expression, mode="eval")
    return CalculatorOutput(result=_safe_eval(tree))


async def execute(inp: CalculatorInput, timeout: float = 5.0) -> ToolResult:
    return await run_with_timeout(_calc(inp), timeout=timeout, tool_name="calculator")
