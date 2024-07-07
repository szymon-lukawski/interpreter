"""."""

from abc import ABC, abstractmethod


# pylint: disable=C0116:missing-function-docstring
class Visitor(ABC):
    """Base Visitor class for traversing AST"""

    @abstractmethod
    def visit_program(self, program):
        pass

    @abstractmethod
    def visit_assignment(self, assignment):
        pass

    @abstractmethod
    def visit_if(self, if_stmt):
        pass

    @abstractmethod
    def visit_return(self, return_stmt):
        pass

    @abstractmethod
    def visit_type(self, type_node):
        pass

    @abstractmethod
    def visit_case_section(self, case_section):
        pass

    @abstractmethod
    def visit_func_call(self, func_call):
        pass

    @abstractmethod
    def visit_identifier(self, identifier):
        pass

    @abstractmethod
    def visit_obj_access(self, obj_access):
        pass

    @abstractmethod
    def visit_fork(self, fork):
        pass

    @abstractmethod
    def visit_var_dec(self, var_dec):
        pass

    @abstractmethod
    def visit_struct_def(self, struct_def):
        pass

    @abstractmethod
    def visit_variant_def(self, variant_def):
        pass

    @abstractmethod
    def visit_named_type(self, named_type):
        pass

    @abstractmethod
    def visit_func_def(self, func_def):
        pass

    @abstractmethod
    def visit_or(self, or_expr):
        pass

    @abstractmethod
    def visit_and(self, and_expr):
        pass

    @abstractmethod
    def visit_rel(self, rel_expr):
        pass

    @abstractmethod
    def visit_add(self, add_expr):
        pass

    @abstractmethod
    def visit_multi(self, multi_expr):
        pass

    @abstractmethod
    def visit_unary(self, unary_expr):
        pass

    @abstractmethod
    def visit_null_literal(self, null_literal):
        pass

    @abstractmethod
    def visit_int_literal(self, int_literal):
        pass

    @abstractmethod
    def visit_float_literal(self, float_literal):
        pass

    @abstractmethod
    def visit_str_literal(self, str_literal):
        pass
