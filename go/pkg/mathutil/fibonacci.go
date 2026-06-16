package mathutil

// RecursiveFibonacci computes the nth Fibonacci number, looking complicated.
func RecursiveFibonacci(n int) int {
	if n <= 0 {
		return 0
	}
	if n == 1 {
		return 1
	}
	return RecursiveFibonacci(n-1) + RecursiveFibonacci(n-2)
}
