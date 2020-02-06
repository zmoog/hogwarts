from datetime import datetime
from app.handlers import PublishLatestGradesHandler
from app.scrapers import GradeScraper
from app.models import Grade, Student

data_path = f"./testdata/placebo/app/handlers/{__name__}"


def test_publish(mocker, student_repository, grade_scraper, notifier):


    cases = [{
        'scraper': [
            {'00002401': [
                Grade(when=datetime(2020, 1, 20), subject='GEOGRAFIA', type='Orale', value='8', comment='La collina.', teacher='Carmigno Alessandra'),
                Grade(when=datetime(2020, 1, 21), subject='GEOGRAFIA', type='Orale', value='9', comment='La collina.', teacher='Carmigno Alessandra'),
                Grade(when=datetime(2020, 1, 23), subject='GEOGRAFIA', type='Orale', value='10', comment='La collina.', teacher='Carmigno Alessandra'),
            ]},
        ],
        'repository': [
            Student(
                '00002401',
                'Filippo',
                'Branca',
                [Grade(when=datetime(2020, 1, 21), subject='GEOGRAFIA', type='Orale', value='9', comment='La collina.', teacher='Carmigno Alessandra')],
                datetime.fromisoformat('2020-01-26T09:05:35.692104'),
                datetime.fromisoformat('2020-01-26T09:05:35.692104')
        )],
        'result': """
Ecco gli ultimi voti di Filippo:

- 23/01/2020: 10 di GEOGRAFIA da Carmigno Alessandra (La collina.)

- 20/01/2020: 8 di GEOGRAFIA da Carmigno Alessandra (La collina.)

"""
    },
    {
        'scraper': [
            {'00002401': [
                Grade(when=datetime(2020, 1, 22), subject='GEOGRAFIA', type='Orale', value='9', comment='La collina.', teacher='Carmigno Alessandra'),
            ]},
        ],
        'repository': [
            Student(
                '00002401',
                'Filippo',
                'Branca',
                [Grade(when=datetime(2020, 1, 22), subject='GEOGRAFIA', type='Orale', value='9', comment='La collina.', teacher='Carmigno Alessandra')],
                datetime.fromisoformat('2020-01-26T09:05:35.692104'),
                datetime.fromisoformat('2020-01-26T09:05:35.692104')
        )],
        'result': """Oggi non ci sono nuovi voti per Filippo."""
    }]

    mocker.patch.object(grade_scraper, "all")
    mocker.patch.object(student_repository, "all")
    mocker.patch.object(notifier, "send")


    for case in cases:

        # reset mock objects
        grade_scraper.all.reset_mock()
        student_repository.all.reset_mock()
        notifier.send.reset_mock()

        # set side effects
        grade_scraper.all.side_effect = case['scraper']
        student_repository.all.side_effect = [case['repository']]
        notifier.send.side_effect = None

        # execute
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

        notifier.send.assert_called_with(case['result'])
