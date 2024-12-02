import unittest
from crawler import get_args

get_args_testcases = [
    # Positive Test Cases
    (
        ["crawler.py", "https://github.com/SpoonLabs/astor", "2"],
        ["https://github.com/SpoonLabs/astor", "2"],
    ),
    (
        ["crawler.py", "https://github.com/SpoonLabs/astor"],
        ["https://github.com/SpoonLabs/astor"],
    ),
    # Negative Test Cases
    (
        ["crawler.py", "http://github.com/SpoonLabs/astor"],
        1,
    ),
    (["https://github.com/SpoonLabs/astor", "2"], 1),
    (["https://github.com/SpoonLabs/astor", "", ""], 1),
    ([""], 1),
    (["test"], 1),
    (["foo", "bar"], 1),
    (["foo", "bar", "54"], 1),
    ([1, 1, 1], 1),
]


class TestCrawler(unittest.TestCase):
    def test_get_args(self):
        for i, (command, expected_result) in enumerate(get_args_testcases):
            with self.subTest(f"Subtest {i} for command '{command}'"):
                print(f"Subtest {i} for command '{command}'")
                try:
                    result = get_args(command)
                    self.assertEqual(result, expected_result)
                except SystemExit as cm:
                    self.assertEqual(cm.code, expected_result)


if __name__ == "__main__":
    unittest.main()
