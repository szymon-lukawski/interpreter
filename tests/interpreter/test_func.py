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
    assert i.scopes.get_symbol("a").value == 1


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
    assert i.scopes.get_symbol("a").value == 3


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
    assert i.scopes.get_symbol("b").value == 3


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
    assert i.scopes.get_symbol("c").value == 3


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
    assert i.scopes.get_symbol("d").value == 6


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
    assert i.scopes.get_symbol("b").value == 1


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
    assert i.scopes.get_symbol("b").value == 2


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
    assert i.scopes.get_symbol("a").value == expected


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
    assert i.scopes.get_symbol("a").value == expected


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
    assert i.scopes.get_symbol("a").value == "BOOM"


def test_calling_scope_not_the_same_as_scope_of_called():
    """a : int = 1; one(): int begin return a + zero; end b : int = one(); zero : int = 0;"""
    ast = Program(
        [
            VariableDeclaration("a", "int", False, IntLiteral(1)),
            FuncDef(
                "one",
                [],
                "int",
                Program(
                    [
                        ReturnStatement(
                            AddExpr(
                                [ObjectAccess(["a"]), ObjectAccess(["zero"])], ["+"]
                            )
                        )
                    ]
                ),
            ),
            VariableDeclaration(
                "b", "int", False, ObjectAccess([FunctionCall("one", [])])
            ),
            VariableDeclaration("zero", "int", False, IntLiteral(0)),
        ]
    )
    i = Interpreter()
    with pytest.raises(RuntimeError) as e:
        ast.accept(i)
    assert str(e.value) == "Variable 'zero' not found in any scope"


def test_variable_and_func_at_the_same_scope_but_variable_interpreted_before_function_call():
    """a : int = 1; one(): int begin return a + zero;  end zero : int = 0; b : int = one();"""
    ast = Program(
        [
            VariableDeclaration("a", "int", False, IntLiteral(1)),
            FuncDef(
                "one",
                [],
                "int",
                Program(
                    [
                        ReturnStatement(
                            AddExpr(
                                [ObjectAccess(["a"]), ObjectAccess(["zero"])], ["+"]
                            )
                        )
                    ]
                ),
            ),
            VariableDeclaration("zero", "int", False, IntLiteral(0)),
            VariableDeclaration(
                "b", "int", False, ObjectAccess([FunctionCall("one", [])])
            ),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.scopes.get_symbol("b").value == 1


def test_function_scope_is_different_than_calling_scope():
    """a : int = 1; func(): int begin return a; end b : int; if 1 begin a : int = 5; b = func(); end"""
    ast = Program(
        [
            VariableDeclaration("a", "int", False, IntLiteral(1)),
            FuncDef("func", [], "int", Program([ReturnStatement(ObjectAccess(["a"]))])),
            VariableDeclaration("b", "int", False),
            IfStatement(
                IntLiteral(1),
                Program(
                    [
                        VariableDeclaration("a", "int", False, IntLiteral(5)),
                        AssignmentStatement(
                            ObjectAccess(["b"]),
                            ObjectAccess([FunctionCall("func", [])]),
                        ),
                    ]
                ),
            ),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.scopes.get_symbol("b").value == 1


def test_complex_function_scope():
    """add(arg1: int, arg2: int) : int
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
    a = add(5,15);
    """
    ast = Program(
        [
            FuncDef(
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
                                            [
                                                ObjectAccess(["arg1"]),
                                                ObjectAccess(["arg2"]),
                                            ],
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
                                        ObjectAccess(
                                            [
                                                FunctionCall(
                                                    "add_sub_function",
                                                    [
                                                        ObjectAccess(["arg1"]),
                                                        ObjectAccess(["arg2"]),
                                                    ],
                                                )
                                            ]
                                        )
                                    )
                                ]
                            ),
                        ),
                        ReturnStatement(
                            ObjectAccess(
                                [
                                    FunctionCall(
                                        "add",
                                        [
                                            ObjectAccess(["arg1"]),
                                            ObjectAccess(["arg2"]),
                                        ],
                                    )
                                ]
                            )
                        ),
                    ]
                ),
            ),
            VariableDeclaration(
                "a",
                "int",
                False,
                ObjectAccess([FunctionCall("add", [IntLiteral(5), IntLiteral(15)])]),
            ),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.scopes.get_symbol("a").value == 20


