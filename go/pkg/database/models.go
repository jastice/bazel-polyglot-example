package database

type User struct {
	ID       int
	Username string
	Password string
}

type Order struct {
	ID     int
	UserID int
	Item   string
	Price  int
}
