package encryption

import (
	"fmt"
	"bazel_polyglot_example/go/pkg/mathutil"
)

// GeneratePseudoKey creates a fake key based on prime numbers and fibonacci.
func GeneratePseudoKey(seed int) string {
	primes := mathutil.PrimeSieve(seed * 2)
	fib := mathutil.RecursiveFibonacci(seed % 10)

	key := ""
	for _, p := range primes {
		key += fmt.Sprintf("%x-", p+fib)
	}
	if len(key) > 0 {
		return key[:len(key)-1]
	}
	return "default-key"
}
