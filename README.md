This repo will analyse whether the number of injuries a football player experiences throughout their career increases
after moving to West Ham.

To run, you must specify via CLI the player name of interest (in lower case, hyphen separated), along with their transfermarkt ID. I plan to add utility for determining the ID from the name at some point.

An example of a valid run configuration is
```
python dataScrape.py andy-carroll 48066
```
 Name        | ID  
 --- | ---
 andy-carroll | 48066
 kieron-dyer | 3118
 robert-snodgrass | 22614
 manuel-lanzini | 135853

# NOTE
This project is far from finished. I am slowly working on it in my spare time, but please appreciate this is not a "released" version,
or an accurate representation of the highest level to which I can code (well...)

tldr; this is a work in progress!

# TODO
- utility for looking up tfmarkt ID from player name
- accept list of players as arg
- investigate gitlab runners - if we use our own image, where will we store it, and will it cost money
- tighten security in general
- tidy dataScrape.py into functions, it's a massive mess
- write proper tests
- add mechanism to scrape multiple pages of injury history (so plots are actually correct)
