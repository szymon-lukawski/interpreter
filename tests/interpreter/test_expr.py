"""test interpretation of expression part of language"""

# pylint: disable=protected-access
# pylint: disable=unidiomatic-typecheck

import pytest
from token_type import TokenType
from interpreter import Interpreter
from AST import *


def test_sanity():
    """."""
    assert 1 == True


def test_int_literal():
    """2"""
    ast = IntLiteral(2)
    i = Interpreter()
    assert 2 == ast.accept(i)


def test_float_literal():
    """2.1"""
    ast = FloatLiteral(2.1)
    i = Interpreter()
    assert abs(2.1 - ast.accept(i)) == 0


def test_str_literal():
    """'Ala ma kota.'"""
    ast = StrLiteral("Ala ma kota.")
    i = Interpreter()
    assert ast.accept(i) == "Ala ma kota."


def test_null():
    """null"""
    ast = NullLiteral()
    i = Interpreter()
    assert ast.accept(i) is None


def test_unary_integer():
    """-2"""
    ast = UnaryExpr(IntLiteral(2))
    i = Interpreter()
    assert ast.accept(i) == -2


def test_unary_float():
    """-2.1"""
    ast = UnaryExpr(FloatLiteral(2.1))
    i = Interpreter()
    assert ast.accept(i) == -2.1


def test_multiplication_two_integers():
    """2*3"""
    ast = MultiExpr([IntLiteral(2), IntLiteral(3)],['*'])
    i = Interpreter()
    assert ast.accept(i) == 6

def test_multiplication_three_integers():
    """2*3*5"""
    ast = MultiExpr([IntLiteral(2), IntLiteral(3), IntLiteral(5)],['*', '*'])
    i = Interpreter()
    assert ast.accept(i) == 30

def test_multiplication_four_integers():
    """2*3*5*7"""
    ast = MultiExpr([IntLiteral(2), IntLiteral(3), IntLiteral(5), IntLiteral(7)],['*', '*', '*'])
    i = Interpreter()
    assert ast.accept(i) == 210

def test_division_two_different_integers():
    """6/3"""
    ast = MultiExpr([IntLiteral(6), IntLiteral(3)],['/'])
    i = Interpreter()
    assert ast.accept(i) == 2

def test_division_three_integers():
    """6/3/2"""
    ast = MultiExpr([IntLiteral(6), IntLiteral(3), IntLiteral(2)],['/', '/'])
    i = Interpreter()
    assert ast.accept(i) == 1

def test_division_four_integers():
    """210/2/3/5"""
    ast = MultiExpr([IntLiteral(210), IntLiteral(2), IntLiteral(3), IntLiteral(5)],['/', '/', '/'])
    i = Interpreter()
    assert ast.accept(i) == 7


def test_two_divided_by_one_half():
    """2/(1/2)"""
    ast = MultiExpr([IntLiteral(2), MultiExpr([IntLiteral(1), IntLiteral(2)],['/'])],['/'])
    i = Interpreter()
    assert ast.accept(i) == 4

def test_unary_two_divided_unary_by_one_half_1():
    """-2/-(1/2)"""
    ast = MultiExpr([UnaryExpr(IntLiteral(2)), UnaryExpr(MultiExpr([IntLiteral(1), IntLiteral(2)],['/']))],['/'])
    i = Interpreter()
    assert ast.accept(i) == 4

def test_unary_two_divided_unary_by_one_half_2():
    """-2/(-1/2)"""
    ast = MultiExpr([UnaryExpr(IntLiteral(2)), MultiExpr([UnaryExpr(IntLiteral(1)), IntLiteral(2)],['/'])],['/'])
    i = Interpreter()
    assert ast.accept(i) == 4

def test_unary_two_divided_unary_by_one_half_3():
    """-2/(1/-2)"""
    ast = MultiExpr([UnaryExpr(IntLiteral(2)), MultiExpr([IntLiteral(1), UnaryExpr(IntLiteral(2))],['/'])],['/'])
    i = Interpreter()
    assert ast.accept(i) == 4


def test_two_divided_unary_by_one_half_3():
    """2/(1/-2)"""
    ast = MultiExpr([IntLiteral(2), MultiExpr([IntLiteral(1), UnaryExpr(IntLiteral(2))],['/'])],['/'])
    i = Interpreter()
    assert ast.accept(i) == -4

