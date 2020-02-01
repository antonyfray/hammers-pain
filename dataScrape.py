# taken from https://fcpython.com/blog/introduction-scraping-data-transfermarkt
import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
'''
page = "https://www.transfermarkt.co.uk/transfers/transferrekorde/statistik/top/plus/0/galerie/0?saison_id=2000"
pageTree = requests.get(page, headers=headers)
pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

Players = pageSoup.find_all("a", {"class": "spielprofil_tooltip"})
print(Players[0].text)

Values = pageSoup.find_all("td", {"class": "rechts hauptlink"})
print(Values[0].text)
'''
# Begin Andy Carroll injury scrape
page = "https://www.transfermarkt.co.uk/andy-carroll/verletzungen/spieler/48066"
pageTree = requests.get(page, headers=headers)
pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

# Get and store nDaysInjured
daysInjArr= []
DaysInjured = pageSoup.find_all("td", {"class": "rechts"})
for i in DaysInjured:
  if "days" in i.text:
    daysInjArr.append(i.text.split()[0])

for i in daysInjArr:
  print("Days inj = {}".format(i))

# Get and store club player is signed to while injured
# wappen is German for coat of arms i.e. club badge. All of the img sources have this in their endpoint
clubInjArr = []
ClubInjuredFor = pageSoup.find_all("img", src=lambda x: x and 'wappen' in x)
for i in ClubInjuredFor:
  clubInjArr.append(i["alt"])
# current code also picks up current club as an extra entry (badge at top of screen) so we need to remove that
del(clubInjArr[0])

for i in clubInjArr:
  print("Club inj for = {}".format(i))

# Get and store injury type
typeInjArr= []
# Many classes have hauptlink in name but we want an exact match
# most recent injury is also highlighted red (bg_rot_20) so we need to collect that too
TypeOfInjury = pageSoup.find_all(lambda tag: tag.name == 'td' and (tag.get('class') == ['hauptlink'] or tag.get('class') == ['hauptlink','bg_rot_20'])) 
for i in TypeOfInjury:
  print(i.text)
  typeInjArr.append(i.text)

for i in typeInjArr:
  print("Type of injury = {}".format(i))

multiArr = []
multiArr.append(typeInjArr)
multiArr.append(clubInjArr)
multiArr.append(daysInjArr)
print("type len = {}".format(len(typeInjArr)))
print("club len = {}".format(len(clubInjArr)))
print("days len = {}".format(len(daysInjArr)))
if not all(len(i) == len(multiArr[0]) for i in multiArr):
  sys.exit("Arrays are not all the same length. This is a problem.")
# TODO Store
# 1) Total number of days injured - done (just need to sum daysInjArr)
# 2) Total number of individual injury occurences
# 3) Club player was signed to when injured - done
# 4) Type of injury (is it the same one every time?)

# TODO Check
# 1) Ensure arrs are all the same length

# TODO Functionality
# 1) If there are multiple pages of injury history, need a way to know how many pages of info there are
# - Can add "ajax/yw1/page/2" to link but at some point we won't get a 200
