from typing import Sequence

from lox import Lox
from lox_token import Token
from token_type import TokenType


class Scanner:
    KEYWORD_TOKEN_TYPES = {
        'and': TokenType.AND,
        'class': TokenType.CLASS,
        'else': TokenType.ELSE,
        'false': TokenType.FALSE,
        'for': TokenType.FOR,
        'fun': TokenType.FUN,
        'if': TokenType.IF,
        'nil': TokenType.NIL,
        'or': TokenType.OR,
        'print': TokenType.PRINT,
        'return': TokenType.RETURN,
        'super': TokenType.SUPER,
        'this': TokenType.THIS,
        'true': TokenType.TRUE,
        'var': TokenType.VAR,
        'while': TokenType.WHILE,
    }

    def __init__(self, source: str):
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.tokens = []

    def scan_tokens(self) -> Sequence[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self) -> None:
        character = self.advance()
        match character:
            case '(':
                self.add_token(TokenType.LEFT_PAREN)
            case ')':
                self.add_token(TokenType.RIGHT_PAREN)
            case '{':
                self.add_token(TokenType.LEFT_BRACE)
            case '}':
                self.add_token(TokenType.RIGHT_BRACE)
            case ',':
                self.add_token(TokenType.COMMA)
            case '.':
                self.add_token(TokenType.DOT)
            case '-':
                self.add_token(TokenType.MINUS)
            case '+':
                self.add_token(TokenType.PLUS)
            case ';':
                self.add_token(TokenType.SEMICOLON)
            case '*':
                self.add_token(TokenType.STAR)
            case '!':
                self.add_token(TokenType.BANG_EQUAL if self.match_next('=') else TokenType.BANG)
            case '=':
                self.add_token(TokenType.EQUAL_EQUAL if self.match_next('=') else TokenType.EQUAL)
            case '<':
                self.add_token(TokenType.LESS_EQUAL if self.match_next('=') else TokenType.LESS)
            case '>':
                self.add_token(TokenType.GREATER_EQUAL if self.match_next('=') else TokenType.GREATER)
            case '/':
                if self.match_next('/'):
                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case ' ' | '\r' | '\t':
                pass
            case '\n':
                self.line += 1
            case '"':
                self.string()
            case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
                self.number()
            case _:
                if Scanner.is_alpha(character):
                    self.identifier()
                else:
                    Lox.error(self.line, '', 'Unexpected character.')

    def string(self) -> None:
        while self.peek() != '"':
            if self.is_at_end():
                Lox.error(self.line, '', 'Unterminated string literal.')
                return
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        self.advance()  # closing quote
        literal = self.source[self.start + 1:self.current - 1]  # trim opening/closing quotes
        self.add_token(TokenType.STRING, literal)

    def number(self) -> None:
        while Scanner.is_digit(self.peek()):
            self.advance()
        if self.peek() == '.' and Scanner.is_digit(self.peek_next()):
            self.advance()  # process the dot
            while Scanner.is_digit(self.peek()):
                self.advance()
        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def identifier(self) -> None:
        while Scanner.is_alpha_numeric(self.peek()):
            self.advance()
        text = self.source[self.start:self.current]
        token_type = Scanner.KEYWORD_TOKEN_TYPES.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)

    def match_next(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def add_token(self, token_type: TokenType, literal=None) -> None:
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def advance(self) -> str:
        current_index = self.current
        self.current += 1
        return self.source[current_index]

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def peek(self) -> str:
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    @staticmethod
    def is_digit(char: str) -> bool:
        return '0' <= char <= '9' or char == '.'

    @staticmethod
    def is_alpha(char: str) -> bool:
        return 'a' <= char <= 'z' or 'A' <= char <= 'Z' or char == '_'

    @staticmethod
    def is_alpha_numeric(char: str) -> bool:
        return Scanner.is_alpha(char) or Scanner.is_digit(char)
