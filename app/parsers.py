from datetime import datetime
from lxml import html
from typing import List
from app.models import Assignment, Grade


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


def extract_assisgnments(page: str) -> List[Assignment]:
    """
    Parses and extract student's assignment from the 'registro di classe' HTML page.
    """
    tree = html.fromstring(page)
    trs = tree.xpath('//*[@id="content-comunicazioni"]/table/tbody/tr')

    assignments = []

    for tr in trs:
        tds = tr.xpath('td')
        # print('when', tds[0].xpath('string()'))
        # print('when', tds[0].xpath('text()'))
        date_text = tds[0].xpath('i')[0].tail

        when = datetime.strptime(date_text,'%d/%m/%Y').date()
        homework = tds[2].text_content()

        assignments.append(Assignment(
            when,
            homework
        ))

    return assignments
