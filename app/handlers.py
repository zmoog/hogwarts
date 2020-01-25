from jinja2 import Template
from app.repositories.student import StudentRepository
from app.scrapers import GradeScraper

# https://jinja.palletsprojects.com/en/2.10.x/templates/
template = Template("""
Ecco gli ultimi voti di {{ student_id }}:

{% for grade in grades %}
- {{ grade.when }}: {{ grade.value }} di {{ grade.subject }} da {{ grade.teacher }}
{% endfor %}
""")


class PublishLatestGradesHandler:

    def __init__(self,
                 repository: StudentRepository,
                 scraper: GradeScraper,
                 notifier
                 ):
        self.repository = repository
        self.scraper = scraper
        self.notifier = notifier

    def handle(self, event, context):

        students = self.repository.all()
        results = self.scraper.all([student.id for student in students])
        
        for student_id, grades in results.items():
            self.notifier.send(
                template.render(
                    student_id=student_id,
                    grades=grades[:5]
            ))
