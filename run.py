
from bauhaus import Encoding, proposition, constraint, utils, print_theory

import random
import time
# Encoding that will store all of your constraints
E = Encoding()

# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@proposition(E)
class Day:

    def __init__(self, day):
        self.day = day

    def __repr__(self):
        return f"Day({self.day})"

@proposition(E)
class PlayGame:

    def __init__(self, day, team):
        self.team = team
        self.day = day

    def __repr__(self):
        return f"PlayGame({self.day}, {self.team})"
# @constraint.at_most_k(E, 13)   # at most 13 back to back game, adding this line cuase my computer to freeze when running the program
@proposition(E)
class BackToBackGame:

    def __init__(self, day):
        self.day = day

    def __repr__(self):
        return f"BackToBackGame({self.day})"
@proposition(E)
class West:
    def __init__(self, team):                          #represent if a team is in West, we can also use it to track number of games if needed, just an idea for how to
                                                       #set up the proposition for teams, If this work, then all other zone can have the same format.
        self.team = team

    def __repr__(self):
        return f"West({self.team})"
@proposition(E)
class countGame:
    def __init__(self, team, time):
        self.team = team
        self.time = time

    def __repr__(self):
        return f"PlayGame({self.team}, {self.time})"
    
# List of all team, assuming we pick bulls
AtlanticList=["Celtics","Nets","Knicks","76ers","Raptors","Wizard"]
CentralList=["Cavaliers","Pistons","Pacers", "Bucks"]
SouthEastList=["Hawks","Hornets","Heat","Magic"]
WestList=['Nuggets','Timberwolves','Thunder','Blazers','Jazz','Warriors','Clippers','Lakers','Suns','Kings','Mavericks','Rockets','Grizzlies','Pelicans','Spurs']
AllTeam=['Nuggets','Timberwolves','Thunder','Blazers','Jazz','Warriors','Clippers','Lakers','Suns','Kings','Mavericks','Rockets','Grizzlies','Pelicans','Spurs',"Hawks","Hornets","Heat","Magic" ,
         "Wizard","Cavaliers","Pistons","Pacers", "Bucks","Celtics","Nets","Knicks","76ers","Raptors"]
# Create proposition
BackToBackList=[]
# Create 182 day object
# Not sure how to set 82 of the Day object to be true. Even if we use random, how do we set a Proposition variable to be true?
day=list(range(180))
for i in range(1,181):
    day[i-1]=Day(i)
    
# Create all back to back games
# This does not account for the fact that we can not have back to back games on the last day of season,this can be added in the constraint
for i in range (180):
    BackToBackList.append(BackToBackGame(i+1))
# Create all play game object



played = []

def count(list,team):
    count = 0
    for i in list:
        if i.team == team:
            count += 1
    return count


#  Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def nba_theory():
    for i in range(0, 180):
        if i == 0:
            E.add_constraint(BackToBackList[i] >> (~day[i+2] & day[i] & day[i+1]))
            E.add_constraint((~BackToBackList[i]&day[i]) >> (~day[i+1] & day[i+2]))
        elif i==len(day)-1:
            continue
        elif i == len(day) - 3:
            E.add_constraint((BackToBackList[i]) >> (~day[i-1] & day[i] & day[i+1]&~BackToBackList[i+1]))
            E.add_constraint((~BackToBackList[i]&day[i]) >> (~day[i+1] & day[i+2]))
        elif i==len(day) -2:
            E.add_constraint((~BackToBackList[i]&day[i]) >> ~day[i+1])
        else:
            E.add_constraint((BackToBackList[i]) >> (~day[i-1] & day[i] & day[i+1] & ~day[i+2]))
            E.add_constraint((~BackToBackList[i]&day[i]) >> (~day[i+1] & day[i+2]))

    i=1
    while(len(played)<82):
        team=random.randint(0,28)
        if AllTeam[team] in WestList:
            if count(played,AllTeam[team])<=2:
                played.append(PlayGame(i,AllTeam[team]))
                E.add_constraint(played[-1])
                i+=1
        elif AllTeam[team] in AtlanticList:
            if count(played,AllTeam[team])<=4:
                played.append(PlayGame(i,AllTeam[team]))
                E.add_constraint(played[-1])
                i+=1
        elif AllTeam[team] in CentralList:
            if count(played,AllTeam[team])<=4:
                played.append(PlayGame(i,AllTeam[team]))
                E.add_constraint(played[-1])
                i+=1
        elif AllTeam[team] in SouthEastList:
            if count(played,AllTeam[team])<=3:
                played.append(PlayGame(i,AllTeam[team]))
                E.add_constraint(played[-1])
                i+=1

    ### Older version of our constraints that does not make sure our team plays the correct number of games with other teams.
    # for i in range(len(day)):
    #    constraint.add_at_most_one(E, playList[i])
    #    E.add_constraint(day[i] >> (playList[i][0]|playList[i][1]|playList[i][2]|playList[i][3]|playList[i][4]|playList[i][5]|playList[i][6]|playList[i][7]|
    #                                playList[i][8]|playList[i][9]|playList[i][10]|
    #                                playList[i][11]|playList[i][12]|playList[i][13]|playList[i][14]|playList[i][15]|playList[i][16]|playList[i][17]
    #                                |playList[i][18]|playList[i][19]|playList[i][20]|playList[i][21]|
    #                                playList[i][22]|playList[i][23]|playList[i][24]|playList[i][25]|playList[i][26]|playList[i][27]|playList[i][28]))
    #    E.add_constraint(~day[i] >> ~(playList[i][0]|playList[i][1]|playList[i][2]|playList[i][3]|playList[i][4]|playList[i][5]|playList[i][6]|playList[i][7]
    #                                |playList[i][8]|playList[i][9]|playList[i][10]|
    #                                playList[i][11]|playList[i][12]|playList[i][13]|playList[i][14]|playList[i][15]|playList[i][16]|playList[i][17]|
    #                                playList[i][18]|playList[i][19]|playList[i][20]|playList[i][21]|
    #                                playList[i][22]|playList[i][23]|playList[i][24]|playList[i][25]|playList[i][26]|playList[i][27]|playList[i][28]))
        
    return E

