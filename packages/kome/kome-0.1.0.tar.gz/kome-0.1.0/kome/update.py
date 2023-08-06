from typing import List, Optional

from kome.expression import BasicExpression, Condition, PyExpression, force_expression
from kome.field import Field
from kome.source import QueryObject
from kome.table import Table


class UpdateSet:
    def __init__(self, field: Field, expr: BasicExpression) -> None:
        self.field = field
        self.expr = expr

    def __str__(self) -> str:
        return f"{self.field.sql}={self.expr.sql}"


class Update:
    def __init__(self) -> None:
        self.table: Optional[Table] = None
        self.sets: List[UpdateSet] = []
        self.where: Optional[Condition] = None

    @property
    def sql(self):
        if not self.table:
            raise RuntimeError("Update Query shoud call 'from_'")
        sql = f"UPDATE {self.table.sql} SET {','.join(map(str, self.sets))}"
        if self.where:
            sql += f" WHERE {self.where.sql}"
        return sql


class UpdateMixin(QueryObject):
    _update: Update

    @property
    def query(self):
        return self._update

    @property
    def sql(self) -> str:
        return self._update.sql


class UpdateClause:
    def __init__(self) -> None:
        self._update = Update()

    def from_(self, table: Table):
        return UpdateFrom(self._update, table)


class UpdateFrom:
    def __init__(self, update: Update, table: Table) -> None:
        update.table = table
        self._update = update

    def set(self, field: Field, expr: PyExpression):
        return UpdateValue(self._update, field, expr)


class UpdateValue(UpdateMixin):
    def __init__(self, update: Update, field: Field, expr: PyExpression) -> None:
        update.sets.append(UpdateSet(field, force_expression(expr)))
        self._update = update

    def set(self, field: Field, expr: PyExpression):
        return UpdateValue(self._update, field, expr)

    def where(self, condition: Condition):
        return UpdateWhere(self._update, condition)


class UpdateWhere(UpdateMixin):
    def __init__(self, update: Update, condition: Condition) -> None:
        update.where = condition
        self._update = update
