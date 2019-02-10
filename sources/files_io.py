import json
from collections import OrderedDict
import sys

def save_data_to_file(data, data_type, show_id):
    """
    Save given data to a file with right file name
    """    
    with open("{0}_{1}.json".format(data_type, show_id), "w") as f:
        json.dump(data, f)

def load_data_from_file(data_type, show_id):
    """
    Load data from given data type and show name, check if file ex
    """
    try:
        with open("{0}_{1}.json".format(data_type, show_id), "r") as f:
            # File exists, load and return data
            data = OrderedDict(json.load(f))
            return data

    except FileNotFoundError:
        # File does not exist, ask user if he/she wants to download it
        want_download = input("File '{0}_{1}.json' does not exist. Do you want to download it? (Y/N): ".format(data_type, show_id))
        
        # If yes return None and handle it in Show_graphs.py
        if want_download.upper() == "Y":
            return None
        
        # If not exit the program
        sys.exit()