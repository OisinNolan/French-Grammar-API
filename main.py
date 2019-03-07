# Imports

import urllib.request
import urllib.parse
import re
from bs4 import BeautifulSoup

# Helper functions

def getWordData(word):
    if word == '':
        return None
    
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
            'article' : 'article',
            'adverbe' : 'adverb',
            'prép' : 'preposition',
            'conj' : 'conjunction',
        }

        for list in data:
            for text in list:
                if text.split()[0] == searchWord and len(text.split()) > 1:
                    textGrammarCode = text.split()[1]
                    #print(textGrammarCode)
                    for code in grammarCodes:
                        if code in textGrammarCode and grammarCodes[code] not in wordDict[searchWord]:
                            wordDict.setdefault(searchWord, []).append(grammarCodes[code])

        return wordDict

    else:
        return None

# API functions

def getAllGenders(word):
    word = word.lower()
    wordDict = getWordData(word)
    if wordDict is None:
        return None
    else:
        genderCodes = ['masculine noun', 'feminine noun', 'masculine plural noun', 'feminine plural noun', 'masculine/feminine noun']
        wordGenders = []

        for code in wordDict[word]:
            if code in genderCodes:
                wordGenders.append(code)

        if len(wordGenders) > 0:
            return wordGenders
        else:
            return None

def getGender(word):
    word = word.lower()
    wordDict = getWordData(word)
    if wordDict is None:
        return None
    else:
        genderCodes = ['masculine noun', 'feminine noun', 'masculine plural noun', 'feminine plural noun', 'masculine/feminine noun']
        wordGenders = []

        for code in wordDict[word]:
            if code in genderCodes:
                wordGenders.append(code)

        if len(wordGenders) > 0:
            return wordGenders[0]
        else:
            return None

def canBeNoun(word):
    word = word.lower()
    if getGender(word) is not None:
        return True
    return False

def isNoun(word):
    word = word.lower()
    if getAllGenders(word) is None:
        return False
    else:
        return True

def canBeVerb(word):
    word = word.lower()
    grammaticalCategories = getAllGrammaticalCategories(word)
    if grammaticalCategories is None:
        return False
    else:
        for category in grammaticalCategories:
            if 'verb' in category:
                return True
        return False

def isVerb(word):
    word = word.lower()
    if 'verb' in getGrammaticalCategory(word):
        return True
    return False

def getAllGrammaticalCategories(word):
    word = word.lower()
    wordDict = getWordData(word)
    if wordDict is None:
        return None
    else:
        return wordDict[word]

def getGrammaticalCategory(word):
    word = word.lower()
    wordDict = getWordData(word)
    if wordDict is None or len(wordDict[word]) <= 0:
        return None
    else:
        return wordDict[word][0]

""" 
Function tests:

testData = ['La', 'fréquentation', 'scolaire', 'ne', 'cesse', 'd’augmenter', 'mondialement', 'de', 'nos', 'jours', 'parallèlement', 'à', 'la', 'diminution', 'de', 'la', 'pauvreté', 'Alors', 'l’école', 'joue', 'un', 'rôle', 'croissant', 'dans', 'la', 'vie', 'et', 'donc', 'il', 'faut', 'l’analyser', 'Considérons', 'l’école', 'comme', 'système', '', 'une', 'composition', 'd’éléments', 'qui', 'fonctionnent', 'ensemble', 'afin', 'de', 'produire', 'dans', 'ce', 'cas', 'des', 'adultes', 'mûrs', 'et', 'instruits', 'Cette', 'dissertation', 'explorera', 'deux', 'tels', 'éléments', 'se', 'concentrant', 'sur', 'leurs', 'interactions', 'avec', 'les', 'inégalités', 'sociales', 'Tout', 'd’abord', 'nous', 'nous', 'intéressons', 'à', 'l’éducation', 'autour', 'de', 'laquelle', 'l’école', 'tourne', 'L’éducation', 'permet', 'à', 'l’étudiant', 'à', 'diriger', 'sa', 'vie', '—', 'elle', 'le', 'rend', 'capable', 'L’éducation', 'encourage', 'la', 'facilité', 'naturelle', 'qui', 'n’est', 'pas', 'forcément', 'déterminée', 'par', 'la', 'classe', 'sociale', 'Prenons', 'l’exemple', 'de', 'l’élève', 'venant', 'd’un', 'milieu', 'pauvre', 'qui', 'travaille', 'dur', 'tout', 'au', 'long', 'de', 'sa', 'scolarité', 'et', 'enfin', 'trouve', 'un', 'emploi', 'bien', 'payé', 'Cet', 'élève', 's’est', 'échappé', 'à', 'la', 'pauvreté', 'grâce', 'à', 'l’éducation', 'Ainsi', 'l’aspect', 'éducatif', 'de', 'l’école', 'sert', 'à', 'réduire', 'les', 'inégalités', 'sociales', 'Toutefois', 'l’école', 'ne', 'consiste', 'pas', 'que', 'de', 'l’éducation', 'L’école', 'assure', 'un', 'paysage', 'social', 'par', 'intermédiaire', 'duquel', 'des', 'liens', 'sociaux', 's’établissent', 'entre', 'les', 'élèves', 'Une', 'école', 'privée', 'ne', 'se', 'limite', 'qu’aux', 'familles', 'qui', 'ont', 'le', 'pouvoir', 'd’y', 'envoyer', 'leurs', 'enfants', 'Ces', 'enfants', 'ne', 'peuvent', 'faire', 'la', 'connaissance', 'que', 'd’eux', 'avec', 'qui', 'ils', 'étudient', 'à', 'l’école', 'En', 'fait', 'l’école', 'privée', 'crée', 'une', 'barrière', 'entre', 'ceux', 'qui', 'ont', 'le', 'pouvoir', 'financier', 'et', 'les', 'autres', 'Cette', 'barrière', 'sert', 'à', 'propager', 'les', 'inégalités', 'qui', 'existent', 'entre', 'les', 'riches', 'et', 'les', 'pauvres', 'parce', 'qu’elle', 'empêche', 'la', 'création', 'de', 'liens', 'entre', 'les', 'deux', 'Enfin', 'imaginons', 'le', 'système', 'éducatif', 'en', 'entier', 'Ce', 'système', 'tel', 'qu’il', 'est', 'expliqué', 'cidessus', 'n’est', 'pas', 'parfaite', 'Cela', 'veut', 'dire', 'qu’il', 'est', 'possible', 'de', 'dépasser', 'de', 'la', 'situation', 'actuelle', 'à', 'une', 'meilleure', 'En', 'conclusion', 'cette', 'dissertation', 'propose', 'la', 'démolition', 'de', 'la', 'barrière', 'sociale', 'qui', 'distingue', 'l’école', 'privée', 'de', 'l’école', 'publique', 'comme', 'moyen', 'd’atteindre', 'ce', 'dépassement']

for word in testData:
    print(word + " : " + str(getGrammaticalCategory(word)))
"""