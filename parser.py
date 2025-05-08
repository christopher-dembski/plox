from typing import Sequence, List

import stmt
from lox_token import Token, TokenType
from expr import Expr, BinaryExpr, UnaryExpr, LiteralExpr, GroupingExpr, VariableExpr, AssignmentExpr, LogicalExpr, \
    CallExpr, GetExpr, ThisExpr, SetExpr, SuperExpr
from stmt import Stmt, PrintStmt, ExpressionStmt, VarStmt, BlockStmt, IfStmt, WhileStmt, FunctionStmt, ReturnStmt


class ParserError(Exception):
    pass


class Parser:
    MAX_ARGUMENTS = 255

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

    def __init__(self, tokens: Sequence[Token], lox):
        self.tokens = tokens
        self.current = 0
        self.lox = lox

    def parse(self) -> Sequence[Stmt]:
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements

    def expression(self) -> Expr:
        return self.assignment()

    def declaration(self) -> Stmt:
        try:
            if self.match(TokenType.CLASS):
                return self.class_declaration()
            if self.match(TokenType.FUN):
                return self.function_declaration("function")
            if self.match(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except ParserError:
            self.synchronize()

    def statement(self) -> Stmt:
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.FOR):
            return self.for_statement()
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.RETURN):
            return self.return_statement()
        if self.match(TokenType.LEFT_BRACE):
            return self.block_statement()
        return self.expression_statement()

    def print_statement(self) -> PrintStmt:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return PrintStmt(value)

    def return_statement(self) -> ReturnStmt:
        keyword = self.previous()
        value = None if self.check(TokenType.SEMICOLON) else self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return ReturnStmt(keyword, value)

    def if_statement(self) -> IfStmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' atfer if.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if statement condition.")
        if_branch = self.statement()
        else_branch = self.statement() if self.match(TokenType.ELSE) else None
        return IfStmt(condition, if_branch, else_branch)

    def while_statement(self) -> WhileStmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' before while statement condition.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after while statement condition.")
        body = self.statement()
        return WhileStmt(condition, body)

    def for_statement(self) -> WhileStmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after for keyword.")
        initializer = None if self.match(TokenType.SEMICOLON) \
            else self.var_declaration() if self.match(TokenType.VAR) \
            else self.expression_statement()
        condition = None if self.check(TokenType.SEMICOLON) else self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after for loop condition.")
        increment = None if self.check(TokenType.RIGHT_PAREN) else self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")
        body = self.statement()
        return Parser.desuagar_for_statement(initializer, condition, increment, body)

    @staticmethod
    def desuagar_for_statement(initializer: VarStmt | ExpressionStmt, condition: Expr, increment: Expr,
                               body: Stmt) -> WhileStmt:
        if increment is not None:
            body = BlockStmt((body, ExpressionStmt(increment)))
        if condition is None:
            condition = LiteralExpr(True)
        body = WhileStmt(condition, body)
        if initializer is not None:
            body = BlockStmt((initializer, body))
        return body

    def block_statement(self) -> BlockStmt:
        statements = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return BlockStmt(statements)

    def var_declaration(self) -> VarStmt:
        name = self.consume(TokenType.IDENTIFIER, "Expected identifier after var.")
        initializer = self.expression() if self.match(TokenType.EQUAL) else None
        self.consume(TokenType.SEMICOLON, "Expect ';' after declaration.")
        return VarStmt(name, initializer)

    def function_declaration(self, kind: str) -> FunctionStmt:
        name = self.consume(TokenType.IDENTIFIER, f"Expect {kind} name.")
        self.consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")
        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            first_iteration = True
            while first_iteration or self.match(TokenType.COMMA):
                first_iteration = False
                if len(parameters) >= Parser.MAX_ARGUMENTS:
                    self.error(self.peek(), f"Can't have more than {Parser.MAX_ARGUMENTS} parameters.")
                parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name."))
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")
        self.consume(TokenType.LEFT_BRACE, f"Expect '{{' befoe {kind} body.")
        body = self.block_statement()
        return FunctionStmt(name, parameters, body)

    def class_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect class name.")
        superclass = None
        if self.match(TokenType.LESS):
            self.consume(TokenType.IDENTIFIER, "Expect superclass name.")
            superclass = VariableExpr(self.previous())
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before class body.")
        methods: List[FunctionStmt] = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            methods.append(self.function_declaration("method"))
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after class body.")
        return stmt.ClassStmt(name, superclass, methods)

    def expression_statement(self) -> ExpressionStmt:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return ExpressionStmt(value)

    def assignment(self) -> Expr:
        expr = self.logical_or()
        if self.match(TokenType.EQUAL):
            value = self.assignment()
            if type(expr) is VariableExpr:
                # we know expr is of type VariableExpr and has a name attribute
                return AssignmentExpr(expr.name, value)
            elif type(expr) is GetExpr:
                # we know expr is of type GetExpr and has obj and name attributes
                return SetExpr(expr.obj, expr.name, value)
            equals_token = self.previous()
            self.lox.error_from_token(equals_token, 'Identifier expected.')
        return expr

    def equality(self) -> Expr:
        expr = self.comparison()
        while self.match(*Parser.EQUALITY_OPERATORS):
            expr = BinaryExpr(left=expr, operator=self.previous(), right=self.comparison())
        return expr

    def logical_or(self) -> Expr:
        expr = self.logical_and()
        while self.match(TokenType.OR):
            expr = LogicalExpr(left=expr, operator=self.previous(), right=self.logical_and())
        return expr

    def logical_and(self) -> Expr:
        expr = self.equality()
        while self.match(TokenType.AND):
            expr = LogicalExpr(left=expr, operator=self.previous(), right=self.equality())
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
        return self.call()

    def call(self) -> Expr:
        expr = self.primary()
        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finish_call(expr)
            elif self.match(TokenType.DOT):
                name = self.consume(TokenType.IDENTIFIER, "Expect property name after '.'.")
                expr = GetExpr(expr, name)
            else:
                break
        return expr

    def finish_call(self, callee: Expr) -> Expr:
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(arguments) >= Parser.MAX_ARGUMENTS:
                    self.error(
                        self.peek(),
                        f"Exceeded maximum number of arguments for function call. "
                        f"The maximum number of arguments is {Parser.MAX_ARGUMENTS}."
                    )
                arguments.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break
        paren = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after argument list.")
        return CallExpr(callee, paren, arguments)

    def primary(self) -> Expr:
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpr(self.previous().literal)
        if self.match(TokenType.SUPER):
            keyword = self.previous()
            self.consume(TokenType.DOT, "Expect '.' after super.")
            method = self.consume(TokenType.IDENTIFIER, "Expect superclass method name.")
            return SuperExpr(keyword, method)
        if self.match(TokenType.THIS):
            return ThisExpr(self.previous())
        if self.match(TokenType.IDENTIFIER):
            return VariableExpr(self.previous())
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
        raise self.error(self.peek(), "Expect expression.")

    def consume(self, token_type: TokenType, message: str) -> Token:
        if self.check(token_type):
            return self.advance()
        raise self.error(self.peek(), message)

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
            if self.previous().type == TokenType.SEMICOLON or self.peek().type in Parser.TERMINATE_SYNCHRONIZE_TOKEN_TYPES:
                return
            self.advance()

    def error(self, token: Token, messge: str) -> ParserError:
        self.lox.error_from_token(token, messge)
        return ParserError()
