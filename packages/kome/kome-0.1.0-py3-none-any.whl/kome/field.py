from typing import Optional

from kome.expression import BasicExpression
from kome.table import AliasedTable, Table
from kome.utils import format_quotes


class Field(BasicExpression):
    def __init__(self, field_name: str, table: Optional[Table] = None):
        self.field_name = field_name
        self.table = table

    @property
    def sql(self) -> str:
        if self.table is None:
            return format_quotes(self.field_name)
        if isinstance(self.table, AliasedTable):
            return f"{format_quotes(self.table.alias)}.{format_quotes(self.field_name)}"
        return f"{self.table.sql}.{format_quotes(self.field_name)}"
