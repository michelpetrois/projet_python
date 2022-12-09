import PySimpleGUI as sg
import os
import urllib3
import sys
import io
import base64
from libcpt import *
import numpy as np
import matplotlib.pyplot as plotter
from matplotlib.ticker import NullFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')
import csv


mess = {}
mess["EN"]={'1': 'Characters Analysis', '2': 'Downloading file', '3': 'Abort Download ?', '4': 'Language', '5': 'OR', '6': 'Font', '7': 'Size', '8': 'Character Types', '9': 'Output Graphs', '10': 'Name', '11': 'Select The Language', '12': 'English', '13': 'French', '14': 'Refresh Settings', '15': 'Input', '16': 'Settings', '17': 'No Filename', '18': 'File not found', '19': 'Browse', '20': 'Passwords by size', '21': 'Uppercase', '22': 'Lowercase', '23': 'Digits', '24': 'Characters', '25': 'Control', '26': 'Extended', '27': 'Character count', '28': 'Char', '29': 'Count', '30': 'Output Tables', "31": 'Font Choice', '32': 'Font size', '33': 'Types', '34': 'Numbers', '35': 'Characters by type', '36': 'length', '37': 'Export to CVS', '38': 'Error processing datas', '39': 'No access to the directory', '40': 'Success', '41': 'Failed', '42': 'File', '43': 'Exit', '44': 'Help', '45': 'About', '46': 'Input File', '47': 'Launch', '48': 'URL', '49': 'CSV Destination'}

mess["FR"]={'1': "Analyse des caractères d'un fichier", '2': 'Téléchargement en cours', '3': 'Abandon du téléchargeent ?', '4': 'Langue', '5': 'OU', '6': 'Police', '7': 'Taille', '8': 'Types de caractères', '9': 'Sortie Graphes', '10': 'Name', '11': 'Choix du langage', '12': 'Anglais', '13': 'Français', '14': "Relancer l'interface", '15': 'Entrée', '16': 'Paramètres', '17': 'Nom de fichier manquant', '18': 'Fichier introuvable', '19': 'Parcourir', '20': 'Mots de passe par taille', '21': 'Majuscules', '22': 'Minuscules', '23': 'Numérique', '24': 'Caractères', '25': 'Contrôle', '26': 'Etendus', '27': 'Comptage des caractères', '28': 'Carac', '29': 'Compt', '30': 'Sortie Tableaux', '31': 'Choix de la police', '32': 'Taille de la police', '33': 'Types', '34': 'Occurences', '35': 'Caractères par types', '36': 'Longueur', '37': 'Exporter en CSV', '38': 'Erreur dans le traitement des données', '39': 'repertoire cible inaccessible', '40': 'Reussi', '41': 'En echec', '42': 'Fichier', '43': 'Sortie', '44': 'Aide', '45': 'Quoi', '46': 'Fichier en Entrée', '47': 'Lancer', '48': 'URL', '49': 'Destination des fichiers CSV' }

version='V1.2'
lang = 'EN'
list_lang = [mess[lang]['12'], mess[lang]['13']]
list_font_size = [ str(taille) for taille in range(8,31,2)]
list_font_name = sg.Text.fonts_installed_list()
list_theme = sg.theme_list()
theme = None
font = 'courier'
size = 15
img = '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'

aide={'FR': "Comment procéder à une annalyse ?\nChoisir l'emplacement du fichier : local ou sur une serveur https (Fichier/Source/Local ou Fichier/Source/Url)\nLancer l'analyse (Fichier/Lancer) : cela va conduire a deux tableaux de données et un camembert, pour passer à l'histogramme, il faut fermer la fenetre du camembert.\nPour sortir les 2 tableaux au format CSV prendre le menu CSV, choisir en premier la destination des fichiers (CSV/Destination) par defaut le repertoire cible est /tmp\npuis l'action d'export (CSV/Export) les deux fichiers sont summary_data.csv et full_data.csv\nPour quitter choisir (Fichier/Sortie) ou sur la X de la fenetre principale.", 'EN': "How to make an analyze ?\nChoose where the file is located : either local or targeted by an URL (File/Source/local or File/Source/Url)\nLaunch analyze (File/Launch): first you will see 2 arrays and a pie graph, to see histobar graph please close the pie graph\nTo export arrays within CSV files, first choose the destination of files (CSV/Destination), the default directory is /tmp and then Export (CSV/Export), the two files are summary_data.csv and full_data.csv\nTo close application you either choose exit (File/Exit) or click X on the top right of the main window"}
filename=':'
table_1=[]
table_2=[]
table1_header=[mess[lang]['21'], mess[lang]['22'], mess[lang]['23'], mess[lang]['24'], mess[lang]['25'], mess[lang]['26']]
lib_head = [mess[lang]['28'], mess[lang]['29']]
table2_header=[alpha+'_'+str(num) for num in range(1,10) for alpha in lib_head]
csv_target='/tmp'
summary_dict = {}

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

