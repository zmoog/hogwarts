from lxml import html
from typing import List
from app.models import Grade


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
            tds[0].text_content(), # when
            tds[1].text_content(), # subject
            tds[2].text_content(), # type
            tds[3].text_content(), # value
            tds[4].text_content(), # comment
            tds[5].text_content(), # teacher
        ))

    return grades
