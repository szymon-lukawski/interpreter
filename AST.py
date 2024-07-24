"""Module defining classes for Abstract syntax tree used in parser"""

from typing import List


class ASTNode:
    def accept(self, visitor):
        return visitor.visit(self)


class Statement(ASTNode):
    pass


class Program(ASTNode):
    def __init__(self, children: List[Statement]) -> None:
        self.children = children

    def accept(self, visitor):
        return visitor.visit_program(self)


class Expr(ASTNode):
    pass


class OrExpr(Expr):
    def __init__(self, children : List[Expr]) -> None:
        self.children = children

    def accept(self, visitor):
        return visitor.visit_or(self)


class AndExpr(Expr):
    def __init__(self, children : List[Expr]) -> None:
        self.children = children

    def accept(self, visitor):
        return visitor.visit_and(self)


class RelationExpr(Expr):
    def __init__(self, left : Expr, right: Expr, operator: str) -> None:
        self.left = left
        self.right = right
        self.operator = operator

    def accept(self, visitor):
        return visitor.visit_rel(self)


class AddExpr(Expr):
    def __init__(self, children: Expr, operations: List[str]) -> None:
        self.children = children
        self.operations = operations

    def accept(self, visitor):
        return visitor.visit_add(self)


class MultiExpr(Expr):
    def __init__(self, children : List[Expr], operations: List[str]) -> None:
        self.children = children
        self.operations = operations

    def accept(self, visitor):
        return visitor.visit_multi(self)


class UnaryExpr(Expr):
    def __init__(self, negated: Expr) -> None:
        self.negated = negated

    def accept(self, visitor):
        return visitor.visit_unary(self)


class Term(Expr):
    pass


class Literal(Term):
    def __init__(self, value : int | float | str | None) -> None:
        self.value = value


class NullLiteral(Literal):
    def __init__(self, value=None) -> None:
        super().__init__(value)

    def accept(self, visitor):
        return visitor.visit_null_literal(self)


class IntLiteral(Literal):
    def accept(self, visitor):
        return visitor.visit_int_literal(self)


class FloatLiteral(Literal):
    def accept(self, visitor):
        return visitor.visit_float_literal(self)


class StrLiteral(Literal):
    def accept(self, visitor):
        return visitor.visit_str_literal(self)


class Comment(Statement):
    pass


class ReturnStatement(Statement):
    def __init__(self, expr: Expr) -> None:
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_return(self)


class CondStatement(Statement):
    pass


class IfStatement(CondStatement):
    def __init__(self, cond: Expr, prog: Program, else_prog: Program = None) -> None:
        self.cond = cond
        self.prog = prog
        self.else_prog = else_prog

    def accept(self, visitor):
        return visitor.visit_if(self)


class WhileStatement(CondStatement):
    def __init__(self, cond: Expr, prog: Program) -> None:
        self.cond = cond
        self.prog = prog


######################

class Type(ASTNode):
    def __init__(self, name) -> None:
        self.name = name

    def accept(self, visitor):
        return visitor.visit_type(self)


class CaseSection(ASTNode):
    def __init__(self, type: str, program: Program) -> None:
        self.type = type
        self.program = program

    def accept(self, visitor):
        return visitor.visit_case_section(self)


class FunctionCall(ASTNode):
    def __init__(self, name: str, args: List[Expr]) -> None:
        self.name = name
        self.args = args

    def accept(self, visitor):
        return visitor.visit_func_call(self)


class ObjectAccess(ASTNode):
    def __init__(self, name_chain: List) -> None:
        self.name_chain = name_chain

    def accept(self, visitor):
        return visitor.visit_obj_access(self)


class AssignmentStatement(Statement):
    def __init__(self, obj_access, expr) -> None:
        self.obj_access = obj_access
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_assignment(self)


class Fork(ASTNode):
    def __init__(self, statements) -> None:
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_fork(self)


class VariableDeclaration(ASTNode):
    def __init__(self, name, var_type, is_mutable) -> None:
        self.name = name
        self.type = var_type
        self.is_mutable = is_mutable

    def accept(self, visitor):
        return visitor.visit_var_dec(self)


class VisitStatement(Statement):
    def __init__(self, obj, css) -> None:
        self.obj = obj
        self.case_sections = css


class StructDef(ASTNode):
    def __init__(self, name, attributes) -> None:
        self.name = name
        self.attributes = attributes

    def accept(self, visitor):
        return visitor.visit_struct_def(self)


class VariantDef(ASTNode):
    pass

    def accept(self, visitor):
        return visitor.visit_variant_def(self)


class NamedType(ASTNode):
    def __init__(self, name, type) -> None:
        self.name = name
        self.type = type

    def accept(self, visitor):
        return visitor.visit_named_type(self)


class FuncDef(ASTNode):
    pass

    def accept(self, visitor):
        return visitor.visit_func_def(self)


class MutParam(ASTNode):
    pass


class NonMutParam(ASTNode):
    pass
