'''
import os
import signal

from multiprocessing.connection import Listener

address = ('localhost', 6000)
listener = Listener(address)
conn = listener.accept()

with open('../tmp/player.pid' ,'r') as fp:
    pid =  int(fp.read())


while True:
    
    with open('../tmp/player.pid' ,'r') as fp:
        pid =  int(fp.read())


    msg = input()
    conn.send(msg+'\n')
    os.kill(pid,signal.SIGXFSZ )


'''

import threading
import argparse
import queue
import numpy as np
import shlex
import subprocess
import sys
import wave
import logging
from deepspeech import Model
from timeit import default_timer as timer

try:
    from shhlex import quote
except ImportError:
    from pipes import quote


import os
import signal

from multiprocessing.connection import Listener


queue = queue.Queue()

def writePidFile():
    pid = str(os.getpid())
    f = open('../tmp/recognizer.pid', 'w')
    f.write(pid)
    f.close()


writePidFile()


for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-2s [%(process)d] %(message)s')




logger  = logging.getLogger("Speech Recognizer")



address = ('localhost', 6000) # TCP CONNECTION
address_two = ('localhost', 6001)

listener = Listener(address)
listener_two = Listener(address_two)

# These constants control the beam search decoder

# Beam width used in the CTC decoder when building candidate transcriptions
BEAM_WIDTH = 500

# The alpha hyperparameter of the CTC decoder. Language Model weight
LM_ALPHA = 0.75

# The beta hyperparameter of the CTC decoder. Word insertion bonus.
LM_BETA = 1.85


# These constants are tied to the shape of the graph used (changing them changes
# the geometry of the first layer), so make sure you use the same constants that
# were used during training

# Number of MFCC features to use
N_FEATURES = 26

# Size of the context window used for producing timesteps in the input vector
N_CONTEXT = 9



model_path = "/home/aditya/Documents/project/indian_model/prebuilt/deepspeech-0.4.1-models/models/output_graph.pb"
model_path = "/home/aditya/Documents/project/indian_model/prebuilt/deepspeech-0.4.1-models/models/output_graph.pbmm"
alphabet_path = "/home/aditya/Documents/project/indian_model/prebuilt/deepspeech-0.4.1-models/models/alphabet.txt"
lm_path = '/home/aditya/Documents/project/indian_model/prebuilt/deepspeech-0.4.1-models/models/lm.binary'
trie_path = "/home/aditya/Documents/project/indian_model/prebuilt/deepspeech-0.4.1-models/models/trie"




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



conn = listener.accept()
conn_two = listener_two.accept()

with open('../tmp/player.pid' ,'r') as fp:
    pid =  int(fp.read())


class Worker(threading.Thread):
    def __init__(self, q):
        self.q = q
        super().__init__()

    def run(self):
        while True:
            try:
                work = self.q.get(timeout=3)  # 3s timeout
            except queue.Empty:
                pass
            # do whatever work you have to do on work
            infer(work)

            self.q.task_done()




w = Worker(queue)
w.start()


def add_to_queue(*args):
    
    msg = conn.recv()
    queue.put(msg)




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

    conn_two.send(inf)
    os.kill(pid,signal.SIGXFSZ)

    inference_end = timer() - inference_start
    logger.info('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length))







signal.signal(signal.SIGXFSZ, add_to_queue)  # regestering signal handler for SIGXFSZ



while True:
    pass



def convert_samplerate(audio_path):
    sox_cmd = 'sox {} --type raw --bits 16 --channels 1 --rate 16000 --encoding signed-integer --endian little --compression 0.0 --no-dither - '.format(quote(audio_path))
    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('SoX returned non-zero status: {}'.format(e.stderr))
    except OSError as e:
        raise OSError(e.errno, 'SoX not found, use 16kHz files or install it: {}'.format(e.strerror))

    return 16000, np.frombuffer(output, np.int16)
