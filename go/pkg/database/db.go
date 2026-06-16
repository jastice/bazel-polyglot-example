package database

import (
	"fmt"
	"bazel_polyglot_example/go/pkg/encryption"
	"bazel_polyglot_example/go/pkg/mathutil"
)

// DB simulates a complicated database connection.
type DB struct {
	users  map[int]User
	orders map[int]Order
}

// NewDB initializes a pseudo-database.
func NewDB() *DB {
	return &DB{
		users:  make(map[int]User),
		orders: make(map[int]Order),
	}
}

// AddUser adds a new user with encrypted password.
func (db *DB) AddUser(username, password string) int {
	id := len(db.users) + 1
	// Generate seed using some math
	seed := mathutil.RecursiveFibonacci(id % 10)
	if seed == 0 {
		seed = 1
	}
	encPassword := encryption.EncryptPayload(password, seed)

	db.users[id] = User{
		ID:       id,
		Username: username,
		Password: encPassword,
	}
	return id
}

// GetUser retrieves a user.
func (db *DB) GetUser(id int) (User, error) {
	if u, ok := db.users[id]; ok {
		return u, nil
	}
	return User{}, fmt.Errorf("user not found")
}

// AddOrder creates an order for a user.
func (db *DB) AddOrder(userID int, item string, price int) int {
	orderID := len(db.orders) + 1
	db.orders[orderID] = Order{
		ID:     orderID,
		UserID: userID,
		Item:   item,
		Price:  price,
	}
	return orderID
}
