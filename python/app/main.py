"""Main application demonstrating all packages working together."""

from python.services.calculator.engine import Calculator
from python.services.analyzer.text_analyzer import TextAnalyzer
from python.libs.datastructs.collections import Matrix


def demo_calculator() -> None:
    print("=" * 60)
    print("  CALCULATOR DEMO")
    print("=" * 60)
    print()

    calc = Calculator()

    calc.compute_add(10, 25)
    calc.compute_multiply(7, 8)
    calc.compute_subtract(100, 37)
    calc.compute_divide(144, 12)
    calc.compute_power(2, 10)
    calc.compute_factorial(6)

    print("Computation History:")
    print(calc.history_table())
    print()

    values = [10.0, 20.0, 30.0, 40.0, 50.0, 15.0, 25.0, 35.0]
    print("Batch Statistics:")
    print(calc.statistics_summary(values))
    print()

    results = calc.batch_compute([1, 2, 3, 4, 5], "multiply")
    print(f"Pairwise products: {results.values}")
    print(f"Mean of products: {results.mean:.2f}")
    print()


def demo_analyzer() -> None:
    print("=" * 60)
    print("  TEXT ANALYZER DEMO")
    print("=" * 60)
    print()

    sample_text = (
        "The quick brown fox jumps over the lazy dog. "
        "A man a plan a canal Panama is a famous palindrome. "
        "The level of the civic duty was extraordinary. "
        "Contact us at info@example.com or support@test.org for details. "
        "The racecar sped past the kayak on the river. "
        "Python programming with Bazel build system is powerful. "
        "The madam told the civic leaders about the level crossing."
    )

    analyzer = TextAnalyzer(sample_text)
    print(analyzer.detailed_report())
    print()


def demo_matrix() -> None:
    print("=" * 60)
    print("  MATRIX OPERATIONS DEMO")
    print("=" * 60)
    print()

    m1 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    m2 = Matrix([[9, 8, 7], [6, 5, 4], [3, 2, 1]])

    print(f"Matrix 1: {m1}")
    print(f"Matrix 2: {m2}")
    print(f"Shape: {m1.shape}")
    print(f"Row means: {m1.row_means()}")
    print(f"Col means: {m1.col_means()}")

    m3 = m1.add_matrix(m2)
    print(f"M1 + M2: {m3}")

    m4 = m1.scale(2.5)
    print(f"M1 * 2.5: {m4}")
    print()


def main() -> None:
    demo_calculator()
    demo_analyzer()
    demo_matrix()
    print("All demos completed successfully!")


if __name__ == "__main__":
    main()
