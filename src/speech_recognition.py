import logging
from deepspeech import Model
import wave
from abc import ABC, abstractmethod
from timeit import default_timer as timer
import numpy as np
import yaml
import subprocess
from res/speech-recognition-neural-network-master/utils.py import int_sequence_to_text
from res/speech-recognition-neural-network-master/data_generator.py import AudioGenerator
from res/speech-recognition-neural-network-master/data_generator.py import vis_train_features
from res/speech-recognition-neural-network-master/sample_models.py import *
from res/speech-recognition-neural-network-master/train_utils.py import train_model


with open("../conf/constants.yaml", 'r') as stream:
    try:
        CONF = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        exit(-1)


logger = logging.getLogger("speech_recognition")

class SpeechRecognizerBase(ABC):

    @abstractmethod
    def __init__(self, *args, **kwargs):    
        pass


    @abstractmethod
    def infer(self, file_path):
        pass


class DeepSpeechEngine(SpeechRecognizerBase):

    def __init__(self, *args, **kwargs):
        logger.info('Loading model from file {}'.format(CONF["ds.model_path"]))
        model_load_start = timer()
        
        self.ds = Model(CONF["ds.model_path"],   CONF["ds.N_FEATURES"],   CONF["ds.N_CONTEXT"],   CONF["ds.alphabet_path"],   CONF["ds.BEAM_WIDTH"])
        
        model_load_end = timer() - model_load_start
        logger.info('Loaded model in {:.3}s.'.format(model_load_end))
        logger.info('Model_Load_Time :: {:.3}.'.format(model_load_end))
        logger.info('Model_Type :: Deepspeech')


        logger.info('Loading language model from files {} {}'.format(CONF["ds.lm_path"], CONF["ds.trie_path"]))
        lm_load_start = timer()
        
        self.ds.enableDecoderWithLM( CONF["ds.alphabet_path"], CONF["ds.lm_path"], CONF["ds.trie_path"], CONF["ds.LM_ALPHA"], CONF["ds.LM_BETA"])
        
        lm_load_end = timer() - lm_load_start
        logger.info('[1.b] Loaded language model in {:.3}s.'.format(lm_load_end))


    def infer(self, file_path):
        fin = wave.open(file_path, 'rb')
        fs = fin.getframerate()
        if fs != 16000:
            logger.info('Warning: original sample rate ({}) is different than 16kHz. Resampling might produce erratic speech recognition.'.format(fs))
            fs, audio = self.convert_samplerate(audio_path)
        else:
            audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)

        audio_length = fin.getnframes() * (1/16000)
        fin.close()

        inference_start = timer()

        inf = self.ds.stt(audio, fs) 
        inference_end = timer() - inference_start
        logger.info('[2] Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length))
        
        logger.info('Inference_Time :: %0.3f' % (inference_end))
        logger.info('Audio_Length :: %0.3f' % (audio_length))
        logger.info('Model_Type :: Deepspeech')

        
        return (file_path, inf)
        

    def convert_samplerate(self, audio_path):
        sox_cmd = 'sox {} --type raw --bits 16 --channels 1 --rate 16000 --encoding signed-integer --endian little --compression 0.0 --no-dither - '.format(quote(audio_path))
        try:
            output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            raise RuntimeError('SoX returned non-zero status: {}'.format(e.stderr))
        except OSError as e:
            raise OSError(e.errno, 'SoX not found, use 16kHz files or install it: {}'.format(e.strerror))

        return 16000, np.frombuffer(output, np.int16)





class SphinxEngine(SpeechRecognizerBase):

    
    def __init__(self, *args, **kwargs):
        logger.info('Loading model from file {}'.format(CONF["sphinx.hmmpath"]))
        model_load_start = timer()
        
        # self.ds = Model(CONF["ds.model_path"],   CONF["ds.N_FEATURES"],   CONF["ds.N_CONTEXT"],   CONF["ds.alphabet_path"],   CONF["ds.BEAM_WIDTH"])
        
        model_load_end = timer() - model_load_start
        logger.info('Loaded model in {:.3}s.'.format(model_load_end))

        # logger.info('Loading language model from files {} {}'.format(lm_path, trie_path))
        # lm_load_start = timer()        

        # self.ds.enableDecoderWithLM(alphabet_path, lm_path, trie_path, LM_ALPHA, LM_BETA)
        
        # lm_load_end = timer() - lm_load_start
        # logger.info('Loaded language model in {:.3}s.'.format(lm_load_end))

    def infer (self, file_path):
        fin = wave.open(file_path, 'rb')
        audio_length = fin.getnframes() * (1/16000)
        fin.close()
          
        inference_start = timer()
        
        inf = subprocess.run(["pocketsphinx_continuous"
                                ,"-hmm",CONF["sphinx.hmmpath"]
                                ,"-lm",CONF["sphinx.lmpath"]
                                ,"-dict",CONF["sphinx.dictpath"]
                                ,"-infile",file_path],stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

                                # "|","awk","-F","\'\n\'","\'{print $F[-1]}\'"
        inf = inf.split()

        inf = ' '.join( filter(lambda x : not x.startswith("INFO") and not x.startswith("-"), inf))

        print(inf)

        inference_end = timer() - inference_start
        
        logger.info('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length))
        logger.info('Inference_Time :: %0.3f' % (inference_end))
        logger.info('Audio_Length :: %0.3f' % (audio_length))
        logger.info('Model_Type :: Deepspeech')

        

        return (file_path,inf)




class RNNEngine(SpeechRecognizerBase):

    
    def __init__(self, *args, **kwargs):
        logger.info('Loading model from file {}'.format(model_path))
        model_load_start = timer()
        
        # self.ds = Model(CONF["ds.model_path"],   CONF["ds.N_FEATURES"],   CONF["ds.N_CONTEXT"],   CONF["ds.alphabet_path"],   CONF["ds.BEAM_WIDTH"])
        
        model_load_end = timer() - model_load_start
        logger.info('Loaded model in {:.3}s.'.format(model_load_end))


        model_end = final_model(input_dim=13,
                        filters=200,
                        kernel_size=11, 
                        conv_stride=2,
                        conv_border_mode='valid',
                        units=250,
                        activation='relu',
                        cell=GRU,
                        dropout_rate=1,
                        number_of_layers=2)

		

    def infer (self, audio_path):
	
        fin = wave.open(file_path, 'rb')
        audio_length = fin.getnframes() * (1/16000)
        fin.close()
          
        inference_start = timer()
		
		#model_end initialised in __init__
        input_to_softmax = model_end
		
		# load the train data
		data_gen = AudioGenerator(spectrogram=False)
		data_gen.load_train_data()
		
		#path to the HDF5 file
		model_path = 'res/speech-recognition-neural-network-master/model_end_new.hdf5'
		
		data_point = data_gen.normalize(data_gen.featurize(audio_path))
	   
		# obtain and decode the acoustic model's predictions
		input_to_softmax.load_weights(model_path)
		prediction = input_to_softmax.predict(np.expand_dims(data_point, axis=0))
		output_length = [input_to_softmax.output_length(data_point.shape[0])] 
		pred_ints = (K.eval(K.ctc_decode(
					prediction, output_length)[0][0])+1).flatten().tolist()
		
		
		
		inf = ''.join(int_sequence_to_text(pred_ints)
		
		
		#copied from above , i don't know what it does
		inf = inf.split()
		inf = ' '.join( filter(lambda x : not x.startswith("INFO") and not x.startswith("-"), inf))

        print(inf)

        inference_end = timer() - inference_start
        
        logger.info('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length))
        logger.info('Inference_Time :: %0.3f' % (inference_end))
        logger.info('Audio_Length :: %0.3f' % (audio_length))
        logger.info('Model_Type :: RNN')
		
		
		return (file_path, inf)
		
