"""Module for parser"""
from typing import List
from lexer import Lexer
from AST import *
from token_type import TokenType
from parser_exceptions import ParserException

class Parser:
    """Parser class"""
    def __init__(self, lexer: Lexer):
        self.lexer : Lexer = lexer

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
        multi_op = self._parse_multi_operator()
        while multi_op:
            multi_exprs.append(multi_op)
            multi_exprs.append(self._parse_multi_expr())
            multi_op = self._parse_multi_operator()
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
        add_op = self._parse_additive_operator()
        while add_op:
            unary_exprs.append(add_op)
            unary_exprs.append(self._parse_unary_expr())
            add_op = self._parse_additive_operator()
        return AddExpr(unary_exprs)
    



    def _parse_additive_operator(self):
        match self.lexer.curr_token.get_type():
            case TokenType.PLUS:
                self._consume_token()
                return TokenType.PLUS
            case TokenType.MINUS:
                self._consume_token()
                return TokenType.MINUS

    def _parse_unary_expr(self):
        if self.lexer.curr_token.get_type() == TokenType.MINUS:
            self._consume_token()
            return UnaryExpr(self._parse_term())
        return self._parse_term()

    def _parse_term(self):
        nested_expr = self._parse_nested_expr()
        if nested_expr:
            return nested_expr
        literal = self._parse_literal()
        if literal:
            return literal
        object_access = self._parse_object_access()
        if object_access:
            return object_access
        raise ParserException()
    
    def _parse_nested_expr(self):
        if self.lexer.curr_token.get_type() == TokenType.LEFT_BRACKET:
            self._consume_token()
            expr = self._parse_expr()
            self._must_parse(TokenType.RIGHT_BRACKET)
            return expr

    def _parse_literal(self):
        literal_class = None
        match self.lexer.curr_token.get_type():
            case TokenType.NULL:
                return NullLiteral([])
            case TokenType.INT_LITERAL:
                literal_class = IntLiteral
            case TokenType.STR_LITERAL:
                literal_class = StrLiteral
            case TokenType.FLOAT_LITERAL:
                literal_class = FloatLiteral
            case _:
                return None
        return literal_class(([self.lexer.curr_token.get_value()]))





    def _consume_token(self):
        self.lexer._next_token()

    def _must_parse(self, token_type: TokenType):
        if self.lexer.curr_token.get_type() == token_type:
            self._consume_token()
        raise ParserException
            
        

