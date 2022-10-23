import gc
import psutil
from pathlib import Path
import time as t
import numpy as np
import collections as col
import threading


# Version 1.0
c=col.Counter()

def read_in_chunks(file_object, chunk_size=1024):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def compte(bloc):
    global c,passwords_length
    local=col.Counter(bloc)
    c+=local
    pwa=np.array(bloc.splitlines())
    get_len = np.vectorize(lambda str: len(str))
    pwl=np.array(get_len(pwa))
    passwords_length+=pwl

def comptage(filename):
    start_time = t.time()

    # Optimisation section
    gc.collect()
    ram=list(psutil.virtual_memory())[4]
    file_size =Path(filename).stat().st_size
    if file_size+(2048*1024*1024) < ram:
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




c,p = comptage('/winbad/file_to_analyze.txt')

print(c)
print(p)


