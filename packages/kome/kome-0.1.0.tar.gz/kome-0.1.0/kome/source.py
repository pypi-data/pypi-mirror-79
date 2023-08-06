from typing import Union

from kome.utils import format_quotes


class QueryObject:
    @property
    def sql(self) -> str:
        raise NotImplementedError()


class BasicQuerySource(QueryObject):
    def as_(self, alias: str) -> QueryObject:
        return AliasedQuerySource(self, alias)


class AliasedQuerySource(QueryObject):
    def __init__(self, qs: BasicQuerySource, alias: str) -> None:
        self.qs = qs
        self.alias = alias

    @property
    def sql(self) -> str:
        return f"{self.qs.sql} AS {format_quotes(self.alias)}"


QuerySource = Union[BasicQuerySource, AliasedQuerySource]
