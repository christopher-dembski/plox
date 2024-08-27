import unittest
from tests.test_helpers.test_case_with_helpers import TestCaseWithHelpers


class TestInterpretValidSingleStatement(TestCaseWithHelpers):

    # literals

    def test_true_literal(self):
        self.assert_print_expression('true', 'true')

    def test_false_literal(self):
        self.assert_print_expression('false', 'false')

    def test_nil_literal(self):
        self.assert_print_expression('nil', 'nil')

    def test_number_literal_integer(self):
        # represented as a float internally, but the .0 should not be printed
        self.assert_print_expression('55', '55')

    def test_number_literal_decimal(self):
        self.assert_print_expression('6.125', '6.125')

    def test_string_literal(self):
        self.assert_print_expression('"hello world"', 'hello world')

    # numeric operators

    def test_addition(self):
        self.assert_print_expression('5 + 3', '8')

    def test_subtraction(self):
        self.assert_print_expression('15 - 1', '14')

    def test_multiplication(self):
        self.assert_print_expression('10 * 10', '100')

    def test_division(self):
        # should not print .0
        self.assert_print_expression('10 / 5', '2')

    def test_division_fractional(self):
        self.assert_print_expression('1 / 2', '0.5')

    # unary operators

    def test_negative(self):
        self.assert_print_expression('-1', '-1')

    def test_not_true(self):
        self.assert_print_expression('!true', 'false')

    def test_not_false(self):
        self.assert_print_expression('!false', 'true')

    def test_negation_non_boolean(self):
        self.assert_print_expression('!1', 'false')
        self.assert_print_expression('!0', 'false')
        self.assert_print_expression('!"hello"', 'false')
        self.assert_print_expression('!nil', 'true')

    def test_double_negation(self):
        self.assert_print_expression('!!true', 'true')
        self.assert_print_expression('!!false', 'false')

    def test_triple_negation(self):
        self.assert_print_expression('!!!true', 'false')
        self.assert_print_expression('!!!false', 'true')

    # comparison

    def test_greater_than_true(self):
        self.assert_print_expression('2 > 1', 'true')

    def test_greater_than_false(self):
        self.assert_print_expression('2 > 3', 'false')
        self.assert_print_expression('2 > 2', 'false')

    def test_greater_than_equal_true(self):
        self.assert_print_expression('2 >= 1', 'true')
        self.assert_print_expression('2 >= 2', 'true')

    def test_greater_than_equal_false(self):
        self.assert_print_expression('2 >= 3', 'false')

    def test_less_than_true(self):
        self.assert_print_expression('1 < 2', 'true')

    def test_less_than_false(self):
        self.assert_print_expression('3 < 2', 'false')
        self.assert_print_expression('2 < 2', 'false')

    def test_less_than_equal_true(self):
        self.assert_print_expression('1 <= 2', 'true')
        self.assert_print_expression('2 <= 2', 'true')

    def test_less_than_equal_false(self):
        self.assert_print_expression('3 <= 2', 'false')

    # equality

    def test_double_equals_number_true(self):
        self.assert_print_expression('1 == 1', 'true')

    def test_double_equals_number_false(self):
        self.assert_print_expression('1 == 2', 'false')

    def test_double_equals_string_true(self):
        self.assert_print_expression('"hello" == "hello"', 'true')

    def test_double_equals_string_false(self):
        self.assert_print_expression('"hello" == "world"', 'false')

    def test_double_equals_nil(self):
        self.assert_print_expression('nil == nil', 'true')

    def test_double_equals_mixed_types(self):
        self.assert_print_expression('6 == "hello"', 'false')
        self.assert_print_expression('nil == false', 'false')
        self.assert_print_expression('true == 5', 'false')

    def test_bang_equals_number_true(self):
        self.assert_print_expression('1 != 1', 'false')

    def test_bang_equals_number_false(self):
        self.assert_print_expression('1 != 2', 'true')

    def test_bang_equals_string_true(self):
        self.assert_print_expression('"hello" != "hello"', 'false')

    def test_bang_equals_string_false(self):
        self.assert_print_expression('"hello" != "world"', 'true')

    def test_bang_equals_nil(self):
        self.assert_print_expression('nil != nil', 'false')

    def test_bang_equals_mixed_types(self):
        self.assert_print_expression('6 != "hello"', 'true')
        self.assert_print_expression('nil != false', 'true')
        self.assert_print_expression('true != 5', 'true')

    # grouping

    def test_single_grouping(self):
        self.assert_print_expression('4 * (1 + 2)', '12')

    def test_redundant_grouping(self):
        self.assert_print_expression('(1 + 2)', '3')

    def test_double_grouping(self):
        self.assert_print_expression('(1 + 2) * (5 + 0)', '15')

    def test_nested_grouping(self):
        self.assert_print_expression('3 + (5 + (2 * 1))', '10')

    # test complex expressions

    def test_complex_espression_1(self):
        self.assert_print_expression('!(5 / (-6.0 * 1) >= 0.0)', 'true')


if __name__ == '__main__':
    unittest.main()
