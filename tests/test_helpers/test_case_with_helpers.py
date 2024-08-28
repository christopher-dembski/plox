import unittest
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from typing import List

from lox import Lox  # lox import must be above interpreter import to avoid circular import
from ast_printer import AstPrinter
from expr import Expr
from interpreter import Interpreter
from environment import Environment
from stmt import Stmt


class TestCaseWithHelpers(unittest.TestCase):

    def setUp(self):
        Lox.HAD_PARSER_ERROR = False
        Lox.HAD_RUNTIME_EXCEPTION = False
        Interpreter.ENVIRONMENT = Environment()

    def assert_prints(self, source: str, expcted_std_out: str | List[str]):
        if type(expcted_std_out) is list:
            expcted_std_out = '\n'.join(expcted_std_out)
        with redirect_stdout(StringIO()) as std_out:
            with redirect_stderr(StringIO()) as std_err:
                Lox.run(source)
        self.assertEqual(
            expcted_std_out,
            std_out.getvalue().rstrip('\n'),
            'Incorrect values printed to std_out.'
        )
        self.assertEqual(
            '',
            std_err.getvalue().rstrip('\n'),
            "Expected no error to be printed to std_err."
        )

    def assert_prints_to_std_err(self, source: str):
        with redirect_stderr(StringIO()) as std_err:
            Lox.run(source)
        self.assertTrue(std_err.getvalue(), msg='Expected error to be printed to std_err.')

    def assert_print_expression(self, source: str, expcted_std_out: str):
        self.assert_prints(f'print {source};', expcted_std_out)

    def assert_expression_prints_to_std_err(self, source: str):
        self.assert_prints_to_std_err(f'print {source};')

    @staticmethod
    def build(ast: Expr | Stmt) -> str:
        return AstPrinter().build_ast_string(ast)
