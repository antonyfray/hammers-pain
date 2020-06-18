# taken from https://fcpython.com/blog/introduction-scraping-data-transfermarkt
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import sys

def getDaysInj(injPageSoup):
    daysInjLst = []
    DaysInjured = injPageSoup.find_all("td", {"class": "rechts"})
    for i in DaysInjured:
        if "days" in i.text:
            daysInjLst.append(i.text.split()[0])

    for i in daysInjLst:
        print("Days inj = {}".format(i))
    return daysInjLst

def getClubInjFor(injPageSoup):
    # wappen is German for coat of arms i.e. club badge. All of the img sources have this in their endpoint
    clubInjLst = []
    ClubInjuredFor = injPageSoup.find_all("img", src=lambda x: x and 'wappen' in x)
    for i in ClubInjuredFor:
        clubInjLst.append(i["alt"])
        # current code also picks up current club as an extra entry (badge at top of screen) so we need to remove that
    del(clubInjLst[0])

    for i in clubInjLst:
        print("Club inj for = {}".format(i))
    return clubInjLst

def getInjTypes(injPageSoup):
    typeInjLst = []
    # Many classes have hauptlink in name but we want an exact match
    # most recent injury is also highlighted red (bg_rot_20) so we need to collect that too
    TypeOfInjury = injPageSoup.find_all(lambda tag: tag.name == 'td' and (tag.get('class') == ['hauptlink'] or tag.get('class') == ['hauptlink','bg_rot_20']))
    for i in TypeOfInjury:
        print(i.text)
        typeInjLst.append(i.text)

    for i in typeInjLst:
        print("Type of injury = {}".format(i))
    return typeInjLst

def getTransferDates(tfPageSoup):
    tfDatesLst = []
    tfDates = tfPageSoup.find_all(lambda tag: tag.name == 'td' and (tag.get('class') == ['zentriert','hide-for-small']))
    for i in tfDates:
        if "," in i.text:
            # need to convert date format into datetime object for processing
            tfDatesLst.append(datetime.strptime(i.text, '%b %d, %Y'))

    print("Transfer dates:")
    for i in tfDatesLst:
        print(i)
    return tfDatesLst

def getDaysAtClub(tfPageSoup):
    daysAtClubLst = []
    print("Days spent at each club")
    # Need to determine time spent at current club
    currentDate = datetime.now()
    for i in range(0,len(tfDatesLst)):
        if i is 0:
            days = (currentDate - tfDatesLst[i]).days
            print(days)
            daysAtClubLst.append(days)
        else:
            days = (tfDatesLst[i-1]-tfDatesLst[i]).days
            print(days)
            daysAtClubLst.append(days)
    return daysAtClubLst

def getClubTransfers(tfPageSoup):
    clubTrnsLst = []
    clubTransfers = tfPageSoup.find_all("img", src=lambda x: x and 'wappen' in x)

    for i in clubTransfers:
        clubTrnsLst.append(i["alt"])
        # current code also picks up current club as an extra entry (badge at top of screen) so we need to remove that
    del(clubTrnsLst[0])

    for i in range(0,len(clubTrnsLst),2):
        if (i+1)==len(clubTrnsLst):
            break
        print('From {} to {}'.format(clubTrnsLst[i],clubTrnsLst[i+1]))
    return clubTrnsLst

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
    daysInjLst = getDaysInj(injPageSoup)

    # Get and store club player is signed to while injured
    clubInjLst = getClubInjFor(injPageSoup)

    # Get and store injury type
    typeInjLst = getInjTypes(injPageSoup)

    # Get date of transfer
    tfDatesLst = getTransferDates(tfPageSoup)

    # Get days spent at each club
    daysAtClubLst = getDaysAtClub(tfPageSoup)

    # Get clubs transferred between
    clubTrnsList = getClubTransfers(tfPageSoup)

# TODO figure out how this time normalisation will work - are we doing total days at club or by season?
# We need to use the above to determine how long a player played for each club
# Could do a function that takes clubTrnsArr and tfDatesArr and determines length of period at each club
# Then have two DF columns - club played for and time played for (in days)...but how would this work with transferring to and from clubs?
# Group by season? By time signed to club?
# Naive approach would be just add together all the days the player spent at the club, but that fails to account for e.g. one injury having a knockon
# effect (chronology of injuries).

    multiLst = []
    multiLst.append(typeInjLst)
    multiLst.append(clubInjLst)
    multiLst.append(daysInjLst)
    print("type len = {}".format(len(typeInjLst)))
    print("club len = {}".format(len(clubInjLst)))
    print("days len = {}".format(len(daysInjLst)))
    if not all(len(i) == len(multiLst[0]) for i in multiLst):
        sys.exit("Arrays are not all the same length. This is a problem.")


#
# Manipulate arrays etc, plot stuff, do calculates of relevant stats
#


# TODO Store
# 1) Total number of days injured - done (just need to sum daysInjArr)
# 2) Total number of individual injury occurences
# 3) Club player was signed to when injured - done
# 4) Type of injury (is it the same one every time?) - done
# 5) Date of transfers between clubs (from https://www.transfermarkt.co.uk/andy-carroll/transfers/spieler/48066) - done
# This is so we can normalise time injured against time playing for the club
# Date format is e.g. Aug 31, 2013 so will need to be able to convert this into dateformat for time comparison
# 6) Date of injury
# TODO Check
# 1) Ensure arrs are all the same length

# TODO Functionality
# 1) If there are multiple pages of injury history, need a way to know how many pages of info there are
# - Can add "ajax/yw1/page/2" to link but at some point we won't get a 200
