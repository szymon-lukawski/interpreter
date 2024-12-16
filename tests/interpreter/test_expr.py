"""test interpretation of expression part of language"""

# pylint: disable=protected-access
# pylint: disable=unidiomatic-typecheck

import pytest
from lexer.token_type import TokenType
from interpreter.interpreter import Interpreter
from parser.AST import *
from interpreter.interpreter_errors import InterpreterError, NotSupportedOperation


def test_sanity():
    """."""
    assert 1 == True


def test_int_literal():
    """2"""
    ast = IntLiteral(2)
    i = Interpreter()
    assert 2 == ast.accept(i).value


def test_float_literal():
    """2.1"""
    ast = FloatLiteral(2.1)
    i = Interpreter()
    assert abs(2.1 - ast.accept(i).value) == 0


def test_str_literal():
    """'Ala ma kota.'"""
    ast = StrLiteral("Ala ma kota.")
    i = Interpreter()
    assert ast.accept(i).value == "Ala ma kota."


def test_null():
    """null"""
    ast = NullLiteral()
    i = Interpreter()
    assert ast.accept(i) is None


def test_unary_integer():
    """-2"""
    ast = UnaryExpr(IntLiteral(2))
    i = Interpreter()
    assert ast.accept(i).value == -2


def test_unary_float():
    """-2.1"""
    ast = UnaryExpr(FloatLiteral(2.1))
    i = Interpreter()
    assert ast.accept(i).value == -2.1


def test_unary_str():
    """-'Ala'"""
    ast = UnaryExpr(StrLiteral("Ala"), pos=(1, 1))
    i = Interpreter()
    with pytest.raises(NotSupportedOperation) as e:
        ast.accept(i)
    assert (
        str(e.value)
        == "NotSupportedOperation: row: 1, column: 1, Can not '-' a string."
    )


def test_unary_struct_value():
    """A : struct begin x: int=10; end a : A; print((-a));"""
    ast = Program(
        [
            StructDef("A", [VariableDeclaration("x", "int", False, IntLiteral(10))]),
            VariableDeclaration("a", "A", False),
            FunctionCall("print", [UnaryExpr(ObjectAccess(["a"]), pos=(1, 1))]),
        ]
    )
    i = Interpreter()
    with pytest.raises(NotSupportedOperation) as e:
        ast.accept(i)
    assert (
        str(e.value)
        == "NotSupportedOperation: row: 1, column: 1, Can not '-' a struct."
    )


def test_unary_variant_with_supported_operation():
    """A : variant begin x: int; y : str; end a : A; a = 1; result : int = -a;"""
    ast = Program(
        [
            VariantDef("A", [NamedType("x", "int"), NamedType("y", "str")]),
            VariableDeclaration("a", "A", False),
            AssignmentStatement(ObjectAccess(["a"]), IntLiteral(1)),
            VariableDeclaration("result", "int", False, UnaryExpr(ObjectAccess(["a"]))),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["result"])).value.value == -1


def test_unary_variant_with_not_supported_operation():
    """A : variant begin x: int; y : str; end a : A; a = 'Ala'; result : int = -a;"""
    ast = Program(
        [
            VariantDef("A", [NamedType("x", "int"), NamedType("y", "str")]),
            VariableDeclaration("a", "A", False),
            AssignmentStatement(ObjectAccess(["a"]), StrLiteral("Ala")),
            VariableDeclaration(
                "result", "int", False, UnaryExpr(ObjectAccess(["a"]), pos=(109, 32))
            ),
        ]
    )
    i = Interpreter()
    with pytest.raises(NotSupportedOperation) as e:
        ast.accept(i)
    assert (
        str(e.value)
        == "NotSupportedOperation: row: 109, column: 32, Can not '-' a string."
    )


def test_multiplication_int_int():
    """2*3"""
    ast = MultiExpr([IntLiteral(2), IntLiteral(3)], ["*"])
    i = Interpreter()
    assert ast.accept(i).value == 6


def test_multiplication_int_float():
    """2*3.2"""
    ast = MultiExpr([IntLiteral(2), FloatLiteral(3.2)], ["*"])
    i = Interpreter()
    assert ast.accept(i).value == 6


