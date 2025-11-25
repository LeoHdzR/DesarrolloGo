package database

import (
	"log"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var DB *gorm.DB

func Connect() {
	dsn := "host=tallergo.ctegygig0fqm.us-east-2.rds.amazonaws.com user=postgres password=orvia1234 dbname=Sistema port=5432 sslmode=disable TimeZone=America/Mexico_City"
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatal("Error al conectar a la base de datos:", err)
	}
	DB = db
}
