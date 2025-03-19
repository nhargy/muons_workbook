import os
import configparser
from pathlib import Path

def load_config(filename='config.ini'):
    """
    Load the machine specific path to the project's raw data, 
    available in config.ini in the root directory.
    """
    project_root = str(Path(__file__).resolve()).split('/src')[0]
    config_path  = os.path.join(project_root, filename)
    config       = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')
    return config

LocalDataPath = load_config()["PATHS"]["LocalDataPath"]

