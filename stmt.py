from abc import ABC, abstractmethod
from typing import Iterable
from typing import Sequence

from lox_token import Token
from expr import Expr, VariableExpr


class Stmt(ABC):

    @abstractmethod
    def accept(self, visitor):
        pass


class StmtVisitor(ABC):

    @abstractmethod
    def visit_expression_stmt(self, stmt):
        pass

    @abstractmethod
    def visit_var_stmt(self, stmt):
        pass

    @abstractmethod
    def visit_print_stmt(self, stmt):
        pass

    @abstractmethod
    def visit_return_stmt(self, stmt):
        pass

    @abstractmethod
    def visit_block_stmt(self, stmt):
        pass

    @abstractmethod
    def visit_function_stmt(self, stmt):
        pass

    @abstractmethod
    def visit_class_stmt(self, stmt):
        pass

    @abstractmethod
    def visit_if_stmt(self, stmt):
        pass

    @abstractmethod
    def visit_while_stmt(self, stmt):
        pass


class ExpressionStmt(Stmt):

    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_expression_stmt(self)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.expression == other.expression

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return f'ExpressionStmt(expression={self.expression})'


class VarStmt(Stmt):

    def __init__(self, name: Token, initializer: Expr):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_var_stmt(self)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.name == other.name and self.initializer == other.initializer

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return f'VarStmt(name={self.name}, initializer={self.initializer})'


class PrintStmt(Stmt):

    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_print_stmt(self)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.expression == other.expression

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return f'PrintStmt(expression={self.expression})'


class ReturnStmt(Stmt):

    def __init__(self, keyword: Token, value: Expr):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_return_stmt(self)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.keyword == other.keyword and self.value == other.value

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return f'ReturnStmt(keyword={self.keyword}, value={self.value})'


class BlockStmt(Stmt):

    def __init__(self, statements: Iterable[Stmt]):
        self.statements = statements

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_block_stmt(self)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.statements == other.statements

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return f'BlockStmt(statements={self.statements})'


class FunctionStmt(Stmt):

    def __init__(self, name: Token, params: Sequence[Token], body: BlockStmt):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_function_stmt(self)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.name == other.name and self.params == other.params and self.body == other.body

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return f'FunctionStmt(name={self.name}, params={self.params}, body={self.body})'


class ClassStmt(Stmt):

    def __init__(self, name: Token, superclass: VariableExpr, methods: Iterable[FunctionStmt]):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_class_stmt(self)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.name == other.name and self.superclass == other.superclass and self.methods == other.methods

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return f'ClassStmt(name={self.name}, superclass={self.superclass}, methods={self.methods})'


class IfStmt(Stmt):

    def __init__(self, condition: Expr, if_branch: Stmt, else_branch: Stmt):
        self.condition = condition
        self.if_branch = if_branch
        self.else_branch = else_branch

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_if_stmt(self)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.condition == other.condition and self.if_branch == other.if_branch and self.else_branch == other.else_branch

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return f'IfStmt(condition={self.condition}, if_branch={self.if_branch}, else_branch={self.else_branch})'


class WhileStmt(Stmt):

    def __init__(self, condition: Expr, body: Stmt):
        self.condition = condition
        self.body = body

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_while_stmt(self)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.condition == other.condition and self.body == other.body

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return f'WhileStmt(condition={self.condition}, body={self.body})'
