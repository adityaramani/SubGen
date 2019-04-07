
import threading
import argparse
import queue
import numpy as np
import shlex
import subprocess
import sys
from time import sleep
import wave
import logging
from deepspeech import Model
from timeit import default_timer as timer
import time
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from timeit import default_timer as timer

from speech_recogition import *
try:
    from shhlex import quote
except ImportError:
    from pipes import quote

import os
import signal

from pathlib import Path

Path("/tmp/stt").mkdir(exist_ok=True)


from multiprocessing.connection import Listener


for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(filename="../logs/server.log",filemode='w',level=logging.DEBUG,format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-2s [ %(process)d ]@ %(message)s ')

logger  = logging.getLogger("Speech Recognizer")


parser = argparse.ArgumentParser(description='Offline Subtitle Generation for videos')
parser.add_argument('-b', '--backend', help='Speech Recognition backend.',required = True ,choices = ["DS", "RNN", "SPHINX"])
__args__ = parser.parse_args()



if __args__.backend == "DS":
    backend = DeepSpeechEngine()

elif __args__.backend == "SPHINX":
    backend = SphinxEngine()

else :
    backend  = RNNEngine()



def writePidFile():
    pid = str(os.getpid())
    f = open('../tmp/recognizer.pid', 'w')
    f.write(pid)
    f.close()


writePidFile()


q = queue.Queue()
seen = set({})





class Worker(threading.Thread):
    def __init__(self, q):
        self.q = q
        super().__init__()

    def run(self):
        while True:
            try:
                p = self.q.get(timeout=3)  # 3s timeout
            except queue.Empty:
                continue
            logging.debug("Infering File  :" + p)
            
            file_path , inf = backend.infer(p)
            conn_two.send(file_path+"$$"+inf)
            os.kill(pid,signal.SIGXFSZ)
            self.q.task_done()



class Watcher(threading.Thread):
    DIRECTORY_TO_WATCH = "/tmp/stt"

    def __init__(self):
        self.observer = Observer()
        super().__init__()


    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print ("Error")

        self.observer.join()



class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            logger.debug ("Received created event - %s." % event.src_path)

        elif event.event_type == 'modified' and event.src_path not in seen:
            seen.add(event.src_path)
            print(event)
            logger.debug("Received modified event - {}. at  {}".format( event.src_path, timer()))
            q.put(event.src_path)    
            

watcher = Watcher()
watcher.start()

worker = Worker(q)
worker.start()



address_two = ('localhost', 6001)
listener_two = Listener(address_two)
conn_two = listener_two.accept()

with open('../tmp/player.pid' ,'r') as fp:
    pid =  int(fp.read())

