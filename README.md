## pour tester des trucs
- essai_dict2cvulticol.py : extraction d'un dico vers un fichier CSV et une presentation dans une table PySimpleGUI
- essai_dl_big.py         : test DL gros fichier non text avec possibilité de cancel (marche pas)
- essai_messages.py       : test pour variabiliser les messages du front (marche en place dans le code principal)
- essai_mutiwindows.py    : code recup pour tester du multi fenetrage (pas utilise)
- essai_numpy.py          : test de manip de numpy + graph matplotlib + integration dans le front (en cours)
- demo_pie.py             : demo de construction d'un pie via matplotlib
- essai_gui2.py : demo gestion windows
- demo_pie.py : demo de matplotlib camembert
- demo_histo.py : demo de matplotlib histogramme
## Code projet utilisable
- essai_gui.py  : partie graphique
- libcpt2.py    : partie back avec fichier entree en dur
- libcpt.py     : partie back 
### A faire
- gerer le "abort" sur les DL de fichiers ou on a pas la taille (ou alors interdire ce type de fichier)
- sur la sortie du back faire un return avec 
    - un array pour les caracteres en detail (caractere/nobre)
    - un ou plusieurs tableaux avec le detail (comptage par type de caractere)
    - un tableau avec les longueurs de mot de passe
- mieux gerer les condition d'echec du back pour retourner de quoi affichier un message propre depuis le front
- integrer les 2 scripts d'essai : essai_dict2cvulticol.py et essai_numpy.py dans le code du front pour les affichages dans les tabs


