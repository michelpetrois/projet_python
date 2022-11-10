import gc
import psutil
from pathlib import Path
import time as t
import numpy as np
import collections as col
import threading


# Version 1.1
c=col.Counter()
passwords_length=np.array(0)

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
    di["Imprimables"]=imprim
    autres=0
    for i in range(0,31):
        autres+=dico[i]
    for i in range(127,255):
        autres+=dico[i]
    di["Autres"]=autres
    return di
def compte(bloc):
    global c,passwords_length
    local=col.Counter(bloc)
    c+=local
    pwa=np.array(bloc.splitlines())
    get_len = np.vectorize(lambda str: len(str))
    pwl=np.array(get_len(pwa))
    print(passwords_length)
    print(pwl)
    passwords_length=np.add(passwords_length,pwl)

def comptage(filename):
    start_time = t.time()
    global c, passwords_length
    # Optimisation section
    gc.collect()
    ram=list(psutil.virtual_memory())[4]
    file_size =Path(filename).stat().st_size
    if (2*file_size) < ram:
        fd = open(filename, "rb")
        passwords = fd.read()
        passwods_arr = np.array(passwords.splitlines())
        get_len = np.vectorize(lambda str: len(str))
        passwords_length = np.array(get_len(passwods_arr))
        c=col.Counter(passwords)
        end_time = t.time()
        print("Process time: ", end_time - start_time)
        d = dict(c)
        e=calc(c)
        return 0,d,passwords_length,e

    #magicn=int(ram/4)
    magicn=256*1024*1024
    print(ram,magicn,file_size,ram-magicn,file_size/magicn)
    threads=list()
    with open(filename,"rb") as f:
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
    d=dict(c)
    e=calc(d)
    return 0,d,passwords_length,e

