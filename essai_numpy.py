# pour matplotlib seul
import numpy as np
import matplotlib.pyplot as plotter
# a ajouter pour grapher dans pysimplegui
from matplotlib.ticker import NullFormatter  # useful for `logit` scale
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
matplotlib.use('TkAgg')

# integration de la figure dans le canva de la window de PySimpleGUI
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def graph1(entete, data):

    # graph pie dans matplotlib
    figureObject, axesObject = plotter.subplots() # init de la frame pour les graphes, retoure une Figure (frame) et des axes, possible de definr la taille ici
    axesObject.pie(data,          # liste de datas a grapher
                   labels = entete,      # tuple de titres sur les slices
                   startangle=90,       # le demarrage de la rotation des slices
                   autopct = '%1.1f%%', # format et valur de la slice dans la pie
                   shadow = True)       # petit effet d'ombre, pas terrible sans slices detachees
    axesObject.set_title('Repartion des tailles')
    axesObject.axis('equal')            # concerve les proportion sur les axes pour pas que les cercles ressembles a des elipses
#    plotter.show()                      # affichage du graph

    # graph histogramme dans matplotlib
    print(entete)
    print(data)
    figureObject1, axesObject1 = plotter.subplots() # init de la frame pour les graphes, retoure une Figure (frame) et des axes, possible de definr la taille ici
    axesObject1.bar(entete, data)

    axesObject1.set(xticks=entete,
                    yticks=data,
                    xlabel='Taille',
                    ylabel='Nombre')
    axesObject1.set_title('Tailles')
    plotter.show()                      # affichage du graph

    ####### fin graph pie avec matplotlib

    # meme pie dans une window

    # define the window layout
    layout = [ [sg.Canvas(key='-CANVAS-'), sg.Canvas(key='-CANVAS1-')],
              [sg.Button('Ok',key='Exit')]]
    # define Window
    window = sg.Window('test window de graphes', layout, finalize=True, element_justification='center', font='Helvetica 18', resizable=True)
    # ajout du  graph dans window
    fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, figureObject) # on passe en argument la Figure qu'on a defini pour le graph matplotlib
    fig_canvas_agg1 = draw_figure(window['-CANVAS1-'].TKCanvas, figureObject1) # on passe en argument la Figure qu'on a defini pour le graph matplotlib


    while True :
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

    window.close()    


a = np.array([1, 1, 2, 3, 4, 1, 2, 5, 6, 7, 2, 3, 1, 2, 4, 8, 9, 0, 4, 1, 2, 6, 2, 6, 2, 1, 9])
entete, cumul = np.unique(a, return_counts=True)
#print(entete)
#print(entete.ndim)
#print(entete.shape)
#print(cumul)
#print(cumul.ndim)
#print(cumul.shape)
taille = np.shape(entete)
deux_dim = np.vstack((entete, cumul))
#print(a)
#print(entete)
#print(cumul)
#print(deux_dim)
#print(deux_dim.ndim)
#print(deux_dim.shape)

graph1(entete, cumul)
