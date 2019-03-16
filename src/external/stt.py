
import logging
import subprocess
import threading
from pydub import AudioSegment
from multiprocessing.connection import Client
from pydub.silence import split_on_silence
import os

import signal


logger = logging.getLogger("SpeechToText")


class ExtractAudio(threading.Thread):

    def __init__(self, audio_path):
        threading.Thread.__init__(self)
        self.audio_path = audio_path[0]

    def extract_audio (self):
        logger.debug("Starting Extarct")
        subprocess.run(["ffmpeg", "-ss","00:00:00", "-i" , self.audio_path,'-to', "00:02:00" ,"-acodec", "pcm_s16le", "-ar" , "16000", "-ac" ,"1" ,"-vn" ,"../tmp/1.wav", "-y"])
        logger.debug("Finished Extarct")
    
    def run(self):
        self.extract_audio()
        sound_file = AudioSegment.from_wav("../tmp/1.wav")
        logger.debug("Started segmenting")

        audio_chunks = split_on_silence(sound_file,
        # must be silent for at least half a second
        min_silence_len=300,
        # consider it silent if quieter than -16 dBFS
        silence_thresh=-20)

        logger.debug("Finished segmenting " + str(len(audio_chunks)))
        
        address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
        conn   = Client(address)
        
        with open('../tmp/recognizer.pid' ,'r') as fp:
            pid =  int(fp.read())

        for i, chunk in enumerate(audio_chunks):
            out_file = "../tmp/chunk{0}.wav".format(i)
            chunk.export(out_file, format="wav")
            logger.info("Sending "  + out_file)
            conn.send(out_file)
            print(pid)
            os.kill(pid,signal.SIGXFSZ)
        # conn.close()

class SpeechRecognizer():
    
    def __init__(self, config):
        pass

    def infer(self, audio ):
        pass