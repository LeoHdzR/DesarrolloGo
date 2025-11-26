package estudiantes

type Estudiante struct {
	ID    uint   `gorm:"primaryKey;column:student_id" json:"student_id"`
	Name  string `gorm:"not null" json:"name" binding:"required"`
	Group string `gorm:"column:group" json:"group"`
	Email string `gorm:"uniqueIndex;not null" json:"email" binding:"required,email"`
}

func (Estudiante) TableName() string {
	return "students"
}
