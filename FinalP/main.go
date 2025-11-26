package main

import (
	"log"
	"os"

	"FinalP/calificaciones"
	"FinalP/database"
	"FinalP/estudiantes"
	"FinalP/materias"

	"github.com/gin-gonic/gin"
)

func main() {
	// 1. Conectar a Base de Datos
	database.ConectarDB()

	// 2. Auto-Migración
	db := database.DB
	err := db.AutoMigrate(
		&estudiantes.Estudiante{},
		&materias.Materia{},
		&calificaciones.Calificacion{},
	)
	if err != nil {
		log.Fatal("Error creando tablas: ", err)
	}

	// 3. Configurar servidor web (Gin)
	r := gin.Default()

	// 4. Definir rutas
	api := r.Group("/api")
	{
		estudiantes.Rutas(api.Group("/students"))
		materias.Rutas(api.Group("/subjects"))
		calificaciones.Rutas(api.Group("/grades"))
	}

	// 5. Iniciar servidor
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	log.Println("Sistema Escolar corriendo en puerto " + port)
	r.Run(":" + port)
}
