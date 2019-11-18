from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import GetSchedule


def get_SPStats():                  # return all td tags
    url = "https://www.footballoutsiders.com/stats/ncaa/2018"  # default URL to parse

    uClient = uReq(url)  # getting html info to parse
    page_soup = uClient.read()
    uClient.close()

    page_soup = soup(page_soup, "html.parser")  # parsing html page
    AllStats = page_soup.findAll("td")
    return AllStats


def cull(lst):              # only gets information for name, overall, offense, defense, special teams
    numberOfTeams = len(lst)
    team = []
    teams = {}
    for i in range(0, numberOfTeams, 15):
        #team.append(lst[0+i].text)
        team.append(lst[5+i].text)
        team.append(lst[7+i].text)
        team.append(lst[9+i].text)
        team.append(lst[11+i].text)
        teams[lst[0+i].text] = team         # stats located at the teams name

        team = []   # reset list for next team

    return teams


def get_all_teams_rankings():
    stats = get_SPStats()
    stats = cull(stats)
    return stats


def compare_get_schedules(team, SP, teams, outcomes):
    allGames = []
    game = []
    for i in range(len(outcomes)):
        print(teams[i])
        if teams[i] in SP:
            game = game + SP[team] + SP[teams[i]]
            game.append(outcomes[teams[i]])
            allGames.append(game)
            print(allGames)
        else:
            continue

    return allGames


if __name__ == '__main__':
    SP = get_all_teams_rankings()
    #print(SP)
    outcomes, teams = GetSchedule.get_all_outcomes_on_schedule("https://www.espn.com/college-football/team/schedule/_/id/52/season/2018")
    #print(outcomes)
    #print(teams)

    print(compare_get_schedules("Florida State", SP, teams, outcomes))




