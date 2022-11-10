import PySimpleGUI as sg
from datetime import datetime
import base64

img = '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'


layout_img = [[sg.Button('', image_data=img, key='-GRAPH-')]]


window = sg.Window("THE TEAM !", layout_img)


while True:
    event, values = window.read()
    if event == '-GRAPH-':
        break

window.close()
