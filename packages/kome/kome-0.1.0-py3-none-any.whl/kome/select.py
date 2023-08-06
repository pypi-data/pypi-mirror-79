from typing import List, Optional, Sequence

from kome.const import JoinType, OrderType
from kome.expression import Condition, Expression
from kome.source import QueryObject, QuerySource


class Order:
    def __init__(self, expr: Expression, order: OrderType) -> None:
        self.expr = expr
        self.order = order

    def __str__(self) -> str:
        return f"{self.expr.sql} {self.order.value}"


class Join:
    def __init__(self, join_type: JoinType, source: QuerySource, on: Condition) -> None:
        self.join_type = join_type
        self.source = source
        self.on = on

    def __str__(self) -> str:
        return f"{self.join_type.value} JOIN ({self.source.sql}) ON {self.on.sql}"


class Select:
    def __init__(self) -> None:
        self.distinct_ = False
        self.select: List[Expression] = []
        self.source: Optional[QuerySource] = None
        self.join: List[Join] = []
        self.where: Optional[Condition] = None
        self.group_by: List[Expression] = []
        self.having: Optional[Condition] = None
        self.order: List[Order] = []
        self.limit: Optional[int] = None

    @property
    def sql(self):
        sql = "SELECT "
        if self.distinct_:
            sql += "DISTINCT "
        sql += ",".join(map(lambda s: s.sql, self.select))
        if not self.source:
            raise Exception("Select Query shoud call 'from_' method.")
        sql += f" FROM ({self.source.sql})"
        if self.join:
            sql += " "
            sql += " ".join(map(str, self.join))
        if self.where:
            sql += f" WHERE {self.where.sql}"
        if self.group_by:
            sql += " GROUP BY "
            sql += ",".join(map(lambda s: s.sql, self.group_by))
        if self.having:
            sql += f" HAVING {self.having.sql}"
        if self.order:
            sql += " ORDER BY "
            sql += ",".join(map(str, self.order))
        if self.limit:
            sql += f" LIMIT {self.limit}"
        return sql


class SelectMixin(QueryObject):
    _select: Select

    @property
    def query(self):
        return self._select

    @property
    def sql(self) -> str:
        return self._select.sql


class SelectClause:
    def __init__(self):
        self._select = Select()

    def from_(self, source: QuerySource):
        return SelectFrom(self._select, source)


class SelectFrom:
    def __init__(self, select: Select, source: QuerySource) -> None:
        select.source = source
        self._select = select

    def select(self, column: Expression, *columns: Expression):
        return SelectTarget(self._select, column, *columns)


class SelectTarget(SelectMixin):
    def __init__(
        self, select: Select, column: Expression, *columns: Expression
    ) -> None:
        select.select.append(column)
        select.select.extend(columns)
        self._select = select

    def distinct(self):
        return SelectDistinct(self._select)

    def left_join(
        self,
        source: QuerySource,
        on: Condition,
        selects: Optional[Sequence[Expression]] = None,
    ):
        return SelectJoin(self._select, JoinType.left, source, on, selects)

    def inner_join(
        self,
        source: QuerySource,
        on: Condition,
        selects: Optional[Sequence[Expression]] = None,
    ):
        return SelectJoin(self._select, JoinType.inner, source, on, selects)

    def where(self, condition: Condition):
        return SelectWhere(self._select, condition)

    def group_by(self, expr: Expression, *exprs: Expression):
        return SelectGroupBy(self._select, expr, *exprs)

    def order_by(self, expr: Expression, order: OrderType = OrderType.asc):
        return SelectOrderBy(self._select, expr, order)

    def limit(self, limit: int):
        return SelectLimit(self._select, limit)


