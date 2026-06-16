"""Tests for datastructs package."""

import unittest

from python.libs.datastructs.collections import StatsList, FrequencyMap, Matrix


class TestStatsList(unittest.TestCase):
    def test_basic_stats(self):
        sl = StatsList([1, 2, 3, 4, 5])
        self.assertEqual(sl.sum, 15.0)
        self.assertEqual(sl.mean, 3.0)
        self.assertEqual(sl.median, 3.0)
        self.assertEqual(len(sl), 5)

    def test_append_extend(self):
        sl = StatsList()
        sl.append(10)
        sl.extend([20, 30])
        self.assertEqual(len(sl), 3)
        self.assertEqual(sl.sum, 60.0)

    def test_scaled(self):
        sl = StatsList([1, 2, 3])
        scaled = sl.scaled(2)
        self.assertEqual(scaled.values, [2, 4, 6])

    def test_normalized(self):
        sl = StatsList([10, 20, 30])
        norm = sl.normalized()
        self.assertAlmostEqual(norm.mean, 0.0, places=10)


class TestFrequencyMap(unittest.TestCase):
    def test_add_and_count(self):
        fm = FrequencyMap()
        fm.add("a")
        fm.add("b")
        fm.add("a")
        self.assertEqual(fm.count("a"), 2)
        self.assertEqual(fm.count("b"), 1)
        self.assertEqual(fm.count("c"), 0)

    def test_most_common(self):
        fm = FrequencyMap()
        fm.add("x", 5)
        fm.add("y", 3)
        fm.add("z", 8)
        top = fm.most_common(2)
        self.assertEqual(top[0][0], "z")
        self.assertEqual(top[1][0], "x")

    def test_frequency(self):
        fm = FrequencyMap()
        fm.add("a", 1)
        fm.add("b", 3)
        self.assertAlmostEqual(fm.frequency("a"), 0.25)


class TestMatrix(unittest.TestCase):
    def test_shape(self):
        m = Matrix([[1, 2], [3, 4], [5, 6]])
        self.assertEqual(m.shape, (3, 2))

    def test_row_means(self):
        m = Matrix([[1, 3], [2, 4]])
        self.assertEqual(m.row_means(), [2.0, 3.0])

    def test_add_matrix(self):
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[5, 6], [7, 8]])
        m3 = m1.add_matrix(m2)
        self.assertEqual(m3.get(0, 0), 6)
        self.assertEqual(m3.get(1, 1), 12)

    def test_scale(self):
        m = Matrix([[1, 2], [3, 4]])
        scaled = m.scale(3)
        self.assertEqual(scaled.get(0, 0), 3)
        self.assertEqual(scaled.get(1, 1), 12)

    def test_invalid_matrix(self):
        with self.assertRaises(ValueError):
            Matrix([[1, 2], [3]])


if __name__ == "__main__":
    unittest.main()
