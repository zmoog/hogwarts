import logging
import requests

from dataclasses import dataclass
from typing import List, Mapping

from lxml import html
from app.models import Credentials

START_URL = 'https://family.sissiweb.it/Secret/REStart.aspx?Customer_ID={customer_id}'
LOGIN_URL = 'https://family.axioscloud.it/Secret/RELogin.aspx'
FAMILY_URL = 'https://family.axioscloud.it/Secret/REFamily.aspx'


class Navigator:

    def __init__(self, credentials: Credentials):
        self.credentials = credentials

    def fetch_red(self, student_ids: List[str]) -> Mapping[str, str]:
        """
        Fetches the grades page for each given student id.
        """
        pages = {}
        with requests.Session() as session:

            state = self._login(session)
            headers = self._build_headers()

            #
            # Go to the family page
            #
            for student_id in student_ids:
                payload = {
                    '__EVENTTARGET': 'FAMILY',
                    '__EVENTARGUMENT': 'RED',
                    '__VIEWSTATE': state.viewstate,
                    '__VIEWSTATEGENERATOR': state.viewstategenerator,
                    '__EVENTVALIDATION': state.eventvalidation,

                    'ctl00$ContentPlaceHolderMenu$ddlAnno': '2019',
                    'ctl00$ContentPlaceHolderMenu$ddlFT': 'FT01',
                    'ctl00$ContentPlaceHolderBody$txtDataSelezionataCAL': '09/12/2019',
                    'ctl00$ContentPlaceHolderBody$txtFunctionSelected': 'nothing',
                    'ctl00$ContentPlaceHolderBody$txtAluSelected': student_id, # '00002401',
                    'ctl00$ContentPlaceHolderBody$txtIDAluSelected': '0',
                }

                resp = session.post(FAMILY_URL, data=payload, headers=headers)

                pages[student_id] = resp.text

        return pages

    def _build_headers(self):
        return {
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Host': 'family.sissiweb.it',
            'Origin': 'https://family.sissiweb.it',
            'Referer': START_URL.format(customer_id=self.credentials.customer_id),
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
        }

    def _login(self, session) -> (str, str, str):
        """
        Performs a new login using the given session.
        """

        headers = self._build_headers()

        #
        # Open the start page
        #        

        resp = session.get(START_URL.format(customer_id=self.credentials.customer_id))
        tree = html.fromstring(resp.text)

        viewstate = tree.xpath('//input[@id="__VIEWSTATE"]')
        viewstategenerator = tree.xpath('//input[@id="__VIEWSTATEGENERATOR"]')
        eventvalidation = tree.xpath('//input[@id="__EVENTVALIDATION"]')

        start_payload = {
            '__VIEWSTATE': viewstate[0].value,
            '__VIEWSTATEGENERATOR': viewstategenerator[0].value,
            '__EVENTVALIDATION': eventvalidation[0].value,
            'ibtnRE.x': 0,
            'ibtnRE.y': 0,
        }

        resp = session.post(
            START_URL.format(customer_id=self.credentials.customer_id),
            data=start_payload,
            headers=headers)

        tree = html.fromstring(resp.text)

        viewstate = tree.xpath('//input[@id="__VIEWSTATE"]')
        viewstategenerator = tree.xpath('//input[@id="__VIEWSTATEGENERATOR"]')
        eventvalidation = tree.xpath('//input[@id="__EVENTVALIDATION"]')

        #
        # Do the login
        #

        login_payload = {
            '__VIEWSTATE': viewstate[0].value,
            '__VIEWSTATEGENERATOR': viewstategenerator[0].value,
            '__EVENTVALIDATION': eventvalidation[0].value,
            'txtUser': self.credentials.username,
            'txtPassword': self.credentials.password,
            'btnLogin': 'Accedi',
        }

        resp = session.post(LOGIN_URL, data=login_payload, headers=headers)
        tree = html.fromstring(resp.text)

        viewstate = tree.xpath('//input[@id="__VIEWSTATE"]')
        viewstategenerator = tree.xpath('//input[@id="__VIEWSTATEGENERATOR"]')
        eventvalidation = tree.xpath('//input[@id="__EVENTVALIDATION"]')

        return State(
            viewstate[0].value,
            viewstategenerator[0].value,
            eventvalidation[0].value
        )


@dataclass
class State:
    viewstate: str
    viewstategenerator: str
    eventvalidation: str