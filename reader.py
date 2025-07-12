import FreeSimpleGUI as sg
from pygame import mixer
import sys
import requests
import json
from gtts import gTTS
from pydub import AudioSegment
import multiprocessing

# pip install FreeSimpleGUI
# pip install pygame

isVerbose = False
isSlow = False

for i in range(1, len(sys.argv)):
    if (sys.argv[i] == "-v" or sys.argv[i] == "--verbose"): isVerbose = True
    if (sys.argv[i] == "-s" or sys.argv[i] == "--slow"): isSlow = True

# game status
PRE_QUESTION = 0
MID_QUESTION = 1
BUZZED = 2

gameStatus = PRE_QUESTION

layout = [  [sg.Text('Quiz Bowl Question Reader')],
            [sg.Button('Play Question'), sg.Button('Buzz'), sg.Button('Quit')],
            [sg.Text('Enter answer:', key='instruction')],
            [sg.InputText(do_not_clear=True, key="input"), sg.Button('Submit')],
            [sg.Text("", key = "answer")]]

window = sg.Window('QBReaderReader', layout)

mixer.init()
correctSound = mixer.Sound("audio/correct.mp3")
incorrectSound = mixer.Sound("audio/incorrect.mp3")

# defaults
diffs = [2]
cats = "Science"

def jprint(obj): # pretty print json object
    text = json.dumps(obj, sort_keys=False, indent=4)
    print(text)

def getTossup(diffs): # gets list of tossups from QBReader API
    global nextTossupAnswer, nextTossupAnswer_sanitized;
    params = {"difficulties" : diffs, "powermarkOnly" : "true", "categories" : cats}
    response = requests.get("https://www.qbreader.org/api/random-tossup", params = params)
    if (response.status_code == 200):
        if (isVerbose): print("tossup received from QBReader")
        tossup = response.json()["tossups"][0]
        nextTossupAnswer = tossup["answer"]
        nextTossupAnswer_sanitized = tossup["answer_sanitized"]
        return tossup
    else:
        raise Exception("Error in retrieving tossups\n Error code " + str(response.status_code))

def tossupToMP3(tossup):
    # audio segments that are the same for each tossupParts
    powermarkAudio = AudioSegment.from_mp3("audio/ding.mp3")
    five_sec_pause = AudioSegment.silent(duration=5000)

    # audio segments that are unique to each tossup
    tossupParts = tossup["question_sanitized"].split("(*)")
    if (len(tossupParts) == 1): tossupParts = tossup["question_sanitized"].split("[*]")
    tossupStartGTTS = gTTS(text = tossupParts[0], lang="en", slow=isSlow).save("tossupStart.mp3")
    tossupEndGTTS = gTTS(text = tossupParts[1], lang="en", slow=isSlow).save("tossupEnd.mp3")

    tossupStartAudio = AudioSegment.from_mp3("tossupStart.mp3")
    tossupEndAudio = AudioSegment.from_mp3("tossupEnd.mp3")
    if (isVerbose): print("tossup audio parts created")

    # concatenating all audio together for each tossup and adding onto the packet
    tossupAudio = tossupStartAudio + powermarkAudio + tossupEndAudio + five_sec_pause
    if (isVerbose): print("tossup concatenated")
    tossupAudio.export("currTossup.mp3", format="mp3")
    if (isVerbose): print("tossup exported as mp3")

def createTossupAudio(tossup):
    global tossupAudio

    if (isVerbose): print("createTossupAudio called")

    # segments that are the same for each tossupParts
    powermarkAudio = AudioSegment.from_mp3("audio/ding.mp3")
    five_sec_pause = AudioSegment.silent(duration=5000)

    # audio segments that are unique to each tossup
    tossupParts = tossup["question_sanitized"].split("(*)")
    if (len(tossupParts) == 1): tossupParts = tossup["question_sanitized"].split("[*]")
    tossupStartGTTS = gTTS(text = tossupParts[0], lang="en", slow=isSlow).save("tossupStart.mp3")
    tossupEndGTTS = gTTS(text = tossupParts[1], lang="en", slow=isSlow).save("tossupEnd.mp3")

    tossupStartAudio = AudioSegment.from_mp3("tossupStart.mp3")
    tossupEndAudio = AudioSegment.from_mp3("tossupEnd.mp3")
    if (isVerbose): print("tossup audio parts created")

    # concatenating all audio together for each tossup and adding onto the packet
    tossupAudio = tossupStartAudio + powermarkAudio + tossupEndAudio + five_sec_pause
    tossupAudio.export("currTossup.mp3", format="mp3")

