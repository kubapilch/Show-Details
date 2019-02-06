import json

def save_data_to_file(data, data_type, show_name):
    """
    Save given data to a file with right file name
    """
    with open("{0}_{1}".format(data_type, show_name), "w") as f:
        json.dump(data, f)

def load_data_from_file(data_type, show_name):
    """
    Load data from given data type and show name, check if file ex
    """
    try:
        with open("{0}_{1}".format(data_type, show_name), "r") as f:
            # File exists, load and return data
            data = json.load(f)
            return data

    except FileNotFoundError:
        # File does not exist, ask user if he/she wants to download it
        raise Exception("File '{0}_{1}' does not exist, run the script with -l or -i flag to download the data first".format(data_type, show_name))
