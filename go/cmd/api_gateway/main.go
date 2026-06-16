package main

import (
	"fmt"
	"bazel_polyglot_example/go/pkg/database"
	"bazel_polyglot_example/go/pkg/encryption"
	"bazel_polyglot_example/go/pkg/mathutil"
)

func main() {
	fmt.Println("API Gateway starting...")
	db := database.NewDB()
	db.AddUser("gateway_admin", "admin_pass")
	enc := encryption.EncryptPayload("healthcheck", mathutil.RecursiveFibonacci(4))
	fmt.Println("Status:", enc)
}
