package mathutil

import "testing"

func TestPrimeSieve(t *testing.T) {
	primes := PrimeSieve(10)
	expected := []int{2, 3, 5, 7}
	if len(primes) != len(expected) {
		t.Fatalf("Expected %d primes, got %d", len(expected), len(primes))
	}
	for i, v := range expected {
		if primes[i] != v {
			t.Errorf("Expected prime %d to be %d, got %d", i, v, primes[i])
		}
	}
}

func TestRecursiveFibonacci(t *testing.T) {
	if RecursiveFibonacci(5) != 5 {
		t.Errorf("Expected Fib(5) to be 5")
	}
	if RecursiveFibonacci(10) != 55 {
		t.Errorf("Expected Fib(10) to be 55")
	}
}
