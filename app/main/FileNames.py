import sys
import os

def get_base_path():
    if getattr(sys, 'frozen', False):  # Running in PyInstaller bundle
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

saveFile = "Save"
discardFile = "Discard"
# CONFIG_PATH = os.getcwd() + '\\app\\main\\config.json'
# reliable path in bundled apps
CONFIG_PATH = os.path.join(get_base_path(), 'config.json')
