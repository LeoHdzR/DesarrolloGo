package materias

type Materia struct {
	ID   uint   `gorm:"primaryKey;column:subject_id" json:"subject_id"`
	Name string `gorm:"not null" json:"name" binding:"required"`
}

func (Materia) TableName() string {
	return "subjects"
}
