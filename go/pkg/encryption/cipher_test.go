package encryption

import "testing"

func TestRot13(t *testing.T) {
	input := "Hello, World!"
	expected := "Uryyb, Jbeyq!"
	if Rot13(input) != expected {
		t.Errorf("Expected %q, got %q", expected, Rot13(input))
	}
	if Rot13(expected) != input {
		t.Errorf("Rot13 should be symmetric")
	}
}

func TestEncryptPayload(t *testing.T) {
	res := EncryptPayload("test", 5)
	if res == "" {
		t.Errorf("Encrypted payload should not be empty")
	}
}
