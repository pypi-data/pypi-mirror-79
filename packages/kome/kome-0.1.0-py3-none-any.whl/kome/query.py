from kome.insert import InsertClause
from kome.select import SelectClause
from kome.update import UpdateClause


class Query:
    @staticmethod
    def select():
        return SelectClause()

    @staticmethod
    def insert():
        return InsertClause()

    @staticmethod
    def update():
        return UpdateClause()
