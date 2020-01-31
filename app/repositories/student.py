from dataclasses import asdict
from typing import List
from datetime import datetime

import boto3

from app.models import Grade, Student
from app import settings


class StudentRepository:

    def __init__(self,
                 table_name=settings.HOGWARTS_MAIN_TABLE_NAME,
                 session=None):
        self.table_name = table_name
        _session = session if session is not None else boto3.Session()
        self.dynamodb = _session.resource('dynamodb')
        self.table = self.dynamodb.Table(self.table_name)


    def update(self, student: Student):
        """
        Save the given student in the database.
        """
        _student_id = 'student:{}'.format(student.id)

        now = datetime.now().isoformat()

        result = self.table.update_item(
            Key={
                'pk': _student_id,
                'sk': student.created_at,
            },
            UpdateExpression="set first_name = :fn, last_name = :ln, grades = :g, updated_at = :u",
            ExpressionAttributeValues={
                ':fn': student.first_name,
            ':ln': student.last_name,
                ':g': [asdict(grade) for grade in student.grades],
                ':u': now,
            },
            ReturnValues='NONE'
        )
        return result

    # def all(self):
        # return [Student(id) for id in ["00002401", "00002138"]]
    def all(self) -> List[Grade]:
        """
        Returns all existing students.
        """
        students = []
        for item in self.table.scan()["Items"]:

            grades =[]
            for grade in item.get('grades'):
                grades.append(Grade(
                    grade.get('when'),
                    grade.get('subject'),
                    grade.get('type'),
                    grade.get('value'),
                    grade.get('comment'),
                    grade.get('teacher')
                ))

            students.append(Student(
                item.get('pk').split(":")[1],
                item.get('first_name'),
                item.get('last_name'),
                grades,
                item.get('sk'), # created_at
                item.get('updated_at'),
            ))
        return students


