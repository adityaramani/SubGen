
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
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from timeit import default_timer as timer


try:
    from shhlex import quote
except ImportError:
    from pipes import quote

from  constants import *
import os
import signal

from multiprocessing.connection import Listener


for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-2s [%(process)d] %(message)s')

logger  = logging.getLogger("Speech Recognizer")




def writePidFile():
    pid = str(os.getpid())
    f = open('../tmp/recognizer.pid', 'w')
    f.write(pid)
    f.close()


writePidFile()


q = queue.Queue()
seen = set({})



def infer(file_path):
    fin = wave.open(file_path, 'rb')
    fs = fin.getframerate()
    if fs != 16000:
        logger.info('Warning: original sample rate ({}) is different than 16kHz. Resampling might produce erratic speech recognition.'.format(fs))
        fs, audio = convert_samplerate(audio_path)
    else:
        audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)

    audio_length = fin.getnframes() * (1/16000)
    fin.close()

    inference_start = timer()

    inf = ds.stt(audio, fs) 
    
    
    logger.info("Inference  = " + inf)

    conn_two.send(file_path+"$$"+inf)
    os.kill(pid,signal.SIGXFSZ)

    inference_end = timer() - inference_start
    logger.info('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length))


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
            # do whatever work you have to do on work
            logging.debug("Infering File  :" + p)
            infer(p)

            self.q.task_done()


worker = Worker(q)
worker.start()



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

address_two = ('localhost', 6001)
listener_two = Listener(address_two)



logger.info('Loading model from file {}'.format(model_path))
model_load_start = timer()
ds = Model(model_path, N_FEATURES, N_CONTEXT, alphabet_path, BEAM_WIDTH)
model_load_end = timer() - model_load_start
logger.info('Loaded model in {:.3}s.'.format(model_load_end))


logger.info('Loading language model from files {} {}'.format(lm_path, trie_path))
lm_load_start = timer()
ds.enableDecoderWithLM(alphabet_path, lm_path, trie_path, LM_ALPHA, LM_BETA)
lm_load_end = timer() - lm_load_start
logger.info('Loaded language model in {:.3}s.'.format(lm_load_end))



conn_two = listener_two.accept()

with open('../tmp/player.pid' ,'r') as fp:
    pid =  int(fp.read())










def convert_samplerate(audio_path):
    sox_cmd = 'sox {} --type raw --bits 16 --channels 1 --rate 16000 --encoding signed-integer --endian little --compression 0.0 --no-dither - '.format(quote(audio_path))
    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('SoX returned non-zero status: {}'.format(e.stderr))
    except OSError as e:
        raise OSError(e.errno, 'SoX not found, use 16kHz files or install it: {}'.format(e.strerror))

    return 16000, np.frombuffer(output, np.int16)
