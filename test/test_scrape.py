
from lxml import html


def test_registro_classe():
    page = open('./test/data/registro_classe.html', 'r').read()
    
    tree = html.fromstring(page)

    trs = tree.xpath('//table[@class="TableRegistroClasseGenitori"]/tbody/tr')

    assert len(trs) == 2

    for tr in trs:

        # print(dir(tr))

        # print(tr.tag)

        tds = tr.xpath('td')

        print(f'there are {len(tds)} tds')
        for td in tds:
            # print(dir(td))
            # print(td.text)
            print(td.text)
            

        # for td in trs:
        #     print(td)

