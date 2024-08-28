from lox_token import Token
from token_type import TokenType
from stmt import StmtVisitor, ExpressionStmt, PrintStmt, VarStmt, Stmt, BlockStmt
from expr import Expr, ExprVisitor, BinaryExpr, GroupingExpr, LiteralExpr, UnaryExpr, AssignmentExpr, VariableExpr


class AstPrinter(ExprVisitor, StmtVisitor):

    def build_ast_string(self, expr: Expr | Stmt) -> str:
        return expr.accept(self)

    def visit_block_stmt(self, stmt: BlockStmt) -> str:
        statements_list = ', '.join(statement.accept(self) for statement in stmt.statements)
        return f'block({statements_list})'

    def visit_var_stmt(self, stmt: VarStmt) -> str:
        return f'stmt(var {stmt.name.lexeme})'

    def visit_expression_stmt(self, stmt: ExpressionStmt) -> str:
        return f'stmt{stmt.expression.accept(self)}'

    def visit_print_stmt(self, stmt: PrintStmt) -> str:
        return f'stmt(print {stmt.expression.accept(self)})'

    def visit_binary_expr(self, expr: BinaryExpr) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: GroupingExpr) -> str:
        return self.parenthesize('group', expr.expression)

    def visit_literal_expr(self, expr: LiteralExpr) -> str:
        if expr.value is None:
            return 'nil'
        if type(expr.value) is str:
            return f'"{expr.value}"'
        return str(expr.value)

    def visit_unary_expr(self, expr: UnaryExpr) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def visit_variable_expr(self, expr: VariableExpr) -> str:
        return expr.name.lexeme

    def visit_assignment_expr(self, expr: AssignmentExpr) -> str:
        return f'(= {expr.name.lexeme} {expr.value.accept(self)})'

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
    print(AstPrinter().build_ast_string(expr))


if __name__ == '__main__':
    main()
