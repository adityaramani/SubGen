import io
import os

import csv

from speech_recognition.speech_recognition import *

rnn = RNNEngine()
 
'''

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types




# Instantiates a client
client = speech.SpeechClient()








# Loads the audio into memory
with io.open("/Users/aramani/Downloads/geeky/42.wav", 'rb') as audio_file:
    content = audio_file.read()
    audio = types.RecognitionAudio(content=content)

config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code='en-US')

# Detects speech in the audio file
response = client.recognize(config, audio)

for result in response.results:
    print('Transcript: {}'.format(result.alternatives[0].transcript))
'''
