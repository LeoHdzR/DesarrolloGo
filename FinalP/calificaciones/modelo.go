package calificaciones

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
