package estudiantes

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
