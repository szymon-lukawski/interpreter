from typing import Dict
import pytest
from pretty_printer import PrettyPrinter
from AST import *


def test_print_int_literal():
    """1"""
    ast = IntLiteral(1)
    printer = PrettyPrinter()
    expected = "1"
    result = printer.print(ast)
    assert expected == result


def test_print_float_literal():
    """1.2"""
    ast = FloatLiteral(1.2)
    printer = PrettyPrinter()
    expected = "1.2"
    result = printer.print(ast)
    assert expected == result


def test_print_str_literal():
    """'abc'"""
    ast = StrLiteral("abc")
    printer = PrettyPrinter()
    expected = "'abc'"
    result = printer.print(ast)
    assert expected == result


def test_print_null():
    """null"""
    ast = NullLiteral()
    printer = PrettyPrinter()
    expected = "null"
    result = printer.print(ast)
    assert expected == result


def test_print_negated_int():
    """-1"""
    ast = UnaryExpr(IntLiteral(1))
    printer = PrettyPrinter()
    expected = "-1"
    result = printer.print(ast)
    assert expected == result


def test_print_negated_float():
    """-1.2"""
    ast = UnaryExpr(FloatLiteral(1.2))
    printer = PrettyPrinter()
    expected = "-1.2"
    result = printer.print(ast)
    assert expected == result


def test_print_negated_str_literal_not_interpretable():
    """-'abc'"""
    ast = UnaryExpr(StrLiteral("abc"))
    printer = PrettyPrinter()
    expected = "-'abc'"
    result = printer.print(ast)
    assert expected == result


def test_print_negated_str_literal_interpretable_as_int():
    """-'1'"""
    ast = UnaryExpr(StrLiteral("1"))
    printer = PrettyPrinter()
    expected = "-'1'"
    result = printer.print(ast)
    assert expected == result


def test_print_negated_str_literal_interpretable_as_float():
    """-'1.2'"""
    ast = UnaryExpr(StrLiteral("1.2"))
    printer = PrettyPrinter()
    expected = "-'1.2'"
    result = printer.print(ast)
    assert expected == result


def test_print_add_ints():
    """1+2"""
    ast = AddExpr([IntLiteral(1), IntLiteral(2)], ["+"])
    printer = PrettyPrinter()
    expected = "1 + 2"
    result = printer.print(ast)
    assert expected == result


def test_print_add_int_and_float():
    """1+2.3"""
    ast = AddExpr([IntLiteral(1), FloatLiteral(2.3)], ["+"])
    printer = PrettyPrinter()
    expected = "1 + 2.3"
    result = printer.print(ast)
    assert expected == result


def test_print_add_float_and_int():
    """1.2+3"""
    ast = AddExpr([FloatLiteral(1.2), IntLiteral(3)], ["+"])
    printer = PrettyPrinter()
    expected = "1.2 + 3"
    result = printer.print(ast)
    assert expected == result


def test_print_add_interpretable_as_int_str_and_int_minus_float():
    """'1'+2-3.4"""
    ast = AddExpr([StrLiteral("1"), IntLiteral(2), FloatLiteral(3.4)], ["+", "-"])
    printer = PrettyPrinter()
    expected = "'1' + 2 - 3.4"
    result = printer.print(ast)
    assert expected == result


def test_print_add_noninterpretable_as_int_str_and_int_minus_float():
    """'abc'+2-3.4"""
    ast = AddExpr([StrLiteral("abc"), IntLiteral(2), FloatLiteral(3.4)], ["+", "-"])
    printer = PrettyPrinter()
    expected = "'abc' + 2 - 3.4"
    result = printer.print(ast)
    assert expected == result


def test_print_multi_int_and_int():
    """1*2"""
    ast = MultiExpr([IntLiteral(1), IntLiteral(2)], ["*"])
    printer = PrettyPrinter()
    expected = "1 * 2"
    result = printer.print(ast)
    assert expected == result


def test_print_multi_int_and_zero():
    """1*0"""
    ast = MultiExpr([IntLiteral(1), IntLiteral(0)], ["*"])
    printer = PrettyPrinter()
    expected = "1 * 0"
    result = printer.print(ast)
    assert expected == result


def test_print_multi_zero_and_int():
    """0*1"""
    ast = MultiExpr([IntLiteral(0), IntLiteral(1)], ["*"])
    printer = PrettyPrinter()
    expected = "0 * 1"
    result = printer.print(ast)
    assert expected == result


def test_print_multi_zero_and_int_divide_by_int():
    """0*1/2"""
    ast = MultiExpr([IntLiteral(0), IntLiteral(1), IntLiteral(2)], ["*", "/"])
    printer = PrettyPrinter()
    expected = "0 * 1 / 2"
    result = printer.print(ast)
    assert expected == result


def test_print_int_divide_by_zero():
    """1/0"""
    ast = MultiExpr([IntLiteral(1), IntLiteral(0)], ["/"])
    printer = PrettyPrinter()
    expected = "1 / 0"
    result = printer.print(ast)
    assert expected == result


