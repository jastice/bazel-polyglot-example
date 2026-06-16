package mathutil

// PrimeSieve returns all prime numbers up to n.
func PrimeSieve(n int) []int {
	if n < 2 {
		return []int{}
	}
	sieve := make([]bool, n+1)
	var primes []int
	for p := 2; p*p <= n; p++ {
		if !sieve[p] {
			for i := p * p; i <= n; i += p {
				sieve[i] = true
			}
		}
	}
	for p := 2; p <= n; p++ {
		if !sieve[p] {
			primes = append(primes, p)
		}
	}
	return primes
}
