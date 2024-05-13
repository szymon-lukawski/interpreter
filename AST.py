"""Module defining classes for Abstract syntax tree used in parser"""



class ASTNode:
    def __init__(self, children) -> None:
        self.children = children

class Program(ASTNode):
    pass

class Statement(ASTNode):
    pass

class Comment(Statement):
    def __init__(self, children, value) -> None:
        super().__init__(children)
        self.value = value

class ReturnStatement(Statement):
    def __init__(self, children, value) -> None:
        super().__init__(children)
        self.value = value

class CondStatement(Statement):
    def __init__(self, children) -> None:
        super().__init__(children)

class IfStatement(CondStatement):
    pass

class WhileStatement(CondStatement):
    pass

class VisitStatement(Statement):
    pass

class Type(ASTNode):
    pass

class CaseSection(ASTNode):
    pass

class FunctionCall(ASTNode):
    pass

class Identifier(ASTNode):
    pass

class ObjectAccess():
    pass

class AssignmentStatement(Statement):
    pass

class MutableVar(ASTNode):
    pass

class UnmutableVar(ASTNode):
    pass

class StructDef(ASTNode):
    pass

class VariantDef(ASTNode):
    pass

class NamedType(ASTNode):
    pass

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
    pass

class SubTract(Expr):
    pass

class MultiExpr(Expr):
    pass

class TimesExpr(MultiExpr):
    pass

class DivideExpr(MultiExpr):
    pass



class UnaryExpr(Expr):
    pass

class Term(Expr):
    pass

class Literal(ASTNode):
    pass

class NullLiteral(Term):
    pass

class IntLiteral(Term):
    pass

class FloatLiteral(Term):
    pass

class StrLiteral(Term):
    pass
