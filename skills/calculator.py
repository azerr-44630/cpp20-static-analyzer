from core.skill_base import Skill
import ast, operator

_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.Pow: operator.pow, ast.USub: operator.neg,
}

def _safe_eval(node):
    if isinstance(node, ast.BinOp):
        return _OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp):
        return _OPS[type(node.op)](_safe_eval(node.operand))
    if isinstance(node, ast.Constant):
        return node.value
    raise ValueError("İcazəsiz ifadə")

class Calculator(Skill):
    name = "calculator"
    description = "Sadə riyazi ifadələri hesablayır (yalnız +,-,*,/,**)"
    risk = "low"

    def run(self, expression, **kwargs):
        try:
            tree = ast.parse(expression, mode="eval")
            return f"Nəticə: {_safe_eval(tree.body)}"
        except Exception as e:
            return f"Xəta: {e}"
