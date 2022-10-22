import urllib3
import sys
import PySimpleGUI as sg
import os

def dl_file(url_file,chunk_size):
    out_file='/tmp/bidon'
    go_dl = False
    content_bytes = 0
    http = urllib3.PoolManager()

    r = http.request( 'GET', url_file, preload_content=False)
    content_bytes = r.headers.get("Content-Length")
    if content_bytes is None:
        content_bytes = 0
    else:
        content_bytes = int(content_bytes)

    with open(out_file, "wb") as f:
        dl_size = 0
        for chunk in r.stream(chunk_size):
            f.write(chunk)
            dl_size = dl_size + chunk_size
            if content_bytes != 0:
                go_dl = sg.one_line_progress_meter('Downloading file',dl_size,content_bytes)
                if not go_dl:
                    sg.one_line_progress_meter_cancel()
                    break
            else:
                print ("Ca charge : "+str(dl_size)+" Ko")
                go_dl = True
    r.release_conn()
    if not go_dl:
        os.remove(out_file)

dl_file('https://www.transfernow.net/dl/20221020WowODQwK',1024)