def dl_file(url_file,chunk_size,out_file):
    global window
    go_dl = False
    content_bytes = 0
    http = urllib3.PoolManager()

    r = http.request( 'GET', url_file, preload_content=False)
    reader = io.BufferedReader(r, 8)
    content_bytes = r.headers.get("Content-Length")
    print("content_bytes", content_bytes)    
    if content_bytes is None:
        window['-ABORT_DL-'].update(visible=True )
        content_bytes = 0
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
                    event, values = window._ReadNonBlocking()
                    if event == 'ABORT_DL':
                        break

    if not go_dl:
        os.remove(out_file)


def draw_pie(entete,data,titre, lang):
    nb_slices = np.shape(entete)
    explode = np.empty(nb_slices)
    explode.fill(0.2)

    # graph pie using matplotlib
    figureObject, axesObject = plotter.subplots(num=titre)
    axesObject.pie(data,
                   labels = entete,
                   startangle=90,
                   autopct = '%1.1f%%',
                   shadow = True,
                   explode = explode)
    axesObject.axis('equal')

    plotter.show()

def draw_histo(entete,data,titre,xlabel,ylabel, lang):
    taille = entete.size
    x_max = np.max(entete)
    y_max = np.max(data)
    figureObject1, axesObject1 = plotter.subplots(figsize=(15,5), num=titre)
    axesObject1.bar(entete, data)

    axesObject1.set(xticks = np.arange(0, x_max+1, 1),
                    #yticks = np.arange(0, y_max+1, 1),
                    xlabel=xlabel,
                    ylabel=ylabel)

    for i in range(0, taille):
        plotter.text(x=entete[i] , y=data[i],  s=f"{data[i]}" )

    plotter.show()




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

def data_to_graph(dict_letter, numpy_cpt, summary_dict, lang):
    draw_table(summary_dict, 1, 1)
    draw_table(dict_letter, 9, 2)

    type_car=[mess[lang][str(i)] for i in range(21,27)]
    entete_pie = np.asarray(type_car)
    type_val=list(summary_dict.values())
    data_pie = np.asarray(type_val)
    titre_pie = mess[lang]['35']
    draw_pie(entete_pie,data_pie,titre_pie, lang)

    entete, data = np.unique(numpy_cpt, return_counts=True)
    titre  = mess[lang]['20']
    xlabel = mess[lang]['36']
    ylabel = mess[lang]['29']
    draw_histo(entete,data,titre,xlabel,ylabel, lang)


def make_window():
    global lang, list_lang, list_font_size, list_font_name, list_theme, theme, font, size, filename, window, table_1, table_2
    sg.theme(theme)
    menu_def = [[mess[lang]['42'], ['Source', ['Local', 'Url'], mess[lang]['47'], mess[lang]['43']]],
                ['CSV', ['Destination', 'Export']],
                [mess[lang]['16'], [ mess[lang]['4'], list_lang, 'Theme', list_theme, mess[lang]['6'], [mess[lang]['10'], list_font_name, mess[lang]['7'], list_font_size ]]],
                ['?', [ mess[lang]['44'], mess[lang]['45']]]]
    layout_menu = [[sg.MenubarCustom(menu_def, key='-MENU-', font=(font, size), bar_font=(font,size), tearoff=True)]]
    layout_file_choice = [[sg.Text(mess[lang]['46']), sg.Text(':'), sg.FileBrowse(mess[lang]['19'], key='-INPUT_FILENAME-', visible=False)]]
    layout_url_choice = [[ sg.Text(mess[lang]['48']), sg.Text(':'), sg.Input(size=100, key='-INPUT_URL-', visible=False, enable_events=True)], [sg.Button(mess[lang]['3'], key='-ABORT_DL-', visible=False)]]
    layout_csv_dest = [[sg.Text(mess[lang]['49']), sg.Text(':'), sg.FolderBrowse(mess[lang]['19'], key='-CSV_TARGET-', visible=False)]]
    layout_top = [[sg.Text(mess[lang]['8'])],[sg.Table(table_1, headings=table1_header,auto_size_columns=True, key='-TABLE1-', num_rows=1, hide_vertical_scroll=True)]]
    layout_middle = [[sg.Text(mess[lang]['27'])], [sg.Table(table_2, headings=table2_header,auto_size_columns=True, key='-TABLE2-', num_rows=25, hide_vertical_scroll=False, vertical_scroll_only=False)]]

    layout = layout_menu + layout_file_choice + layout_url_choice + layout_csv_dest + layout_top + layout_middle 
#    window = sg.Window(mess[lang]['1'], layout, grab_anywhere=True, resizable=True, margins=(0,0), use_custom_titlebar=True, finalize=True, keep_on_top=True)
    window = sg.Window(mess[lang]['1'], layout, resizable=True, location = (10, 50) )
    return window


