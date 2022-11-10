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
mess["EN"]={'1': 'Select local File to Analyze', '2': 'Downloading file', '3': 'Abort Download ?', '4': 'Select local File to Analyze', '5': 'OR', '6': 'Give the URL of the input file', '7': 'Launch Analyze', '8': 'Output Matrix', '9': 'Output Graphs', '10': 'Select Theme Name', '11': 'Select The Language', '12': 'English', '13': 'French', '14': 'Refresh Settings', '15': 'Input', '16': 'Settings', '17': 'No Filename', '18': 'File not found', '19': 'Browse', '20': 'Passwords by size', '21': 'Uppercase', '22': 'Lowercase', '23': 'Digits', '24': 'Others', '25': 'Not Printables'}
mess["FR"]={'1': 'Sélectionner le fichier local à analyser', '2': 'Téléchargement en cours', '3': 'Abandon du téléchargeent ?', '4': 'Choisir le fichier lacal à analyser', '5': 'OU', '6': "Fournir l'URL du fichier à analyser", '7': "Lancer l'analyse", '8': 'Sortie Tableau', '9': 'Sortie Graphe', '10': 'Choix du theme', '11': 'Choix du langage', '12': 'Anglais', '13': 'Français', '14': "Relancer l'interface", '15': 'Entrée', '16': 'Paramètres', '17': 'Nom de fichier manquant', '18': 'Fichier introuvable', '19': 'Parcourir', '20': 'Mots de passe par taille', '21': 'Majuscules', '22': 'Minuscules', '23': 'Numérique', '24': 'Autres', '25': 'Non Imprimables' }
lang = "FR"
control=""
layout=[]
tab3_layout=[]
header_line=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


a = np.array([1, 1, 2, 3, 4, 1, 2, 5, 6, 7, 2, 3, 1, 2, 4, 8, 9, 0, 4, 1, 2, 6, 2, 6, 2, 1, 9])
input_dict={10: 14344391, 97: 8840897, 101: 7215609, 49: 6734380, 48: 5740291, 105: 5561841, 50: 5237479, 111: 5183289, 110: 4834279, 114: 4583500, 108: 4468017, 115: 4163001, 57: 3855490, 51: 3767584, 56: 3567258, 116: 3436156, 52: 3391342, 53: 3355180, 109: 3210393, 54: 3118364, 55: 3100596, 99: 2615356, 100: 2489245, 121: 2376512, 104: 2342106, 117: 2310646, 98: 2113153, 107: 2014184, 103: 1721051, 112: 1626136, 106: 1238200, 118: 1052686, 102: 983982, 119: 803872, 122: 763971, 65: 604870, 120: 481014, 69: 459998, 73: 357135, 76: 331897, 79: 330478, 82: 320192, 78: 316845, 83: 315458, 77: 260296, 46: 253548, 84: 249590, 67: 209435, 68: 199573, 95: 193780, 66: 188255, 113: 179143, 72: 163121, 89: 161134, 75: 144155, 33: 143170, 85: 137387, 45: 134634, 80: 131718, 71: 130282, 42: 123988, 74: 122475, 64: 108303, 32: 100814, 70: 81449, 86: 76328, 87: 59776, 90: 53620, 47: 53062, 35: 49228, 36: 36173, 88: 36085, 224: 34760, 184: 30697, 44: 30187, 92: 28677, 43: 27513, 38: 27483, 61: 24486, 41: 19012, 63: 18778, 81: 17956, 40: 17087, 39: 15590, 59: 12791, 34: 12235, 60: 11176, 93: 10847, 37: 10707, 126: 8371, 58: 8168, 91: 7769, 195: 7574, 94: 6402, 96: 5679, 185: 5497, 177: 4352, 62: 3584, 136: 2839, 159: 2609, 153: 2537, 133: 2078, 163: 2029, 132: 1871, 194: 1723, 160: 1712, 183: 1658, 182: 1575, 179: 1478, 176: 1442, 150: 1388, 129: 1360, 149: 1302, 151: 1264, 167: 1200, 216: 1182, 180: 1106, 123: 1072, 178: 1065, 125: 983, 196: 921, 170: 895, 162: 872, 158: 862, 181: 837, 128: 811, 171: 766, 217: 764, 137: 749, 169: 727, 226: 725, 124: 714, 161: 637, 173: 607, 188: 537, 145: 527, 165: 516, 215: 450, 206: 430, 164: 425, 148: 363, 168: 354, 186: 336, 135: 310, 197: 297, 152: 269, 156: 263, 208: 244, 138: 237, 130: 227, 209: 195, 131: 192, 155: 162, 134: 159, 207: 152, 140: 145, 143: 137, 141: 136, 166: 136, 174: 125, 147: 117, 191: 117, 172: 114, 189: 101, 241: 100, 175: 97, 187: 95, 225: 88, 190: 86, 154: 85, 239: 82, 139: 73, 142: 58, 144: 51, 146: 43, 157: 39, 227: 29, 231: 21, 229: 19, 228: 19, 230: 17, 203: 11, 246: 11, 198: 8, 232: 7, 210: 7, 204: 7, 252: 7, 248: 6, 240: 6, 192: 6, 8: 6, 233: 5, 250: 5, 253: 5, 237: 4, 219: 3, 236: 3, 247: 3, 213: 3, 205: 3, 201: 3, 243: 2, 249: 2, 238: 2, 200: 2, 223: 2, 3: 2, 211: 1, 127: 1, 214: 1, 234: 1, 221: 1, 26: 1, 4: 1}

entete, data = np.unique(a, return_counts=True)
def draw_pie(entete,data,titre):
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

        axesObject.set_title(titre)
        axesObject.axis('equal')

        draw_figure(window['-GRAPH1-'].TKCanvas, figureObject)

def draw_histo(entete,data,titre,xlabel,ylabel):
    x_max = np.max(entete)
    y_max = np.max(data)
    figureObject1, axesObject1 = plotter.subplots() # init de la frame pour les graphes, retoure une Figure (frame) et des axes, possible de definr la taille ici
    axesObject1.bar(entete, data)

    axesObject1.set(xticks = np.arange(0, x_max+1, 1),
                    yticks = np.arange(0, y_max+1, 1),
                    xlabel=xlabel,
                    ylabel=ylabel)

    axesObject1.set_title(titre)

    fig_canvas_agg1 = draw_figure(window['-GRAPH2-'].TKCanvas, figureObject1)

#def draw_table():


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
table1_header=[mess[lang]['21'], mess[lang]['22'], mess[lang]['23'], mess[lang]['24'], mess[lang]['25']]
tab2_layout = [[sg.Text(mess[lang]['8'])],
               [sg.Table([], headings=table1_header,auto_size_columns=False, key='-TABLE1-')],
               [sg.Table([], headings=header_line,auto_size_columns=False, key='-TABLE2-')]]
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
        draw_pie(entete,data,"REPARTION DES TAILLES DE PASSWD")
        draw_histo(entete,data,"HISTOGRAMME","Abscicces","Ordonnées")

    if event == '-EXIT-':
        break

window.close()

