"""Tests for mathutils package."""

import unittest

from python.libs.mathutils.operations import add, subtract, multiply, divide, power, factorial
from python.libs.mathutils.stats import mean, median, variance, standard_deviation


class TestOperations(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertAlmostEqual(add(0.1, 0.2), 0.3, places=10)

    def test_subtract(self):
        self.assertEqual(subtract(10, 4), 6)
        self.assertEqual(subtract(3, 5), -2)

    def test_multiply(self):
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(multiply(-2, 3), -6)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        self.assertAlmostEqual(divide(1, 3), 0.333333, places=5)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            divide(1, 0)

    def test_power(self):
        self.assertEqual(power(2, 10), 1024)
        self.assertEqual(power(3, 0), 1)

    def test_factorial(self):
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(6), 720)

    def test_factorial_negative(self):
        with self.assertRaises(ValueError):
            factorial(-1)


class TestStats(unittest.TestCase):
    def test_mean(self):
        self.assertEqual(mean([1, 2, 3, 4, 5]), 3.0)
        self.assertAlmostEqual(mean([1.5, 2.5, 3.5]), 2.5)

    def test_mean_empty(self):
        with self.assertRaises(ValueError):
            mean([])

    def test_median_odd(self):
        self.assertEqual(median([1, 3, 5]), 3)
        self.assertEqual(median([5, 1, 3]), 3)

    def test_median_even(self):
        self.assertEqual(median([1, 2, 3, 4]), 2.5)

    def test_variance(self):
        self.assertAlmostEqual(variance([2, 4, 4, 4, 5, 5, 7, 9]), 4.0, places=1)

    def test_standard_deviation(self):
        vals = [2, 4, 4, 4, 5, 5, 7, 9]
        self.assertAlmostEqual(standard_deviation(vals), variance(vals) ** 0.5)


if __name__ == "__main__":
    unittest.main()
