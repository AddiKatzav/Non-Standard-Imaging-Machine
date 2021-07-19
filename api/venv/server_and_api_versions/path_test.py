"""
This module deals with getting relative path to ScanConfigs, loading the given config_yaml_file.
    config_yaml_file is a yaml file which holds all the arguments for the scan.
    the config_yaml_file divided to several objects (form objects):
    1)  "text_box"
    2)  "radio_button"
    3) "checkbox"
"""


from pathlib import Path
import yaml

current_path = Path().absolute()  # The current application path
config_yaml_file = "basic_cfg.yml"


#The desired config file you want to load,Located in ScanConfigs

def getPathScanConfigFile(current_path,config_yaml_file,directory="ScanConfigs"):
    path_of_file = getPathFile(current_path, "ScanConfigs")
    path_of_config_file = path_of_file / config_yaml_file
    return path_of_config_file

def getPathFile(current_path,directory):
    path_of_main_dir = current_path.parents[1]  #Going to Flask_React_Merged
    path_of_file = Path.joinpath(path_of_main_dir, directory)
    return path_of_file



"""path_config_file = getPathScanConfigFile(current_path,config_yaml_file)
print("The path to config file is :", path_config_file)
config_yaml_file = open(path_config_file, "r")
#DONT FORGET TO CLOSE config_yaml_file!!!
parsed_config_yaml_file = yaml.load(config_yaml_file, Loader=yaml.FullLoader)
print(parsed_config_yaml_file["text_box"])
print(parsed_config_yaml_file["radio_button"])
print(parsed_config_yaml_file["checkbox"])


config_yaml_file.close()
"""