def test_multiplication_int_str():
    """2*'Ala'"""
    ast = MultiExpr([IntLiteral(2), StrLiteral("Ala")], ["*"], pos=(109, 32))
    i = Interpreter()
    with pytest.raises(InterpreterError) as e:
        ast.accept(i)
    assert (
        str(e.value)
        == "InterpreterError: row: 109, column: 32, Can not convert 'Ala' str into int"
    )


def test_multiplication_int_struct():
    """A : struct begin x: int=10; end a : A; result : int = 2 * a;"""
    ast = Program(
        [
            StructDef("A", [VariableDeclaration("x", "int", False, IntLiteral(10))]),
            VariableDeclaration("a", "A", False),
            VariableDeclaration(
                "result",
                "int",
                False,
                MultiExpr([IntLiteral(2), ObjectAccess(["a"])], ["*"], pos=(32, 1)),
            ),
        ]
    )
    i = Interpreter()
    with pytest.raises(NotSupportedOperation) as e:
        ast.accept(i)
    assert (
        str(e.value)
        == "NotSupportedOperation: row: 32, column: 1, Can not '*' a  struct."
    )


def test_multiplication_int_variant_compatible():
    """A : variant begin x: int; y : str; end a : A; a = 2; result : int = 2 * a;"""
    ast = Program(
        [
            VariantDef("A", [NamedType("x", "int"), NamedType("y", "str")]),
            VariableDeclaration("a", "A", False),
            AssignmentStatement(ObjectAccess(["a"]), IntLiteral(2)),
            VariableDeclaration(
                "result",
                "int",
                False,
                MultiExpr([IntLiteral(2), ObjectAccess(["a"])], ["*"]),
            ),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["result"])).value == 4


def test_multiplication_int_variant_not_compatible():
    """A : variant begin x: int; y : str; end a : A; a = 'Ala'; result : int = 2 * a;"""
    ast = Program(
        [
            VariantDef("A", [NamedType("x", "int"), NamedType("y", "str")]),
            VariableDeclaration("a", "A", False),
            AssignmentStatement(ObjectAccess(["a"]), StrLiteral("Ala")),
            VariableDeclaration(
                "result",
                "int",
                False,
                MultiExpr([IntLiteral(2), ObjectAccess(["a"])], ["*"], pos=(22, 33)),
            ),
        ]
    )
    i = Interpreter()
    with pytest.raises(InterpreterError) as e:
        ast.accept(i)
    assert (
        str(e.value)
        == "InterpreterError: row: 22, column: 33, Can not convert 'Ala' str into int"
    )


def test_multiplication_float_int():
    """3.2*3"""
    ast = MultiExpr([FloatLiteral(3.2), IntLiteral(3)], ["*"])
    i = Interpreter()
    assert abs(ast.accept(i).value - 9.6) < 10**-9


def test_multiplication_float_float():
    """3.2*3.14"""
    ast = MultiExpr([FloatLiteral(3.2), FloatLiteral(3.14)], ["*"])
    i = Interpreter()
    assert abs(ast.accept(i).value - 10.048) < 10**-9


def test_multiplication_float_str_not_compatible():
    """3.2*3.14"""
    ast = MultiExpr([FloatLiteral(3.2), StrLiteral("Ala")], ["*"], pos=(22, 33))
    i = Interpreter()
    with pytest.raises(InterpreterError) as e:
        ast.accept(i)
    assert (
        str(e.value)
        == "InterpreterError: row: 22, column: 33, Can not convert 'Ala' str into float"
    )


def test_multiplication_float_str_compatible():
    """3.2*'3.14'"""
    ast = MultiExpr([FloatLiteral(3.2), StrLiteral("3.14")], ["*"])
    i = Interpreter()
    assert abs(ast.accept(i).value - 10.048) < 10**-9


def test_multiplication_float_struct():
    """A : struct begin x: float = 10.1; end a : A; result : float = 3.14 * a;"""
    ast = Program(
        [
            StructDef(
                "A", [VariableDeclaration("x", "float", False, FloatLiteral(10.1))]
            ),
            VariableDeclaration("a", "A", False),
            VariableDeclaration(
                "result",
                "float",
                False,
                MultiExpr(
                    [FloatLiteral(3.14), ObjectAccess(["a"])], ["*"], pos=(32, 1)
                ),
            ),
        ]
    )
    i = Interpreter()
    with pytest.raises(NotSupportedOperation) as e:
        ast.accept(i)
    assert (
        str(e.value)
        == "NotSupportedOperation: row: 32, column: 1, Can not '*' a  struct."
    )


