import unittest
import sys
from unittest.mock import patch
from main import get_arguments, validate_arguments, generate_url


class TestCLI(unittest.TestCase):

    def test_get_arguments_valid(self):
        # Test with valid arguments (2 arguments)
        with patch.object(
            sys, "argv", ["main.py", "https://github.com/user/repo", "5"]
        ):
            arguments = get_arguments(sys.argv)
            self.assertEqual(
                arguments,
                ["https://github.com/user/repo", "5"],
                "Should return valid arguments.",
            )

    def test_get_arguments_invalid_too_few(self):
        # Test with too few arguments (no arguments)
        with patch.object(sys, "argv", ["main.py"]):
            arguments = get_arguments(sys.argv)
            self.assertIsNone(arguments, "Should return None for too few arguments.")

    def test_get_arguments_invalid_too_many(self):
        # Test with too many arguments
        with patch.object(
            sys, "argv", ["main.py", "https://github.com/user/repo", "5", "extra"]
        ):
            arguments = get_arguments(sys.argv)
            self.assertIsNone(arguments, "Should return None for too many arguments.")

    def test_validate_arguments_valid(self):
        # Test with valid URL and integer
        arguments = ["https://github.com/user/repo", "5"]
        validated_arguments = validate_arguments(arguments)
        self.assertEqual(
            validated_arguments, arguments, "Should return the valid arguments."
        )

    def test_validate_arguments_invalid_url(self):
        # Test with invalid URL
        arguments = ["invalidurl", "5"]
        validated_arguments = validate_arguments(arguments)
        self.assertIsNone(validated_arguments, "Should return None for an invalid URL.")

    def test_validate_arguments_invalid_integer(self):
        # Test with a non-integer for the second argument
        arguments = ["https://github.com/user/repo", "notaninteger"]
        validated_arguments = validate_arguments(arguments)
        self.assertIsNone(
            validated_arguments, "Should return None for a non-integer argument."
        )


if __name__ == "__main__":
    unittest.main()
