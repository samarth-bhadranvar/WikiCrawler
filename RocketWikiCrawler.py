import requests
from bs4 import BeautifulSoup
import datetime
from dateutil.parser import parse
from collections import defaultdict
# import pandas as pd

html = requests.get("https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches")
b = BeautifulSoup(html.text,'lxml')

listTable = b.find('table',class_="wikitable")

#retreiving all rows
rowsList = listTable.find_all(name='tr')

#To hold extracted date in ISO8601 format
dateString = ""

#True: Launches were successful on that date
dateFlag = False

start = parse("01-01-2019")
end = parse("31-12-2019")
date_generated = [(start + datetime.timedelta(days=x)).isoformat()+"+00:00" for x in range(0, (end-start).days+1)]
#All the dates of the year
#using collections for simplicity's sake
dateCountDict = defaultdict(int)
for date in date_generated:
    dateCountDict[date]=0

# print(dateCountDict)
for rowIndex in range(3,len(rowsList)):
    row = rowsList[rowIndex]
    if not row.style:
        columnsList = row.find_all(name='td')
        columnsListLength = len(columnsList)
        #For carrier rocket
        if columnsListLength == 5:
            if dateFlag:
                dateCountDict[dateString]+=1
            #date extraction and formatting
            dateString=columnsList[0].span.get_text()
            if '[' in dateString:
                dateString = dateString[:dateString.index('[')]
            if '(' in dateString:
                dateString = dateString[:dateString.index('(')]
            dateString = dateString+" 2019"
            dateObj = parse(dateString)
            dateString=dateObj.isoformat()+"+00:00"
            dateFlag = False
        #For payloads
        if columnsListLength == 6:
            payloadStatus = columnsList[5].get_text()
            if '[' in payloadStatus:
                payloadStatus = payloadStatus[:payloadStatus.index('[')]
            if '(' in payloadStatus:
                payloadStatus = payloadStatus[:payloadStatus.index('(')]
            if payloadStatus.strip().lower() in ['successful', 'operational','en route']:
                #Launches successful
                dateFlag = dateFlag or True
            else:
                dateFlag = dateFlag or False

# print(dateCountDict)
out = open("orbital_launches_output.csv","w")

out.write("date, value\n")

for entry in dateCountDict.keys():
    #Space after ',' as mentioned in the assignment description
    out.write(entry+", "+str(dateCountDict[entry]))
    out.write("\n")

out.close()

print("Please check output file: orbital_launches_output.csv")