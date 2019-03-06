import urllib.request
import re

print("Enter a French word:")
searchWord = input().lower();

url = 'http://www.wordreference.com/fren/' + searchWord

req = urllib.request.Request(
    url, 
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
)

byteData = urllib.request.urlopen(req)
stringData = byteData.read().decode('utf-8')

regex = searchWord + ".*?(masculin|féminin)"

wordsInHtml = re.findall(regex, stringData)

if len(wordsInHtml) > 0:
    wordGenderCode = re.findall("(masculin|féminin)", wordsInHtml[0])[0]

    wordGender = ""
    if wordGenderCode == "masculin":
        wordGender = "masculine"
    elif wordGenderCode == "féminin":
        wordGender = "feminine"
    print(searchWord + " is " + wordGender)

else:
    print("Sorry, word not found!")