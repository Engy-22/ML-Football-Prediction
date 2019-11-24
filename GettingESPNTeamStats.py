from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import csv
import GetSchedule


def get_ESPN_stats(year):                  # return all td tags
    url = "https://www.espn.com/college-football/stats/team/_/view/defense/stat/total/season/"
    url2 = "/table/passing/sort/yardsPerGame/dir/asc"  # default URL to parse
    url = url + str(year)
    url = url + url2

    uClient = uReq(url)  # getting html info to parse
    page_soup = uClient.read()
    uClient.close()

    page_soup = soup(page_soup, "html.parser")  # parsing html page
    AllStats = page_soup.findAll("td")
    stats = []

    for i in range(len(AllStats)):              # getting only text version
        stats.append(AllStats[i].text)

    NUMBER_OF_TEAMS = 130

    PASS_BIAS = 134
    RUSH_BIAS = 136
    SCORE_BIAS = 138


    dic = {}

    for i in range(0, NUMBER_OF_TEAMS):
        dic[name_cheak_espn(stats[i])] = [float(stats[(i*9)+PASS_BIAS]), float(stats[(i*9) + RUSH_BIAS]),
                         float(stats[(i*9)+SCORE_BIAS])]

    url = "https://www.espn.com/college-football/stats/team/_/season/"
    url = url + str(year)

    uClient = uReq(url)  # getting html info to parse
    page_soup = uClient.read()
    uClient.close()

    page_soup = soup(page_soup, "html.parser")  # parsing html page
    AllStats = page_soup.findAll("td")
    stats = []

    for i in range(len(AllStats)):  # getting only text version
        stats.append(AllStats[i].text)

    for i in range(0, NUMBER_OF_TEAMS):
        dic[name_cheak_espn(stats[i])] = dic[name_cheak_espn(stats[i])] + [float(stats[(i*9) + PASS_BIAS]),
                                                                           float(stats[(i*9) + RUSH_BIAS]),
                                                                           float(stats[(i*9) + SCORE_BIAS])]

    return dic


# Standardizes names of team when reading in from espn
def name_cheak_espn(name):      # see if names need changing from nicknames on espn

    if name == "Miami":
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
    elif name == "Ohio State Buckeyes":
        return "Ohio State"
    elif name == "Nebraska Cornhuskers":
        return "Nebraska"
    elif name == "Clemson Tigers":
        return "Clemson"
    elif name == "Utah Utes":
        return "Utah"
    elif name == "Wisconsin Badgers":
        return "Wisconsin"
    elif name == "Michigan Wolverines":
        return "Michigan"
    elif name == "Georgia Bulldogs":
        return "Georgia"
    elif name == "Missouri Tigers":
        return "Missouri"
    elif name == "Pittsburgh Panthers":
        return "Pittsburgh Panthers"
    elif name == "Iowa Hawkeyes":
        return "Iowa"
    elif name == "Florida Gators":
        return "Florida"
    elif name == "Oregon Ducks":
        return "Oregon"
    elif name == "Minnesota Golden Gophers":
        return "Minnesota"
    elif name == "Minnesota Golden Gophers":
        return "Minnesota"
    elif name == "Minnesota Golden Gophers":
        return "Minnesota"
    elif name == "Miami Hurricanes":
        return "Miami"
    elif name == "Penn State Nittany Lions":
        return "Penn State"
    elif name == "Indiana Hoosiers":
        return "Indiana"
    elif name == "Virginia Cavaliers":
        return "Virginia"
    elif name == "Auburn Tigers":
        return "Auburn"
    elif name == "Texas A&M Aggies":
        return "Texas A&M"
    elif name == "TCU Horned Frogs":
        return "TCU"
    elif name == "Alabama Crimson Tide":
        return "Alabama"
    elif name == "Notre Dame Fighting Irish":
        return "Notre Dame"
    elif name == "Kentucky Wildcats":
        return "Kentucky"
    elif name == "Michigan State Spartans":
        return "Michigan State"
    elif name == "Kentucky Wildcats":
        return "Kentucky"
    elif name == "Northwestern Wildcats":
        return "Northwestern"
    elif name == "Tennessee Volunteers":
        return "Tennessee"
    elif name == "Oklahoma Sooners":
        return "Oklahoma"
    elif name == "Washington Huskies":
        return "Washington"
    elif name == "Baylor Bears":
        return "Baylor"
    elif name == "Iowa State Cyclones":
        return "Iowa State"
    elif name == "Kansas State Wildcats":
        return "Kansas State"
    elif name == "Virginia Tech Hokies":
        return "Virginia Tech"
    elif name == "LSU Tigers":
        return "LSU"
    elif name == "Duke Blue Devils":
        return "Duke"
    elif name == "NC State Wolfpack":
        return "NC State"
    elif name == "Arizona State Sun Devils":
        return "Arizona State"
    elif name == "South Carolina Gamecocks":
        return "South Carolina"
    elif name == "California Golden Bears":
        return "Cal"
    elif name == "Mississippi State Bulldogs":
        return "Mississippi"
    elif name == "USC Trojans":
        return "USC"
    elif name == "BYU Cougars":
        return "BYU"
    elif name == "North Carolina Tar Heels":
        return "North Carolina"
    elif name == "Georgia Tech Yellow Jackets":
        return "Georgia Tech"
    elif name == "Wake Forest Demon Deacons":
        return "Wake Forest"
    elif name == "West Virginia Mountaineers":
        return "West Virginia"
    elif name == "Oklahoma State Cowboys":
        return "Oklahoma State"
    elif name == "Ole Miss Rebels":
        return "Ole Miss"
    elif name == "Stanford Cardinal":
        return "Stanford"
    elif name == "Louisville Cardinals":
        return "Louisville"
    elif name == "Florida State Seminoles":
        return "Florida State"
    elif name == "Oregon State Beavers":
        return "Oregon State"
    elif name == "Syracuse Orange":
        return "Syracuse"
    elif name == "UCLA Bruins":
        return "UCLA"
    elif name == "Maryland Terrapins":
        return "Maryland"
    elif name == "Arkansas Razorbacks":
        return "Arkansas"
    elif name == "Rutgers Scarlet Knights":
        return "Rutgers"
    elif name == "Texas Longhorns":
        return "Texas"
    elif name == "Washington State Cougars":
        return "Washington State"
    elif name == "Colorado Buffaloes":
        return "Colorado"
    elif name == "Kansas Jayhawks":
        return "Kansas"
    elif name == "Vanderbilt Commodores":
        return "Vanderbilt"
    elif name == "Texas Tech Red Raiders":
        return "Texas Tech"
    elif name == "Arizona Wildcats":
        return "Arizona"
    elif name == "Boston College Eagles":
        return "Boston College"
    else:
        return name


