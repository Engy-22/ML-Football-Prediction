from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import GetSchedule
import csv


def get_SPStats(year):                  # return all td tags
    url = "https://www.footballoutsiders.com/stats/ncaa/"  # default URL to parse
    url = url + str(year)
    uClient = uReq(url)  # getting html info to parse
    page_soup = uClient.read()
    uClient.close()

    page_soup = soup(page_soup, "html.parser")  # parsing html page
    AllStats = page_soup.findAll("td")
    return AllStats


def get_efficiency_stats(year):                  # return all td tags
    url = "http://www.espn.com/college-football/statistics/teamratings/_/year/"  # default URL to parse
    urlEnd = "/tab/efficiency"
    url = url + str(year)
    url = url + urlEnd
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
            "Mississippi State": "344", "Ole Miss": "145", "Arkansas": "8", "Ohio State": "194", "Penn State": "213",
            "Michigan": "130", "Indiana": "84", "Maryland": "120", "Rutgers": "164",
            "Minnesota": "135", "Wisconsin": "275", "Iowa": "2294", "Illinois": "356", "Purdue": "2509",
            "Nebraska": "158", "Northwestern": "77", "Oregon": "2483", "Oregon State": "204", "Washington": "264",
            "Stanford": "24", "California": "25", "Washington State": "265", "Utah": "254", "USC": "30", "UCLA": "26",
            "Arizona State": "9", "Arizona": "12", "Colorado": "38", "Oklahoma": "201", "Baylor": "239",
            "Oklahoma State": "197", "Iowa State": "66", "Texas": "251", "Kansas State": "2306", "TCU": "2628",
            "Texas Tech": "2641", "West Virginia": "277", "Kansas": "2305", "Notre Dame": "87"}

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
    elif name == "Mich. St":
        return "Michigan State"
    elif name == "Oregon St":
        return "Oregon State"
    elif name == "Cal":
        return "California"
    elif name == "Washington St":
        return "Washington State"
    elif name == "UNC":
        return "North Carolina"
    elif name == "OSU":
        return "Ohio State"
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


def get_all_teams_rankings(year):           # gets all S&P+ rankings
    stats = get_SPStats(year)
    stats = cull(stats)
    return stats


def compare_get_schedules(team, SP, espnRankings, soFar, year):
    url = "https://www.espn.com/college-football/team/schedule/_/id/"
    urlEnd = "/season/"
    url = url + espn_codes(team) + urlEnd + str(year)
    print(str(team))
    outcomes, teams = GetSchedule.get_all_outcomes_on_schedule(url)

    allGames = []   # will store complete list of games for data
    game = []       # will store one game at a time

    for i in range(len(outcomes)):
        # if it's not in the dictionary then the team isn't D1
        if teams[i] in SP and teams[i] in espnRankings and (team, teams[i]) not in soFar:
            game = game + SP[team] + espnRankings[team] + SP[teams[i]] + espnRankings[teams[i]]
            game.append(outcomes[teams[i]])     # append outcome to stats
            allGames.append(game)

            game = []       # clear list for next team
            soFar[(teams[i], team)] = ""
        else:
            continue

    return allGames


def save_to_csv(games, file):
    file = file + ".csv"
    with open(file, 'w', newline='') as lines:
        for game in games:
            thewriter = csv.writer(lines)  # writing to csv
            thewriter.writerow(game)


def save_to_games():
    with open('games.csv', 'w', newline='') as lines:
        for line in open("games2017.csv"):
            csv_row = line.split()
            thewriter = csv.writer(lines)  # writing to csv
            thewriter.writerow(csv_row)

        for line in open("games2018.csv"):
            csv_row = line.split()
            thewriter = csv.writer(lines)  # writing to csv
            thewriter.writerow(csv_row)


if __name__ == '__main__':
    code = {"Boston College": "103", "Clemson": "228", "Florida State": "52", "Louisville": "97", "NC State": "152",
            "Syracuse": "193", "Wake Forest": "154", "Duke": "150", "Georgia Tech": "59", "Miami-FL": "2390",
            "North Carolina": "153", "Pittsburgh": "221", "Virginia": "258", "Virginia Tech": "259", "Georgia": "61",
            "Florida": "57", "Tennessee": "2633", "South Carolina": "2579", "Kentucky": "96", "Missouri": "142",
            "Vanderbilt": "238", "LSU": "99", "Alabama": "333", "Texas A&M": "245", "Auburn": "2",
            "Mississippi State": "344", "Ole Miss": "145", "Arkansas": "8", "Ohio State": "194", "Penn State": "213",
            "Michigan": "130", "Indiana": "84", "Maryland": "120", "Rutgers": "164",
            "Minnesota": "135", "Wisconsin": "275", "Iowa": "2294", "Illinois": "356", "Purdue": "2509",
            "Nebraska": "158", "Northwestern": "77", "Oregon": "2483", "Oregon State": "204", "Washington": "264",
            "Stanford": "24", "California": "25", "Washington State": "265", "Utah": "254", "USC": "30", "UCLA": "26",
            "Arizona State": "9", "Arizona": "12", "Colorado": "38", "Oklahoma": "201", "Baylor": "239",
            "Oklahoma State": "197", "Iowa State": "66", "Texas": "251", "Kansas State": "2306", "TCU": "2628",
            "Texas Tech": "2641", "West Virginia": "277", "Kansas": "2305", "Notre Dame": "87"}

    year = 2017

    SP = get_all_teams_rankings(year)
    espnRankings = get_all_team_rankings_espn(year)

    soFar = {}
    allGames = []

    for name in code:
        allGames = allGames + compare_get_schedules(name, SP, espnRankings, soFar, year)

    save_to_csv(allGames, "games2017")

    year = year + 1
    SP = get_all_teams_rankings(year)
    espnRankings = get_all_team_rankings_espn(year)
    soFar = {}
    allGames = []
    for name in code:
        allGames = allGames + compare_get_schedules(name, SP, espnRankings, soFar, year)
    save_to_csv(allGames, "games2018")

    print()
    for i in allGames:
        print(i)


    save_to_games()
