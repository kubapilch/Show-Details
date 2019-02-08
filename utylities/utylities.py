from collections import OrderedDict

def retrive_id_from_link(link):
    """
    Parse the link and retrives the id of a show
    """
    # Id of a show/movie in imdb is always after '/tt', if it is not there it is a wrong link
    if not "/tt" in link:
        raise Exception("Invalid link!")

    elements = link.split("/")

    # elements[2:] because first two elementes are from https
    for element in elements[2:]:
        if "tt" in element:
            # Id found retrive it and break the loop
            id = element[2:]
            break
    else:
        # Didn't find the id
        raise Exception("Invalid link!")

    return id


def normalize_data(data):
    """
    Normalize data to max value 10 and returns
    """
    # Top number in data pack
    top = 0

    # Find top 
    for season in data.values():
        top = max(season) if top < max(season) else top

    data_noramlized = OrderedDict()

    # Loop through seasons
    for season, votes in zip(data.keys(), data.values()):

        # Loop through each episode and normalize the data
        for vote in votes:
            new_vote = (vote*10)/top

            # Make sure that data_normalize[season] exist and append
            # if not create and assign a list
            if season in data_noramlized.keys():
                data_noramlized[season].append(new_vote)
            else:
                data_noramlized[season] = [new_vote]

    return data_noramlized

def prepare_data_for_presentation(data):
    prepared_data = OrderedDict()

    # Loop through each season
    for season, episodes in enumerate(data.values(), 1):

        # Loop through each episode in a season
        for episode_number, episode_review in enumerate(episodes, 1):
            if episode_review == 0:
                continue
            
            # Save data in a format that will be presented ex. 'S1E13':8.5
            prepared_data['S{0}E{1}'.format(season, episode_number)] = float(episode_review)

    return prepared_data
