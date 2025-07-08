import PySimpleGUI as sg
from pygame import mixer

# pip install --upgrade --extra-index-url https://PySimpleGUI.net/install PySimpleGUI
# pip install pygame

# All the stuff inside your window.
layout = [  [sg.Text('Quiz Bowl Question Reader')],
            [sg.Button('Play Question'), sg.Button('Buzz')],
            [sg.Button('Quit')]]

window = sg.Window('QBReaderReader', layout)

mixer.init()
ding = mixer.Sound("audio/ding.mp3")

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    mixer.music.load("tossup.mp3")

    print("event: ", event)
    print("values: ", values)

    # on button pressed
    if (event == "Play Question"):
        print("Play Question pressed")
        mixer.music.play(0)
    if (event == "Buzz"):
        print("Buzz Pressed")
        ding.play()
        mixer.music.pause()

    if event == sg.WIN_CLOSED or event == 'Quit':
        break

    # print('You entered ', values[0])
