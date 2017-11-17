import platform

from os import path

LATEST_VERSION = '0a06'

if platform == 'Windows':
    BIN = 'NDC.EXE'
else:
    BIN = 'ndc'

BIN_PATH = path.join(path.dirname(__file__), LATEST_VERSION, BIN)
