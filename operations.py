from interpreter_types import *
from multipledispatch import dispatch    

@dispatch(BuiltInValue, BuiltInValue)
def add(left, right):
    return add(left.value, right.value)


@dispatch(StructValue, BuiltInValue)
def add(left, right):
    raise RuntimeError("Can not add struct and built in")

@dispatch(VariantValue, BuiltInValue)
def add(left, right):
    return add(left.value, right)

@dispatch(BuiltInValue, StructValue)
def add(left, right):
    raise RuntimeError("Can not add built in and structs ")

@dispatch(StructValue, StructValue)
def add(left, right):
    raise RuntimeError("Can not add structs")

@dispatch(VariantValue, StructValue)
def add(left, right):
    return add(left.value, right)

@dispatch(BuiltInValue, VariantValue)
def add(left, right):
    return add(left, right.value)

@dispatch(StructValue, VariantValue)
def add(left, right):
    return add(left, right.value)

@dispatch(VariantValue, VariantValue)
def add(left, right):
    return add(left.value, right.value)

@dispatch(int, int)
def add(left, right):
    return BuiltInValue('int', left + right)

@dispatch(float, int)
def add(left, right):
    return BuiltInValue('float', left + float(right))

@dispatch(str, int)
def add(left, right):
    return BuiltInValue('str', left + str(right))



@dispatch(object, object)
def add(left, right):
    raise NotImplementedError

# -------------------

@dispatch(BuiltInValue, BuiltInValue)
def sub(left, right):
    return sub(left.value, right.value)

@dispatch(StructValue, BuiltInValue)
def sub(left, right):
    raise RuntimeError("Can not sub struct and built in")

@dispatch(VariantValue, BuiltInValue)
def sub(left, right):
    return sub(left.value, right)

@dispatch(BuiltInValue, StructValue)
def sub(left, right):
    raise RuntimeError("Can not sub built in and structs ")

@dispatch(StructValue, StructValue)
def sub(left, right):
    raise RuntimeError("Can not sub structs")

@dispatch(VariantValue, StructValue)
def sub(left, right):
    return sub(left.value, right)

@dispatch(BuiltInValue, VariantValue)
def sub(left, right):
    return sub(left, right.value)

@dispatch(StructValue, VariantValue)
def sub(left, right):
    return sub(left, right.value)

@dispatch(VariantValue, VariantValue)
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

@dispatch(StructValue, BuiltInValue)
def add(left, right):
    raise RuntimeError("Can not mul struct and built in")

@dispatch(VariantValue, BuiltInValue)
def mul(left, right):
    return mul(left.value, right)

@dispatch(BuiltInValue, StructValue)
def mul(left, right):
    raise RuntimeError("Can not mul built in and structs ")

@dispatch(StructValue, StructValue)
def mul(left, right):
    raise RuntimeError("Can not mul structs")

@dispatch(VariantValue, StructValue)
def mul(left, right):
    return mul(left.value, right)

@dispatch(BuiltInValue, VariantValue)
def mul(left, right):
    return mul(left, right.value)

@dispatch(StructValue, VariantValue)
def mul(left, right):
    return mul(left, right.value)

@dispatch(VariantValue, VariantValue)
def mul(left, right):
    return add(left.value, right.value)

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

@dispatch(StructValue, BuiltInValue)
def div(left, right):
    raise RuntimeError("Can not div struct and built in")

@dispatch(VariantValue, BuiltInValue)
def div(left, right):
    return div(left.value, right)

@dispatch(BuiltInValue, StructValue)
def div(left, right):
    raise RuntimeError("Can not div built in and structs ")

@dispatch(StructValue, StructValue)
def div(left, right):
    raise RuntimeError("Can not div structs")

@dispatch(VariantValue, StructValue)
def div(left, right):
    return div(left.value, right)

@dispatch(BuiltInValue, VariantValue)
def div(left, right):
    return div(left, right.value)

@dispatch(StructValue, VariantValue)
def div(left, right):
    return div(left, right.value)

@dispatch(VariantValue, VariantValue)
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

@dispatch(StructValue, BuiltInValue)
def eq(left, right):
    raise RuntimeError("Can not eq struct and built in")

@dispatch(VariantValue, BuiltInValue)
def eq(left, right):
    return eq(left.value, right)

@dispatch(BuiltInValue, StructValue)
def eq(left, right):
    raise RuntimeError("Can not eq built in and structs ")

@dispatch(StructValue, StructValue)
def eq(left, right):
    raise RuntimeError("Can not eq structs")

@dispatch(VariantValue, StructValue)
def eq(left, right):
    return eq(left.value, right)

@dispatch(BuiltInValue, VariantValue)
def eq(left, right):
    return eq(left, right.value)

