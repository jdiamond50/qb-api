import sys
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

isVerbose = False
isSlow = False

for i in range(1, len(sys.argv)):
    if (sys.argv[i] == "-v" or sys.argv[i] == "--verbose"): isVerbose = True
    if (sys.argv[i] == "-s" or sys.argv[i] == "--slow"): isSlow = True

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
        try: #
            index = val.index("-")
        except: # if single number
            diffs.append(int(val))
        else: # if range
            diffRange = val.split("-")
            for i in range(int(diffRange[0]), int(diffRange[1])+1):
                diffs.append(i)
    return diffs

def parseCats(userResponse):
    cats = []
    for cat in userResponse:
        cats.append(cat)
    return cats

def jprint(obj): # pretty print json object
    text = json.dumps(obj, sort_keys=False, indent=4)
    print(text)

def getTossups(numTossups, diffs, cats): # gets list of tossups from QBReader API
    params = {"number" : numTossups, "difficulties" : diffs, "categories" : cats, "powermarkOnly" : "true"}
    response = requests.get("https://www.qbreader.org/api/random-tossup", params = params)
    if (response.status_code == 200):
        if (isVerbose): print("tossups received from QBReader")
        return response.json()["tossups"]
    else:
        raise Exception("Error in retrieving tossups\n Error code " + str(response.status_code))

def makePacket(tossups): # converts list of tossups into audio file
    packetAudio = AudioSegment.silent(duration=1)

    # same audio segments for all tossups
    five_sec_pause = AudioSegment.silent(duration=5000)
    introAnswerGTTS = gTTS(text = "Answer:", lang="en", slow=isSlow).save("introAnswer.mp3")
    introAnswerAudio = AudioSegment.from_mp3("introAnswer.mp3")
    powermarkAudio = AudioSegment.from_mp3("ding.mp3")

    for i in range(len(tossups)):
        tossup = tossups[i]

        # audio segments that are unique to each tossup
        introTossupGTTS = gTTS(text = ("Tossup " + str(i+1)), lang="en", slow=isSlow).save("introTossup.mp3")

        tossupParts = tossup["question_sanitized"].split("(*)")
        if (len(tossupParts) == 1): tossupParts = tossup["question_sanitized"].split("[*]")
        tossupStartGTTS = gTTS(text = tossupParts[0], lang="en", slow=isSlow).save("tossupStart.mp3")
        tossupEndGTTS = gTTS(text = tossupParts[1], lang="en", slow=isSlow).save("tossupEnd.mp3")

        answerGTTS = gTTS(text = tossup["answer_sanitized"], lang="en", slow=isSlow).save("answer.mp3")
        if (isVerbose): print("created answer " + str(i+1) + " audio")

        introTossupAudio = AudioSegment.from_mp3("introTossup.mp3")
        tossupStartAudio = AudioSegment.from_mp3("tossupStart.mp3")
        tossupEndAudio = AudioSegment.from_mp3("tossupEnd.mp3")
        answerAudio = AudioSegment.from_mp3("answer.mp3")

        # concatenating all audio together for each tossup and adding onto the packet
        packetAudio = packetAudio + introTossupAudio + tossupStartAudio + powermarkAudio + tossupEndAudio + five_sec_pause + introAnswerAudio + answerAudio

        if (isVerbose): print("tossup " + str(i+1) + " added to packet")

    packetAudio.export("packet.mp3", format="mp3")

diffs = parseDiffs(diffsUserResponse)
cats = parseCats(catsUserResponse)
makePacket(getTossups(numTossups, diffs, cats))
