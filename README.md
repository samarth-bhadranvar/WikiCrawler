# WikiCrawler
#Samarth Bhadranvar

Web crawler to extract number of launches with atleast one payload status being successful, operational or en route for every day in 2019
from https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches
<br/>
<br/>
Output File:<br/>
-orbital_launches_output.csv<br/>
-Format:<br/>
 ISO_date, int<br/>
 (space after ',' as per the description)

Env and libs:<br/>
-Python 3.7<br/>
-Requests 2.22.0<br/>
-BeautifulSoup 4.8.2
