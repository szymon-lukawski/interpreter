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

    def visit_float_literal(self, float_literal: FloatLiteral):
        self.parts.append(f"FloatLiteral({float_literal.value})")

    def visit_str_literal(self, str_literal: StrLiteral):
        self.parts.append(f"StrLiteral('{str_literal.value}')")

    def visit_null_literal(self, null_literal: NullLiteral):
        self.parts.append(f"NullLiteral()")
    
    def visit_unary(self, unary_expr: UnaryExpr):
        self.parts.append("UnaryExpr(")
        unary_expr.negated.accept(self)
        self.parts.append(")")

    def visit_add(self, add_expr : AddExpr):
        self._visit_additive_or_multiplicative(add_expr, True)

    def visit_multi(self, multi_expr: MultiExpr):
        self._visit_additive_or_multiplicative(multi_expr, False)
        
    def _visit_additive_or_multiplicative(self, expr: MultiExpr | AddExpr,  is_additive: bool):
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

    def visit_and(self, and_expr: AndExpr):
        self._visit_logical(and_expr, True)

    def visit_or(self, or_expr: OrExpr):
        self._visit_logical(or_expr, False)

    def _visit_logical(self, expr: AndExpr | OrExpr, is_and: bool):
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

        
    def visit_obj_access(self, obj_access: ObjectAccess):
        self.parts.append(f"ObjectAccess([{", ".join([f"'{name}'" for name in obj_access.name_chain])}])")


    def visit_var_dec(self, var_dec: VariableDeclaration):
        self.parts.append(f"VariableDeclaration('{var_dec.name}', '{var_dec.type}', {var_dec.is_mutable}")
        if var_dec.default_value:
            self.parts.append(", ")
            var_dec.default_value.accept(self)
        self.parts.append(")")


    def visit_assignment(self, assignment: AssignmentStatement):
        self.parts.append("AssignmentStatement(")
        assignment.obj_access.accept(self)
        self.parts.append(", ")
        assignment.expr.accept(self)
        self.parts.append(")")
    
    
    def visit_if(self, if_stmt: IfStatement):
        self.parts.append("IfStatement(")
        if_stmt.cond.accept(self)
        self.parts.append(", ")
        if_stmt.prog.accept(self)
        if if_stmt.else_prog:
            self.parts.append(", ")
            if_stmt.else_prog.accept(self)
        self.parts.append(")")

    def visit_while(self, while_stmt: WhileStatement):
        self.parts.append("WhileStatement(")
        while_stmt.cond.accept(self)
        self.parts.append(", ")
        while_stmt.prog.accept(self)
        self.parts.append(")")

    def visit_program(self, program: Program):
        self._visit_titled_list("Program", program.children)

    def _visit_titled_list(self, title : str, list_: List[Statement]):
        self.parts.append(f"{title}(")
        self._visit_list(list_)
        self.parts.append(")")

    def _visit_list(self, list_: List[Statement]):
        self.parts.append("[")
        for i, element in enumerate(list_, start=1):
            element.accept(self)
            if i != len(list_):
                self.parts.append(", ")
        self.parts.append("]")


    def visit_variant_def(self, variant_def : VariantDef):
        self.parts.append(f"VariantDef('{variant_def.name}', ")
        self._visit_list(variant_def.named_types)
        self.parts.append(")")

        
    def visit_named_type(self, named_type : NamedType):
        self.parts.append(f"NamedType('{named_type.name}', '{named_type.type}')")
    


    def visit_case_section(self, case_section : CaseSection):
        self.parts.append(f"CaseSection('{case_section.type}', ")
        case_section.program.accept(self)
        self.parts.append(")")
    
    def visit_visit(self, visit_statement: VisitStatement):
        self.parts.append("VisitStatement(")
        visit_statement.obj.accept(self)
        self.parts.append(", ")
        self._visit_list(visit_statement.case_sections)
        self.parts.append(")")
    
    def visit_func_call(self, func_call):
        return super().visit_func_call(func_call)
    
    def visit_func_def(self, func_def):
        return super().visit_func_def(func_def)

    
    def visit_return(self, return_stmt):
        return super().visit_return(return_stmt)
    
    
    def visit_struct_def(self, struct_def: StructDef):
        self.parts.append(f"StructDef('{struct_def.name}', ")
        self._visit_list(struct_def.attributes)
        self.parts.append(")")
    
    

    
        
