"""Text analysis service combining string utils with data structures."""

from python.libs.stringutils.transforms import capitalize_words, camel_to_snake
from python.libs.stringutils.validators import is_palindrome, is_valid_email, is_valid_identifier
from python.libs.datastructs.collections import FrequencyMap, StatsList
from python.libs.formatting.formatters import ReportFormatter, TableFormatter


class TextAnalyzer:
    """Analyzes text and produces statistical reports."""

    def __init__(self, text: str):
        self._text = text
        self._words = text.split()
        self._word_freq = FrequencyMap()
        self._char_freq = FrequencyMap()
        self._analyze()

    def _analyze(self) -> None:
        for word in self._words:
            self._word_freq.add(word.lower())
        for char in self._text:
            if char.strip():
                self._char_freq.add(char.lower())

    @property
    def word_count(self) -> int:
        return len(self._words)

    @property
    def char_count(self) -> int:
        return len(self._text)

    @property
    def unique_words(self) -> int:
        return len(set(w.lower() for w in self._words))

    def word_lengths(self) -> StatsList:
        return StatsList([float(len(w)) for w in self._words])

    def word_frequency_report(self, top_n: int = 10) -> str:
        return ReportFormatter.format_frequency_map(
            "word frequency analysis", self._word_freq, top_n
        )

    def char_frequency_report(self, top_n: int = 10) -> str:
        return ReportFormatter.format_frequency_map(
            "character frequency analysis", self._char_freq, top_n
        )

    def find_palindromes(self) -> list[str]:
        return [w for w in set(self._words) if len(w) > 1 and is_palindrome(w)]

    def find_emails(self) -> list[str]:
        return [w for w in self._words if is_valid_email(w)]

    def find_identifiers(self) -> list[str]:
        return [w for w in self._words if is_valid_identifier(w)]

    def summary_table(self) -> str:
        lengths = self.word_lengths()
        table = TableFormatter(["metric", "value"])
        table.add_row(["Total Words", self.word_count])
        table.add_row(["Unique Words", self.unique_words])
        table.add_row(["Total Characters", self.char_count])
        table.add_row(["Avg Word Length", f"{lengths.mean:.2f}"])
        table.add_row(["Median Word Length", f"{lengths.median:.1f}"])
        table.add_row(["Palindromes Found", len(self.find_palindromes())])
        table.add_row(["Emails Found", len(self.find_emails())])
        return table.render()

    def detailed_report(self) -> str:
        sections = [
            capitalize_words("text analysis report"),
            "=" * 40,
            "",
            self.summary_table(),
            "",
            self.word_frequency_report(top_n=5),
            "",
            self.char_frequency_report(top_n=10),
        ]
        palindromes = self.find_palindromes()
        if palindromes:
            sections.append("")
            sections.append(f"Palindromes: {', '.join(palindromes)}")
        return "\n".join(sections)
