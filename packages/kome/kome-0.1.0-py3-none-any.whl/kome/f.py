from kome.expression import BasicExpression


class SQLFunction(BasicExpression):
    def __init__(self, func_name: str, *args: BasicExpression) -> None:
        self.func_name = func_name
        self.args = args

    @property
    def sql(self) -> str:
        return f"{self.func_name}({','.join(map(lambda v:v.sql,self.args))})"


def count(expr: BasicExpression):
    return SQLFunction("COUNT", expr)
