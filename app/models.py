from datetime import date
from dataclasses import dataclass


@dataclass
class Grade:
    when: str
    subject: str
    type: str
    value: str
    comment: str
    teacher: str


@dataclass
class Credentials:
    customer_id: str
    username: str
    password: str
