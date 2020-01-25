import os
import pytest

from app.models import Credentials
from app.navigator import Navigator
from app.scrapers import GradeScraper
from app.repositories.student import StudentRepository


@pytest.fixture(scope='session')
def credentials() -> Credentials:
    return Credentials(
        get_environment_variable("AXIOS_CUSTOMER_ID"),
        get_environment_variable("AXIOS_USERNAME"),
        get_environment_variable("AXIOS_PASSWORD"),
    )


@pytest.fixture(scope='function')
def navigator(credentials: Credentials) -> Navigator:
    return Navigator(credentials)


@pytest.fixture(scope='function')
def grade_scraper(navigator: Navigator) -> GradeScraper:
    return GradeScraper(navigator)


@pytest.fixture(scope='function')
def student_repository() -> StudentRepository:
    return StudentRepository()


@pytest.fixture(scope='function')
def load_html() -> str:
    """
    Returns HTML page content from the data directory.
    """
    def _load_html(page_name: str) -> str:
        return open(f'./test/data/{page_name}.html', 'r').read()

    return _load_html


def get_environment_variable(variable_name):
    assert variable_name in os.environ and os.environ[variable_name], f"Missing environment variable '${variable_name}'"
    return os.environ[variable_name]
