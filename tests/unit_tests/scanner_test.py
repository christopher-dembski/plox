import unittest

from scanner import Scanner
from lox_token import Token, TokenType
from tests.test_helpers.test_case_with_helpers import TestCaseWithHelpers


class TestScanner(TestCaseWithHelpers):

    def test_scan_tokens(self):
        scanner = Scanner(
            'x = 3\n'
            'if (x < 5) {\n'
            ' print "x is less than 5"\n'
            '}'
        )
        expected_tokens = [
            Token(TokenType.IDENTIFIER, 'x', None, 1),
            Token(TokenType.EQUAL, '=', None, 1),
            Token(TokenType.NUMBER, '3', 3, 1),
            Token(TokenType.IF, 'if', None, 2),
            Token(TokenType.LEFT_PAREN, '(', None, 2),
            Token(TokenType.IDENTIFIER, 'x', None, 2),
            Token(TokenType.LESS, '<', None, 2),
            Token(TokenType.NUMBER, '5', 5, 2),
            Token(TokenType.RIGHT_PAREN, ')', None, 2),
            Token(TokenType.LEFT_BRACE, '{', None, 2),
            Token(TokenType.PRINT, 'print', None, 3),
            Token(TokenType.STRING, '"x is less than 5"', 'x is less than 5', 3),
            Token(TokenType.RIGHT_BRACE, '}', None, 4),
            Token(TokenType.EOF, '', None, 4)
        ]
        self.assertEqual(expected_tokens, scanner.scan_tokens())

    def test_scan_tokens_book_example(self):
        scanner = Scanner(
            '// this is a comment\n'
            '(( )){} // grouping stuff\n'
            '!*+-/=<> <= == // operators\n'
        )
        expected_tokens = [
            Token(TokenType.LEFT_PAREN, '(', None, 2),
            Token(TokenType.LEFT_PAREN, '(', None, 2),
            Token(TokenType.RIGHT_PAREN, ')', None, 2),
            Token(TokenType.RIGHT_PAREN, ')', None, 2),
            Token(TokenType.LEFT_BRACE, '{', None, 2),
            Token(TokenType.RIGHT_BRACE, '}', None, 2),
            Token(TokenType.BANG, '!', None, 3),
            Token(TokenType.STAR, '*', None, 3),
            Token(TokenType.PLUS, '+', None, 3),
            Token(TokenType.MINUS, '-', None, 3),
            Token(TokenType.SLASH, '/', None, 3),
            Token(TokenType.EQUAL, '=', None, 3),
            Token(TokenType.LESS, '<', None, 3),
            Token(TokenType.GREATER, '>', None, 3),
            Token(TokenType.LESS_EQUAL, '<=', None, 3),
            Token(TokenType.EQUAL_EQUAL, '==', None, 3),
            Token(TokenType.EOF, '', None, 4)
        ]
        self.assertEqual(expected_tokens, scanner.scan_tokens())

    def test_scan_tokens_handles_string_literals(self):
        scanner = Scanner('"hello" != "@world"')
        expected_tokens = [
            Token(TokenType.STRING, '"hello"', 'hello', 1),
            Token(TokenType.BANG_EQUAL, '!=', None, 1),
            Token(TokenType.STRING, '"@world"', '@world', 1),
            Token(TokenType.EOF, '', None, 1)
        ]
        self.assertEqual(expected_tokens, scanner.scan_tokens())

    def test_scan_tokens_handles_number_literals(self):
        scanner = Scanner('3.14159 < 2.71828')
        expected_tokens = [
            Token(TokenType.NUMBER, '3.14159', 3.14159, 1),
            Token(TokenType.LESS, '<', None, 1),
            Token(TokenType.NUMBER, '2.71828', 2.71828, 1),
            Token(TokenType.EOF, '', None, 1)
        ]
        self.assertEqual(expected_tokens, scanner.scan_tokens())

    def test_scan_tokens_handles_identifiers(self):
        scanner = Scanner('orchid5 == pretty_flower')
        expected_tokens = [
            Token(TokenType.IDENTIFIER, 'orchid5', None, 1),
            Token(TokenType.EQUAL_EQUAL, '==', None, 1),
            Token(TokenType.IDENTIFIER, 'pretty_flower', None, 1),
            Token(TokenType.EOF, '', None, 1)
        ]
        self.assertEqual(expected_tokens, scanner.scan_tokens())

    def test_scan_tokens_handles_keywords(self):
        scanner = Scanner('and')
        expected_tokens = [
            Token(TokenType.AND, 'and', None, 1),
            Token(TokenType.EOF, '', None, 1)
        ]
        self.assertEqual(expected_tokens, scanner.scan_tokens())


if __name__ == '__main__':
    unittest.main()
