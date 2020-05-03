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


# TODO
- utility for looking up tfmarkt ID from player name
- accept list of players as arg
- investigate gitlab runners - if we use our own image, where will we store it, and will it cost money
- tighten security in general
- tidy dataScrape.py into functions, it's a massive mess
- write proper tests