def test_print_zero_times_zero():
    """0*0"""
    ast = MultiExpr([IntLiteral(0), IntLiteral(0)], ["*"])
    printer = PrettyPrinter()
    expected = "0 * 0"
    result = printer.print(ast)
    assert expected == result


def test_print_zero_divided_by_zero():
    """0/0"""
    ast = MultiExpr([IntLiteral(0), IntLiteral(0)], ["/"])
    printer = PrettyPrinter()
    expected = "0 / 0"
    result = printer.print(ast)
    assert expected == result


def test_print_zero_divided_by_zero_but_floats():
    """0.0/0.0"""
    ast = MultiExpr([FloatLiteral(0.0), FloatLiteral(0.0)], ["/"])
    printer = PrettyPrinter()
    expected = "0.0 / 0.0"
    result = printer.print(ast)
    assert expected == result


def test_print_interpretable_as_int_str_divided_by_zero():
    """'1'/0"""
    ast = MultiExpr([StrLiteral("1"), IntLiteral(0)], ["/"])
    printer = PrettyPrinter()
    expected = "'1' / 0"
    result = printer.print(ast)
    assert expected == result


def test_print_interpretable_as_int_str_divided_by_interpretable_as_int_str_zero():
    """'1'/'0'"""
    ast = MultiExpr([StrLiteral("1"), StrLiteral("0")], ["/"])
    printer = PrettyPrinter()
    expected = "'1' / '0'"
    result = printer.print(ast)
    assert expected == result


def test_print_interpretable_as_int_str_divided_by_interpretable_as_float_str_zero():
    """'1'/'0.0'"""
    ast = MultiExpr([StrLiteral("1"), StrLiteral("0.0")], ["/"])
    printer = PrettyPrinter()
    expected = "'1' / '0.0'"
    result = printer.print(ast)
    assert expected == result


def test_sum_of_number_and_multiplication():
    """1+2*3"""
    ast = AddExpr(
        [IntLiteral(1), MultiExpr([IntLiteral(2), IntLiteral(3)], ["*"])], ["+"]
    )
    printer = PrettyPrinter()
    expected = "1 + 2 * 3"
    result = printer.print(ast)
    assert expected == result


def test_unary_of_multiplication():
    """-(1 * 2)"""
    ast = UnaryExpr(MultiExpr([IntLiteral(1), IntLiteral(2)], ["*"]))
    printer = PrettyPrinter()
    expected = "-(1 * 2)"
    result = printer.print(ast)
    assert expected == result


def test_unary_of_division():
    """-(1 / 2)"""
    ast = UnaryExpr(MultiExpr([IntLiteral(1), IntLiteral(2)], ["/"]))
    printer = PrettyPrinter()
    expected = "-(1 / 2)"
    result = printer.print(ast)
    assert expected == result


def test_unary_of_sum():
    """-(1 + 2)"""
    ast = UnaryExpr(AddExpr([IntLiteral(1), IntLiteral(2)], ["+"]))
    printer = PrettyPrinter()
    expected = "-(1 + 2)"
    result = printer.print(ast)
    assert expected == result


def test_unary_of_subtraction():
    """-(1 - 2)"""
    ast = UnaryExpr(AddExpr([IntLiteral(1), IntLiteral(2)], ["-"]))
    printer = PrettyPrinter()
    expected = "-(1 - 2)"
    result = printer.print(ast)
    assert expected == result


multi_operators = ["*", "/"]
rel_operators = ["<", "<=", "!=", "==", ">=", ">"]


@pytest.mark.parametrize("rel_operator", rel_operators)
def test_unary_relation_less_than(rel_operator):
    """-(1 [operator] 2)"""
    ast = UnaryExpr(RelationExpr(IntLiteral(1), IntLiteral(2), rel_operator))
    printer = PrettyPrinter()
    expected = f"-(1 {rel_operator} 2)"
    result = printer.print(ast)
    assert expected == result


def test_unary_of_logic_and():
    """-(1 & 2)"""
    ast = UnaryExpr(AndExpr([IntLiteral(1), IntLiteral(2)]))
    printer = PrettyPrinter()
    expected = "-(1 & 2)"
    result = printer.print(ast)
    assert expected == result


def test_unary_of_logic_or():
    """-(1 | 2)"""
    ast = UnaryExpr(OrExpr([IntLiteral(1), IntLiteral(2)]))
    printer = PrettyPrinter()
    expected = "-(1 | 2)"
    result = printer.print(ast)
    assert expected == result


def test_multiplication_of_sum():
    """(1 + 2) * 3"""
    ast = MultiExpr(
        [AddExpr([IntLiteral(1), IntLiteral(2)], ["+"]), IntLiteral(3)], ["*"]
    )
    printer = PrettyPrinter()
    expected = "(1 + 2) * 3"
    result = printer.print(ast)
    assert expected == result


