import numpy as np
import scipy.io.wavfile as wav
from time import sleep

from python_speech_features import mfcc

def read(audio_file):
    fs, audio = wav.read(audio_filename)
    return fs, audio

def audiofile_to_input_vector(audio_filename, numcep, numcontext):
    r"""
    Given a WAV audio file at ``audio_filename``, calculates ``numcep`` MFCC features
    at every 0.01s time step with a window length of 0.025s. Appends ``numcontext``
    context frames to the left and right of each time step, and returns this data
    in a numpy array.
    """
    # Load wav files
    while True:
        try:
            fs, audio = wav.read(audio_filename)
            print("success  ", audio_filename)
            break
        except:
            sleep(1)
            print("sleeping")
            continue
    # Get mfcc coefficients
    features = mfcc(audio, samplerate=fs, numcep=numcep, winlen=0.032, winstep=0.02, winfunc=np.hamming,nfft=2048)


    # Add empty initial and final contexts
    empty_context = np.zeros((numcontext, numcep), dtype=features.dtype)
    features = np.concatenate((empty_context, features, empty_context))

    return features
