from enum import Enum


class OrderType(Enum):
    desc = "DESC"
    asc = "ASC"


class Arithmetic(Enum):
    add = "+"
    sub = "-"
    mul = "*"
    div = "/"


class Comparator(Enum):
    pass


class Equality(Comparator):
    eq = "="
    ne = "<>"
    gt = ">"
    gte = ">="
    lt = "<"
    lte = "<="


class Matching(Comparator):
    not_like = " NOT LIKE "
    like = " LIKE "
    not_ilike = " NOT ILIKE "
    ilike = " ILIKE "
    regex = " REGEX "
    bin_regex = " REGEX BINARY "


class JoinType(Enum):
    left = "LEFT"
    inner = "INNER"
