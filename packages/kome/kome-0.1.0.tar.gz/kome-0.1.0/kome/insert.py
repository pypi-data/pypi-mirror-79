from typing import List, Optional, Union

from kome.expression import BasicExpression, P, Premitive, force_expression
from kome.field import Field
from kome.source import QueryObject
from kome.table import BasicTable
from kome.utils import format_quotes

InsertableValue = Union[Premitive, P]
# query
"""
INSERT INTO テーブル名 [ (列名1 [ ,列名2・・・]) ]
VALUES (値A1 [, 値A2 ...]) [, (値B1 [, 値B2 ...]) ...];
"""


class Insert:
    def __init__(self) -> None:
        self.table: Optional[BasicTable] = None
        self.fields: List[Field] = []
        self.values: List[List[BasicExpression]] = []

    @property
    def sql(self) -> str:
        if self.table is None:
            raise RuntimeError("Insert Query shoud call 'into'")
        sql = f"INSERT INTO {self.table.sql} ({','.join(map(lambda v:format_quotes(v.field_name) ,self.fields))}) VALUES "
        sql += ",".join(
            map(lambda v: "(" + ",".join(map(lambda k: k.sql, v)) + ")", self.values)
        )
        return sql


class InsertMixin(QueryObject):
    _insert: Insert

    @property
    def query(self):
        return self._insert

    @property
    def sql(self) -> str:
        return self._insert.sql


class InsertClause:
    def __init__(self) -> None:
        self._insert = Insert()

    def into(self, table: BasicTable):
        return InsertInto(self._insert, table)


class InsertInto:
    def __init__(self, insert: Insert, table: BasicTable) -> None:
        insert.table = table
        self._insert = insert

    def columns(self, field: Field, *fields: Field):
        return InsertColumns(self._insert, field, *fields)


class InsertColumns:
    def __init__(self, insert: Insert, field: Field, *fields: Field) -> None:
        insert.fields.append(field)
        insert.fields.extend(fields)
        self._insert = insert

    def values(self, value: InsertableValue, *values: InsertableValue):
        return InsertValues(self._insert, value, *values)


class InsertValues(InsertMixin):
    def __init__(
        self, insert: Insert, value: InsertableValue, *values: InsertableValue
    ) -> None:
        if len(insert.fields) != 1 + len(values):
            raise ValueError(
                f"inser value length not match. \n\t{insert.fields=}\n\tvalues={(value,*values)}"
            )
        insert.values.append(list(map(force_expression, [value, *values])))
        self._insert = insert

    def values(self, value: InsertableValue, *values: InsertableValue):
        return InsertValues(self._insert, value, *values)
