import requests
import json
from gtts import gTTS

print("Enter Difficulties:")
print("(ex: \"3\" OR \"4-6, 8\")")
diffsUserResponse = input().split(", ")

print("Enter Categories:")
print("(ex: \"Literature\" or \"Philosophy, Science\")")
catsUserResponse = input().split(", ")

print("Enter number of Questions")
print("(ex: \"2\" or \"7\")")
numTossups = int(input())

def parseDiffs(userResponse):
    diffs = []
    for val in userResponse:
        try:
            index = val.index("-")
        except:
            diffs.append(int(val))
        else:
            diffRange = val.split("-")
            for i in range(int(diffRange[0]), int(diffRange[1])+1):
                diffs.append(i)
    return diffs

def parseCats(userResponse):
    cats = []
    for cat in userResponse:
        cats.append(cat)
    return cats

def jprint(obj):
    text = json.dumps(obj, sort_keys=False, indent=4)
    print(text)

def getTossups(numTossups, diffs, cats):
    params = {"number" : numTossups, "difficulties" : diffs, "categories" : cats}
    response = requests.get("https://www.qbreader.org/api/random-tossup", params = params)
    if (response.status_code == 200):
        return response.json()["tossups"]

def makePacket(tossups):
    packetText = ""
    for i in range(len(tossups)):
        tossup = tossups[i]
        tossupText = "Tossup " + str(i+1) + ": " + tossup["question_sanitized"] + "Answer: " + tossup["answer_sanitized"] + "."
        packetText += tossupText
    audio = gTTS(text=packetText, lang="en", slow=False)
    audio.save("packet.mp3")

diffs = parseDiffs(diffsUserResponse)
cats = parseCats(catsUserResponse)
makePacket(getTossups(numTossups, diffs, cats))
