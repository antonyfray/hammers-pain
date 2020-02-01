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

#print(pageSoup)
daysInjArr= []
DaysInjured = pageSoup.find_all("td", {"class": "rechts"})
for i in DaysInjured:
  if "days" in i.text:
    daysInjArr.append(i.text.split()[0])

for i in daysInjArr:
  print("Days inj = {}".format(i))

# TODO Store
# 1) Total number of days injured
# 2) Total number of individual injury occurences
# 3) Club player was signed to when injured
# 4) Type of injury (is it the same one every time?)
