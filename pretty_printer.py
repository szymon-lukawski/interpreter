"""Module that provides class to turn AST into formatted human readable code"""

from typing import Callable
from visitor import Visitor
from AST import * 


class PrettyPrinter(Visitor):
    def __init__(self) -> None:
        self.parts = []
        self.indentation_multiplier = 4
        self.space_multiplier = 1
        self.curr_alligment = 0
        self.curr_indentation = 0
        self.precedence = {
            'OrExpr' : 1,
            'AndExpr' : 2,
            'RelationExpr' : 3,
            'AddExpr': 4,
            'MultiExpr': 5,
            'UnaryExpr' : 6,
            'ObjectAccess' : 7,
            'IntLiteral' : 7,
            'FloatLiteral' : 7,
            'StrLiteral' : 7,
            'NullLiteral' : 7,
        }

    def _needs_brackets(self, child : Expr, parent : Expr) -> bool:
        parent_prec = self.precedence[type(parent).__name__]
        child_prec = self.precedence[type(child).__name__]
        return child_prec < parent_prec


    def print(self, ast : ASTNode) -> str:
        """Returns a formatted code representation of AST"""
        self.parts = []
        ast.accept(self)
        return ''.join(self.parts)
    
    def visit_int_literal(self, int_literal: IntLiteral):
        self._add(str(int_literal.value))

    def visit_float_literal(self, float_literal: FloatLiteral):
        self._add(str(float_literal.value))

    def visit_str_literal(self, str_literal: StrLiteral):
        self._add(f"'{str_literal.value}'")

    def visit_null_literal(self, null_literal: NullLiteral):
        self._add('null')
    
    def visit_unary(self, unary_expr: UnaryExpr):
        self._add("-")
        self._enclose_if_necesary(unary_expr.negated, unary_expr)

    def visit_add(self, add_expr : AddExpr):
        self._visit_additive_or_multiplicative(add_expr)

    def visit_multi(self, multi_expr: MultiExpr):
        self._visit_additive_or_multiplicative(multi_expr)

    def _enclose_if_necesary(self, child : Expr, parent: Expr):
        needs_brackets = self._needs_brackets(child, parent)
        if needs_brackets:
            self._add('(')
        child.accept(self)
        if needs_brackets:
            self._add(')')

        
    def _visit_additive_or_multiplicative(self, expr: MultiExpr | AddExpr):
        for i, child in enumerate(expr.children):
            self._enclose_if_necesary(child, expr)
            if i != len(expr.children)-1:
                self._add(f"{self.space_multiplier*" "}{expr.operations[i]}{self.space_multiplier*" "}")

    def visit_and(self, and_expr: AndExpr):
        self._visit_logical(and_expr, True)

    def visit_or(self, or_expr: OrExpr):
        self._visit_logical(or_expr, False)

    def _visit_logical(self, expr: AndExpr | OrExpr, is_and: bool):
        for i, child in enumerate(expr.children):
            self._enclose_if_necesary(child, expr)
            if i != len(expr.children) - 1:
                self._add(f"{self.space_multiplier*" "}{'&' if is_and else '|'}{self.space_multiplier*" "}")

    def visit_rel(self, rel_expr: RelationExpr):
        self._enclose_if_necesary(rel_expr.left, rel_expr)
        self._add(f"{self.space_multiplier*' '}{rel_expr.operator}{self.space_multiplier*' '}")
        self._enclose_if_necesary(rel_expr.right, rel_expr)
        

        
    def visit_obj_access(self, obj_access: ObjectAccess):
        self._add(".".join(obj_access.name_chain))


    def visit_var_dec(self, var_dec: VariableDeclaration):
        self._add_indented("")
        self._visit_start_var_dec_or_param(var_dec)
        self._add(';\n')

    def visit_assignment(self, assignment: AssignmentStatement):
        self._add_indented("")
        assignment.obj_access.accept(self)
        self._add(f"{self.space_multiplier*" "}={self.space_multiplier*" "}")
        assignment.expr.accept(self)
        self._add(';\n')
    
    
    def visit_if(self, if_stmt: IfStatement):
        self._add_indented(f"if{self.space_multiplier*" "}")
        if_stmt.cond.accept(self)
        self._add("\n")
        self._add_block(self._if_content, if_stmt.prog)
        if if_stmt.else_prog:
            self._add_indented("else\n")
            self._add_block(self._else_content, if_stmt.else_prog)

    def _if_content(self, prog: Program):
        prog.accept(self)

    def _else_content(self, else_prog: Program):
        else_prog.accept(self)

    def visit_while(self, while_stmt: WhileStatement):
        self._add_indented(f"while{self.space_multiplier*" "}")
        while_stmt.cond.accept(self)
        self._add('\n')
        self._add_indented("begin\n")
        self.curr_indentation += 1
        while_stmt.prog.accept(self)
        self.curr_indentation -= 1
        self._add_indented("end\n")
        

    def visit_program(self, program: Program):
        for statement in program.children:
            statement.accept(self)


    def visit_variant_def(self, variant_def : VariantDef):
        self._add_indented(f"{variant_def.name}{self.space_multiplier*' '}:{self.space_multiplier*' '}variant\n")
        self._add_indented("begin\n")
        self.curr_indentation += 1
        for named_type in variant_def.named_types:
            named_type.accept(self)
        self.curr_indentation -= 1
        self._add_indented("end\n")

        
    def visit_named_type(self, named_type : NamedType):
        self._add_indented(f"{named_type.name}{self.space_multiplier*' '}:{self.space_multiplier*' '}{named_type.type};\n")
    


    def visit_case_section(self, case_section : CaseSection):
        self._add_indented(f"case{self.space_multiplier*' '}{case_section.type}\n")
        self._add_indented('begin\n')
        self.curr_indentation += 1
        case_section.program.accept(self)
        self.curr_indentation -= 1
        self._add_indented("end\n")
    
    def visit_visit(self, visit_statement: VisitStatement):
        self._add_indented(f"visit{self.space_multiplier*' '}")
        visit_statement.obj.accept(self)
        self._add('\n')
        self._add_indented("begin\n")
        self.curr_indentation += 1
        for case_section in visit_statement.case_sections:
            case_section.accept(self)
        self.curr_indentation -= 1
        self._add_indented("end\n")
    
    def visit_func_call(self, func_call: FunctionCall):
        self._add(f"{func_call.name}(")
        for i, arg in enumerate(func_call.args, start=1):
            arg.accept(self)
            if i != len(func_call.args):
                self._add(f',{self.space_multiplier*" "}')
        self._add(")")

    def _visit_start_var_dec_or_param(self, var_or_param : VariableDeclaration | Param):
        self._add(f"{var_or_param.name}{self.space_multiplier*' '}:{self.space_multiplier*' '}{f"mut{self.space_multiplier*' '}" if var_or_param.is_mutable else ""}{var_or_param.type}")
        if var_or_param.default_value:
            self._add(f"{self.space_multiplier*" "}={self.space_multiplier*" "}")
            var_or_param.default_value.accept(self)

    def visit_param(self, param : Param):
        self._visit_start_var_dec_or_param(param)

        
    
    def visit_func_def(self, func_def : FuncDef):
        self._add_indented(f"{func_def.name}(")
        for i, param in enumerate(func_def.params, start=1):
            param.accept(self)
            if i != len(func_def.params):
                self._add(f',{self.space_multiplier*" "}')
        self._add(f"){self.space_multiplier*' '}:{self.space_multiplier*' '}{func_def.type}\n")
        self._add_indented("begin\n")
        self.curr_indentation += 1
        func_def.prog.accept(self)
        self.curr_indentation -= 1
        self._add_indented("end\n")
    

    
    def visit_return(self, return_stmt: ReturnStatement):
        self._add_indented(f"return{self.space_multiplier*' '}")
        return_stmt.expr.accept(self)
        self._add(";\n")

    
    
    def visit_struct_def(self, struct_def: StructDef):
        self._add_indented(f"{struct_def.name}{self.space_multiplier*' '}:{self.space_multiplier*' '}struct\n")
        self._add_block(self._struct_def_content, struct_def.attributes)

    def _struct_def_content(self, attrs : List[VariableDeclaration]):
        for attr in attrs:
            attr.accept(self)

    def _add_block(self, content : Callable, args):
        self._add_indented("begin\n")
        self.curr_indentation += 1
        content(args)
        self.curr_indentation -= 1
        self._add_indented("end\n")

    
    def _add_indented(self, string : str):
        self.parts.append(f"{self.curr_indentation*self.indentation_multiplier*' '}{string}")

    def _add(self, string : str):
        self.parts.append(string)