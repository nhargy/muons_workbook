import os
import configparser
from pathlib import Path

def get_project_root():
    """
    Get the local path to the project root.
    """
    project_root = str(Path(__file__).resolve()).split('/src')[0]
    return project_root


def load_config(filename='config.ini'):
    """
    Load the machine specific path to the project's raw data, 
    available in config.ini in the root directory.
    """
    project_root = get_project_root()
    config_path  = os.path.join(project_root, filename)
    config       = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')
    return config


ProjectRoot   = get_project_root()
DataPath      = load_config()["PATHS"]["DataPath"]
LocalDataPath = os.path.join(ProjectRoot, "lcd")
OutPath       = os.path.join(ProjectRoot, "out") 
PlotsPath     = os.path.join(ProjectRoot, "plots") 
ScriptsPath   = os.path.join(ProjectRoot, "scripts") 
TestsPath     = os.path.join(ProjectRoot, "tests")
PagesPath     = os.path.join(ProjectRoot, "pages")
StudiesPath   = os.path.join(ProjectRoot, "studies") 