@dispatch(StructValue, VariantValue)
def eq(left, right):
    return eq(left, right.value)

@dispatch(VariantValue, VariantValue)
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

@dispatch(StructValue, BuiltInValue)
def ieq(left, right):
    raise RuntimeError("Can not ieq struct and built in")

@dispatch(VariantValue, BuiltInValue)
def ieq(left, right):
    return ieq(left.value, right)

@dispatch(BuiltInValue, StructValue)
def ieq(left, right):
    raise RuntimeError("Can not ieq built in and structs ")

@dispatch(StructValue, StructValue)
def ieq(left, right):
    raise RuntimeError("Can not ieq structs")

@dispatch(VariantValue, StructValue)
def ieq(left, right):
    return ieq(left.value, right)

@dispatch(BuiltInValue, VariantValue)
def ieq(left, right):
    return ieq(left, right.value)

@dispatch(StructValue, VariantValue)
def ieq(left, right):
    return ieq(left, right.value)

@dispatch(VariantValue, VariantValue)
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

@dispatch(StructValue, BuiltInValue)
def lt(left, right):
    raise RuntimeError("Can not lt struct and built in")

@dispatch(VariantValue, BuiltInValue)
def lt(left, right):
    return lt(left.value, right)

@dispatch(BuiltInValue, StructValue)
def lt(left, right):
    raise RuntimeError("Can not lt built in and structs ")

@dispatch(StructValue, StructValue)
def lt(left, right):
    raise RuntimeError("Can not lt structs")

@dispatch(VariantValue, StructValue)
def lt(left, right):
    return lt(left.value, right)

@dispatch(BuiltInValue, VariantValue)
def lt(left, right):
    return lt(left, right.value)

@dispatch(StructValue, VariantValue)
def lt(left, right):
    return lt(left, right.value)

@dispatch(VariantValue, VariantValue)
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

@dispatch(StructValue, BuiltInValue)
def gt(left, right):
    raise RuntimeError("Can not gt struct and built in")

@dispatch(VariantValue, BuiltInValue)
def gt(left, right):
    return gt(left.value, right)

@dispatch(BuiltInValue, StructValue)
def gt(left, right):
    raise RuntimeError("Can not gt built in and structs ")

@dispatch(StructValue, StructValue)
def gt(left, right):
    raise RuntimeError("Can not gt structs")

@dispatch(VariantValue, StructValue)
def gt(left, right):
    return gt(left.value, right)

@dispatch(BuiltInValue, VariantValue)
def gt(left, right):
    return gt(left, right.value)

@dispatch(StructValue, VariantValue)
def gt(left, right):
    return gt(left, right.value)

@dispatch(VariantValue, VariantValue)
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

@dispatch(StructValue, BuiltInValue)
def lteq(left, right):
    raise RuntimeError("Can not lteq struct and built in")

@dispatch(VariantValue, BuiltInValue)
def lteq(left, right):
    return lteq(left.value, right)

@dispatch(BuiltInValue, StructValue)
def lteq(left, right):
    raise RuntimeError("Can not lteq built in and structs ")

@dispatch(StructValue, StructValue)
def lteq(left, right):
    raise RuntimeError("Can not lteq structs")

@dispatch(VariantValue, StructValue)
def lteq(left, right):
    return lteq(left.value, right)

@dispatch(BuiltInValue, VariantValue)
def lteq(left, right):
    return lteq(left, right.value)

@dispatch(StructValue, VariantValue)
def lteq(left, right):
    return lteq(left, right.value)

@dispatch(VariantValue, VariantValue)
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

@dispatch(StructValue, BuiltInValue)
def gteq(left, right):
    raise RuntimeError("Can not gteq struct and built in")

@dispatch(VariantValue, BuiltInValue)
def gteq(left, right):
    return gteq(left.value, right)

@dispatch(BuiltInValue, StructValue)
def gteq(left, right):
    raise RuntimeError("Can not gteq built in and structs ")

@dispatch(StructValue, StructValue)
def gteq(left, right):
    raise RuntimeError("Can not gteq structs")

@dispatch(VariantValue, StructValue)
def gteq(left, right):
    return gteq(left.value, right)

@dispatch(BuiltInValue, VariantValue)
def gteq(left, right):
    return gteq(left, right.value)

@dispatch(StructValue, VariantValue)
def gteq(left, right):
    return gteq(left, right.value)

@dispatch(VariantValue, VariantValue)
def gteq(left, right):
    return gteq(left.value, right.value)

@dispatch(int, int)
def gteq(left, right):
    return BuiltInValue('int', int(left >= right))


@dispatch(object, object)
def gteq(left, right):
    raise NotImplementedError