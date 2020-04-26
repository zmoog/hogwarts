from datetime import date

from jinja2 import Template

from app.repositories.student import StudentRepository
from app.scrapers import AssignmentScraper, GradeScraper

# https://jinja.palletsprojects.com/en/2.10.x/templates/
template = Template("""{% if grades %}
Ecco gli ultimi voti di {{ student.first_name }}:
{% for grade in grades %}
- {{ grade.when }}: {{ grade.value }} di {{ grade.subject }} da {{ grade.teacher }} ({{ grade.comment }})
{% endfor %}
{% else %}Oggi non ci sono nuovi voti per {{ student.first_name }}.{% endif %}
""")

assignments_template = Template("""{% if todays_assignments %}

Ecco i compiti in scadenza oggi per {{ student.first_name }}:

{% for assignment in todays_assignments %}
- {{ assignment.when }}: {{ assignment.homework }}
{% endfor %}

{% else %}Oggi non ci sono compiti in scadenza per {{ student.first_name }}.{% endif %}

{% if future_assignments %}
I seguenti giorni hanno compiti da completare:
{% for assignment in future_assignments %}
- {{ assignment.when }}: {{ assignment.homework }}
{% endfor %}

{% endif %}
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
            new_grades.sort(key=lambda grade: grade.when, reverse=True)

            self.notifier.send(
                template.render(
                    student=student,
                    grades=new_grades
            ))
            
            if new_grades:
                # store latest grades for future reference
                student.grades += new_grades
                self.repository.update(student)


class PublishAssignmentsHandler:

    def __init__(self,
                 repository: StudentRepository,
                 scraper: AssignmentScraper,
                 notifier
                 ):
        self.repository = repository
        self.scraper = scraper
        self.notifier = notifier

    def handle(self, event, context):
        students = self.repository.all()
        assignments = self.scraper.all([student.id for student in students])
        today = date.today()

        for student in students: 

            todays_assignments = []
            past_assignments = []
            future_assignments = []

            for assignment in assignments[student.id]:
                if assignment.when < today:
                    past_assignments.append(assignment)
                if assignment.when == today:
                    todays_assignments.append(assignment)
                if assignment.when > today:
                    future_assignments.append(assignment)

            # todays_assignments = list(filter(lambda a: a.when == today, assignments[student.id]))
            self.notifier.send(
                assignments_template.render(
                    student=student,
                    todays_assignments=todays_assignments,
                    past_assignments=past_assignments,
                    future_assignments=future_assignments
            ))
