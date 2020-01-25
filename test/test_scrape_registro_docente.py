
from lxml import html


def test_registro_classe():
    page = open('./tests/data/registro_docente.html', 'r').read()
    
    tree = html.fromstring(page)

    trs = tree.xpath('//*[@id="votiEle"]/div/table/tbody/tr')

    assert len(trs) == 27

    for tr in trs:

        # print(dir(tr))

        # print(tr.tag)

        tds = tr.xpath('td')

        print(f'there are {len(tds)} tds')
        for td in tds:
            # print(dir(td))
            # print(td.text)
            print("[", td.text_content(), "]")
            

        assert False

        # for td in trs:
        #     print(td)



# //*[@id="votiEle"]/div/table/tbody/tr[1]/td[4]/span