def test_multiplication_of_sums():
    """(1 + 2) * (3 + 4)"""
    ast = MultiExpr(
        [
            AddExpr([IntLiteral(1), IntLiteral(2)], ["+"]),
            AddExpr([IntLiteral(3), IntLiteral(4)], ["+"]),
        ],
        ["*"],
    )
    printer = PrettyPrinter()
    expected = "(1 + 2) * (3 + 4)"
    result = printer.print(ast)
    assert expected == result


def test_division_of_sum():
    """(1 + 2) / 3"""
    ast = MultiExpr(
        [AddExpr([IntLiteral(1), IntLiteral(2)], ["+"]), IntLiteral(3)], ["/"]
    )
    printer = PrettyPrinter()
    expected = "(1 + 2) / 3"
    result = printer.print(ast)
    assert expected == result


def test_sum_divided_by_unary():
    """(1 + 2) / -3"""
    ast = MultiExpr(
        [AddExpr([IntLiteral(1), IntLiteral(2)], ["+"]), UnaryExpr(IntLiteral(3))],
        ["/"],
    )
    printer = PrettyPrinter()
    expected = "(1 + 2) / -3"
    result = printer.print(ast)
    assert expected == result


def test_sum_divided_by_unary_sum():
    """(1 + 2) / -(3 + 4)"""
    ast = MultiExpr(
        [
            AddExpr([IntLiteral(1), IntLiteral(2)], ["+"]),
            UnaryExpr(AddExpr([IntLiteral(3), IntLiteral(4)], ["+"])),
        ],
        ["/"],
    )
    printer = PrettyPrinter()
    expected = "(1 + 2) / -(3 + 4)"
    result = printer.print(ast)
    assert expected == result


def test_unary_sum_divided_by_unary_sum():
    """-(1 + 2) / -(3 + 4)"""
    ast = MultiExpr(
        [
            UnaryExpr(AddExpr([IntLiteral(1), IntLiteral(2)], ["+"])),
            UnaryExpr(AddExpr([IntLiteral(3), IntLiteral(4)], ["+"])),
        ],
        ["/"],
    )
    printer = PrettyPrinter()
    expected = "-(1 + 2) / -(3 + 4)"
    result = printer.print(ast)
    assert expected == result


@pytest.mark.parametrize("multi_operator", multi_operators)
@pytest.mark.parametrize("rel_operator", rel_operators)
def test_multiplication_of_relative(multi_operator: str, rel_operator: str):
    """(1 [operator] 2) * 3"""
    ast = MultiExpr(
        [RelationExpr(IntLiteral(1), IntLiteral(2), rel_operator), IntLiteral(3)],
        [multi_operator],
    )
    printer = PrettyPrinter()
    expected = f"(1 {rel_operator} 2) {multi_operator} 3"
    result = printer.print(ast)
    assert expected == result


@pytest.mark.parametrize("multi_operator", multi_operators)
@pytest.mark.parametrize("rel_operator", rel_operators)
def test_multi_of_relative_and_unary(multi_operator: str, rel_operator: str):
    """(1 [operator] 2) [* | /] 3"""
    ast = MultiExpr(
        [
            RelationExpr(IntLiteral(1), IntLiteral(2), rel_operator),
            UnaryExpr(IntLiteral(3)),
        ],
        [multi_operator],
    )
    printer = PrettyPrinter()
    expected = f"(1 {rel_operator} 2) {multi_operator} -3"
    result = printer.print(ast)
    assert expected == result


@pytest.mark.parametrize("multi_op", multi_operators)
@pytest.mark.parametrize("rel_op1", rel_operators)
@pytest.mark.parametrize("rel_op2", rel_operators)
def test_multi_of_relative_and_relative(multi_op: str, rel_op1: str, rel_op2: str):
    """(1 [operator1] 2) [* | /] (3 [operator2] 4)"""
    ast = MultiExpr(
        [
            RelationExpr(IntLiteral(1), IntLiteral(2), rel_op1),
            RelationExpr(IntLiteral(3), IntLiteral(4), rel_op2),
        ],
        [multi_op],
    )
    printer = PrettyPrinter()
    expected = f"(1 {rel_op1} 2) {multi_op} (3 {rel_op2} 4)"
    result = printer.print(ast)
    assert expected == result


@pytest.mark.parametrize("multi_op", multi_operators)
@pytest.mark.parametrize("rel_op1", rel_operators)
@pytest.mark.parametrize("rel_op2", rel_operators)
def test_multi_of_unary_relative_and_relative(
    multi_op: str, rel_op1: str, rel_op2: str
):
    """-(1 [operator1] 2) [* | /] (3 [operator2] 4)"""
    ast = MultiExpr(
        [
            UnaryExpr(RelationExpr(IntLiteral(1), IntLiteral(2), rel_op1)),
            RelationExpr(IntLiteral(3), IntLiteral(4), rel_op2),
        ],
        [multi_op],
    )
    printer = PrettyPrinter()
    expected = f"-(1 {rel_op1} 2) {multi_op} (3 {rel_op2} 4)"
    result = printer.print(ast)
    assert expected == result


