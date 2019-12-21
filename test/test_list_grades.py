from app.navigator import Navigator
from app.scrapers import GradeScraper
from app.models import Credentials, Grade


def test_list_grades(credentials):
    
    navigator = Navigator(credentials)
    grade_scraper = GradeScraper(navigator)

    response = grade_scraper.all(['00002401'])

    print(response)

    # assert False
    assert len(response) is 1
    for student_id, grades in response.items():
        assert all([isinstance(grade, Grade) for grade in grades])
        print(student_id, grades)

    assert False
