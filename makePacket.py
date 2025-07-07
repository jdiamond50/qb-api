import requests
import json
from gtts import gTTS
from pydub import AudioSegment

# python3 -m venv qb-venv
# source qb-venv/bin/activate

# pip install requests
# pip install gTTS
# pip install pydub
# brew install ffmpeg

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
    packetAudio = AudioSegment.silent(duration=1)
    five_sec_pause = AudioSegment.silent(duration=5000)
    introAnswerGTTS = gTTS(text = "Answer:", lang="en", slow=False).save("introAnswer.mp3")
    introAnswerAudio = AudioSegment.from_mp3("introAnswer.mp3")

    for i in range(len(tossups)):
        tossup = tossups[i]

        introTossupGTTS = gTTS(text = ("Tossup " + str(i+1)), lang="en", slow=False).save("introTossup.mp3")
        tossupGTTS = gTTS(text = tossup["question_sanitized"], lang="en", slow=False).save("tossup.mp3")
        answerGTTS = gTTS(text = tossup["answer_sanitized"], lang="en", slow=False).save("answer.mp3")

        introTossupAudio = AudioSegment.from_mp3("introTossup.mp3")
        tossupAudio = AudioSegment.from_mp3("tossup.mp3")
        answerAudio = AudioSegment.from_mp3("answer.mp3")

        packetAudio = packetAudio + introTossupAudio + tossupAudio + five_sec_pause + introAnswerAudio + answerAudio

    packetAudio.export("packet.mp3", format="mp3")

diffs = parseDiffs(diffsUserResponse)
cats = parseCats(catsUserResponse)
makePacket(getTossups(numTossups, diffs, cats))
