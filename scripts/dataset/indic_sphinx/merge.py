trans = open("/home/aditya/Desktop/indic_train.transcription")
fileids = open("/home/aditya/Desktop/indic_train.fileids")


for t in trans:
    l  = next(fileids)
    print(t.strip() +' (' + l.strip() +' )')
 
