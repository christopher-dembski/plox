import unittest

from ast_printer import AstPrinter
from expr import BinaryExpr, UnaryExpr, LiteralExpr, GroupingExpr
from lox_token import Token
from token_type import TokenType


class TestAstPrinter(unittest.TestCase):
    def test_ast_printer(self):
        expr = BinaryExpr(
            UnaryExpr(
                Token(TokenType.MINUS, '-', None, 1),
                LiteralExpr(123)
            ),
            Token(TokenType.STAR, '*', None, 1),
            GroupingExpr(LiteralExpr(45.67))
        )
        self.assertEqual(
            AstPrinter().print(expr),
            '(* (- 123) (group 45.67))'
        )


if __name__ == '__main__':
    unittest.main()
