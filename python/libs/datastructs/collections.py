"""Custom data structures with statistical capabilities."""

from python.libs.mathutils.operations import add, multiply, divide
from python.libs.mathutils.stats import mean, median, variance


class StatsList:
    """A list that tracks statistical properties of its numeric contents."""

    def __init__(self, values: list[float] | None = None):
        self._values: list[float] = list(values) if values else []

    def append(self, value: float) -> None:
        self._values.append(value)

    def extend(self, values: list[float]) -> None:
        self._values.extend(values)

    @property
    def values(self) -> list[float]:
        return list(self._values)

    @property
    def sum(self) -> float:
        result = 0.0
        for v in self._values:
            result = add(result, v)
        return result

    @property
    def mean(self) -> float:
        return mean(self._values)

    @property
    def median(self) -> float:
        return median(self._values)

    @property
    def variance(self) -> float:
        return variance(self._values)

    def scaled(self, factor: float) -> "StatsList":
        return StatsList([multiply(v, factor) for v in self._values])

    def normalized(self) -> "StatsList":
        m = self.mean
        v = self.variance ** 0.5
        if v == 0:
            return StatsList([0.0] * len(self._values))
        return StatsList([divide(x - m, v) for x in self._values])

    def __len__(self) -> int:
        return len(self._values)

    def __repr__(self) -> str:
        return f"StatsList({self._values})"


class FrequencyMap:
    """Tracks frequency counts of items."""

    def __init__(self):
        self._counts: dict[str, int] = {}

    def add(self, item: str, count: int = 1) -> None:
        self._counts[item] = self._counts.get(item, 0) + count

    def count(self, item: str) -> int:
        return self._counts.get(item, 0)

    @property
    def total(self) -> int:
        return sum(self._counts.values())

    def most_common(self, n: int | None = None) -> list[tuple[str, int]]:
        sorted_items = sorted(self._counts.items(), key=lambda x: x[1], reverse=True)
        if n is not None:
            return sorted_items[:n]
        return sorted_items

    def frequency(self, item: str) -> float:
        if self.total == 0:
            return 0.0
        return divide(self.count(item), self.total)

    def __repr__(self) -> str:
        return f"FrequencyMap({self._counts})"


class Matrix:
    """Simple matrix with basic operations."""

    def __init__(self, rows: list[list[float]]):
        if not rows or not rows[0]:
            raise ValueError("Matrix cannot be empty")
        col_len = len(rows[0])
        for row in rows:
            if len(row) != col_len:
                raise ValueError("All rows must have the same length")
        self._rows = [list(row) for row in rows]

    @property
    def shape(self) -> tuple[int, int]:
        return len(self._rows), len(self._rows[0])

    def get(self, row: int, col: int) -> float:
        return self._rows[row][col]

    def row_means(self) -> list[float]:
        return [mean(row) for row in self._rows]

    def col_means(self) -> list[float]:
        num_rows, num_cols = self.shape
        result = []
        for c in range(num_cols):
            col_values = [self._rows[r][c] for r in range(num_rows)]
            result.append(mean(col_values))
        return result

    def scale(self, factor: float) -> "Matrix":
        return Matrix([[multiply(v, factor) for v in row] for row in self._rows])

    def add_matrix(self, other: "Matrix") -> "Matrix":
        if self.shape != other.shape:
            raise ValueError("Matrices must have the same shape")
        return Matrix([
            [add(self._rows[r][c], other._rows[r][c]) for c in range(self.shape[1])]
            for r in range(self.shape[0])
        ])

    def __repr__(self) -> str:
        return f"Matrix({self._rows})"
