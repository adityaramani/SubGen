!sudo get install git 
!sudo get install automake
!sudo get install libtool
!sudo get install bison
!sudo get install python-dev
!sudo get install swig
!sudo get install make 
!sudo get install pkg-config




!git clone https://github.com/cmusphinx/sphinxbase.git
!cd sphinxbase
!./autogen.sh 
!make
!sudo make install

!cd..

!git clone https://github.com/cmusphinx/pocketsphinx.git
!cd pocketsphinx
!./autogen.sh 
!make
!sudo make install

!cd..

!git clone https://github.com/cmusphinx/sphinxtrain.git
!cd sphinxtrain
!./autogen.sh 
!make
!sudo make install

Copy en-in file into pocket sphinx/model file
!cp -a /usr/local/share/pocketsphinx/model/en-us/en-us .

!cp -a /usr/local/share/pocketsphinx/model/en-us/cmudict-en-us.dict .
!cp -a /usr/local/share/pocketsphinx/model/en-us/en-us.lm.bin .

/*make transcripts in format
<s> data </s> (filename)


make fileids in formt
filename1
filename2*/

!cd wav
!sphinx_fe -argfile en-us/feat.params \
        -samprate 16000 -c arctic20.fileids \
       -di . -do . -ei wav -eo mfc -mswav yes
 
!cp /usr/local/libexec/sphinxtrain/bw .
!cp /usr/local/libexec/sphinxtrain/map_adapt .
!cp /usr/local/libexec/sphinxtrain/mk_s2sendump .

! ./bw \
 -hmmdir en-in \
 -moddeffn en-in/mdef \
 -ts2cbfn .cont. \
  -feat 1s_c_d_dd \
  -lda en-in/feature_transform \
  -cmn current \
  -agc none \
  -dictfn en_in.dic \
  -ctlfn indianeng.fileids \
  -lsnfn indianeng.transcription \
  -accumdir .



!cp -a en-in en-in-adapt
!./map_adapt \
     -moddeffn en-in/mdef.txt \
     -ts2cbfn .cont. \
     -meanfn en-in/means \
     -varfn en-in/variances \
     -mixwfn en-in/mixture_weights \
     -tmatfn en-in/transition_matrices \
     -accumdir . \
     -mapmeanfn en-in-adapt/means \
     -mapvarfn en-in-adapt/variances \
     -mapmixwfn en-in-adapt/mixture_weights \
     -maptmatfn en-in-adapt/transition_matrices
     
     
!./mk_s2sendump \
    -pocketsphinx yes \
    -moddeffn en-us-adapt/mdef.txt \
    -mixwfn en-us-adapt/mixture_weights \
    -sendumpfn en-us-adapt/sendump

!pocketsphinx_continuous -hmm en-in-adapt -lm en-us.lm.bin -dict en_in.dic -infile ASF001-EN-ST01U13.wav
