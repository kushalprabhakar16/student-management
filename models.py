from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    marks = db.Column(db.JSON, nullable=False, default=list)
    average = db.Column(db.Float, nullable=True)
    grade = db.Column(db.String(2), nullable=False, default="-")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def calculate_average(self):
        if not self.marks:
            self.average = None
            self.grade = "-"
            return
        self.average = round(sum(self.marks) / len(self.marks), 2)
        if self.average >= 90:
            self.grade = "A+"
        elif self.average >= 80:
            self.grade = "A"
        elif self.average >= 70:
            self.grade = "B"
        elif self.average >= 60:
            self.grade = "C"
        elif self.average >= 50:
            self.grade = "D"
        else:
            self.grade = "F"

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "email": self.email,
            "marks": self.marks or [],
            "average": self.average,
            "grade": self.grade,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
