from datetime import datetime
from lxml import html
from typing import List
from app.models import Grade, DATE_FORMAT


def extract_grades(page) -> List[Grade]:
    """
    Parses and extract student's grade from the HTML page.
    """
    tree = html.fromstring(page)
    trs = tree.xpath('//*[@id="votiEle"]/div/table/tbody/tr')

    grades =[]

    for tr in trs:
        tds = tr.xpath('td')
        grades.append(Grade(
            datetime.strptime(tds[0].text_content(), DATE_FORMAT), # when
            str(tds[1].text_content()), # subject
            str(tds[2].text_content()), # type
            str(tds[3].text_content()), # value
            str(tds[4].text_content()), # comment
            str(tds[5].text_content()), # teacher
        ))

    return grades
