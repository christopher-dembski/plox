from typing import Sequence

from token_type import TokenType
from lox_token import Token
from expr import ExprVisitor, Expr, LiteralExpr, GroupingExpr, UnaryExpr, BinaryExpr, VariableExpr, AssignmentExpr, \
    LogicalExpr
from stmt import StmtVisitor, Stmt, ExpressionStmt, PrintStmt, VarStmt, BlockStmt, IfStmt, WhileStmt
from environment import Environment
from runtime_exception import RuntimeException


class Interpreter(ExprVisitor, StmtVisitor):

    def __init__(self, lox):
        self.lox = lox
        self.environment = Environment()

    def interpret(self, stmts: Sequence[Stmt]) -> None:
        try:
            for stmt in stmts:
                self.execute(stmt)
        except RuntimeException as exception:
            self.lox.runtime_exception(exception)

    def execute(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def evaluate(self, expr: Expr) -> object:
        return expr.accept(self)

    def visit_literal_expr(self, expr: LiteralExpr) -> object:
        return expr.value

    def visit_grouping_expr(self, expr: GroupingExpr) -> object:
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: UnaryExpr) -> object:
        operator = expr.operator
        operand = self.evaluate(expr.right)
        match operator.type:
            case TokenType.MINUS:
                Interpreter.check_number_operand(operator, operand)
                return -operand
            case TokenType.BANG:
                return not Interpreter.is_truthy(operand)
            case _:
                raise AssertionError('This case should not be reachable. Invalid operator for unary expression.')

    def visit_binary_expr(self, expr: BinaryExpr) -> object:
        operator = expr.operator
        left_operand = self.evaluate(expr.left)
        right_operand = self.evaluate(expr.right)

        match operator.type:
            case TokenType.PLUS:
                Interpreter.validate_addition_operands(operator, left_operand, right_operand)
                return left_operand + right_operand
            case TokenType.MINUS:
                Interpreter.check_number_operands(operator, left_operand, right_operand)
                return left_operand - right_operand
            case TokenType.STAR:
                Interpreter.check_number_operands(operator, left_operand, right_operand)
                return left_operand * right_operand
            case TokenType.SLASH:
                Interpreter.check_number_operands(operator, left_operand, right_operand)
                return left_operand / right_operand
            case TokenType.GREATER:
                Interpreter.check_number_operands(operator, left_operand, right_operand)
                return left_operand > right_operand
            case TokenType.GREATER_EQUAL:
                Interpreter.check_number_operands(operator, left_operand, right_operand)
                return left_operand >= right_operand
            case TokenType.LESS:
                Interpreter.check_number_operands(operator, left_operand, right_operand)
                return left_operand < right_operand
            case TokenType.LESS_EQUAL:
                Interpreter.check_number_operands(operator, left_operand, right_operand)
                return left_operand <= right_operand
            case TokenType.EQUAL_EQUAL:
                return Interpreter.is_equal(left_operand, right_operand)
            case TokenType.BANG_EQUAL:
                return not Interpreter.is_equal(left_operand, right_operand)
            case _:
                raise AssertionError('This case should not be reachable. Invalid operator for binary exression.')

    def visit_logical_expr(self, expr: LogicalExpr) -> object:
        left = self.evaluate(expr.left)
        if expr.operator.type == TokenType.OR:
            return left if Interpreter.is_truthy(left) else self.evaluate(expr.right)
        if expr.operator.type == TokenType.AND:
            return left if not Interpreter.is_truthy(left) else self.evaluate(expr.right)
        raise AssertionError('This case should not be reachable. Invalid operator for logical expression.')

    def visit_expression_stmt(self, stmt: ExpressionStmt) -> None:
        self.evaluate(stmt.expression)

    def visit_if_stmt(self, stmt: IfStmt) -> None:
        if Interpreter.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.if_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

    def visit_while_stmt(self, stmt: WhileStmt) -> None:
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    def visit_print_stmt(self, stmt: PrintStmt) -> None:
        value = self.evaluate(stmt.expression)
        print(self.stringify_value(value))

    def visit_block_stmt(self, stmt: BlockStmt) -> None:
        previous_environment = self.environment
        self.environment = Environment(previous_environment)
        try:
            for statement in stmt.statements:
                statement.accept(self)
        finally:
            self.environment = previous_environment

    def visit_var_stmt(self, stmt: VarStmt) -> None:
        value = self.evaluate(stmt.initializer) if stmt.initializer else None
        self.environment.define(stmt.name.lexeme, value)

    def visit_assignment_expr(self, expr: AssignmentExpr) -> object:
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visit_variable_expr(self, expr: VariableExpr) -> object:
        return self.environment.get(expr.name)

    @staticmethod
    def is_truthy(value: object) -> bool:
        return value is not None and value is not False

    @staticmethod
    def is_equal(value_a: object, value_b: object) -> bool:
        # like Lox, Python does not perform implicit conversion, so we can use '==' to test equality
        return value_a == value_b

    @staticmethod
    def check_number_operand(operator: Token, operand: object) -> None:
        if type(operand) is not float:
            raise RuntimeException(operator, 'Operand must be a number.')

    @staticmethod
    def check_number_operands(operator: Token, operand_a: object, operand_b) -> None:
        if type(operand_a) is not float or type(operand_b) is not float:
            raise RuntimeException(operator, 'Operands must be numbers.')

    @staticmethod
    def validate_addition_operands(operator: Token, operand_a: object, operand_b: object):
        both_floats = type(operand_a) is float and type(operand_b) is float
        both_strings = type(operand_a) is str and type(operand_b) is str
        if not (both_floats or both_strings):
            raise RuntimeException(operator, 'Operands must both be numbers or both be strings.')

    @staticmethod
    def stringify_value(value: object) -> str:
        if type(value) is float:
            float_string = str(value)
            if float_string.endswith('.0'):
                return float_string[:-2]
            return float_string
        elif type(value) is str:
            # calling str on value to silence type warning
            return str(value)
        elif type(value) is bool:
            return 'true' if value else 'false'
        elif value is None:
            return 'nil'