def finalizeTossup():
    global tossupAnswer, tossupAnswer_sanitized

    if (isVerbose): print("finalizeTossup called")

    tossupAnswer = nextTossupAnswer
    tossupAnswer_sanitized = nextTossupAnswer_sanitized
    if (isVerbose): print("set tossupAnswer to ", tossupAnswer)
    if (isVerbose): print("tossup exported as mp3")

def checkAnswer(answerline, givenAnswer):
    if (isVerbose):
        print("response evaluation:")
        print("answerline: ", answerline)
        print("givenAnswer: ", givenAnswer)
    params = {"answerline" : answerline, "givenAnswer" : givenAnswer}
    return requests.get("https://www.qbreader.org/api/check-answer", params = params).json()

def changeInstruction(str):
    window["instruction"].update(str)

def tossupPlaying():
    if (gameStatus == MID_QUESTION and not mixer.music.get_busy()): return False
    return True

def displayAnswer():
    if (isVerbose): print("tossupOver() called")
    window["answer"].update("Answer: " + tossupAnswer_sanitized)

timeoutDuration = 100

if (__name__ == "__main__"):
    tossup = getTossup(diffs)
    p = multiprocessing.Process(target=createTossupAudio, args=(tossup, ))
    p.start()

    # Event Loop to process "events" and get the "values" of the inputs
    while (True):

        event, values = window.read(timeout = timeoutDuration)

        if (not tossupPlaying()):
            displayAnswer()
            gameStatus = PRE_QUESTION

        # play question button
        if (event == "Play Question" and gameStatus == PRE_QUESTION):
            if (isVerbose): print("(button) play question registered")
            changeInstruction("Enter answer:")
            window["answer"].update("")
            # tossupToMP3(getTossup(diffs))
            p.join()
            finalizeTossup()
            mixer.music.load("currTossup.mp3")
            gameStatus = MID_QUESTION
            mixer.music.play(0)
            # createTossupAudio(getTossup(diffs))
            tossup = getTossup(diffs)
            p = multiprocessing.Process(target=createTossupAudio, args=(tossup, ))
            p.start()

        # buzz button
        if (event == "Buzz" and gameStatus == MID_QUESTION):
            if (isVerbose): print("(button) buzz registered")
            gameStatus = BUZZED
            mixer.music.pause()

        # submit button
        if (event == "Submit" and gameStatus == BUZZED and len(values) > 0):
            if (isVerbose): print("(button) submit registered")
            window["input"].update("")
            responseEvaluation = checkAnswer(tossupAnswer, values["input"])
            if (isVerbose): jprint(responseEvaluation)
            # correct response
            if (responseEvaluation["directive"] == "accept"):
                if (isVerbose): print("correct answer provided")
                correctSound.play()
                changeInstruction("Correct!")
                window["answer"].update("Answer: " + tossupAnswer_sanitized)
                gameStatus = PRE_QUESTION
            # incorrect response
            if (responseEvaluation["directive"] == "reject"):
                if (isVerbose): print("incorrect answer")
                incorrectSound.play()
                changeInstruction("Enter answer:")
                gameStatus = MID_QUESTION
                mixer.music.unpause()
            # prompted response
            if (responseEvaluation["directive"] == "prompt"):
                try:
                    if (isVerbose): print("promted with direction ", responseEvaluation["directedPrompt"])
                    changeInstruction("Prompt: " + responseEvaluation["directedPrompt"])
                except:
                    if (isVerbose): print("prompted")
                    changeInstruction("Prompt:")

        # close reader
        if event == sg.WIN_CLOSED or event == 'Quit':
            break
