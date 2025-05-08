from enum import Enum, auto
from typing import Iterable, Dict, List
from expr import ExprVisitor, Expr, VariableExpr, AssignmentExpr, BinaryExpr, CallExpr, GroupingExpr, LiteralExpr, \
    LogicalExpr, UnaryExpr, GetExpr, ThisExpr, SetExpr
from lox_token import Token
from stmt import StmtVisitor, Stmt, BlockStmt, VarStmt, FunctionStmt, ExpressionStmt, IfStmt, PrintStmt, ReturnStmt, \
    WhileStmt, ClassStmt

Scope = Dict[str, bool]


class Resolver(ExprVisitor, StmtVisitor):
    class FunctionType(Enum):
        NONE = auto()
        FUNCTION = auto()
        METHOD = auto()

    class ClassType(Enum):
        NONE = auto()
        CLASS = auto()

    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes: List[Scope] = []
        self.current_function: Resolver.FunctionType = Resolver.FunctionType.NONE
        self.current_class = Resolver.ClassType.NONE

    def visit_block_stmt(self, stmt: BlockStmt):
        self.begin_scope()
        self.resolve_stmts(stmt.statements)
        self.end_scope()

    def visit_class_stmt(self, stmt: ClassStmt):
        enclosing_class = self.current_class
        self.current_class = Resolver.ClassType.CLASS
        self.declare(stmt.name)
        self.define(stmt.name)
        self.begin_scope()
        self.scopes[-1]["this"] = True
        for method in stmt.methods:
            declaration = Resolver.FunctionType.METHOD
            self.resolve_function(method, declaration)
        self.end_scope()
        self.current_class = enclosing_class

    def visit_expression_stmt(self, stmt: ExpressionStmt):
        self.resolve_expr(stmt.expression)

    def visit_function_stmt(self, stmt: FunctionStmt):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt, Resolver.FunctionType.FUNCTION)

    def visit_if_stmt(self, stmt: IfStmt):
        self.resolve_expr(stmt.condition)
        self.resolve_stmt(stmt.if_branch)
        if stmt.else_branch is not None:
            self.resolve_stmt(stmt.else_branch)

    def visit_print_stmt(self, stmt: PrintStmt):
        self.resolve_expr(stmt.expression)

    def visit_return_stmt(self, stmt: ReturnStmt):
        if self.current_function == Resolver.FunctionType.NONE:
            self.interpreter.lox.error_from_token(stmt.keyword, "Can't return from top-level code.")
        if stmt.value is not None:
            self.resolve_expr(stmt.value)

    def visit_var_stmt(self, stmt: VarStmt):
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve_expr(stmt.initializer)
        self.define(stmt.name)

    def visit_while_stmt(self, stmt: WhileStmt):
        self.resolve_expr(stmt.condition)
        self.resolve_stmt(stmt.body)

    def visit_assignment_expr(self, expr: AssignmentExpr):
        self.resolve_expr(expr.value)
        self.resolve_local(expr, expr.name)

    def visit_binary_expr(self, expr: BinaryExpr):
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)

    def visit_call_expr(self, expr: CallExpr):
        self.resolve_expr(expr.callee)
        for argument in expr.arguments:
            self.resolve_expr(argument)

    def visit_get_expr(self, expr: GetExpr):
        self.resolve_expr(expr.obj)

    def visit_this_expr(self, expr: ThisExpr):
        if self.current_class == Resolver.ClassType.NONE:
            self.interpreter.lox.error_from_token(expr.keyword, "Can't use 'this' outside of a class.")
            return
        self.resolve_local(expr, expr.keyword)

    def visit_grouping_expr(self, expr: GroupingExpr):
        self.resolve_expr(expr.expression)

    def visit_literal_expr(self, expr: LiteralExpr):
        # deliberately take no action
        pass

    def visit_logical_expr(self, expr: LogicalExpr):
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)

    def visit_set_expr(self, expr: SetExpr):
        self.resolve_expr(expr.value)
        self.resolve_expr(expr.obj)

    def visit_unary_expr(self, expr: UnaryExpr):
        self.resolve_expr(expr.right)

    def visit_variable_expr(self, expr: VariableExpr):
        if len(self.scopes) > 0 and self.scopes[-1].get(expr.name.lexeme, None) is False:
            self.interpreter.lox.error_from_token(expr.name, "Can't read local variable in its own initializer.")
        self.resolve_local(expr, expr.name)

    def resolve_stmts(self, statements: Iterable[Stmt]):
        for statement in statements:
            self.resolve_stmt(statement)

    def resolve_stmt(self, stmt: Stmt):
        stmt.accept(self)

    def resolve_expr(self, expr: Expr):
        expr.accept(self)

    def resolve_function(self, function: FunctionStmt, function_type: FunctionType):
        enclosing_function = self.current_function
        self.current_function = function_type
        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve_stmts(function.body.statements)
        self.end_scope()
        self.current_function = enclosing_function

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name: Token):
        if len(self.scopes) == 0:
            return
        scope: Scope = self.scopes[-1]
        if name.lexeme in scope:
            self.interpreter.lox.error_from_token(name, "Already a variable with this name in this scope.")
        scope[name.lexeme] = False

    def define(self, name: Token):
        if len(self.scopes) == 0:
            return
        scope: Scope = self.scopes[-1]
        scope[name.lexeme] = True

    def resolve_local(self, expr: Expr, name: Token):
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return
