"""Module for printing AST using visitor base class"""

from visitor import Visitor
from AST import *


class Printer(Visitor):
    def __init__(self) -> None:
        self.parts = []

    def print(self, ast : ASTNode):
        ast.accept(self)
        return ''.join(self.parts)
    
    def visit_int_literal(self, int_literal: IntLiteral):
        self.parts.append(f"IntLiteral({int_literal.value})")

    def visit_float_literal(self, float_literal):
        self.parts.append(f"FloatLiteral({float_literal.value})")

    def visit_str_literal(self, str_literal):
        self.parts.append(f"FloatLiteral({str_literal.value})")

    def visit_null_literal(self, null_literal):
        self.parts.append(f"NullLiteral()")
    
    def visit_unary(self, unary_expr: UnaryExpr):
        self.parts.append("UnaryExpr(")
        unary_expr.negated.accept(self)
        self.parts.append(")")

    def visit_add(self, add_expr : AddExpr):
        self._visit_additive_or_multiplicative(add_expr, True)

    def visit_multi(self, multi_expr):
        self._visit_additive_or_multiplicative(multi_expr, False)
        
    def _visit_additive_or_multiplicative(self, expr,  is_additive):
        if is_additive:
            self.parts.append("AddExpr([")
        else:
            self.parts.append("MultiExpr([")
        for i, child in enumerate(expr.children, start=1):
            child.accept(self)
            if i != len(expr.children):
                self.parts.append(",")
        self.parts.append("], [")
        for i, operation in enumerate(expr.operations, start=1):
            self.parts.append(f"'{operation}'")
            if i != len(expr.children):
                self.parts.append(",")
        self.parts.append("])")

    def visit_and(self, and_expr):
        self._visit_logical(and_expr, True)

    def visit_or(self, or_expr):
        self._visit_logical(or_expr, False)

    def _visit_logical(self, expr, is_and):
        if is_and:
            self.parts.append("AndExpr([")
        else:
            self.parts.append("OrExpr([")
        for i, child in enumerate(expr.children, start=1):
            child.accept(self)
            if i != len(expr.children):
                self.parts.append(",")
        self.parts.append("])")
        