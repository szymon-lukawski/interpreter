from interpreter_types import *
from multipledispatch import dispatch    

@dispatch(BuiltInValue, BuiltInValue)
def add(left, right):
    return add(left.value, right.value)

@dispatch(int, int)
def add(left, right):
    return BuiltInValue('int', left + right)


@dispatch(object, object)
def add(left, right):
    raise NotImplementedError

# -------------------

@dispatch(BuiltInValue, BuiltInValue)
def sub(left, right):
    return sub(left.value, right.value)

@dispatch(int, int)
def sub(left, right):
    return BuiltInValue('int', left - right)


@dispatch(object, object)
def sub(left, right):
    raise NotImplementedError

# -----------------------

@dispatch(BuiltInValue, BuiltInValue)
def mul(left, right):
    return mul(left.value, right.value)

@dispatch(int, int)
def mul(left, right):
    return BuiltInValue('int', left * right)


@dispatch(object, object)
def mul(left, right):
    raise NotImplementedError

# -------------------------

@dispatch(BuiltInValue, BuiltInValue)
def div(left, right):
    return div(left.value, right.value)

@dispatch(int, int)
def div(left, right):
    return BuiltInValue('int', int(left / right))


@dispatch(object, object)
def div(left, right):
    raise NotImplementedError


# --------------------------


@dispatch(BuiltInValue, BuiltInValue)
def eq(left, right):
    return eq(left.value, right.value)

@dispatch(int, int)
def eq(left, right):
    return BuiltInValue('int', int(left == right))


@dispatch(object, object)
def eq(left, right):
    raise NotImplementedError


# --------------------------


@dispatch(BuiltInValue, BuiltInValue)
def ieq(left, right):
    return ieq(left.value, right.value)

@dispatch(int, int)
def ieq(left, right):
    return BuiltInValue('int', int(left != right))


@dispatch(object, object)
def ieq(left, right):
    raise NotImplementedError

# --------------------------


@dispatch(BuiltInValue, BuiltInValue)
def lt(left, right):
    return lt(left.value, right.value)

@dispatch(int, int)
def lt(left, right):
    return BuiltInValue('int', int(left < right))


@dispatch(object, object)
def lt(left, right):
    raise NotImplementedError

# --------------------------


@dispatch(BuiltInValue, BuiltInValue)
def gt(left, right):
    return gt(left.value, right.value)

@dispatch(int, int)
def gt(left, right):
    return BuiltInValue('int', int(left > right))


@dispatch(object, object)
def gt(left, right):
    raise NotImplementedError

# --------------------------


@dispatch(BuiltInValue, BuiltInValue)
def lteq(left, right):
    return lteq(left.value, right.value)

@dispatch(int, int)
def lteq(left, right):
    return BuiltInValue('int', int(left <= right))


@dispatch(object, object)
def lteq(left, right):
    raise NotImplementedError


# --------------------------


@dispatch(BuiltInValue, BuiltInValue)
def gteq(left, right):
    return gteq(left.value, right.value)

@dispatch(int, int)
def gteq(left, right):
    return BuiltInValue('int', int(left >= right))


@dispatch(object, object)
def gteq(left, right):
    raise NotImplementedError