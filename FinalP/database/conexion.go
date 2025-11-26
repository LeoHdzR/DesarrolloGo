package database

import (
	"log"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var DB *gorm.DB

func ConectarDB() {
	var err error

	// ESCRIBE TUS DATOS DE AWS AQUÍ DIRECTAMENTE:
	// Asegúrate de cambiar 'tu_password' y 'nombre_bd' (usualmente es 'postgres' o 'initial_db')
	dsn := "host=tallergo.ctegygig0fqm.us-east-2.rds.amazonaws.com user=postgres password=orvia123 dbname=postgres port=5432 sslmode=require"

	DB, err = gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatal("Falló la conexión a PostgreSQL: ", err)
	}
}
