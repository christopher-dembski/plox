import unittest
from tests.test_helpers.test_case_with_helpers import TestCaseWithHelpers


class TestInterpretValidSingleStatement(TestCaseWithHelpers):

    # literals

    def test_true_literal(self):
        self.assert_prints('true', 'true')

    def test_false_literal(self):
        self.assert_prints('false', 'false')

    def test_nil_literal(self):
        self.assert_prints('nil', 'nil')

    def test_number_literal_integer(self):
        # represented as a float internally, but the .0 should not be printed
        self.assert_prints('55', '55')

    def test_number_literal_decimal(self):
        self.assert_prints('6.125', '6.125')

    def test_string_literal(self):
        self.assert_prints('"hello world"', 'hello world')

    # numeric operators

    def test_addition(self):
        self.assert_prints('5 + 3', '8')

    def test_subtraction(self):
        self.assert_prints('15 - 1', '14')

    def test_multiplication(self):
        self.assert_prints('10 * 10', '100')

    def test_division(self):
        # should not print .0
        self.assert_prints('10 / 5', '2')

    def test_division_fractional(self):
        self.assert_prints('1 / 2', '0.5')

    # unary operators

    def test_negative(self):
        self.assert_prints('-1', '-1')

    def test_not_true(self):
        self.assert_prints('!true', 'false')

    def test_not_false(self):
        self.assert_prints('!false', 'true')

    def test_negation_non_boolean(self):
        self.assert_prints('!1', 'false')
        self.assert_prints('!0', 'false')
        self.assert_prints('!"hello"', 'false')
        self.assert_prints('!nil', 'true')

    def test_double_negation(self):
        self.assert_prints('!!true', 'true')
        self.assert_prints('!!false', 'false')

    def test_triple_negation(self):
        self.assert_prints('!!!true', 'false')
        self.assert_prints('!!!false', 'true')

    # comparison

    def test_greater_than_true(self):
        self.assert_prints('2 > 1', 'true')

    def test_greater_than_false(self):
        self.assert_prints('2 > 3', 'false')
        self.assert_prints('2 > 2', 'false')

    def test_greater_than_equal_true(self):
        self.assert_prints('2 >= 1', 'true')
        self.assert_prints('2 >= 2', 'true')

    def test_greater_than_equal_false(self):
        self.assert_prints('2 >= 3', 'false')

    def test_less_than_true(self):
        self.assert_prints('1 < 2', 'true')

    def test_less_than_false(self):
        self.assert_prints('3 < 2', 'false')
        self.assert_prints('2 < 2', 'false')

    def test_less_than_equal_true(self):
        self.assert_prints('1 <= 2', 'true')
        self.assert_prints('2 <= 2', 'true')

    def test_less_than_equal_false(self):
        self.assert_prints('3 <= 2', 'false')

    # equality

    def test_double_equals_number_true(self):
        self.assert_prints('1 == 1', 'true')

    def test_double_equals_number_false(self):
        self.assert_prints('1 == 2', 'false')

    def test_double_equals_string_true(self):
        self.assert_prints('"hello" == "hello"', 'true')

    def test_double_equals_string_false(self):
        self.assert_prints('"hello" == "world"', 'false')

    def test_double_equals_nil(self):
        self.assert_prints('nil == nil', 'true')

    def test_double_equals_mixed_types(self):
        self.assert_prints('6 == "hello"', 'false')
        self.assert_prints('nil == false', 'false')
        self.assert_prints('true == 5', 'false')

    def test_bang_equals_number_true(self):
        self.assert_prints('1 != 1', 'false')

    def test_bang_equals_number_false(self):
        self.assert_prints('1 != 2', 'true')

    def test_bang_equals_string_true(self):
        self.assert_prints('"hello" != "hello"', 'false')

    def test_bang_equals_string_false(self):
        self.assert_prints('"hello" != "world"', 'true')

    def test_bang_equals_nil(self):
        self.assert_prints('nil != nil', 'false')

    def test_bang_equals_mixed_types(self):
        self.assert_prints('6 != "hello"', 'true')
        self.assert_prints('nil != false', 'true')
        self.assert_prints('true != 5', 'true')

    # grouping

    def test_single_grouping(self):
        self.assert_prints('4 * (1 + 2)', '12')

    def test_redundant_grouping(self):
        self.assert_prints('(1 + 2)', '3')

    def test_double_grouping(self):
        self.assert_prints('(1 + 2) * (5 + 0)', '15')

    def test_nested_grouping(self):
        self.assert_prints('3 + (5 + (2 * 1))', '10')

    # test complex expressions

    def test_complex_espression_1(self):
        self.assert_prints('!(5 / (-6.0 * 1) >= 0.0)', 'true')


if __name__ == '__main__':
    unittest.main()
