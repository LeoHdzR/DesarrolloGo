package calificaciones

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
