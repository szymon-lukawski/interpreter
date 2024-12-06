import pytest
from token_type import TokenType
from interpreter import Interpreter
from AST import *
from multiprocessing import Process


def test_sanity():
    """."""
    assert 1 == True


def test_no_arg_function():
    """return_one () : int begin return 1; end a : int = return_one();"""
    ast = Program(
        [
            FuncDef("return_one", [], "int", Program([ReturnStatement(IntLiteral(1))])),
            VariableDeclaration(
                "a",
                "int",
                False,
                ObjectAccess(
                    [
                        FunctionCall("return_one", []),
                    ]
                ),
            ),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.scopes.get_variable_value("a") == 1


def test_sum_of_two_no_arg_functions():
    """return_one () : int begin return 1; end  return_two () : int begin return 2; end a : int = return_one() + return_two();"""
    ast = Program(
        [
            FuncDef("return_one", [], "int", Program([ReturnStatement(IntLiteral(1))])),
            FuncDef("return_two", [], "int", Program([ReturnStatement(IntLiteral(2))])),
            VariableDeclaration(
                "a",
                "int",
                False,
                AddExpr(
                    [
                        ObjectAccess(
                            [
                                FunctionCall("return_one", []),
                            ]
                        ),
                        ObjectAccess(
                            [
                                FunctionCall("return_two", []),
                            ]
                        ),
                    ],
                    ["+"],
                ),
            ),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.scopes.get_variable_value("a") == 3


def test_func_with_one_arg():
    """add_one(a : int) : int begin return a + 1; end b : int = add_one(2);"""
    ast = Program(
        [
            FuncDef(
                "add_one",
                [Param("a", "int", False)],
                "int",
                Program(
                    [
                        ReturnStatement(
                            AddExpr(
                                [
                                    ObjectAccess(
                                        [
                                            "a",
                                        ]
                                    ),
                                    IntLiteral(1),
                                ],
                                ["+"],
                            )
                        )
                    ]
                ),
            ),
            VariableDeclaration(
                "b",
                "int",
                False,
                ObjectAccess(
                    [
                        FunctionCall("add_one", [IntLiteral(2)]),
                    ]
                ),
            ),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.scopes.get_variable_value("b") == 3


def test_add_two_integers():
    """add(a:int, b: int):int begin return a + b; end c : int = add(1,2);"""
    ast = Program(
        [
            FuncDef(
                "add",
                [Param("a", "int", False), Param("b", "int", False)],
                "int",
                Program(
                    [
                        ReturnStatement(
                            AddExpr(
                                [
                                    ObjectAccess(
                                        [
                                            "a",
                                        ]
                                    ),
                                    ObjectAccess(
                                        [
                                            "b",
                                        ]
                                    ),
                                ],
                                ["+"],
                            )
                        )
                    ]
                ),
            ),
            VariableDeclaration(
                "c",
                "int",
                False,
                ObjectAccess(
                    [
                        FunctionCall("add", [IntLiteral(1), IntLiteral(2)]),
                    ]
                ),
            ),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.scopes.get_variable_value("c") == 3


def test_add_three_integers():
    """add(a:int, b: int, c: int):int begin return a + b + c; end d : int = add(1,2,3);"""
    ast = Program(
        [
            FuncDef(
                "add",
                [
                    Param("a", "int", False),
                    Param("b", "int", False),
                    Param("c", "int", False),
                ],
                "int",
                Program(
                    [
                        ReturnStatement(
                            AddExpr(
                                [
                                    ObjectAccess(
                                        [
                                            "a",
                                        ]
                                    ),
                                    ObjectAccess(
                                        [
                                            "b",
                                        ]
                                    ),
                                    ObjectAccess(
                                        [
                                            "c",
                                        ]
                                    ),
                                ],
                                ["+", "+"],
                            )
                        )
                    ]
                ),
            ),
            VariableDeclaration(
                "d",
                "int",
                False,
                ObjectAccess(
                    [
                        FunctionCall(
                            "add", [IntLiteral(1), IntLiteral(2), IntLiteral(3)]
                        ),
                    ]
                ),
            ),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.scopes.get_variable_value("d") == 6
