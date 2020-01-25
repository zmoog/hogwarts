import os

#
# https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html
#
from app.handlers import PublishLatestGradesHandler
from app.repositories.student import StudentRepository
from app.scrapers import Navigator
from app.scrapers import Credentials
from app.scrapers import GradeScraper
from app.notification.pushover import PushoverNotifier
from app.notification.telegram import TelegramNotifier
from app import settings

creds = Credentials(
    settings.AXIOS_CUSTOMER_ID,
    settings.AXIOS_USERNAME,
    settings.AXIOS_PASSWORD
)

publisher = PublishLatestGradesHandler(
    StudentRepository(),
    GradeScraper(Navigator(creds)),
    TelegramNotifier(
        settings.TELEGRAM_TOKEN,
        settings.TELEGRAM_GROUP_CHAT_ID
    ))


def handler(event, context):
    """
    https://docs.aws.amazon.com/lambda/latest/dg/with-scheduled-events.html
    """

    print(event, context)

    publisher.handle(event, context)

    return {}