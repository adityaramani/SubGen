import csv
from random import shuffle
reader = csv.reader(open('data.csv'), delimiter = ',')

all_line = []

for line in reader:
    all_line.append(line)


shuffle(all_line)

overall_size = 50000

train_size = int(0.7 * overall_size)

dev_size = int(0.2 * overall_size)

val_size = int(0.1 *overall_size )


header = ["wav_filename","wav_filesize","transcript"]


with open('train.csv' ,'w') as fp:
    writer = csv.writer(fp,delimiter=',')
    writer.writerow(header)
    for i in range(train_size):
        writer.writerow(all_line[i])



with open('dev.csv' ,'w') as fp:
    writer = csv.writer(fp,delimiter=',')
    writer.writerow(header)
    for i in range(train_size,train_size+dev_size):
        writer.writerow(all_line[i])

with open('val.csv' ,'w') as fp:
    writer = csv.writer(fp,delimiter=',')
    writer.writerow(header)
    for i in range(val_size, 0 ,-1):
        writer.writerow(all_line[-i])

           
