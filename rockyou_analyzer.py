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
import csv


# vars
lang='EN'
core_number = os.cpu_count()
mess = {}
mess["EN"]={'1': 'Characters Analysis', '2': 'Downloading file', '3': 'Abort Download ?', '4': 'Select local File to Analyze', '5': 'OR', '6': 'Give the URL of the input file', '7': 'Launch Analyze', '8': 'Character Types', '9': 'Output Graphs', '10': 'Select Theme Name', '11': 'Select The Language', '12': 'English', '13': 'French', '14': 'Refresh Settings', '15': 'Input', '16': 'Settings', '17': 'No Filename', '18': 'File not found', '19': 'Browse', '20': 'Passwords by size', '21': 'Uppercase', '22': 'Lowercase', '23': 'Digits', '24': 'Characters', '25': 'Control', '26': 'Extended', '27': 'Character count', '28': 'Char', '29': 'Count', '30': 'Output Tables', "31": 'Font Choice', '32': 'Font size', '33': 'Types', '34': 'Numbers', '35': 'Caracteres by type', '36': 'length', '37': 'Export to CVS', '38': 'Error processing datas', '39': 'No access to tmp dir', '40': 'CSV files are on /tmp directory', '41': 'Failed'}

mess["FR"]={'1': "Analyse des caractères d'un fichier", '2': 'Téléchargement en cours', '3': 'Abandon du téléchargement ?', '4': 'Choisir le fichier local à analyser', '5': 'OU', '6': "Fournir l'URL du fichier à analyser", '7': "Lancer l'analyse", '8': 'Types de caractères', '9': 'Sortie Graphes', '10': 'Choix du theme', '11': 'Choix du langage', '12': 'Anglais', '13': 'Français', '14': "Relancer l'interface", '15': 'Entrée', '16': 'Paramètres', '17': 'Nom de fichier manquant', '18': 'Fichier introuvable', '19': 'Parcourir', '20': 'Mots de passe par taille', '21': 'Majuscules', '22': 'Minuscules', '23': 'Numérique', '24': 'Caractères', '25': 'Contrôle', '26': 'Etendus', '27': 'Comptage des caractères', '28': 'Carac', '29': 'Compt', '30': 'Sortie Tableaux', '31': 'Choix de la police', '32': 'Taille de la police', '33': 'Types', '34': 'Occurences', '35': 'Caractères par types', '36': 'Longueur', '37': 'Exporter en CSV', '38': 'Erreur dans le traitement des données', '39': 'repertoire tmp inaccessible', '40': 'Les fichiers CSV sont dans le répertoire /tmp', '41': 'En echec' }

control=""
layout=[]
tab3_layout=[]
header_line=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
table_1=[]
table_2=[]
summary_dict={}
font_name="Courier"
font_size=12

def export_to_csv(entete, data, output_file):
    cr = True
    try:
        f = open(output_file, "w")
        writer = csv.writer(f)
    except Exception as e1:
        print(e1)
        cr = False
    else:
        try:
            writer.writerow(entete)
            for ligne in data:
                writer.writerow(ligne)
        except Exception as e2:
            print(e2)
            cr = False
    finally:
        f.close()
        return cr

def data_to_graph(dict_letter, numpy_cpt, summary_dict, lang):
    draw_table(summary_dict, 1, 1)
    draw_table(dict_letter, 9, 2)

    type_car=[mess[lang][str(i)] for i in range(21,27)]
    entete = np.asarray(type_car)
    type_val=list(summary_dict.values())
    data = np.asarray(type_val)
    titre = mess[lang]['35']
    draw_pie(entete,data,titre, lang)

    entete, data = np.unique(numpy_cpt, return_counts=True)
    titre  = mess[lang]['20']
    xlabel = mess[lang]['36']
    ylabel = mess[lang]['29']
    draw_histo(entete,data,titre,xlabel,ylabel, lang)


def draw_pie(entete,data,titre, lang):
        nb_slices = np.shape(entete)
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

        draw_figure(window['-GRAPH1-'].TKCanvas, figureObject,'left')

