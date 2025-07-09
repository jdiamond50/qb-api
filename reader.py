import PySimpleGUI as sg
from pygame import mixer
import sys
import requests
import json
from gtts import gTTS
from pydub import AudioSegment

# pip install --upgrade --extra-index-url https://PySimpleGUI.net/install PySimpleGUI
# pip install pygame

isVerbose = True

# game status
PRE_QUESTION = 0
MID_QUESTION = 1
BUZZED = 2

gameStatus = PRE_QUESTION

layout = [  [sg.Text('Quiz Bowl Question Reader')],
            [sg.Button('Play Question'), sg.Button('Buzz'), sg.Button('Quit')],
            [sg.Text('Enter answer:', key='instruction'), sg.InputText(do_not_clear=False), sg.Button('Submit')]]

window = sg.Window('QBReaderReader', layout)

mixer.init()
ding = mixer.Sound("audio/ding.mp3")

# defaults
diffs = [2]
cats = "Science"

def jprint(obj): # pretty print json object
    text = json.dumps(obj, sort_keys=False, indent=4)
    print(text)

def getTossup(diffs): # gets list of tossups from QBReader API
    global tossupAnswer;
    params = {"difficulties" : diffs, "powermarkOnly" : "true", "categories" : cats}
    response = requests.get("https://www.qbreader.org/api/random-tossup", params = params)
    if (response.status_code == 200):
        if (isVerbose): print("tossup received from QBReader")
        tossupAnswer = response.json()["tossups"][0]["answer"]
        return response.json()["tossups"][0]
    else:
        raise Exception("Error in retrieving tossups\n Error code " + str(response.status_code))

def tossupToMP3(tossup):
    # audio segments that are the same for each tossupParts
    powermarkAudio = AudioSegment.from_mp3("audio/ding.mp3")
    five_sec_pause = AudioSegment.silent(duration=5000)

    # audio segments that are unique to each tossup
    tossupParts = tossup["question_sanitized"].split("(*)")
    if (len(tossupParts) == 1): tossupParts = tossup["question_sanitized"].split("[*]")
    tossupStartGTTS = gTTS(text = tossupParts[0], lang="en", slow="false").save("tossupStart.mp3")
    tossupEndGTTS = gTTS(text = tossupParts[1], lang="en", slow="false").save("tossupEnd.mp3")

    tossupStartAudio = AudioSegment.from_mp3("tossupStart.mp3")
    tossupEndAudio = AudioSegment.from_mp3("tossupEnd.mp3")
    if (isVerbose): print("tossup audio parts created")

    # concatenating all audio together for each tossup and adding onto the packet
    tossupAudio = tossupStartAudio + powermarkAudio + tossupEndAudio + five_sec_pause
    if (isVerbose): print("tossup concatenated")

    tossupAudio.export("currTossup.mp3", format="mp3")
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

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    # play question button
    if (event == "Play Question" and gameStatus == PRE_QUESTION):
        print("(button) play question registered")
        changeInstruction("Enter answer:")
        tossupToMP3(getTossup(diffs))
        mixer.music.load("currTossup.mp3")
        gameStatus = MID_QUESTION
        mixer.music.play(0)

    # buzz button
    if (event == "Buzz" and gameStatus == MID_QUESTION):
        print("(button) buzz registered")
        gameStatus = BUZZED
        ding.play()
        mixer.music.pause()

    # submit button
    if (event == "Submit" and gameStatus == BUZZED):
        print("(button) submit registered")
        responseEvaluation = checkAnswer(tossupAnswer, values[0])
        if (isVerbose): jprint(responseEvaluation)
        # correct response
        if (responseEvaluation["directive"] == "accept"):
            if (isVerbose): print("correct answer provided")
            changeInstruction("Correct!")
            gameStatus = PRE_QUESTION
        # incorrect response
        if (responseEvaluation["directive"] == "reject"):
            if (isVerbose): print("incorrect answer")
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
