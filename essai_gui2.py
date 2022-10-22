import PySimpleGUI as sg


layout = [[sg.Button('Save')]]
window = sg.Window('Window Title',
                   layout,
                   default_element_size=(12, 1),
                   resizable=True,finalize=True)  # this is the chang
window.bind('<Configure>',"Event")

while True:
    event, values = window.read()
    if event == 'Save':
        print('clicked save')

    if event == "Event":
        print(window.size)

    if event == sg.WIN_CLOSED:
        print("I am done")
        break