@pytest.mark.parametrize("multi_op", multi_operators)
@pytest.mark.parametrize("rel_op1", rel_operators)
@pytest.mark.parametrize("rel_op2", rel_operators)
def test_multi_of_relative_and_unary_relative(
    multi_op: str, rel_op1: str, rel_op2: str
):
    """(1 [operator1] 2) [* | /] -(3 [operator2] 4)"""
    ast = MultiExpr(
        [
            RelationExpr(IntLiteral(1), IntLiteral(2), rel_op1),
            UnaryExpr(RelationExpr(IntLiteral(3), IntLiteral(4), rel_op2)),
        ],
        [multi_op],
    )
    printer = PrettyPrinter()
    expected = f"(1 {rel_op1} 2) {multi_op} -(3 {rel_op2} 4)"
    result = printer.print(ast)
    assert expected == result


@pytest.mark.parametrize("multi_op", multi_operators)
@pytest.mark.parametrize("rel_op1", rel_operators)
@pytest.mark.parametrize("rel_op2", rel_operators)
def test_multi_of_unary_relative_and_unary_relative(
    multi_op: str, rel_op1: str, rel_op2: str
):
    """-(1 [operator1] 2) [* | /] -(3 [operator2] 4)"""
    ast = MultiExpr(
        [
            UnaryExpr(RelationExpr(IntLiteral(1), IntLiteral(2), rel_op1)),
            UnaryExpr(RelationExpr(IntLiteral(3), IntLiteral(4), rel_op2)),
        ],
        [multi_op],
    )
    printer = PrettyPrinter()
    expected = f"-(1 {rel_op1} 2) {multi_op} -(3 {rel_op2} 4)"
    result = printer.print(ast)
    assert expected == result


logical_operators_class_pair = [("&", AndExpr), ("|", OrExpr)]


@pytest.mark.parametrize("multi_op", multi_operators)
@pytest.mark.parametrize("logical_op_pair", logical_operators_class_pair)
def test_multi_of_logical_and_number(
    multi_op: str, logical_op_pair: tuple[str, AndExpr | OrExpr]
):
    """(1 [operator] 2) [* | /] 3"""
    logical_op, class_ = logical_op_pair
    ast = MultiExpr([class_([IntLiteral(1), IntLiteral(2)]), IntLiteral(3)], [multi_op])
    printer = PrettyPrinter()
    expected = f"(1 {logical_op} 2) {multi_op} 3"
    result = printer.print(ast)
    assert expected == result


add_operators = ["+", "-"]


@pytest.mark.parametrize("rel_operator", rel_operators)
@pytest.mark.parametrize("add_op", add_operators)
def test_add_of_relative_and_number(add_op: str, rel_operator: str):
    """(1 [operator] 2) [+ | -] 3"""
    ast = AddExpr(
        [RelationExpr(IntLiteral(1), IntLiteral(2), rel_operator), IntLiteral(3)],
        [add_op],
    )
    printer = PrettyPrinter()
    expected = f"(1 {rel_operator} 2) {add_op} 3"
    result = printer.print(ast)
    assert expected == result


@pytest.mark.parametrize("logical_op_pair", logical_operators_class_pair)
@pytest.mark.parametrize("add_op", add_operators)
def test_add_of_logical(add_op: str, logical_op_pair: tuple[str, AndExpr | OrExpr]):
    """(1 [operator] 2) [+ | -] 3"""
    logical_op, class_ = logical_op_pair
    ast = AddExpr([class_([IntLiteral(1), IntLiteral(2)]), IntLiteral(3)], [add_op])
    printer = PrettyPrinter()
    expected = f"(1 {logical_op} 2) {add_op} 3"
    result = printer.print(ast)
    assert expected == result


@pytest.mark.parametrize("rel_op", rel_operators)
def test_relation_of_logical_and(rel_op: str):
    """(1 & 2) [rel_op] 3"""
    ast = RelationExpr(AndExpr([IntLiteral(1), IntLiteral(2)]), IntLiteral(3), rel_op)
    printer = PrettyPrinter()
    expected = f"(1 & 2) {rel_op} 3"
    result = printer.print(ast)
    assert expected == result


@pytest.mark.parametrize("rel_op", rel_operators)
def test_relation_of_logical_or(rel_op: str):
    """(1 | 2) [rel_op] 3"""
    ast = RelationExpr(OrExpr([IntLiteral(1), IntLiteral(2)]), IntLiteral(3), rel_op)
    printer = PrettyPrinter()
    expected = f"(1 | 2) {rel_op} 3"
    result = printer.print(ast)
    assert expected == result


def test_1_or_2_all_and_3():
    """(1 | 2) & 3"""
    ast = AndExpr([OrExpr([IntLiteral(1), IntLiteral(2)]), IntLiteral(3)])
    printer = PrettyPrinter()
    expected = "(1 | 2) & 3"
    result = printer.print(ast)
    assert expected == result


def test_print_zero_or_one():
    """0|1"""
    ast = OrExpr([IntLiteral(0), IntLiteral(1)])
    printer = PrettyPrinter()
    expected = "0 | 1"
    result = printer.print(ast)
    assert expected == result


