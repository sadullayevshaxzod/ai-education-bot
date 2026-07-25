"""
Tests for the common application.
"""

from django.test import TestCase

from .utils import generate_numeric_code


class GenerateNumericCodeTests(TestCase):
    """
    Tests for generate_numeric_code utility.
    """

    def test_default_length(self) -> None:
        """
        Default code should contain 6 digits.
        """
        code = generate_numeric_code()

        self.assertEqual(len(code), 6)
        self.assertTrue(code.isdigit())

    def test_custom_length(self) -> None:
        """
        Custom length should be respected.
        """
        code = generate_numeric_code(4)

        self.assertEqual(len(code), 4)
        self.assertTrue(code.isdigit())

    def test_invalid_length(self) -> None:
        """
        Length less than one should raise ValueError.
        """
        with self.assertRaises(ValueError):
            generate_numeric_code(0)