from app.models import Student
class StudentRepository:
    
    def all(self):
        return [Student(id) for id in ["00002401", "00002138"]]

