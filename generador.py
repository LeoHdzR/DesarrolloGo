import os

# Configuración del proyecto
BASE_DIR = "FinalP"

# Diccionario con rutas y contenido de archivos
files = {
    "go.mod": """module FinalP

go 1.21

require (
	github.com/gin-gonic/gin v1.9.1
	gorm.io/driver/postgres v1.5.0
	gorm.io/gorm v1.25.7
)
""",
    "main.go": """package main

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
""",
    "database/conexion.go": """package database

import (
	"log"
	"os"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var DB *gorm.DB

func ConectarDB() {
	var err error
	dsn := os.Getenv("DATABASE_URL")
	
	if dsn == "" {
		log.Fatal("ERROR: La variable de entorno DATABASE_URL no existe.")
	}

	DB, err = gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatal("Falló la conexión a PostgreSQL: ", err)
	}
}
""",
    "estudiantes/modelo.go": """package estudiantes

type Estudiante struct {
	ID    uint   `gorm:"primaryKey;column:student_id" json:"student_id"`
	Name  string `gorm:"not null" json:"name" binding:"required"`
	Group string `gorm:"column:group" json:"group"`
	Email string `gorm:"uniqueIndex;not null" json:"email" binding:"required,email"`
}

func (Estudiante) TableName() string {
	return "students"
}
""",
    "estudiantes/controlador.go": """package estudiantes

import (
	"FinalP/database"
	"net/http"
	"github.com/gin-gonic/gin"
)

func Rutas(r *gin.RouterGroup) {
	r.POST("", crear)
	r.GET("", listar)
	r.GET("/:id", obtenerUno)
	r.PUT("/:id", actualizar)
	r.DELETE("/:id", eliminar)
}

func crear(c *gin.Context) {
	var e Estudiante
	if err := c.ShouldBindJSON(&e); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	if err := database.DB.Create(&e).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "No se pudo crear (¿Email duplicado?)"})
		return
	}
	c.JSON(http.StatusCreated, e)
}

func listar(c *gin.Context) {
	var lista []Estudiante
	database.DB.Find(&lista)
	c.JSON(http.StatusOK, lista)
}

func obtenerUno(c *gin.Context) {
	var e Estudiante
	if err := database.DB.First(&e, c.Param("id")).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "No encontrado"})
		return
	}
	c.JSON(http.StatusOK, e)
}

func actualizar(c *gin.Context) {
	var e Estudiante
	id := c.Param("id")
	if err := database.DB.First(&e, id).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "No encontrado"})
		return
	}
	if err := c.ShouldBindJSON(&e); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	database.DB.Save(&e)
	c.JSON(http.StatusOK, e)
}

func eliminar(c *gin.Context) {
	if err := database.DB.Delete(&Estudiante{}, c.Param("id")).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al eliminar"})
		return
	}
	c.JSON(http.StatusOK, gin.H{"mensaje": "Eliminado"})
}
""",
    "materias/modelo.go": """package materias

type Materia struct {
	ID   uint   `gorm:"primaryKey;column:subject_id" json:"subject_id"`
	Name string `gorm:"not null" json:"name" binding:"required"`
}

func (Materia) TableName() string {
	return "subjects"
}
""",
    "materias/controlador.go": """package materias

import (
	"FinalP/database"
	"net/http"
	"github.com/gin-gonic/gin"
)

func Rutas(r *gin.RouterGroup) {
	r.POST("", crear)
	r.GET("/:id", obtenerUno)
	r.PUT("/:id", actualizar)
	r.DELETE("/:id", eliminar)
}

func crear(c *gin.Context) {
	var m Materia
	if err := c.ShouldBindJSON(&m); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	database.DB.Create(&m)
	c.JSON(http.StatusCreated, m)
}

func obtenerUno(c *gin.Context) {
	var m Materia
	if err := database.DB.First(&m, c.Param("id")).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "No encontrada"})
		return
	}
	c.JSON(http.StatusOK, m)
}

func actualizar(c *gin.Context) {
	var m Materia
	id := c.Param("id")
	if err := database.DB.First(&m, id).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "No encontrada"})
		return
	}
	if err := c.ShouldBindJSON(&m); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	database.DB.Save(&m)
	c.JSON(http.StatusOK, m)
}

func eliminar(c *gin.Context) {
	if err := database.DB.Delete(&Materia{}, c.Param("id")).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al eliminar"})
		return
	}
	c.JSON(http.StatusOK, gin.H{"mensaje": "Eliminada"})
}
""",
    "calificaciones/modelo.go": """package calificaciones

import (
	"FinalP/estudiantes"
	"FinalP/materias"
)

type Calificacion struct {
	ID        uint    `gorm:"primaryKey;column:grade_id" json:"grade_id"`
	StudentID uint    `gorm:"column:student_id;not null" json:"student_id" binding:"required"`
	SubjectID uint    `gorm:"column:subject_id;not null" json:"subject_id" binding:"required"`
	Score     float64 `gorm:"column:grade;not null" json:"grade" binding:"required,min=0,max=100"`

	Student estudiantes.Estudiante `gorm:"foreignKey:StudentID" json:"-"`
	Subject materias.Materia       `gorm:"foreignKey:SubjectID" json:"-"`
}

func (Calificacion) TableName() string {
	return "grades"
}
""",
    "calificaciones/controlador.go": """package calificaciones

import (
	"FinalP/database"
	"net/http"
	"github.com/gin-gonic/gin"
)

func Rutas(r *gin.RouterGroup) {
	r.POST("", crear)
	r.PUT("/:id", actualizar)
	r.DELETE("/:id", eliminar)
	r.GET("/student/:student_id", listarPorEstudiante)
	r.GET("/:id/student/:student_id", obtenerPorIdYEstudiante)
}

func crear(c *gin.Context) {
	var cal Calificacion
	if err := c.ShouldBindJSON(&cal); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	if err := database.DB.Create(&cal).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al guardar"})
		return
	}
	c.JSON(http.StatusCreated, cal)
}

func actualizar(c *gin.Context) {
	var cal Calificacion
	id := c.Param("id")
	if err := database.DB.First(&cal, id).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "No encontrada"})
		return
	}
	var input struct { Score float64 `json:"grade"` }
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	cal.Score = input.Score
	database.DB.Save(&cal)
	c.JSON(http.StatusOK, cal)
}

func eliminar(c *gin.Context) {
	if err := database.DB.Delete(&Calificacion{}, c.Param("id")).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al eliminar"})
		return
	}
	c.JSON(http.StatusOK, gin.H{"mensaje": "Eliminada"})
}

func listarPorEstudiante(c *gin.Context) {
	var lista []Calificacion
	if err := database.DB.Where("student_id = ?", c.Param("student_id")).Find(&lista).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, lista)
}

func obtenerPorIdYEstudiante(c *gin.Context) {
	var cal Calificacion
	if err := database.DB.Where("grade_id = ? AND student_id = ?", c.Param("id"), c.Param("student_id")).First(&cal).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "No encontrada"})
		return
	}
	c.JSON(http.StatusOK, cal)
}
"""
}

def create_project():
    # Crear carpeta raíz
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
        print(f"Carpeta '{BASE_DIR}' creada.")
    
    # Crear archivos
    for file_path, content in files.items():
        full_path = os.path.join(BASE_DIR, file_path)
        directory = os.path.dirname(full_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Generado: {full_path}")

    print("\\n-----------------------------------")
    print("PROYECTO CREADO EXITOSAMENTE")
    print("-----------------------------------")
    print("1. cd FinalP")
    print("2. go mod tidy")
    print("3. Configura tu DATABASE_URL")
    print("4. go run main.go")

if __name__ == "__main__":
    create_project()