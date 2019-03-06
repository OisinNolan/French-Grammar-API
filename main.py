import urllib.request
import re
from bs4 import BeautifulSoup

print("Enter a French word:")
searchWord = input().lower()
searchWordForURL = searchWord.replace(" ", "%20")

url = 'http://www.wordreference.com/fren/' + searchWordForURL

req = urllib.request.Request(
    url, 
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
)

byteData = urllib.request.urlopen(req)
stringData = byteData.read().decode('utf8')

soup = BeautifulSoup(stringData, features="lxml")
data = []
noEntryFound = soup.find('p', attrs={'id':'noEntryFound'})

if not noEntryFound:
    table = soup.find('table', attrs={'class':'WRD'})

    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    searchWordText = ""
    wordDict = {}

    wordMatch = False

    for list in data:
        for text in list:
            if text[:len(searchWord)] == searchWord and not wordMatch:
                wordDict[searchWord] = text.split()[1][:-3]
                wordMatch = True
                // only match word if it actually is a nom!

    genderCodes = {
        'nm' : 'masculine',
        'nf' : 'feminine',
        'nmpl' : 'masculine plural',
        'nfpl' : 'feminine plural',
    }

    output = searchWord + " is " + genderCodes[wordDict[searchWord]]
    print(output)

else:
    print("Sorry, word not found!")