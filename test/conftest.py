import os
import pytest

from app.models import Credentials


@pytest.fixture(scope='session')
def credentials():
    return Credentials(
        get_environment_variable("AXIOS_CUSTOMER_ID"),
        get_environment_variable("AXIOS_USERNAME"),
        get_environment_variable("AXIOS_PASSWORD"),
    )

def get_environment_variable(variable_name):
    assert variable_name in os.environ and os.environ[variable_name], f"Missing environment variable '${variable_name}'"
    return os.environ[variable_name]
