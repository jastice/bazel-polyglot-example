"""Tests for stringutils package."""

import unittest

from python.libs.stringutils.transforms import (
    capitalize_words, reverse_string, snake_to_camel, camel_to_snake, truncate,
)
from python.libs.stringutils.validators import (
    is_palindrome, is_valid_email, contains_only_digits, is_valid_identifier,
)


class TestTransforms(unittest.TestCase):
    def test_capitalize_words(self):
        self.assertEqual(capitalize_words("hello world"), "Hello World")
        self.assertEqual(capitalize_words("foo bar baz"), "Foo Bar Baz")

    def test_reverse_string(self):
        self.assertEqual(reverse_string("hello"), "olleh")
        self.assertEqual(reverse_string(""), "")

    def test_snake_to_camel(self):
        self.assertEqual(snake_to_camel("hello_world"), "helloWorld")
        self.assertEqual(snake_to_camel("foo_bar_baz"), "fooBarBaz")

    def test_camel_to_snake(self):
        self.assertEqual(camel_to_snake("helloWorld"), "hello_world")
        self.assertEqual(camel_to_snake("fooBarBaz"), "foo_bar_baz")

    def test_truncate(self):
        self.assertEqual(truncate("hello world", 8), "hello...")
        self.assertEqual(truncate("short", 10), "short")


class TestValidators(unittest.TestCase):
    def test_is_palindrome(self):
        self.assertTrue(is_palindrome("racecar"))
        self.assertTrue(is_palindrome("A man a plan a canal Panama"))
        self.assertFalse(is_palindrome("hello"))

    def test_is_valid_email(self):
        self.assertTrue(is_valid_email("user@example.com"))
        self.assertTrue(is_valid_email("foo.bar@test.org"))
        self.assertFalse(is_valid_email("not-an-email"))
        self.assertFalse(is_valid_email("@missing.com"))

    def test_contains_only_digits(self):
        self.assertTrue(contains_only_digits("12345"))
        self.assertFalse(contains_only_digits("123a5"))
        self.assertFalse(contains_only_digits(""))

    def test_is_valid_identifier(self):
        self.assertTrue(is_valid_identifier("hello_world"))
        self.assertTrue(is_valid_identifier("_private"))
        self.assertFalse(is_valid_identifier("123abc"))
        self.assertFalse(is_valid_identifier("hello world"))


if __name__ == "__main__":
    unittest.main()
