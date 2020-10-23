import os, sys
import http.server
import socketserver
import webbrowser
import time
import socket
from datetime import datetime

def fn_as_path():
    return os.path.join(os.path.dirname(sys.argv[0]), os.path.splitext(os.path.basename(sys.argv[0]))[0])

def run_http(path = None):
    if path:
        os.chdir(path)
    else:
        os.chdir(fn_as_path())
    os.system('python -m http.server')

def open_web(url):
    time.sleep(3)
    webbrowser.open(url)

def host_timezone():
    ts = time.time()
    utc_offset = (datetime.fromtimestamp(ts) -
                  datetime.utcfromtimestamp(ts)).total_seconds()
    return utc_offset / 3600
