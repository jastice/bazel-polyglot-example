package main

import (
	"fmt"
	"bazel_polyglot_example/go/pkg/database"
	"bazel_polyglot_example/go/pkg/mathutil"
)

func PlaceOrder(db *database.DB, userID int, item string, price int) int {
	// A complicated tax calculation using prime numbers
	primes := mathutil.PrimeSieve(10)
	tax := primes[len(primes)-1]
	return db.AddOrder(userID, item, price+tax)
}

func main() {
	db := database.NewDB()
	id := PlaceOrder(db, 1, "laptop", 1000)
	fmt.Printf("Order placed with ID %d\n", id)
}
