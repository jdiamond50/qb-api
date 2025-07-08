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
            [sg.Text('Enter answer here'), sg.InputText(do_not_clear=False), sg.Button('Submit')]]

window = sg.Window('QBReaderReader', layout)

mixer.init()
ding = mixer.Sound("audio/ding.mp3")

# defaults
diffs = [3, 4, 5]

def getTossup(diffs): # gets list of tossups from QBReader API
    params = {"difficulties" : diffs, "powermarkOnly" : "true"}
    response = requests.get("https://www.qbreader.org/api/random-tossup", params = params)
    if (response.status_code == 200):
        if (isVerbose): print("tossup received from QBReader")
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

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    print("event: ", event)
    print("values: ", values)

    # on button pressed
    if (event == "Play Question" and gameStatus == PRE_QUESTION):
        print("Play Question pressed")
        tossupToMP3(getTossup(diffs))
        mixer.music.load("currTossup.mp3")
        gameStatus = MID_QUESTION
        mixer.music.play(0)
    if (event == "Buzz" and gameStatus == MID_QUESTION):
        print("Buzz Pressed")
        gameStatus = BUZZED
        ding.play()
        mixer.music.pause()
    if (event == "Submit" and gameStatus == BUZZED):
        print("Submit pressed")
        print("answer: ", values[0])
        if (values[0] == "correct"):
            print("answer is correct")
            gameStatus = PRE_QUESTION
        else:
            print("answer is incorrect")
            mixer.music.unpause()
            gameStatus = MID_QUESTION

    if event == sg.WIN_CLOSED or event == 'Quit':
        break

    # print('You entered ', values[0])