some_ints = [-1000, -194, -32, -1, 0, 1, 4, 7, 21, 31, 81, 133, 1001]


@pytest.mark.parametrize("x", some_ints)
@pytest.mark.parametrize("y", some_ints)
def test_add_two_integers(x, y):
    """x+y"""
    ast = AddExpr([IntLiteral(x), IntLiteral(y)], ["+"])
    i = Interpreter()
    assert ast.accept(i) == x+y

@pytest.mark.parametrize("x", some_ints)
@pytest.mark.parametrize("y", some_ints)
def test_subtract_two_integers(x, y):
    """x-y"""
    ast = AddExpr([IntLiteral(x), IntLiteral(y)], ["-"])
    i = Interpreter()
    assert ast.accept(i) == x-y

@pytest.mark.parametrize("x", some_ints)
@pytest.mark.parametrize("y", some_ints)
@pytest.mark.parametrize("z", some_ints)
def test_add_three_integers(x, y, z):
    """x+y+z"""
    ast = AddExpr([IntLiteral(x), IntLiteral(y), IntLiteral(z)], ["+", "+"])
    i = Interpreter()
    assert ast.accept(i) == x+y+z

def test_1_plus_2_minus_3():
    """1+2-3"""
    ast = AddExpr([IntLiteral(1), IntLiteral(2), IntLiteral(3)], ["+", "-"])
    i = Interpreter()
    assert ast.accept(i) == 0


def test_1_minus_2_plus_3():
    """1-2+3"""
    ast = AddExpr([IntLiteral(1), IntLiteral(2), IntLiteral(3)], ["-", "+"])
    i = Interpreter()
    assert ast.accept(i) == 2


def test_1_minus_unary_minus_3():
    """1--3"""
    ast = AddExpr([IntLiteral(1), UnaryExpr(IntLiteral(3))], ["-"])
    i = Interpreter()
    assert ast.accept(i) == 4



def test_unary_minus_3_minus_1():
    """-3-1"""
    ast = AddExpr([UnaryExpr(IntLiteral(3)), IntLiteral(1)], ["-"])
    i = Interpreter()
    assert ast.accept(i) == -4

def test_unary_3_times_2_plus_4():
    """-3*2+4"""
    ast = AddExpr([MultiExpr([UnaryExpr(IntLiteral(3)), IntLiteral(2)], ['*']), IntLiteral(4)], ['+'])
    i = Interpreter()
    assert ast.accept(i) == -2

def test_unary_3_plus_2_times_4():
    """-3+2*4"""
    ast = AddExpr([UnaryExpr(IntLiteral(3)), MultiExpr([IntLiteral(2), IntLiteral(4)], ['*'])], ['+'])
    i = Interpreter()
    assert ast.accept(i) == 5

def test_multiplication_of_sums():
    """(2+3)*(5+7)"""
    ast = MultiExpr([AddExpr([IntLiteral(2), IntLiteral(3)], ['+']), AddExpr([IntLiteral(5), IntLiteral(7)], ['+'])], ['*'])
    i = Interpreter()
    assert ast.accept(i) == 60

def test_division_of_sums():
    """(2+3)/(5+7)"""
    ast = MultiExpr([AddExpr([IntLiteral(2), IntLiteral(3)], ['+']), AddExpr([IntLiteral(5), IntLiteral(7)], ['+'])], ['/'])
    i = Interpreter()
    assert ast.accept(i) == 5/12

def test_division_of_sums_but_using_unary():
    """(2--3)/(5+7)"""
    ast = MultiExpr([AddExpr([IntLiteral(2), UnaryExpr(IntLiteral(3))], ['-']), AddExpr([IntLiteral(5), IntLiteral(7)], ['+'])], ['/'])
    i = Interpreter()
    assert ast.accept(i) == 5/12

def test_equal_one_is_one():
    """1 == 1"""
    ast = RelationExpr(IntLiteral(1), IntLiteral(1), '==')
    i = Interpreter()
    assert ast.accept(i) == 1

