from app.handlers import PublishLatestGradesHandler
from app.scrapers import GradeScraper
from app.models import Grade
from app.notification.pushover import PushoverNotifier


def test_publish(mocker, student_repository, grade_scraper):

    notifier = PushoverNotifier()

    mocker.patch.object(grade_scraper, "all")
    grade_scraper.all.side_effect = [{'00002401': [Grade(when='22/01/2020', subject='GEOGRAFIA', type='Orale', value='9', comment='La collina.', teacher='Carmigno Alessandra')]}]

    notifier_spy = mocker.spy(notifier, "send")

    publisher = PublishLatestGradesHandler(
        student_repository,
        grade_scraper,
        notifier
    )

    event = {
        "account": "123456789012",
        "region": "us-east-2",
        "detail": {},
        "detail-type": "Scheduled Event",
        "source": "aws.events",
        "time": "2019-03-01T01:23:45Z",
        "id": "cdc73f9d-aea9-11e3-9d5a-835b769c0d9c",
        "resources": [
            "arn:aws:events:us-east-1:123456789012:rule/my-schedule"
        ]
    }
    context = {}

    publisher.handle(event, context)

    notifier_spy.assert_called_once()
    # assert len(notifier_spy.spy_return) > 0
