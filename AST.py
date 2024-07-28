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
    def __init__(self, children: List[Expr]) -> None:
        self.children = children

    def accept(self, visitor):
        return visitor.visit_or(self)


class AndExpr(Expr):
    def __init__(self, children: List[Expr]) -> None:
        self.children = children

    def accept(self, visitor):
        return visitor.visit_and(self)


class RelationExpr(Expr):
    def __init__(self, left: Expr, right: Expr, operator: str) -> None:
        self.left = left
        self.right = right
        self.operator = operator

    def accept(self, visitor):
        return visitor.visit_rel(self)


class AddExpr(Expr):
    def __init__(self, children: List[Expr], operations: List[str]) -> None:
        self.children = children
        self.operations = operations

    def accept(self, visitor):
        return visitor.visit_add(self)


class MultiExpr(Expr):
    def __init__(self, children: List[Expr], operations: List[str]) -> None:
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
    def __init__(self, value: int | float | str | None) -> None:
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

    def accept(self, visitor):
        return visitor.visit_while(self)

######################

class ObjectAccess(ASTNode):
    def __init__(self, name_chain: List[str]) -> None:
        self.name_chain = name_chain

    def accept(self, visitor):
        return visitor.visit_obj_access(self)


class CaseSection(ASTNode):
    def __init__(self, type_: str, program: Program) -> None:
        self.type = type_
        self.program = program

    def accept(self, visitor):
        return visitor.visit_case_section(self)

class VisitStatement(Statement):
    def __init__(self, obj : ObjectAccess, css: List[CaseSection]) -> None:
        self.obj = obj
        self.case_sections = css

    def accept(self, visitor):
        return visitor.visit_visit(self)





class AssignmentStatement(Statement):
    def __init__(self, obj_access, expr) -> None:
        self.obj_access = obj_access
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_assignment(self)


class VariableDeclaration(ASTNode):
    def __init__(self, name : str, var_type : str, is_mutable : bool, default_value : Expr = None) -> None:
        self.name = name
        self.type = var_type
        self.is_mutable = is_mutable
        self.default_value = default_value

    def accept(self, visitor):
        return visitor.visit_var_dec(self)


class StructDef(ASTNode):
    def __init__(self, name: str, attributes : List[VariableDeclaration]) -> None:
        self.name = name
        self.attributes = attributes

    def accept(self, visitor):
        return visitor.visit_struct_def(self)


class NamedType(ASTNode):
    def __init__(self, name: str, type_: str) -> None:
        self.name = name
        self.type = type_

    def accept(self, visitor):
        return visitor.visit_named_type(self)


class VariantDef(ASTNode):
    def __init__(self, name: str, named_types: List[NamedType]) -> None:
        self.name = name
        self.named_types = named_types

    def accept(self, visitor):
        return visitor.visit_variant_def(self)


class ReturnStatement(Statement):
    def __init__(self, expr: Expr) -> None:
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_return(self)

class Param(ASTNode):
    def __init__(self, name : str, var_type : str, is_mutable : bool, default_value : Expr = None) -> None:
        self.name = name
        self.type = var_type
        self.is_mutable = is_mutable
        self.default_value = default_value

    def accept(self, visitor):
        return visitor.visit_param(self)

class FuncDef(ASTNode):
    def __init__(self, name : str, params : List[Param], type_ : str, prog : Program) -> None:
        self.name = name
        self.params = params
        self.type = type_
        self.prog = prog

    def accept(self, visitor):
        return visitor.visit_func_def(self)


class FunctionCall(ASTNode):
    def __init__(self, name: str, args: List[Expr]) -> None:
        self.name = name
        self.args = args

    def accept(self, visitor):
        return visitor.visit_func_call(self)
