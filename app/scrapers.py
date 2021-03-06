from datetime import date

from typing import List, Mapping

from app.models import Assignment, Credentials, Grade
from app.navigator import Navigator
from app.parsers import extract_assisgnments, extract_grades


class GradeScraper:
    """
    GradeScraper fetches the grades from the school's website.
    """
    def __init__(self, navigator: Navigator):
        self.navigator = navigator

    def all(self, student_ids: List[str]) -> Mapping[str, List[Grade]]:
        """
        Returns all grades for each student the the ``student_ids`` list.
        """
        pages = self.navigator.fetch_red(student_ids, '2019', 'FT02')

        return dict(map(lambda kv: (kv[0],  extract_grades(kv[1])), pages.items()))


class AssignmentScraper:
    """
    AssignmentScraper fetches the assignments from the school's website.
    """
    def __init__(self, navigator: Navigator):
        self.navigator = navigator

    def all(self, student_ids: List[str]) -> Mapping[str, List[Assignment]]:
        """
        Returns all assignments for each student the the ``student_ids`` list.
        """
        pages = self.navigator.fetch_rec(student_ids, '2019', 'FT02')

        return dict(map(lambda kv: (kv[0],  extract_assisgnments(kv[1])), pages.items()))
