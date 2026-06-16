package encryption

import "strings"

// Rot13 implements a simple Caesar cipher to look like encryption.
func Rot13(input string) string {
	var out strings.Builder
	for _, c := range input {
		switch {
		case 'a' <= c && c <= 'z':
			out.WriteRune('a' + (c-'a'+13)%26)
		case 'A' <= c && c <= 'Z':
			out.WriteRune('A' + (c-'A'+13)%26)
		default:
			out.WriteRune(c)
		}
	}
	return out.String()
}

// EncryptPayload combines rot13 and a pseudo key.
func EncryptPayload(payload string, seed int) string {
	key := GeneratePseudoKey(seed)
	return Rot13(payload) + "||" + key
}
