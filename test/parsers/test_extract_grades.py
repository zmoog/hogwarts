from app.parsers import extract_grades


def test_registro_docente(load_html):

    grades = extract_grades(load_html('registro_docente'))

    assert len(grades) == 27
