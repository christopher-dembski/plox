import unittest
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO

from lox import Lox


class TestCaseWithHelpers(unittest.TestCase):

    def setUp(self):
        Lox.HAD_PARSER_ERROR = False
        Lox.HAD_RUNTIME_EXCEPTION = False

    def assert_prints(self, source: str, expcted_std_out: str):
        with redirect_stdout(StringIO()) as std_out:
            with redirect_stderr(StringIO()) as std_err:
                Lox.run(source)
        self.assertEqual(expcted_std_out, std_out.getvalue().rstrip('\n'))
        self.assertEqual('', std_err.getvalue().rstrip('\n'))

    def assert_prints_to_std_err(self, source: str):
        with redirect_stderr(StringIO()) as std_err:
            Lox.run(source)
        self.assertTrue(std_err.getvalue(), msg='Expected error to be printed to std_err.')