def draw_histo(entete,data,titre,xlabel,ylabel, lang):
    taille = entete.size
    x_max = np.max(entete)
    y_max = np.max(data)
    figureObject1, axesObject1 = plotter.subplots() # init de la frame pour les graphes, retoure une Figure (frame) et des axes, possible de definr la taille ici
    axesObject1.bar(entete, data)

    axesObject1.set(xticks = np.arange(0, x_max+1, 1),
                    #yticks = np.arange(0, y_max+1, 1),
                    xlabel=xlabel,
                    ylabel=ylabel)

    for i in range(0, taille):
        plotter.text(x=entete[i] , y=data[i],  s=f"{data[i]}" )

    axesObject1.set_title(titre)

    draw_figure(window['-GRAPH1-'].TKCanvas, figureObject1,'right')



def draw_table(input_dict, nb_col, dest_table):
    global window
    # preparation des données pour le tableau
    if dest_table == 2: # tableau du bas
        table_2=[]
        row_line=[]
        nb_elem=0
        for elem in input_dict.keys():
            # if elem is not printable give its ascii number value instead
            if elem > 32 and elem < 127:
                    prn_elem = chr(elem)
            else:
                prn_elem = "ASCII("+str(elem)+")"
            if nb_elem < nb_col:
                row_line.append(prn_elem)
                row_line.append(input_dict[elem])
                nb_elem = nb_elem + 1
            else:
               table_2.append(row_line)
               row_line=[prn_elem]
               row_line.append(input_dict[elem])
               nb_elem=1
        window['-TABLE2-'].update(values=table_2 )
    if dest_table == 1:
        row_line=list(input_dict.values())
        table_1.append(row_line)
        window['-TABLE1-'].update(values=table_1)



def draw_figure(canvas, figure, side_pos):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.get_tk_widget().pack(side=side_pos, fill='y', expand=1)
    figure_canvas_agg.draw()
    return figure_canvas_agg


