
import logging
import subprocess
import threading
from pydub import AudioSegment

from multiprocessing.connection import Client
from pydub.silence import split_on_silence
from timeit import default_timer as timer
from pathlib import Path
import os
import time 
import signal

SPLIT_INTERVAL = 10

logger = logging.getLogger("SpeechToText")


class ExtractAudio(threading.Thread):

    def __init__(self, audio_path):
        threading.Thread.__init__(self)
        self.audio_path = audio_path[0]
        Path("/tmp/stt/").mkdir(exist_ok=True)

        self.audio_length = int(float(subprocess.run(["ffprobe" ,"-i" , self.audio_path ,
                                        "-show_entries","format=duration", "-v" ,"quiet" ,"-of" ,'csv=p=0'],
                                        stdout=subprocess.PIPE).stdout.decode('utf-8').strip()))

    
    def extract_audio (self):
        logger.debug("Starting Extarct")
        ts = timer()
        intermediate_name = 0
        
        for i in range(0, self.audio_length-SPLIT_INTERVAL, SPLIT_INTERVAL):
            start_time =  time.strftime('%H:%M:%S', time.gmtime(i))
            end_time =  time.strftime('%H:%M:%S', time.gmtime(i+SPLIT_INTERVAL))
            print(start_time , end_time)
            subprocess.run(["ffmpeg"#,"-nostats", "-loglevel", "0" 
                            ,"-ss",str(i), "-i" , self.audio_path 
                            ,"-t", str(SPLIT_INTERVAL) 
                            ,"-acodec", "pcm_s16le", "-ar" , "16000"
                            , "-ac" ,"1" ,#'-af', 'highpass=f=200, lowpass=f=800',
                            "-vn" ,"/tmp/stt/" + str(intermediate_name)+".wav", "-y"])
            logger.debug("Chunk " +  str(intermediate_name)+" in {}s ".format( timer()))
            
            intermediate_name+=1
        
        logger.debug("Finished Extarcting  in {:.3}s ".format(timer() - ts))
    

    def run(self):
        
        self.extract_audio()
        
class SpeechRecognizer():
    
    def __init__(self, config):
        pass

    def infer(self, audio ):
        pass


if __name__ == "__main__":
    ExtractAudio(["/home/aditya/Downloads/indian.mp4"]).start()