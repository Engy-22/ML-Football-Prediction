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


def get_efficiency_stats(url):                  # return all td tags
    #url = "http://www.espn.com/college-football/statistics/teamratings/_/year/2018/tab/efficiency"  # default URL to parse

    uClient = uReq(url)  # getting html info to parse
    page_soup = uClient.read()
    uClient.close()

    page_soup = soup(page_soup, "html.parser")  # parsing html page
    AllStats = page_soup.findAll("td")
    stats = []
    for i in range(len(AllStats)):              # getting only text version
        stats.append(AllStats[i].text)

    stats = stats[8:]       # cuts off unnecessary information at the beginning

    return stats


def espn_codes(name):
    code = {"Boston College": "103", "Clemson": "228", "Florida State": "52", "Louisville": "97", "NC State": "152",
            "Syracuse": "193", "Wake Forest": "154", "Duke": "150", "Georgia Tech": "59", "Miami-FL": "2390",
            "North Carolina": "153", "Pittsburgh": "221", "Virginia": "258", "Virginia Tech": "259", "Georgia": "61",
            "Florida": "57", "Tennessee": "2633", "South Carolina": "2579", "Kentucky": "96", "Missouri": "142",
            "Vanderbilt": "238", "LSU": "99", "Alabama": "333", "Texas A&M": "245", "Auburn": "2",
            "Mississippi State": "344", "Ole Miss": "145", "Arkansas": "8"}

    return code[name]


def get_all_team_rankings_espn(url):
    lst = get_efficiency_stats(url)
    teams = {}
    while len(lst) != 0:
        name = parse_name_espn(lst[0])          # save name for dictionary location
        name = name_cheak_espn(name)
        team = lst[1:5]                         # stats from espn efficiency rating
        teams[name] = team     # stored at the teams name
        lst = lst[6:]

    return teams


def name_cheak_espn(name):      # see if names need changing from nicknames on espn
    if name == "FSU":
        return "Florida State"
    elif name == "S Carolina":
        return "South Carolina"
    elif name == "Pitt":
        return "Pittsburgh"
    elif name == "UVA":
        return "Virginia"
    elif name == "VT":
        return "Virginia Tech"
    elif name == "Miss St":
        return "Mississippi State"
    elif name == "Miami":
        return "Miami-FL"
    else:
        return name


def parse_name_espn(name):
    for i in name:
        if name[-1] == ',':     # if you hit a comma that the whole name
            return name[:-1]
        else:
            name = name[:-1]    # take off one letter and loop


def cull(lst):              # only gets information for name, overall, offense, defense, special teams
    numberOfTeams = len(lst)
    team = []
    teams = {}
    for i in range(0, numberOfTeams, 15):
        team.append(lst[5+i].text)
        team.append(lst[7+i].text)
        team.append(lst[9+i].text)
        team.append(lst[11+i].text)
        teams[lst[0+i].text] = team         # stats located at the teams name

        team = []   # reset list for next team

    return teams


def get_all_teams_rankings():           # gets all S&P+ rankings
    stats = get_SPStats()
    stats = cull(stats)
    return stats


def compare_get_schedules(team, SP, espnRankings, soFar):
    year = 2018
    url = "https://www.espn.com/college-football/team/schedule/_/id/"
    urlEnd = "/season/"
    url = url + espn_codes(team) + urlEnd + str(year)
    outcomes, teams = GetSchedule.get_all_outcomes_on_schedule(url)

    allGames = []   # will store complete list of games for data
    game = []       # will store one game at a time

    for i in range(len(outcomes)):
        print(teams[i])
        if teams[i] in SP and teams[i] in espnRankings and (team, teams[i]) not in soFar:         # if it's not in the dictionary then the team isn't D1
            game = game + SP[team] + espnRankings[team] + SP[teams[i]] + espnRankings[teams[i]]
            game.append(outcomes[teams[i]])     # append outcome to stats
            allGames.append(game)
            #print(allGames)
            game = []       # clear list for next team
            soFar[(teams[i], team)] = ""
        else:
            continue

    if ("Florida", "Florida State") in soFar:
        print("Its working!!!")
    return allGames



if __name__ == '__main__':
    code = {"Boston College": "103", "Clemson": "228", "Florida State": "52", "Louisville": "97", "NC State": "152",
            "Syracuse": "193", "Wake Forest": "154", "Duke": "150", "Georgia Tech": "59", "Miami-FL": "2390",
            "North Carolina": "153", "Pittsburgh": "221", "Virginia": "258", "Virginia Tech": "259", "Georgia": "61",
            "Florida": "57", "Tennessee": "2633", "South Carolina": "2579", "Kentucky": "96", "Missouri": "142",
            "Vanderbilt": "238", "LSU": "99", "Alabama": "333", "Texas A&M": "245", "Auburn": "2",
            "Mississippi State": "344", "Ole Miss": "145", "Arkansas": "8"}


    SP = get_all_teams_rankings()
    #outcomes, teams = GetSchedule.get_all_outcomes_on_schedule("https://www.espn.com/college-football/team/schedule/_/id/52/season/2018")

    espnRankings = get_all_team_rankings_espn("http://www.espn.com/college-football/statistics/teamratings/_/year/2018/tab/efficiency")
    soFar = {}
    allGames = []
    for i in code:
        allGames = allGames + compare_get_schedules(i, SP, espnRankings, soFar)

    print()
    for i in allGames:
        print(i)
