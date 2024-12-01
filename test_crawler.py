import unittest
import crawler

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
        ["test.py", "https://github.com/SpoonLabs/astor"],
        ["https://github.com/SpoonLabs/astor"],
    ),
    (
        ["crawler.py", "http://github.com/SpoonLabs/astor"],
        ["http://github.com/SpoonLabs/astor"],
    ),
    (["https://github.com/SpoonLabs/astor", "2"], 1),
    (["https://github.com/SpoonLabs/astor", "", ""], 1),
    ([""], 1),
    (["test"], 1),
    (["foo", "bar"], 1),
    (["foo", "bar", "54"], 1),
    ([1, 1, 1], 1),
]

generate_url_testcases = [
    # Positive Test Cases
    (
        ["https://github.com/SpoonLabs/astor"],
        "https://github.com/search?q=repo%3ASpoonLabs/astor%20path%3A.md&type=code",
    ),
    (
        ["https://github.com/vim/vim"],
        "https://github.com/search?q=repo%3Avim/vim%20path%3A.md&type=code",
    )
]


class TestCrawler(unittest.TestCase):
    def test_get_args(self):
        for i, (command, expected_result) in enumerate(get_args_testcases):
            with self.subTest(f"Subtest {i} for command '{command}'"):
                print(f"Subtest {i} for command '{command}'")
                try:
                    result = crawler.get_args(command)
                    self.assertEqual(result, expected_result)
                except SystemExit as cm:
                    self.assertEqual(cm.code, expected_result)

    def test_generate_url(self):
        for i, (test_url, expected_url) in enumerate(generate_url_testcases):
            with self.subTest(f"Subtest {i} for command '{expected_url}'"):
                print(f"Subtest {i} for url '{test_url}'")
                try:
                    generated_url = crawler.generate_url(test_url)
                    self.assertEqual(generated_url, expected_url)
                except SystemExit as cm:
                    self.assertEqual(cm.code, expected_url)


if __name__ == "__main__":
    unittest.main()
