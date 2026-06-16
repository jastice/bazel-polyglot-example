"""Calculator service that combines math operations with formatted output."""

from python.libs.mathutils.operations import add, subtract, multiply, divide, power, factorial
from python.libs.mathutils.stats import mean, median, standard_deviation
from python.libs.formatting.formatters import TableFormatter, ReportFormatter
from python.libs.datastructs.collections import StatsList


class Calculator:
    """A calculator that maintains history and provides formatted results."""

    def __init__(self):
        self._history: list[tuple[str, float]] = []

    def _record(self, expression: str, result: float) -> float:
        self._history.append((expression, result))
        return result

    def compute_add(self, a: float, b: float) -> float:
        return self._record(f"{a} + {b}", add(a, b))

    def compute_subtract(self, a: float, b: float) -> float:
        return self._record(f"{a} - {b}", subtract(a, b))

    def compute_multiply(self, a: float, b: float) -> float:
        return self._record(f"{a} * {b}", multiply(a, b))

    def compute_divide(self, a: float, b: float) -> float:
        return self._record(f"{a} / {b}", divide(a, b))

    def compute_power(self, base: float, exp: float) -> float:
        return self._record(f"{base} ^ {exp}", power(base, exp))

    def compute_factorial(self, n: int) -> int:
        result = factorial(n)
        self._history.append((f"{n}!", result))
        return result

    def batch_compute(self, values: list[float], operation: str) -> StatsList:
        results = StatsList()
        for i in range(len(values) - 1):
            if operation == "add":
                results.append(self.compute_add(values[i], values[i + 1]))
            elif operation == "multiply":
                results.append(self.compute_multiply(values[i], values[i + 1]))
            elif operation == "subtract":
                results.append(self.compute_subtract(values[i], values[i + 1]))
        return results

    def statistics_summary(self, values: list[float]) -> str:
        data = StatsList(values)
        return ReportFormatter.format_stats_list("computation results", data)

    def history_table(self) -> str:
        table = TableFormatter(["expression", "result"])
        for expr, result in self._history:
            table.add_row([expr, f"{result:.4f}"])
        return table.render()

    @property
    def history(self) -> list[tuple[str, float]]:
        return list(self._history)

    def clear_history(self) -> None:
        self._history.clear()
