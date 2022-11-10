import PySimpleGUI as sg
import os
import urllib3
import sys
import io
from libcpt import *
import numpy as np
import matplotlib.pyplot as plotter
from matplotlib.ticker import NullFormatter  
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')


# vars
core_number = os.cpu_count()
mess = {}
mess["EN"]={'1': 'Select local File to Analyze', '2': 'Downloading file', '3': 'Abort Download ?', '4': 'Select local File to Analyze', '5': 'OR', '6': 'Give the URL of the input file', '7': 'Launch Analyze', '8': 'Output Matrix', '9': 'Output Graphs', '10': 'Select Theme Name', '11': 'Select The Language', '12': 'English', '13': 'French', '14': 'Refresh Settings', '15': 'Input', '16': 'Settings', '17': 'No Filename', '18': 'File not found', '19': 'Browse', '20': 'Passwords by size'}
mess["FR"]={'1': 'Sélectionner le fichier local à analyser', '2': 'Téléchargement en cours', '3': 'Abandon du téléchargeent ?', '4': 'Choisir le fichier lacal à analyser', '5': 'OU', '6': "Fournir l'URL du fichier à analyser", '7': "Lancer l'analyse", '8': 'Sortie Tableau', '9': 'Sortie Graphe', '10': 'Choix du theme', '11': 'Choix du langage', '12': 'Anglais', '13': 'Français', '14': "Relancer l'interface", '15': 'Entrée', '16': 'Paramètres', '17': 'Nom de fichier manquant', '18': 'Fichier introuvable', '19': 'Parcourir', '20': 'Mots de passe par taille'}
lang = "FR"
control=""
layout=[]
tab3_layout=[]


# integrate matplotlib figure into a pysimplegui canvas
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

# drawing a pie
def graph_pie(entete, data, graph_label, canvas_label):

    global layout, tab3_layout, window

    # data integration
    nb_slices = np.shape(entete)
    x_max = np.max(entete)
    y_max = np.max(data)
    explode = np.empty(nb_slices)
    explode.fill(0.2)

    # graph pie using matplotlib
    figureObject, axesObject = plotter.subplots() 
    axesObject.pie(data,          
                   labels = entete,
                   startangle=90,
                   autopct = '%1.1f%%',
                   shadow = True,
                   explode = explode)

    axesObject.set_title(graph_label)
    axesObject.axis('equal')

    # complete the tab layout
    print("tab3_layout",tab3_layout)
    print('layout',layout)
    tab3_layout.append([sg.Canvas(key=canvas_label)])
    print("tab3_layout",tab3_layout)
    print('layout',layout)
    window.refresh()
    # adding matplotlib graph to the canvas
    fig_canvas_agg = draw_figure(window[canvas_label].TKCanvas, figureObject) # on passe en argument la Figure qu'on a defini pour le graph matplotlib


def dl_file(url_file,chunk_size,out_file):
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
            except:
                r.release_conn()
                go_dl = True
                break
            else:
                f.write(chunk)
                dl_size = dl_size + chunk_size
                print(str(dl_size))
                if content_bytes != 0:
                    go_dl = sg.one_line_progress_meter(mess[lang]['2'],dl_size,content_bytes)
                    if not go_dl:
                        sg.one_line_progress_meter_cancel()
                        break
                else:
                    go_dl = sg.popup_auto_close(mess[lang]['3'])
                    if not go_dl:
                        break
                    
    if not go_dl:
        os.remove(out_file)

def data_to_graph(cr, chars, passwd):
    entete, cumul = np.unique(passwd, return_counts=True)
    graph_pie(entete, cumul, mess[lang]['20'], '-CANVAS1-')

def main_window(lang="EN",theme=None) :
    global layout, tab3_layout, window
    #sg.theme('Dark Amber')  # Let's set our own color theme
    sg.theme(new_theme = theme)
    theme_list = sg.theme_list()

    # The tab 1, 2, 3 layouts - what goes inside the tab
    tab1_layout = [[sg.Text(mess[lang]['4'])],
                   [sg.Text(''), sg.FileBrowse(mess[lang]['19'], key='-BROWSEINPUT-')],
                   [sg.Text(mess[lang]['5'])],
                   [sg.Text(mess[lang]['6']), sg.Input(size=(30,1), key='-URL-')],
                   [sg.HorizontalSeparator(pad=(2,2))],
                   [sg.Button(mess[lang]['7'], expand_x=True, expand_y=True, key='-LAUNCH-')]]

    tab2_layout = [[sg.Text(mess[lang]['8'])]]
    tab3_layout = [[sg.Text(mess[lang]['9'])]]
    tab4_layout = [[ sg.Text(mess[lang]['10']), sg.Combo(values=sg.theme_list(), default_value='No_Change',auto_size_text=True, k='-THEME LIST-')],
                   [ sg.Text(mess[lang]['11']), sg.Radio(mess[lang]['12'],'Language', key='-LANG_EN-'), sg.Radio(mess[lang]['13'],'Language', key='-LANG_FR-')],
                   [ sg.Button(mess[lang]['14'], key='-REFRESH-')]]
    
    # The TabgGroup layout - it must contain only Tabs
    tab_group_layout = [[ sg.TabGroup([[sg.Tab(mess[lang]['15'], tab1_layout, key='-TAB1-'),
                          sg.Tab(mess[lang]['8'], tab2_layout, key='-TAB2-'),
                          sg.Tab(mess[lang]['9'], tab3_layout, key='-TAB3-'),
                          sg.Tab(mess[lang]['16'], tab4_layout, key='-TAB4-')]], expand_x=True, expand_y=True) ]]

    # The window layout - defines the entire window
    layout = [[sg.TabGroup(tab_group_layout,
                           enable_events=True,
                           key='-TABGROUP-'),
                           sg.Sizegrip()]]



    # create the window
    window = sg.Window(mess[lang]["1"], layout, resizable=True)
    
    while True:
        event, values = window.read()       # type: str, dict
        print(event, values)
        if event == '-REFRESH-':
            new_theme = values['-THEME LIST-']
            if values['-LANG_FR-']:
                lang = "FR"
            if values['-LANG_EN-']:
                lang = "EN"
            window.close()
            if new_theme != 'No_Change':
                main_window(lang,new_theme)
            else:
                main_window(lang)
        if event == '-LAUNCH-':
            if values['-BROWSEINPUT-'] == '':
                if values['-URL-'] == '':
                    sg.popup(mess[lang]['17'], no_titlebar=True, keep_on_top=True)
                else:
                    file_url = values['-URL-']
                    if not os.path.isdir('/tmp'):
                        os.makedirs('/tmp')
                    filename = '/tmp/file_to_analyze.txt'
                    if os.path.exists(filename):
                        os.remove(filename)
                    dl_file(file_url,1024,filename)
            else:
                filename = values['-BROWSEINPUT-']
            if os.path.exists(filename):
                dict_letter, numpy_cpt = comptage(filename)
                data_to_graph(0, dict_letter, numpy_cpt) 
            else:
                sg.popup(mess[lang]['18'], no_titlebar=True, keep_on_top=True)

        if event == sg.WIN_CLOSED:
            break
    window.close()

main_window()
