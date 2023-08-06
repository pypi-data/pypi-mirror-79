from typing import Union

from kome.const import Comparator, Equality
from kome.source import QueryObject
from kome.utils import format_quotes

Premitive = Union[str, int, float, bool]
PyExpression = Union[Premitive, "BasicExpression"]


def force_expression(value: PyExpression):
    if isinstance(value, BasicExpression):
        return value
    if isinstance(value, (str, int, bool, float)):
        return PyPremitiveExpression(value)
    raise Exception(f"not support, {value}")


class BasicExpression(QueryObject):
    def as_(self, alias: str):
        return AliasedExpression(self, alias)

    def __eq__(self, o: PyExpression):
        return Condition(self, force_expression(o), Equality.eq)

    def __ne__(self, o: PyExpression):
        return Condition(self, force_expression(o), Equality.ne)

    def __gt__(self, o: PyExpression):
        return Condition(self, force_expression(o), Equality.gt)

    def __gte__(self, o: PyExpression):
        return Condition(self, force_expression(o), Equality.gte)

    def __lt__(self, o: PyExpression):
        return Condition(self, force_expression(o), Equality.lt)

    def __lte__(self, o: PyExpression):
        return Condition(self, force_expression(o), Equality.lte)


class PyPremitiveExpression(BasicExpression):
    def __init__(self, value: Premitive) -> None:
        self.value = value

    @property
    def sql(self) -> str:
        if isinstance(self.value, bool):
            return "TRUE" if self.value else "FALSE"
        if isinstance(self.value, str):
            return f"'{self.value}'"
        if isinstance(self.value, int):
            return str(self.value)
        raise Exception(f"wait for support. {type(self.value)}")


class AliasedExpression(QueryObject):
    def __init__(self, expr: BasicExpression, alias: str) -> None:
        self.expr = expr
        self.alias = alias

    @property
    def sql(self) -> str:
        return f"{self.expr.sql} AS {format_quotes(self.alias)}"


Expression = Union[BasicExpression, AliasedExpression]


class Condition(BasicExpression):
    def __init__(
        self, left: BasicExpression, right: BasicExpression, comparator: Comparator
    ) -> None:
        self.left = left
        self.right = right
        self.comparator = comparator

    @property
    def sql(self) -> str:
        return f"{self.left.sql}{self.comparator.value}{self.right.sql}"


class P(BasicExpression):
    def __init__(self, placeholder: str) -> None:
        self.placeholder = placeholder

    @property
    def sql(self) -> str:
        return str(self.placeholder)
