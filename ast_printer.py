from lox_token import Token
from token_type import TokenType

from expr import Expr, ExprVisitor, BinaryExpr, GroupingExpr, LiteralExpr, UnaryExpr


class AstPrinter(ExprVisitor):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def visit_binary_expr(self, expr: BinaryExpr) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: GroupingExpr) -> str:
        return self.parenthesize('group', expr.expression)

    def visit_literal_expr(self, expr: LiteralExpr) -> str:
        return 'nil' if expr.value is None else str(expr.value)

    def visit_unary_expr(self, expr: UnaryExpr) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *exprs: Expr) -> str:
        return '(' + name + " " + " ".join(expr.accept(self) for expr in exprs) + ')'


def main():
    expr = BinaryExpr(
        UnaryExpr(
            Token(TokenType.MINUS, '-', None, 1),
            LiteralExpr(123)
        ),
        Token(TokenType.STAR, '*', None, 1),
        GroupingExpr(LiteralExpr(45.67))
    )
    print(AstPrinter().print(expr))


if __name__ == '__main__':
    main()