def test_print_one_or_zero():
    """1|0"""
    ast = OrExpr([IntLiteral(1), IntLiteral(0)])
    printer = PrettyPrinter()
    expected = "1 | 0"
    result = printer.print(ast)
    assert expected == result


def test_print_zero_or_zero_as_float_or_zero_as_int_str_or_zero_as_float_str_or_one():
    """0|0.0|'0'|'0.0'|1"""
    ast = OrExpr(
        [
            IntLiteral(0),
            FloatLiteral(0.0),
            StrLiteral("0"),
            StrLiteral("0.0"),
            IntLiteral(1),
        ]
    )
    printer = PrettyPrinter()
    expected = "0 | 0.0 | '0' | '0.0' | 1"
    result = printer.print(ast)
    assert expected == result


def test_print_one_and_zero():
    """1&0"""
    ast = AndExpr([IntLiteral(1), IntLiteral(0)])
    printer = PrettyPrinter()
    expected = "1 & 0"
    result = printer.print(ast)
    assert expected == result


def test_print_one_and_float():
    """1&1.2"""
    ast = AndExpr([IntLiteral(1), FloatLiteral(1.2)])
    printer = PrettyPrinter()
    expected = "1 & 1.2"
    result = printer.print(ast)
    assert expected == result


def test_print_one_and_float_and_one_as_int_str():
    """1&1.2&'1'"""
    ast = AndExpr([IntLiteral(1), FloatLiteral(1.2), StrLiteral("1")])
    printer = PrettyPrinter()
    expected = "1 & 1.2 & '1'"
    result = printer.print(ast)
    assert expected == result


def test_print_and_all_types_interpetable_as_true():
    """1&1.2&'1'&'1.2'"""
    ast = AndExpr(
        [IntLiteral(1), FloatLiteral(1.2), StrLiteral("1"), StrLiteral("1.2")]
    )
    printer = PrettyPrinter()
    expected = "1 & 1.2 & '1' & '1.2'"
    result = printer.print(ast)
    assert expected == result


def test_and_or_and():
    """0&1|2&3"""
    ast = OrExpr(
        [
            AndExpr([IntLiteral(0), IntLiteral(1)]),
            AndExpr([IntLiteral(2), IntLiteral(3)]),
        ]
    )
    printer = PrettyPrinter()
    expected = "0 & 1 | 2 & 3"
    result = printer.print(ast)
    assert expected == result


def test_or_and_or():
    """0|1&2|3"""
    ast = OrExpr(
        [IntLiteral(0), AndExpr([IntLiteral(1), IntLiteral(2)]), IntLiteral(3)]
    )
    printer = PrettyPrinter()
    expected = "0 | 1 & 2 | 3"
    result = printer.print(ast)
    assert expected == result


def test_print_less_than():
    """1<2"""
    ast = RelationExpr(IntLiteral(1), IntLiteral(2), "<")
    printer = PrettyPrinter()
    expected = "1 < 2"
    result = printer.print(ast)
    assert expected == result


def test_print_less_eq_than():
    """1<=2"""
    ast = RelationExpr(IntLiteral(1), IntLiteral(2), "<=")
    printer = PrettyPrinter()
    expected = "1 <= 2"
    result = printer.print(ast)
    assert expected == result


def test_print_greater_than():
    """1>2"""
    ast = RelationExpr(IntLiteral(1), IntLiteral(2), ">")
    printer = PrettyPrinter()
    expected = "1 > 2"
    result = printer.print(ast)
    assert expected == result


def test_print_greater_eq_than():
    """1>=2"""
    ast = RelationExpr(IntLiteral(1), IntLiteral(2), ">=")
    printer = PrettyPrinter()
    expected = "1 >= 2"
    result = printer.print(ast)
    assert expected == result


def test_print_not_eq_than():
    """1!=2"""
    ast = RelationExpr(IntLiteral(1), IntLiteral(2), "!=")
    printer = PrettyPrinter()
    expected = "1 != 2"
    result = printer.print(ast)
    assert expected == result


def test_print_eq_than():
    """1==2"""
    ast = RelationExpr(IntLiteral(1), IntLiteral(2), "==")
    printer = PrettyPrinter()
    expected = "1 == 2"
    result = printer.print(ast)
    assert expected == result


def test_complex_part_1():
    """-(1 < 2 & 3 >= 4)"""
    ast = UnaryExpr(
        AndExpr(
            [
                RelationExpr(IntLiteral(1), IntLiteral(2), "<"),
                RelationExpr(IntLiteral(3), IntLiteral(4), ">="),
            ]
        )
    )
    printer = PrettyPrinter()
    expected = "-(1 < 2 & 3 >= 4)"
    result = printer.print(ast)
    assert expected == result


