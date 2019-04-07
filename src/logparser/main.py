
import argparse
import logging
import json
import process.logprocessor as logprocessor
import os
import pathlib
import time


parser = argparse.ArgumentParser(description='QOSPROC Log Parser and Publisher')
parser.add_argument('-d', '--debug', default=False, action='store_true', help='Run in debug mode.')
parser.add_argument('-p', '--work-dir', required=True, help='Path to log file to parse.')
parser.add_argument('-r', '--report-url', help='Url to where the parsed data should be published')
parser.add_argument('-s', '--schema', required=True,help='Json file that contains the keys that must be parsed from the log')
parser.add_argument('-f', '--write-schema', default=False, action='store_true',help='Flag that controls if schema should be created or not')


for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

__args__ = parser.parse_args()

if __args__.debug:
    print(__args__)
    logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-2s [%(process)d] %(message)s')
    
else:
    logging.basicConfig(level=logging.INFO,format='%(asctime)s %(name)s +%(lineno)s: %(levelname)-2s %(message)s')

logger = logging.getLogger("MainLogger")

schema = json.load(open(__args__.schema, 'r'))



if __args__.write_schema :
    for key in schema:
        rp.write_schema(key, schema[key]['csv_path'])
        logger.info("writing schema for key = " + key)
    exit(0)


if not os.path.exists('work/processed.txt'):
    pathlib.Path('./work').mkdir(exist_ok=True)
    with open('work/processed.txt', 'w'): pass



def find_processed_files():
    with open('work/processed.txt', 'r') as fp:
        lines = fp.readlines()
    return lines

starttime=time.time()

writter = open("work/output.json", 'a')

lp  = logprocessor.LogProcessor(json.load(open(__args__.schema)), writter.write)

while True:

    files_work_dir  =  map(lambda x: x.strip(), next(os.walk(__args__.work_dir))[2])
    qosproc_log_files  = set(filter( lambda x: 'log' in x, files_work_dir))
    
    processed_files = set( map(lambda x : x.strip(),find_processed_files()))
    logger.info("Processed Files = " + str(processed_files))
    to_be_processed = sorted( qosproc_log_files  - processed_files, key = str.lower)
    logger.info("To be processed = " + str(to_be_processed))

    op = open('work/processed.txt', 'a')
    
    for log_file in to_be_processed:
        logger.info("Parsing  [" +  log_file + " ] ")
        with open(__args__.work_dir+'/'+ log_file) as fp:
            for line in fp:
                lp.read_line(line)

        op.write(log_file+'\n')

    op.close()
    break


writter.close()