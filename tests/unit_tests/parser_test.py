import unittest

from lox_token import Token
from token_type import TokenType
from expr import BinaryExpr, UnaryExpr, LiteralExpr, GroupingExpr
from parser import Parser
from ast_printer import AstPrinter


class TestParser(unittest.TestCase):
    def test_parser(self):
        tokens = [
            Token(TokenType.MINUS, '-', None, 1),
            Token(TokenType.NUMBER, '56', 56, 1),
            Token(TokenType.STAR, '*', None, 1),
            Token(TokenType.LEFT_PAREN, '(', None, 1),
            Token(TokenType.TRUE, 'true', None, 1),
            Token(TokenType.PLUS, '+', None, 1),
            Token(TokenType.STRING, '"hello"', 'hello', 1),
            Token(TokenType.RIGHT_PAREN, ')', None, 1),
            Token(TokenType.EOF, '', None, 1)
        ]
        expression = Parser(tokens).parse()
        expected_expression = BinaryExpr(
            UnaryExpr(
                Token(TokenType.MINUS, '-', None, 1),
                LiteralExpr(56)
            ),
            Token(TokenType.STAR, '*', None, 1),
            GroupingExpr(
                BinaryExpr(
                    LiteralExpr(True),
                    Token(TokenType.PLUS, '+', None, 1),
                    LiteralExpr('hello')
                )
            )
        )
        # equality of expressions is checked recursively
        self.assertEqual(
            expected_expression,
            expression,
            msg=f'{AstPrinter().build_ast_string(expression)} '
                f'should equal '
                f'{AstPrinter().build_ast_string(expected_expression)}'
        )

    if __name__ == '__main__':
        unittest.main()
