import json


def save_data_to_file(data, data_type, show_name):
    """
    Save given data to a file with right file name
    """

    with open("{0}_{1}".format(data_type, show_name), "w") as f:
        json.dump(data, f)
                    