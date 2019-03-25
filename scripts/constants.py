
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



# model_path = "/home/aditya/Documents/project/indian_model/1/exported/output_graph.pb"
model_path = "/home/aditya/Documents/project/indian_model/prebuilt/deepspeech-0.4.1-models/models/output_graph.pbmm"
alphabet_path = "/home/aditya/Documents/project/indian_model/prebuilt/deepspeech-0.4.1-models/models/alphabet.txt"
lm_path = '/home/aditya/Documents/project/indian_model/prebuilt/deepspeech-0.4.1-models/models/lm.binary'
trie_path = "/home/aditya/Documents/project/indian_model/prebuilt/deepspeech-0.4.1-models/models/trie"

