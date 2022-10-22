import PySimpleGUI as sg
import os
import urllib3
import sys
import io
from libcpt import *


# vars
core_number = os.cpu_count()
mess = {}
mess["EN"]={'1': 'Select local File to Analyze'}
mess["FR"]={'1': 'Selectionner le fichier local a analyser'}

def dl_file(url_file,chunk_size,out_file):
    print("DANS DL_FILE")
    go_dl = False
    content_bytes = 0
    http = urllib3.PoolManager()

    r = http.request( 'GET', url_file, preload_content=False)
    reader = io.BufferedReader(r, 8)
    content_bytes = r.headers.get("Content-Length")
    if content_bytes is None:
        content_bytes = 0
#        sg.popup('Downloading file with unknown size, it can take time', auto_close = True, keep_on_top=True)
        # win_dl = sg.Window('Downloading File', [[sg.T('Abort Download?')], [sg.Button('Abort',key='-ABORT_DL-')]], disable_close=True, modal=True, return_keyboard_events=True)
    else:
        content_bytes = int(content_bytes)

    with open(out_file, "wb") as f:
        dl_size = 0
        #for chunk in r.stream(chunk_size):
        while True:
            try:
                chunk = reader.read(chunk_size)
                print(type(chunk))
                print('######################################'+str(chunk))
            except:
                print('FERMETURE STREAM')
                r.release_conn()
                go_dl = True
                break
            else:
                f.write(chunk)
                dl_size = dl_size + chunk_size
                print(str(dl_size))
                if content_bytes != 0:
                    go_dl = sg.one_line_progress_meter('Downloading file',dl_size,content_bytes)
                    if not go_dl:
                        sg.one_line_progress_meter_cancel()
                        break
                else:
                    go_dl = sg.popup_auto_close('Abort Download ?')
                    if not go_dl:
                        break
                    
    if not go_dl:
        os.remove(out_file)

def analyze_file(filename, nb_threads):
    print('processing')

def main_window(theme=None) :
    #sg.theme('Dark Amber')  # Let's set our own color theme
    sg.theme(new_theme = theme)
    theme_list = sg.theme_list()

    # The tab 1, 2, 3 layouts - what goes inside the tab
    tab1_layout = [[sg.Text('Select local File to Analyze')],
                   [sg.Text(''), sg.FileBrowse(key='-BROWSEINPUT-')],
                   [sg.Text('OR')],
                   [sg.Text('Give the URL of the input file'), sg.Input(size=(30,1), key='-URL-')],
                   [sg.Text('Number of Core CPU to use : 1 to '+str(core_number))],
                   [sg.Slider(range=(1,core_number),disable_number_display=True,resolution=1,default_value=1,tick_interval=1,orientation='h', key='-SLIDER-')],
                   [sg.HorizontalSeparator(pad=(2,2))],
                   [sg.Button('Launch Analyze', expand_x=True, expand_y=True, key='-LAUNCH-')]]

    tab2_layout = [[sg.Text('Output Matrix')]]
    tab3_layout = [[sg.Text('Output Graphs')]]
    tab4_layout = [[ sg.Text('Select Theme Name'), sg.Combo(values=sg.theme_list(), default_value='No_Change',auto_size_text=True, k='-THEME LIST-')],
                   [ sg.Text('Select The Language'), sg.Radio('English','Language', key='-LANG EN-'), sg.Radio('French','Language', key='-LANG FR-')],
                   [ sg.Button('Refresh Settings', key='-REFRESH-')]]
    
    # The TabgGroup layout - it must contain only Tabs
    tab_group_layout = [[ sg.TabGroup([[sg.Tab('Input', tab1_layout, key='-TAB1-'),
                          sg.Tab('Output Maxtrix', tab2_layout, key='-TAB2-'),
                          sg.Tab('Output Graphs', tab3_layout, key='-TAB3-'),
                          sg.Tab('Settings', tab4_layout, key='-TAB4-')]], expand_x=True, expand_y=True) ]]

    # The window layout - defines the entire window
    layout = [[sg.TabGroup(tab_group_layout,
                           enable_events=True,
                           key='-TABGROUP-'),
                           sg.Sizegrip()]
             ]

    # create the window
    window = sg.Window('Static analysis of a file', layout, resizable=True)
    
    while True:
        event, values = window.read()       # type: str, dict
        print(event, values)
        if event == '-REFRESH-':
            new_theme = values['-THEME LIST-']
            window.close()
            if new_theme != 'No_Change':
                main_window(new_theme)
            else:
                main_window()
        if event == '-LAUNCH-':
            print("DANS LAUNCH")
            if values['-BROWSEINPUT-'] == '':
                if values['-URL-'] == '':
                    sg.popup('No Filename', no_titlebar=True, keep_on_top=True)
                else:
                    print("DANS URL")
                    file_url = values['-URL-']
                    if not os.path.isdir('/tmp'):
                        os.makedirs('/tmp')
                    filename = '/tmp/file_to_analyze.txt'
                    if os.path.exists(filename):
                        os.remove(filename)
                    print ("before DL file "+file_url+" "+filename)
                    dl_file(file_url,1024,filename)
                    print ('Apres DL file')
            else:
                filename = values['-BROWSEINPUT-']
            if os.path.exists(filename):
                dict_letter, numpy_cpt = comptage(filename)
            else:
                sg.popup('File not found', no_titlebar=True, keep_on_top=True)

        if event == sg.WIN_CLOSED:
            break
    window.close()

main_window()