def test_complex_part_2():
    """5 != 6 & (7 == 8 | 9 > 10)"""
    ast = AndExpr(
        [
            RelationExpr(IntLiteral(5), IntLiteral(6), "!="),
            OrExpr(
                [
                    RelationExpr(IntLiteral(7), IntLiteral(8), "=="),
                    RelationExpr(IntLiteral(9), IntLiteral(10), ">"),
                ]
            ),
        ]
    )
    printer = PrettyPrinter()
    expected = "5 != 6 & (7 == 8 | 9 > 10)"
    result = printer.print(ast)
    assert expected == result


def test_complex_part_3():
    """(11 <= 12 | 13 > 14) & -15 < 16 | 17 == 18 & -19 >= 20"""
    ast = OrExpr(
        [
            AndExpr(
                [
                    OrExpr(
                        [
                            RelationExpr(IntLiteral(11), IntLiteral(12), "<="),
                            RelationExpr(IntLiteral(13), IntLiteral(14), ">"),
                        ]
                    ),
                    RelationExpr(UnaryExpr(IntLiteral(15)), IntLiteral(16), "<"),
                ]
            ),
            AndExpr(
                [
                    RelationExpr(IntLiteral(17), IntLiteral(18), "=="),
                    RelationExpr(UnaryExpr(IntLiteral(19)), IntLiteral(20), ">="),
                ]
            ),
        ]
    )
    printer = PrettyPrinter()
    expected = "(11 <= 12 | 13 > 14) & -15 < 16 | 17 == 18 & -19 >= 20"
    result = printer.print(ast)
    assert expected == result