# uses get schedule module to retrieve the teams played and outcomes for each team
def get_schedule(TEAM, codes, YEAR):
    url = "https://www.espn.com/college-football/team/schedule/_/id/"
    urlEnd = "/season/"
    url = url + codes[TEAM] + urlEnd + str(YEAR)
    print(str(TEAM))
    outcomes, teams = GetSchedule.get_all_outcomes_on_schedule(url)

    return outcomes, teams


# saves all information to NAME in csv format, line line per game
def save_to_csv(games, NAME):
    NAME = NAME + ".csv"

    with open(NAME, 'w', newline='') as lines:
        """games.insert(0, ["D_pass", "D_rush", "D_pts", "O_pass", "O_rush",
                         "O_pts", "BD_pass", "BD_rush","BD_pts",
                         "BO_pass","BO_rush","BO_pts","outcome"])"""
        for game in games:
            thewriter = csv.writer(lines)  # writing to csv
            thewriter.writerow(game)


# Saves two CSV files and combines them into one
def save_to_one_csv(GAMES1, GAMES2):
    GAMES1 = GAMES1 + ".csv"
    GAMES2 = GAMES2 + ".csv"

    reader = csv.reader(open(GAMES1))
    GAMES1 = list(reader)
    reader = csv.reader(open(GAMES2))
    GAMES2 = list(reader)

    myGAMES = GAMES1 + GAMES2
    print(myGAMES)

    myGAMES.insert(0, ["D_pass", "D_rush", "D_pts", "O_pass", "O_rush",
                         "O_pts", "BD_pass", "BD_rush","BD_pts",
                         "BO_pass","BO_rush","BO_pts","outcome"])

    save_to_csv(myGAMES, "games")


if __name__ == '__main__':
    codes = {"Boston College": "103", "Clemson": "228", "Florida State": "52", "Louisville": "97", "NC State": "152",
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


    """ YEAR = 2018
    TEST_TEAM = "Boston College"
    toSave = []

    stats = get_ESPN_stats(YEAR)
    print(stats)

    saved = 0
    for team in stats:
        if team in codes:
            saved = saved + 1
            outcomes, teams = get_schedule(team, codes, YEAR)
            if saved == 25:
                print("\nSaved some\n")
                save_to_csv(toSave, "ESPN_2018")
            for i in range(0, len(teams)):

                if teams[i] in stats:
                    toSave.append(stats[team] + stats[teams[i]] + [int(outcomes[teams[i]])])


    print("FSU")
    print(stats["Florida State"])

    save_to_csv(toSave, "ESPN_2018")
    for game in toSave:
        if len(game) != 13:
            print(len(game))

    print(toSave) """

    save_to_one_csv("ESPN_2018", "ESPN_2019")