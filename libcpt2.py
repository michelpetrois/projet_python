import gc
import psutil
from pathlib import Path
import time as t
import numpy as np
import collections as col
import threading


# Version 1.0
c = col.Counter()

def read_in_chunks(file_object, chunk_size=1024):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def compte(bloc):
    global c,passwords_length
    print("dans compte",passwords_length)
    local=col.Counter(bloc)
    c+=local
    pwa=np.array(bloc.splitlines())
    get_len = np.vectorize(lambda str: len(str))
    pwl=np.array(get_len(pwa))
    passwords_length += pwl

def comptage(filename):
    start_time = t.time()

    # Optimisation section
    gc.collect()
    ram=list(psutil.virtual_memory())[4]
    file_size =Path(filename).stat().st_size
    if file_size+(1024*1024) < ram: # sortir proprement si la taill de la RAM est pas bonne
    #if file_size+(2048*1024*1024) < ram:
        fd = open(filename, "rb")
        passwords = fd.read()
        passwods_arr = np.array(passwords.splitlines())
        get_len = np.vectorize(lambda str: len(str))
        passwords_length = np.array(get_len(passwods_arr))
        c=col.Counter(passwords)
        end_time = t.time()
        print("Process time: ", end_time - start_time)
        return c,passwords_length

    #magicn=int(ram/4)
    magicn=256*1024*1024
    print(ram,magicn,file_size,ram-magicn,file_size/magicn)
    threads=list()
    with open(filename,"rb") as f:
        print("dans comptage",passwords_length)
        for passwords in read_in_chunks(f,magicn):
           x = threading.Thread(target=compte, args=(passwords,))
           threads.append(x)
           x.start()
           end_time = t.time()
           print("Process time: ", end_time - start_time)
    for index, thread in enumerate(threads):
        thread.join()
    end_time = t.time()
    print("Process time: ", end_time - start_time)
    return c,passwords_length


c,p = comptage('/winbad/rockyou2021_1000.txt')

print(str(type(c)))
print(c) #  voir pour sortir c au format dico genre { valeur_ascii: comptage_caractere, ..... } j'ai deja un bout de code qui sait traiter ca pour en faire un tableau, oun un numpay a 2 dimensions ou 2 numpy
         # pour la synthese des caracteres (existe pas today)
         # caracteres imprimables entre 33 et 126 inclus
         # caracteres alpha maj entre 65 et 90 inclus
         # caracteres alpha min entre 97 et 122 inclus
         # caracteres num entre 48 et 57 inclus
         # caracterss spe sur les autres plages
         # sortie soit en 2 array a une dimension (un tableau pour le type et un tableau pour le comptage) soit un tableau a 2 dimensions (["alpha_maj", "alpha_min", "num", "spe", "no_print"],[cpt_alpha_maj, cpt_alpha_min, ......]) Aujourd'hui j'ai du code pour traiter 2 tableaux a 1 dimension
print(str(type(p)))
print(p) # en l'etat c'est gerable



