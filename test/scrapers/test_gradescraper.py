from app.navigator import Navigator
from app.scrapers import GradeScraper
from app.models import Credentials, Grade


def test_all(mocker, navigator, load_html):
    
    mocker.patch.object(navigator, "fetch_red")
    navigator.fetch_red.side_effect = [
        {
            '00002401': load_html("registro_docente")
        }
    ]

    grade_scraper = GradeScraper(navigator)

    response = grade_scraper.all(['00002401'])

    assert len(response) is 1
    for student_id, grades in response.items():
        assert all([isinstance(grade, Grade) for grade in grades])
        # print(student_id, grades)
