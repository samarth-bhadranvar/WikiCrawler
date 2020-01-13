# wiki_crawler
#Samarth Bhadranvar

Web crawler to extract number of launches with atleast one payload status being successful, operational or en route for every day in 2019
from https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches

Output File:
-orbital_launches_output.csv
-Format:
 ISO_date, int
 (space after ',' as per the description)

Env and libs:
-Python 3.7
-Requests 2.22.0
-BeautifulSoup 4.8.2