def main():
    global lang, list_lang, list_font_size, list_font_name, list_theme, theme, font, size, filename, table_1, table_2, csv_target, summary_dict
    window = make_window()
    while True:
        event, values = window.read()       # type: str, dict
        print(event, values, list_lang)
        print('font', font,"size",size)
        if event == sg.WIN_CLOSED or event == mess[lang]['43']:
            break
        # Source
        if event == 'Local':
            window['-INPUT_FILENAME-'].update(mess[lang]['19'], visible=True)
        if event == 'Url':
            window['-INPUT_URL-'].update(visible=True)
        # CSV
        if event == 'Destination':
            window['-CSV_TARGET-'].update(visible=True)
            print("fonction destination CSV")
        if event == 'Export':
            if values['-CSV_TARGET-'] != '':
                csv_target = values['-CSV_TARGET-']
            if summary_dict == {}:
                sg.popup(mess[lang]['38'], no_titlebar=True, keep_on_top=True,  background_color='red', text_color='black')
            else:
                data_summary=[]
                data_full=[]
                skip_it = False
                cr_write = True
                if not os.path.isdir(csv_target):
                    try:
                        os.makedirs(csv_target)
                    except:
                        sg.popup(mess[lang]['39'], no_titlebar=True, keep_on_top=True,  background_color='red', text_color='black')
                        skip_it = True

                if not skip_it:
                    entete_summary=[mess[lang]['21'], mess[lang]['22'], mess[lang]['23'], mess[lang]['24'], mess[lang]['25'], mess[lang]['26']]
                    data_summary.append(list(summary_dict.values()))
                    cr_write = export_to_csv(entete_summary, data_summary,csv_target+'/summary_data.csv')
                    if cr_write:
                        entete_full = [mess[lang]['28'], mess[lang]['29']]
                        for elem in dict_letter.keys():
                            if elem > 32 and elem < 127:
                                prn_elem = chr(elem)
                            else:
                                prn_elem = "ASCII("+str(elem)+")"
                            data_full.append([prn_elem, dict_letter[elem]])
                        cr_write = export_to_csv(entete_full, data_full,csv_target+'/full_data.csv')
                    if cr_write:
                        sg.popup(mess[lang]['40'], no_titlebar=True, keep_on_top=True, background_color = 'green', text_color = 'black')
                    else:
                        sg.popup(mess[lang]['41'], no_titlebar=True, keep_on_top=True,  background_color='red', text_color='black')
                print("fonction lancement de l'export")
        # Settings
        if event in list_lang:
            if event == mess[lang]['12']:
                lang = 'EN'
            if event == mess[lang]['13']:
                lang = 'FR'
            list_lang = [mess[lang]['12'], mess[lang]['13']]
            table_1 = []
            table_2 = []
            print("LANG", lang)
            window = make_window()
        if event in list_theme:
            table_1 = []
            table_2 = []
            theme = event
            print("THEME", theme)
            window = make_window()
        if event in list_font_size:
            table_1 = []
            table_2 = []
            size = int(event)
            print('SIZE', size)
            window = make_window()
        if event in list_font_name:
            font =  event
            table_1 = []
            table_2 = []
            print('FONT', font)
            window = make_window()
        # divers
        if event == mess[lang]['44']:
             sg.popup(aide[lang], no_titlebar=True, keep_on_top=True, background_color='yellow', text_color='black')
        if event == mess[lang]['45']:
            sg.popup(title=version, image=base64.b64decode(img), location=(50,50))
        # launch analyze
        if event == mess[lang]['47']:
            if values['-INPUT_FILENAME-'] != '':
                filename = values['-INPUT_FILENAME-']
            else:
                if values['-INPUT_URL-'] != '':
                    file_url = values['-INPUT_URL-']
                    if not os.path.isdir('/tmp'):
                        os.makedirs('/tmp')
                        filename = '/tmp/file_to_analyze.txt'
                    if os.path.exists(filename):
                        os.remove(filename)
                    dl_file(file_url,1024,filename)

            if filename == '':
                sg.popup(mess[lang]['18'], no_titlebar=True, keep_on_top=True, background_color='red', text_color='black')
            else:
                if os.path.exists(filename):
                    rc, dict_letter, numpy_cpt, summary_dict = comptage(filename)
                    print("numpy", numpy_cpt)
                    if rc != 0:
                        sg.popup(mess[lang]['38'], no_titlebar=True, keep_on_top=True, background_color='red', text_color='black')
                    else:
                        data_to_graph(dict_letter, numpy_cpt, summary_dict, lang)
                else:
                    sg.popup(mess[lang]['18'], no_titlebar=True, keep_on_top=True,  background_color='red', text_color='black')
            
main()
