import PySimpleGUI as sg
from pygame import mixer

# pip install --upgrade --extra-index-url https://PySimpleGUI.net/install PySimpleGUI
# pip install pygame

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

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    print("event: ", event)
    print("values: ", values)

    # on button pressed
    if (event == "Play Question" and gameStatus == PRE_QUESTION):
        print("Play Question pressed")
        mixer.music.load("tossup.mp3")
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
