from typing import Sequence

from lox_token import Token, TokenType
from expr import Expr, BinaryExpr, UnaryExpr, LiteralExpr, GroupingExpr


class ParserError(Exception):
    pass


class Parser:
    EQUALITY_OPERATORS = (TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL)
    COMPARISON_OPERATORS = (TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL)
    TERM_OPERATORS = (TokenType.PLUS, TokenType.MINUS)
    FACTOR_OPERATORS = (TokenType.STAR, TokenType.SLASH)
    UNARY_OPERATORS = (TokenType.MINUS, TokenType.BANG)

    TERMINATE_SYNCHRONIZE_TOKEN_TYPES = (
        TokenType.CLASS,
        TokenType.FOR,
        TokenType.FUN,
        TokenType.IF,
        TokenType.PRINT,
        TokenType.RETURN,
        TokenType.VAR,
        TokenType.WHILE
    )

    def __init__(self, tokens: Sequence[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        try:
            return self.expression()
        except ParserError:
            return None

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()
        while self.match(*Parser.EQUALITY_OPERATORS):
            expr = BinaryExpr(left=expr, operator=self.previous(), right=self.comparison())
        return expr

    def comparison(self) -> Expr:
        expr = self.term()
        while self.match(*Parser.COMPARISON_OPERATORS):
            expr = BinaryExpr(left=expr, operator=self.previous(), right=self.term())
        return expr

    def term(self) -> Expr:
        expr = self.factor()
        while self.match(*Parser.TERM_OPERATORS):
            expr = BinaryExpr(left=expr, operator=self.previous(), right=self.factor())
        return expr

    def factor(self) -> Expr:
        expr = self.unary()
        while self.match(*Parser.FACTOR_OPERATORS):
            expr = BinaryExpr(left=expr, operator=self.previous(), right=self.unary())
        return expr

    def unary(self) -> Expr:
        if self.match(*Parser.UNARY_OPERATORS):
            return UnaryExpr(operator=self.previous(), right=self.unary())
        return self.primary()

    def primary(self) -> Expr:
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpr(self.previous().literal)

        if self.match(TokenType.TRUE):
            return LiteralExpr(True)
        if self.match(TokenType.FALSE):
            return LiteralExpr(False)
        if self.match(TokenType.NIL):
            return LiteralExpr(None)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return GroupingExpr(expr)

        raise Parser.error(self.peek(), "Expect expression.")

    def consume(self, token_type: TokenType, message: str) -> Token:
        if self.check(token_type):
            return self.advance()
        raise Parser.error(self.peek(), message)

    def match(self, *token_types: TokenType) -> bool:
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def check(self, token_type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == token_type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON or self.peek() in Parser.TERMINATE_SYNCHRONIZE_TOKEN_TYPES:
                return
            self.advance()

    @staticmethod
    def error(token: Token, messge: str) -> ParserError:
        Lox.error_from_token(token, messge)
        return ParserError()

# avoid circular import
from lox import Lox
