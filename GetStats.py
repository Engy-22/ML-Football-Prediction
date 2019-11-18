from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq


def get_SPStats():                  # return all td tags
    url = "https://www.footballoutsiders.com/stats/ncaa/2018"  # default URL to parse

    uClient = uReq(url)  # getting html info to parse
    page_soup = uClient.read()
    uClient.close()

    page_soup = soup(page_soup, "html.parser")  # parsing html page
    AllStats = page_soup.findAll("td")
    return AllStats


def cull(lst):              # only gets information for name, overall, offense, defense, special teams
    teams = 130
    ret = []
    print(len(lst))
    for i in range(0, teams):
        ret.append(lst[0].text)
        ret.append(lst[5].text)
        ret.append(lst[7].text)
        ret.append(lst[9].text)
        ret.append(lst[11].text)
        for r in range(15):
            lst.pop(0)

    return ret


if __name__=='__main__':
    SPStats = get_SPStats()
    print(SPStats)
    SPStats = cull(SPStats)
    print(SPStats)