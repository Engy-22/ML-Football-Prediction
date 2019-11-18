from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq


def get_td_tags():

    url = "https://www.espn.com/college-football/team/schedule/_/id/52/season/2018"  # default URL to parse

    uClient = uReq(url)  # getting html info to parse
    page_soup = uClient.read()
    uClient.close()

    page_soup = soup(page_soup, "html.parser")  # parsing html page
    AllStats = page_soup.findAll("td")
    return AllStats


def get_outcomes(tags):         # returns the name and the outcome of the game on a schedule
    tags = tags[9:]
    name = parse_name(tags[0])
    outcome = tags[1][0]        # outcome of the game is the first letter in the score
    return name, outcome


def parse_name(name):           # removes the 'vs' in front of the name and the ranking if any
    name = name[3:]
    for i in name:
        if i.isalpha():
            return name
        else:
            name = name[1:]     # if no ranking just return


if __name__=='__main__':
    test = []
    tags = get_td_tags()
    for i in tags:
        test.append(i.text)
    print("tags")
    print(len(test))
    print(test)
    get_outcomes(test)