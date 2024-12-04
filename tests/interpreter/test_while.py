import pytest
from token_type import TokenType
from interpreter import Interpreter
from AST import *
from multiprocessing import Process


def test_sanity():
    """."""
    assert 1 == True


def target_for_endless_test():
    ast = Program([WhileStatement(IntLiteral(1), Program([]))])
    i = Interpreter()
    ast.accept(i)

def test_endless_loop():
    """while 1 begin end"""
    process = Process(target=target_for_endless_test)
    process.start()
    process.join(timeout=3)
    if process.is_alive():
        process.terminate()
        process.join()  # Ensure it exits cleanly
        assert True  # Test passes
    else:
        assert False

def test_while_but_efectively_empty_if():
    """a: mut int = 1; while a begin a = a-1; end"""
    ast = Program([VariableDeclaration('a', 'int', True, IntLiteral(1)), WhileStatement(ObjectAccess(['a']), Program([AssignmentStatement(ObjectAccess(['a']), AddExpr([ObjectAccess(['a']), IntLiteral(1)], ['-']))]))])
    i = Interpreter()
    ast.accept(i)
    # This should run just once


def test_can_not_refer_to_variable_after_poped_scope():
    """a: mut int = 1; while a begin a = a-1; b : mut int = 4; end b = 1;"""
    ast = Program([VariableDeclaration('a', 'int', True, IntLiteral(1)), WhileStatement(ObjectAccess(['a']), Program([AssignmentStatement(ObjectAccess(['a']), AddExpr([ObjectAccess(['a']), IntLiteral(1)], ['-'])), VariableDeclaration('b', 'int', True, IntLiteral(4))])), AssignmentStatement(ObjectAccess(['b']), IntLiteral(1))])
    i = Interpreter()
    with pytest.raises(RuntimeError) as e:
        ast.accept(i)
    assert str(e.value) == "Variable 'b' not found in any scope"



