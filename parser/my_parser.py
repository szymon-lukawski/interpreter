"""Module for parser"""

from typing import List
from lexer.lexer import Lexer
from parser.AST import *
from lexer.token_type import TokenType
from parser.parser_exceptions import (
    ParserException,
    ExpectedDifferentToken,
    PatternNotRecognised,
)
from lexer.utils import get_type_name


class Parser:
    """Parser class"""

    def __init__(self, lexer: Lexer):
        self.lexer: Lexer = lexer
        self.lexer._next_token()

    def parse_program(self):
        """
        Parses program :) returns Program AST\n
        program \:\:\= {statement};
        """
        statements: List[Statement] = []
        pos = self._get_current_pos()
        while statement := self._try_parse_statement():
            statements.append(statement)
        return Program(statements, pos)

    def _parse_statement(self):
        pos = self._get_current_pos()
        if statement := self._try_parse_statement():
            return statement
        raise PatternNotRecognised(position=pos)

    def _try_parse_statement(self):
        """statement ::=  variable_declaration_statement
        | assignment_statement
        | if_statement
        | while_statement
        | function_definition_statement
        | type_definition_statement
        | visit_statement
        | return_statement
        | block
        | function_call_statement
        """
        if prog := self._try_parse_block():
            return prog
        if ret_state := self._try_parse_return():
            return ret_state
        if while_state := self._try_parse_while_statement():
            return while_state
        if if_state := self._try_parse_if_statement():
            return if_state
        if visit_state := self._try_parse_visit_statement():
            return visit_state
        if (
            starting_with_identifier := self._try_parse_dec_and_def_or_assign_or_fun_call()
        ):
            return starting_with_identifier


    def _try_parse_return(self):
        """return_statement ::== 'return', [expression], ';';"""
        pos = self._get_current_pos()
        if self._try_parse(TokenType.RETURN):
            expr = self._parse_expr()
            self._must_parse(TokenType.SEMICOLON)
            return ReturnStatement(expr, pos)

    def _try_parse_while_statement(self):
        """while_statement ::= 'while', expression, block;"""
        pos = self._get_current_pos()
        if self._try_parse(TokenType.WHILE):
            cond = self._parse_expr()
            prog = self._parse_block()
            return WhileStatement(cond, prog, pos)

    def _try_parse_if_statement(self):
        """if_statement ::= 'if', expression, block, ['else', block];"""
        pos = self._get_current_pos()
        if self._try_parse(TokenType.IF):
            cond = self._parse_expr()
            prog = self._parse_block()
            else_prog = None
            if self._try_parse(TokenType.ELSE):
                else_prog = self._parse_block()
            return IfStatement(cond, prog, else_prog, pos)

    def _try_parse_visit_statement(self):
        """visit_statement ::= 'visit', object_access, 'begin', {case_section} ,'end';"""
        pos = self._get_current_pos()
        if self._try_parse(TokenType.VISIT):
            obj = self._parse_object_access()
            self._must_parse(TokenType.BEGIN)
            case_sections = self._try_parse_case_sections()
            self._must_parse(TokenType.END)
            return VisitStatement(obj, case_sections, pos)

    def _try_parse_case_sections(self):
        """{case_section ::= 'case', type, 'begin', program,'end';}"""
        case_sections = []
        pos = self._get_current_pos()
        while self._try_parse(TokenType.CASE):
            type_ = self._parse_type()
            program = self._parse_block()
            case_sections.append(CaseSection(type_, program,pos))
            pos = self._get_current_pos()
        return case_sections

    def _try_parse_object_access(self, initial_name: str = None, pos=None):
        """object_access ::=  func_or_ident, {('.', func_or_ident)};"""
        funcs_or_idents = []
        pos = self._get_current_pos() if not pos else pos
        if not initial_name:
            funcs_or_idents.append(self._try_parse_func_or_name())
        else:
            funcs_or_idents.append(self._try_parse_func_or_name(initial_name))
        if funcs_or_idents[0]:
            while self._try_parse(TokenType.DOT):
                funcs_or_idents.append(self._parse_func_or_name())
            return ObjectAccess(funcs_or_idents, pos)

    def _parse_object_access(self):
        if obj_access := self._try_parse_object_access():
            return obj_access
        raise ExpectedDifferentToken(
            self._get_current_pos(), "Expected object access"
        )

    def _parse_func_or_name(self):
        if func_or_name_with_pos := self._try_parse_func_or_name():
            return func_or_name_with_pos
        raise ExpectedDifferentToken(
            self._get_current_pos(), "Expected function call or just identifier"
        )

    def _try_parse_dec_and_def_or_assign_or_fun_call(self):
        """identifier"""
        pos = self._get_current_pos()
        if name := self._try_parse_identifier():
            return self._parse_after_identifier(name, pos)

    def _parse_after_identifier(self, name, pos):
        if self.lexer.curr_token.get_type() == TokenType.DOT or self.lexer.curr_token.get_type() == TokenType.ASSIGNMENT:
            return self._parse_rest_assignment(name, pos)
        if self._try_parse(TokenType.COLON):
            # variable declaration or type def
            if struct := self._try_parse_rest_struct(name, pos):
                return struct
            if variant := self._try_parse_rest_variant(name, pos):
                return variant
            # must be variable declaration or error
            return self._parse_rest_var_dec_statement(name, pos)
        if self._try_parse(TokenType.LEFT_BRACKET):
            return self._parse_rest_func_def_or_func_call(name, pos)
        raise ExpectedDifferentToken(
            position=self.lexer.curr_token.get_pos(), msg="Expected: . = : ("
        )

    def _try_parse_no_arg_or_no_param_function_def_or_call(self, name, pos):
        if self._try_parse(TokenType.RIGHT_BRACKET):
            if self._try_parse(TokenType.COLON):
                return self._parse_rest_func_def(name, [], pos)
            self._must_parse(TokenType.SEMICOLON)
            return FunctionCall(name, [], pos)

    def _parse_rest_func_def(self, name, params=None, pos=None):
        type_ = self._parse_type()
        program = self._parse_block()
        return FuncDef(name, params, type_, program, pos)

    def _parse_start_with_identifier_func_def_or_call(self, name, pos):
        pos_arg_or_param = self._get_current_pos()
        if ident := self._try_parse_identifier():
            if self._try_parse(TokenType.COLON):
                params = self._parse_params([self._parse_param(ident, pos_arg_or_param)])
                self._must_parse(TokenType.RIGHT_BRACKET)
                self._must_parse(TokenType.COLON)
                return self._parse_rest_func_def(name, params, pos)
            first_arg = self._try_parse_object_access(ident, pos_arg_or_param) # albo funkcja
            args = self._try_parse_args(first_arg)
            return self._parse_ending_of_function_call_statement(name, args, pos)

    def _parse_ending_of_function_call_statement(self, name, args, pos):
        self._must_parse(TokenType.RIGHT_BRACKET)
        self._must_parse(TokenType.SEMICOLON)
        return FunctionCall(name, args, pos)

    def _parse_rest_func_def_or_func_call(self, name, pos):
        if empty_brackets_func_call_or_def := (
            self._try_parse_no_arg_or_no_param_function_def_or_call(name, pos)
        ):
            return empty_brackets_func_call_or_def
        if start_with_identifier := self._parse_start_with_identifier_func_def_or_call(
            name, pos
        ):
            return start_with_identifier
        args = self._try_parse_args()
        return self._parse_ending_of_function_call_statement(name, args, pos)

    def _try_parse_rest_variant(self, name, pos):
        if self._try_parse(TokenType.VARIANT):
            self._must_parse(TokenType.BEGIN)
            named_types = self._try_parse_named_types()
            self._must_parse(TokenType.END)
            return VariantDef(name, named_types, pos)

    def _try_parse_named_types(self) -> List[NamedType]:
        """{named_type_statement}"""
        named_types = []
        while named_type := self._try_parse_named_type():
            named_types.append(named_type)
        return named_types

    def _try_parse_named_type(self) -> NamedType:
        """named_type_statement ::= identifier, ':', type, ';'"""
        pos = self._get_current_pos()
        if name := self._try_parse_identifier():
            self._must_parse(TokenType.COLON)
            type_ = self._parse_type()
            self._must_parse(TokenType.SEMICOLON)
            return NamedType(name, type_, pos)

    def _try_parse_rest_struct(self, name, pos):
        if self._try_parse(TokenType.STRUCT):
            self._must_parse(TokenType.BEGIN)
            var_decs = []
            while var_dec_state := self._try_parse_var_dec_stat():
                var_decs.append(var_dec_state)
            self._must_parse(TokenType.END)
            return StructDef(name, var_decs, pos)

    def _parse_rest_assignment(self, name, pos):
        """{'.', identifier} '=', expr, ';'"""
        attr_access = [name]
        while self._try_parse(TokenType.DOT):
            attr_access.append(self._parse_identifier())
        self._must_parse(TokenType.ASSIGNMENT)
        expr = self._parse_expr()
        self._must_parse(TokenType.SEMICOLON)
        return AssignmentStatement(ObjectAccess(attr_access), expr, pos)

    def _try_parse_var_dec_stat(self):
        """identifier, ':', ['mut'], type, ['=', expression]"""
        pos = self._get_current_pos()
        if name := self._try_parse_identifier():
            self._must_parse(TokenType.COLON)
            return self._parse_rest_var_dec_statement(name, pos)

    def _parse_rest_var_dec_statement(self, name, pos):
        """['mut'], type, ['=', expression]"""
        expr = None
        is_mutable = bool(self._try_parse(TokenType.MUT))
        var_type = self._parse_type()
        is_no_expr = self._try_parse(TokenType.SEMICOLON)
        if not is_no_expr:
            self._must_parse(TokenType.ASSIGNMENT)
            expr = self._parse_expr()
            self._must_parse(TokenType.SEMICOLON)
            return VariableDeclaration(name, var_type, is_mutable, expr, pos)
        return VariableDeclaration(name, var_type, is_mutable, pos=pos)

    def _try_parse_func_or_name(self, name=None):
        """identifier ['(', args, ')']"""
        pos=self._get_current_pos()
        if not name:
            name = self._try_parse_identifier()
        if self._try_parse(TokenType.LEFT_BRACKET):
            args = self._try_parse_args()
            self._must_parse(TokenType.RIGHT_BRACKET)
            return FunctionCall(name, args, pos)
        return name

    def _parse_identifier(self):
        """identifier"""
        if name := self._try_parse_identifier():
            return name
        raise ExpectedDifferentToken(
            self.lexer.curr_token.get_pos(), "Expected identifier"
        )

    def _try_parse_identifier(self):
        curr_t = self.lexer.curr_token
        if curr_t.get_type() == TokenType.IDENTIFIER:
            name = curr_t.get_value()
            self._consume_token()
            return name

    def _try_parse_args(self, initial_arg=None):
        """args ::= [expression , {',', expression}]"""
        args = []
        if initial_arg:
            args.append(initial_arg)
            self._try_parse(TokenType.COMMA)

        if expr := self._try_parse_expr():
            args.append(expr)
            while self._try_parse(TokenType.COMMA):
                args.append(self._parse_expr())
        return args

    def _parse_params(self, initial_params: List[Param]):
        """params ::= param , {',', param};"""
        if initial_params == []:
            params = []
        else:
            params = [] + initial_params
            self._try_parse(TokenType.COMMA)
        if self.lexer.curr_token.get_type() != TokenType.RIGHT_BRACKET:
            params.append(self._parse_param())
            while self.lexer.curr_token.get_type() == TokenType.COMMA:
                self._consume_token()
                params.append(self._parse_param())
        return params

    def _parse_param(self, name: str = None, pos = None):
        """param ::= identifier, ':', ['mut'], type;"""
        if not name:
            pos = self._get_current_pos()
            name = self._parse_identifier()
            self._must_parse(TokenType.COLON)
        is_mutable = bool(self._try_parse(TokenType.MUT))
        type_ = self._parse_type()
        is_no_expr = self.lexer.curr_token.get_type() == TokenType.COMMA or self.lexer.curr_token.get_type() == TokenType.RIGHT_BRACKET
        if not is_no_expr:
            self._must_parse(TokenType.ASSIGNMENT)
            expr = self._parse_expr()
            return Param(name, type_, is_mutable, expr, pos)
        return Param(name, type_, is_mutable, pos=pos)

    def _parse_type(self):
        """type ::=  'int'
        | 'float'
        | 'str'
        | 'null_type'
        | identifier;"""
        tt = self.lexer.curr_token.get_type()
        if (
            tt == TokenType.INT
            or tt == TokenType.FLOAT
            or tt == TokenType.STR
            or tt == TokenType.NULL_TYPE
            or tt == TokenType.IDENTIFIER
        ):
            name = get_type_name(self.lexer.curr_token)
            self._consume_token()
            return name
        raise ExpectedDifferentToken(self.lexer.curr_token.get_pos(), "Expected type")

    def _try_parse_block(self):
        """block ::= 'begin', program, 'end';"""
        if self._try_parse(TokenType.BEGIN):
            temp = self.parse_program()
            self._must_parse(TokenType.END)
            return temp

    def _parse_block(self):
        if block := self._try_parse_block():
            return block
        raise ExpectedDifferentToken(self.lexer.curr_token.get_pos(), "Expected block")

    def _parse_expr(self):
        """expression ::= logical_or_expression;"""
        return self._parse_logical_or_expr()

    def _try_parse_expr(self):
        return self._try_parse_logical_or_expr()

    def _try_parse_logical_or_expr(self):
        if and_expr := self._try_parse_logical_and_expr():
            return self._try_parse_rest_logical_or(and_expr)

    def _try_parse_rest_logical_or(self, first : Expr):
        pos = first.pos
        and_exprs = [first]
        while self._try_parse(TokenType.OR):
            and_exprs.append(self._parse_logical_and_expr())
        if len(and_exprs) == 1:
            return first
        return OrExpr(and_exprs, pos)

    def _try_parse_rest_logical_and(self, first):
        pos = first.pos
        rel_exprs = [first]
        while self._try_parse(TokenType.AND):
            rel_exprs.append(self._parse_rel_expr())
        if len(rel_exprs) == 1:
            return first
        return AndExpr(rel_exprs, pos)

    def _try_parse_logical_and_expr(self):
        if rel_expr := self._try_parse_rel_expr():
            return self._try_parse_rest_logical_and(rel_expr)

    def _try_parse_rel_expr(self):
        if add_expr := self._try_parse_add_expr():
            return self._try_parse_rest_logical_and(add_expr)

    def _try_parse_add_expr(self):
        if multi_expr := self._try_parse_multi_expr():
            return self._try_parse_rest_add_expr(multi_expr)

    def _try_parse_rest_add_expr(self, first):
        pos = first.pos
        multi_exprs = [first]
        operations = []
        while op := self._try_parse_additive_operator():
            operations.append(op)
            multi_exprs.append(self._parse_multi_expr())
        if len(multi_exprs) == 1:
            return first
        return AddExpr(multi_exprs, operations, pos)

    def _try_parse_multi_expr(self):
        if unary_expr := self._try_parse_unary_expr():
            return self._try_parse_rest_multi_expr(unary_expr)

    def _try_parse_rest_multi_expr(self, first):
        pos = first.pos
        unary_exprs = [first]
        operations = []
        while op := self._try_parse_multi_operator():
            operations.append(op)
            unary_exprs.append(self._parse_unary_expr())
        if len(unary_exprs) == 1:
            return first
        return MultiExpr(unary_exprs, operations, pos)

    def _parse_logical_or_expr(self):
        """logical_or_expression ::= logical_and_expression, {'|', logical_and_expression};"""
        and_expr = self._parse_logical_and_expr()
        return self._try_parse_rest_logical_or(and_expr)

    def _parse_logical_and_expr(self):
        """logical_and_expression ::= relational_expr {'&', relational_expr};"""
        rel_expr = self._parse_rel_expr()
        return self._try_parse_rest_logical_and(rel_expr)

    def _parse_rel_expr(self):
        """relational_expr ::= additive_expr, [relational_operator, additive_expr];"""
        first = self._parse_add_expr()
        return self._try_parse_rest_rel_expr(first)

    def _try_parse_rest_rel_expr(self, first):
        if rel := self._try_parse_rel_operator():
            return RelationExpr(first, self._parse_add_expr(), rel, first.pos)
        return first

    def _try_parse_rel_operator(self):
        """'<' | '<=', '!=' | '==' | '>=' | '>'"""
        less = self._try_parse(TokenType.LESS)
        if less:
            return "<"
        less_eq = self._try_parse(TokenType.LESS_EQUAL)
        if less_eq:
            return "<="
        ineq = self._try_parse(TokenType.INEQUAL)
        if ineq:
            return "!="
        eq = self._try_parse(TokenType.EQUAL)
        if eq:
            return "=="
        greater_eq = self._try_parse(TokenType.GREATER_EQUAL)
        if greater_eq:
            return ">="
        greater = self._try_parse(TokenType.GREATER)
        if greater:
            return ">"

    def _parse_add_expr(self):
        """additive_expr ::= multi_expr, {additive_operator, multi_expr};"""
        multi_expr = self._parse_multi_expr()
        return self._try_parse_rest_add_expr(multi_expr)

    def _try_parse_multi_operator(self):
        """'*' | '/'"""
        times = self._try_parse(TokenType.TIMES)
        if times:
            return "*"
        divide = self._try_parse(TokenType.DIVIDE)
        if divide:
            return "/"

    def _parse_multi_expr(self):
        """multi_expr ::= unary_expr, {multi_operator, unary_expr};"""
        unary_expr = self._parse_unary_expr()
        return self._try_parse_rest_multi_expr(unary_expr)

    def _try_parse_additive_operator(self):
        """'+' | '-'"""
        plus = self._try_parse(TokenType.PLUS)
        if plus:
            return "+"
        minus = self._try_parse(TokenType.MINUS)
        if minus:
            return "-"

    def _parse_unary_expr(self):
        """unary_expr ::= ['-'], term;"""
        pos = self._get_current_pos()
        if self._try_parse(TokenType.MINUS):
            return UnaryExpr(self._parse_term(), pos)
        return self._parse_term()

    def _try_parse_unary_expr(self):
        pos = self._get_current_pos()
        if self._try_parse(TokenType.MINUS):
            return UnaryExpr(self._parse_term(), pos)
        return self._try_parse_term()

    def _try_parse_term(self):
        """term  ::=	literal
        | object_access
        | '(', expression, ')';"""
        if (
            (nested_expr := self._try_parse_nested_expr())
            or (literal := self._try_parse_literal())
            or (object_access := self._try_parse_object_access())
        ):
            return nested_expr or literal or object_access

    def _parse_term(self):
        if term := self._try_parse_term():
            return term
        raise ExpectedDifferentToken(
            self.lexer.curr_token.get_pos(),
            "Expected literal, object access or nested expression",
        )

    def _try_parse_nested_expr(self):
        """'(', expression, ')';"""
        if self._try_parse(TokenType.LEFT_BRACKET):
            expr = self._parse_expr()
            self._must_parse(TokenType.RIGHT_BRACKET)
            return expr

    def _try_parse_literal(self):
        literal_class = None
        match self.lexer.curr_token.get_type():
            case TokenType.NULL:
                self._consume_token()
                return NullLiteral()
            case TokenType.INT_LITERAL:
                literal_class = IntLiteral
            case TokenType.STR_LITERAL:
                literal_class = StrLiteral
            case TokenType.FLOAT_LITERAL:
                literal_class = FloatLiteral
            case _:
                return None
        temp_value = self.lexer.curr_token.get_value()
        self._consume_token()
        return literal_class(temp_value)

    def _shall(self, parsed, if_not_parsed_msg: str = None):
        if not parsed:
            raise ExpectedDifferentToken(
                position=self.lexer.curr_token.get_pos(), msg=if_not_parsed_msg
            )
        return parsed

    def _try_parse(self, token_type: TokenType):
        if self.lexer.curr_token.get_type() == token_type:
            self._consume_token()
            return True

    def _consume_token(self):
        self.lexer._next_token()

    def _must_parse(self, token_type: TokenType):
        if self.lexer.curr_token.get_type() == token_type:
            self._consume_token()
            return
        raise ExpectedDifferentToken(
            self.lexer.curr_token.get_pos(), f"Expected token type: {token_type}"
        )

    def _get_current_pos(self):
        return self.lexer.curr_token.get_pos()