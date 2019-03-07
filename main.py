# Imports

import urllib.request
import urllib.parse
import re
from bs4 import BeautifulSoup

# Helper functions

def getWordData(word):
    searchWord = word.lower()
    searchWordForURL = searchWord.replace(" ", "%20")

    url = 'http://www.wordreference.com/fren/' + urllib.parse.quote(searchWordForURL)

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
        wordDict.setdefault(searchWord, [])

        wordMatch = False

        # need to add more codes here, ie pron, nmf
        grammarCodes = {
            'nmnom' : 'masculine noun',
            'nfnom' : 'feminine noun',
            'mfnom' : 'masculine/feminine noun',
            'mplnom' : 'masculine plural noun',
            'fplnom' : 'feminine plural noun',
            'adj' : 'adjective',
            'vtrverbe' : 'transitive verb',
            'viverbe' : 'intransitive verb',
            'interjinterjection' : 'interjection',
            'pron' : 'pronoun',
        }

        for list in data:
            for text in list:
                if text.split()[0] == searchWord:
                    textGrammarCode = text.split()[1]
                    print(textGrammarCode)
                    for code in grammarCodes:
                        if code in textGrammarCode and grammarCodes[code] not in wordDict[searchWord]:
                            wordDict.setdefault(searchWord, []).append(grammarCodes[code])

        return wordDict

    else:
        return None

# API functions

def getGender(word):
    wordDict = getWordData(word)
    genderCodes = ['masculine noun', 'feminine noun', 'masculine plural noun', 'feminine plural noun', 'masculine/feminine noun']
    wordGenders = []

    for code in wordDict[word]:
        if code in genderCodes:
            wordGenders.append(code)

    return wordGenders
