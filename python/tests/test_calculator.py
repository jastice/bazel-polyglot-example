"""Tests for calculator service."""

import unittest

from python.services.calculator.engine import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_basic_operations(self):
        self.assertEqual(self.calc.compute_add(2, 3), 5)
        self.assertEqual(self.calc.compute_subtract(10, 4), 6)
        self.assertEqual(self.calc.compute_multiply(3, 7), 21)
        self.assertEqual(self.calc.compute_divide(15, 3), 5)

    def test_power_and_factorial(self):
        self.assertEqual(self.calc.compute_power(2, 8), 256)
        self.assertEqual(self.calc.compute_factorial(5), 120)

    def test_history(self):
        self.calc.compute_add(1, 2)
        self.calc.compute_multiply(3, 4)
        self.assertEqual(len(self.calc.history), 2)
        self.assertEqual(self.calc.history[0], ("1 + 2", 3))
        self.assertEqual(self.calc.history[1], ("3 * 4", 12))

    def test_clear_history(self):
        self.calc.compute_add(1, 1)
        self.calc.clear_history()
        self.assertEqual(len(self.calc.history), 0)

    def test_batch_compute(self):
        results = self.calc.batch_compute([1, 2, 3, 4], "add")
        self.assertEqual(results.values, [3, 5, 7])

    def test_history_table(self):
        self.calc.compute_add(10, 20)
        table = self.calc.history_table()
        self.assertIn("10 + 20", table)
        self.assertIn("30.0000", table)

    def test_statistics_summary(self):
        summary = self.calc.statistics_summary([10, 20, 30, 40, 50])
        self.assertIn("Mean", summary)
        self.assertIn("Median", summary)


if __name__ == "__main__":
    unittest.main()
