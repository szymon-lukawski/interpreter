"""Module for printing AST using visitor base class"""

from visitor import Visitor
from AST import *


class Printer(Visitor):
    def __init__(self) -> None:
        self.parts = []

    def print(self, ast : ASTNode):
        self.parts = []
        ast.accept(self)
        return ''.join(self.parts)
    
    def visit_int_literal(self, int_literal: IntLiteral):
        self.parts.append(f"IntLiteral({int_literal.value})")

    def visit_float_literal(self, float_literal):
        self.parts.append(f"FloatLiteral({float_literal.value})")

    def visit_str_literal(self, str_literal):
        self.parts.append(f"StrLiteral('{str_literal.value}')")

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
                self.parts.append(", ")
        self.parts.append("], [")
        for i, operation in enumerate(expr.operations, start=1):
            self.parts.append(f"'{operation}'")
            if i != len(expr.operations):
                self.parts.append(", ")
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
                self.parts.append(", ")
        self.parts.append("])")

    def visit_rel(self, rel_expr: RelationExpr):
        self.parts.append("RelationExpr(")
        rel_expr.left.accept(self)
        self.parts.append(", ")
        rel_expr.right.accept(self)
        self.parts.append(f", '{rel_expr.operator}')")

        
    def visit_obj_access(self, obj_access):
        self.parts.append(f"ObjectAccess([{", ".join([f"'{name}'" for name in obj_access.name_chain])}])")

    def visit_assignment(self, assignment):
        self.parts.append("AssignmentStatement(")
        assignment.obj_access.accept(self)
        self.parts.append(", ")
        assignment.expr.accept(self)
        self.parts.append(")")
    
    def visit_case_section(self, case_section):
        return super().visit_case_section(case_section)
    
    def visit_fork(self, fork):
        return super().visit_fork(fork)
    
    def visit_func_call(self, func_call):
        return super().visit_func_call(func_call)
    
    def visit_func_def(self, func_def):
        return super().visit_func_def(func_def)
    
    def visit_identifier(self, identifier):
        return super().visit_identifier(identifier)
    
    def visit_if(self, if_stmt):
        return super().visit_if(if_stmt)
    
    def visit_named_type(self, named_type):
        return super().visit_named_type(named_type)

    
    def visit_program(self, program):
        return super().visit_program(program)
    

    
    def visit_return(self, return_stmt):
        return super().visit_return(return_stmt)
    
    def visit_struct_def(self, struct_def):
        return super().visit_struct_def(struct_def)
    
    def visit_type(self, type_node):
        return super().visit_type(type_node)
    
    def visit_var_dec(self, var_dec):
        return super().visit_var_dec(var_dec)
    
    def visit_variant_def(self, variant_def):
        return super().visit_variant_def(variant_def)
    
        