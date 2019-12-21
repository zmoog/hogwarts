
from app.parsers import extract_grades


def test_registro_classe():

    page = open('./test/data/registro_docente.html', 'r').read()
    
    grades = extract_grades(page)

    assert len(grades) == 27
