"""."""

from abc import ABC, abstractmethod

from parser.AST import *


# pylint: disable=C0116:missing-function-docstring
class Visitor(ABC):
    """Base Visitor class for traversing AST"""

    @abstractmethod
    def visit_program(self, program: Program):
        pass

    @abstractmethod
    def visit_assignment(self, assignment: AssignmentStatement):
        pass

    @abstractmethod
    def visit_if(self, if_stmt: IfStatement):
        pass

    @abstractmethod
    def visit_while(self, while_stmt: WhileStatement):
        pass

    @abstractmethod
    def visit_return(self, return_stmt: ReturnStatement):
        pass


    @abstractmethod
    def visit_case_section(self, case_section: CaseSection):
        pass

    @abstractmethod
    def visit_func_call(self, func_call: FunctionCall):
        pass

    @abstractmethod
    def visit_obj_access(self, obj_access: ObjectAccess):
        pass


    @abstractmethod
    def visit_var_dec(self, var_dec: VariableDeclaration):
        pass


    @abstractmethod
    def visit_struct_def(self, struct_def: StructDef):
        pass

    @abstractmethod
    def visit_variant_def(self, variant_def: VariableDeclaration):
        pass

    @abstractmethod
    def visit_named_type(self, named_type: NamedType):
        pass

    @abstractmethod
    def visit_visit(self, visit_statement: VisitStatement):
        pass

    @abstractmethod
    def visit_param(self, param : Param):
        pass

    @abstractmethod
    def visit_func_def(self, func_def: FuncDef):
        pass

    @abstractmethod
    def visit_or(self, or_expr: OrExpr):
        pass

    @abstractmethod
    def visit_and(self, and_expr: AndExpr):
        pass

    @abstractmethod
    def visit_rel(self, rel_expr: RelationExpr):
        pass

    @abstractmethod
    def visit_add(self, add_expr: AddExpr):
        pass

    @abstractmethod
    def visit_multi(self, multi_expr: MultiExpr):
        pass

    @abstractmethod
    def visit_unary(self, unary_expr: UnaryExpr):
        pass

    @abstractmethod
    def visit_null_literal(self, null_literal: NullLiteral):
        pass

    @abstractmethod
    def visit_int_literal(self, int_literal: IntLiteral):
        pass

    @abstractmethod
    def visit_float_literal(self, float_literal: FloatLiteral):
        pass

    @abstractmethod
    def visit_str_literal(self, str_literal: StrLiteral):
        pass
