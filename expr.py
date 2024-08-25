from lox_token import Token
from abc import ABC, abstractmethod


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


class ExprVisitor(ABC):
    @abstractmethod
    def visit_binary_expr(self, expr):
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr):
        pass

    @abstractmethod
    def visit_literal_expr(self, expr):
        pass

    @abstractmethod
    def visit_unary_expr(self, expr):
        pass


class BinaryExpr(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_binary_expr(self)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.left == other.left and self.operator == other.operator and self.right == other.right

    def __repr__(self):
        return f'BinaryExpr(left={self.left}, operator={self.operator}, right={self.right})'


class GroupingExpr(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_grouping_expr(self)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.expression == other.expression

    def __repr__(self):
        return f'GroupingExpr(expression={self.expression})'


class LiteralExpr(Expr):
    def __init__(self, value: object):
        self.value = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_literal_expr(self)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.value == other.value

    def __repr__(self):
        return f'LiteralExpr(value={self.value})'


class UnaryExpr(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_unary_expr(self)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.operator == other.operator and self.right == other.right

    def __repr__(self):
        return f'UnaryExpr(operator={self.operator}, right={self.right})'
