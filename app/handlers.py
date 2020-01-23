from app.repositories.student import StudentRepository
from app.scrapers import GradeScraper


class PublishLatestGradesHandler:

    def __init__(self,
                 repository: StudentRepository,
                 scraper: GradeScraper,
                 slack):
        self.repository = repository
        self.scraper = scraper
        self.slack = slack

    def handle(self, event, context):

        students = repository.all()
        # students = self.scraper.all(["00002401", "00002138"])
