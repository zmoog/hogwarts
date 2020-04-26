from datetime import date
from app.parsers import extract_assisgnments


def test_registro_classe(load_html):

    assignments = extract_assisgnments(load_html('registro_classe'))

    today = date.today()

    [print(assignment.when, assignment.homework) for assignment in assignments if assignment.when > today]

    assert len(assignments) == 7
    assert assignments[0].when == date(2020, 4, 20)

