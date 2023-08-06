from typing import Optional

from kome.expression import Condition
from kome.source import QueryObject
from kome.table import BasicTable, Table
from kome.utils import format_quotes


class Delete:
    def __init__(self) -> None:
        self.table: Optional[Table] = None
        self.where: Optional[Condition] = None

    @property
    def sql(self) -> str:
        if self.table is None:
            raise RuntimeError("Delete Query shoud call 'from_'")
        if isinstance(self.table, BasicTable):
            sql = f"DELETE FROM {self.table.sql}"
        else:
            sql = f"DELETE {format_quotes(self.table.alias)} FROM {self.table.sql}"
        if self.where:
            sql += f" WHERE {self.where.sql}"
        return sql


class DeleteMixin(QueryObject):
    _delete: Delete

    @property
    def query(self):
        return self._delete

    @property
    def sql(self) -> str:
        return self._delete.sql


class DeleteClause:
    def __init__(self) -> None:
        self._delete = Delete()

    def from_(self, table: Table):
        return DeleteFrom(self._delete, table)


class DeleteFrom:
    def __init__(self, delete: Delete, table: Table) -> None:
        delete.table = table
        self._delete = delete

    def where(self, condition: Condition):
        return DeleteWhere(self._delete, condition)

    def all(self):
        # delete all is too dangerous.
        # So if you need to delete all records, you should expressly say all.
        return DeleteAll(self._delete)


class DeleteAll(DeleteMixin):
    def __init__(self, delete: Delete) -> None:
        self._delete = delete


class DeleteWhere(DeleteMixin):
    def __init__(self, delete: Delete, condition: Condition) -> None:
        delete.where = condition
        self._delete = delete
