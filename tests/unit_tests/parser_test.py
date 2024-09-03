import unittest

from lox import Lox
from lox_token import Token
from tests.test_helpers.test_case_with_helpers import TestCaseWithHelpers
from token_type import TokenType
from stmt import ExpressionStmt
from expr import BinaryExpr, UnaryExpr, LiteralExpr, GroupingExpr
from parser import Parser
from tools.ast_printer import AstPrinter


class TestParser(TestCaseWithHelpers):

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
            Token(TokenType.SEMICOLON, ';', None, 1),
            Token(TokenType.EOF, '', None, 1)
        ]
        parsed_statement = Parser(tokens, Lox()).parse()[0]
        expected_statement = ExpressionStmt(
            BinaryExpr(
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
        )
        # equality of expressions is checked recursively
        self.assertEqual(
            expected_statement,
            parsed_statement,
            msg=f'{AstPrinter().build_ast_string(parsed_statement)} '
                f'should equal '
                f'{AstPrinter().build_ast_string(expected_statement)}'
        )


if __name__ == '__main__':
    unittest.main()
