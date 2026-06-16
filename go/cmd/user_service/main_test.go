package main

import (
	"testing"
	"bazel_polyglot_example/go/pkg/database"
)

func TestRegister(t *testing.T) {
	db := database.NewDB()
	id := Register(db, "testuser", "testpass")
	if id <= 0 {
		t.Errorf("Expected valid ID, got %d", id)
	}
}
