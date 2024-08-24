import unittest

import Expr
from AstPrinter import AstPrinter
from lox_token import Token
from token_type import TokenType


class TestAstPrinter(unittest.TestCase):
    def test_ast_printer(self):
        expr = Expr.Binary(
            Expr.Unary(
                Token(TokenType.MINUS, '-', None, 1),
                Expr.Literal(123)
            ),
            Token(TokenType.STAR, '*', None, 1),
            Expr.Grouping(Expr.Literal(45.67))
        )
        self.assertEqual(
            AstPrinter().print(expr),
            '(* (- 123) (group 45.67))'
        )


if __name__ == '__main__':
    unittest.main()
