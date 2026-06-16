"""Formatting utilities for displaying data."""

from python.libs.stringutils.transforms import capitalize_words, truncate
from python.libs.datastructs.collections import StatsList, FrequencyMap


class TableFormatter:
    """Formats data into text tables."""

    def __init__(self, headers: list[str], col_width: int = 15):
        self._headers = headers
        self._rows: list[list[str]] = []
        self._col_width = col_width

    def add_row(self, values: list) -> None:
        self._rows.append([str(v) for v in values])

    def _format_cell(self, text: str) -> str:
        return truncate(text, self._col_width).ljust(self._col_width)

    def render(self) -> str:
        lines = []
        header_line = " | ".join(
            self._format_cell(capitalize_words(h)) for h in self._headers
        )
        lines.append(header_line)
        lines.append("-" * len(header_line))
        for row in self._rows:
            line = " | ".join(self._format_cell(v) for v in row)
            lines.append(line)
        return "\n".join(lines)


class ReportFormatter:
    """Formats statistical reports from data structures."""

    @staticmethod
    def format_stats_list(name: str, data: StatsList) -> str:
        lines = [
            f"=== {capitalize_words(name)} ===",
            f"  Count:    {len(data)}",
            f"  Sum:      {data.sum:.4f}",
            f"  Mean:     {data.mean:.4f}",
            f"  Median:   {data.median:.4f}",
        ]
        if len(data) >= 2:
            lines.append(f"  Variance: {data.variance:.4f}")
        return "\n".join(lines)

    @staticmethod
    def format_frequency_map(name: str, freq: FrequencyMap, top_n: int = 5) -> str:
        lines = [
            f"=== {capitalize_words(name)} ===",
            f"  Total items: {freq.total}",
            f"  Top {top_n}:",
        ]
        for item, count in freq.most_common(top_n):
            pct = freq.frequency(item) * 100
            bar = "#" * int(pct / 2)
            lines.append(f"    {truncate(item, 20):22s} {count:5d} ({pct:5.1f}%) {bar}")
        return "\n".join(lines)