def test_multiplication_float_variant_compatible():
    """A : variant begin x: int; y : str; end a : A; a = 3.2; result : float = 3.14 * a;"""
    ast = Program(
        [
            VariantDef("A", [NamedType("x", "int"), NamedType("y", "str")]),
            VariableDeclaration("a", "A", False),
            AssignmentStatement(ObjectAccess(["a"]), FloatLiteral(3.2)),
            VariableDeclaration(
                "result",
                "float",
                False,
                MultiExpr([FloatLiteral(3.14), ObjectAccess(["a"])], ["*"]),
            ),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert abs(i.visit_obj_access(ObjectAccess(["result"])).value - (3.14 * 3)) < 10**-9


def test_multiplication_float_variant_not_compatible():
    """A : variant begin x: int; y : str; end a : A; a = 'Ala'; result : float = 3.14 * a;"""
    ast = Program(
        [
            VariantDef("A", [NamedType("x", "int"), NamedType("y", "str")]),
            VariableDeclaration("a", "A", False),
            AssignmentStatement(ObjectAccess(["a"]), StrLiteral("Ala")),
            VariableDeclaration(
                "result",
                "float",
                False,
                MultiExpr(
                    [FloatLiteral(3.14), ObjectAccess(["a"])], ["*"], pos=(101, 202)
                ),
            ),
        ]
    )
    i = Interpreter()
    with pytest.raises(InterpreterError) as e:
        ast.accept(i)
    assert (
        str(e.value)
        == "InterpreterError: row: 101, column: 202, Can not convert 'Ala' str into float"
    )


def test_multiplication_str_int():
    """'Ala'*2"""
    ast = MultiExpr([StrLiteral("Ala"), IntLiteral(2)], ["*"])
    i = Interpreter()
    assert ast.accept(i).value == "AlaAla"


def test_multiplication_str_float():
    """'Ala'*3.14"""
    ast = MultiExpr([StrLiteral("Ala"), FloatLiteral(3.14)], ["*"])
    i = Interpreter()
    assert ast.accept(i).value == "AlaAlaAla"


def test_multiplication_str_str():
    """'ABC'*'12345'"""
    ast = MultiExpr([StrLiteral("ABC"), StrLiteral("12345")], ["*"])
    i = Interpreter()
    assert ast.accept(i).value == "A1B2C3"


def test_division_int_int():
    """12/5"""
    ast = MultiExpr([IntLiteral(12), IntLiteral(5)], ["/"])
    i = Interpreter()
    assert ast.accept(i).value == 2


def test_division_int_int_by_zero():
    """12/0"""
    ast = MultiExpr([IntLiteral(12), IntLiteral(0)], ["/"], pos=(90, 12))
    i = Interpreter()
    with pytest.raises(InterpreterError) as e:
        ast.accept(i)
    assert str(e.value) == "DivisionByZero: row: 90, column: 12, Not good."


def test_division_int_float_less_than_1():
    """12/0.5"""
    ast = MultiExpr([IntLiteral(12), FloatLiteral(0.5)], ["/"], pos=(90, 12))
    i = Interpreter()
    with pytest.raises(InterpreterError) as e:
        ast.accept(i)
    assert str(e.value) == "DivisionByZero: row: 90, column: 12, Not good."


def test_division_int_float():
    """12/1.5"""
    ast = MultiExpr([IntLiteral(12), FloatLiteral(1.5)], ["/"], pos=(90, 12))
    i = Interpreter()
    ast.accept(i)
    assert abs(ast.accept(i).value - 12) < 10**-9

def test_division_int_str():
    """12/'1.5'"""
    ast = MultiExpr([IntLiteral(12), StrLiteral('1.5')], ["/"], pos=(90, 12))
    i = Interpreter()
    ast.accept(i)
    assert abs(ast.accept(i).value - 12) < 10**-9

def test_division_str_int():
    """'Ala'/0"""
    ast = MultiExpr([StrLiteral('Ala'), IntLiteral(0)], ["/"], pos=(90, 12))
    i = Interpreter()
    ast.accept(i)
    assert ast.accept(i).value == 'A'

def test_division_str_float():
    """'Ala'/0"""
    ast = MultiExpr([StrLiteral('Ala'), FloatLiteral(1.7)], ["/"], pos=(90, 12))
    i = Interpreter()
    ast.accept(i)
    assert ast.accept(i).value == 'l'


def test_division_str_str():
    """'AAAABABAB'/'AB'"""
    ast = MultiExpr([StrLiteral('AAAABABAB123'), StrLiteral('AB')], ["/"], pos=(90, 12))
    i = Interpreter()
    ast.accept(i)
    assert ast.accept(i).value == 'AAA123'

def test_add_int_int():
    """102 + 103"""
    ast = AddExpr([IntLiteral(102), IntLiteral(103)], ["+"], pos=(90, 12))
    i = Interpreter()
    assert ast.accept(i).value == 205

def test_add_int_float():
    """102 + 103"""
    ast = AddExpr([IntLiteral(102), FloatLiteral(103.2)], ["+"], pos=(90, 12))
    i = Interpreter()
    assert ast.accept(i).value == 205

def test_add_int_str():
    """102 + '103'"""
    ast = AddExpr([IntLiteral(102), StrLiteral('103.2')], ["+"], pos=(90, 12))
    i = Interpreter()
    assert ast.accept(i).value == 205

def test_add_float_int():
    """102.1 + 103"""
    ast = AddExpr([FloatLiteral(102.1), IntLiteral(103)], ["+"], pos=(90, 12))
    i = Interpreter()
    assert ast.accept(i).value == 205.1

def test_add_float_float():
    """102.3 + 103.3"""
    ast = AddExpr([FloatLiteral(102.3), FloatLiteral(103.3)], ["+"], pos=(90, 12))
    i = Interpreter()
    assert ast.accept(i).value == 205.6

def test_add_float_str():
    """102.3 + '103.3'"""
    ast = AddExpr([FloatLiteral(102.3), StrLiteral('103.3')], ["+"], pos=(90, 12))
    i = Interpreter()
    assert ast.accept(i).value == 205.6


def test_add_str_int():
    """'Ala' + 103"""
    ast = AddExpr([StrLiteral('Ala'), IntLiteral(103)], ["+"], pos=(90, 12))
    i = Interpreter()
    assert ast.accept(i).value == 'Ala103'

def test_add_str_float():
    """'Ala' + 3.14"""
    ast = AddExpr([StrLiteral('Ala'), FloatLiteral(3.14)], ["+"], pos=(90, 12))
    i = Interpreter()
    assert ast.accept(i).value == 'Ala3.1400'

def test_add_str_str():
    """'Ala' + '3.14'"""
    ast = AddExpr([StrLiteral('Ala'), StrLiteral('3.14')], ["+"], pos=(90, 12))
    i = Interpreter()
    assert ast.accept(i).value == 'Ala3.14'

def test_sub_str_str():
    """'ABCBA' - 'B'"""
    ast = AddExpr([StrLiteral('ABCBA'), StrLiteral('B')], ["-"], pos=(90, 12))
    i = Interpreter()
    assert ast.accept(i).value == 'ACBA'




# def test_multiplication_three_integers():
#     """2*3*5"""
#     ast = MultiExpr([IntLiteral(2), IntLiteral(3), IntLiteral(5)], ["*", "*"])
#     i = Interpreter()
#     assert ast.accept(i) == 30


# def test_multiplication_four_integers():
#     """2*3*5*7"""
#     ast = MultiExpr(
#         [IntLiteral(2), IntLiteral(3), IntLiteral(5), IntLiteral(7)], ["*", "*", "*"]
#     )
#     i = Interpreter()
#     assert ast.accept(i) == 210


# def test_division_two_different_integers():
#     """6/3"""
#     ast = MultiExpr([IntLiteral(6), IntLiteral(3)], ["/"])
#     i = Interpreter()
#     assert ast.accept(i) == 2


# def test_division_three_integers():
#     """6/3/2"""
#     ast = MultiExpr([IntLiteral(6), IntLiteral(3), IntLiteral(2)], ["/", "/"])
#     i = Interpreter()
#     assert ast.accept(i) == 1


# def test_division_four_integers():
#     """210/2/3/5"""
#     ast = MultiExpr(
#         [IntLiteral(210), IntLiteral(2), IntLiteral(3), IntLiteral(5)], ["/", "/", "/"]
#     )
#     i = Interpreter()
#     assert ast.accept(i) == 7


# def test_two_divided_by_one_half():
#     """2/(1/2)"""
#     ast = MultiExpr(
#         [IntLiteral(2), MultiExpr([IntLiteral(1), IntLiteral(2)], ["/"])], ["/"]
#     )
#     i = Interpreter()
#     assert ast.accept(i) == 4


# def test_unary_two_divided_unary_by_one_half_1():
#     """-2/-(1/2)"""
#     ast = MultiExpr(
#         [
#             UnaryExpr(IntLiteral(2)),
#             UnaryExpr(MultiExpr([IntLiteral(1), IntLiteral(2)], ["/"])),
#         ],
#         ["/"],
#     )
#     i = Interpreter()
#     assert ast.accept(i) == 4


# def test_unary_two_divided_unary_by_one_half_2():
#     """-2/(-1/2)"""
#     ast = MultiExpr(
#         [
#             UnaryExpr(IntLiteral(2)),
#             MultiExpr([UnaryExpr(IntLiteral(1)), IntLiteral(2)], ["/"]),
#         ],
#         ["/"],
#     )
#     i = Interpreter()
#     assert ast.accept(i) == 4


# def test_unary_two_divided_unary_by_one_half_3():
#     """-2/(1/-2)"""
#     ast = MultiExpr(
#         [
#             UnaryExpr(IntLiteral(2)),
#             MultiExpr([IntLiteral(1), UnaryExpr(IntLiteral(2))], ["/"]),
#         ],
#         ["/"],
#     )
#     i = Interpreter()
#     assert ast.accept(i) == 4


# def test_two_divided_unary_by_one_half_3():
#     """2/(1/-2)"""
#     ast = MultiExpr(
#         [IntLiteral(2), MultiExpr([IntLiteral(1), UnaryExpr(IntLiteral(2))], ["/"])],
#         ["/"],
#     )
#     i = Interpreter()
#     assert ast.accept(i) == -4


# some_ints = [-1000, -194, -32, -1, 0, 1, 4, 7, 21, 31, 81, 133, 1001]


# @pytest.mark.parametrize("x", some_ints)
# @pytest.mark.parametrize("y", some_ints)
# def test_add_two_integers(x, y):
#     """x+y"""
#     ast = AddExpr([IntLiteral(x), IntLiteral(y)], ["+"])
#     i = Interpreter()
#     assert ast.accept(i) == x + y


# @pytest.mark.parametrize("x", some_ints)
# @pytest.mark.parametrize("y", some_ints)
# def test_subtract_two_integers(x, y):
#     """x-y"""
#     ast = AddExpr([IntLiteral(x), IntLiteral(y)], ["-"])
#     i = Interpreter()
#     assert ast.accept(i) == x - y


# @pytest.mark.parametrize("x", some_ints)
# @pytest.mark.parametrize("y", some_ints)
# @pytest.mark.parametrize("z", some_ints)
# def test_add_three_integers(x, y, z):
#     """x+y+z"""
#     ast = AddExpr([IntLiteral(x), IntLiteral(y), IntLiteral(z)], ["+", "+"])
#     i = Interpreter()
#     assert ast.accept(i) == x + y + z


# def test_1_plus_2_minus_3():
#     """1+2-3"""
#     ast = AddExpr([IntLiteral(1), IntLiteral(2), IntLiteral(3)], ["+", "-"])
#     i = Interpreter()
#     assert ast.accept(i) == 0


# def test_1_minus_2_plus_3():
#     """1-2+3"""
#     ast = AddExpr([IntLiteral(1), IntLiteral(2), IntLiteral(3)], ["-", "+"])
#     i = Interpreter()
#     assert ast.accept(i) == 2


# def test_1_minus_unary_minus_3():
#     """1--3"""
#     ast = AddExpr([IntLiteral(1), UnaryExpr(IntLiteral(3))], ["-"])
#     i = Interpreter()
#     assert ast.accept(i) == 4


# def test_unary_minus_3_minus_1():
#     """-3-1"""
#     ast = AddExpr([UnaryExpr(IntLiteral(3)), IntLiteral(1)], ["-"])
#     i = Interpreter()
#     assert ast.accept(i) == -4


# def test_unary_3_times_2_plus_4():
#     """-3*2+4"""
#     ast = AddExpr(
#         [MultiExpr([UnaryExpr(IntLiteral(3)), IntLiteral(2)], ["*"]), IntLiteral(4)],
#         ["+"],
#     )
#     i = Interpreter()
#     assert ast.accept(i) == -2


# def test_unary_3_plus_2_times_4():
#     """-3+2*4"""
#     ast = AddExpr(
#         [UnaryExpr(IntLiteral(3)), MultiExpr([IntLiteral(2), IntLiteral(4)], ["*"])],
#         ["+"],
#     )
#     i = Interpreter()
#     assert ast.accept(i) == 5


# def test_multiplication_of_sums():
#     """(2+3)*(5+7)"""
#     ast = MultiExpr(
#         [
#             AddExpr([IntLiteral(2), IntLiteral(3)], ["+"]),
#             AddExpr([IntLiteral(5), IntLiteral(7)], ["+"]),
#         ],
#         ["*"],
#     )
#     i = Interpreter()
#     assert ast.accept(i) == 60


# def test_division_of_sums():
#     """(2+3)/(5+7)"""
#     ast = MultiExpr(
#         [
#             AddExpr([IntLiteral(2), IntLiteral(3)], ["+"]),
#             AddExpr([IntLiteral(5), IntLiteral(7)], ["+"]),
#         ],
#         ["/"],
#     )
#     i = Interpreter()
#     assert ast.accept(i) == 5 / 12


# def test_division_of_sums_but_using_unary():
#     """(2--3)/(5+7)"""
#     ast = MultiExpr(
#         [
#             AddExpr([IntLiteral(2), UnaryExpr(IntLiteral(3))], ["-"]),
#             AddExpr([IntLiteral(5), IntLiteral(7)], ["+"]),
#         ],
#         ["/"],
#     )
#     i = Interpreter()
#     assert ast.accept(i) == 5 / 12


# def test_equal_one_is_one():
#     """1 == 1"""
#     ast = RelationExpr(IntLiteral(1), IntLiteral(1), "==")
#     i = Interpreter()
#     assert ast.accept(i) == 1


# def test_2_is_3():
#     """2 == 3"""
#     ast = RelationExpr(IntLiteral(2), IntLiteral(3), "==")
#     i = Interpreter()
#     assert ast.accept(i) == 0


# def test_float_more_than_one_is_one():
#     """1.2 == 1"""
#     ast = RelationExpr(FloatLiteral(1.2), IntLiteral(1), "==")
#     i = Interpreter()
#     assert ast.accept(i) == 0


# def test_float_slighthly_more_than_one_is_one():
#     """1.0000001 == 1"""
#     ast = RelationExpr(FloatLiteral(1.0000001), IntLiteral(1), "==")
#     i = Interpreter()
#     assert ast.accept(i) == 0


# def test_not_equal_one_is_not_one():
#     """1 != 1"""
#     ast = RelationExpr(IntLiteral(1), IntLiteral(1), "!=")
#     i = Interpreter()
#     assert ast.accept(i) == 0


# def test_seventh_digit_after_comma_different_float():
#     """1.0000001 != 1.0000002"""
#     ast = RelationExpr(FloatLiteral(1.0000001), FloatLiteral(1.0000002), "!=")
#     i = Interpreter()
#     assert ast.accept(i) == 1


# def test_seventh_digit_after_comma_different_float_x_10():
#     """10.0000001 != 10.0000002"""
#     ast = RelationExpr(FloatLiteral(10.0000001), FloatLiteral(10.0000002), "!=")
#     i = Interpreter()
#     assert ast.accept(i) == 1


# def test_seventh_digit_after_comma_different_float_x_100():
#     """100.0000001 != 100.0000002"""
#     ast = RelationExpr(FloatLiteral(100.0000001), FloatLiteral(100.0000002), "!=")
#     i = Interpreter()
#     assert ast.accept(i) == 1


# def test_seventh_digit_after_comma_different_float_x_big():
#     """2000000000.0000001 != 2000000000.0000002"""
#     ast = RelationExpr(
#         FloatLiteral(2000000000.0000001), FloatLiteral(2000000000.0000002), "!="
#     )
#     i = Interpreter()
#     assert ast.accept(i) == 1


# def test_unary_one_int_is_not_unary_one_float():
#     """-1 != -1.0"""
#     ast = RelationExpr(UnaryExpr(IntLiteral(1)), UnaryExpr(FloatLiteral(1.0)), "!=")
#     i = Interpreter()
#     assert ast.accept(i) == 0


# def test_sum_of_ints_is_not_sum_of_slithly_more_floats():
#     """1+2 != 1.0001 + 2"""
#     ast = RelationExpr(
#         AddExpr([IntLiteral(1), IntLiteral(2)], ["+"]),
#         AddExpr([FloatLiteral(1.0001), IntLiteral(2)], ["+"]),
#         "!=",
#     )
#     i = Interpreter()
#     assert ast.accept(i) == 1


# def test_sum_of_multi_is_not_multi_of_sum():
#     """2*3+5*7 != (2+3)*(5+7)"""
#     ast = RelationExpr(
#         AddExpr(
#             [
#                 MultiExpr([IntLiteral(2), IntLiteral(3)], ["*"]),
#                 MultiExpr([IntLiteral(5), IntLiteral(7)], ["*"]),
#             ],
#             ["+"],
#         ),
#         MultiExpr(
#             [
#                 AddExpr([IntLiteral(2), IntLiteral(3)], ["+"]),
#                 AddExpr([IntLiteral(5), IntLiteral(7)], ["+"]),
#             ],
#             ["*"],
#         ),
#         "!=",
#     )
#     i = Interpreter()
#     assert ast.accept(i) == 1


# def test_unary_of_logical_sum_of_multi_is_not_multi_of_sum():
#     """-(2*3+5*7 != (2+3)*(5+7))"""
#     ast = UnaryExpr(
#         RelationExpr(
#             AddExpr(
#                 [
#                     MultiExpr([IntLiteral(2), IntLiteral(3)], ["*"]),
#                     MultiExpr([IntLiteral(5), IntLiteral(7)], ["*"]),
#                 ],
#                 ["+"],
#             ),
#             MultiExpr(
#                 [
#                     AddExpr([IntLiteral(2), IntLiteral(3)], ["+"]),
#                     AddExpr([IntLiteral(5), IntLiteral(7)], ["+"]),
#                 ],
#                 ["*"],
#             ),
#             "!=",
#         )
#     )
#     i = Interpreter()
#     assert ast.accept(i) == 0


# def test_unary_of_one():
#     """-(1)"""
#     ast = UnaryExpr(IntLiteral(1))
#     i = Interpreter()
#     assert ast.accept(i) == -1


# def test_unary_of_zero():
#     """-(0)"""
#     ast = UnaryExpr(IntLiteral(0))
#     i = Interpreter()
#     assert ast.accept(i) == 0


# numbers = [-2, -1, 0, 1, 2]


# @pytest.mark.parametrize("x", numbers)
# @pytest.mark.parametrize("y", numbers)
# def test_x_less_than_y(x, y):
#     """x < y"""
#     ast = RelationExpr(IntLiteral(x), IntLiteral(y), "<")
#     i = Interpreter()
#     assert ast.accept(i) == (x < y)


# @pytest.mark.parametrize("x", numbers)
# @pytest.mark.parametrize("y", numbers)
# def test_x_less__or_equal_than_y(x, y):
#     """x <= y"""
#     ast = RelationExpr(IntLiteral(x), IntLiteral(y), "<=")
#     i = Interpreter()
#     assert ast.accept(i) == (x <= y)


# @pytest.mark.parametrize("x", numbers)
# @pytest.mark.parametrize("y", numbers)
# def test_x_equal_y(x, y):
#     """x == y"""
#     ast = RelationExpr(IntLiteral(x), IntLiteral(y), "==")
#     i = Interpreter()
#     assert ast.accept(i) == (x == y)


# @pytest.mark.parametrize("x", numbers)
# @pytest.mark.parametrize("y", numbers)
# def test_x_not_equal_y(x, y):
#     """x != y"""
#     ast = RelationExpr(IntLiteral(x), IntLiteral(y), "!=")
#     i = Interpreter()
#     assert ast.accept(i) == (x != y)


# @pytest.mark.parametrize("x", numbers)
# @pytest.mark.parametrize("y", numbers)
# def test_x_greater_or_equal_than_y(x, y):
#     """x >= y"""
#     ast = RelationExpr(IntLiteral(x), IntLiteral(y), ">=")
#     i = Interpreter()
#     assert ast.accept(i) == (x >= y)


# @pytest.mark.parametrize("x", numbers)
# @pytest.mark.parametrize("y", numbers)
# def test_x_greater_than_y(x, y):
#     """x > y"""
#     ast = RelationExpr(IntLiteral(x), IntLiteral(y), ">")
#     i = Interpreter()
#     assert ast.accept(i) == (x > y)
