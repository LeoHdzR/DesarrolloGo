package materias

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
