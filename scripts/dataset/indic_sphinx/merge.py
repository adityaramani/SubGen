trans = open("/Users/aramani/Documents/project/scripts/dataset/indic_sphinx/etc/indic_test.transcription")
fileids = open("/Users/aramani/Documents/project/scripts/dataset/indic_sphinx/etc/indic_test.fileids")


for t in trans:
    l  = next(fileids)
    print(t.strip() +' (' + l.strip() +' )')
 