"""Module defining classes for Abstract syntax tree used in parser"""

from typing import List


# TODO add argument and data validation in each constructor
class ASTNode:
    def accept(self, visitor):
        return visitor.visit(self)


class Statement(ASTNode):
    pass


def _eq_for_ast_with_children(my_object: object, other: object):
    if type(my_object) != type(other) or len(other.children) != len(my_object.children):
        return False
    for i, my_child in enumerate(my_object.children):
        other_child = other.children[i]
        if not other_child == my_child:
            return False
    return True


class Program(ASTNode):
    def __init__(self, children: List[Statement]) -> None:
        self.children = children

    def accept(self, visitor):
        return visitor.visit_program(self)

    def __eq__(self, other: object) -> bool:
        return _eq_for_ast_with_children(self, other)


class Expr(ASTNode):
    pass


class OrExpr(Expr):
    def __init__(self, children: List[Expr]) -> None:
        self.children = children

    def accept(self, visitor):
        return visitor.visit_or(self)

    def __eq__(self, other: object) -> bool:
        return _eq_for_ast_with_children(self, other)


class AndExpr(Expr):
    def __init__(self, children: List[Expr]) -> None:
        self.children = children

    def accept(self, visitor):
        return visitor.visit_and(self)

    def __eq__(self, other: object) -> bool:
        return _eq_for_ast_with_children(self, other)


class RelationExpr(Expr):
    def __init__(self, left: Expr, right: Expr, operator: str) -> None:
        self.left = left
        self.right = right
        self.operator = operator

    def accept(self, visitor):
        return visitor.visit_rel(self)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, RelationExpr)
            and self.operator == other.operator
            and self.left == other.left
            and self.right == other.right
        )


def _eq_for_ast_with_children_and_operations(
    my_object, other: object
):
    return (
        type(my_object) == type(other)
        and my_object.operations == other.operations
        and len(my_object.children) == len(other.children)
        and all([(my_child == other.children[i]) for i, my_child in enumerate(my_object.children)])
    )


class AddExpr(Expr):
    def __init__(self, children: List[Expr], operations: List[str]) -> None:
        self.children = children
        self.operations = operations

    def accept(self, visitor):
        return visitor.visit_add(self)

    def __eq__(self, other: object) -> bool:
        return _eq_for_ast_with_children_and_operations(self, other)


class MultiExpr(Expr):
    def __init__(self, children: List[Expr], operations: List[str]) -> None:
        self.children = children
        self.operations = operations

    def accept(self, visitor):
        return visitor.visit_multi(self)

    def __eq__(self, other: object) -> bool:
        return _eq_for_ast_with_children_and_operations(self, other)


class UnaryExpr(Expr):
    def __init__(self, negated: Expr) -> None:
        self.negated = negated

    def accept(self, visitor):
        return visitor.visit_unary(self)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, UnaryExpr) and self.negated == other.negated


class Term(Expr):
    pass


class Literal(Term):
    def __init__(self, value: int | float | str | None) -> None:
        self.value = value

    def __eq__(self, other: object) -> bool:
        return type(self) == type(other) and self.value == other.value


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

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, IfStatement)
            and self.cond == other.cond
            and self.prog == other.prog
            and self.else_prog == other.else_prog
        )


class WhileStatement(CondStatement):
    def __init__(self, cond: Expr, prog: Program) -> None:
        self.cond = cond
        self.prog = prog

    def accept(self, visitor):
        return visitor.visit_while(self)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, WhileStatement)
            and self.cond == other.cond
            and self.prog == other.prog
        )


######################


class ObjectAccess(ASTNode):
    def __init__(self, name_chain: List[str]) -> None:
        self.name_chain = name_chain

    def accept(self, visitor):
        return visitor.visit_obj_access(self)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ObjectAccess) and self.name_chain == other.name_chain


