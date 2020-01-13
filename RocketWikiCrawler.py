import requests
from bs4 import BeautifulSoup
import datetime
from dateutil.parser import parse
from collections import defaultdict
# import pandas as pd


html = requests.get("https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches")

b = BeautifulSoup(html.text,'lxml')

listTable = b.find('table',class_="wikitable")

rowsList = listTable.find_all(name='tr')

dateString = ""
dateFlag = False

start = parse("01-01-2019")
end = parse("31-12-2019")
date_generated = [(start + datetime.timedelta(days=x)).isoformat()+"+00:00" for x in range(0, (end-start).days+1)]
print("len of dates=",len(date_generated))
dateCountDict = defaultdict(int)

for date in date_generated:
    dateCountDict[date]=0

print(dateCountDict)

for rowIndex in range(3,len(rowsList)):
    row = rowsList[rowIndex]
    if not row.style:
        columnsList = row.find_all(name='td')
        columnsListLength = len(columnsList)
        if columnsListLength == 5:

            print("dateFlag now = ",dateFlag)
            if dateFlag:
                print(dateString,"#==#",dateFlag)
                dateCountDict[dateString]+=1

            print("columnsList[0].span.get_text()===",columnsList[0].span.get_text())
            dateString=columnsList[0].span.get_text()
            if '[' in dateString:
                print("[] found")
                dateString = dateString[:dateString.index('[')]
            if '(' in dateString:
                print("() found")
                dateString = dateString[:dateString.index('(')]
            dateString = dateString+" 2019"
            print("now date =", dateString)
            dateObj = parse(dateString)
            dateString=dateObj.isoformat()+"+00:00"
            print("new dateString=",dateString)
            dateFlag = False
        if columnsListLength == 6:
            payloadStatus = columnsList[5].get_text()
            if '[' in payloadStatus:
                print("[] found")
                payloadStatus = payloadStatus[:payloadStatus.index('[')]
            if '(' in payloadStatus:
                print("() found")
                payloadStatus = payloadStatus[:payloadStatus.index('(')]
            print("now payloadStatus =", payloadStatus)
            print(dateString,":",columnsList[0].get_text(),"==",payloadStatus)
            if payloadStatus.strip().lower() in ['successful', 'operational','en route']:
                print("PASSED=",payloadStatus.lower())
                dateFlag = dateFlag or True
                print("dateFlag=",dateFlag)
            else:
                print("FAILED=",payloadStatus.lower())
                dateFlag = dateFlag or False
                print("dateFlag=",dateFlag)





print("FINALLLLLLLLY")

print(dateCountDict)

out = open("output.txt","w")

for entry in dateCountDict.keys():
    out.write(entry+", "+str(dateCountDict[entry]))
    out.write("\n")

out.close()
