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


a = np.array([1, 1, 2, 3, 4, 1, 2, 5, 6, 7, 2, 3, 1, 2, 4, 8, 9, 0, 4, 1, 2, 6, 2, 6, 2, 1, 9])
entete, data = np.unique(a, return_counts=True)

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


# The tab 1, 2, 3 layouts - what goes inside the tab
tab1_layout = [[sg.Text(mess[lang]['4'])],
               [sg.Text(''), sg.FileBrowse(mess[lang]['19'], key='-BROWSEINPUT-')],
               [sg.Text(mess[lang]['5'])],
               [sg.Text(mess[lang]['6']), sg.Input(size=(30,1), key='-URL-')],
               [sg.HorizontalSeparator(pad=(2,2))],
               [sg.Button(mess[lang]['7'], expand_x=True, expand_y=True, key='-LAUNCH-')]]

tab2_layout = [[sg.Text(mess[lang]['8'])]]
tab3_layout = [[sg.Text(mess[lang]['9'])],
               [sg.Canvas(key='-GRAPH1-')],[sg.Canvas(key='-GRAPH2-')] ]
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
    if event == '-LAUNCH-':
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

        axesObject.set_title('GRAPH LABEL')
        axesObject.axis('equal')

        draw_figure(window['-GRAPH1-'].TKCanvas, figureObject)
    if event == '-EXIT-':
        break

window.close()

