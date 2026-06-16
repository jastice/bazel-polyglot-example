"""Tests for text analyzer service."""

import unittest

from python.services.analyzer.text_analyzer import TextAnalyzer


class TestTextAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = TextAnalyzer(
            "the quick brown fox jumps over the lazy dog the fox"
        )

    def test_word_count(self):
        self.assertEqual(self.analyzer.word_count, 11)

    def test_unique_words(self):
        self.assertEqual(self.analyzer.unique_words, 8)

    def test_word_lengths(self):
        lengths = self.analyzer.word_lengths()
        self.assertEqual(len(lengths), 11)
        self.assertAlmostEqual(lengths.mean, sum(len(w) for w in "the quick brown fox jumps over the lazy dog the fox".split()) / 11)

    def test_find_palindromes(self):
        analyzer = TextAnalyzer("the racecar and kayak were level")
        palindromes = analyzer.find_palindromes()
        self.assertIn("racecar", palindromes)
        self.assertIn("kayak", palindromes)
        self.assertIn("level", palindromes)

    def test_find_emails(self):
        analyzer = TextAnalyzer("contact user@example.com or admin@test.org today")
        emails = analyzer.find_emails()
        self.assertEqual(len(emails), 2)
        self.assertIn("user@example.com", emails)

    def test_summary_table(self):
        table = self.analyzer.summary_table()
        self.assertIn("Total Words", table)
        self.assertIn("11", table)

    def test_detailed_report(self):
        report = self.analyzer.detailed_report()
        self.assertIn("Text Analysis Report", report)
        self.assertIn("word frequency", report.lower())


if __name__ == "__main__":
    unittest.main()
