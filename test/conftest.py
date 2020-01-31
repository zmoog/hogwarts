import os
import pytest
import boto3
import placebo

from app.models import Credentials
from app.navigator import Navigator
from app.scrapers import GradeScraper
from app.repositories.student import StudentRepository
from app.notification.telegram import TelegramNotifier
from app import settings


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


# @pytest.fixture(scope='function')
# def student_repository() -> StudentRepository:
#     return StudentRepository(settings.HOGWARTS_MAIN_TABLE_NAME)

@pytest.fixture(scope="function")
def student_repository(boto_session):
    return StudentRepository(session=boto_session)


@pytest.fixture(scope="function")
def notifier():
    return TelegramNotifier(
        settings.TELEGRAM_TOKEN,
        settings.TELEGRAM_GROUP_CHAT_ID)


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


@pytest.fixture(scope='module')  # 'function' or 'module'
def boto_session(request):
    data_path = getattr(request.module, "data_path", "./testdata/placebo")

    session = boto3.session.Session()
    pill = placebo.attach(session, data_path=data_path)

    if os.getenv('PLACEBO_MODE', "playback").lower() == 'record':
        pill.record()
    else:
        pill.playback()
    yield session




