from jinja2 import Template

from app.repositories.student import StudentRepository
from app.scrapers import GradeScraper

# https://jinja.palletsprojects.com/en/2.10.x/templates/
template = Template("""{% if grades %}
Ecco gli ultimi voti di {{ student.first_name }}:
{% for grade in grades %}
- {{ grade.when }}: {{ grade.value }} di {{ grade.subject }} da {{ grade.teacher }} ({{ grade.comment }})
{% endfor %}
{% else %}Oggi non ci sono nuovi voti per {{ student.first_name }}.{% endif %}
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

        for student in students: 

            yesterdays_grades = student.grades
            todays_grades = results[student.id]

            new_grades = list(set(todays_grades) - set(yesterdays_grades))

            self.notifier.send(
                template.render(
                    student=student,
                    grades=new_grades
            ))
            
            if new_grades:
                # store latest grades for future reference
                student.grades += new_grades
                self.repository.update(student)
