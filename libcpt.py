import gc
import psutil
from pathlib import Path
import numpy as np
import collections as col
import threading

# Version 0.x : tests, benchs wtih chunck size and threads
# Version 1.0 : Lecture en une fois et thread si file trop gros
# Version 1.1 : Bug avec numpy corrigé dans thread, ajout du calcul MAJ,min....
# Version 1.2 : Exception sur IO et Threads (intégré dans lib en fait)
# Version 1.3 : Nettoyage du code

# Var globales a cause threads
c=col.Counter()
passwords_length=np.array(0)
e=dict()
d=dict()

def read_in_chunks(file_object, chunk_size=1024):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def calc(dico):
    di=dict()
    MAJ=0
    for i in range(65,90):
        MAJ+=dico[i]
    di["Majuscules"]=MAJ
    min=0
    for i in range(97,122):
        min+=dico[i]
    di["Minuscules"]=min
    num=0
    for i in range(48,57):
        num+=dico[i]
    di["Numeriques"]=num
    imprim=0
    for i in range(32,64):
        imprim+=dico[i]
    for i in range(91,96):
        imprim+=dico[i]
    for i in range(123,126):
        imprim+=dico[i]
    di["Caracteres"]=imprim
    autres=0
    for i in range(0,31):
        autres+=dico[i]
    autres+=dico[127]
    di["Caractere Controle"]=autres
    autres=0
    for i in range(128,255):
        autres+=dico[i]
    di["ASCII Etendu"]=autres
    return di
def compte(bloc):
    global c,passwords_length
    local=col.Counter(bloc)
    c+=local
    pwa=np.array(bloc.splitlines())
    get_len = np.vectorize(lambda str: len(str))
    pwl=np.array(get_len(pwa))
    passwords_length=np.add(passwords_length,pwl)

def comptage(filename):
    global c, passwords_length,e,d
    gc.collect()
    ram=list(psutil.virtual_memory())[4]
    try:
        file_size =Path(filename).stat().st_size
    except (IOError,FileNotFoundError) as exc:
        e["Erreur"]=exc
        return 1,d,passwords_length,e
    if (2*file_size) < ram:
        try:
            fd = open(filename, "rb")
        except (IOError,FileNotFoundError) as exc:
            e["Erreur"]=exc
            return 1, d, passwords_length, e
        passwords = fd.read()
        compte(passwords)
    else:
        magicn=256*1024*1024
        threads=list()
        try:
            with open(filename,"rb") as fd:
                for passwords in read_in_chunks(fd,magicn):
                    x = threading.Thread(target=compte, args=(passwords,))
                    threads.append(x)
                    x.start()
        except (IOError,OSError,FileNotFoundError) as exc:
            e["Erreur"] = exc
            return 1, d, passwords_length, e
        for index, thread in enumerate(threads):
            thread.join()
    d=dict(c)
    e=calc(c)
    return 0,d,passwords_length,e

