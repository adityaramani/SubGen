import logging
import argparse
import sys
from external import extract_audio,app,app

parser = argparse.ArgumentParser(description='Offline Subtitle Generation for videos')
parser.add_argument('-d', '--debug', default=False, action='store_true', help='Run in debug mode.')
parser.add_argument('-p', '--path', help='Port number the interface runs on.', required = True)


for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

__args__ = parser.parse_args()

if __args__.debug:
    print(__args__)


if __args__.debug:
    logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-2s [%(process)d] %(message)s')
    # logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    # print(logging.getLogger().handlers)
else:
    logging.basicConfig(level=logging.INFO,format='%(asctime)s %(name)s +%(lineno)s: %(levelname)-2s %(message)s')


logger = logging.getLogger("MainLogger")
logger.debug("Started")

app.main()



# extract_audio(__args__.path)


# import vlc
# i=vlc.Instance( '--fullscreen')

# p=i.media_player_new()
# m=i.media_new('file:////Users/aramani/Downloads/France vs Argentina 4-3 All Goals and Extended Highlights w- English Commentary (World Cup) 2018 HD.mp4')
# m.get_mrl()
# p.set_media(m)

# if sys.platform == "darwin":
#     from PyQt5 import QtWidgets
#     # from PyQt5 import QtGui
#     import sys

#     vlcApp =QtWidgets.QApplication(sys.argv)
#     vlcWidget = QtWidgets.QFrame()
#     vlcWidget.resize(700,700)
#     vlcWidget.show()
#     p.set_nsobject(int(vlcWidget.winId()))

# p.play()
