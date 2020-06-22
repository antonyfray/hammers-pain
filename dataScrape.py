# taken from https://fcpython.com/blog/introduction-scraping-data-transfermarkt
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def getDaysInj(injPageSoup):
    daysInjList = []
    DaysInjured = injPageSoup.find_all("td", {"class": "rechts"})
    for i in DaysInjured:
        if "days" in i.text:
            daysInjList.append(i.text.split()[0])

    for i in daysInjList:
        print("Days inj = {}".format(i))
    return daysInjList

def getClubInjFor(injPageSoup):
    # wappen is German for coat of arms i.e. club badge. All of the img sources have this in their endpoint
    clubInjList = []
    ClubInjuredFor = injPageSoup.find_all("img", src=lambda x: x and 'wappen' in x)
    for i in ClubInjuredFor:
        clubInjList.append(i["alt"])
        # current code also picks up current club as an extra entry (badge at top of screen) so we need to remove that
    del(clubInjList[0])

    for i in clubInjList:
        print("Club inj for = {}".format(i))
    return clubInjList

def getInjTypes(injPageSoup):
    typeInjList = []
    # Many classes have hauptlink in name but we want an exact match
    # most recent injury is also highlighted red (bg_rot_20) so we need to collect that too
    TypeOfInjury = injPageSoup.find_all(lambda tag: tag.name == 'td' and (tag.get('class') == ['hauptlink'] or tag.get('class') == ['hauptlink','bg_rot_20']))
    for i in TypeOfInjury:
        print(i.text)
        typeInjList.append(i.text)

    for i in typeInjList:
        print("Type of injury = {}".format(i))
    return typeInjList

def getTransferDates(tfPageSoup):
    tfDatesList = []
    tfDates = tfPageSoup.find_all(lambda tag: tag.name == 'td' and (tag.get('class') == ['zentriert','hide-for-small']))
    for i in tfDates:
        if "," in i.text:
            # need to convert date format into datetime object for processing
            tfDatesList.append(datetime.strptime(i.text, '%b %d, %Y'))

    print("Transfer dates:")
    for i in tfDatesList:
        print(i)
    return tfDatesList

def getDaysAtClub(tfPageSoup):
    daysAtClubList = []
    print("Days spent at each club")
    # Need to determine time spent at current club
    currentDate = datetime.now()
    for i in range(0,len(tfDatesList)):
        if i is 0:
            days = (currentDate - tfDatesList[i]).days
            print(days)
            daysAtClubList.append(days)
        else:
            days = (tfDatesList[i-1]-tfDatesList[i]).days
            print(days)
            daysAtClubList.append(days)
    return daysAtClubList

def getClubHistory(tfPageSoup):
    clubHistList = []
    clubHistory = tfPageSoup.find_all("img", src=lambda x: x and 'wappen' in x)

    for i in clubHistory:
        clubHistList.append(i["alt"])
    # current code also picks up current club as an extra entry (badge at top of screen) so we need to remove that
    del(clubHistList[0])

    return clubHistList[1::2]

def getClubTransfers(tfPageSoup):
    # TODO start of this is duplicated with the above. Should have one function that returns a list/tuple of lists
    clubTrnsList = []
    clubTransfers = tfPageSoup.find_all("img", src=lambda x: x and 'wappen' in x)

    for i in clubTransfers:
        clubTrnsList.append(i["alt"])
        # current code also picks up current club as an extra entry (badge at top of screen) so we need to remove that
    del(clubTrnsList[0])

    for i in range(0,len(clubTrnsList),2):
        if (i+1)==len(clubTrnsList):
            break
        print('From {} to {}'.format(clubTrnsList[i],clubTrnsList[i+1]))
    return clubTrnsList

if __name__ == "__main__":

    # User input
    playerName = sys.argv[1] # must be lower case
    playerID = sys.argv[2]
    print("playerName = {}".format(playerName))
    print("playerID = {}".format(playerID))

    # BeautifulSoup config
    headers = {'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    # Player scrape - injuries
    injPage = "https://www.transfermarkt.co.uk/"+playerName+"/verletzungen/spieler/"+playerID
    injPageTree = requests.get(injPage, headers=headers)
    injPageSoup = BeautifulSoup(injPageTree.content, 'html.parser')
    # Player scrape -transfers
    tfPage = "https://www.transfermarkt.co.uk/"+playerName+"/transfers/spieler/"+playerID
    tfPageTree = requests.get(tfPage, headers=headers)
    tfPageSoup = BeautifulSoup(tfPageTree.content, 'html.parser')

    # Get and store nDaysInjured
    daysInjList = getDaysInj(injPageSoup)

    # Get and store club player is signed to while injured
    clubInjList = getClubInjFor(injPageSoup)

    # Get and store injury type
    typeInjList = getInjTypes(injPageSoup)

    # Get date of transfer
    tfDatesList = getTransferDates(tfPageSoup)

    # Get days spent at each club
    daysAtClubList = getDaysAtClub(tfPageSoup)

    # Get clubs transferred between
    clubTrnsList = getClubTransfers(tfPageSoup)

    # Get list of clubs (to correspond to daysAtClub)
    clubHistList = getClubHistory(tfPageSoup)


# TODO figure out how this time normalisation will work - are we doing total days at club or by season?
# We need to use the above to determine how long a player played for each club
# Could do a function that takes clubTrnsArr and tfDatesArr and determines length of period at each club
# Then have two DF columns - club played for and time played for (in days)...but how would this work with transferring to and from clubs?
# Group by season? By time signed to club?
# Naive approach would be just add together all the days the player spent at the club, but that fails to account for e.g. one injury having a knockon
# effect (chronology of injuries).

    multiList = []
    multiList.append(typeInjList)
    multiList.append(clubInjList)
    multiList.append(daysInjList)
    print("type len = {}".format(len(typeInjList)))
    print("club len = {}".format(len(clubInjList)))
    print("days len = {}".format(len(daysInjList)))
    if not all(len(i) == len(multiList[0]) for i in multiList):
        sys.exit("Arrays are not all the same length. This is a problem.")

    # TODO plot in different file, read in dataframe and do it that way
    plt.bar(clubHistList,daysAtClubList, label=playerName)
    plt.xlabel("Club")
    plt.ylabel("Days Spent at Club")
    plt.legend(loc="upper right")
    fig1 = plt.gcf() # get current figure - before we save locally
    plt.show()
    plt.draw()
    fig1.savefig("clubVsDays.png")


# TODO
# Date of transfers between clubs (from https://www.transfermarkt.co.uk/andy-carroll/transfers/spieler/48066) - done
# This is so we can normalise time injured against time playing for the club
# Date format is e.g. Aug 31, 2013 so will need to be able to convert this into dateformat for time comparison

# TODO create a dataframe from what we scrape for use with seaborn


# TODO Functionality
# 1) If there are multiple pages of injury history, need a way to know how many pages of info there are
# - Can add "ajax/yw1/page/2" to link but at some point we won't get a 200
