import logging
import requests

from lxml import html

START_URL = 'https://family.sissiweb.it/Secret/REStart.aspx?Customer_ID=91014810013'
FAMILY_URL = 'https://family.axioscloud.it/Secret/REFamily.aspx'


# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

def main():
    with requests.Session() as session:

        resp = session.get(START_URL)

        print(resp.status_code)

        tree = html.fromstring(resp.text)

        viewstate = tree.xpath('//input[@id="__VIEWSTATE"]')
        viewstategenerator = tree.xpath('//input[@id="__VIEWSTATEGENERATOR"]')
        eventvalidation = tree.xpath('//input[@id="__EVENTVALIDATION"]')

        # print(viewstate, viewstategenerator, eventvalidation)

        start_payload = {
            '__VIEWSTATE': viewstate[0].value,
            '__VIEWSTATEGENERATOR': viewstategenerator[0].value,
            '__EVENTVALIDATION': eventvalidation[0].value,
            'ibtnRE.x': 0,
            'ibtnRE.y': 0,
        }
        # print('start_payload', start_payload)

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Host': 'family.sissiweb.it',
            'Origin': 'https://family.sissiweb.it',
            'Referer': START_URL,
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
        }
        resp = session.post(START_URL, data=start_payload, headers=headers)
        # print(resp.status_code)
        # print(resp.headers.get('location'))

        tree = html.fromstring(resp.text)

        viewstate = tree.xpath('//input[@id="__VIEWSTATE"]')
        viewstategenerator = tree.xpath('//input[@id="__VIEWSTATEGENERATOR"]')
        eventvalidation = tree.xpath('//input[@id="__EVENTVALIDATION"]')

        # print(viewstate, viewstategenerator, eventvalidation)        

        login_payload = {
            '__VIEWSTATE': viewstate[0].value,
            '__VIEWSTATEGENERATOR': viewstategenerator[0].value,
            '__EVENTVALIDATION': eventvalidation[0].value,
            'txtUser': 'user',
            'txtPassword': 'password',
            'btnLogin': 'Accedi',
        }
        # print('login_pay load', login_payload)

        resp = session.post('https://family.axioscloud.it/Secret/RELogin.aspx', data=login_payload, headers=headers)
        print(resp.status_code)
        print(resp.text)



        tree = html.fromstring(resp.text)

        viewstate = tree.xpath('//input[@id="__VIEWSTATE"]')
        viewstategenerator = tree.xpath('//input[@id="__VIEWSTATEGENERATOR"]')
        eventvalidation = tree.xpath('//input[@id="__EVENTVALIDATION"]')

        # print(viewstate, viewstategenerator, eventvalidation)        

        payload = {
            '__EVENTTARGET': 'FAMILY',
            '__EVENTARGUMENT': 'REC',
            '__VIEWSTATE': viewstate[0].value,
            '__VIEWSTATEGENERATOR': viewstategenerator[0].value,
            '__EVENTVALIDATION': eventvalidation[0].value,

            'ctl00$ContentPlaceHolderMenu$ddlAnno': '2019',
            'ctl00$ContentPlaceHolderMenu$ddlFT': 'FT01',
            'ctl00$ContentPlaceHolderBody$txtDataSelezionataCAL': '17/11/2019',
            'ctl00$ContentPlaceHolderBody$txtFunctionSelected': 'nothing',
            'ctl00$ContentPlaceHolderBody$txtAluSelected': '00002401',
            'ctl00$ContentPlaceHolderBody$txtIDAluSelected': '0',
        }
        # print('payload', payload)

        resp = session.post(FAMILY_URL, data=payload, headers=headers)
        print(resp.status_code)
        print(resp.text)

        tree = html.fromstring(resp.text)

        tds = tree.xpath('//table[@class="TableRegistroClasseGenitori"]/tbody/tr')

        for td in tds:
            print(td)


main()
