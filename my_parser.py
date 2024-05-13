"""Module for parser"""
from typing import List
from lexer import Lexer
from AST import *
from token_type import TokenType
from parser_exceptions import ParserException

class Parser:
    """Parser class"""
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

    def parse_program(self):
        """Parses program :) returns Program AST"""
        statements : List = []
        while self.lexer.curr_token.get_type() != TokenType.EOT and self.lexer.curr_token.get_type() != TokenType.END:
            statements.append(self._parse_statement())
        return Program(statements)
    
    def _parse_statement(self):
        curr_token_type = self.lexer.curr_token.get_type()
        if curr_token_type == TokenType.COMMENT:
            return Comment([], self.lexer.curr_token.get_value())
        if curr_token_type == TokenType.BEGIN:
            return self._parse_block()
        if curr_token_type == TokenType.RETURN:
            self._consume_token()
            ret_expr = self._parse_expr()
            self._must_parse(TokenType.SEMICOLON)
            return ReturnStatement([], ret_expr)

        if curr_token_type in [TokenType.WHILE, TokenType.IF]:
            is_if = curr_token_type == TokenType.IF
            self._consume_token()
            cond_expr = self._parse_expr()
            cond_program = self._parse_block()
            statement_class = IfStatement if is_if else WhileStatement
            return statement_class([cond_expr, cond_program])
        
        if curr_token_type == TokenType.VISIT:
            self._consume_token()
            obj = self._parse_object_access()
            self._must_parse(TokenType.BEGIN)
            cs = self._parse_case_sections()
            self._must_parse(TokenType.END)

            return VisitStatement([obj, cs])

        
        if curr_token_type == TokenType.IDENTIFIER:
            self._parse_dec_and_def_or_assign()

    def _parse_case_sections(self):
        css = []
        while self.lexer.curr_token() == TokenType.CASE:
            self._consume_token()
            t = self._parse_type()
            p = self._parse_block()
            css.append(CaseSection([t,p]))
        return css

    def _parse_object_access(self):
        funcs_or_idents = []
        funcs_or_idents.append(self._parse_func_or_ident())
        while self.lexer.curr_token.get_type() == TokenType.DOT:
            self._consume_token()
            funcs_or_idents.append(self._parse_func_or_ident())
        return ObjectAccess(funcs_or_idents)

    def _parse_dec_and_def_or_assign(self):
        name = self.lexer.curr_token.get_value()
        self._consume_token()
        curr_tt = self.lexer.curr_token.get_type()
        if curr_tt == TokenType.DOT:
            # assignment
            attr_access = [name]
            while self.lexer.curr_token.get_type() == TokenType.DOT:
                name = self.lexer.curr_token.get_value()
                self._must_parse(TokenType.IDENTIFIER)
                attr_access.append()
            self._must_parse(TokenType.ASSIGNMENT)
            expr = self._parse_expr()
            self._must_parse(TokenType.SEMICOLON)
            return AssignmentStatement([attr_access, expr])
        if curr_tt == TokenType.COLON:
            # variable declaration or type def
            self._consume_token()
            curr_tt = self.lexer.curr_token.get_type()
            if curr_tt == TokenType.STRUCT:
                self._consume_token()
                self._must_parse(TokenType.BEGIN)
                var_dec = []
                while self.lexer.curr_token.get_type() != TokenType.END:
                    var_dec.append(self._parse_var_dec_stat())
                self._consume_token()
                return StructDef([name, var_dec])
            if curr_tt == TokenType.VARIANT:
                self._consume_token()
                self._must_parse(TokenType.BEGIN)
                named_types = []
                while self.lexer.curr_token.get_type() != TokenType.END:
                    # named type
                    name1 = self.lexer.curr_token.get_value()
                    self._must_parse(TokenType.IDENTIFIER)
                    self._must_parse(TokenType.COLON)
                    t = self._parse_type()
                    self._must_parse(TokenType.SEMICOLON)
                    named_types.append(NamedType([name1, t]))
                self._consume_token()
                return VariantDef([name, named_types])
            # must be variable declaration or error
            return self._parse_rest_var_dec_statement(name)
        if curr_tt == TokenType.LEFT_BRACKET:
            self._consume_token()
            params = self._parse_params()
            self._must_parse(TokenType.RIGHT_BRACKET)
            self._must_parse(TokenType.COLON)
            t = self._parse_type()
            p = self._parse_block()
            return FuncDef([name, params, t, p])



    # identifier, ':', ['mut'], type, ['=', expression]
    def _parse_var_dec_stat(self):
        name = self.lexer.curr_token.get_value()
        self._must_parse(TokenType.IDENTIFIER)
        self._must_parse(TokenType.COLON)
        return self._parse_rest_var_dec_statement(name)
        

    #  ['mut'], type, ['=', expression]
    def _parse_rest_var_dec_statement(self,name):
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
        return var_class([name,t,expr])

    def _parse_func_or_ident(self):
        name = self.lexer.curr_token.get_value()
        self._must_parse(TokenType.IDENTIFIER)
        if self.lexer.curr_token.get_type() == TokenType.LEFT_BRACKET:
            self._consume_token()
            # zakładamy ze jest to function call
            args = self._parse_args()
            self._must_parse(TokenType.RIGHT_BRACKET)
            return FunctionCall([name, args])
        return Identifier([name])

    def _parse_args(self):
        args = []
        if self.lexer.curr_token() != TokenType.RIGHT_BRACKET:
            args.append(self._parse_expr())
            while self.lexer.curr_token() == TokenType.COMMA:
                self._consume_token()
                args.append(self._parse_expr())
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
        if self.lexer.curr_token.get_type() == TokenType.MUT:
            param_class = MutParam
            self._consume_token()
        else:
            param_class = NonMutParam
        t = self._parse_type()
        return param_class([name, t])






        
    def _parse_type(self):
        tt = self.lexer.curr_token()
        if tt == TokenType.INT or tt== TokenType.FLOAT or tt == TokenType.STR or TokenType.IDENTIFIER:
            return Type([tt]) # TODO
        # Czy parse type zawsze ma wolac wyjątek?
        raise ParserException(self.lexer.curr_token.get_pos())

            

    def _parse_block(self):
        self._must_parse(TokenType.BEGIN)
        temp = self.parse_program()
        self._must_parse(TokenType.END)
        return temp
    
    def _parse_expr(self):
        return 1

    def _consume_token(self):
        self.lexer._next_token()

    def _must_parse(self, token_type: TokenType):
        if self.lexer.curr_token.get_type() == token_type:
            self._consume_token()
        raise ParserException
            
        

