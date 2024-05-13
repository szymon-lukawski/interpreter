"""Module for parser"""

from typing import List
from lexer import Lexer
from AST import *
from token_type import TokenType
from parser_exceptions import ParserException


class Parser:
    """Parser class"""

    def __init__(self, lexer: Lexer):
        self.lexer: Lexer = lexer
        self.lexer._next_token()
        self._buffered = None

    def parse_program(self):
        """Parses program :) returns Program AST"""
        statements: List = []
        while (
            self.lexer.curr_token.get_type() != TokenType.EOT
            and self.lexer.curr_token.get_type() != TokenType.END
        ):
            statements.append(self._parse_statement())
        return Program(statements)

    def _parse_statement(self):
        prog = self._parse_block()
        if prog:
            return prog
        ret_state = self._parse_return_statement()
        if ret_state:
            return ret_state
        while_state = self._parse_while_statement()
        if while_state:
            return while_state
        if_state = self._parse_if_statement()
        if if_state:
            return if_state
        visit_state = self._parse_visit_statement()
        if visit_state:
            return visit_state
        starting_with_identifier = self._parse_dec_and_def_or_assign_or_fun_call()
        if starting_with_identifier:
            return starting_with_identifier
        raise ParserException()

    def _parse_return_statement(self):
        if self._try_parse(TokenType.RETURN):
            expr = self._shall(self._parse_expr)
            self._must_parse(TokenType.SEMICOLON)
            return ReturnStatement(expr)

    def _parse_while_statement(self):
        if self._try_parse(TokenType.WHILE):
            cond = self._shall(self._parse_expr())
            prog = self._shall(self._parse_block())
            return WhileStatement(cond, prog)

    def _parse_if_statement(self):
        if self._try_parse(TokenType.IF):
            cond = self._shall(self._parse_expr())
            prog = self._shall(self._parse_block())
            else_prog = None
            if self._try_parse(TokenType.ELSE):
                else_prog = self._shall(self._parse_block())
            return IfStatement(cond, prog, else_prog)

    def _parse_visit_statement(self):
        if self._try_parse(TokenType.VISIT):
            obj = self._shall(self._parse_object_access())
            self._must_parse(TokenType.BEGIN)
            css = self._parse_case_sections()
            self._must_parse(TokenType.END)
            return VisitStatement(obj, css)

    def _parse_case_sections(self):
        css = []
        while self.lexer.curr_token() == TokenType.CASE:
            self._consume_token()
            t = self._shall(self._parse_type())
            p = self._shall(self._parse_block())
            css.append(CaseSection(t, p))
        return css

    def _parse_object_access(self):
        funcs_or_idents = []
        funcs_or_idents.append(self._parse_func_or_ident())
        while self.lexer.curr_token.get_type() == TokenType.DOT:
            self._consume_token()
            funcs_or_idents.append(self._parse_func_or_ident())
        if len(funcs_or_idents) == 1:
            return funcs_or_idents[0]
        return ObjectAccess(funcs_or_idents)

    def _parse_dec_and_def_or_assign_or_fun_call(self):
        name = self._parse_identifier()
        match self.lexer.curr_token.get_type():
            case TokenType.DOT:
                # assignment
                return self._shall(self._parse_rest_assignment(name))
            case TokenType.COLON:
                # variable declaration or type def
                self._consume_token()
                struct = self._parse_rest_struct(name)
                if struct:
                    return struct
                variant = self._parse_rest_variant(name)
                if variant:
                    return variant
                # must be variable declaration or error
                return self._shall(self._parse_rest_var_dec_statement(name))
            case TokenType.LEFT_BRACKET:
                return self._shall(self._parse_rest_func_def_or_func_call(name))

    def _parse_rest_func_def_or_func_call(self, name):
        if self._try_parse(TokenType.LEFT_BRACKET):
            buffered = self.lexer.curr_token
            match buffered.get_type():
                case TokenType.RIGHT_BRACKET:
                    if self._try_parse(TokenType.COLON):
                        t = self._shall(self._parse_type())
                        p = self._shall(self._parse_block())
                        return FuncDef(name, [], t, p)
                    self._must_parse(TokenType.SEMICOLON)
                    return FunctionCall(name, [])
                case TokenType.IDENTIFIER:
                    self._consume_token()
                    if self._try_parse(TokenType.COLON):
                        self._buffered = buffered
                        params = self._parse_params()
                        self._must_parse(TokenType.RIGHT_BRACKET)
                        self._must_parse(TokenType.COLON)
                        t = self._shall(self._parse_type())
                        p = self._shall(self._parse_block())
                        return FuncDef(name, params, t, p)
                    self._buffered = buffered
                    args = self._parse_args()
                    self._must_parse(TokenType.RIGHT_BRACKET)
                    self._must_parse(TokenType.SEMICOLON)
                    return FunctionCall(name, args)
                case _:
                    args = self._parse_args()
                    self._must_parse(TokenType.RIGHT_BRACKET)
                    self._must_parse(TokenType.SEMICOLON)
                    return FunctionCall(name, args)

    def _parse_rest_variant(self, name):
        if self._try_parse(TokenType.VARIANT):
            self._must_parse(TokenType.BEGIN)
            named_types = self._parse_named_types()
            self._must_parse(TokenType.END)
            return VariantDef(name, named_types)

    def _parse_named_types(self) -> List[NamedType]:
        named_types = []
        named_type = self._parse_named_type()
        while named_type:
            named_types.append(named_type)
            named_type = self._parse_named_type()
        return named_types

    def _parse_named_type(self) -> NamedType:
        name = self._parse_identifier()
        if name:
            self._must_parse(TokenType.COLON)
            t = self._shall(self._parse_type())
            self._must_parse(TokenType.SEMICOLON)
            return NamedType(name, t)

    def _parse_rest_struct(self, name):
        if self._try_parse(TokenType.STRUCT):
            self._must_parse(TokenType.BEGIN)
            var_decs = []
            var_dec_state = self._parse_var_dec_stat()
            while var_dec_state:
                var_decs.append(var_dec_state)
                var_dec_state = self._parse_var_dec_stat()
            return StructDef(name, var_decs)

    def _parse_rest_assignment(self, name):
        attr_access = [name]
        while self._try_parse(TokenType.DOT):
            attr_access.append(self._shall(self._parse_identifier()))
        self._must_parse(TokenType.ASSIGNMENT)
        expr = self._shall(self._parse_expr())
        self._must_parse(TokenType.SEMICOLON)
        return AssignmentStatement(attr_access, expr)

    # identifier, ':', ['mut'], type, ['=', expression]
    def _parse_var_dec_stat(self):
        name = self.lexer.curr_token.get_value()
        self._must_parse(TokenType.IDENTIFIER)
        self._must_parse(TokenType.COLON)
        return self._parse_rest_var_dec_statement(name)

    #  ['mut'], type, ['=', expression]
    def _parse_rest_var_dec_statement(self, name):
        if self.lexer.curr_token.get_type() == TokenType.MUT:
            var_class = MutableVar
            self._consume_token()
        else:
            var_class = UnmutableVar

        t = self._parse_type()
        if self.lexer.curr_token.get_type() == TokenType.SEMICOLON:
            self._consume_token()
            return var_class([name, t])
        self._must_parse(TokenType.ASSIGNMENT)
        expr = self._parse_expr()
        self._must_parse(TokenType.SEMICOLON)
        return var_class([name, t, expr])

    def _parse_func_or_ident(self):
        name = self._shall(self._parse_identifier())
        if self._try_parse(TokenType.LEFT_BRACKET):
            args = self._parse_args()
            self._must_parse(TokenType.RIGHT_BRACKET)
            if args:
                return FunctionCall(name, args)
        return Identifier(name)

    def _parse_identifier(self):
        curr_t = self.lexer.curr_token
        if curr_t.get_type() == TokenType.IDENTIFIER:
            name = curr_t.get_value()
            self._consume_token()
            return name

    def _parse_args(self):
        args = []
        expr = self._parse_expr()
        if expr:
            args.append(expr)
            while self._try_parse(TokenType.COMMA):
                args.append(self._shall(self._parse_expr()))
        return args

    def _parse_params(self):
        params = []
        if self.lexer.curr_token() != TokenType.RIGHT_BRACKET:
            params.append(self._parse_param())
            while self.lexer.curr_token() == TokenType.COMMA:
                self._consume_token()
                params.append(self._parse_param())
        return params

    def _parse_param(self):
        name = self.lexer.curr_token.get_value()
        self._must_parse(TokenType.IDENTIFIER)
        self._must_parse(TokenType.COLON)
        if self._try_parse(TokenType.MUT):
            param_class = MutParam
        else:
            param_class = NonMutParam
        t = self._shall(self._parse_type())
        return param_class([name, t])

    def _parse_type(self):
        tt = self.lexer.curr_token()
        if (
            tt == TokenType.INT
            or tt == TokenType.FLOAT
            or tt == TokenType.STR
            or tt == TokenType.NULL_TYPE
            or tt == TokenType.IDENTIFIER
        ):
            self._consume_token()
            return Type(tt)

    def _parse_block(self):
        if self._try_parse(TokenType.BEGIN):
            temp = self.parse_program()
            self._must_parse(TokenType.END)
            return temp

    # logical or expr
    def _parse_expr(self):
        return self._parse_logical_or_expr()

    def _parse_logical_or_expr(self):
        and_exprs = []
        and_exprs.append(self._parse_logical_and_expr())
        while self.lexer.curr_token.get_type() == TokenType.OR:
            self._consume_token()
            and_exprs.append(self._parse_logical_and_expr())
        if len(and_exprs) == 1:
            return and_exprs[0]
        return OrExpr(and_exprs)

    def _parse_logical_and_expr(self):
        rel_exprs = []
        rel_exprs.append(self._parse_rel_expr())
        while self.lexer.curr_token.get_type() == TokenType.AND:
            self._consume_token()
            rel_exprs.append(self._parse_rel_expr())
        if len(rel_exprs) == 1:
            return rel_exprs[0]
        return AndExpr(rel_exprs)

    def _parse_rel_expr(self):
        first = self._parse_add_expr()
        rel = self._parse_rel_operator()
        if rel:
            return RelationExpr(first, rel, self._parse_add_expr())
        return first

    def _parse_rel_operator(self):
        match self.lexer.curr_token.get_type():
            case TokenType.LESS:
                self._consume_token()
                return TokenType.LESS
            case TokenType.LESS_EQUAL:
                self._consume_token()
                return TokenType.LESS_EQUAL
            case TokenType.GREATER:
                self._consume_token()
                return TokenType.GREATER
            case TokenType.GREATER_EQUAL:
                self._consume_token()
                return TokenType.GREATER_EQUAL
            case TokenType.EQUAL:
                self._consume_token()
                return TokenType.EQUAL
            case TokenType.INEQUAL:
                self._consume_token()
                return TokenType.INEQUAL

    def _parse_add_expr(self):
        multi_exprs = []
        multi_exprs.append(self._parse_multi_expr())
        additive_op = self._parse_additive_operator()
        while additive_op:
            multi_exprs.append(additive_op)
            multi_exprs.append(self._parse_multi_expr())
            additive_op = self._parse_additive_operator()
        if len(multi_exprs) == 1:
            return multi_exprs[0]
        return AddExpr(multi_exprs)

    def _parse_multi_operator(self):
        match self.lexer.curr_token.get_type():
            case TokenType.TIMES:
                self._consume_token()
                return TokenType.TIMES
            case TokenType.DIVIDE:
                self._consume_token()
                return TokenType.DIVIDE

    def _parse_multi_expr(self):
        unary_exprs = []
        unary_exprs.append(self._parse_unary_expr())
        multi_op = self._parse_multi_operator()
        while multi_op:
            unary_exprs.append(multi_op)
            unary_exprs.append(self._parse_unary_expr())
            multi_op = self._parse_multi_operator()
        if len(unary_exprs) == 1:
            return unary_exprs[0]
        return MultiExpr(unary_exprs)

    def _parse_additive_operator(self):
        match self.lexer.curr_token.get_type():
            case TokenType.PLUS:
                self._consume_token()
                return TokenType.PLUS
            case TokenType.MINUS:
                self._consume_token()
                return TokenType.MINUS

    def _parse_unary_expr(self):
        if self._try_parse(TokenType.MINUS):
            return UnaryExpr(self._shall(self._parse_term()))
        return self._shall(self._parse_term())

    def _parse_term(self):
        if (
            (nested_expr := self._parse_nested_expr())
            or (literal := self._parse_literal())
            or (object_access := self._parse_object_access())
        ):
            return nested_expr or literal or object_access

    def _parse_nested_expr(self):
        if self._try_parse(TokenType.LEFT_BRACKET):
            expr = self._parse_expr()
            self._must_parse(TokenType.RIGHT_BRACKET)
            return expr

    def _parse_literal(self):
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

    def _shall(self, parsed):
        if not parsed:
            raise ParserException()
        return parsed

    def _try_parse(self, token_type: TokenType):
        if self.lexer.curr_token.get_type() == token_type:
            self._consume_token()
            return True

    def _consume_token(self):
        if self._buffered:
            temp = self._buffered
            self._buffered = None
            return temp
        self.lexer._next_token()

    def _must_parse(self, token_type: TokenType):
        if self.lexer.curr_token.get_type() == token_type:
            self._consume_token()
        raise ParserException