def test_print_complex_logical_expr():
    """-(1 < 2 & 3 >= 4) |
    5 != 6 & (7 == 8 | 9 > 10) & ((11 <= 12 | 13 > 14) & -15 < 16 | 17 == 18 & -19 >= 20) |
    21 != 22 & (23 < 24 | 25 >= 26) |
    -(27 == 28) & (29 != 30 | 31 <= 32)"""
    ast = OrExpr(
        [
            UnaryExpr(
                AndExpr(
                    [
                        RelationExpr(IntLiteral(1), IntLiteral(2), "<"),
                        RelationExpr(IntLiteral(3), IntLiteral(4), ">="),
                    ]
                )
            ),
            AndExpr(
                [
                    AndExpr(
                        [
                            RelationExpr(IntLiteral(5), IntLiteral(6), "!="),
                            OrExpr(
                                [
                                    RelationExpr(IntLiteral(7), IntLiteral(8), "=="),
                                    RelationExpr(IntLiteral(9), IntLiteral(10), ">"),
                                ]
                            ),
                        ]
                    ),
                    OrExpr(
                        [
                            AndExpr(
                                [
                                    OrExpr(
                                        [
                                            RelationExpr(
                                                IntLiteral(11), IntLiteral(12), "<="
                                            ),
                                            RelationExpr(
                                                IntLiteral(13), IntLiteral(14), ">"
                                            ),
                                        ]
                                    ),
                                    RelationExpr(
                                        UnaryExpr(IntLiteral(15)), IntLiteral(16), "<"
                                    ),
                                ]
                            ),
                            AndExpr(
                                [
                                    RelationExpr(IntLiteral(17), IntLiteral(18), "=="),
                                    RelationExpr(
                                        UnaryExpr(IntLiteral(19)), IntLiteral(20), ">="
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
            AndExpr(
                [
                    RelationExpr(IntLiteral(21), IntLiteral(22), "!="),
                    OrExpr(
                        [
                            RelationExpr(IntLiteral(23), IntLiteral(24), "<"),
                            RelationExpr(IntLiteral(25), IntLiteral(26), ">="),
                        ]
                    ),
                ]
            ),
            AndExpr(
                [
                    UnaryExpr(RelationExpr(IntLiteral(27), IntLiteral(28), "==")),
                    OrExpr(
                        [
                            RelationExpr(IntLiteral(29), IntLiteral(30), "!="),
                            RelationExpr(IntLiteral(31), IntLiteral(32), "<="),
                        ]
                    ),
                ]
            ),
        ]
    )
    printer = PrettyPrinter()
    expected = "-(1 < 2 & 3 >= 4) | 5 != 6 & (7 == 8 | 9 > 10) & ((11 <= 12 | 13 > 14) & -15 < 16 | 17 == 18 & -19 >= 20) | 21 != 22 & (23 < 24 | 25 >= 26) | -(27 == 28) & (29 != 30 | 31 <= 32)"
    result = printer.print(ast)
    assert expected == result


def test_object_access_simple_identifier():
    """a"""
    ast = ObjectAccess(["a"])
    expected = "a"
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_object_access_one_dot():
    """a.b"""
    ast = ObjectAccess(["a", "b"])
    expected = "a.b"
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_object_access_one_dot_same_name():
    """a.a"""
    ast = ObjectAccess(["a", "a"])
    expected = "a.a"
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_object_access_4_dots():
    """a.b.c.d.e"""
    ast = ObjectAccess(["a", "b", "c", "d", "e"])
    expected = "a.b.c.d.e"
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_assignment_simple():
    """a=1"""
    ast = AssignmentStatement(ObjectAccess(["a"]), IntLiteral(1))
    expected = "a = 1;\n"
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_assignment_object_access_chained():
    """a.b.c.d=1"""
    ast = AssignmentStatement(ObjectAccess(["a", "b", "c", "d"]), IntLiteral(1))
    expected = "a.b.c.d = 1;\n"
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_assignment_more_complicated_expr():
    """a=(1+2*3)/4"""
    ast = AssignmentStatement(
        ObjectAccess(["a"]),
        MultiExpr(
            [
                AddExpr(
                    [IntLiteral(1), MultiExpr([IntLiteral(2), IntLiteral(3)], ["*"])],
                    ["+"],
                ),
                IntLiteral(4),
            ],
            ["/"],
        ),
    )
    expected = "a = (1 + 2 * 3) / 4;\n"
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_empty_program():
    # TODO can empty program even exist?
    """<Empty>"""
    ast = Program([])
    expected = ""
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_program_with_assignment():
    """a=1;"""
    ast = Program([AssignmentStatement(ObjectAccess(["a"]), IntLiteral(1))])
    expected = "a = 1;\n"
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_variable_declaration():
    """a: int;"""
    ast = VariableDeclaration("a", "int", False)
    expected = "a : int;\n"
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_mutable_variable_declaration():
    """a: mut int;"""
    ast = VariableDeclaration("a", "int", True)
    expected = "a : mut int;\n"
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_mutable_variable_declaration_float():
    """a: mut float;"""
    ast = VariableDeclaration("a", "float", True)
    expected = "a : mut float;\n"
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_mutable_variable_declaration_MyType():
    """a: mut MyType;"""
    ast = VariableDeclaration("a", "MyType", True)
    expected = "a : mut MyType;\n"
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_simple_if_empty_program():
    """if 1 begin end"""
    ast = IfStatement(IntLiteral(1), Program([]))
    expected = "if 1\nbegin\nend\n"
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_simple_if_assignment():
    """if 1 begin a = 12; end"""
    ast = IfStatement(
        IntLiteral(1),
        Program([AssignmentStatement(ObjectAccess(["a"]), IntLiteral(12))]),
    )
    expected = "if 1\nbegin\n    a = 12;\nend\n"
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_if_assignment_else_assignment():
    """if 1 begin a = 12; end else begin a = 123; end"""
    ast = IfStatement(
        IntLiteral(1),
        Program([AssignmentStatement(ObjectAccess(["a"]), IntLiteral(12))]),
        Program([AssignmentStatement(ObjectAccess(["a"]), IntLiteral(123))]),
    )
    expected = "if 1\nbegin\n    a = 12;\nend\nelse\nbegin\n    a = 123;\nend\n"
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_simple_while():
    """while 1 begin a = a + 1; end"""
    ast = WhileStatement(
        IntLiteral(1),
        Program(
            [
                AssignmentStatement(
                    ObjectAccess(["a"]),
                    AddExpr([ObjectAccess(["a"]), IntLiteral(1)], ["+"]),
                )
            ]
        ),
    )
    expected = "while 1\nbegin\n    a = a + 1;\nend\n"
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_named_type():
    """p2d : Punkt2D;"""
    ast = NamedType("p2d", "Punkt2D")
    expected = "p2d : Punkt2D;\n"
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_variant_def():
    """
    Punkt : variant
    begin
        p2d : Punkt2D;
        p3d : Punkt3D;
    end
    """
    ast = VariantDef(
        "Punkt", [NamedType("p2d", "Punkt2D"), NamedType("p3d", "Punkt3D")]
    )
    expected = "Punkt : variant\nbegin\n    p2d : Punkt2D;\n    p3d : Punkt3D;\nend\n"
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_case_section():
    """
    case Punkt2D
    begin
        wiadmosc = '[' + p2d.x + '; ' +p2d.y + ']';
    end
    """
    ast = CaseSection(
        "Punkt2D",
        Program(
            [
                AssignmentStatement(
                    ObjectAccess(["wiadomosc"]),
                    AddExpr(
                        [
                            StrLiteral("["),
                            ObjectAccess(["p2d", "x"]),
                            StrLiteral("; "),
                            ObjectAccess(["p2d", "y"]),
                            StrLiteral("]"),
                        ],
                        ["+", "+", "+", "+"],
                    ),
                )
            ]
        ),
    )
    expected = (
        "case Punkt2D\nbegin\n    wiadomosc = '[' + p2d.x + '; ' + p2d.y + ']';\nend\n"
    )
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_visit_punkt_example():
    """
    visit punkt
    begin
        case Punkt2D
        begin
            wiadmosc = '[' + p2d.x + '; ' + p2d.y + ']';
        end
        case Punkt3D
        begin
            wiadmosc = '[' + p3d.x + '; ' + p3d.y + '; ' + p3d.z + ']';
        end
    end
    """
    ast = VisitStatement(
        ObjectAccess(["punkt"]),
        [
            CaseSection(
                "Punkt2D",
                Program(
                    [
                        AssignmentStatement(
                            ObjectAccess(["wiadomosc"]),
                            AddExpr(
                                [
                                    StrLiteral("["),
                                    ObjectAccess(["p2d", "x"]),
                                    StrLiteral("; "),
                                    ObjectAccess(["p2d", "y"]),
                                    StrLiteral("]"),
                                ],
                                ["+", "+", "+", "+"],
                            ),
                        )
                    ]
                ),
            ),
            CaseSection(
                "Punkt3D",
                Program(
                    [
                        AssignmentStatement(
                            ObjectAccess(["wiadomosc"]),
                            AddExpr(
                                [
                                    StrLiteral("["),
                                    ObjectAccess(["p3d", "x"]),
                                    StrLiteral("; "),
                                    ObjectAccess(["p3d", "y"]),
                                    StrLiteral("; "),
                                    ObjectAccess(["p3d", "z"]),
                                    StrLiteral("]"),
                                ],
                                ["+", "+", "+", "+", "+", "+"],
                            ),
                        )
                    ]
                ),
            ),
        ],
    )

    expected = "visit punkt\nbegin\n    case Punkt2D\n    begin\n        wiadomosc = '[' + p2d.x + '; ' + p2d.y + ']';\n    end\n    case Punkt3D\n    begin\n        wiadomosc = '[' + p3d.x + '; ' + p3d.y + '; ' + p3d.z + ']';\n    end\nend\n"
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_struct_example_Punkt1D():
    """
    Point1D : struct
    begin
    x : mut int = 0; @ wartość domyślna wynosi 0
    end
    """
    ast = StructDef("Point1D", [VariableDeclaration("x", "int", True, IntLiteral(0))])
    expected = "Point1D : struct\nbegin\n    x : mut int = 0;\nend\n"
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_struct_example_Punkt2D():
    """
    Point2D : struct
    begin
    x : mut int = 0; @ wartość domyślna wynosi 0
    y : mut int = 0; @ wartość domyślna wynosi 0
    end
    """
    ast = StructDef(
        "Point2D",
        [
            VariableDeclaration("x", "int", True, IntLiteral(0)),
            VariableDeclaration("y", "int", True, IntLiteral(0)),
        ],
    )
    expected = (
        "Point2D : struct\nbegin\n    x : mut int = 0;\n    y : mut int = 0;\nend\n"
    )
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_empty_struct():
    """Cos : struct begin end"""
    ast = StructDef("Cos", [])
    expected = "Cos : struct\nbegin\nend\n"
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_empty_func_def_no_params():
    """nothing_func() : null_type begin end"""
    ast = FuncDef("nothing_func", [], "null_type", Program([]))
    expected = "nothing_func() : null_type\nbegin\nend\n"
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_empty_func_def_one_int_param():
    """nothing_func(arg1 : int) : null_type begin end"""
    ast = FuncDef(
        "nothing_func", [Param("arg1", "int", False)], "null_type", Program([])
    )
    expected = "nothing_func(arg1 : int) : null_type\nbegin\nend\n"
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_func_def_example_nested_function():
    """
    add(arg1: int, arg2: int) : int
    begin
        add_sub_function(arg1: int, arg2: int) : int
        begin
            return arg1 + arg2;
        end

        add(arg1: int, arg2: int) : int
        begin
            return add_sub_function(arg1, arg2);
        end

        return add(arg1, arg2);
    end
    """
    ast = FuncDef(
        "add",
        [Param("arg1", "int", False), Param("arg2", "int", False)],
        "int",
        Program(
            [
                FuncDef(
                    "add_sub_function",
                    [Param("arg1", "int", False), Param("arg2", "int", False)],
                    "int",
                    Program(
                        [
                            ReturnStatement(
                                AddExpr(
                                    [ObjectAccess(["arg1"]), ObjectAccess(["arg2"])],
                                    ["+"],
                                )
                            )
                        ]
                    ),
                ),
                FuncDef(
                    "add",
                    [Param("arg1", "int", False), Param("arg2", "int", False)],
                    "int",
                    Program(
                        [
                            ReturnStatement(
                                FunctionCall(
                                    "add_sub_function",
                                    [ObjectAccess(["arg1"]), ObjectAccess(["arg2"])],
                                )
                            )
                        ]
                    ),
                ),
                ReturnStatement(
                    FunctionCall(
                        "add", [ObjectAccess(["arg1"]), ObjectAccess(["arg2"])]
                    )
                ),
            ]
        ),
    )
    expected = """add(arg1 : int, arg2 : int) : int
begin
    add_sub_function(arg1 : int, arg2 : int) : int
    begin
        return arg1 + arg2;
    end
    add(arg1 : int, arg2 : int) : int
    begin
        return add_sub_function(arg1, arg2);
    end
    return add(arg1, arg2);
end
"""
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected


def test_simple_return():
    """return 0;"""
    ast = ReturnStatement(IntLiteral(0))
    expected = "return 0;\n"
    printer = PrettyPrinter()
    result = printer.print(ast)
    assert result == expected
