import language_tool_python


class Spellchecker:
    def __init__(self, locale="en-US"):
        self.tool = language_tool_python.LanguageTool(locale)

    def check(self, s, n_replacements=3):
        matches = list(
            filter(
                lambda m: m.message == "Possible spelling mistake found.",
                self.tool.check(s),
            )
        )

        return list(
            map(
                lambda m: {
                    "context": m.context,  # maybe replace with sentence
                    "word": m.context[m.offsetInContext :].split()[0],
                    "replacements": m.replacements[:n_replacements],
                },
                matches,
            )
        )
