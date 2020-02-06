from datetime import date
from dataclasses import dataclass
from typing import List

DATE_FORMAT = '%d/%m/%Y'


@dataclass
class Grade:
    when: date
    subject: str
    type: str
    value: str
    comment: str
    teacher: str

    def __hash__(self):
        return hash((self.when, self.subject, self.type, self.value, self.teacher))

    def __post_init__(self):
        # I'm using this to avoid having empty
        # string on attributes saved in DynamoDB.
        if self.comment == '':
            self.comment = '.'

@dataclass
class Student:
    id: str
    first_name: str
    last_name: str
    grades: List[Grade]
    created_at: date
    updated_at: date


@dataclass
class Credentials:
    customer_id: str
    username: str
    password: str