def main_window(lang='EN',theme=None,font_name='courier') :
    global window, table_1, table_2, summary_dict, font_size
    sg.theme(new_theme = theme)
    # The tab 1, 2, 3 layouts - what goes inside the tab
    tab1_layout = [[sg.Text(mess[lang]['4'], font=(font_name, font_size))],
                   [sg.Text(''), sg.FileBrowse(mess[lang]['19'], key='-BROWSEINPUT-', font=(font_name, font_size))],
                   [sg.Text(mess[lang]['5'], font=(font_name, font_size))],
                   [sg.Text(mess[lang]['6'], font=(font_name, font_size)), sg.Input(size=(30,1), font=(font_name, font_size),  key='-URL-')],
                   [sg.VPush()],
                   [sg.HorizontalSeparator(pad=(2,2))],
                   [sg.VPush()],
                   [sg.Push(), sg.Button(mess[lang]['7'], expand_x=True, expand_y=True, key='-LAUNCH-', font=(font_name, font_size, 'bold')), sg.Push()]]

    table1_header=[mess[lang]['21'], mess[lang]['22'], mess[lang]['23'], mess[lang]['24'], mess[lang]['25'], mess[lang]['26']]
    lib_head = [mess[lang]['28'], mess[lang]['29']]
    table2_header=[alpha+'_'+str(num) for num in range(1,10) for alpha in lib_head]
    tab2_layout = [[sg.Text(mess[lang]['8'])],
                   [sg.Table(table_1, headings=table1_header,auto_size_columns=True, key='-TABLE1-', num_rows=1, hide_vertical_scroll=True)],
                   [sg.Text(mess[lang]['27'])],
                   [sg.Table(table_2, headings=table2_header,auto_size_columns=True, key='-TABLE2-', num_rows=25, hide_vertical_scroll=False)],
                   [sg.HorizontalSeparator(pad=(2,2))],
                   [sg.VPush()],
                   [sg.Push(), sg.Button(mess[lang]['37'], expand_x=True, expand_y=True, key='-TO_CSV-', font=(font_name, font_size)), sg.Push()]]
    tab3_layout = [[sg.Text(mess[lang]['9'])],
                   [sg.Canvas(key='-GRAPH1-',expand_y=True)]]
    tab4_layout = [[ sg.Text(mess[lang]['10'], font=(font_name, font_size)), sg.Combo(values=sg.theme_list(), default_value='Random',auto_size_text=True, k='-THEME LIST-')],
                   [ sg.Text(mess[lang]['31'], font=(font_name, font_size)), sg.Combo(values=sg.Text.fonts_installed_list(), default_value='Courier', auto_size_text=True, key='-FONT_NAME-')],
                   [ sg.Text(mess[lang]['32'], font=(font_name, font_size)), sg.Spin([i for i in range(8,32,2)], initial_value=font_size, key='-FONT_SIZE-')],
                   [ sg.Text(mess[lang]['11'], font=(font_name, font_size)), sg.Radio(mess[lang]['12'],'Language', key='-LANG_EN-', font=(font_name, font_size)), sg.Radio(mess[lang]['13'],'Language', key='-LANG_FR-', font=(font_name, font_size))],
                   [ sg.VPush(), sg.Button(mess[lang]['14'], key='-REFRESH-', font=(font_name, font_size))]]

    # The TabgGroup layout - it must contain only Tabs
    tab_group_layout = [[ sg.TabGroup([[sg.Tab(mess[lang]['15'], tab1_layout, key='-TAB1-', font=(font_name)),
                          sg.Tab(mess[lang]['30'], tab2_layout, key='-TAB2-'),
                          sg.Tab(mess[lang]['9'], tab3_layout, key='-TAB3-'),
                          sg.Tab(mess[lang]['16'], tab4_layout, key='-TAB4-')]], expand_x=True, expand_y=True) ]]

    # The window layout - defines the entire window
    layout = [[sg.TabGroup(tab_group_layout,
                           enable_events=True,
                           key='-TABGROUP-'),
                           sg.Sizegrip()]]



    # create the window
    window = sg.Window(mess[lang]["1"], layout, resizable=True, location=(50,50), finalize=True)

    while True:
        event, values = window.read()       # type: str, dict
        #print(event, values)
        if event == sg.WIN_CLOSED:
            break

        if event == '-REFRESH-':
            new_theme = values['-THEME LIST-']
            if new_theme == 'Random':
                new_theme=None
            font_name = values['-FONT_NAME-']
            font_size = values['-FONT_SIZE-']
            if values['-LANG_FR-']:
                lang = "FR"
            if values['-LANG_EN-']:
                lang = "EN"
            filename=''
            table_1=[]
            table_2=[]
            dict_letter={}
            summary_dict={}
            window.close()
            main_window(lang, new_theme, font_name)
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
                rc, dict_letter, numpy_cpt, summary_dict = comptage(filename)
                if rc != 0:
                    sg.popup(mess[lang]['38'], no_titlebar=True, keep_on_top=True)
                else:
                    data_to_graph(dict_letter, numpy_cpt, summary_dict, lang)
            else:
                sg.popup(mess[lang]['18'], no_titlebar=True, keep_on_top=True)
        if event == '-TO_CSV-':
            if summary_dict == {}:
                sg.popup(mess[lang]['18'], no_titlebar=True, keep_on_top=True)
            else:
                data_summary=[]
                data_full=[]
                skip_it = False
                cr_write = True
                if not os.path.isdir('/tmp'):
                    try:
                        os.makedirs('/tmp')
                    except:
                        sg.popup(mess[lang]['39'], no_titlebar=True, keep_on_top=True)
                        skip_it = True
                        
                if not skip_it:
                    entete_summary=[mess[lang]['21'], mess[lang]['22'], mess[lang]['23'], mess[lang]['24'], mess[lang]['25'], mess[lang]['26']]
                    data_summary.append(list(summary_dict.values()))
                    cr_write = export_to_csv(entete_summary, data_summary,'/tmp/summary_data.csv')
                    if cr_write:
                        entete_full = [mess[lang]['28'], mess[lang]['29']]
                        for elem in dict_letter.keys():
                            if elem > 32 and elem < 127:
                                prn_elem = chr(elem)
                            else:
                                prn_elem = "ASCII("+str(elem)+")"
                            data_full.append([prn_elem, dict_letter[elem]])
                        cr_write = export_to_csv(entete_full, data_full,'/tmp/full_data.csv')
                    if cr_write:
                        sg.popup(mess[lang]['40'], no_titlebar=True, keep_on_top=True, background_color = 'green', text_color = 'black')
                        window['-TAB2-'].update(background_color = 'yellow')
                    else:
                        sg.popup(mess[lang]['41'], no_titlebar=True, keep_on_top=True)

    window.close()
main_window()
