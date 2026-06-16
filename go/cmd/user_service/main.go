package main

import (
	"fmt"
	"bazel_polyglot_example/go/pkg/database"
)

func Register(db *database.DB, username, password string) int {
	return db.AddUser(username, password)
}

func main() {
	db := database.NewDB()
	id := Register(db, "admin", "secret")
	fmt.Printf("User registered with ID %d\n", id)
}