def test_functional_call_without_assignment():
    """x : mut int = 12; a(): null_type begin x = 7; end a();"""
    ast = Program(
        [
            VariableDeclaration("x", "int", True, IntLiteral(12)),
            FuncDef(
                "a",
                [],
                "null_type",
                Program([AssignmentStatement(ObjectAccess(["x"]), IntLiteral(7))]),
            ),
            FunctionCall("a", []),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.scopes.get_symbol("x").value == 7


def test_max_recursion_depth():
    """a() : null_type begin a(); end a();"""
    ast = Program(
        [
            FuncDef("a", [], "null_type", Program([FunctionCall("a", [])])),
            FunctionCall("a", []),
        ]
    )
    i = Interpreter()
    with pytest.raises(RuntimeError) as e:
        ast.accept(i)
    assert str(e.value) == "Maximal recursion depth reached!"


def test_args_evaled_from_left_to_right():
    """c : mut int = 0; increment_and_return(): int begin c = c + 1; return c; end Three_Ints : struct begin x: int; y: int; z:int; end Three_Ints(x: int, y: int, z: int): Three_Ints begin rv : mut Three_Ints; rv.x = x; rv.y = y; rv.z = z; return rv; end result : Three_Ints = Three_Ints( increment_and_return(), increment_and_return(), increment_and_return());"""
    ast = Program(
        [
            VariableDeclaration("c", "int", True, IntLiteral(0)),
            FuncDef(
                "increment_and_return",
                [],
                "int",
                Program(
                    [
                        AssignmentStatement(
                            ObjectAccess(["c"]),
                            AddExpr([ObjectAccess(["c"]), IntLiteral(1)], ["+"]),
                        ),
                        ReturnStatement(ObjectAccess(["c"])),
                    ]
                ),
            ),
            StructDef(
                "Three_Ints",
                [
                    VariableDeclaration("x", "int", False),
                    VariableDeclaration("y", "int", False),
                    VariableDeclaration("z", "int", False),
                ],
            ),
            FuncDef(
                "Three_Ints",
                [
                    Param("x", "int", False),
                    Param("y", "int", False),
                    Param("z", "int", False),
                ],
                "Three_Ints",
                Program(
                    [
                        VariableDeclaration("rv", "Three_Ints", True),
                        AssignmentStatement(
                            ObjectAccess(["rv", "x"]), ObjectAccess(["x"])
                        ),
                        AssignmentStatement(
                            ObjectAccess(["rv", "y"]), ObjectAccess(["y"])
                        ),
                        AssignmentStatement(
                            ObjectAccess(["rv", "z"]), ObjectAccess(["z"])
                        ),
                        ReturnStatement(ObjectAccess(["rv"])),
                    ]
                ),
            ),
            VariableDeclaration(
                "result",
                "Three_Ints",
                True, # TODO  False should be able to work but does not
                ObjectAccess(
                    [
                        FunctionCall(
                            "Three_Ints",
                            [
                                ObjectAccess(
                                    [FunctionCall("increment_and_return", [])]
                                ),
                                ObjectAccess(
                                    [FunctionCall("increment_and_return", [])]
                                ),
                                ObjectAccess(
                                    [FunctionCall("increment_and_return", [])]
                                ),
                            ],
                        )
                    ]
                ),
            ),
        ]
    )
    i = Interpreter()
    ast.accept(i)
    assert i.visit_obj_access(ObjectAccess(["result", "x"])) == 1
    assert i.visit_obj_access(ObjectAccess(["result", "y"])) == 2
    assert i.visit_obj_access(ObjectAccess(["result", "z"])) == 3
