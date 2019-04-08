import logging
import argparse
import sys
import os

def writePidFile():
    pid = str(os.getpid())
    f = open('../tmp/player.pid', 'w')
    f.write(pid)
    f.close()

writePidFile()

from app import app

parser = argparse.ArgumentParser(description='Offline Subtitle Generation for videos')
parser.add_argument('-d', '--debug', default=False, action='store_true', help='Run in debug mode.')
parser.add_argument('-p', '--path', help='Port number the interface runs on.')


for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

__args__ = parser.parse_args()

if __args__.debug:
    print(__args__)


if __args__.debug:
    logging.basicConfig(filename="../logs/player.log",filemode='w',level=logging.DEBUG,format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-2s [ %(thread)d ]@ %(message)s')
    # logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    # print(logging.getLogger().handlers)
else:
    logging.basicConfig(level=logging.INFO,format='%(asctime)s %(name)s +%(lineno)s: %(levelname)-2s %(message)s')


logger = logging.getLogger("MainLogger")
logger.debug("Started")

app.main()