class CaseSection(ASTNode):
    def __init__(self, type_: str, program: Program) -> None:
        self.type = type_
        self.program = program

    def accept(self, visitor):
        return visitor.visit_case_section(self)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, CaseSection)
            and self.type == other.type
            and self.program == other.program
        )


class VisitStatement(Statement):
    def __init__(self, obj: ObjectAccess, css: List[CaseSection]) -> None:
        self.obj = obj
        self.case_sections = css

    def accept(self, visitor):
        return visitor.visit_visit(self)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, VisitStatement)
            and self.obj == other.obj
            and all(
                [
                    (my_case_section == other.case_sections[i])
                    for i, my_case_section in enumerate(self.case_sections)
                ]
            )
        )


class AssignmentStatement(Statement):
    def __init__(self, obj_access: ObjectAccess, expr: Expr) -> None:
        self.obj_access = obj_access
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_assignment(self)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, AssignmentStatement)
            and self.obj_access == other.obj_access
            and self.expr == other.expr
        )


class VariableDeclaration(ASTNode):
    def __init__(
        self, name: str, var_type: str, is_mutable: bool, default_value: Expr = None
    ) -> None:
        self.name = name
        self.type = var_type
        self.is_mutable = is_mutable
        self.default_value = default_value

    def accept(self, visitor):
        return visitor.visit_var_dec(self)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, VariableDeclaration)
            and self.name == other.name
            and self.type == other.type
            and self.is_mutable == other.is_mutable
            and self.default_value == other.default_value
        )


class StructDef(ASTNode):
    def __init__(self, name: str, attributes: List[VariableDeclaration]) -> None:
        self.name = name
        self.attributes = attributes

    def accept(self, visitor):
        return visitor.visit_struct_def(self)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, StructDef)
            and self.name == other.name
            and all(
                [(my_attr == other.attributes[i]) for i, my_attr in enumerate(self.attributes)]
            )
        )


class NamedType(ASTNode):
    def __init__(self, name: str, type_: str) -> None:
        self.name = name
        self.type = type_

    def accept(self, visitor):
        return visitor.visit_named_type(self)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, NamedType)
            and self.name == other.name
            and self.type == other.type
        )


class VariantDef(ASTNode):
    def __init__(self, name: str, named_types: List[NamedType]) -> None:
        self.name = name
        self.named_types = named_types

    def accept(self, visitor):
        return visitor.visit_variant_def(self)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, VariantDef)
            and self.name == other.name
            and all(
                [
                    (my_named_type == other.named_types[i])
                    for i, my_named_type in enumerate(self.named_types)
                ]
            )
        )


class ReturnStatement(Statement):
    def __init__(self, expr: Expr) -> None:
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_return(self)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ReturnStatement) and self.expr == other.expr


class Param(ASTNode):
    def __init__(
        self, name: str, var_type: str, is_mutable: bool, default_value: Expr = None
    ) -> None:
        self.name = name
        self.type = var_type
        self.is_mutable = is_mutable
        self.default_value = default_value

    def accept(self, visitor):
        return visitor.visit_param(self)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Param)
            and self.name == other.name
            and self.type == other.type
            and self.is_mutable == other.is_mutable
            and self.default_value == other.default_value
        )


class FuncDef(ASTNode):
    def __init__(
        self, name: str, params: List[Param], type_: str, prog: Program
    ) -> None:
        self.name = name
        self.params = params
        self.type = type_
        self.prog = prog

    def accept(self, visitor):
        return visitor.visit_func_def(self)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, FuncDef)
            and self.name == other.name
            and all([(my_param == other.params[i]) for i, my_param in enumerate(self.params)])
            and self.type == other.type
            and self.prog == other.prog
        )


class FunctionCall(ASTNode):
    def __init__(self, name: str, args: List[Expr]) -> None:
        self.name = name
        self.args = args

    def accept(self, visitor):
        return visitor.visit_func_call(self)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, FunctionCall)
            and self.name == other.name
            and all([(my_arg == other.args[i]) for i, my_arg in enumerate(self.args)])
        )
