base_path = "/media/aditya/AE02DDA702DD7535/Users/Aditya/Downloads/IndicTTS/extracted/"
genders  = ['male', 'female']


import os
import re

full_pattern = re.compile('[^a-zA-Z ]')

def re_replace(string):
    return re.sub(full_pattern, '', string)



for gender in genders:
    path  = base_path+gender
    dirs =  next(os.walk(path))[1]
    for dir in dirs:
        p = path+ '/' + dir
        if gender == 'male' and 'manipuri' in dir:
            continue
        folder =  next(os.walk(p))[1][0]
        data_file = p+'/'+folder+'/txt.done.data'
        tmp = p + '/' + folder +'/wav/'
        with open(data_file,'rb') as fp:
            
                for line in fp:
                        try:
                                line = line.decode('utf-8')
                                data = line[1: -2].split('"')
                                file_name = data[0].strip()
                                transcript = data[1].strip()
                                full_path =tmp + file_name+'.wav'
                                size = os.stat(full_path).st_size
                                transcript = re_replace(transcript.lower())
                                if transcript == '':
                                        continue
                                else:
                                        print(full_path,size ,transcript, sep=',')
                        except:
                                continue
