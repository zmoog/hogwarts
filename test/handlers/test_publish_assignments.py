from datetime import date
from app.handlers import PublishAssignmentsHandler
from app.models import Assignment, Student

data_path = f"./testdata/placebo/app/handlers/{__name__}"


def test_publish(mocker, student_repository, assignment_scraper, notifier):
    cases = [
        {
            'scraper': [
                {
                    '00002401': [
                        Assignment(date.today(), 'bla bla')
                    ]
                }
            ],
            'repository': [
                Student(
                    '00002401',
                    'Filippo',
                    'Branca',
                    [],
                    '2020-01-26T09:05:35.692104',
                    '2020-01-26T09:05:35.692104')                
            ],
            'result': """

Ecco i compiti in scadenza oggi per Filippo:


- 2020-04-26: bla bla




"""
        }
    ]

    mocker.patch.object(assignment_scraper, "all")
    mocker.patch.object(student_repository, "all")
    mocker.patch.object(notifier, "send")

    for case in cases:

        # reset mock objects
        assignment_scraper.all.reset_mock()
        student_repository.all.reset_mock()
        notifier.send.reset_mock()

        # set side effects
        assignment_scraper.all.side_effect = case['scraper']
        student_repository.all.side_effect = [case['repository']]
        notifier.send.side_effect = None

        # execute
        publisher = PublishAssignmentsHandler(
            student_repository,
            assignment_scraper,
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