class SelectDistinct(SelectMixin):
    def __init__(self, select: Select) -> None:
        select.distinct_ = True
        self._select = select

    def left_join(
        self,
        source: QuerySource,
        on: Condition,
        selects: Optional[Sequence[Expression]] = None,
    ):
        return SelectJoin(self._select, JoinType.left, source, on, selects)

    def inner_join(
        self,
        source: QuerySource,
        on: Condition,
        selects: Optional[Sequence[Expression]] = None,
    ):
        return SelectJoin(self._select, JoinType.inner, source, on, selects)

    def where(self, condition: Condition):
        return SelectWhere(self._select, condition)

    def group_by(self, expr: Expression, *exprs: Expression):
        return SelectGroupBy(self._select, expr, *exprs)

    def order_by(self, expr: Expression, order: OrderType = OrderType.asc):
        return SelectOrderBy(self._select, expr, order)

    def limit(self, limit: int):
        return SelectLimit(self._select, limit)


class SelectJoin(SelectMixin):
    def __init__(
        self,
        select: Select,
        join_type: JoinType,
        source: QuerySource,
        on: Condition,
        selects: Optional[Sequence[Expression]] = None,
    ):
        select.join.append(Join(join_type, source, on))
        if selects:
            select.select.extend(selects)
        self._select = select

    def left_join(
        self,
        source: QuerySource,
        on: Condition,
        selects: Optional[Sequence[Expression]] = None,
    ):
        return SelectJoin(self._select, JoinType.left, source, on, selects)

    def inner_join(
        self,
        source: QuerySource,
        on: Condition,
        selects: Optional[Sequence[Expression]] = None,
    ):
        return SelectJoin(self._select, JoinType.inner, source, on, selects)

    def where(self, condition: Condition):
        return SelectWhere(self._select, condition)

    def group_by(self, expr: Expression, *exprs: Expression):
        return SelectGroupBy(self._select, expr, *exprs)

    def order_by(self, expr: Expression, order: OrderType = OrderType.asc):
        return SelectOrderBy(self._select, expr, order)

    def limit(self, limit: int):
        return SelectLimit(self._select, limit)


class SelectWhere(SelectMixin):
    def __init__(self, select: Select, condition: Condition):
        select.where = condition
        self._select = select

    def group_by(self, expr: Expression, *exprs: Expression):
        return SelectGroupBy(self._select, expr, *exprs)

    def order_by(self, expr: Expression, order: OrderType = OrderType.asc):
        return SelectOrderBy(self._select, expr, order)

    def limit(self, limit: int):
        return SelectLimit(self._select, limit)


class SelectGroupBy(SelectMixin):
    def __init__(self, select: Select, expr: Expression, *exprs: Expression) -> None:
        select.group_by.append(expr)
        select.group_by.extend(exprs)
        self._select = select

    def having(self, condition: Condition):
        return SelectHaving(self._select, condition)

    def order_by(self, expr: Expression, order: OrderType = OrderType.asc):
        return SelectOrderBy(self._select, expr, order)

    def limit(self, limit: int):
        return SelectLimit(self._select, limit)


class SelectHaving(SelectMixin):
    def __init__(self, select: Select, condition: Condition) -> None:
        select.having = condition
        self._select = select

    def order_by(self, expr: Expression, order: OrderType = OrderType.asc):
        return SelectOrderBy(self._select, expr, order)

    def limit(self, limit: int):
        return SelectLimit(self._select, limit)


class SelectOrderBy(SelectMixin):
    def __init__(self, select: Select, expr: Expression, order: OrderType):
        select.order.append(Order(expr, order))
        self._select = select

    def order_by(self, expr: Expression, order: OrderType = OrderType.asc):
        return SelectOrderBy(self._select, expr, order)

    def limit(self, limit: int):
        return SelectLimit(self._select, limit)


class SelectLimit(SelectMixin):
    def __init__(self, select: Select, limit: int) -> None:
        if limit < 1:
            raise SelectLimit.SelectLimitError(limit)
        select.limit = limit
        self._select = select

    class SelectLimitError(Exception):
        def __init__(self, limit: int) -> None:
            super().__init__(f"Limt must be positive integer. But got {limit}")
