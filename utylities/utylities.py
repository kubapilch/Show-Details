from collections import OrderedDict
import sys

def retrive_id_from_link(link):
    """
    Parse the link and retrives the id of a show
    """
    # Id of a show/movie in imdb is always after '/tt', if it is not there it is a wrong link
    if not "/tt" in link:
        sys.exit("Invalid link!")

    elements = link.split("/")

    # elements[2:] because first two elementes are from https
    for element in elements[2:]:
        if "tt" in element:
            # Id found retrive it and break the loop
            shwo_id = element[2:]
            break
    else:
        # Didn't find the id
        sys.exit("Invalid link!")

    return shwo_id


def normalize_data(data):
    """
    Normalize data to max value 10 and returns
    """
    # Top number in data pack
    top = max(data.values())

    data_noramlized = OrderedDict()

    # Normalize each episode
    for episode, review in data.items():
        data_noramlized[episode] = (review * 10)/top

    return data_noramlized

def prepare_data_for_presentation(data):
    """
    Prepare data for presentation, skip some episodes and change labels to ex. ["S1E14":8.6]
    """
    prepared_data = OrderedDict()

    # Loop through each season
    for season, episodes in enumerate(data.values(), 1):

        # Loop through each episode in a season
        for episode_number, episode_data in enumerate(episodes, 1):
            # If the episode data is 0 skip this episode, ex. episodes hasn't been aired yet or noone has rated it.
            if episode_data == 0:
                continue
            
            # Save data in a format that will be presented ex. 'S1E13':8.5
            prepared_data['S{0}E{1}'.format(season, episode_number)] = float(episode_data)

    return prepared_data
