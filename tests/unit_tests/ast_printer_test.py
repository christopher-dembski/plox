import unittest

from lox_token import Token
from token_type import TokenType
from expr import BinaryExpr, UnaryExpr, LiteralExpr, GroupingExpr, AssignmentExpr, VariableExpr
from stmt import VarStmt, ExpressionStmt, PrintStmt
from tests.test_helpers.test_case_with_helpers import TestCaseWithHelpers


class TestAstPrinter(TestCaseWithHelpers):

    def test_ast_printer(self):
        ast = BinaryExpr(
            UnaryExpr(
                Token(TokenType.MINUS, '-', None, 1),
                LiteralExpr(123)
            ),
            Token(TokenType.STAR, '*', None, 1),
            GroupingExpr(LiteralExpr(45.67))
        )
        self.assertEqual('(* (- 123) (group 45.67))', self.build(ast))

    def test_variable_expression(self):
        ast = VariableExpr(
            Token(TokenType.IDENTIFIER, 'a', None, 1)
        )
        self.assertEqual('a', self.build(ast))

    def test_assignment_expression(self):
        ast = AssignmentExpr(
            Token(TokenType.IDENTIFIER, 'a', None, 1),
            LiteralExpr(5)
        )
        self.assertEqual('(= a 5)', self.build(ast))

    def test_var_statement(self):
        ast = VarStmt(
            Token(TokenType.IDENTIFIER, 'a', None, 1),
            LiteralExpr(5)
        )
        self.assertEqual('stmt(var a)', self.build(ast))

    def test_expression_statement(self):
        ast = ExpressionStmt(
            AssignmentExpr(
                Token(TokenType.IDENTIFIER, 'a', None, 1),
                LiteralExpr(5)
            )
        )
        self.assertEqual('stmt(= a 5)', self.build(ast))

    def test_print_statement(self):
        ast = PrintStmt(LiteralExpr(9))
        self.assertEqual('stmt(print 9)', self.build(ast))


if __name__ == '__main__':
    unittest.main()
