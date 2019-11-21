from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq


def get_td_tags(url):
    ret = []
    #url = "https://www.espn.com/college-football/team/schedule/_/id/52/season/2018"  # default URL to parse

    uClient = uReq(url)  # getting html info to parse
    page_soup = uClient.read()
    uClient.close()

    page_soup = soup(page_soup, "html.parser")  # parsing html page
    AllStats = page_soup.findAll("td")

    for i in AllStats:
        ret.append(i.text)

    return ret


def get_outcomes(tags):         # returns the name and the outcome of the game on a schedule
    name = parse_name(tags[0])
    outcome = tags[1][0]        # outcome of the game is the first letter in the score
    return name, outcome


def parse_name(name):           # removes the 'vs' in front of the name and the ranking if any
    name = name[2:]
    for i in name:
        if i.isalpha():
            return name[:-1]
        else:
            name = name[1:]     # if no ranking just return


def get_all_outcomes_on_schedule(url):      # main function to call helpers, returns all the games from a given url
    games = {}
    tags = get_td_tags(url)         # get all the tags for the list
    tags = tags[9:]
    team = []

    for i in range(12):
        game, outcome = get_outcomes(tags)

        if outcome == "C" or outcome == "P":
            continue
        if outcome == "W":
            outcome = 1
        else:
            outcome = 0
        team.append(game)
        games[game] = outcome       # add to found so far
        tags = tags[7:]             # move to next game

    return games, team


if __name__=='__main__':
    dic, teams = get_all_outcomes_on_schedule("")