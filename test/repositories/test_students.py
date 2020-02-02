from datetime import datetime
from app.repositories.student import StudentRepository

data_path = f"./testdata/placebo/app/repositories/{__name__}"


def test_all(student_repository: StudentRepository):
    
    students = student_repository.all()

    print(students)

    assert len(students) > 0

    for student in students:
        assert student.id is not None
        assert student.first_name is not None
        assert student.last_name is not None
        assert student.grades is not None
        assert student.created_at is not None
        assert student.updated_at is not None


def test_update(student_repository: StudentRepository):

    students = student_repository.all()

    for student in students:
        student.updated_at = datetime.now().isoformat()
        student_repository.update(student)
