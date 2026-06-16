"""Statistical functions."""

from python.libs.mathutils.operations import add, divide


def mean(values: list[float]) -> float:
    if not values:
        raise ValueError("Cannot compute mean of empty list")
    total = values[0]
    for v in values[1:]:
        total = add(total, v)
    return divide(total, len(values))


def median(values: list[float]) -> float:
    if not values:
        raise ValueError("Cannot compute median of empty list")
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    mid = n // 2
    if n % 2 == 0:
        return divide(add(sorted_vals[mid - 1], sorted_vals[mid]), 2)
    return sorted_vals[mid]


def variance(values: list[float]) -> float:
    if len(values) < 2:
        raise ValueError("Need at least 2 values for variance")
    m = mean(values)
    squared_diffs = [(v - m) ** 2 for v in values]
    return mean(squared_diffs)


def standard_deviation(values: list[float]) -> float:
    return variance(values) ** 0.5
