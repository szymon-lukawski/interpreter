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


def test_two_returns():
    """a() : int begin return 1; return 2; end b : int = a();"""
    ast = Program(
        [
            FuncDef(
                "a",
                [],
                "int",
                Program(
                    [ReturnStatement(IntLiteral(1)), ReturnStatement(IntLiteral(2))]
                ),
            ),
            VariableDeclaration(
                "b", "int", False, ObjectAccess([FunctionCall("a", [])])
            ),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.scopes.get_variable_value("b") == 1


def test_return_in_if():
    """a(): int begin if 1 begin return 2; end return 3; end b : int = a();"""
    ast = Program(
        [
            FuncDef(
                "a",
                [],
                "int",
                Program(
                    [
                        IfStatement(
                            IntLiteral(1), Program([ReturnStatement(IntLiteral(2))])
                        ),
                        ReturnStatement(IntLiteral(3)),
                    ]
                ),
            ),
            VariableDeclaration(
                "b", "int", False, ObjectAccess([FunctionCall("a", [])])
            ),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.scopes.get_variable_value("b") == 2


idx_fib_pairs = list(zip(range(1, 7), [1, 2, 3, 5, 8, 13]))


@pytest.mark.parametrize("n,expected", idx_fib_pairs)
def test_rec_fib(n, expected):
    """fib(n : int) : int begin if n < 2 begin return 1; end return fib(n-1) + fib(n-2); end a : int = fib(<n>);"""
    ast = Program(
        [
            FuncDef(
                "fib",
                [Param("n", "int", False)],
                "int",
                Program(
                    [
                        IfStatement(
                            RelationExpr(ObjectAccess(["n"]), IntLiteral(2), "<"),
                            Program([ReturnStatement(IntLiteral(1))]),
                        ),
                        ReturnStatement(
                            AddExpr(
                                [
                                    ObjectAccess(
                                        [
                                            FunctionCall(
                                                "fib",
                                                [
                                                    AddExpr(
                                                        [
                                                            ObjectAccess(["n"]),
                                                            IntLiteral(1),
                                                        ],
                                                        ["-"],
                                                    )
                                                ],
                                            )
                                        ]
                                    ),
                                    ObjectAccess(
                                        [
                                            FunctionCall(
                                                "fib",
                                                [
                                                    AddExpr(
                                                        [
                                                            ObjectAccess(["n"]),
                                                            IntLiteral(2),
                                                        ],
                                                        ["-"],
                                                    )
                                                ],
                                            )
                                        ]
                                    ),
                                ],
                                ["+"],
                            )
                        ),
                    ]
                ),
            ),
            VariableDeclaration(
                "a", "int", False, ObjectAccess([FunctionCall("fib", [IntLiteral(n)])])
            ),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.scopes.get_variable_value("a") == expected


@pytest.mark.parametrize("n,expected", idx_fib_pairs)
def test_iter_fib(n, expected):
    """fib(n : mut int) : int begin a:mut int=0; b: mut int = 1; c : mut int = 1; while n > 0 begin c = a + b; a = b; b = c; n = n - 1; end return b;  end a : int = fib(1);"""
    ast = Program(
        [
            FuncDef(
                "fib",
                [Param("n", "int", True)],
                "int",
                Program(
                    [
                        VariableDeclaration("a", "int", True, IntLiteral(0)),
                        VariableDeclaration("b", "int", True, IntLiteral(1)),
                        VariableDeclaration("c", "int", True, IntLiteral(1)),
                        WhileStatement(
                            RelationExpr(ObjectAccess(["n"]), IntLiteral(0), ">"),
                            Program(
                                [
                                    AssignmentStatement(
                                        ObjectAccess(["c"]),
                                        AddExpr(
                                            [ObjectAccess(["a"]), ObjectAccess(["b"])],
                                            ["+"],
                                        ),
                                    ),
                                    AssignmentStatement(
                                        ObjectAccess(["a"]), ObjectAccess(["b"])
                                    ),
                                    AssignmentStatement(
                                        ObjectAccess(["b"]), ObjectAccess(["c"])
                                    ),
                                    AssignmentStatement(
                                        ObjectAccess(["n"]),
                                        AddExpr(
                                            [ObjectAccess(["n"]), IntLiteral(1)], ["-"]
                                        ),
                                    ),
                                ]
                            ),
                        ),
                        ReturnStatement(ObjectAccess(["b"])),
                    ]
                ),
            ),
            VariableDeclaration(
                "a", "int", False, ObjectAccess([FunctionCall("fib", [IntLiteral(n)])])
            ),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.scopes.get_variable_value("a") == expected


def test_return_inside_if_inside_while():
    """msg_when_done(n : mut int) : str begin while 1 begin if n < 0 begin return 'BOOM'; end n = n - 1; end end a : str = msg_when_done(100);"""
    ast = Program(
        [
            FuncDef(
                "msg_when_done",
                [Param("n", "int", True)],
                "str",
                Program(
                    [
                        WhileStatement(
                            IntLiteral(1),
                            Program(
                                [
                                    IfStatement(
                                        RelationExpr(
                                            ObjectAccess(["n"]), IntLiteral(0), "<"
                                        ),
                                        Program([ReturnStatement(StrLiteral("BOOM"))]),
                                    ),
                                    AssignmentStatement(
                                        ObjectAccess(["n"]),
                                        AddExpr(
                                            [ObjectAccess(["n"]), IntLiteral(1)], ["-"]
                                        ),
                                    ),
                                ]
                            ),
                        )
                    ]
                ),
            ),
            VariableDeclaration(
                "a",
                "str",
                False,
                ObjectAccess([FunctionCall("msg_when_done", [IntLiteral(100)])]),
            ),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.scopes.get_variable_value("a") == "BOOM"
