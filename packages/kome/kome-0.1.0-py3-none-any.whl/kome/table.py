from typing import Union

from kome.source import AliasedQuerySource, BasicQuerySource
from kome.utils import format_quotes


class BasicTable(BasicQuerySource):
    def __init__(self, table_name: str) -> None:
        self.table_name = table_name

    def as_(self, alias: str):
        return AliasedTable(self, alias)

    @property
    def sql(self) -> str:
        return f"{format_quotes(self.table_name)}"


class AliasedTable(AliasedQuerySource):
    def __init__(self, table: BasicTable, alias: str) -> None:
        self.table = table
        self.alias = alias

    @property
    def sql(self) -> str:
        return f"{self.table.sql} AS {format_quotes(self.alias)}"


Table = Union[BasicTable, AliasedTable]
