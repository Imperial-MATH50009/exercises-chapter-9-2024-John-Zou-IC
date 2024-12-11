"""Write a docstring."""

import numbers as numb
from functools import singledispatch


class Expression:
    """Write a docstring."""

    def __init__(self, *oper):
        """Write a docstring."""
        self.operands = oper

    def __add__(self, other):
        """Write a docstring."""
        if isinstance(other, numb.Number):
            return Add(self, Number(other))
        return Add(self, other)

    def __radd__(self, other):
        """Write a docstring."""
        if isinstance(other, numb.Number):
            return Add(Number(other), self)
        return Add(other, self)

    def __mul__(self, other):
        """Write a docstring."""
        if isinstance(other, numb.Number):
            return Mul(self, Number(other))
        return Mul(self, other)

    def __rmul__(self, other):
        """Write a docstring."""
        if isinstance(other, numb.Number):
            return Mul(Number(other), self)
        return Mul(other, self)

    def __sub__(self, other):
        """Write a docstring."""
        if isinstance(other, numb.Number):
            return Sub(self, Number(other))
        return Sub(self, other)

    def __rsub__(self, other):
        """Write a docstring."""
        if isinstance(other, numb.Number):
            return Sub(Number(other), self)
        return Sub(other, self)

    def __truediv__(self, other):
        """Write a docstring."""
        if isinstance(other, numb.Number):
            return Div(self, Number(other))
        return Div(self, other)

    def __rtruediv__(self, other):
        """Write a docstring."""
        if isinstance(other, numb.Number):
            return Div(Number(other), self)
        return Div(other, self)

    def __pow__(self, other):
        """Write a docstring."""
        if isinstance(other, numb.Number):
            return Pow(self, Number(other))
        return Pow(self, other)

    def __rpow__(self, other):
        """Write a docstring."""
        if isinstance(other, numb.Number):
            return Pow(Number(other), self)
        return Pow(other, self)

    def __repr__(self):
        """Write a docstring."""
        raise NotImplementedError


class Terminal(Expression):
    """Write a docstring."""

    precedence = 0

    def __init__(self, val):
        """Write a docstring."""
        self.value = val
        super().__init__()

    def __repr__(self):
        """Write a docstring."""
        return f"{self.value}"

    def __str__(self):
        """Write a docstring."""
        return f"{self.value}"


class Number(Terminal):
    """Write a docstring."""

    pass


class Symbol(Terminal):
    """Write a docstring."""

    pass


class Operator(Expression):
    """Write a docstring."""

    def __init__(self, oper1, oper2):
        """Write a docstring."""
        super().__init__(oper1, oper2)

    def __repr__(self):
        """Write a docstring."""
        return type(self).__name__ + repr(self.operands)

    def __str__(self):
        """Write a docstring."""
        if self.operands[0].precedence > self.precedence:
            if self.operands[1].precedence > self.precedence:
                return f"({str(self.operands[0])}) {
                    self.symbol} ({str(self.operands[1])})"
            else:
                return f"({str(self.operands[0])}) {
                    self.symbol} {str(self.operands[1])}"
        elif self.operands[1].precedence > self.precedence:
            return f"{str(self.operands[0])} {
                self.symbol} ({str(self.operands[1])})"
        return f"{str(self.operands[0])} {self.symbol} {
            str(self.operands[1])}"


class Add(Operator):
    """Write a docstring."""

    precedence = 3
    symbol = "+"


class Mul(Operator):
    """Write a docstring."""

    precedence = 2
    symbol = "*"


class Sub(Operator):
    """Write a docstring."""

    precedence = 3
    symbol = "-"


class Div(Operator):
    """Write a docstring."""

    precedence = 2
    symbol = "/"


class Pow(Operator):
    """Write a docstring."""

    precedence = 1
    symbol = "^"


def postvisitor(expr, visitor, **kwargs):
    """Write a docstring."""
    stack = [expr]
    visited = {}
    while stack:
        e = stack.pop()
        unvisited_children = list()
        for o in e.operands:
            if o not in visited:
                unvisited_children.append(o)
        if unvisited_children:
            stack.append(e)
            for i in unvisited_children:
                stack.append(i)
        else:
            visited[e] = visitor(e, *(visited[o] for o in e.operands),
                                 **kwargs)
    return visited[expr]


@singledispatch
def differentiate(expr, *o, **kwargs):
    """Write a docstring."""
    raise NotImplementedError(
        f"Cannot differentiate a {type(expr).__name__}"
    )


@differentiate.register(Number)
def _(expr, *o, **kwargs):
    return Number(0.0)


@differentiate.register(Symbol)
def _(expr, *o, var, **kwargs):
    if str(expr) == var:
        return Number(1.0)
    return Number(0.0)


@differentiate.register(Add)
def _(expr, *o, **kwargs):
    return Add(differentiate(expr.operands[0], *o, **kwargs),
               differentiate(expr.operands[1], *o, **kwargs))


@differentiate.register(Mul)
def _(expr, *o, **kwargs):
    term1 = differentiate(expr.operands[0], *o, **kwargs) * expr.operands[1]
    term2 = differentiate(expr.operands[1], *o, **kwargs) * expr.operands[0]
    return Add(term1, term2)


@differentiate.register(Div)
def _(expr, *o, **kwargs):
    term1 = differentiate(expr.operands[0], *o, **kwargs) * expr.operands[1]
    term2 = expr.operands[0] * differentiate(expr.operands[1], *o, **kwargs)
    return (term1 - term2) / expr.operands[1] ** 2


@differentiate.register(Pow)
def _(expr, *o, **kwargs):
    term1 = differentiate(expr.operands[0], *o, **kwargs)
    term1 *= expr.operands[1] * expr.operands[0] ** (expr.operands[1] - 1)
    return term1
