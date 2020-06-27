# taken from https://fcpython.com/blog/introduction-scraping-data-transfermarkt
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# BeautifulSoup config
headers = {'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

class Player():
    # After init, accessible properties of class:
    # playerName - Name of player
    # playerID - ID of player on transfermarkt
    # injPageSoup - BeautifulSoup for player's injury history page
    # tfPageSoup - BeautifulSoup for player's transfer history page
    # daysInjList - List of days player was injured for for each injury instance
    # clubInjList - List of clubs player was signed to for each injury instance
    # typeInjList - List of injury types player suffered with
    # tfDatesList - List of dates on which player transferred from one club to another
    # clubHistList - List of clubs player was signed to

    def __init__(self, playerName, playerID):
        self.playerName = playerName
        self.playerID = playerID # TODO add utility to obtain playerID from playerName, rather than have user pass it
        self.setPageSoups()
        self.scrapeDaysInj()
        self.scrapeClubInjFor()
        self.scrapeInjTypes()
        self.scrapeTransferDates()
        self.scrapeClubHistory()

    def setPageSoups(self):
        # Injuries
        injPage = "https://www.transfermarkt.co.uk/"+self.playerName+"/verletzungen/spieler/"+self.playerID
        injPageTree = requests.get(injPage, headers=headers)
        self.injPageSoup = BeautifulSoup(injPageTree.content, 'html.parser')

        # Transfers
        tfPage = "https://www.transfermarkt.co.uk/"+playerName+"/transfers/spieler/"+playerID
        tfPageTree = requests.get(tfPage, headers=headers)
        self.tfPageSoup = BeautifulSoup(tfPageTree.content, 'html.parser')

    def scrapeDaysInj(self):
        self.daysInjList = []
        DaysInjured = self.injPageSoup.find_all("td", {"class": "rechts"})
        for i in DaysInjured:
            if "days" in i.text:
                self.daysInjList.append(i.text.split()[0])

        for i in self.daysInjList:
            print("Days inj = {}".format(i))

    def scrapeClubInjFor(self):
        # wappen is German for coat of arms i.e. club badge. All of the img sources have this in their endpoint
        self.clubInjList = []
        ClubInjuredFor = self.injPageSoup.find_all("img", src=lambda x: x and 'wappen' in x)
        for i in ClubInjuredFor:
            self.clubInjList.append(i["alt"])
        # current code also picks up current club as an extra entry (badge at top of screen) so we need to remove that
        del(self.clubInjList[0])

        for i in self.clubInjList:
            print("Club inj for = {}".format(i))

    def scrapeInjTypes(self):
        self.typeInjList = []
        # Many classes have hauptlink in name but we want an exact match
        # most recent injury is also highlighted red (bg_rot_20) so we need to collect that too
        TypeOfInjury = self.injPageSoup.find_all(lambda tag: tag.name == 'td' and (tag.get('class') == ['hauptlink'] or tag.get('class') == ['hauptlink','bg_rot_20']))
        for i in TypeOfInjury:
            print(i.text)
            self.typeInjList.append(i.text)

        for i in self.typeInjList:
            print("Type of injury = {}".format(i))

    def scrapeTransferDates(self):
        self.tfDatesList = []
        tfDates = self.tfPageSoup.find_all(lambda tag: tag.name == 'td' and (tag.get('class') == ['zentriert','hide-for-small']))
        for i in tfDates:
            if "," in i.text:
                # need to convert date format into datetime object for processing
                self.tfDatesList.append(datetime.strptime(i.text, '%b %d, %Y'))

        print("Transfer dates:")
        for i in self.tfDatesList:
            print(i)

    def scrapeClubHistory(self):
        self.clubHistList = []
        clubHistory = self.tfPageSoup.find_all("img", src=lambda x: x and 'wappen' in x)

        for i in clubHistory:
            self.clubHistList.append(i["alt"])
        # current code also picks up current club as an extra entry (badge at top of screen) so we need to remove that
        del(self.clubHistList[0])
        # History obtained above prints (Club 1 --> Club 2, Club 2 --> Club 3, so we need to remove duplicates from final result)
        self.clubHistList = self.clubHistList[1::2]
        self.printClubTransfers()

    def printClubTransfers(self):
        for i in range(0,len(self.clubHistList),2):
            if (i+1)==len(self.clubHistList):
                break
            print('From {} to {}'.format(self.clubHistList[i],self.clubHistList[i+1]))

    def calcTotalDaysInjured(self):
        daysInjDict = {}
        for i in range(0,len(self.clubInjList),1):
            if self.clubInjList[i] in daysInjDict:
                daysInjDict[self.clubInjList[i]] += float(self.daysInjList[i])
            else:
                daysInjDict[self.clubInjList[i]] = float(self.daysInjList[i])

        for key, value in daysInjDict.items():
            print("Club: {} Days: {}".format(key,value))
        return daysInjDict

    def calcDaysAtClub(self):
        daysAtClubList = []
        print("Days spent at each club")
        # Need to determine time spent at current club
        currentDate = datetime.now()
        for i in range(0,len(self.tfDatesList)):
            if i is 0:
                days = (currentDate - self.tfDatesList[i]).days
                print(days)
                daysAtClubList.append(days)
            else:
                days = (self.tfDatesList[i-1]-self.tfDatesList[i]).days
                print(days)
                daysAtClubList.append(days)
        return daysAtClubList

if __name__ == "__main__":

    # User input
    playerName = sys.argv[1] # TODO enforce string and add lower-case
    playerID = sys.argv[2] #TODO enforce integer

    playerInQuestion = Player(playerName,playerID)
    print("playerName = {}".format(playerInQuestion.playerName))
    print("playerID = {}".format(playerInQuestion.playerID))

    clubHistList = playerInQuestion.clubHistList
    daysAtClubList = playerInQuestion.calcDaysAtClub()
    daysInjDict = playerInQuestion.calcTotalDaysInjured()

    # TODO update below to use proper test syntax and methods
    multiList = []
    multiList.append(playerInQuestion.typeInjList)
    multiList.append(playerInQuestion.clubInjList)
    multiList.append(playerInQuestion.daysInjList)
    print("type len = {}".format(len(playerInQuestion.typeInjList)))
    print("club len = {}".format(len(playerInQuestion.clubInjList)))
    print("days len = {}".format(len(playerInQuestion.daysInjList)))
    if not all(len(i) == len(multiList[0]) for i in multiList):
        sys.exit("Arrays are not all the same length. This is a problem.")

    # TODO plot in different file, read in dataframe and do it that way
    plt.bar(clubHistList,daysAtClubList,color='b',label='Days at Club')
    plt.bar(daysInjDict.keys(),daysInjDict.values(),alpha=0.5,color='r',label='Days Injured')
    plt.xlabel("Club")
    plt.ylabel("Days")
    plt.legend(loc="upper right")
    fig1 = plt.gcf() # get current figure - before we save locally
    plt.show()
    plt.draw()
    fig1.savefig(playerName+".png")


# TODO
# Date of transfers between clubs (from https://www.transfermarkt.co.uk/andy-carroll/transfers/spieler/48066) - done
# This is so we can normalise time injured against time playing for the club
# Date format is e.g. Aug 31, 2013 so will need to be able to convert this into dateformat for time comparison

# TODO create a dataframe from what we scrape for use with seaborn


# TODO Functionality
# 1) If there are multiple pages of injury history, need a way to know how many pages of info there are
# - Can add "ajax/yw1/page/2" to link but at some point we won't get a 200

# TODO figure out how this time normalisation will work - are we doing total days at club or by season?
# We need to use the above to determine how long a player played for each club
# Could do a function that takes clubTrnsArr and tfDatesArr and determines length of period at each club
# Then have two DF columns - club played for and time played for (in days)...but how would this work with transferring to and from clubs?
# Group by season? By time signed to club?
# Naive approach would be just add together all the days the player spent at the club, but that fails to account for e.g. one injury having a knockon
# effect (chronology of injuries).