def test_2_is_3():
    """2 == 3"""
    ast = RelationExpr(IntLiteral(2), IntLiteral(3), '==')
    i = Interpreter()
    assert ast.accept(i) == 0

def test_float_more_than_one_is_one():
    """1.2 == 1"""
    ast = RelationExpr(FloatLiteral(1.2), IntLiteral(1), '==')
    i = Interpreter()
    assert ast.accept(i) == 0

def test_float_slighthly_more_than_one_is_one():
    """1.0000001 == 1"""
    ast = RelationExpr(FloatLiteral(1.0000001), IntLiteral(1), '==')
    i = Interpreter()
    assert ast.accept(i) == 0

def test_not_equal_one_is_not_one():
    """1 != 1"""
    ast = RelationExpr(IntLiteral(1), IntLiteral(1), '!=')
    i = Interpreter()
    assert ast.accept(i) == 0

def test_seventh_digit_after_comma_different_float():
    """1.0000001 != 1.0000002"""
    ast = RelationExpr(FloatLiteral(1.0000001), FloatLiteral(1.0000002), '!=')
    i = Interpreter()
    assert ast.accept(i) == 1


def test_seventh_digit_after_comma_different_float_x_10():
    """10.0000001 != 10.0000002"""
    ast = RelationExpr(FloatLiteral(10.0000001), FloatLiteral(10.0000002), '!=')
    i = Interpreter()
    assert ast.accept(i) == 1


def test_seventh_digit_after_comma_different_float_x_100():
    """100.0000001 != 100.0000002"""
    ast = RelationExpr(FloatLiteral(100.0000001), FloatLiteral(100.0000002), '!=')
    i = Interpreter()
    assert ast.accept(i) == 1


def test_seventh_digit_after_comma_different_float_x_big():
    """2000000000.0000001 != 2000000000.0000002"""
    ast = RelationExpr(FloatLiteral(2000000000.0000001), FloatLiteral(2000000000.0000002), '!=')
    i = Interpreter()
    assert ast.accept(i) == 1


def test_unary_one_int_is_not_unary_one_float():
    """-1 != -1.0"""
    ast = RelationExpr(UnaryExpr(IntLiteral(1)), UnaryExpr(FloatLiteral(1.0)), '!=')
    i = Interpreter()
    assert ast.accept(i) == 0

def test_sum_of_ints_is_not_sum_of_slithly_more_floats():
    """1+2 != 1.0001 + 2"""
    ast = RelationExpr(AddExpr([IntLiteral(1), IntLiteral(2)], ['+']), AddExpr([FloatLiteral(1.0001), IntLiteral(2)], ['+']), '!=')
    i = Interpreter()
    assert ast.accept(i) == 1

def test_sum_of_multi_is_not_multi_of_sum():
    """2*3+5*7 != (2+3)*(5+7)"""
    ast = RelationExpr(AddExpr([MultiExpr([IntLiteral(2), IntLiteral(3)], ['*']), MultiExpr([IntLiteral(5), IntLiteral(7)], ['*'])], ['+']), MultiExpr([AddExpr([IntLiteral(2), IntLiteral(3)], ['+']), AddExpr([IntLiteral(5), IntLiteral(7)], ['+'])], ['*']), '!=')
    i = Interpreter()
    assert ast.accept(i) == 1

def test_unary_of_logical_sum_of_multi_is_not_multi_of_sum():
    """-(2*3+5*7 != (2+3)*(5+7))"""
    ast = UnaryExpr(RelationExpr(AddExpr([MultiExpr([IntLiteral(2), IntLiteral(3)], ['*']), MultiExpr([IntLiteral(5), IntLiteral(7)], ['*'])], ['+']), MultiExpr([AddExpr([IntLiteral(2), IntLiteral(3)], ['+']), AddExpr([IntLiteral(5), IntLiteral(7)], ['+'])], ['*']), '!='))
    i = Interpreter()
    assert ast.accept(i) == 0


def test_unary_of_one():
    """-(1)"""
    ast = UnaryExpr(IntLiteral(1))
    i = Interpreter()
    assert ast.accept(i) == -1

def test_unary_of_zero():
    """-(0)"""
    ast = UnaryExpr(IntLiteral(0))
    i = Interpreter()
    assert ast.accept(i) == 0