if __name__ == "__main__":

    T = nba_theory()
    # Don't compile until you're finished adding all your constraints!

    compile_start = time.time()
    T = T.compile()
    compile_end = time.time()
    compile_total_time = compile_end - compile_start
    print("Compile time: ", compile_total_time)
    print("\nSatisfiable: %s" % T.satisfiable())
    # print("# Solutions: %d" % count_solutions(T))

    solve_start = time.time()
    # Store the result in a dictionary
    dict1 = T.solve()
    solve_end = time.time()
    solve_total_time = solve_end - solve_start
    print("Solve time: ", solve_total_time)

    # The list of days that a game is played
    list_days = []
    # The list of games that played
    list_game = []
    # The list of BackToBack games
    list_btb = []

    # for keys in dict1:
    #     if dict1.get(keys) == True:
    #         print(keys, dict1.get(keys))

    for key in dict1:
        if type(key) == type(PlayGame(day, "")) and dict1.get(key) == True:
            list_game.append([key, dict1.get(key)])
        elif type(key) == type(BackToBackGame(day)):
            list_btb.append([key, dict1.get(key)])
        elif type(key) == type(Day(day)) and dict1.get(key) == True:
            list_days.append([key, dict1.get(key)])
        else:
            continue

    sort_start = time.time()

    # We used insertion sort to sort the result.
    for i in range(0, len(list_days)):
        key = list_days[i][0].day
        j = i - 1
        while j >= 0 and key < list_days[j][0].day:
            tmp = list_days[j + 1]
            list_days[j + 1] = list_days[j]
            list_days[j] = tmp
            j -= 1

    for i in range(0, len(list_game)):
        key = list_game[i][0].day
        j = i - 1
        while j >= 0 and key < list_game[j][0].day:
            tmp = list_game[j + 1]
            list_game[j + 1] = list_game[j]
            list_game[j] = tmp
            j -= 1

    ### This part is the deprecated sorting for BackToBack games.
    # for i in range(0, len(list_btb)):
    #    key = list_btb[i][0].day
 
    #    # Move elements of arr[0..i-1], that are
    #    # greater than key, to one position ahead
    #    # of their current position
    #    j = i - 1
    #    while j >= 0 and key < list_btb[j][0].day:
    #            tmp = list_btb[j + 1]
    #            list_btb[j + 1] = list_btb[j]
    #            list_btb[j] = tmp
    #            j -= 1

               
    sort_end = time.time()
    sort_total_time = sort_end - sort_start
    print("Sort time: ", sort_total_time)
    print()
    # Prints the theory
    print_theory(dict1, "objects")
    print()

    # Formatting string for the output.
    formation = "{0:^12}\t\t{1:^12}\t\t{2:^12}"
    print(formation.format("Game number:", "Play with:", "Play on day:"))
    print("--------------------------------------------------------------------------------")
    # Loop the sorted game list and prints out the final schedule.
    for index in range(len(list_game)):
        print(formation.format(list_game[index][0].day, list_game[index][0].team, list_days[index][0].day))
