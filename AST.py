"""Module defining classes for Abstract syntax tree used in parser"""



class ASTNode:
    pass

class Program(ASTNode):
    pass

class Statement(ASTNode):
    pass

class Comment(Statement):
    pass

class ReturnStatement(Statement):
    def __init__(self, expr) -> None:
        self.expr = expr

class CondStatement(Statement):
    pass

class IfStatement(CondStatement):
    def __init__(self, cond, prog, else_prog = None) -> None:
        self.cond = cond
        self.prog = prog
        self.else_prog = else_prog

class WhileStatement(CondStatement):
    def __init__(self, cond, prog) -> None:
        self.cond = cond
        self.prog = prog
class VisitStatement(Statement):
    def __init__(self, obj, css) -> None:
        self.obj = obj
        self.case_sections = css


class Type(ASTNode):
    pass

class CaseSection(ASTNode):
    def __init__(self, type, program) -> None:
        self.type = type
        self.program = program

class FunctionCall(ASTNode):
    def __init__(self, name: str, args) -> None:
        self.name = name
        self.args = args

class Identifier(ASTNode):
    def __init__(self, name) -> None:
        self.name = name
class ObjectAccess(ASTNode):
    def __init__(self, nested_objects) -> None:
        self.nested_objects = nested_objects

class AssignmentStatement(Statement):
    def __init__(self, attr_access, expr) -> None:
        self.attr_access = attr_access
        self.expr = expr

class MutableVar(ASTNode):
    pass

class UnmutableVar(ASTNode):
    pass

class StructDef(ASTNode):
    pass

class VariantDef(ASTNode):
    pass

class NamedType(ASTNode):
    def __init__(self, name, type) -> None:
        self.name = name
        self.type = type


class FuncDef(ASTNode):
    pass

class MutParam(ASTNode):
    pass

class NonMutParam(ASTNode):
    pass


class Expr(ASTNode):
    pass

class OrExpr(Expr):
    pass

class AndExpr(Expr):
    pass
class RelationExpr(Expr):
    pass

class AddExpr(Expr):
    def __init__(self, children) -> None:
        self.children = children

class SubTract(Expr):
    pass

class MultiExpr(Expr):
    def __init__(self, children) -> None:
        self.children = children

class TimesExpr(MultiExpr):
    pass

class DivideExpr(MultiExpr):
    pass



class UnaryExpr(Expr):
    def __init__(self, negated) -> None:
        self.negated = negated
class Term(Expr):
    pass

class Literal(Term):
    def __init__(self, value) -> None:
        self.value = value

class NullLiteral(Literal):
    def __init__(self, value = None) -> None:
        super().__init__(value)

class IntLiteral(Literal):
    pass

class FloatLiteral(Literal):
    pass

class StrLiteral(Literal):
    pass
