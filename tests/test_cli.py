import unittest
from pcs_cli.cli import CLI

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
        cli = CLI()
        for i, (command, expected_result) in enumerate(get_args_testcases):
            with self.subTest(f"Subtest {i} for command '{command}'"):
                print(f"\nSubtest {i} for command '{command}'")
                try:
                    result = cli.get_args(command)
                    self.assertEqual(result, expected_result)
                    print(f"Successfully no Cmd errors for Subset {i}")
                except SystemExit as cm:
                    self.assertEqual(cm.code, expected_result)


if __name__ == "__main__":
    unittest.main()
