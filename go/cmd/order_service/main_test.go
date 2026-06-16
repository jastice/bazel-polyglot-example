package main

import (
	"testing"
	"bazel_polyglot_example/go/pkg/database"
)

func TestPlaceOrder(t *testing.T) {
	db := database.NewDB()
	id := PlaceOrder(db, 1, "phone", 500)
	if id <= 0 {
		t.Errorf("Expected valid order ID, got %d", id)
	}
}
